#!/usr/bin/env python3
"""Generate plugins/ (lbvs-aidlc, lbvs-ecc, lbvs-aidlc-observer), the .omp/agents twins, .claude-plugin/marketplace.json
and .codex-plugin/plugin.json from the repo-template sources. Regenerate after editing any AIDLC skill, agent, hook,
vendored skill or shared doc; the generated trees are committed so the marketplace can serve them."""

import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aidlc import PACKAGE_ROOT, SKILL_DIRECTORIES, ecc_inventory  # noqa: E402

PLUGIN_VERSION = "0.2.0"
PLUGINS_ROOT = PACKAGE_ROOT / "plugins"
MARKETPLACE = PACKAGE_ROOT / ".claude-plugin/marketplace.json"
CODEX_MANIFEST = PACKAGE_ROOT / ".codex-plugin/plugin.json"
OMP_AGENTS = PACKAGE_ROOT / ".omp/agents"
REPOSITORY = "https://github.com/mkhan-lb/lbvs-aidlc"
AUTHOR = {"name": "Logicbroker / Virtualstock engineering"}
DOCS = ("WORKFLOW.md", "USAGE.md", "ARTIFACTS.md", "PLUGINS.md")
GLOSSARY_DIR = PACKAGE_ROOT / "docs/glossary"
GLOSSARIES = ("virtualstock", "logicbroker")
AGENTS = tuple(sorted(p.name for p in (PACKAGE_ROOT / ".claude/agents").glob("*.md")))
HOOK_SCRIPTS = ("protect-tests.sh", "pr-guard.sh", "artifact-guard.sh", "argument-guard.sh", "scaffold-check.sh", "style-mode.sh", "glossary-context.sh")
SHARED_SKILLS = ("architecture-decision-records", "doc-coauthoring", "unslop", "caveman")
OBSERVER_SKILL = "continuous-learning-v2"
OBSERVE_HOOK = "skills/" + OBSERVER_SKILL + "/hooks/observe.sh"
ROOT = "${CLAUDE_PLUGIN_ROOT}"
HELPER = 'python3 "' + ROOT + '/scripts/aidlc.py"'
PLUGINS = {
    "lbvs-aidlc": {
        "description": "Company AIDLC: Anthropic AI-native SDLC stages with confirmation gates, bug-fix evidence loop, brownfield onboarding, project-mode detection and git/artifact guards.",
        "keywords": ["aidlc", "sdlc", "workflow", "review", "evidence"],
    },
    "lbvs-ecc": {
        "description": "Optional engineering skill library vendored from Everything Claude Code: language, framework, testing, security and operations patterns.",
        "keywords": ["skills", "patterns", "testing", "security"],
    },
    "lbvs-aidlc-observer": {
        "description": "Opt-in continuous-learning observer: records tool use into project-scoped instincts; off by default.",
        "keywords": ["observer", "learning", "hooks"],
    },
}
REWRITES = (
    # Markdown links from skills/<name>/SKILL.md to shared docs.
    (re.compile(r"\]\(\.\./\.\./\.\./docs/([A-Z_]+\.md)(#[^)]*)?\)"), r"](" + ROOT + r"/docs/\1\2)"),
    # Prose mentions of shared docs and the helper.
    (re.compile(r"(?<![/\w])docs/(WORKFLOW|USAGE|ARTIFACTS|PLUGINS)\.md"), ROOT + r"/docs/\1.md"),
    (re.compile(r"python3 scripts/aidlc\.py"), HELPER),
    (re.compile(r"`REVIEW\.md`"), "`REVIEW.md` (the repository's own file, else `" + ROOT + "/REVIEW.md`)"),
    # Repository-layout paths to files the plugin ships elsewhere.
    (re.compile(r"(?<!\w)(?:\.\./)*\.claude/skills/"), ROOT + "/skills/"),
    (re.compile(r"(?<!\w)(?:\.\./)*\.claude/agents/"), ROOT + "/agents/"),
    (re.compile(r"(?<![\w/])\.claude/hooks/(protect-tests|pr-guard|artifact-guard|argument-guard|scaffold-check|style-mode|glossary-context)\.sh"), ROOT + r"/hooks/\1.sh"),
    (re.compile(r"(?<![\w/])\.claude/hooks/worktree-(create|remove)\.sh"), ROOT + r"/hooks/worktree-\1.sh"),
    (re.compile(r"(?<![\w/])docs/vendor/(aws-aidlc/NOTICE\.md|anthropic-skills/NOTICE\.md|ecc/LICENSE|cursor-plugins/(?:LICENSE|manifest\.json)|caveman/(?:LICENSE|manifest\.json))"), ROOT + r"/docs/vendor/\1"),
)


