#!/usr/bin/env python3
"""Local AIDLC artifact operations. This tool never grants approvals or deploys."""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
CHANGE_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
STAGE_FILES = (("intent", "intent.md"), ("spec", "spec.md"), ("plan", "plan.md"),
               ("evidence", "evidence.md"), ("review", "review.md"))
NEXT_STAGE = {"": "intent", "intent": "design", "spec": "plan", "plan": "build",
              "evidence": "review", "review": "done"}
SKILLS = ("init", "intent", "design", "plan", "build", "verify", "review", "fix", "onboard", "learn",
          "ticket", "spike", "ship", "handoff", "resume", "ideate")
MANUAL_SKILLS = frozenset(("handoff", "resume", "ideate"))
SKILL_DIRECTORIES = ("aidlc",) + tuple("aidlc-" + name for name in SKILLS)
CODE_SUFFIXES = frozenset((
    ".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".java", ".kt", ".cs", ".rb", ".php", ".rs",
    ".swift", ".c", ".cc", ".cpp", ".h", ".hpp", ".scala", ".sql", ".tf", ".vue", ".svelte",
))
SKIP_DIRECTORIES = frozenset((
    ".git", ".hg", ".svn", "node_modules", "vendor", "dist", "build", "target", ".venv", "venv",
    "__pycache__", ".claude", ".omp", ".aidlc", "changes", "docs",
))
BROWNFIELD_CODE_FILES = 10
BROWNFIELD_COMMITS = 20
REQUIRED_ASSETS = (
    "GOALS.md", "IMPLEMENTATION_PLAN.md", "FUTURE_WORK.md", "README.md", "LICENSE",
    "AGENTS.md", "CLAUDE.md", "REVIEW.md", "docs/COVERAGE.md", "docs/DEPENDENCIES.md",
    "docs/PREREQUISITES.md", "docs/ARTIFACTS.md", "docs/VERIFICATION.md",
    "docs/COMPATIBILITY.md", "docs/MEASURES.md", "docs/PLUGINS.md",
    "docs/WORKFLOW.md", "docs/USAGE.md", "docs/REFERENCE.md",
    ".omp/AGENTS.md", ".omp/RULES.md", ".omp/config.yml", ".worktreeinclude",
    ".omp/hooks/pre/aidlc-guards.ts", ".omp/agents/aidlc-verifier.md", ".omp/agents/aidlc-repo-scout.md",
    ".vscode/settings.json", ".vscode/extensions.json",
    ".mcp.json", ".claude/settings.json",
    ".claude/hooks/check-package.sh", ".claude/hooks/project-mode.sh",
    ".claude/hooks/protect-tests.sh", ".claude/hooks/worktree-create.sh",
    ".claude/rules/package-maintenance.md",
    ".claude/skills/aidlc-review/references/review-options.md",
    ".claude/skills/aidlc-intent/templates/intent.md",
    ".claude/skills/aidlc-design/templates/spec.md",
    ".claude/skills/aidlc-plan/templates/plan.md",
    ".claude/skills/aidlc-review/templates/review.md",
    ".claude/skills/aidlc-fix/templates/evidence.md",
    ".claude/skills/aidlc-handoff/templates/handoff.md",
    ".claude/skills/aidlc-learn/templates/learning.md",
    ".claude/skills/aidlc-ideate/templates/ideation.md",
    ".claude/skills/aidlc-spike/templates/spike.md",
    ".claude/skills/aidlc-ship/templates/pr-body.md",
    ".claude/skills/aidlc-init/templates/agent.md",
    "docs/adr/README.md", "docs/adr/template.md",
    "docs/incidents/README.md", "docs/incidents/template.md",
    "docs/security/README.md", "docs/security/threat-model-template.md",
    "docs/references/README.md", "docs/references/libraries.md",
    "docs/platform/README.md", "docs/platform/platform.md",
    "templates/conventions/CONVENTIONS.md", "templates/conventions/.editorconfig",
    "templates/conventions/.pre-commit-config.yaml", "templates/conventions/ruff.toml", "templates/conventions/biome.json",
    ".claude/agents/aidlc-verifier.md", ".claude/agents/aidlc-repo-scout.md",
    ".claude/agents/aidlc-design-reviewer.md", ".claude/agents/aidlc-threat-modeler.md",
    ".claude/agents/aidlc-test-critic.md",
    ".omp/agents/aidlc-design-reviewer.md", ".omp/agents/aidlc-threat-modeler.md",
    ".omp/agents/aidlc-test-critic.md",
    "docs/vendor/aws-aidlc/NOTICE.md",
    "docs/vendor/ecc/manifest.json", "docs/vendor/ecc/LICENSE",
    "docs/vendor/anthropic-skills/manifest.json", "docs/vendor/anthropic-skills/NOTICE.md",
    "mcp-configs/ecc.mcp-servers.example.json",
) + tuple(".claude/skills/{}/SKILL.md".format(name) for name in SKILL_DIRECTORIES)


