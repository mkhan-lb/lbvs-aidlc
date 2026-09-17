# Bundled skills, subagents and plugins by stage

Everything here is a **recommendation**. The package installs nothing by itself: no marketplace registration, plugin, LSP server or MCP connection is added by `python3 scripts/aidlc.py package`, by the hooks or by any `aidlc-*` skill. Two deliberate exceptions are declared, not performed: [`.mcp.json`](../.mcp.json) names three remote MCP servers that Claude Code connects only after you approve them once per project, and `python3 scripts/aidlc.py doctor --install` runs the package-manager installers for missing optional tools (`graphify`, `codegraph`, `gh`) only when you invoke that flag. Install what your team needs with the exact commands below, review each plugin's permissions and context cost in `/plugin` first, and keep company policy (managed settings, allowed marketplaces) authoritative. Inventory checked on 16 September 2026 against the [commands reference](https://code.claude.com/docs/en/commands), [sub-agents](https://code.claude.com/docs/en/sub-agents), [discover plugins](https://code.claude.com/docs/en/discover-plugins) and the [official marketplace catalog](https://github.com/anthropics/claude-plugins-official).

Official marketplace plugins install with `/plugin install <name>@claude-plugins-official`. Third-party plugins first need `/plugin marketplace add <owner>/<repo>`.

## Stage table

| Stage | AIDLC entry | Bundled Claude Code skills / subagents to use | Official marketplace plugins worth installing |
| --- | --- | --- | --- |
| Onboard (brownfield) | `/aidlc-onboard`, `aidlc-repo-scout` agent, `python3 scripts/aidlc.py mode` | `/init` with `CLAUDE_CODE_NEW_INIT=1` as the alternative CLAUDE.md bootstrap; Explore subagent for read-only repository research; `/doctor` for setup and CLAUDE.md trims; existing `inherit-legacy-style` skill when staying legacy | `claude-md-management`, `code-modernization` (modernize route), one LSP plugin per language (below), `context7` for current library docs |
| Ticket intake | `/aidlc-ticket <KEY or issue URL>` → confirmed change ID + seeded `intent.md` | AskUserQuestion to confirm the derived ID; `gh issue view` for GitHub issues when the CLI is authenticated | `atlassian` (Jira read via `getJiraIssue`), `github` (issue read) — both declared in `.mcp.json`; the skill never writes back |
| Spike | `/aidlc-spike [id]` → `changes/<id>/spike.md` | Explore subagent and `aidlc-repo-scout` for read-only research; `graphify query`/`path` when `graphify-out/` exists; `/deep-research` for external questions | `context7` (current library docs), `codegraph` MCP when installed; `architecture-decision-records` at the end gate |
| Intent | `/aidlc <id>` → `aidlc-intent` | AskUserQuestion interview; Explore subagent for grounding in current behaviour; `doc-coauthoring` to structure a long intent with a stakeholder | `atlassian` (Jira source records), `github` (issues/PRs), `slack` (originator threads); optional `compound-engineering` `ce-brainstorm` (below) |
| Design | `aidlc-design` | Plan subagent for read-only research; `/design` only where Claude Design is available; `architecture-decision-records` when the spec fixes a boundary, technology or contract; `docs/security/threat-model-template.md` for a new interface, store, credential or trust boundary — both offered, never automatic | `feature-dev` (structured feature design), `context7`, `security-guidance` (design-time security hints) |
| Plan | `aidlc-plan` | Native plan mode (`Shift+Tab`), Plan/Explore subagents; `/batch` only for a change that decomposes into independent worktrees and PRs | `feature-dev`, `atlassian` (link the plan to the ticket) |
| Build | `aidlc-build` | `/goal` for a completion condition; `/run` and `/run-skill-generator` to drive the app; `/simplify` after the diff is green; `/fewer-permission-prompts` to trim repeated prompts | LSP plugin for the language (diagnostics after each edit), `commit-commands`, `hookify` (turn a repeated correction into a hook), `playwright` for browser-driven UI checks |
| Verify | `aidlc-verify`, `aidlc-verifier` agent | `/verify` (user-invoked) to build and run the change; `/run`; `/debug` when a session misbehaves | `playwright`, `sentry` (compare against live errors when authorised) |
| Review | `aidlc-review`, root `REVIEW.md` | `/code-review` (bundled; also `/review`), `/security-review` where available (save triaged results as `docs/security/findings/YYYY-MM-DD-security-review.md` on request), fresh-context subagent for adversarial review; Compliance check reports an architectural change without an ADR as a finding | `code-review`, `pr-review-toolkit`, `security-guidance`, `github` (PR comments only with explicit authority) |
| Fix / evidence | `/aidlc-fix <id>` → `changes/<id>/evidence.md` | Failing-test-first loop with `protect-tests.sh` active; `/verify` and `/run` for observed proof; `/debug`; offer of `docs/incidents/YYYY-MM-DD-<slug>.md` for alert/incident-sourced defects and `docs/security/findings/` for security defects | `sentry` (incident/alert references), `atlassian` and `github` (Jira key and PR URL in the evidence), `playwright` (screenshots/recordings) |
| Learn | `aidlc-learn` | `/skill-doctor` to keep skills lean; `/doctor` to trim CLAUDE.md after a lesson lands in it; a recurring correction becomes a rule, not another lesson | `claude-md-management`, `session-report` (what the session actually did), `project-artifact` |
| Cross-cutting | `/aidlc`, hooks, `.claude/rules/`, `python3 scripts/aidlc.py status` and `current` to find the change in play | `/doctor`, `/skill-doctor`, `/fewer-permission-prompts`, `/batch`, Explore/Plan/general-purpose subagents, `/loop` for repeated checks | `hookify`, `claude-md-management`, `context7`, LSP plugins, `github`, `atlassian`, `slack`, `sentry`, `session-report`, `project-artifact` |