def rewrite(text):
    for pattern, replacement in REWRITES:
        text = pattern.sub(replacement, text)
    return text


def copy_verbatim(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def copy_rewritten(source, target):
    if source.suffix != ".md":
        return copy_verbatim(source, target)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rewrite(source.read_text(encoding="utf-8")), encoding="utf-8")


def render_json(data):
    return (json.dumps(data, indent=2) + "\n").encode("utf-8")


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(render_json(data))


def write_manifest(plugin_root, name):
    write_json(plugin_root / ".claude-plugin/plugin.json", {
        "name": name,
        "description": PLUGINS[name]["description"],
        "version": PLUGIN_VERSION,
        "author": AUTHOR,
        "repository": REPOSITORY,
        "keywords": PLUGINS[name]["keywords"],
    })


def codex_manifest(skills, mcp_servers):
    """Codex plugin manifest in the shape ECC ships; skills and MCP only, no hooks or agents. Unverified in a Codex session."""
    return {
        "name": "lbvs-aidlc",
        "version": PLUGIN_VERSION,
        "description": PLUGINS["lbvs-aidlc"]["description"],
        "author": AUTHOR,
        "repository": REPOSITORY,
        "license": "MIT",
        "skills": skills,
        "mcpServers": mcp_servers,
    }


def omp_agent(name):
    """The Oh My Pi twin of .claude/agents/<name>: same description, lowercase tools, verbatim reads, a body that defers to the Claude file."""
    frontmatter = (PACKAGE_ROOT / ".claude/agents" / name).read_text(encoding="utf-8")[4:].partition("\n---\n")[0]
    fields = {block.partition(":")[0]: block.rstrip("\n") for block in re.split(r"^(?=[A-Za-z_-]+:)", frontmatter, flags=re.M) if block}
    tools = [tool.strip().lower() for tool in fields["tools"].partition(":")[2].split(",")] if "tools" in fields else []
    body = "Read `.claude/agents/{}` first and follow it exactly; it is the single definition of this agent. Tool names in this host are lowercase.".format(name)
    if "bash" in tools:
        body += " `bash` can still mutate state: respect the delegating session's authorised scope and never edit source, tests or artifacts."
    head = ["name: " + name[:-3], fields["description"]] + (["tools: " + ", ".join(tools)] if tools else []) + ["read-summarize: false"]
    return "---\n" + "\n".join(head) + "\n---\n\n" + body + "\n"


def build_omp_agents(agents_root):
    """Regenerate every .omp/agents twin under agents_root; returns the twin count."""
    if agents_root.exists():
        shutil.rmtree(agents_root)
    agents_root.mkdir(parents=True)
    for name in AGENTS:
        (agents_root / name).write_text(omp_agent(name), encoding="utf-8")
    return len(AGENTS)


def vendor_skills():
    """{skill name: declared repository-relative files} for every pinned vendored skill."""
    files, modes = ecc_inventory()
    return {name: [f for f in files if f.startswith(".claude/skills/{}/".format(name))] for name in modes}


def copy_vendor_skill(plugin_root, name, files):
    for relative in files:
        copy_verbatim(PACKAGE_ROOT / relative, plugin_root / "skills" / Path(relative).relative_to(".claude/skills"))


def script_hook(name, timeout=10, **fields):
    return {"type": "command", **fields, "command": 'sh "' + ROOT + '/hooks/' + name + '"', "timeout": timeout}


def helper_hook(arguments, timeout):
    return {"type": "command", "command": HELPER + " " + arguments, "timeout": timeout}


