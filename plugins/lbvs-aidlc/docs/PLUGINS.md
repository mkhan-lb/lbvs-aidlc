# Bundled skills, subagents and plugins by stage

Everything here is a recommendation. The package installs nothing by itself: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" install`, the hooks and the `lbvs-aidlc-*` skills add no marketplace registration, plugin, LSP server or MCP connection, and installing this package's own plugins is the engineer's explicit `claude plugin install`. Two exceptions are declared, not performed: [`.mcp.json`](../.mcp.json) names three remote MCP servers that Claude Code connects only after you approve them once per project ([MCP servers](REFERENCE.md#mcp-servers)), and `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" doctor --install` runs the package-manager installers for missing optional tools (`graphify`, `codegraph`, `gh`) only when you pass that flag. Review each plugin's permissions and context cost in `/plugin` before installing, and keep company policy (managed settings, allowed marketplaces) authoritative. Inventory checked on 16 September 2026 against the [commands reference](https://code.claude.com/docs/en/commands), [sub-agents](https://code.claude.com/docs/en/sub-agents), [discover plugins](https://code.claude.com/docs/en/discover-plugins) and the [official marketplace catalog](https://github.com/anthropics/claude-plugins-official).

Official marketplace plugins install with `/plugin install <name>@claude-plugins-official`. Third-party plugins first need `/plugin marketplace add <owner>/<repo>`.

## Stage table

| Stage | AIDLC entry | Bundled Claude Code skills and subagents to use | Official marketplace plugins worth installing |
| --- | --- | --- | --- |
| Onboard (brownfield) | `/lbvs-aidlc-onboard`, `lbvs-aidlc-repo-scout` agent, `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" mode`, `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" conventions` (report; greenfield offered `--apply`) | `/init` with `CLAUDE_CODE_NEW_INIT=1` as the alternative CLAUDE.md bootstrap; Explore subagent for read-only research; `/doctor` for setup and CLAUDE.md trims; the `inherit-legacy-style` skill when staying legacy; [`docs/platform/README.md`](platform/README.md) when cloud delivery is needed | `claude-md-management`, `code-modernization` (modernize route), one LSP plugin per language (below), `context7` |
| Ticket intake | `/lbvs-aidlc-ticket <KEY or issue URL>`, which returns a confirmed change ID and a seeded `intent.md` | AskUserQuestion to confirm the derived ID; `gh issue view` for GitHub issues when the CLI is authenticated | `atlassian` (Jira read via `getJiraIssue`) and `github` (issue read), both declared in `.mcp.json`; the skill never writes back |
| Spike | `/lbvs-aidlc-spike [id]`, which writes `changes/<id>/spike.md` | Explore subagent and `lbvs-aidlc-repo-scout` for read-only research; `graphify query` and `graphify path` when `graphify-out/` exists; `/deep-research` for external questions | `context7`, `codegraph` MCP when installed; `architecture-decision-records` at the end gate |
| Intent | `/lbvs-aidlc <id>`, which invokes `lbvs-aidlc-intent` | AskUserQuestion interview; Explore subagent for grounding in current behaviour; `doc-coauthoring` to structure a long intent with a stakeholder | `atlassian` (Jira source records), `github` (issues and PRs), `slack` (originator threads); optional `compound-engineering` `ce-brainstorm` (below) |
| Design | `lbvs-aidlc-design`, `lbvs-aidlc-design-reviewer` agent (READY / NOT READY before the gate), `lbvs-aidlc-threat-modeler` agent (when the threat-model offer is accepted) | Plan subagent for read-only research; `context7` MCP (`resolve-library-id`, then `query-docs`) before designing against a library, logged in `docs/references/libraries.md`; `docs/platform/platform.md` when present; `/design` only where Claude Design is available; `architecture-decision-records` when the design offers an ADR; `docs/security/threat-model-template.md` when it offers a threat model | `feature-dev` (structured feature design), `context7`, `security-guidance` (design-time security hints) |
| Plan | `lbvs-aidlc-plan` (tasks carry `_Requirements: R…_` trace lines; every R-ID covered) | Native plan mode (`Shift+Tab`), Plan and Explore subagents; `context7` for any library the plan relies on; `docs/platform/platform.md` for orb values and pipeline config; `/batch` only for a change that decomposes into independent worktrees and PRs | `feature-dev`, `atlassian` (link the plan to the ticket) |
| Build | `lbvs-aidlc-build` (one task at a time; `[x]` only after the task's check) | `context7` before implementing against a library; the repository's own pre-commit and lint before a task is declared done; `/goal` for a completion condition; `/run` and `/run-skill-generator` to drive the app; `/simplify` after the diff is green; `/fewer-permission-prompts` to trim repeated prompts | LSP plugin for the language (diagnostics after each edit), `commit-commands`, `hookify` (turn a repeated correction into a hook), `playwright` for browser-driven UI checks |
| Verify | `lbvs-aidlc-verify` (table `R-ID \| check \| observed result \| not run`), `lbvs-aidlc-verifier` agent | `/verify` (user-invoked) to build and run the change; `/run`; `/debug` when a session misbehaves | `playwright`, `sentry` (compare against live errors when authorised) |
| Review | `lbvs-aidlc-review`, root `REVIEW.md` (the repository's own file, else `${CLAUDE_PLUGIN_ROOT}/REVIEW.md`) | `/code-review` (bundled; also `/review`) at the effort the [review tier](WORKFLOW.md#review-loop-and-escalation) sets; `/security-review` where available (triaged results saved as `docs/security/findings/YYYY-MM-DD-security-review.md` on request); a fresh-context subagent for adversarial review; Compliance check reports an architectural change without an ADR as a finding | `code-review`, `pr-review-toolkit`, `security-guidance`, `github` (PR comments only with explicit authority) |
| Ship | `/lbvs-aidlc-ship [id]`, which commits, pushes `aidlc/<id>` and opens the PR from `templates/pr-body.md` ([ship gate](WORKFLOW.md#shipping-a-reviewed-change)) | `gh pr create --base <default branch> --body-file …` when `gh` is authenticated; `git status` and the diff shown first; never merge, approve or enable auto-merge | `github` MCP (PR creation when `gh` is absent), `commit-commands`, `atlassian` (ticket link in the PR body) |
| Fix and evidence | `/lbvs-aidlc-fix <id>`, which writes `changes/<id>/evidence.md` | The [failing-test-first loop](WORKFLOW.md#bug-fix-evidence-loop) with `protect-tests.sh` active; `/verify` and `/run` for observed proof; `/debug`; the offer of `docs/incidents/YYYY-MM-DD-<slug>.md` for alert- or incident-sourced defects and of `docs/security/findings/` for security defects | `sentry` (incident and alert references), `atlassian` and `github` (Jira key and PR URL in the evidence), `playwright` (screenshots and recordings) |
| Learn | `lbvs-aidlc-learn` (lessons carry `Confidence`, `Observations`, `Scope`; a re-observed topic bumps the lesson; promotion rule in [knowledge stores](WORKFLOW.md#knowledge-stores)) | `/skill-doctor` to keep skills lean; `/doctor` to trim CLAUDE.md after a lesson lands in it; the optional, off-by-default `lbvs-aidlc-observer@lbvs-aidlc` plugin ([ECC skill library](USAGE.md#12-use-the-optional-ecc-skill-library)), which does not replace `lbvs-aidlc-learn` | `claude-md-management`, `session-report` (what the session did), `project-artifact` |
| Cross-cutting | `/lbvs-aidlc`, hooks, `.claude/rules/`, `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" status` and `current` to find the change in play | `/doctor`, `/skill-doctor`, `/fewer-permission-prompts`, `/batch`, Explore, Plan and general-purpose subagents, `/loop` for repeated checks | `hookify`, `claude-md-management`, `context7`, LSP plugins, `github`, `atlassian`, `slack`, `sentry`, `session-report`, `project-artifact` |

