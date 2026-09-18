#!/usr/bin/env python3
"""Local AIDLC artifact operations. This tool never grants approvals or deploys."""

import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
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
SKILL_DIRECTORIES = ("lbvs-aidlc",) + tuple("lbvs-aidlc-" + name for name in SKILLS)
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
    ".omp/hooks/pre/aidlc-guards.ts", ".omp/agents/lbvs-aidlc-verifier.md", ".omp/agents/lbvs-aidlc-repo-scout.md",
    ".vscode/settings.json", ".vscode/extensions.json",
    ".mcp.json", ".claude/settings.json", ".claude-plugin/marketplace.json", "scripts/build_plugin.py",
    ".claude/hooks/check-package.sh", ".claude/hooks/project-mode.sh",
    ".claude/hooks/protect-tests.sh", ".claude/hooks/worktree-create.sh", ".claude/hooks/worktree-remove.sh",
    ".claude/hooks/pr-guard.sh", ".claude/hooks/artifact-guard.sh",
    ".claude/hooks/argument-guard.sh", ".claude/hooks/scaffold-check.sh",
    ".claude/rules/package-maintenance.md",
    ".claude/skills/lbvs-aidlc-review/references/review-options.md",
    ".claude/skills/lbvs-aidlc-intent/templates/intent.md",
    ".claude/skills/lbvs-aidlc-design/templates/spec.md",
    ".claude/skills/lbvs-aidlc-plan/templates/plan.md",
    ".claude/skills/lbvs-aidlc-review/templates/review.md",
    ".claude/skills/lbvs-aidlc-fix/templates/evidence.md",
    ".claude/skills/lbvs-aidlc-handoff/templates/handoff.md",
    ".claude/skills/lbvs-aidlc-learn/templates/learning.md",
    ".claude/skills/lbvs-aidlc-ideate/templates/ideation.md",
    ".claude/skills/lbvs-aidlc-spike/templates/spike.md",
    ".claude/skills/lbvs-aidlc-ship/templates/pr-body.md",
    ".claude/skills/lbvs-aidlc-init/templates/agent.md",
    ".claude/skills/lbvs-aidlc-onboard/templates/repo-profile.md",
    "docs/adr/README.md", "docs/adr/template.md",
    "docs/incidents/README.md", "docs/incidents/template.md",
    "docs/security/README.md", "docs/security/threat-model-template.md",
    "docs/platform/README.md", "docs/platform/platform.md",
    "docs/glossary/README.md", "docs/glossary/template.md", "docs/glossary/logicbroker-glossary.md",
    "docs/glossary/logicbroker-glossary-comparison.md", "docs/glossary/virtualstock-glossary.md",
    "docs/playbooks/README.md", "docs/playbooks/template.md",
    "templates/conventions/CONVENTIONS.md", "templates/conventions/.editorconfig",
    "templates/conventions/.pre-commit-config.yaml", "templates/conventions/ruff.toml", "templates/conventions/biome.json",
    ".claude/agents/lbvs-aidlc-verifier.md", ".claude/agents/lbvs-aidlc-repo-scout.md",
    ".claude/agents/lbvs-aidlc-design-reviewer.md", ".claude/agents/lbvs-aidlc-threat-modeler.md",
    ".claude/agents/lbvs-aidlc-test-critic.md", ".claude/agents/lbvs-aidlc-conventions-checker.md",
    ".omp/agents/lbvs-aidlc-design-reviewer.md", ".omp/agents/lbvs-aidlc-threat-modeler.md",
    ".omp/agents/lbvs-aidlc-test-critic.md", ".omp/agents/lbvs-aidlc-conventions-checker.md",
    "docs/vendor/aws-aidlc/NOTICE.md",
    "docs/vendor/ecc/manifest.json", "docs/vendor/ecc/LICENSE",
    "docs/vendor/anthropic-skills/manifest.json", "docs/vendor/anthropic-skills/NOTICE.md",
    "docs/vendor/cursor-plugins/manifest.json", "docs/vendor/cursor-plugins/LICENSE",
    "mcp-configs/ecc.mcp-servers.example.json",
) + tuple(".claude/skills/{}/SKILL.md".format(name) for name in SKILL_DIRECTORIES)


def new_change(root, change_id):
    if not CHANGE_ID.fullmatch(change_id):
        raise ValueError("change-id must be lowercase ASCII words/digits separated by single hyphens")
    if not root.is_dir():
        raise ValueError("target root must be an existing directory")
    # Read the template before creating anything; failure must not leave an empty change.
    # The plugin build lays skills out under skills/ instead of .claude/skills/.
    template = PACKAGE_ROOT / ".claude/skills/lbvs-aidlc-intent/templates/intent.md"
    if not template.is_file():
        template = PACKAGE_ROOT / "skills/lbvs-aidlc-intent/templates/intent.md"
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
    print("Refine the intent with the engineer, then use lbvs-aidlc-design for the spec.")
    print("No approval, commit, push, or deployment was performed.")