def new_change(root, change_id):
    if not CHANGE_ID.fullmatch(change_id):
        raise ValueError("change-id must be lowercase ASCII words/digits separated by single hyphens")
    if not root.is_dir():
        raise ValueError("target root must be an existing directory")
    # Read the template before creating anything; failure must not leave an empty change.
    # The plugin build lays skills out under skills/ instead of .claude/skills/.
    template = PACKAGE_ROOT / ".claude/skills/aidlc-intent/templates/intent.md"
    if not template.is_file():
        template = PACKAGE_ROOT / "skills/aidlc-intent/templates/intent.md"
    content = template.read_text(encoding="utf-8")
    content = content.replace("{{change_id}}", change_id)
    changes = root / "changes"
    if changes.is_symlink():
        raise ValueError("refusing a symlinked changes directory")
    changes.mkdir(exist_ok=True)
    destination = changes / change_id
    # Exclusive creation protects existing work, including an existing symlink.
    destination.mkdir()
    intent = destination / "intent.md"
    try:
        with intent.open("x", encoding="utf-8") as stream:
            stream.write(content)
    except OSError:
        # Only remove an empty directory created by this invocation.
        try:
            destination.rmdir()
        except OSError:
            pass
        raise
    print("Created draft: {}".format(intent))
    print("Refine the intent with the engineer, then use aidlc-design for the spec.")
    print("No approval, commit, push, or deployment was performed.")


VENDOR_MANIFESTS = ("docs/vendor/ecc/manifest.json", "docs/vendor/anthropic-skills/manifest.json")


def ecc_inventory():
    """Read every pinned import inventory without discovering arbitrary skill files."""
    files = []
    modes = {}
    for relative in VENDOR_MANIFESTS:
        manifest = PACKAGE_ROOT / relative
        for component in (manifest, *manifest.parents):
            if component == PACKAGE_ROOT:
                break
            if component.is_symlink():
                raise ValueError("refusing a symlinked vendor manifest: {}".format(manifest))
        data = json.loads(manifest.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("schema_version") != 1:
            raise ValueError("unsupported vendor manifest schema: {}".format(relative))
        skills = data.get("skills")
        if not isinstance(skills, list) or not skills:
            raise ValueError("vendor manifest must declare its imported skills: {}".format(relative))
        for skill in skills:
            if not isinstance(skill, dict):
                raise ValueError("invalid vendor skill entry in {}".format(relative))
            name, manual = skill.get("name"), skill.get("manual")
            if (not isinstance(name, str) or not CHANGE_ID.fullmatch(name)
                    or name.startswith("aidlc-") or name in modes or not isinstance(manual, bool)):
                raise ValueError("invalid or duplicate vendor skill name/invocation mode: {!r}".format(name))
            resources = skill.get("files")
            if not isinstance(resources, list) or not resources:
                raise ValueError("vendor skill has no declared resources: {}".format(name))
            prefix = ".claude/skills/{}/".format(name)
            paths = []
            for resource in resources:
                path = resource.get("path") if isinstance(resource, dict) else None
                if (not isinstance(path, str) or not path.startswith(prefix)
                        or "\\" in path or ".." in Path(path).parts or path != Path(path).as_posix()):
                    raise ValueError("invalid vendor resource path: {!r}".format(path))
                paths.append(path)
            if prefix + "SKILL.md" not in paths:
                raise ValueError("vendor skill is missing its declared entrypoint: {}".format(name))
            files.extend(paths)
            modes[name] = manual
    if len(files) != len(set(files)):
        raise ValueError("duplicate vendor resource paths")
    return tuple(files), modes


def local_links(text):
    # Fenced examples describe a consumer's files, not package dependencies.
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if (marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence)
                    and not marker[2].strip()):
                fence = None
            continue
        if marker:
            fence = marker[1]
            continue
        for target in re.findall(r"\[[^\]\n]+\]\(([^)\s]+)\)", line):
            parts = urlsplit(target)
            if not parts.scheme and not parts.netloc and parts.path:
                yield target, unquote(parts.path)