def aidlc_hooks():
    return {"hooks": {
        "SessionStart": [{
            "matcher": "startup|resume",
            "hooks": [helper_hook('--root "${CLAUDE_PROJECT_DIR}" mode', 10), script_hook("scaffold-check.sh"), script_hook("style-mode.sh"), script_hook("glossary-context.sh")],
        }],
        "PreToolUse": [
            {"matcher": "Edit|Write|MultiEdit|NotebookEdit", "hooks": [script_hook("protect-tests.sh"), script_hook("artifact-guard.sh")]},
            {"matcher": "Bash", "hooks": [script_hook("pr-guard.sh", **{"if": "Bash(gh *)"}), script_hook("pr-guard.sh", **{"if": "Bash(git push*)"})]},
        ],
        "UserPromptExpansion": [{"matcher": "lbvs-aidlc", "hooks": [script_hook("argument-guard.sh")]}],
        # create_worktree()/remove_worktree() take the repository from the hook payload's cwd,
        # so the same helper serves the adopting repository from inside the plugin.
        "WorktreeCreate": [{"hooks": [helper_hook("worktree", 120)]}],
        "WorktreeRemove": [{"hooks": [helper_hook("worktree-remove", 60)]}],
    }}


def observer_hooks():
    def observe(phase):
        return {"type": "command", "command": 'bash "' + ROOT + "/" + OBSERVE_HOOK + '" ' + phase, "timeout": 10}
    return {"hooks": {
        "PreToolUse": [{"matcher": "*", "hooks": [observe("pre")]}],
        "PostToolUse": [{"matcher": "*", "hooks": [observe("post")]}],
    }}


def aidlc_readme():
    return (
        "# lbvs-aidlc plugin\n\n"
        "Generated by `python3 scripts/build_plugin.py` from the repo-template sources; do not edit by hand.\n\n"
        "Skills are namespaced `/lbvs-aidlc:<skill>` (`/lbvs-aidlc:lbvs-aidlc <change-id>` starts a change; "
        "`/lbvs-aidlc:lbvs-aidlc-init` sets a repository up). Agents: "
        + ", ".join("`lbvs-aidlc:{}`".format(name[:-3]) for name in AGENTS)
        + ". Hooks: project-mode, scaffold-version, reply-style and glossary-index lines at session start, reproduction-test protection while "
        "`.aidlc/fix/*.json` exists in the project, artifact content-boundary lint on `changes/**` and `docs/solutions/**`, "
        "a confirmation gate on `git commit`/`git push`, and one-bare-ID argument checking on `/lbvs-aidlc*` commands. "
        'The helper is reachable as `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" <subcommand>` or `bin/aidlc`; '
        "`conventions` uses the bundled `templates/conventions/`.\n\n"
        "Oh My Pi loads the same plugin: `package.json` registers `omp/aidlc-guards.ts`, which supplies the mode line, "
        "test protection, artifact lint and the commit/push confirmation for omp sessions. `.codex-plugin/plugin.json` "
        "exposes the skills and `.mcp.json` to Codex; agents and hooks are not carried, and this surface is unverified in a Codex session.\n\n"
        "The plugin does not ship a `CLAUDE.md`; run `/lbvs-aidlc:lbvs-aidlc-onboard` or `/init` in the adopting repository. "
        "Shared workflow docs live under `docs/` inside the plugin and are referenced via `${CLAUDE_PLUGIN_ROOT}`.\n"
    )