VENDOR_MANIFESTS = ("docs/vendor/ecc/manifest.json", "docs/vendor/anthropic-skills/manifest.json", "docs/vendor/cursor-plugins/manifest.json")


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
                    or name.startswith(("aidlc-", "lbvs-aidlc")) or name in modes or not isinstance(manual, bool)):
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
        print("Brownfield: run {}lbvs-aidlc-onboard before the first change unless conventions are already recorded.".format(prefix))
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
        print("Brownfield: keep the repository's conventions; lbvs-aidlc-onboard records them in CLAUDE.md. Copy a default only where none exists.")
    return 0


PROFILE_PATH = "docs/repo-profile.md"


def profile(root):
    """Report whether docs/repo-profile.md exists and whether its manifests changed since it was verified."""
    file = root / PROFILE_PATH
    if not file.is_file():
        print("profile: missing ({}). Write one with /lbvs-aidlc-onboard or /lbvs-aidlc-init; stages will scout until it exists.".format(PROFILE_PATH))
        return 0
    head = file.read_text(encoding="utf-8").splitlines()[:12]
    verified = next((line for line in head if line.startswith("Last verified:")), "")
    manifests = next((line for line in head if line.startswith("Manifests:")), "")
    match = re.search(r"\bat ([0-9a-f]{7,40})\b", verified)
    if not match:
        print("profile: present but its header lacks `Last verified: <date> at <commit>`; treat as stale.")
        return 0
    revision = match.group(1)
    paths = [path for path in re.split(r"[\s,]+", manifests.partition(":")[2]) if path]
    if not git_out(root, "rev-parse", "--verify", "--quiet", revision + "^{commit}"):
        print("profile: stale (verified at {}, which is not in this repository's history).".format(revision[:12]))
        return 0
    tracked = set(git_out(root, "ls-files", "--", *paths).splitlines()) if paths else set()
    unknown = [path for path in paths if path not in tracked]
    if unknown:
        print("profile: stale (Manifests lists path(s) git does not track: {}). Fix the header or refresh with /lbvs-aidlc-onboard.".format(", ".join(unknown)))
        return 0
    log = git_out(root, "log", "--format=%h", revision + "..HEAD", "--", *paths) if paths else ""
    commits = [line for line in log.split("\n") if line]
    if commits:
        print("profile: stale ({} manifest commit(s) since {}: {}). Refresh with /lbvs-aidlc-onboard.".format(
            len(commits), revision[:12], ", ".join(commits[:5]) + (" …" if len(commits) > 5 else "")))
    else:
        print("profile: fresh ({}; no manifest changes since {}).".format(verified.partition(":")[2].strip(), revision[:12]))
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
        print("No changes yet. Start one with /lbvs-aidlc <change-id>.")
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
        print("Current change: none resolved; name one or start /lbvs-aidlc <change-id>.")
    print("Presence of a file is not proof the stage is complete; read the artifact.")
    return 0


def print_current(root):
    change_id, source = current_change(root)
    if not change_id:
        print("No current change resolved. Ask the engineer for the ID or start /lbvs-aidlc <change-id>.")
        return 1
    print("{}\t{}".format(change_id, source))
    return 0


ARTIFACT_RULES = (
    ("session-uri", re.compile(r"(?:artifact|agent|history|local|xd)://")),
    ("machine-path", re.compile(r"/Users/|/home/|/tmp/|/var/folders/|/private/|[A-Za-z]:\\")),
)


def repository_root(start):
    top = git_out(start, "rev-parse", "--show-toplevel")
    return Path(top) if top else start


def artifact_files(root, change_id=None):
    changes = root / "changes"
    scopes = [changes / change_id] if change_id else [changes]
    scopes.append(root / "docs" / "solutions")
    for scope in scopes:
        if scope.is_dir():
            yield from sorted(p for p in scope.rglob("*.md") if p.is_file())


def lint_text(relative, text):
    hits = 0
    for number, line in enumerate(text.splitlines(), 1):
        for rule, pattern in ARTIFACT_RULES:
            for match in pattern.finditer(line):
                print("{}:{}: {} {}".format(relative, number, rule, match.group(0)))
                hits += 1
    return hits