def first_content_line(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            return line.strip()
    return ""


def check_instruction_files():
    """AGENTS.md is canonical; CLAUDE.md and .omp/AGENTS.md import it instead of duplicating it."""
    canonical = PACKAGE_ROOT / "AGENTS.md"
    if canonical.is_symlink() or not canonical.is_file():
        raise ValueError("AGENTS.md must be a regular file holding the shared instructions")
    for relative, expected in (("CLAUDE.md", "@AGENTS.md"), (".omp/AGENTS.md", "@../AGENTS.md")):
        file = PACKAGE_ROOT / relative
        if file.is_symlink() or not file.is_file():
            raise ValueError("{} must be a regular file".format(relative))
        if first_content_line(file) != expected:
            raise ValueError("{} must start by importing the shared instructions with {}".format(relative, expected))


def project_mode(root):
    """Classify the target as greenfield or brownfield; an explicit .aidlc/mode file wins."""
    override = root / ".aidlc" / "mode"
    if override.is_file():
        value = override.read_text(encoding="utf-8").strip()
        if value not in ("greenfield", "brownfield"):
            raise ValueError(".aidlc/mode must contain greenfield or brownfield")
        return value, ["declared in .aidlc/mode"]
    code_files = 0
    for directory, subdirectories, files in os.walk(root):
        subdirectories[:] = sorted(d for d in subdirectories if d not in SKIP_DIRECTORIES and not d.startswith("."))
        code_files += sum(1 for f in files if Path(f).suffix in CODE_SUFFIXES)
        if code_files >= BROWNFIELD_CODE_FILES:
            break
    commits = 0
    if shutil.which("git"):
        result = subprocess.run(["git", "-C", str(root), "rev-list", "--count", "HEAD"],
                                capture_output=True, text=True, timeout=10, check=False)
        if result.returncode == 0 and result.stdout.strip().isdigit():
            commits = int(result.stdout.strip())
    reasons = ["{} code files (threshold {})".format(
        "{}+".format(code_files) if code_files >= BROWNFIELD_CODE_FILES else code_files, BROWNFIELD_CODE_FILES),
        "{} commits (threshold {})".format(commits, BROWNFIELD_COMMITS)]
    brownfield = code_files >= BROWNFIELD_CODE_FILES or commits >= BROWNFIELD_COMMITS
    return ("brownfield" if brownfield else "greenfield"), reasons


def print_mode(root):
    mode, reasons = project_mode(root)
    print("AIDLC project mode: {} — {}".format(mode, "; ".join(reasons)))
    if mode == "brownfield":
        # Plugin hooks receive CLAUDE_PLUGIN_ROOT; the skill is then namespaced.
        prefix = "/lbvs-aidlc:" if os.environ.get("CLAUDE_PLUGIN_ROOT") else "/"
        print("Brownfield: run {}aidlc-onboard before the first change unless conventions are already recorded.".format(prefix))
    print("Override with .aidlc/mode containing greenfield or brownfield.")


CONVENTION_FILES = (".editorconfig", ".pre-commit-config.yaml", "ruff.toml", "biome.json", "CONVENTIONS.md")
# Files that mean the repository already owns that concern; the default is then not offered.
CONVENTION_EQUIVALENTS = {
    ".pre-commit-config.yaml": (".pre-commit-config.yaml", ".pre-commit-config.yml", "lefthook.yml", ".husky"),
    "ruff.toml": ("ruff.toml", ".ruff.toml", "pyproject.toml", "setup.cfg", ".flake8", "tox.ini"),
    "biome.json": ("biome.json", "biome.jsonc", ".eslintrc", ".eslintrc.js", ".eslintrc.cjs", ".eslintrc.json",
                   "eslint.config.js", "eslint.config.mjs", ".prettierrc", "prettier.config.js"),
    ".editorconfig": (".editorconfig",),
    "CONVENTIONS.md": ("CONVENTIONS.md", "CONTRIBUTING.md"),
}


def conventions(root, apply=False):
    """Report repository conventions versus the package defaults; --apply copies only missing defaults."""
    source_dir = PACKAGE_ROOT / "templates" / "conventions"
    mode, _ = project_mode(root)
    print("Project mode: {}. Defaults come from templates/conventions/; existing repository files always win.".format(mode))
    copied = []
    for name in CONVENTION_FILES:
        existing = [candidate for candidate in CONVENTION_EQUIVALENTS[name] if (root / candidate).exists()]
        if existing:
            print("  {:<26} repository owns it: {}".format(name, ", ".join(existing)))
            continue
        if apply:
            target = root / name
            with (source_dir / name).open("rb") as src, target.open("xb") as dst:
                shutil.copyfileobj(src, dst)
            copied.append(name)
            print("  {:<26} copied default".format(name))
        else:
            print("  {:<26} missing — default available ({} to copy)".format(name, "`conventions --apply`"))
    if apply:
        print("Copied {} file(s); nothing was overwritten. Review the diff, pin hook revisions, then `pre-commit install`.".format(len(copied)))
    elif mode == "greenfield":
        print("Greenfield: run `python3 scripts/aidlc.py conventions --apply` to adopt the defaults, or record your own in CLAUDE.md.")
    else:
        print("Brownfield: keep the repository's conventions; aidlc-onboard records them in CLAUDE.md. Copy a default only where none exists.")
    return 0


def git_out(root, *args):
    result = subprocess.run(("git", "-C", str(root)) + args, capture_output=True, text=True,
                            timeout=15, check=False)
    return result.stdout.strip() if result.returncode == 0 else ""


def change_stages(root):
    """Report each change directory with the stage artifacts actually present."""
    changes = root / "changes"
    if not changes.is_dir() or changes.is_symlink():
        return []
    rows = []
    for directory in sorted(p for p in changes.iterdir() if p.is_dir() and not p.is_symlink()):
        present = [name for name, file in STAGE_FILES if (directory / file).is_file()]
        handoffs = directory / "handoffs"
        rows.append({
            "id": directory.name,
            "present": present,
            "reached": present[-1] if present else "",
            "handoffs": sum(1 for p in handoffs.glob("*.md")) if handoffs.is_dir() else 0,
        })
    return rows


def branch_change_id(root):
    """Recover the change ID from the branch name, including EnterWorktree's sanitised form."""
    branch = git_out(root, "rev-parse", "--abbrev-ref", "HEAD")
    for prefix in ("aidlc/", "aidlc+", "worktree-aidlc/", "worktree-aidlc+"):
        if branch.startswith(prefix):
            candidate = branch[len(prefix):]
            if CHANGE_ID.fullmatch(candidate):
                return candidate, "branch " + branch
    return None, None


def current_change(root):
    """Resolve the change in play without the engineer repeating its ID."""
    change_id, source = branch_change_id(root)
    if change_id:
        return change_id, source
    pointer = root / ".aidlc" / "current"
    if pointer.is_file():
        candidate = pointer.read_text(encoding="utf-8").strip()
        if CHANGE_ID.fullmatch(candidate):
            return candidate, ".aidlc/current"
    open_changes = [row["id"] for row in change_stages(root) if row["reached"] != "review"]
    if len(open_changes) == 1:
        return open_changes[0], "the only change without review.md"
    return None, None


def print_status(root):
    rows = change_stages(root)
    change_id, source = current_change(root)
    if not rows:
        print("No changes yet. Start one with /aidlc <change-id>.")
    for row in rows:
        marker = "*" if row["id"] == change_id else " "
        missing = [name for name, _ in STAGE_FILES if name not in row["present"]]
        print("{} {:<28} reached: {:<9} next: {:<7} have: {:<34} missing: {}{}".format(
            marker, row["id"], row["reached"] or "-", NEXT_STAGE.get(row["reached"], "?"),
            ",".join(row["present"]) or "-", ",".join(missing) or "-",
            "  handoffs: {}".format(row["handoffs"]) if row["handoffs"] else ""))
    if change_id:
        print("Current change: {} (from {}).".format(change_id, source))
    else:
        print("Current change: none resolved; name one or start /aidlc <change-id>.")
    print("Presence of a file is not proof the stage is complete; read the artifact.")
    return 0


def print_current(root):
    change_id, source = current_change(root)
    if not change_id:
        print("No current change resolved. Ask the engineer for the ID or start /aidlc <change-id>.")
        return 1
    print("{}\t{}".format(change_id, source))
    return 0


def worktree_path(root, name):
    """Create or reuse a descriptive worktree; replaces Claude Code's default naming."""
    slug = re.sub(r"[^A-Za-z0-9._+/-]", "-", name).strip("-/")
    if not slug or ".." in slug.split("/"):
        raise ValueError("unusable worktree name: {!r}".format(name))
    match = re.fullmatch(r"aidlc[+/](.+)", slug)
    change_id = match.group(1) if match else slug
    # An explicit aidlc prefix, or a name that is already a change under changes/, gets the
    # descriptive branch; anything else keeps Claude Code's default shape.
    if match or (CHANGE_ID.fullmatch(change_id) and (root / "changes" / change_id).is_dir()):
        branch, directory = "aidlc/" + change_id, "aidlc+" + change_id
    else:
        branch, directory = "worktree-" + slug, slug.replace("/", "+")
    destination = root / ".claude" / "worktrees" / directory
    if destination.is_dir():
        return destination
    existing = git_out(root, "rev-parse", "--verify", "--quiet", "refs/heads/" + branch)
    add = ["worktree", "add", str(destination)]
    add += [branch] if existing else ["-b", branch, "HEAD"]
    result = subprocess.run(["git", "-C", str(root)] + add, capture_output=True, text=True,
                            timeout=120, check=False)
    if result.returncode:
        raise ValueError("git worktree add failed: {}".format(result.stderr.strip() or result.returncode))
    # This hook replaces the default behaviour, so .worktreeinclude is ours to honour.
    include = root / ".worktreeinclude"
    if include.is_file():
        patterns = [line.strip() for line in include.read_text(encoding="utf-8").splitlines()
                    if line.strip() and not line.startswith("#")]
        for pattern in patterns:
            listed = git_out(root, "ls-files", "--others", "--ignored", "--exclude-standard", "--", pattern)
            for relative in (line for line in listed.splitlines() if line):
                source, target = root / relative, destination / relative
                if source.is_file() and not source.is_symlink() and not target.exists():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)
    return destination


