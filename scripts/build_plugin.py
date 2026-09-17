#!/usr/bin/env python3
"""Generate plugins/lbvs-aidlc from the repo-template sources. Regenerate after editing any AIDLC skill,
agent, hook or shared doc; the generated tree is committed so the marketplace can serve it."""

import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aidlc import PACKAGE_ROOT, SKILL_DIRECTORIES  # noqa: E402

PLUGIN_NAME = "lbvs-aidlc"
PLUGIN_ROOT = PACKAGE_ROOT / "plugins" / PLUGIN_NAME
DOCS = ("WORKFLOW.md", "USAGE.md", "ARTIFACTS.md", "PLUGINS.md", "COMPATIBILITY.md")
AGENTS = tuple(sorted(p.name for p in (PACKAGE_ROOT / ".claude/agents").glob("*.md")))
ROOT = "${CLAUDE_PLUGIN_ROOT}"
REWRITES = (
    # Markdown links from skills/<name>/SKILL.md to shared docs.
    (re.compile(r"\]\(\.\./\.\./\.\./docs/([A-Z_]+\.md)(#[^)]*)?\)"), r"](" + ROOT + r"/docs/\1\2)"),
    # Prose mentions of shared docs and the helper.
    (re.compile(r"(?<![/\w])docs/(WORKFLOW|USAGE|ARTIFACTS|PLUGINS|COMPATIBILITY)\.md"), ROOT + r"/docs/\1.md"),
    (re.compile(r"python3 scripts/aidlc\.py"), 'python3 "' + ROOT + '/scripts/aidlc.py"'),
    (re.compile(r"`REVIEW\.md`"), "`REVIEW.md` (the repository's own file, else `" + ROOT + "/REVIEW.md`)"),
    # Repository-layout paths to files the plugin ships elsewhere.
    (re.compile(r"(?<!\w)(?:\.\./)*\.claude/skills/"), ROOT + "/skills/"),
    (re.compile(r"(?<!\w)(?:\.\./)*\.claude/agents/"), ROOT + "/agents/"),
    (re.compile(r"(?<![\w/])\.claude/hooks/protect-tests\.sh"), ROOT + "/hooks/protect-tests.sh"),
    (re.compile(r"(?<![\w/])\.claude/hooks/worktree-(create|remove)\.sh"), ROOT + r"/hooks/worktree-\1.sh"),
    (re.compile(r"(?<![\w/])docs/vendor/(aws-aidlc/NOTICE\.md|ecc/LICENSE)"), ROOT + r"/docs/vendor/\1"),
)


def rewrite(text):
    for pattern, replacement in REWRITES:
        text = pattern.sub(replacement, text)
    return text