def lint_artifacts(root, change_id=None):
    """Content boundary (docs/ARTIFACTS.md#content-boundary): change artifacts and lessons carry no session or machine-local references."""
    if change_id and not CHANGE_ID.fullmatch(change_id):
        raise ValueError("invalid change ID: {}".format(change_id))
    if change_id and not (root / "changes" / change_id).is_dir():
        raise ValueError("no such change: changes/{}".format(change_id))
    hits = 0
    count = 0
    for file in artifact_files(root, change_id):
        count += 1
        hits += lint_text(file.relative_to(root).as_posix(), file.read_text(encoding="utf-8"))
    if hits:
        return 1
    print("lint-artifacts: clean ({} files)".format(count))
    return 0


def lint_stdin(relative):
    """The artifact-guard hooks pipe an edit's new text here before it lands in the file."""
    if lint_text(Path(relative).as_posix(), sys.stdin.read()):
        return 1
    print("lint-artifacts: clean ({})".format(relative))
    return 0


def worktree_path(root, name):
    """Create or reuse a descriptive worktree; replaces Claude Code's default naming."""
    slug = re.sub(r"[^A-Za-z0-9._+/-]", "-", name).strip("-/")
    if not slug or ".." in slug.split("/"):
        raise ValueError("unusable worktree name: {!r}".format(name))
    match = re.fullmatch(r"aidlc[+/](.+)", slug)
    change_id = match.group(1) if match else slug
    if match and not CHANGE_ID.fullmatch(change_id):
        raise ValueError("aidlc/<change-id> must match ^[a-z0-9]+(-[a-z0-9]+)*$: {!r}".format(change_id))
    # An explicit aidlc branch prefix, or a name that is already a change under changes/, gets the
    # descriptive branch; anything else keeps Claude Code's default shape.
    if match or (CHANGE_ID.fullmatch(change_id) and (root / "changes" / change_id).is_dir()):
        branch, directory = "aidlc/" + change_id, "aidlc+" + change_id
    else:
        branch, directory = "worktree-" + slug, slug.replace("/", "+")
    destination = root / ".claude" / "worktrees" / directory
    if destination.is_dir():
        if not (destination / ".git").exists():
            raise ValueError("{} exists but is not a git worktree; remove it or run `git worktree prune`".format(destination))
        return destination
    existing = git_out(root, "rev-parse", "--verify", "--quiet", "refs/heads/" + branch)
    add = ["worktree", "add", str(destination)]
    add += [branch] if existing else ["-b", branch, "HEAD"]
    result = subprocess.run(["git", "-C", str(root)] + add, capture_output=True, text=True,
                            timeout=120, check=False)
    if result.returncode:
        raise ValueError("git worktree add failed: {}".format(result.stderr.strip() or result.returncode))
    # This hook replaces the default behaviour, so .worktreeinclude is ours to honour. The file uses
    # gitignore syntax, so let git evaluate it: copy the ignored files it selects.
    include = root / ".worktreeinclude"
    if include.is_file():
        ignored = set(git_out(root, "ls-files", "-z", "--others", "--ignored", "--exclude-standard").split("\0"))
        wanted = set(git_out(root, "ls-files", "-z", "--others", "--ignored", "--exclude-from=" + str(include)).split("\0"))
        for relative in sorted(path for path in ignored & wanted if path):
            source, target = root / relative, destination / relative
            if source.is_file() and not source.is_symlink() and not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
    return destination