def create_worktree():
    """WorktreeCreate hook: read the requested name on stdin, print the worktree path."""
    payload = json.loads(sys.stdin.read() or "{}")
    name = payload.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("WorktreeCreate input has no usable name")
    root = Path(payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or Path.cwd())
    top = git_out(root, "rev-parse", "--show-toplevel")
    if not top:
        raise ValueError("worktree creation needs a git repository")
    destination = worktree_path(Path(top), name)
    print("AIDLC worktree: {} on branch {}".format(
        destination, git_out(destination, "rev-parse", "--abbrev-ref", "HEAD")), file=sys.stderr)
    print(destination)
    return 0


def package(destination):
    """Export declared resources and their local links; never overlay a repository."""
    destination = destination.absolute()
    if destination.exists() or destination.is_symlink():
        raise FileExistsError("package destination already exists: {}".format(destination))
    if not destination.parent.is_dir():
        raise ValueError("package destination parent must be an existing directory")
    check_instruction_files()
    ecc_files, ecc_modes = ecc_inventory()
    seeds = set(REQUIRED_ASSETS + ecc_files) | {"scripts/aidlc.py", ".gitignore"}
    skill_directories = set(SKILL_DIRECTORIES) | set(ecc_modes)
    pending = [PACKAGE_ROOT / relative for relative in sorted(seeds)]
    files = set()
    directories = set()
    while pending:
        source = pending.pop()
        # Reject symlink resources rather than copying their targets into a release.
        for component in (source, *source.parents):
            if component == PACKAGE_ROOT:
                break
            if component.is_symlink():
                raise ValueError("refusing a symlinked package resource: {}".format(source))
        try:
            relative = source.resolve().relative_to(PACKAGE_ROOT)
        except ValueError:
            raise ValueError("package link escapes source root: {}".format(source)) from None
        parts = relative.parts
        allowed = (
            not parts
            or relative.as_posix() in seeds
            or (parts[0] == "docs" and not any(part.startswith(".") for part in parts)
                and (len(parts) == 1 or parts[1] not in ("solutions", "ideation")))
            or parts[:2] == ("templates", "conventions")
            or (parts[:2] == (".claude", "skills") and
                (len(parts) == 2 or parts[2] in skill_directories))
        )
        if not allowed:
            raise ValueError("not a distributable package resource: {}".format(relative))
        if relative in files or relative in directories:
            continue
        if source.is_dir():
            if relative.as_posix() in seeds:
                raise ValueError("required package asset is not a file: {}".format(relative))
            # A navigation link does not authorise copying every file in a directory.
            directories.add(relative)
            continue
        if not source.is_file():
            raise ValueError("missing package resource: {}".format(relative))
        files.add(relative)
        if source.suffix == ".md":
            pending.extend(source.parent / path for _, path in local_links(source.read_text(encoding="utf-8")))
    # Reserve the new destination exclusively, including against dangling symlinks.
    destination.mkdir()
    try:
        for relative in sorted(directories):
            (destination / relative).mkdir(parents=True, exist_ok=True)
        for relative in sorted(files):
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with (PACKAGE_ROOT / relative).open("rb") as source, target.open("xb") as output:
                shutil.copyfileobj(source, output)
    except OSError as error:
        # Do not erase a partial tree that another writer may have touched.
        raise ValueError("incomplete new package left at {}: {}".format(destination, error)) from error
    print("Created standalone package: {} ({} files)".format(destination, len(files)))
    print("Existing repositories are never overlaid. Review and merge adoption changes explicitly.")
    print("Shared project configuration is included. No existing/local/global settings, permissions, plugins, or remote records were changed.")