Bundled skills are prompt-based and ship with the CLI; `/verify` and `/deep-research` are user-invoked only. A project skill with the same name replaces the bundled one, so keep the `aidlc-*` names distinct from bundled names.

Two project-local mechanics interact with these tools. The helper `python3 scripts/aidlc.py` owns `check`, `doctor`, `new`, `mode`, `status`, `current`, `worktree` and `package`; its `doctor` and `status` are unrelated to the bundled `/doctor` command or any plugin command of the same word. The four registered hooks are `check-package` and `project-mode` (SessionStart), `protect-tests` (PreToolUse) and `worktree-create` (WorktreeCreate) — the last one replaces the host's worktree naming, so a worktree requested as `aidlc/<change-id>`, including one started from `/batch`, lands in `.claude/worktrees/aidlc+<change-id>` on branch `aidlc/<change-id>` and carries the `.worktreeinclude` files. Installing a plugin does not change either mechanism.

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

Connector plugins (`github`, `atlassian`, `slack`, `sentry`) add MCP servers that need their own authentication. This repository already declares **context7**, **github** and **atlassian** as remote HTTP servers in [`.mcp.json`](../.mcp.json) with no credentials in the file: context7 works anonymously with lower rate limits and takes an optional `CONTEXT7_API_KEY` whose value must be `Bearer <key>`; github requires `GITHUB_PERSONAL_ACCESS_TOKEN` (`gh auth token` prints one); atlassian authenticates by OAuth 2.1 in the browser the first time you run `/mcp`. Claude Code asks once per project before connecting them, and `python3 scripts/aidlc.py doctor` reports which variables are set. Installing the marketplace connector plugins on top is redundant unless you want their extra tooling; reuse an already-approved company connection where one exists. AIDLC skills read remote records and never write them back without explicit authority. The ECC catalog under `mcp-configs/` remains a verbatim upstream snapshot (its GitHub entry is outdated); `.mcp.json` is the live configuration.

## Optional code-graph tooling

Two tools answer "how does this code hang together" for the skills. Both are optional; the AIDLC skills use graphify's committed output when present, treat codegraph as an extra MCP tool the session may expose, and continue without either. `python3 scripts/aidlc.py doctor` reports whether each executable is installed and `doctor --install` runs the installers below for the missing ones — nothing else.

