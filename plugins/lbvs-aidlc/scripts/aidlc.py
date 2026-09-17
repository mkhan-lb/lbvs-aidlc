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
SKILLS = ("intent", "design", "plan", "build", "verify", "review", "fix", "onboard", "learn",
          "handoff", "resume", "ideate")
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
    "GOALS.md", "IMPLEMENTATION_PLAN.md", "FUTURE_WORK.md", "README.md",
    "AGENTS.md", "CLAUDE.md", "REVIEW.md", "docs/COVERAGE.md", "docs/DEPENDENCIES.md",
    "docs/PREREQUISITES.md", "docs/ARTIFACTS.md", "docs/VERIFICATION.md",
    "docs/COMPATIBILITY.md", "docs/MEASURES.md", "docs/PLUGINS.md",
    "docs/WORKFLOW.md", "docs/USAGE.md",
    ".omp/AGENTS.md", ".omp/RULES.md", ".omp/config.yml", ".worktreeinclude",
    ".mcp.json", ".claude/settings.json",
    ".claude/hooks/check-package.sh", ".claude/hooks/project-mode.sh", ".claude/hooks/protect-tests.sh",
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
    "docs/deferred/templates/incident.md",
    ".claude/agents/aidlc-verifier.md", ".claude/agents/aidlc-repo-scout.md",
    "docs/vendor/ecc/manifest.json", "docs/vendor/ecc/LICENSE",
    "mcp-configs/ecc.mcp-servers.example.json",
) + tuple(".claude/skills/{}/SKILL.md".format(name) for name in SKILL_DIRECTORIES)


def new_change(root, change_id):
    if not CHANGE_ID.fullmatch(change_id):
        raise ValueError("change-id must be lowercase ASCII words/digits separated by single hyphens")
    if not root.is_dir():
        raise ValueError("target root must be an existing directory")
    # Read the template before creating anything; failure must not leave an empty change.
    content = (PACKAGE_ROOT / ".claude/skills/aidlc-intent/templates/intent.md").read_text(encoding="utf-8")
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


def ecc_inventory():
    """Read the pinned import inventory without discovering arbitrary skill files."""
    manifest = PACKAGE_ROOT / "docs/vendor/ecc/manifest.json"
    for component in (manifest, *manifest.parents):
        if component == PACKAGE_ROOT:
            break
        if component.is_symlink():
            raise ValueError("refusing a symlinked ECC manifest: {}".format(manifest))
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("unsupported ECC manifest schema")
    skills = data.get("skills")
    if not isinstance(skills, list) or not skills:
        raise ValueError("ECC manifest must declare its imported skills")
    files = []
    modes = {}
    for skill in skills:
        if not isinstance(skill, dict):
            raise ValueError("invalid ECC skill entry")
        name, manual = skill.get("name"), skill.get("manual")
        if (not isinstance(name, str) or not CHANGE_ID.fullmatch(name)
                or name.startswith("aidlc-") or name in modes or not isinstance(manual, bool)):
            raise ValueError("invalid or duplicate ECC skill name/invocation mode")
        resources = skill.get("files")
        if not isinstance(resources, list) or not resources:
            raise ValueError("ECC skill has no declared resources: {}".format(name))
        prefix = ".claude/skills/{}/".format(name)
        paths = []
        for resource in resources:
            relative = resource.get("path") if isinstance(resource, dict) else None
            if (not isinstance(relative, str) or not relative.startswith(prefix)
                    or "\\" in relative or ".." in Path(relative).parts
                    or relative != Path(relative).as_posix()):
                raise ValueError("invalid ECC resource path: {!r}".format(relative))
            paths.append(relative)
        if prefix + "SKILL.md" not in paths:
            raise ValueError("ECC skill is missing its declared entrypoint: {}".format(name))
        files.extend(paths)
        modes[name] = manual
    if len(files) != len(set(files)):
        raise ValueError("duplicate ECC resource paths")
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
        print("Brownfield: run /aidlc-onboard before the first change unless conventions are already recorded.")
    print("Override with .aidlc/mode containing greenfield or brownfield.")


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


def doctor(root):
    missing = []
    for executable in ("python3", "git", "claude"):
        path = shutil.which(executable)
        print("{}: {}".format(executable, path or "MISSING"))
        if path is None:
            missing.append(executable)
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
    print("NOT CHECKED: Claude authentication/entitlements, policy owners, branch protection,")
    print("managed controls, CI credentials, deployment, monitoring, and incident integrations.")
    print("See docs/PREREQUISITES.md. Tool presence does not establish operational readiness.")
    return 1 if missing else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="target project for new/doctor/mode (default: current directory)")
    commands = parser.add_subparsers(dest="command", required=True)
    new = commands.add_parser("new", help="create only a draft intent; refuse to overwrite work")
    new.add_argument("change_id")
    commands.add_parser("check", help="check this package's required assets and local links")
    commands.add_parser("doctor", help="inspect local prerequisites without changing configuration")
    commands.add_parser("mode", help="report greenfield or brownfield for the target project; .aidlc/mode overrides")
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
        return doctor(args.root.resolve())
    except (OSError, ValueError) as error:
        print("ERROR: {}".format(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