def main_checkout(start):
    """The main working tree of the repository containing `start`, even when `start` is inside a linked worktree."""
    common = git_out(start, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if not common:
        return None
    top = git_out(Path(common).parent, "rev-parse", "--show-toplevel")
    return Path(top) if top else None


def hook_payload():
    payload = json.loads(sys.stdin.read() or "{}")
    if not isinstance(payload, dict):
        raise ValueError("hook input must be a JSON object")
    return payload


def create_worktree():
    """WorktreeCreate hook: read the requested name on stdin, print the worktree path."""
    payload = hook_payload()
    name = payload.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("WorktreeCreate input has no usable name")
    start = Path(payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or Path.cwd())
    top = main_checkout(start)
    if top is None:
        raise ValueError("worktree creation needs a git repository")
    destination = worktree_path(top, name)
    print("AIDLC worktree: {} on branch {}".format(
        destination, git_out(destination, "rev-parse", "--abbrev-ref", "HEAD")), file=sys.stderr)
    print(destination)
    return 0


def remove_worktree():
    """WorktreeRemove hook: remove a worktree this hook created; keep dirty trees and unmerged branches."""
    payload = hook_payload()
    target = payload.get("worktree_path")
    if not isinstance(target, str) or not target.strip():
        raise ValueError("WorktreeRemove input has no worktree_path")
    target = Path(target).resolve()
    top = main_checkout(Path(payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or Path.cwd()))
    if top is None or target.parent != (top / ".claude" / "worktrees").resolve():
        raise ValueError("refusing to remove {}: not under {}/.claude/worktrees".format(target, top))
    branch = git_out(target, "rev-parse", "--abbrev-ref", "HEAD") if target.is_dir() else ""
    result = subprocess.run(["git", "-C", str(top), "worktree", "remove", str(target)],
                            capture_output=True, text=True, timeout=60, check=False)
    if result.returncode:
        raise ValueError("git worktree remove refused (uncommitted work is kept): {}".format(result.stderr.strip()))
    # Delete only fully merged auto-named branches; aidlc/<id> branches carry the change and stay.
    if branch.startswith("worktree-"):
        subprocess.run(["git", "-C", str(top), "branch", "-d", branch], capture_output=True, text=True, timeout=15, check=False)
    print("AIDLC worktree removed: {}".format(target), file=sys.stderr)
    return 0


MANIFEST_PATH = Path(".aidlc/manifest.json")
PLUGIN_MANIFEST = Path("plugins/lbvs-aidlc/.claude-plugin/plugin.json")
MARKETPLACE = Path(".claude-plugin/marketplace.json")
PACKAGE_NAME = "lbvs-aidlc"
# Knowledge stores: a repository that already keeps one is not seeded with our index and template.
STORE_DIRS = ("docs/adr", "docs/incidents", "docs/security", "docs/references", "docs/playbooks",
              "docs/glossary", "docs/platform")
# Repository state the plugin cannot carry; skills, agents, hooks, helper and docs come from the plugin.
SCAFFOLD_FILES = ("REVIEW.md",)
GENERATED = {"changes/.gitkeep": b""}
# Files the adopting repository owns: install never creates or overwrites them, it prints what to merge.
REPO_OWNED = {
    "AGENTS.md": "add one line pointing at `/lbvs-aidlc` and the plugin's docs/WORKFLOW.md (Codex and Copilot read this file)",
    "CLAUDE.md": "add `@AGENTS.md` or one line pointing at `/lbvs-aidlc`; do not create it where the repository forbids a root CLAUDE.md",
    ".gitignore": "append: **/.aidlc/fix/  **/.aidlc/current  **/.claude/worktrees/  **/.claude/settings.local.json  .codegraph/",
    ".worktreeinclude": "list the ignored files worktrees need (.env, .claude/settings.local.json)",
    ".claude/settings.json": "merge the plugin declaration below; the plugin carries the skills, agents, hooks and helper",
}
OMP_INSTALL = ("Oh My Pi: omp plugin marketplace add {repo} && omp plugin install --scope project {plugin}@{market}"
               "  (writes .omp/plugins/installed_plugins.json; commit it)")


def scaffold():
    """Every file install seeds, relative to the adopting repository."""
    files = {Path(name) for name in SCAFFOLD_FILES + tuple(GENERATED)}
    for store in STORE_DIRS:
        files.update(p.relative_to(PACKAGE_ROOT) for p in (PACKAGE_ROOT / store).rglob("*") if p.is_file())
    return files


def seed(relative):
    name = relative.as_posix()
    return GENERATED[name] if name in GENERATED else (PACKAGE_ROOT / relative).read_bytes()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def package_revision():
    revision = git_out(PACKAGE_ROOT, "rev-parse", "HEAD") or "unknown"
    dirty = bool(git_out(PACKAGE_ROOT, "status", "--porcelain")) if revision != "unknown" else False
    return revision + ("+dirty" if dirty else "")


def plugin_version():
    manifest = PACKAGE_ROOT / PLUGIN_MANIFEST
    if not manifest.is_file():
        return "unknown"
    return json.loads(manifest.read_text(encoding="utf-8")).get("version", "unknown")


def origin_repo():
    """`owner/repo` of this package's origin remote, as Claude's marketplace source and `omp plugin marketplace add` want it."""
    url = git_out(PACKAGE_ROOT, "remote", "get-url", "origin")
    path = url.split(":", 1)[1] if "://" not in url and ":" in url else urlsplit(url).path
    return re.sub(r"\.git\Z", "", path.strip("/")) or "OWNER/REPO"


def plugin_declaration():
    """The .claude/settings.json block that enables this marketplace and its plugins, plus the Oh My Pi command."""
    market = json.loads((PACKAGE_ROOT / MARKETPLACE).read_text(encoding="utf-8"))
    repo = origin_repo()
    block = {
        "extraKnownMarketplaces": {market["name"]: {"source": {"source": "github", "repo": repo}}},
        "enabledPlugins": {"{}@{}".format(PACKAGE_NAME, market["name"]): True},
    }
    lines = [json.dumps(block, indent=2)]
    for plugin in market.get("plugins", []):
        if plugin["name"] != PACKAGE_NAME and plugin.get("defaultEnabled", True):
            lines.append('  optional in enabledPlugins: "{}@{}": true  ({})'.format(
                plugin["name"], market["name"], plugin.get("description", "")))
    lines.append(OMP_INSTALL.format(repo=repo, plugin=PACKAGE_NAME, market=market["name"]))
    return "\n".join(lines)


def owned_hints():
    hints = dict(REPO_OWNED)
    hints[".claude/settings.json"] += "\n" + plugin_declaration()
    return hints


def print_owned_hints(names):
    print("Repository-owned files (never written; merge by hand):")
    for name in sorted(names):
        print("  {:<24} {}".format(name, REPO_OWNED[name]))
    if ".claude/settings.json" in names:
        print(plugin_declaration())


def store_of(relative):
    for store in STORE_DIRS:
        if relative.as_posix().startswith(store + "/"):
            return store
    return None


def foreign_stores(repo, recorded=()):
    """Stores the repository already keeps and we never seeded: skip our index/template there."""
    seeded = {store_of(Path(name)) for name in recorded}
    return {store for store in STORE_DIRS
            if store not in seeded and (repo / store).is_dir() and any((repo / store).iterdir())}


def adoption_root(repo):
    repo = repo.resolve()
    if not repo.is_dir():
        raise ValueError("not a directory: {}".format(repo))
    if repo == PACKAGE_ROOT:
        raise ValueError("refusing to install the package into itself")
    return repo


def write_manifest(repo, files, skipped=()):
    manifest = {
        "package": PACKAGE_NAME,
        "plugin_version": plugin_version(),
        "source": git_out(PACKAGE_ROOT, "remote", "get-url", "origin") or "unknown",
        "branch": git_out(PACKAGE_ROOT, "rev-parse", "--abbrev-ref", "HEAD") or "unknown",
        "revision": package_revision(),
        "installed": datetime.date.today().isoformat(),
        "files": {f.as_posix(): digest(seed(f)) for f in sorted(files)},
        "owned": {name: digest(text.encode("utf-8")) for name, text in sorted(owned_hints().items())},
        "skipped": sorted(f.as_posix() for f in skipped),
    }
    target = repo / MANIFEST_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def install(repo, apply=False):
    """Seed repository state into an existing repository; never overwrite, never touch repository-owned files."""
    repo = adoption_root(repo)
    if (repo / MANIFEST_PATH).exists():
        raise ValueError("{} exists: already installed; use `sync`".format(MANIFEST_PATH))
    files = scaffold()
    stores = foreign_stores(repo)
    plan = {"write": [], "identical": [], "keep": [], "skip": []}
    for relative in sorted(files):
        target = repo / relative
        if store_of(relative) in stores:
            plan["skip"].append(relative)
        elif not target.exists():
            plan["write"].append(relative)
        elif digest(target.read_bytes()) == digest(seed(relative)):
            plan["identical"].append(relative)
        else:
            plan["keep"].append(relative)
    print("install {} <- {} plugin {} @ {}".format(repo, PACKAGE_NAME, plugin_version(), package_revision()))
    for relative in plan["write"]:
        print("  write     {}".format(relative.as_posix()))
    for relative in plan["keep"]:
        print("  keep      {}  (exists and differs; yours kept)".format(relative.as_posix()))
    for relative in plan["skip"]:
        print("  skip      {}  (you already keep {}/; reconcile via /lbvs-aidlc-onboard)".format(
            relative.as_posix(), store_of(relative)))
    print("{} to write, {} identical, {} kept, {} skipped, {} repository-owned.".format(
        len(plan["write"]), len(plan["identical"]), len(plan["keep"]), len(plan["skip"]), len(REPO_OWNED)))
    print_owned_hints(REPO_OWNED)
    if not apply:
        print("Report only; add --apply to write.")
        return 0
    for relative in plan["write"]:
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(seed(relative))
    write_manifest(repo, files - set(plan["skip"]), plan["skip"])
    print("Wrote {} files and {}. Review with `git status`, then commit; nothing was committed.".format(
        len(plan["write"]), MANIFEST_PATH))
    return 0


def sync(repo, apply=False):
    """Three-way compare package, manifest and repository; update untouched files, report the rest, delete nothing."""
    repo = adoption_root(repo)
    manifest_file = repo / MANIFEST_PATH
    if not manifest_file.is_file():
        raise ValueError("{} missing: not installed; use `install`".format(MANIFEST_PATH))
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    files = scaffold()
    recorded = manifest.get("files", {})
    skipped = set(manifest.get("skipped", []))
    stores = foreign_stores(repo, recorded)
    plan = {"update": [], "add": [], "conflict": [], "removed": [], "local": [], "absent": []}
    current = 0
    for name in sorted(set(recorded) | {f.as_posix() for f in files}):
        relative = Path(name)
        if name in skipped or (name not in recorded and store_of(relative) in stores):
            skipped.add(name)
            continue
        target = repo / relative
        pkg = digest(seed(relative)) if relative in files else None
        old = recorded.get(name)
        local = digest(target.read_bytes()) if target.is_file() else None
        if pkg is None:
            plan["removed"].append(relative)
        elif pkg == old:
            if local == old:
                current += 1
            else:
                plan["local" if local else "absent"].append(relative)
        elif local == pkg:
            current += 1
        elif old is None and local is None:
            plan["add"].append(relative)
        elif local == old:
            plan["update"].append(relative)
        else:
            plan["conflict"].append(relative)
    hints = owned_hints()
    owned_changed = [name for name in sorted(hints)
                     if manifest.get("owned", {}).get(name) not in (None, digest(hints[name].encode("utf-8")))]
    print("sync {} <- {} plugin {} @ {} (installed {} @ {}, plugin {})".format(
        repo, PACKAGE_NAME, plugin_version(), package_revision(), manifest.get("installed", "?"),
        manifest.get("revision", "?"), manifest.get("plugin_version", "?")))
    labels = {
        "update": "package changed, yours untouched",
        "add": "new in package",
        "conflict": "changed in both; resolve by hand",
        "removed": "no longer scaffolded; delete or keep — the plugin provides it",
        "local": "edited locally, package unchanged; kept",
        "absent": "deleted locally, package unchanged; kept absent",
    }
    for kind in ("update", "add", "conflict", "removed", "local", "absent"):
        for relative in plan[kind]:
            print("  {:<9} {}  ({})".format(kind, relative.as_posix(), labels[kind]))
    for name in owned_changed:
        print("  guidance  {}  (repository-owned; package hint changed)".format(name))
    print("{} current, {} to update, {} to add, {} conflicts, {} no longer scaffolded, {} local edits, {} absent, {} skipped stores.".format(
        current, len(plan["update"]), len(plan["add"]), len(plan["conflict"]),
        len(plan["removed"]), len(plan["local"]), len(plan["absent"]), len(skipped)))
    if owned_changed:
        print_owned_hints(owned_changed)
    if not apply:
        print("Report only; add --apply to write the updates and additions.")
        return 1 if plan["conflict"] else 0
    for relative in plan["update"] + plan["add"]:
        (repo / relative).parent.mkdir(parents=True, exist_ok=True)
        (repo / relative).write_bytes(seed(relative))
    # Conflicts keep their recorded hash so the next sync still sees them; everything else moves to the package's.
    write_manifest(repo, {f for f in files if f.as_posix() not in skipped}, (Path(name) for name in skipped))
    refreshed = json.loads(manifest_file.read_text(encoding="utf-8"))
    for relative in plan["conflict"]:
        refreshed["files"][relative.as_posix()] = recorded[relative.as_posix()]
    manifest_file.write_text(json.dumps(refreshed, indent=2) + "\n", encoding="utf-8")
    print("Wrote {} updates and {} additions; {} conflicts left for you. Nothing was committed.".format(
        len(plan["update"]), len(plan["add"]), len(plan["conflict"])))
    return 1 if plan["conflict"] else 0


def update(repo, source=None, apply=False):
    """Run from the adopting repository: fetch the package it was installed from and sync against it."""
    manifest_file = repo / MANIFEST_PATH
    if not manifest_file.is_file():
        raise ValueError("{} missing: not installed; run `install` from the package checkout".format(MANIFEST_PATH))
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    if source is not None:
        checkout = source.resolve()
        if not (checkout / "scripts" / "aidlc.py").is_file():
            raise ValueError("{} is not a package checkout (no scripts/aidlc.py)".format(checkout))
        return run_sync(checkout, repo, apply)
    url, branch = manifest.get("source"), manifest.get("branch")
    if not url or url == "unknown":
        raise ValueError("manifest records no package source; pass --from <package checkout>")
    with tempfile.TemporaryDirectory(prefix="lbvs-aidlc-update-") as temporary:
        checkout = Path(temporary) / "package"
        clone = ["git", "clone", "--quiet", "--depth", "1"] + (["--branch", branch] if branch and branch != "unknown" else [])
        result = subprocess.run(clone + [url, str(checkout)], capture_output=True, text=True, timeout=300, check=False)
        if result.returncode:
            raise ValueError("clone of {} failed: {}".format(url, result.stderr.strip()))
        print("update from {} ({})".format(url, branch or "default branch"))
        return run_sync(checkout, repo, apply)


def run_sync(checkout, repo, apply):
    command = [sys.executable, str(checkout / "scripts" / "aidlc.py"), "sync", str(repo)] + (["--apply"] if apply else [])
    return subprocess.run(command, check=False).returncode


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
        if relative in (".mcp.json", ".claude/settings.json", ".claude-plugin/marketplace.json"):
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
    modes = {"lbvs-aidlc": False}
    modes.update({"lbvs-aidlc-" + name: name in MANUAL_SKILLS for name in SKILLS})
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
        if name in SKILL_DIRECTORIES:
            errors.extend(check_aidlc_skill(name, text, frontmatter))
    errors.extend(check_agents())
    errors.extend(check_instructions_size())
    errors.extend(check_plugin_build())
    return finish_check(errors, assets, link_count)


def check_plugin_build():
    """The committed plugins/lbvs-aidlc tree must equal a fresh build; drift is the one way a single branch can lie."""
    builder = PACKAGE_ROOT / "scripts" / "build_plugin.py"
    if not builder.is_file():
        return []
    result = subprocess.run([sys.executable, str(builder), "--check"], capture_output=True, text=True, timeout=120, check=False)
    return [line for line in result.stdout.splitlines() if line.startswith("plugin drift:")] if result.returncode else []


SKILL_KEYS = frozenset(("name", "description", "when_to_use", "argument-hint", "disable-model-invocation"))
SKILL_BYTES = {"lbvs-aidlc": 7788}
SKILL_BYTES_DEFAULT = 7168
LISTING_CHARS = 1536  # Claude Code truncates description + when_to_use beyond this in the skill listing.
AGENT_KEYS = frozenset(("name", "description", "tools"))
AGENT_BODY_BYTES = 3072
INSTRUCTION_LINES = 60


def frontmatter_fields(frontmatter):
    return {match.group(1): match.group(2).strip() for match in re.finditer(r"^([A-Za-z_-]+):\s*(.*)$", frontmatter, re.M)}


def check_aidlc_skill(name, text, frontmatter):
    """The size and listing rules every AIDLC skill is written against; keeps them a check, not prose."""
    errors = []
    size = len(text.encode("utf-8"))
    cap = SKILL_BYTES.get(name, SKILL_BYTES_DEFAULT)
    if size > cap:
        errors.append("skill exceeds its size budget ({} > {} bytes): {}".format(size, cap, name))
    fields = frontmatter_fields(frontmatter)
    unexpected = sorted(set(fields) - SKILL_KEYS)
    if unexpected:
        errors.append("skill frontmatter has undeclared keys {}: {}".format(unexpected, name))
    listing = len(fields.get("description", "")) + len(fields.get("when_to_use", ""))
    if listing > LISTING_CHARS:
        errors.append("skill description + when_to_use exceed the listing cap ({} > {} chars): {}".format(listing, LISTING_CHARS, name))
    return errors


def check_agents():
    """Agent files are the whole system prompt of a subagent: one definition, small body, mirrored description."""
    errors = []
    for file in sorted((PACKAGE_ROOT / ".claude/agents").glob("*.md")):
        text = file.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            errors.append("missing agent frontmatter: {}".format(file.name))
            continue
        frontmatter, _, body = text[4:].partition("\n---\n")
        fields = frontmatter_fields(frontmatter)
        if fields.get("name") != file.stem:
            errors.append("agent name does not match filename: {}".format(file.name))
        if not fields.get("description"):
            errors.append("agent has no description: {}".format(file.name))
        unexpected = sorted(set(fields) - AGENT_KEYS)
        if unexpected:
            errors.append("agent frontmatter has undeclared keys {}: {}".format(unexpected, file.name))
        if len(body.encode("utf-8")) > AGENT_BODY_BYTES:
            errors.append("agent body exceeds {} bytes: {}".format(AGENT_BODY_BYTES, file.name))
        mirror = PACKAGE_ROOT / ".omp/agents" / file.name
        if not mirror.is_file():
            errors.append("agent has no .omp/agents mirror: {}".format(file.name))
        elif frontmatter_fields(mirror.read_text(encoding="utf-8").split("---", 2)[1]).get("description") != fields.get("description"):
            errors.append("agent description differs between .claude/agents and .omp/agents: {}".format(file.name))
    return errors


def check_instructions_size():
    lines = (PACKAGE_ROOT / "AGENTS.md").read_text(encoding="utf-8").count("\n")
    if lines > INSTRUCTION_LINES:
        return ["AGENTS.md is {} lines; keep it at most {} (facts Claude cannot infer; procedures belong in skills)".format(lines, INSTRUCTION_LINES)]
    return []


def finish_check(errors, assets, link_count):
    if errors:
        for error in errors:
            print("ERROR: " + error, file=sys.stderr)
        return 1
    print("PASS: {} required assets; {} local links resolve.".format(len(assets), link_count))
    print("Package integrity only: approvals, service integrations, and model behavior are not verified here.")
    return 0


OPTIONAL_TOOLS = (
    # executable, purpose, ordered install candidates (prerequisite executable, argv)
    ("graphify", "code knowledge graph used by lbvs-aidlc-repo-scout, lbvs-aidlc-fix and lbvs-aidlc-onboard",
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
        data = json.loads(config.read_text(encoding="utf-8"))
    except ValueError as error:
        print("MCP: .mcp.json is not valid JSON ({})".format(error))
        return
    servers = data.get("mcpServers", {}) if isinstance(data, dict) else None
    if not isinstance(servers, dict):
        print("MCP: .mcp.json must be a JSON object with an `mcpServers` object")
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
    parser.add_argument("--root", type=Path, help="target project for new/doctor/mode/status/current/lint-artifacts (default: current directory; its repository for lint-artifacts)")
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
    commands.add_parser("worktree-remove", help="WorktreeRemove hook: remove a hook-created worktree; keeps uncommitted work and aidlc/<id> branches")
    conv = commands.add_parser("conventions", help="compare repository conventions with the package defaults; --apply copies only missing defaults")
    conv.add_argument("--apply", action="store_true", help="copy missing default convention files into the target project (never overwrites)")
    commands.add_parser("profile", help="report whether docs/repo-profile.md exists and is fresh (manifests unchanged since its Last verified commit)")
    lint = commands.add_parser("lint-artifacts", help="scan changes/<id>/**/*.md (all changes without an ID) and docs/solutions/**/*.md for session references and machine paths; exit 1 on any hit")
    lint.add_argument("--root", dest="lint_root", type=Path, metavar="PATH", help="repository to scan (default: the repository containing the current directory)")
    lint.add_argument("--stdin", metavar="PATH", help="lint text read from stdin as if it were repository file PATH (the artifact-guard hooks use this); no scan")
    lint.add_argument("change_id", nargs="?", help="limit the scan to changes/<change_id>/")
    for name, text in (("install", "seed repository state (REVIEW.md, knowledge-store seeds, changes/) into an existing repository and print the plugin declaration to merge (report only; --apply writes new files, never overwrites)"),
                       ("sync", "compare an installed repository's seeds with this package (report only; --apply updates files you have not edited; never deletes)")):
        adopt = commands.add_parser(name, help=text)
        adopt.add_argument("repo", type=Path, help="root of the adopting repository")
        adopt.add_argument("--apply", action="store_true", help="write; without it only report")
    upd = commands.add_parser("update", help="from an installed repository: fetch the package recorded in .aidlc/manifest.json and sync against it (report only; --apply writes)")
    upd.add_argument("--from", dest="source", type=Path, metavar="PACKAGE", help="use this local package checkout instead of cloning the recorded source")
    upd.add_argument("--apply", action="store_true", help="write; without it only report")
    args = parser.parse_args()
    root = (args.root or Path.cwd()).resolve()
    try:
        if args.command == "lint-artifacts":
            if args.stdin:
                return lint_stdin(args.stdin)
            return lint_artifacts((args.lint_root or args.root or repository_root(Path.cwd())).resolve(), args.change_id)
        if args.command == "new":
            new_change(root, args.change_id)
            return 0
        if args.command == "check":
            return check_package()
        if args.command == "install":
            return install(args.repo, apply=args.apply)
        if args.command == "sync":
            return sync(args.repo, apply=args.apply)
        if args.command == "update":
            return update((args.root or repository_root(Path.cwd())).resolve(), source=args.source, apply=args.apply)
        if args.command == "mode":
            print_mode(root)
            return 0
        if args.command == "status":
            return print_status(root)
        if args.command == "current":
            return print_current(root)
        if args.command == "worktree":
            return create_worktree()
        if args.command == "worktree-remove":
            return remove_worktree()
        if args.command == "conventions":
            return conventions(root, apply=args.apply)
        if args.command == "profile":
            return profile(root)
        return doctor(root, install=getattr(args, "install", False))
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print("ERROR: {}".format(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