def check_package():
    errors = []
    link_count = 0
    check_instruction_files()
    ecc_files, ecc_modes = ecc_inventory()
    assets = REQUIRED_ASSETS + ecc_files
    for relative in assets:
        file = PACKAGE_ROOT / relative
        if not file.is_file():
            errors.append("missing asset: {}".format(relative))
            continue
        content = file.read_bytes()
        if not content.strip():
            errors.append("empty asset: {}".format(relative))
        if relative in (".mcp.json", ".claude/settings.json"):
            try:
                if not isinstance(json.loads(content), dict):
                    errors.append("configuration must be a JSON object: {}".format(relative))
            except ValueError as error:
                errors.append("invalid JSON configuration: {}: {}".format(relative, error))
        text = content.decode("utf-8") if file.suffix == ".md" else ""
        for target, path in local_links(text):
            linked = (file.parent / path).resolve()
            if not linked.exists():
                errors.append("broken local link: {} -> {}".format(relative, target))
            link_count += 1
    modes = {"aidlc": False}
    modes.update({"aidlc-" + name: name in MANUAL_SKILLS for name in SKILLS})
    modes.update(ecc_modes)
    for name, manual in modes.items():
        file = PACKAGE_ROOT / ".claude/skills" / name / "SKILL.md"
        if not file.is_file():
            continue
        text = file.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            errors.append("missing skill frontmatter: {}".format(name))
            continue
        frontmatter = text.split("---", 2)[1]
        if not re.search(r"^name: {}\s*$".format(re.escape(name)), frontmatter, re.M):
            errors.append("skill name does not match directory: {}".format(name))
        explicit = bool(re.search(r"^disable-model-invocation: true\s*$", frontmatter, re.M))
        if manual != explicit:
            errors.append("skill invocation mode differs from inventory: {}".format(name))
        if re.search(r"^(allowed-tools|hooks|model|agent|context):", frontmatter, re.M):
            errors.append("skill must not grant tools or override the runtime: {}".format(name))
    if errors:
        for error in errors:
            print("ERROR: " + error, file=sys.stderr)
        return 1
    print("PASS: {} required assets; {} local links resolve.".format(len(assets), link_count))
    print("Package integrity only: approvals, service integrations, and model behavior are not verified here.")
    return 0