def build_aidlc(plugin_root, vendored):
    write_manifest(plugin_root, "lbvs-aidlc")
    for name in SKILL_DIRECTORIES:
        for source in (PACKAGE_ROOT / ".claude/skills" / name).rglob("*"):
            if source.is_file() and not source.name.startswith("."):
                copy_rewritten(source, plugin_root / "skills" / source.relative_to(PACKAGE_ROOT / ".claude/skills"))
    for name in SHARED_SKILLS:
        copy_vendor_skill(plugin_root, name, vendored[name])
    for name in AGENTS:
        copy_rewritten(PACKAGE_ROOT / ".claude/agents" / name, plugin_root / "agents" / name)
    for name in DOCS:
        copy_rewritten(PACKAGE_ROOT / "docs" / name, plugin_root / "docs" / name)
    copy_rewritten(PACKAGE_ROOT / "REVIEW.md", plugin_root / "REVIEW.md")
    copy_verbatim(PACKAGE_ROOT / "scripts/aidlc.py", plugin_root / "scripts/aidlc.py")
    for source in (PACKAGE_ROOT / "templates/conventions").iterdir():
        if source.is_file():
            copy_rewritten(source, plugin_root / "templates/conventions" / source.name)
    for name in HOOK_SCRIPTS:
        copy_verbatim(PACKAGE_ROOT / ".claude/hooks" / name, plugin_root / "hooks" / name)
    for source in GLOSSARY_DIR.iterdir():
        if source.is_file():
            copy_verbatim(source, plugin_root / "docs/glossary" / source.name)
    for notice in ("docs/vendor/aws-aidlc/NOTICE.md", "docs/vendor/anthropic-skills/NOTICE.md", "docs/vendor/ecc/LICENSE", "docs/vendor/cursor-plugins/LICENSE", "docs/vendor/cursor-plugins/manifest.json", "docs/vendor/caveman/LICENSE", "docs/vendor/caveman/manifest.json"):
        copy_verbatim(PACKAGE_ROOT / notice, plugin_root / notice)
    copy_verbatim(PACKAGE_ROOT / ".mcp.json", plugin_root / ".mcp.json")
    copy_verbatim(PACKAGE_ROOT / ".omp/hooks/pre/aidlc-guards.ts", plugin_root / "omp/aidlc-guards.ts")
    launcher = plugin_root / "bin/aidlc"
    launcher.parent.mkdir(parents=True)
    launcher.write_text('#!/bin/sh\nexec python3 "$(dirname "$0")/../scripts/aidlc.py" "$@"\n', encoding="utf-8")
    launcher.chmod(0o755)
    write_json(plugin_root / "package.json", {
        "name": "lbvs-aidlc",
        "version": PLUGIN_VERSION,
        "private": True,
        "omp": {"extensions": ["./omp/aidlc-guards.ts"]},
    })
    write_json(plugin_root / "hooks/hooks.json", aidlc_hooks())
    write_json(plugin_root / ".codex-plugin/plugin.json", codex_manifest("./skills/", "./.mcp.json"))
    (plugin_root / "README.md").write_text(aidlc_readme(), encoding="utf-8")


def build_ecc(plugin_root, vendored):
    write_manifest(plugin_root, "lbvs-ecc")
    for name, files in vendored.items():
        if name not in SHARED_SKILLS and name != OBSERVER_SKILL:
            copy_vendor_skill(plugin_root, name, files)
    for notice in ("docs/vendor/ecc/LICENSE", "docs/vendor/ecc/manifest.json"):
        copy_verbatim(PACKAGE_ROOT / notice, plugin_root / notice)


def build_observer(plugin_root, vendored):
    write_manifest(plugin_root, "lbvs-aidlc-observer")
    copy_vendor_skill(plugin_root, OBSERVER_SKILL, vendored[OBSERVER_SKILL])
    copy_verbatim(PACKAGE_ROOT / "docs/vendor/ecc/LICENSE", plugin_root / "docs/vendor/ecc/LICENSE")
    write_json(plugin_root / "hooks/hooks.json", observer_hooks())


BUILDERS = {"lbvs-aidlc": build_aidlc, "lbvs-ecc": build_ecc, "lbvs-aidlc-observer": build_observer}


def build(plugins_root):
    """Regenerate every plugin tree under plugins_root; returns {plugin name: file count}."""
    vendored = vendor_skills()
    counts = {}
    for name, builder in BUILDERS.items():
        plugin_root = plugins_root / name
        if plugin_root.exists():
            shutil.rmtree(plugin_root)
        builder(plugin_root, vendored)
        counts[name] = sum(1 for p in plugin_root.rglob("*") if p.is_file())
    return counts


def marketplace():
    def entry(name, **extra):
        return {
            "name": name,
            "source": "./plugins/" + name,
            "description": PLUGINS[name]["description"],
            "version": PLUGIN_VERSION,
            "category": "productivity",
            "tags": PLUGINS[name]["keywords"],
            **extra,
        }
    return {
        "name": "lbvs-aidlc",
        "description": "Company AIDLC plugins: the Anthropic AI-native SDLC workflow for Claude Code and Oh My Pi.",
        "owner": {**AUTHOR, "url": REPOSITORY},
        "plugins": [entry("lbvs-aidlc"), entry("lbvs-ecc"), entry("lbvs-aidlc-observer", defaultEnabled=False)],
    }