def copy_rewritten(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix == ".md":
        target.write_text(rewrite(source.read_text(encoding="utf-8")), encoding="utf-8")
    else:
        shutil.copy2(source, target)


def main():
    if PLUGIN_ROOT.exists():
        shutil.rmtree(PLUGIN_ROOT)
    manifest = {
        "name": PLUGIN_NAME,
        "description": "Company AIDLC: Anthropic AI-native SDLC stages with confirmation gates, bug-fix evidence loop, brownfield onboarding and project-mode detection.",
        "version": "0.1.0",
        "author": {"name": "Logicbroker / Virtualstock engineering"},
        "repository": "https://github.com/mkhan-lb/lbvs-aidlc",
        "keywords": ["aidlc", "sdlc", "workflow", "review", "evidence"],
    }
    (PLUGIN_ROOT / ".claude-plugin").mkdir(parents=True)
    (PLUGIN_ROOT / ".claude-plugin/plugin.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    for name in SKILL_DIRECTORIES:
        for source in (PACKAGE_ROOT / ".claude/skills" / name).rglob("*"):
            if source.is_file():
                copy_rewritten(source, PLUGIN_ROOT / "skills" / source.relative_to(PACKAGE_ROOT / ".claude/skills"))
    for name in AGENTS:
        copy_rewritten(PACKAGE_ROOT / ".claude/agents" / name, PLUGIN_ROOT / "agents" / name)
    for name in DOCS:
        copy_rewritten(PACKAGE_ROOT / "docs" / name, PLUGIN_ROOT / "docs" / name)
    copy_rewritten(PACKAGE_ROOT / "REVIEW.md", PLUGIN_ROOT / "REVIEW.md")
    copy_rewritten(PACKAGE_ROOT / "scripts/aidlc.py", PLUGIN_ROOT / "scripts/aidlc.py")
    for source in (PACKAGE_ROOT / "templates/conventions").iterdir():
        if source.is_file():
            copy_rewritten(source, PLUGIN_ROOT / "templates/conventions" / source.name)
    copy_rewritten(PACKAGE_ROOT / ".claude/hooks/protect-tests.sh", PLUGIN_ROOT / "hooks/protect-tests.sh")
    for notice in ("docs/vendor/aws-aidlc/NOTICE.md", "docs/vendor/ecc/LICENSE"):
        copy_rewritten(PACKAGE_ROOT / notice, PLUGIN_ROOT / notice)

    helper = 'python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py"'
    hooks = {
        "hooks": {
            "SessionStart": [{
                "matcher": "startup|resume",
                "hooks": [{
                    "type": "command",
                    "command": helper + ' --root "${CLAUDE_PROJECT_DIR}" mode',
                    "timeout": 10,
                }],
            }],
            "PreToolUse": [{
                "matcher": "Edit|Write|MultiEdit|NotebookEdit",
                "hooks": [{
                    "type": "command",
                    "command": 'sh "${CLAUDE_PLUGIN_ROOT}/hooks/protect-tests.sh"',
                    "timeout": 10,
                }],
            }],
            # create_worktree()/remove_worktree() take the repository from the hook payload's cwd,
            # so the same helper serves the adopting repository from inside the plugin.
            "WorktreeCreate": [{
                "hooks": [{"type": "command", "command": helper + " worktree", "timeout": 120}],
            }],
            "WorktreeRemove": [{
                "hooks": [{"type": "command", "command": helper + " worktree-remove", "timeout": 60}],
            }],
        }
    }
    (PLUGIN_ROOT / "hooks/hooks.json").write_text(json.dumps(hooks, indent=2) + "\n", encoding="utf-8")

    (PLUGIN_ROOT / "README.md").write_text(
        "# lbvs-aidlc plugin\n\n"
        "Generated by `python3 scripts/build_plugin.py` from the repo-template sources; do not edit by hand.\n\n"
        "Skills are namespaced `/lbvs-aidlc:<skill>` (`/lbvs-aidlc:lbvs-aidlc <change-id>` starts a change; "
        "`/lbvs-aidlc:lbvs-aidlc-init` sets a repository up). Agents: "
        + ", ".join("`lbvs-aidlc:{}`".format(name[:-3]) for name in AGENTS)
        + ". Hooks: project-mode line at session start and "
        "reproduction-test protection while `.aidlc/fix/*.json` exists in the project. The helper is reachable as "
        '`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" <subcommand>`; `conventions` uses the bundled '
        "`templates/conventions/`.\n\n"
        "The plugin does not ship a `CLAUDE.md`; run `/lbvs-aidlc:lbvs-aidlc-onboard` or `/init` in the adopting repository. "
        "Shared workflow docs live under `docs/` inside the plugin and are referenced via `${CLAUDE_PLUGIN_ROOT}`.\n",
        encoding="utf-8",
    )
    files = sum(1 for p in PLUGIN_ROOT.rglob("*") if p.is_file())
    print("Generated {} ({} files)".format(PLUGIN_ROOT.relative_to(PACKAGE_ROOT), files))


if __name__ == "__main__":
    main()