OPTIONAL_TOOLS = (
    # executable, purpose, ordered install candidates (prerequisite executable, argv)
    ("graphify", "code knowledge graph used by aidlc-repo-scout, aidlc-fix and aidlc-onboard",
     (("uv", ["uv", "tool", "install", "graphifyy"]), ("pipx", ["pipx", "install", "graphifyy"]))),
    ("codegraph", "local pre-indexed symbol/call graph exposed as the codegraph MCP server",
     (("npm", ["npm", "install", "-g", "@colbymchenry/codegraph"]),)),
    ("gh", "GitHub CLI for PR references in evidence.md and the github MCP token",
     (("brew", ["brew", "install", "gh"]),)),
    ("omp", "Oh My Pi host (optional second harness)", ()),
)
MCP_AUTH = {
    "context7": ("optional", "CONTEXT7_API_KEY", "works anonymously with lower rate limits; set the key (value `Bearer <key>`) for more"),
    "github": ("required", "GITHUB_PERSONAL_ACCESS_TOKEN", "PAT with repo scope; `gh auth token` prints one for the logged-in account"),
    "atlassian": ("oauth", None, "OAuth 2.1 in the browser on first use: run /mcp in Claude Code and authenticate"),
    "codegraph": ("binary", None, "local stdio server; needs the codegraph executable and `codegraph init` in the repository"),
}


