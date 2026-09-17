# lbvs-aidlc

The company AIDLC package: an AI-native development lifecycle for Claude Code based on [Anthropic's AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook) and the [Claude Code best practices](https://code.claude.com/docs/en/best-practices).

**Intent → design → plan → build → verify → review → fixes and re-review**, with a bug-fix evidence loop and durable lessons.

One orchestrator, `/aidlc <change-id>`, starts a change, runs each stage skill and stops at a **stage gate**: it summarises outputs and asks you to proceed, revise or stop before the next stage. The stage skills are also invocable on their own and Claude may load them when your request matches. Three utilities stay manual (`/aidlc-handoff`, `/aidlc-resume`, `/aidlc-ideate`). Evaluation runners, configuration-regression gates, approval enforcement, delivery (**CircleCI later**) and maintenance remain deferred.

An additional **37 ECC skills** provide optional engineering patterns and explicitly selected operational guidance; they supplement the lifecycle and are unchanged by this package's AIDLC work. Bundled Claude Code skills and marketplace plugins worth pairing with each stage are listed in [docs/PLUGINS.md](docs/PLUGINS.md); nothing is installed automatically.

**Start with the [practical usage recipes](docs/USAGE.md).** See the [workflow contract](docs/WORKFLOW.md), [artifact conventions](docs/ARTIFACTS.md), and [review options](.claude/skills/aidlc-review/references/review-options.md) for detail.

## Distribution

| Branch | Form | Use |
| --- | --- | --- |
| `main` | Repo template — `python3 scripts/aidlc.py package <new-dir>` exports a standalone tree | Primary. New services start from the export; existing repositories merge the relevant files explicitly. |
| `plugin-marketplace` | Claude Code plugin marketplace — `.claude-plugin/marketplace.json` + generated `plugins/lbvs-aidlc/` | Teams that want namespaced, versioned skills (`/lbvs-aidlc:aidlc <id>`) installed per repository via `extraKnownMarketplaces` + `enabledPlugins` in `.claude/settings.json`, or fleet-wide via managed settings. |

```sh
# plugin route
claude plugin marketplace add mkhan-lb/lbvs-aidlc#plugin-marketplace
claude plugin install lbvs-aidlc@lbvs-aidlc
```

The plugin carries the AIDLC skills, both agents, the project-mode and test-protection hooks and the shared workflow docs (reached via `${CLAUDE_PLUGIN_ROOT}`); it does not carry the ECC library, a `CLAUDE.md` or the package-integrity hook. Regenerate it on that branch with `python3 scripts/build_plugin.py` after changing any AIDLC skill, agent, hook or shared doc.

## Design decisions

- **Instructions.** `AGENTS.md` is the one shared instruction file (under 60 lines, ends with *Things Claude gets wrong here*). `CLAUDE.md` is `@AGENTS.md` plus a Claude-only section and `.omp/AGENTS.md` is `@../AGENTS.md` for Oh My Pi; `check` rejects duplicated text or symlinks. Codex reads `AGENTS.md` directly.
- **Stages are model-invocable.** `/aidlc` orchestrates; each stage ends at an explicit confirmation gate. Only `aidlc-handoff`, `aidlc-resume` and `aidlc-ideate` are manual.
- **Hooks stay narrow and deterministic.** Two `SessionStart` context hooks (package check, project mode) and one `PreToolUse` guardrail that exists only while a bug fix is in progress. No approval gates or formatters — those belong to the adopting repository.
- **Bugs leave evidence.** `/aidlc-fix` commits the failing test before the fix, blocks edits to it while fixing, records `changes/<id>/evidence.md` with Jira/PR/incident references, and offers `/aidlc-learn`.
- **Brownfield is detected, not assumed.** `mode` classifies the repository at session start (≥10 code files or ≥20 commits; `.aidlc/mode` overrides); `/aidlc-onboard` scouts read-only and asks modernize vs stay-legacy before drafting a repository `CLAUDE.md`.
- **Every change runs in a worktree** named `aidlc/<change-id>`; `.worktreeinclude` carries `.env` and local settings into it.
- **Non-technical entry** is optional Compound Engineering brainstorming; **caveman** is per-engineer opt-in; **ECC skills** are vendored and untouched by AIDLC work.

## Status


## Working without ceremony

- **No IDs to remember.** `/aidlc` with no argument resolves the change from the branch (`aidlc/<id>`), then `.aidlc/current`, then the only change without `review.md`, and asks only if none of those answer. `python3 scripts/aidlc.py status` lists every change with the stage artifacts present, the stage reached and the next one; `current` prints just the ID and its source.
- **Descriptive branches with your ticket key.** Change IDs are `^[a-z0-9]+(-[a-z0-9]+)*$`, so prefix the ticket: `vs-1234-order-export`. The `WorktreeCreate` hook then produces `.claude/worktrees/aidlc+vs-1234-order-export` on branch **`aidlc/vs-1234-order-export`** (branched from local `HEAD`) instead of Claude Code's default `worktree-…` name, and copies `.worktreeinclude` files itself. Non-AIDLC worktree names keep the default shape. Because the hook replaces the host's creation logic, Claude Code's worktree sweep leaves these alone: remove one with `git worktree remove`.
- **Gates or auto-advance, your choice.** `/aidlc` asks the flow policy once per run: *confirm each stage*, *auto-advance when clear, stop before build*, or *auto-advance when clear, including build*. Auto-advance requires the stage to have saved **and read back** its artifact with no open questions, no failed or missing required check and no pending CE review; it announces each hop. Review always asks, and so does every commit, push or deployment.
Verified in native sessions (see [verification](docs/VERIFICATION.md#company-aidlc-restructure)): all 13 `aidlc*` commands load from the export and, namespaced, from the plugin; both `SessionStart` hooks fire; the test-protection hook denies edits to a protected test and allows others; Oh My Pi receives the imported instructions, sticky rules and skills. Not yet driven end to end in a native session: a full `/aidlc` stage-gate conversation, `/aidlc-fix` on a real defect, `EnterWorktree`, and CE brainstorming — the next trial.

## Start locally

Python 3 is sufficient for the helper; no third-party Python packages are required. Claude Code and authorised model access are required for the skills.

```sh
python3 scripts/aidlc.py doctor
python3 scripts/aidlc.py check
python3 scripts/aidlc.py mode
python3 scripts/aidlc.py new example-change
```

Replace `example-change` with the real change ID (`^[a-z0-9]+(-[a-z0-9]+)*$`). `new` creates only `changes/example-change/intent.md` as a draft and refuses to overwrite. `mode` prints one line, `AIDLC project mode: greenfield` or `brownfield`, with its reasons; `.aidlc/mode` containing either word overrides detection. None of the commands approve, commit, push or deploy.

For a separate target directory, put the root option before the subcommand: `python3 scripts/aidlc.py --root /path/to/project new example-change`. This creates an intent there; it does **not** install the package into that repository.

### Project configuration

| Asset | Role |
| --- | --- |
| `AGENTS.md` | Canonical shared instructions for every agent host. |
| [`CLAUDE.md`](CLAUDE.md) | `@AGENTS.md` import plus a Claude-specific section; no symlink. |
| `.omp/AGENTS.md` | Imports `@../AGENTS.md` for Oh My Pi. |
| [`.claude/settings.json`](.claude/settings.json) | Registers the three hooks below and declares the Compound Engineering marketplace/plugin at project scope; no permissions, model selection or telemetry. |
| [`.claude/hooks/check-package.sh`](.claude/hooks/check-package.sh) | `SessionStart`: read-only package check (`aidlc.py check`). |
| `.claude/hooks/project-mode.sh` | `SessionStart`: injects the `AIDLC project mode:` line as context. |
| `.claude/hooks/protect-tests.sh` | `PreToolUse` on `Edit\|Write\|MultiEdit\|NotebookEdit`: denies edits to test paths listed in `.aidlc/fix/*.json` while a fix is in progress. |
| [`.claude/rules/`](.claude/rules/package-maintenance.md) | Path-scoped rules; loaded when matching files are touched. |
| `.worktreeinclude` | Copies `.env` and `.claude/settings.local.json` into new worktrees. |

[.mcp.json](.mcp.json) contains only `{"mcpServers":{}}`. `.claude/settings.local.json` is ignored and never exported; `.aidlc/fix/` is ignored. Inherited user/managed settings, hooks and MCP connections still apply. The hooks are integrity and guardrail aids, not approval or security boundaries. See [runtime-file usage](docs/USAGE.md#project-runtime-files-and-shared-instructions).

### Export a complete standalone tree

```sh
python3 scripts/aidlc.py package /path/to/new-aidlc-copy
python3 /path/to/new-aidlc-copy/scripts/aidlc.py check
```

The destination must not exist and its parent must exist. Export includes the declared skills, agents, templates, shared guidance, the helper, settings, hooks, rules, `.worktreeinclude`, the empty MCP map and locally linked reference/evidence files. It does not copy Git history, `changes/` artifacts, solution/ideation stores, `.aidlc/`, local settings, credentials or plugin installations. Content is copied verbatim, **not secret-scanned**; inspect it before sharing.

Launch Claude in the exported tree to use it. For an **existing codebase**, adoption is an explicit reviewed merge: compare and merge the package files with the repository's existing `AGENTS.md`/`CLAUDE.md`, `REVIEW.md`, settings, hooks and safeguards; the exporter never overlays a repository or mutates global settings. `--add-dir` alone is not a supported installation. See the [adoption recipe](docs/USAGE.md#11-export-and-adopt-without-overwriting-a-repository).

## Orchestrator, stages and utilities

Every command accepts exactly one ID matching `^[a-z0-9]+(-[a-z0-9]+)*$`: a change ID, except `aidlc-ideate`, which takes a topic ID. Put context, paths, CE selection and requested actions in conversation, not extra arguments.

| Command | Purpose |
| --- | --- |
| `/aidlc <change-id>` | Start or continue a change: propose a worktree, read the project mode (brownfield without a conventions record runs `aidlc-onboard` first), then run intent → design → plan → build → verify → review with a stage gate after each. |
| `/aidlc-intent <change-id>` | Clarify problem, outcome, scope and questions into `intent.md`. |
| `/aidlc-design <change-id>` | Turn intent and repository context into `spec.md`. |
| `/aidlc-plan <change-id>` | Propose an implementation plan read-only; standalone planning supported. |
| `/aidlc-build <change-id>` | Save the confirmed plan (save-only on request) and implement the agreed scope with task checks. |
| `/aidlc-verify <change-id>` | Exercise changed behaviour; report passed, failed and not-run checks without fixing code. |
| `/aidlc-review <change-id>` | Hand artifacts and evidence to an existing reviewer; collect local findings. |
| `/aidlc-fix <change-id>` | Bug-fix loop: reproduce, commit a failing test, protect it, fix, verify, write `changes/<change-id>/evidence.md` with Jira/PR references, offer a lesson. |
| `/aidlc-onboard` | Brownfield onboarding: `aidlc-repo-scout` conventions report, modernize/legacy decision, proposed repository `CLAUDE.md` and `.claude/rules/` drafts written only on confirmation. |
| `/aidlc-learn <change-id>` | Capture one verified, non-obvious lesson, or honestly skip. |

| Manual utility | Purpose |
| --- | --- |
| `/aidlc-handoff <change-id>` | Immutable snapshot under `changes/<change-id>/handoffs/`. |
| `/aidlc-resume <change-id>` | Read-only orientation from a selected snapshot or current artifacts, then stop. |
| `/aidlc-ideate <topic-id>` | Compare and save candidate directions before a change is chosen. |

**Stage gates.** At the end of each stage the skill summarises the artifact path, decisions, open questions and checks run, then asks: *Proceed to \<next stage\>*, *Revise this stage*, or *Stop here*. Only *Proceed* invokes the next skill; nothing auto-advances. After review the options are *Fix findings (build)*, *Capture lesson (aidlc-learn)*, or *Done*.

**Worktrees.** `/aidlc` and `/aidlc-fix` start by proposing a dedicated branch/worktree named `aidlc/<change-id>` (EnterWorktree when available, otherwise `git worktree add ../<repo>-<change-id> -b aidlc/<change-id>`) and ask before creating it.

Planning does not save `plan.md`; `aidlc-build` saves the exact confirmed proposal after the normal writable transition. The skills are advisory instructions, not security controls; existing repository rules and tool permissions apply. `aidlc-verifier` (Bash-capable) and `aidlc-repo-scout` (Read/Glob/Grep only) are the two subagents. No commit, push, PR, merge or deployment happens without your explicit authorisation.

## Non-technical originators

Product owners and other non-engineers enter through optional Compound Engineering brainstorming (`ce-brainstorm`) with an engineer's help; the returned brief becomes the intent source. See [PLUGINS.md](docs/PLUGINS.md#compound-engineering-non-technical-entry) for setup and a comparison with the playbook's claude.ai/Cowork route.

## Optional ECC skill library

The selected library comes from [ECC](https://github.com/affaan-m/ECC/tree/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills), pinned at `8321021c54d670126ce3b2969d5deb880b4b0c2a`; 37 skills imported into `.claude/skills/`. 26 reference/pattern skills load when relevant; 11 operational skills (`canary-watch`, `codebase-onboarding`, `eval-harness`, `gan-style-harness`, `git-workflow`, `github-ops`, `growth-log`, `jira-integration`, `parallel-execution-optimizer`, `production-audit`, `terminal-ops`) require explicit invocation. The [import manifest](docs/vendor/ecc/manifest.json) records provenance and adaptations; retain the [ECC MIT license](docs/vendor/ecc/LICENSE). [MCP examples](mcp-configs/ecc.mcp-servers.example.json) are reference-only. See [selection guidance](docs/USAGE.md#12-use-the-optional-ecc-skill-library).

## Optional Compound Engineering

Ordinary AIDLC works without CE. Select each integration explicitly in conversation: brainstorming (`aidlc-intent`), document review (`aidlc-design`, `aidlc-plan`), continuity (`aidlc-handoff`, `aidlc-resume`), ideation (`aidlc-ideate`) and lightweight learning capture (`aidlc-learn`). CE **3.26.3** (`EveryInc/compound-engineering-plugin`, MIT) is *declared* at project scope in [`.claude/settings.json`](.claude/settings.json) via `extraKnownMarketplaces` and `enabledPlugins`, which pins the marketplace and plugin for everyone; **each engineer still runs the install once per clone** — a trial in a fresh clone showed the declaration alone does not materialise it locally (verified: 0 CE skills before `claude plugin install compound-engineering@compound-engineering-plugin --scope project`, 35 after). Declaring the plugin is not selecting it either: skills ask before any CE handoff, and report **prepared — not run** when it is absent. Contracts reference commit `082c83e0537c803ac1d927daafc2e6eb6962dedf`; see the [workflow guide](docs/WORKFLOW.md#optional-compound-engineering-discovery). Caveman is opt-in at user scope for engineers only ([details](docs/PLUGINS.md#caveman-opt-in-engineers-only)).

## Review and delivery boundaries

Prefer an existing reviewer over a custom engine. [Review options](.claude/skills/aidlc-review/references/review-options.md) supplies scope capture, a complete context packet and provider handoffs. If invocation is unavailable the result is **prepared — not run**, never fabricated findings. Fixes, remote comments, commits, merges and deployment require separate authority.

## Repository layout

```text
.
├── AGENTS.md                    # canonical shared instructions
├── CLAUDE.md                    # @AGENTS.md + Claude-specific section
├── REVIEW.md                    # review policy
├── .omp/AGENTS.md               # @../AGENTS.md for Oh My Pi
├── .mcp.json                    # empty project MCP server map
├── .worktreeinclude             # files copied into new worktrees
├── README.md, GOALS.md, IMPLEMENTATION_PLAN.md, FUTURE_WORK.md
├── .claude/
│   ├── settings.json            # SessionStart + PreToolUse hooks
│   ├── settings.local.json      # ignored local {}; never exported
│   ├── hooks/                   # check-package.sh, project-mode.sh, protect-tests.sh
│   ├── rules/                   # path-scoped rules
│   ├── skills/
│   │   ├── aidlc/               # orchestrator
│   │   ├── aidlc-intent/ … aidlc-review/   # stage skills with templates
│   │   ├── aidlc-fix/           # evidence template
│   │   ├── aidlc-onboard/
│   │   ├── aidlc-learn/, aidlc-ideate/, aidlc-handoff/, aidlc-resume/
│   │   └── <ECC skill>/         # 37 selected bundles
│   └── agents/                  # aidlc-verifier.md, aidlc-repo-scout.md
├── scripts/aidlc.py             # check, doctor, new, package, mode
├── mcp-configs/                 # inactive upstream example catalog
├── docs/                        # USAGE, WORKFLOW, ARTIFACTS, PLUGINS, VERIFICATION, sources/, evidence/, vendor/ecc/
├── .aidlc/                      # mode override; fix/ markers (ignored)
└── changes/<change-id>/         # intent.md, spec.md, plan.md, review.md, evidence.md, handoffs/
```

- [Goals](GOALS.md), [implementation plan](IMPLEMENTATION_PLAN.md), [future work](FUTURE_WORK.md): current scope and deferred work.
- [Plugins](docs/PLUGINS.md), [coverage](docs/COVERAGE.md), [dependencies](docs/DEPENDENCIES.md), [measures](docs/MEASURES.md), [compatibility](docs/COMPATIBILITY.md), [prerequisites](docs/PREREQUISITES.md): reference.
- [Verification](docs/VERIFICATION.md): executed scenarios and limits; [source snapshot](docs/sources/anthropic-playbook.md): unchanged reference.

## License

[MIT](LICENSE). Skills imported from ECC keep their upstream [MIT license](docs/vendor/ecc/LICENSE) and in-file attributions; the [playbook snapshot](docs/sources/anthropic-playbook.md) is reference material, not relicensed.