def glossary_index(company):
    """One line per term (term, aliases, domain, first sentence) plus the naming-trap bullets of docs/glossary/<company>-glossary.md."""
    text = (GLOSSARY_DIR / (company + "-glossary.md")).read_text(encoding="utf-8")
    terms, traps, section = [], [], None
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        elif line.startswith("| **") and section == "Glossary":
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            head = cells[0].split("<br>")
            term = head[0].strip("*")
            domain = re.sub(r"</?em>", "", head[-1]).strip()
            aliases = "; ".join(part.strip() for part in head[1:-1] if part.strip())
            first = re.split(r"(?<=[.!?])\s", cells[1].split("<br>")[0].strip())[0]
            terms.append("- {} ({}): {}".format(term, "; ".join(filter(None, (aliases, domain))), first))
        elif line.startswith("- ") and section in ("Naming traps", "Words to use carefully"):
            traps.append(line)
    if not terms:
        raise ValueError("no glossary rows found in docs/glossary/{}-glossary.md".format(company))
    return (
        "# {} glossary index\n\n".format(company.capitalize())
        + "Generated by `scripts/build_plugin.py` from `{0}-glossary.md` in this directory; do not edit. One line per term: term (aliases; domain): first sentence of the definition. "
        "The full entry, its usage note and its evidence are in `{0}-glossary.md`.\n\n## Terms\n\n".format(company)
        + "\n".join(terms) + "\n\n## Naming traps\n\n" + "\n".join(traps) + "\n"
    )


def root_files():
    """{generated repository file outside plugins/: wanted bytes}."""
    files = {
        MARKETPLACE: render_json(marketplace()),
        CODEX_MANIFEST: render_json(codex_manifest("./plugins/lbvs-aidlc/skills/", "./plugins/lbvs-aidlc/.mcp.json")),
    }
    for company in GLOSSARIES:
        files[GLOSSARY_DIR / (company + "-index.md")] = glossary_index(company).encode("utf-8")
    return files


def tree(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()} if root.is_dir() else {}


def drifted(fresh, committed):
    """Repository-relative paths where the committed tree differs from the freshly built one."""
    wanted, current = tree(fresh), tree(committed)
    prefix = committed.relative_to(PACKAGE_ROOT).as_posix() + "/"
    changed = sorted(p for p in wanted.keys() & current.keys() if wanted[p] != current[p])
    return [prefix + p for p in sorted(set(wanted) ^ set(current)) + changed]


def check():
    """Exit 1 when a committed plugin, agent twin or root manifest differs from a fresh build; lists the drifted paths."""
    drift = []
    with tempfile.TemporaryDirectory(prefix="lbvs-aidlc-plugins-") as temporary:
        fresh = Path(temporary)
        build(fresh / "plugins")
        build_omp_agents(fresh / "agents")
        for name in BUILDERS:
            drift.extend(drifted(fresh / "plugins" / name, PLUGINS_ROOT / name))
        drift.extend(drifted(fresh / "agents", OMP_AGENTS))
    drift.extend(path.relative_to(PACKAGE_ROOT).as_posix() for path, wanted in root_files().items() if not path.is_file() or path.read_bytes() != wanted)
    for path in drift:
        print("plugin drift: {}".format(path))
    if drift:
        print("Regenerate with: python3 scripts/build_plugin.py")
    return 1 if drift else 0


def main():
    if sys.argv[1:] == ["--check"]:
        return check()
    if sys.argv[1:]:
        print("usage: build_plugin.py [--check]", file=sys.stderr)
        return 2
    # Root files first: the plugin build copies the generated glossary indexes.
    for path, content in root_files().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        print("Generated {}".format(path.relative_to(PACKAGE_ROOT)))
    print("Generated {} ({} agent twins)".format(OMP_AGENTS.relative_to(PACKAGE_ROOT), build_omp_agents(OMP_AGENTS)))
    for name, count in build(PLUGINS_ROOT).items():
        print("Generated {}/{} ({} files)".format(PLUGINS_ROOT.relative_to(PACKAGE_ROOT), name, count))
    return 0


if __name__ == "__main__":
    sys.exit(main())