def install_optional(executable, candidates):
    for prerequisite, argv in candidates:
        if shutil.which(prerequisite):
            print("  installing with: {}".format(" ".join(argv)))
            result = subprocess.run(argv, check=False)
            if result.returncode == 0 and shutil.which(executable):
                print("  installed: {}".format(shutil.which(executable)))
                return True
            print("  install command exited {}".format(result.returncode))
            return False
    print("  no supported installer found ({}); see docs/PLUGINS.md".format(
        ", ".join(prerequisite for prerequisite, _ in candidates) or "manual install only"))
    return False


def report_mcp(root):
    config = root / ".mcp.json"
    if not config.is_file():
        print("MCP: no .mcp.json in the target project")
        return
    try:
        servers = json.loads(config.read_text(encoding="utf-8")).get("mcpServers", {})
    except ValueError as error:
        print("MCP: .mcp.json is not valid JSON ({})".format(error))
        return
    if not servers:
        print("MCP: .mcp.json declares no project servers")
        return
    print("MCP servers declared in .mcp.json (Claude asks once per project before connecting):")
    for name in sorted(servers):
        kind, variable, note = MCP_AUTH.get(name, ("unknown", None, "auth requirements not catalogued here"))
        state = ""
        if variable:
            state = " — {} is {}".format(variable, "set" if os.environ.get(variable) else "NOT set")
        print("  {}: auth {}{}; {}".format(name, kind, state, note))
    print("  Jira/Confluence go through the atlassian server; nothing here stores credentials in the repository.")