Bundled skills are prompt-based and ship with the CLI; `/verify` and `/deep-research` are user-invoked only. A project skill with the same name replaces the bundled one, so keep the `lbvs-aidlc-*` names distinct from bundled names.

Two project-local mechanisms sit beside these tools, and installing a plugin changes neither. The helper `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py"` owns the subcommands listed in [REFERENCE.md](REFERENCE.md#helper); its `doctor` and `status` are unrelated to the bundled `/doctor` command or to any plugin command of the same word. The hook scripts are `protect-tests.sh`, `pr-guard.sh`, `artifact-guard.sh`, `argument-guard.sh`, `scaffold-check.sh`, `style-mode.sh` and `glossary-context.sh` (seven), plus the helper's `mode` line and, in this repository only, `worktree-create.sh` and `worktree-remove.sh` ([worktrees](WORKFLOW.md#worktrees)). At SessionStart they run in the order helper `mode`, `scaffold-check.sh`, `style-mode.sh`, `glossary-context.sh`; `glossary-context.sh` prints the company glossary index in Claude Code, and under Oh My Pi the guard extension runs the same script and appends its output to the first user turn. What each hook registers is in [project configuration](REFERENCE.md#project-configuration). ECC's `continuous-learning-v2` hooks are not among them; only its lesson schema was borrowed into the learning template ([imported skills](REFERENCE.md#optional-ecc-skill-library)).

## Official marketplace install commands

```text
/plugin install security-guidance@claude-plugins-official
/plugin install code-review@claude-plugins-official
/plugin install pr-review-toolkit@claude-plugins-official
/plugin install commit-commands@claude-plugins-official
/plugin install claude-md-management@claude-plugins-official
/plugin install hookify@claude-plugins-official
/plugin install feature-dev@claude-plugins-official
/plugin install code-modernization@claude-plugins-official
/plugin install context7@claude-plugins-official
/plugin install playwright@claude-plugins-official
/plugin install github@claude-plugins-official
/plugin install atlassian@claude-plugins-official
/plugin install slack@claude-plugins-official
/plugin install sentry@claude-plugins-official
/plugin install session-report@claude-plugins-official
/plugin install project-artifact@claude-plugins-official
```

Code-intelligence (LSP) plugins give Claude diagnostics after every edit. Install one per language in the repository; the plugin does not install the language server binary itself:

```text
/plugin install typescript-lsp@claude-plugins-official
/plugin install pyright-lsp@claude-plugins-official
/plugin install gopls-lsp@claude-plugins-official
/plugin install rust-analyzer-lsp@claude-plugins-official
/plugin install jdtls-lsp@claude-plugins-official
/plugin install kotlin-lsp@claude-plugins-official
/plugin install csharp-lsp@claude-plugins-official
/plugin install php-lsp@claude-plugins-official
/plugin install ruby-lsp@claude-plugins-official
/plugin install swift-lsp@claude-plugins-official
/plugin install clangd-lsp@claude-plugins-official
/plugin install lua-lsp@claude-plugins-official
```

Connector plugins (`github`, `atlassian`, `slack`, `sentry`) add MCP servers that need their own authentication. This repository already declares `context7`, `github` and `atlassian` in [`.mcp.json`](../.mcp.json) ([MCP servers](REFERENCE.md#mcp-servers)), so the marketplace connector plugins are redundant unless you want their extra tooling; reuse an already-approved company connection where one exists. AIDLC skills read remote records and never write them back without explicit authority. The ECC catalog under `mcp-configs/` is a verbatim upstream snapshot; `.mcp.json` is the live configuration.

## Optional code-graph tooling

Two optional tools answer "how does this code hang together" for the skills, which use graphify's committed output when present, treat codegraph as an extra MCP tool the session may expose, and continue without either. `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" doctor` reports whether each executable is installed; `doctor --install` runs the installers below for the missing ones and nothing else.

graphify ([Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify), Apache-2.0; PyPI name `graphifyy`) turns a repository into a queryable knowledge graph by deterministic AST parsing. Code-only runs are local and need no API key; docs and PDFs are summarised through your assistant. Install once per machine (`uv tool install graphifyy` or `pipx install graphifyy`), then run `/graphify .` in the repository to produce `graphify-out/` (`graph.html`, `GRAPH_REPORT.md`, `graph.json`), which is designed to be committed. `lbvs-aidlc-repo-scout` cites `GRAPH_REPORT.md` under Layout and Hotspots, `/lbvs-aidlc-fix` traces callers with `graphify query "<symbol>"` and `graphify path "<A>" "<B>"`, `/lbvs-aidlc-spike` reads the report and runs queries for its findings, and `/lbvs-aidlc-onboard` offers to build the graph before scouting. `graphify install --project` also writes the `/graphify` skill into `${CLAUDE_PLUGIN_ROOT}/skills/`; keep that repository-local and out of this package.

codegraph ([colbymchenry/codegraph](https://github.com/colbymchenry/codegraph), MIT, about 71k stars) is a pre-indexed, auto-syncing local code graph served as a stdio MCP server (`codegraph serve --mcp`) with one tool, `codegraph_explore`, which returns the relevant symbols' source, call paths and blast radius in one call. Install with `npm install -g @colbymchenry/codegraph` (or the upstream `install.sh`), then run `codegraph install` once per machine and `codegraph init` once per repository. `codegraph install` writes the MCP server entry into the agent configuration, appends a marker-fenced CodeGraph section to the repository's `CLAUDE.md` and `AGENTS.md` and sets auto-allow permissions for Claude Code, so run it in the adopting repository, review the resulting diff before committing it, and do not run it in this package. `codegraph init` creates `.codegraph/`, which is gitignored here. Telemetry is on by default; `codegraph telemetry off` (or `CODEGRAPH_TELEMETRY=0`) turns it off. `codegraph uninstall` reverses the configuration edits. A team may run both tools; neither is required, and no skill installs either.

## Optional third-party plugins

### Compound Engineering (non-technical entry)

The AIDLC stages assume an engineer at the keyboard. Product owners and other non-technical originators can enter through CE brainstorming instead: `ce-brainstorm` interviews them in plain language and returns a brief that `lbvs-aidlc-intent` imports as the intent source. Engineers set the plugin up and help the originator run it; the contract is in the [workflow guide](WORKFLOW.md#optional-compound-engineering-discovery).

This repository declares the plugin at project scope in `.claude/settings.json`, which pins it without installing it; each engineer runs the install once per clone ([CE availability](USAGE.md#ce-availability)). A repository that adopted only the skills adds the marketplace as well:

```text
/plugin marketplace add EveryInc/compound-engineering-plugin
/plugin install compound-engineering@compound-engineering-plugin --scope project
```

This route needs Claude Code plus the plugin (v3.26.3 reviewed; MIT), so the originator either works in Claude Code with an engineer or hands the brief to one. The playbook's own route for non-engineers is claude.ai or Cowork with a GitHub connector committing `intent.md` on their behalf into a shared intent home; that avoids Claude Code but needs the connector and a watched intent folder that this package does not set up. CE brainstorming is the lighter local option; the claude.ai or Cowork route scales better across an organisation. Neither is required for ordinary engineer-led intent.

### Caveman (bundled, lite by default)

The `lbvs-aidlc` plugin carries the MIT `caveman` skill from [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) and applies its lite level to chat replies at session start through `style-mode.sh` (Claude Code) and the guard extension (Oh My Pi), so both hosts behave the same without a second install. Lite drops filler, pleasantries and hedging but keeps articles and full sentences; code, commits, PR bodies, `changes/` artifacts and lessons are never compressed, and caveman's auto-clarity rules win for warnings and ordered steps. The other levels are `full`, `ultra` and `off`; where the level is set is in the `style-mode.sh` row of [project configuration](REFERENCE.md#project-configuration), and "normal mode" turns it off for the current session. Evidence from the upstream README: a JetBrains paired A/B over 86 tasks measured about 8.5 % fewer output tokens with no detectable quality change; this package has not measured its own sessions. The upstream plugin's hooks, its `full` default and the BSL-1.1 engine and proxy are not imported; install the upstream plugin at user scope only if you want its `/caveman` toggles.

## Distribution note

The package is also published as a Claude Code plugin marketplace from the committed `plugins/lbvs-aidlc/` tree on `main`; routes, pinning and install steps are in [distribution](REFERENCE.md#distribution) and the [adoption recipe](USAGE.md#11-install-the-plugin-and-scaffold-a-repository). Company-wide pinning of the recommendations above is a separate decision ([future work](../FUTURE_WORK.md#f7--company-adoption-and-spec-driven-additions)).