**graphify** ([Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify), Apache-2.0; PyPI name `graphifyy`) turns a repository into a queryable knowledge graph by deterministic AST parsing — code-only runs are local and need no API key; docs/PDFs are summarised through your assistant. Install once per machine (`uv tool install graphifyy` or `pipx install graphifyy`), then run `/graphify .` in the repository to produce `graphify-out/` (`graph.html`, `GRAPH_REPORT.md`, `graph.json`), which is designed to be committed. The AIDLC skills use it when present and continue without it: `aidlc-repo-scout` cites `GRAPH_REPORT.md` under Layout and Hotspots, `/aidlc-fix` traces callers with `graphify query "<symbol>"` and `graphify path "<A>" "<B>"`, `/aidlc-spike` reads the report and runs queries for its findings, and `/aidlc-onboard` offers to build the graph before scouting. `graphify install --project` also writes the `/graphify` skill into `.claude/skills/`; keep that repository-local and out of this package.

**codegraph** ([colbymchenry/codegraph](https://github.com/colbymchenry/codegraph), MIT, about 71k stars) is a pre-indexed, auto-syncing local code graph served as a stdio MCP server (`codegraph serve --mcp`) that exposes a single tool, `codegraph_explore`, returning the relevant symbols' source, call paths and blast radius in one call. Install with `npm install -g @colbymchenry/codegraph` (or the upstream `install.sh`), then run `codegraph install` once per machine and `codegraph init` once per repository. Note what `codegraph install` does: it writes the MCP server entry into the agent configuration, appends a marker-fenced CodeGraph section to the repository's `CLAUDE.md`/`AGENTS.md` and sets auto-allow permissions for Claude Code — so run it in the **adopting repository**, review the resulting diff before committing it, and do not run it in this package. `codegraph init` creates `.codegraph/`, which is gitignored here. Telemetry is on by default; turn it off with `codegraph telemetry off` (or `CODEGRAPH_TELEMETRY=0`). `codegraph uninstall` reverses the configuration edits.

Positioning: graphify gives a **committed, reviewable graph** plus the `/graphify` skill and CLI queries that the AIDLC skills cite by path; codegraph gives a **live-synced local index behind MCP** that any agent in the session can query without a build step. A team may run both; neither is required, and no skill installs either.

## Optional third-party plugins

### Compound Engineering (non-technical entry)

The AIDLC stages assume an engineer at the keyboard. Product owners and other non-technical originators can enter through CE brainstorming instead: `ce-brainstorm` interviews them in plain language and returns a brief that `aidlc-intent` imports as the intent source. Engineers set the plugin up and help the originator run it; the contract is in the [workflow guide](WORKFLOW.md#optional-compound-engineering-discovery).

In this repository (and its exports) the plugin is already declared at project scope in `.claude/settings.json`; it installs after workspace trust. For a repository that adopted only the skills, add it by hand:

```text
/plugin marketplace add EveryInc/compound-engineering-plugin
/plugin install compound-engineering@compound-engineering-plugin --scope project
```

Requirements and limits: this route needs Claude Code plus the plugin (v3.26.3 reviewed; MIT), so the originator either works in Claude Code with an engineer or hands the brief to one. The playbook's own route for non-engineers is claude.ai or Cowork with a GitHub connector committing `intent.md` on their behalf into a shared intent home; that avoids Claude Code entirely but needs the connector and a watched intent folder that this package does not set up. CE brainstorming is the lighter local option; the claude.ai/Cowork route scales better across an organisation. Neither is required for ordinary engineer-led intent.

### Caveman (opt-in, engineers only)

Caveman is a skill plus two hooks that compress Claude's chat replies (fragments, no filler); code, commits, docs and PR text stay in normal prose. Evidence from its README: a JetBrains paired A/B over 86 tasks measured about 8.5 % fewer output tokens with no detectable quality change; on agentic coding sessions most tokens are code and tool calls that the skill does not touch. Its terse output is not suitable for non-technical readers, so install it only at **user scope** for engineers who want it, never in project settings:

```text
/plugin marketplace add JuliusBrussee/caveman
/plugin install caveman@caveman --scope user
```

The separate caveman proxy (`@caveman-ai/cli`) is BSL-1.1 licensed and sends anonymous telemetry by default; it is not part of this recommendation.

## Distribution note

Company-wide pinning of these recommendations through `extraKnownMarketplaces`/`enabledPlugins` or managed settings, and publishing this package itself as a marketplace plugin, are tracked on a separate branch (see [future work](../FUTURE_WORK.md#f7--company-adoption-and-spec-driven-additions)). The repo-template export remains the supported distribution.