def doctor(root, install=False):
    missing = []
    for executable in ("python3", "git", "claude"):
        path = shutil.which(executable)
        print("{}: {}".format(executable, path or "MISSING"))
        if path is None:
            missing.append(executable)
    print("Optional tools (skills use them when present):")
    for executable, purpose, candidates in OPTIONAL_TOOLS:
        path = shutil.which(executable)
        if path:
            print("  {}: {}".format(executable, path))
            continue
        commands = " | ".join(" ".join(argv) for _, argv in candidates) or "manual install; see docs/PLUGINS.md"
        print("  {}: not installed — {}. Install: {}".format(executable, purpose, commands))
        if install and candidates:
            install_optional(executable, candidates)
    if not install:
        print("  Run `python3 scripts/aidlc.py doctor --install` to run the listed installers for the missing tools.")
    report_mcp(root)
    if shutil.which("git"):
        try:
            result = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, timeout=10, check=False,
            )
        except subprocess.TimeoutExpired:
            print("git repository: check timed out")
            missing.append("git repository")
        else:
            if result.returncode:
                print("git repository: MISSING (artifact history, worktrees and PRs need one)")
                missing.append("git repository")
            else:
                print("git repository: " + result.stdout.strip())
    print("NOT CHECKED: Claude authentication/entitlements, MCP connectivity, policy owners, branch protection,")
    print("managed controls, CI credentials, deployment, monitoring, and incident integrations.")
    print("See docs/PREREQUISITES.md. Tool presence does not establish operational readiness.")
    return 1 if missing else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="target project for new/doctor/mode/status/current (default: current directory)")
    commands = parser.add_subparsers(dest="command", required=True)
    new = commands.add_parser("new", help="create only a draft intent; refuse to overwrite work")
    new.add_argument("change_id")
    commands.add_parser("check", help="check this package's required assets and local links")
    doc = commands.add_parser("doctor", help="inspect local prerequisites and MCP auth needs; --install runs the listed installers for missing optional tools")
    doc.add_argument("--install", action="store_true", help="install missing optional tools with the available package manager (uv/pipx, npm, brew)")
    commands.add_parser("mode", help="report greenfield or brownfield for the target project; .aidlc/mode overrides")
    commands.add_parser("status", help="list changes under changes/ with the stage artifacts present")
    commands.add_parser("current", help="print the change ID in play (branch, .aidlc/current, or the only open change)")
    commands.add_parser("worktree", help="WorktreeCreate hook: read the requested name on stdin, print the worktree path")
    conv = commands.add_parser("conventions", help="compare repository conventions with the package defaults; --apply copies only missing defaults")
    conv.add_argument("--apply", action="store_true", help="copy missing default convention files into the target project (never overwrites)")
    export = commands.add_parser("package", help="export a complete standalone tree to a new directory; never overwrite")
    export.add_argument("destination", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "new":
            new_change(args.root.resolve(), args.change_id)
            return 0
        if args.command == "check":
            return check_package()
        if args.command == "package":
            package(args.destination)
            return 0
        if args.command == "mode":
            print_mode(args.root.resolve())
            return 0
        if args.command == "status":
            return print_status(args.root.resolve())
        if args.command == "current":
            return print_current(args.root.resolve())
        if args.command == "worktree":
            return create_worktree()
        if args.command == "conventions":
            return conventions(args.root.resolve(), apply=args.apply)
        return doctor(args.root.resolve(), install=getattr(args, "install", False))
    except (OSError, ValueError) as error:
        print("ERROR: {}".format(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
