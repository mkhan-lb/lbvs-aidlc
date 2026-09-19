# Reference

Package documentation for the maintainer of this repository: what each file contains, which file registers which hook, which helper subcommand does what and which directories are generated. The workflow rules live in [WORKFLOW.md](WORKFLOW.md) and the artifacts in [ARTIFACTS.md](ARTIFACTS.md); this page links to them instead of repeating them. Engineers start with the [README](../README.md) and the [usage recipes](USAGE.md).

## Helper

`scripts/aidlc.py` needs Python 3 and no third-party packages. The skills need Claude Code or another [supported host](#hosts) and model access.

```sh
python3 scripts/aidlc.py doctor [--install]
python3 scripts/aidlc.py check
python3 scripts/aidlc.py conventions [--apply]
python3 scripts/aidlc.py new example-change
python3 scripts/aidlc.py lint-artifacts --root ../my-service example-change
python3 scripts/aidlc.py install ../my-service --apply
aidlc update --apply            # inside an adopting repository; `aidlc` is on PATH while the plugin is enabled
```

| Subcommand | What it does |
| --- | --- |
| `check` | Validates the skills, agents, hooks and their frontmatter, both vendor manifests, the knowledge-store indexes and templates, and every relative link in the docs together with its anchor (`broken anchor: <file> -> <link>`; anchors follow GitHub slug rules: lowercase, punctuation dropped, spaces to hyphens). Rejects duplicated text or a symlink between `AGENTS.md` and `CLAUDE.md`. Parses the [host compliance table](COMPATIBILITY.md#host-compliance). Runs `build_plugin.py --check` (below). |
| `doctor` | Reports `python3`, `git` and `claude`, the optional tools (`graphify`, `codegraph`, `gh`, `omp`) and, for every server in `.mcp.json`, what authentication it needs and whether the variable is set. `doctor --install` also runs the listed installer (`uv tool install` or `pipx`, `npm install -g`, `brew install`) for each missing optional tool; it never installs plugins, edits settings or connects a server. |
| `mode` | Prints one line, `AIDLC project mode: greenfield` or `brownfield`, with its reasons: brownfield when the repository has at least 10 code files or at least 20 commits. `.aidlc/mode` containing either word overrides detection. |
| `status`, `current` | `status` lists every change with its artifacts, the stage reached and the next one. `current` prints the resolved change ID and its source ([resolution order](WORKFLOW.md#change-ids-you-do-not-have-to-remember)). |
| `profile` | Prints `missing`, `fresh` or `stale (<n> manifest commits since <rev>)` for `docs/repo-profile.md`. |
| `report-context` | Prints the facts `/lbvs-aidlc-report` puts in an issue: package repository (from the plugin manifest, else the origin remote), helper layout and plugin version, host (`OMPCODE` or `CLAUDECODE` in the environment), workstation, project name and remote (never its path), mode and scaffold manifest, change in play, `gh auth status`. Home paths become `~`; nothing is filed. |
| `conventions` | Compares the repository with the defaults in `templates/conventions/` (`.editorconfig`, `.pre-commit-config.yaml`, `ruff.toml`, `biome.json`, `CONVENTIONS.md`) and reports, per file, whether the repository already owns that concern (an existing `pyproject.toml`, ESLint or Prettier config or `CONTRIBUTING.md`) or a default is available. `conventions --apply` copies only the missing defaults and never overwrites. |
| `lint-artifacts` | Scans `changes/<change-id>/**/*.md` (every change when the ID is omitted) and `docs/solutions/**/*.md` under `--root` for the mechanical half of the [content boundary](ARTIFACTS.md#content-boundary) with two rules: `session-uri` (`artifact://`, `agent://`, `history://`, `local://`, `xd://`) and `machine-path` (`/Users/`, `/home/`, `/tmp/`, `/var/folders/`, `/private/`, drive letters). It prints one `path:line: <rule> <text>` per hit and exits 1, else `lint-artifacts: clean (<n> files)`. `--stdin` lints piped text; `artifact-guard.sh` uses it. |
| `new` | Creates only `changes/<change-id>/intent.md` as a draft and refuses to overwrite. Replace `example-change` with a real [change ID](WORKFLOW.md#change-ids-you-do-not-have-to-remember). |
| `install`, `sync`, `update` | Scaffold and refresh an adopting repository ([below](#plugins-and-the-repository-scaffold)). |
| `worktree`, `worktree-remove` | The two worktree hooks ([project configuration](#project-configuration)). |

None of the subcommands approve, commit, push or deploy. For a separate target directory, put the root option before the subcommand (`python3 scripts/aidlc.py --root /path/to/project new example-change`); this creates an intent there and does not install the package.

`scripts/build_plugin.py` generates the three plugin trees under `plugins/`, the `.omp/agents/` twins of `.claude/agents/`, the marketplace and Codex manifests, and `docs/glossary/virtualstock-index.md` and `docs/glossary/logicbroker-index.md` from the two glossaries (one line per term with the term, its aliases, its domain and the first sentence of its definition, then the naming traps). Do not hand-edit generated files. `build_plugin.py --check`, and therefore `check`, fails when any generated file differs from its source, a drifted index included.

## Project configuration

| Asset | Role |
| --- | --- |
| `AGENTS.md` | Canonical shared instructions for every agent host. |
| [`CLAUDE.md`](../CLAUDE.md) | `@AGENTS.md` import plus a Claude-specific section; no symlink. |
| `.omp/` | Oh My Pi. `AGENTS.md` imports `@../AGENTS.md`; `RULES.md` holds the sticky rules; `agents/` holds the six agents, generated from `.claude/agents/*.md` by `build_plugin.py` (description verbatim, tools lowercased, `read-summarize: false`). `hooks/pre/aidlc-guards.ts` is an adapter, because omp does not run Claude's shell hooks: it builds the Claude-shaped payload for each event and runs the same scripts (`protect-tests.sh`, `artifact-guard.sh`, `pr-guard.sh`, `scaffold-check.sh`, `style-mode.sh`, `glossary-context.sh` and the helper's `mode`), turning `deny` into a block and `ask` into an omp confirm dialog. No rule lives in the TypeScript. |
| `.vscode/` | Recommends the Claude Code extension and points Copilot Chat's code-generation instructions at `AGENTS.md`. Optional, editor-only. |
| [`.claude/settings.json`](../.claude/settings.json) | Registers this repository's hooks: `SessionStart` runs `check-package.sh`, `project-mode.sh`, `scaffold-check.sh`, `style-mode.sh` and `glossary-context.sh` in that order; `PreToolUse` runs `protect-tests.sh` and `artifact-guard.sh` on the edit tools and `pr-guard.sh` on Bash; `UserPromptExpansion` runs `argument-guard.sh`; `WorktreeCreate` and `WorktreeRemove` run the two worktree scripts. It also declares the CE plugin. The plugin's `hooks/hooks.json` gives adopters the seven scripts from `protect-tests.sh` to `glossary-context.sh` below, with `SessionStart` in the order helper `mode`, `scaffold-check.sh`, `style-mode.sh`, `glossary-context.sh`, and runs `aidlc.py worktree` and `worktree-remove` directly. |
| [`.claude/hooks/check-package.sh`](../.claude/hooks/check-package.sh) | `SessionStart`, this repository only: runs `aidlc.py check`; prints nothing when it passes and the errors as context when it fails. |
| `.claude/hooks/project-mode.sh` | `SessionStart`, this repository only: prints the `AIDLC project mode:` line as context. The plugin runs the helper `mode` for the same line. |
| `.claude/hooks/protect-tests.sh` | `PreToolUse` on `Edit\|Write\|MultiEdit\|NotebookEdit`: denies edits to the test paths listed in `.aidlc/fix/*.json` while a fix is in progress ([fix loop](WORKFLOW.md#bug-fix-evidence-loop)). Markers are looked up in the repository that contains the edited file first, then the session's working tree and `CLAUDE_PROJECT_DIR`, so the hook holds inside worktrees and for a sibling checkout. |
| `.claude/hooks/pr-guard.sh` | `PreToolUse` on `Bash` with `if: Bash(gh *)` and `if: Bash(git push*)`: `gh pr create\|merge\|ready\|edit\|close`, a non-GET `gh api … /pulls…` call or a force-push (`--force*`, `+refspec`) returns `permissionDecision: "ask"`, so the engineer confirms in the permission prompt, also in auto mode. Ordinary `git commit` and `git push` are not hooked. |
| `.claude/hooks/artifact-guard.sh` | `PreToolUse` on the edit tools under `changes/**/*.md` or `docs/solutions/**/*.md`: pipes the new text through `aidlc.py lint-artifacts --stdin` and denies with the hit lines, so the [content boundary](ARTIFACTS.md#content-boundary) is checked at write time. |
| `.claude/hooks/argument-guard.sh` | `UserPromptExpansion` matching `lbvs-aidlc`: blocks a `/lbvs-aidlc*` command whose argument is not one bare ID (`lbvs-aidlc-init` and `lbvs-aidlc-onboard` take none; `lbvs-aidlc-ticket` is exempt), with the reason shown in the transcript. The ID shape is in [WORKFLOW.md](WORKFLOW.md#change-ids-you-do-not-have-to-remember). |
| `.claude/hooks/scaffold-check.sh` | `SessionStart`: when `.aidlc/manifest.json` records a different `plugin_version` from the running plugin, prints one line asking for `aidlc update`. |
| `.claude/hooks/style-mode.sh` | `SessionStart`: prints the reply-style block for chat replies. Level from `AIDLC_STYLE`, else `.aidlc/style` (`lite`, `full`, `ultra`, `off`), else `lite`. What each level means is in [PLUGINS.md](PLUGINS.md#caveman-bundled-lite-by-default). |
| `.claude/hooks/glossary-context.sh` | `SessionStart`: prints a `[aidlc-glossary]` block on the first turn: the company glossary index (one line per term with the term, its aliases, its domain and the first sentence of its definition), the glossary's naming traps, then the path of the full glossary file for the complete entry, usage note and evidence. The company comes from `AIDLC_GLOSSARY`, else the file `.aidlc/glossary`, else the `Company:` line of `docs/repo-profile.md` (`virtualstock` or `logicbroker`, case-insensitive); `off`, an unknown value or no source prints nothing. It reads `docs/glossary/` under `CLAUDE_PLUGIN_ROOT` when set, else under the repository. The block costs roughly two to three thousand tokens once per session instead of a stage reading the 40 KB glossary. |
| `.claude/hooks/worktree-create.sh` | `WorktreeCreate`: runs `python3 scripts/aidlc.py worktree`, which creates `.claude/worktrees/aidlc+<change-id>` on branch `aidlc/<change-id>` from local `HEAD` and copies the `.worktreeinclude` files itself (gitignore syntax, evaluated by git). It refuses invalid change IDs and stale directories that are not worktrees, keeps the default `worktree-<name>` shape for other names and always creates under the main checkout. Because it replaces the host's creation logic, Claude Code's worktree sweep leaves these trees alone. The naming rule is in [WORKFLOW.md](WORKFLOW.md#worktrees). |
| `.claude/hooks/worktree-remove.sh` | `WorktreeRemove`: runs `python3 scripts/aidlc.py worktree-remove`, which removes only paths under `.claude/worktrees/`, never forces (a dirty tree is kept and the refusal reported) and deletes only fully merged auto-named `worktree-*` branches; `aidlc/<id>` branches stay. |
| [`.claude/rules/`](../.claude/rules/package-maintenance.md) | Path-scoped rules, loaded when matching files are touched. |
| `.worktreeinclude` | Copies `.env` and `.claude/settings.local.json` into new worktrees. |
| [`templates/conventions/`](../templates/conventions/CONVENTIONS.md) | The defaults that `conventions --apply` copies. |

## MCP servers

[.mcp.json](../.mcp.json) declares three remote (HTTP) servers and no credentials. `context7` (`https://mcp.context7.com/mcp`) serves current library docs; it works anonymously with lower rate limits, and `CONTEXT7_API_KEY` set to the literal value `Bearer <key>` raises them. `github` (`https://api.githubcopilot.com/mcp/`) requires `GITHUB_PERSONAL_ACCESS_TOKEN`, which `gh auth token` prints for the logged-in account. `atlassian` (`https://mcp.atlassian.com/v2/mcp`) authenticates with OAuth 2.1 in the browser the first time you run `/mcp`. Claude Code asks once per project before connecting project-declared servers; `doctor` reports which variables are set. The ECC catalog under `mcp-configs/` is a verbatim upstream snapshot whose GitHub entry is outdated; the live configuration is `.mcp.json`. `.claude/settings.local.json`, `.aidlc/fix/` and `.codegraph/` are ignored. Inherited user and managed settings, hooks and MCP connections still apply ([runtime files](USAGE.md#project-runtime-files-and-shared-instructions)).

## Plugins and the repository scaffold

`python3 scripts/build_plugin.py` generates three plugins into `plugins/`, listed in [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json), which both Claude Code and Oh My Pi read:

| Plugin | Contents | Enabled |
| --- | --- | --- |
| `lbvs-aidlc` | the 18 `lbvs-aidlc*` skills plus `architecture-decision-records`, `doc-coauthoring`, `unslop` and `caveman`; the six agents; `hooks/hooks.json` and the seven hook scripts; `bin/aidlc` on the Bash PATH; `scripts/aidlc.py`; `docs/{WORKFLOW,ARTIFACTS,USAGE,PLUGINS}.md`; `docs/glossary/` in full (README, template, comparison, both glossaries, both generated indexes); `REVIEW.md`; `templates/conventions/`; `.mcp.json`; `package.json` whose `omp.extensions` loads `omp/aidlc-guards.ts` for Oh My Pi | on install |
| `lbvs-ecc` | the 37 ECC reference skills with their licence and manifest | on install; a repository opts in |
| `lbvs-aidlc-observer` | `continuous-learning-v2` with its observation hooks registered | `defaultEnabled: false`; `claude plugin enable lbvs-aidlc-observer@lbvs-aidlc` |

`PLUGIN_VERSION` in `build_plugin.py` is the release number: bump it, regenerate, commit. Engineers receive the new version on `/plugin marketplace update` (automatically once an administrator sets `autoUpdate: true` on the marketplace in managed settings); Oh My Pi engineers run `omp plugin upgrade`.

An adopting repository holds only its own state. `python3 scripts/aidlc.py install <repo>` reports and `install <repo> --apply` writes `REVIEW.md` when absent, the knowledge-store seeds (`docs/adr/`, `incidents/`, `security/`, `references/`, `playbooks/`, `glossary/`, `platform/`, skipping any store the repository already keeps), `changes/.gitkeep` and `.aidlc/manifest.json` (package source, branch, revision, plugin version, one hash per file, skipped seeds). It never creates or overwrites `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `.claude/settings.json` or `.worktreeinclude`; for each it prints what to merge, including the exact `extraKnownMarketplaces` and `enabledPlugins` block and, for Oh My Pi, the `omp plugin install --scope project` command whose `.omp/plugins/installed_plugins.json` is committed. `sync <repo> [--apply]` compares package, manifest and repository three ways and updates only files you have not edited. `update [--from <pkg>] [--apply]`, run inside the repository, clones the recorded source and runs its `sync`; a manifest from the earlier full install lists the now plugin-provided files as `removed` and deletes nothing. See the [adoption recipe](USAGE.md#11-install-the-plugin-and-scaffold-a-repository).

## Commands

Every command accepts exactly one ID: a change ID, except `lbvs-aidlc-ideate` (a topic ID), `lbvs-aidlc-ticket` (a ticket key or issue URL), `lbvs-aidlc-report` (an optional kind and summary) and `lbvs-aidlc-init` and `lbvs-aidlc-onboard` (none). Context, paths, CE selection and requested actions go in conversation. The ID shape and resolution order are in [WORKFLOW.md](WORKFLOW.md#change-ids-you-do-not-have-to-remember); every stage follows the [stage gates](WORKFLOW.md#stage-gates-and-the-flow-policy) and the [review loop](WORKFLOW.md#review-loop-and-escalation).

| Command | Purpose |
| --- | --- |
| `/lbvs-aidlc <change-id>` | Start or continue a change: propose the worktree, read the project mode, ask the kind of work (*Feature/change*, *Bug fix*, *Spike/investigation*), then run the stages and the review loop. A ticket key is redirected to `/lbvs-aidlc-ticket`. |
| `/lbvs-aidlc-ticket <KEY or issue URL>` | Read a Jira issue (Atlassian MCP) or GitHub issue (`gh issue view` or the github MCP) read-only, derive and confirm `<key>-<slug>`, write `.aidlc/current` and create `intent.md`. Never writes back; asks for pasted text without a connector. |
| `/lbvs-aidlc-spike [change-id]` | Time-boxed read-only investigation saved as `changes/<change-id>/spike.md`; never implements. |
| `/lbvs-aidlc-intent <change-id>` | Clarify problem, outcome, scope and questions into `intent.md`. |
| `/lbvs-aidlc-design <change-id>` | Turn intent and repository context into `spec.md`; runs the read-only `lbvs-aidlc-design-reviewer` before its gate. |
| `/lbvs-aidlc-plan <change-id>` | Propose an implementation plan read-only; saving belongs to build ([why](WORKFLOW.md#saving-a-plan-before-implementation)). |
| `/lbvs-aidlc-build <change-id>` | Save the confirmed plan (save-only on request), then implement one task at a time, ticking each in `plan.md` after its check passes. |
| `/lbvs-aidlc-verify <change-id>` | Exercise changed behaviour and report coverage per R-ID without fixing code ([traceability](WORKFLOW.md#traceability-from-requirement-to-check)). |
| `/lbvs-aidlc-review <change-id>` | Hand artifacts, evidence and diff to an existing reviewer at a tier; record the pass in `review.md`. |
| `/lbvs-aidlc-fix <change-id>` | [Bug-fix loop](WORKFLOW.md#bug-fix-evidence-loop) ending in `evidence.md`. |
| `/lbvs-aidlc-ship [change-id]` | Commit, push and open the PR after a clean review pass, [conventions checker](WORKFLOW.md#pre-pr-conventions-check) first ([shipping](WORKFLOW.md#shipping-a-reviewed-change)). |
| `/lbvs-aidlc-init` | Idempotent, report-first repository setup wizard ([details](WORKFLOW.md#repository-setup-with-lbvs-aidlc-init)). |
| `/lbvs-aidlc-onboard` | Brownfield onboarding; drafts are written only on confirmation ([project mode](WORKFLOW.md#project-mode-and-onboarding)). |
| `/lbvs-aidlc-learn <change-id>` | Capture one verified, non-obvious lesson or skip ([knowledge stores](WORKFLOW.md#knowledge-stores)). |

| Manual utility | Purpose |
| --- | --- |
| `/lbvs-aidlc-handoff <change-id>` | Immutable snapshot under `changes/<change-id>/handoffs/` ([handoff and resume](WORKFLOW.md#durable-handoff-and-resume)). |
| `/lbvs-aidlc-resume <change-id>` | Read-only orientation from a snapshot or the current artifacts, then stop. |
| `/lbvs-aidlc-ideate <topic-id>` | Compare and save candidate directions before a change exists ([ideation](WORKFLOW.md#compare-directions-before-intent)). |
| `/lbvs-aidlc-report [bug \| request] [summary]` | File a `process-bug` or `workflow-request` issue on the package repository from session facts (`report-context`), after a duplicate search and only on **File it**; the record for how the workflow behaved ([content boundary](ARTIFACTS.md#content-boundary)). |

The skills are advisory instructions, not security controls; existing repository rules and tool permissions apply. Six subagents live under `.claude/agents/`, each with an `.omp/agents/` twin; their tools, callers and outputs are in [WORKFLOW.md](WORKFLOW.md#skills-agents-and-hooks) and their provenance under [imported skills](#imported-skills). `/lbvs-aidlc-init` may add repository-specific agents from its bundled `templates/agent.md`.

## Imported skills

| Skill | Source | What it writes |
| --- | --- | --- |
| `architecture-decision-records` | [ECC](https://github.com/affaan-m/ECC) at `8321021c54d670126ce3b2969d5deb880b4b0c2a`, `skills/architecture-decision-records/SKILL.md` | `docs/adr/NNNN-short-title.md` from `docs/adr/template.md` and a row in `docs/adr/README.md`, after you confirm. Upstream references to ECC's `planner` and `code-reviewer` agents mean `lbvs-aidlc-plan` and `lbvs-aidlc-review` here. |
| `doc-coauthoring` | [anthropics/skills](https://github.com/anthropics/skills) at `34040c9c568585f6929bedeaad110ad08f079624`, `skills/doc-coauthoring/SKILL.md` | Nothing on its own; the drafting result is saved through the owning AIDLC skill or knowledge store. |
| `caveman` | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman), `skills/caveman/SKILL.md` (MIT part of a split-licence repository) | Nothing; the reply-style rules that `style-mode.sh` applies. Provenance in [docs/vendor/caveman/manifest.json](vendor/caveman/manifest.json). |
| `unslop` | [cursor/plugins](https://github.com/cursor/plugins) at `e8d856f0273b42ebafe0ec3546bd645709e7c1b0`, `pstack/skills/unslop/SKILL.md` (MIT) | Nothing; thirty numbered rules for removing AI tells, applied to every document this package or an adopting repository writes. Provenance in [docs/vendor/cursor-plugins/manifest.json](vendor/cursor-plugins/manifest.json). |

All four are model-invocable, keep their upstream text and carry one added *AIDLC integration* paragraph. Provenance and hashes live in [docs/vendor/ecc/manifest.json](vendor/ecc/manifest.json) and [docs/vendor/anthropic-skills/manifest.json](vendor/anthropic-skills/manifest.json). The anthropics/skills repository has no root license file and this skill no per-skill license; [NOTICE.md](vendor/anthropic-skills/NOTICE.md) records its README sentence verbatim ("Many skills in this repo are open source (Apache 2.0)").

Four of the six agents under `.claude/agents/` adapt an upstream agent, rewritten rather than copied; the notices are in [docs/vendor/aws-aidlc/](vendor/aws-aidlc/NOTICE.md) and [docs/vendor/ecc/](vendor/ecc/LICENSE):

| Agent | Adapted from |
| --- | --- |
| `lbvs-aidlc-design-reviewer` | awslabs/aidlc-workflows architecture reviewer (MIT-0) |
| `lbvs-aidlc-threat-modeler` | awslabs/aidlc-workflows devsecops agent (MIT-0); false-positive list of ECC's security-reviewer (MIT) |
| `lbvs-aidlc-test-critic` | ECC's pr-test-analyzer (MIT), idea only |
| `lbvs-aidlc-conventions-checker` | awslabs/aidlc-workflows quality and developer agents (MIT-0); ECC's code-reviewer (MIT) |

## Knowledge stores

What goes into a store, when a skill offers a record and how a lesson becomes a rule is in [WORKFLOW.md](WORKFLOW.md#knowledge-stores). This table is each store's path, naming, template and index:

| Store | Record | Template and index |
| --- | --- | --- |
| [`docs/adr/`](adr/README.md) | `NNNN-short-title.md`; superseded, never renumbered or deleted | [`template.md`](adr/template.md); indexed in the README |
| [`docs/incidents/`](incidents/README.md) | `YYYY-MM-DD-short-title.md` | [`template.md`](incidents/template.md); README index |
| [`docs/security/`](security/README.md) | `threat-models/<name>.md`; `findings/YYYY-MM-DD-<source>.md` | [`threat-model-template.md`](security/threat-model-template.md); README index |
| [`docs/references/`](references/README.md) | One row per library in [`libraries.md`](references/libraries.md) | `libraries.md` is both log and index |
| `docs/solutions/` (or the CE `docs_root`) | One lesson per file | [learning template](../.claude/skills/lbvs-aidlc-learn/templates/learning.md) |
| [`docs/platform/`](platform/README.md) (pointer layer, not a store) | `platform.md`, one per adopting service | [`platform.md`](platform/platform.md) template; README |
| `docs/repo-profile.md` (in the adopting repository) | One file with a `Last verified: <date> at <commit>` header | [`repo-profile.md`](../.claude/skills/lbvs-aidlc-onboard/templates/repo-profile.md) in the onboard skill; `aidlc.py profile` reports freshness |
| [`docs/glossary/`](glossary/README.md) | [`logicbroker-glossary.md`](glossary/logicbroker-glossary.md) (58 terms), [`virtualstock-glossary.md`](glossary/virtualstock-glossary.md) (51 terms), the [comparison guide](glossary/logicbroker-glossary-comparison.md) | [`template.md`](glossary/template.md) is the blank entry; `logicbroker-index.md` and `virtualstock-index.md` are generated by `build_plugin.py` and printed at session start by `glossary-context.sh` |
| [`docs/playbooks/`](playbooks/README.md) | `<kebab-title>.md` | [`template.md`](playbooks/template.md); README index |

The store model is adapted from the team-knowledge chapter of AWS's [aidlc-workflows](https://github.com/awslabs/aidlc-workflows/blob/main/docs/harness-engineering/07-team-knowledge.md) and the ADR template shape of the sibling `shared-services-aidlc` repository; the lesson schema comes from ECC's `continuous-learning-v2` ([below](#optional-ecc-skill-library)). Automatic feeds remain [deferred](../FUTURE_WORK.md#f5--maintenance-and-operational-feedback).

## Hosts

| Host | What loads | Gaps |
| --- | --- | --- |
| Claude Code | The `lbvs-aidlc` plugin: skills (`/lbvs-aidlc:*`), six agents, the hooks from `hooks/hooks.json`, `bin/aidlc`, shared docs; `CLAUDE.md` imports `AGENTS.md`. | External-source plugins are not auto-installed from project settings (v2.1.195+): each engineer runs `claude plugin install` once; cloud sessions and managed settings install them. |
| Oh My Pi | The same marketplace (`omp plugin marketplace add`, `omp plugin install --scope project`): plugin skills, the six agents from `agents/`, and `omp/aidlc-guards.ts` loaded through `package.json` `omp.extensions`. The extension runs the plugin's own hook scripts (listed under `.omp/` above) and, when loaded from the plugin, prepends the plugin's `bin/` to PATH so `aidlc <subcommand>` resolves in the bash tool. Verified on a scratch repository from the generated plugin. | No Skill tool: stages are reached through the [skill route](WORKFLOW.md#skill-route). The `reviewer` task agent has no effort argument, so tiers are recorded as `effort not configurable`. No `WorktreeCreate` equivalent: use `git worktree add`. The mode line describes the session root, not a sibling target repository. The package check does not run at start; run `aidlc.py check` yourself. |
| Codex | `AGENTS.md` (verified once); `.codex-plugin/plugin.json` at the repository root and inside `plugins/lbvs-aidlc/` declare the skills and MCP servers for `codex plugin marketplace add mkhan-lb/lbvs-aidlc && codex plugin add lbvs-aidlc@lbvs-aidlc`. | The plugin route is unverified in a Codex session; agents and hooks are unsupported ([host compliance](COMPATIBILITY.md#host-compliance)). |
| VS Code + Copilot Chat | `AGENTS.md` via `.vscode/settings.json` code-generation instructions. | Copilot has no skills, gates or hooks; it only sees the shared instructions. |

Optional tooling (`graphify`, `codegraph`, the GitHub CLI, the Atlassian MCP) is described in [PLUGINS.md](PLUGINS.md#optional-code-graph-tooling); `doctor` reports which are installed and `doctor --install` installs the missing ones.

## Optional ECC skill library

The selected library comes from [ECC](https://github.com/affaan-m/ECC/tree/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills), pinned at `8321021c54d670126ce3b2969d5deb880b4b0c2a`; 38 skills are imported into `.claude/skills/`. 26 reference and pattern skills load when relevant; 12 operational skills (`canary-watch`, `codebase-onboarding`, `continuous-learning-v2`, `eval-harness`, `gan-style-harness`, `git-workflow`, `github-ops`, `growth-log`, `jira-integration`, `parallel-execution-optimizer`, `production-audit`, `terminal-ops`) require explicit invocation. `architecture-decision-records` comes from the same pin but is adapted to write into `docs/adr/` ([imported skills](#imported-skills)). The [import manifest](vendor/ecc/manifest.json) records provenance and adaptations; retain the [ECC MIT license](vendor/ecc/LICENSE). See [selection guidance](USAGE.md#12-use-the-optional-ecc-skill-library).

`continuous-learning-v2` is vendored complete at the pin (`.claude/skills/continuous-learning-v2/`: hooks, `claude --model haiku` observer scripts, instinct CLI) but off by default. Nothing in this package registers its hooks; they run only through the separate `lbvs-aidlc-observer@lbvs-aidlc` plugin (`defaultEnabled: false`), which `/lbvs-aidlc-init` reports on and never enables. When enabled, observations (tool inputs and outputs) and personal instincts are stored under `${XDG_DATA_HOME:-~/.local/share}/ecc-homunculus/`, never in the repository, and the model calls run on that engineer's account. An instinct becomes shared knowledge only when an engineer promotes it through review; `/lbvs-aidlc-learn` stays the confirmed per-change lesson.

## Optional Compound Engineering

Ordinary AIDLC works without CE. Each integration (brainstorming, document review, continuity, ideation, learning capture) is selected in conversation; the contracts are in [WORKFLOW.md](WORKFLOW.md#optional-compound-engineering-discovery) and [CE document review](WORKFLOW.md#optional-ce-document-review). CE 3.26.3 (`EveryInc/compound-engineering-plugin`, MIT) is declared at project scope in [`.claude/settings.json`](../.claude/settings.json) via `extraKnownMarketplaces` and `enabledPlugins`. Each engineer still runs the install once per clone: a trial in a fresh clone had 0 CE skills before `claude plugin install compound-engineering@compound-engineering-plugin --scope project` and 35 after. Contracts reference commit `082c83e0537c803ac1d927daafc2e6eb6962dedf`. Non-technical originators enter through CE brainstorming with an engineer ([PLUGINS.md](PLUGINS.md#compound-engineering-non-technical-entry)). Caveman is opt-in at user scope for engineers only ([details](PLUGINS.md#caveman-bundled-lite-by-default)).

## Design decisions

- **Names carry the package prefix.** Commands are `/lbvs-aidlc` and `/lbvs-aidlc-<stage>`, agents `lbvs-aidlc-<role>`, so they stay distinct from the other AIDLC packages an engineer may have loaded (AWS `aidlc-workflows`, `shared-services-aidlc`, `product-aidlc`) and from the plugin form `/lbvs-aidlc:lbvs-aidlc-<stage>`. The branch prefix `aidlc/<change-id>`, `.aidlc/`, `changes/`, `scripts/aidlc.py`, the `AIDLC project mode:` line and "AIDLC" as the lifecycle name are unchanged. Renamed 2026-09-17; `docs/VERIFICATION.md` keeps the earlier names.
- **One shared instruction file.** `AGENTS.md` (under 60 lines, ends with *Things Claude gets wrong here*); `CLAUDE.md` and `.omp/AGENTS.md` import it, Codex reads it directly.
- **Stages are model-invocable.** Each ends at a [gate](WORKFLOW.md#stage-gates-and-the-flow-policy). Only `lbvs-aidlc-handoff`, `lbvs-aidlc-resume` and `lbvs-aidlc-ideate` are manual.
- **Hooks stay narrow and deterministic.** Seven shell hooks in the plugin plus the helper `mode` line and the worktree entries; this repository adds the package check and the mode-line wrapper. Each injects context, denies a specific write, asks for a specific command or names a worktree; approval gates and formatters belong to the adopting repository ([rules](WORKFLOW.md#skills-agents-and-hooks)).
- **Bugs leave evidence.** `/lbvs-aidlc-fix` writes the failing test first and protects it with `protect-tests.sh` ([evidence loop](WORKFLOW.md#bug-fix-evidence-loop)).
- **Brownfield is detected, not assumed.** `mode` classifies the repository at session start; `/lbvs-aidlc-onboard` scouts read-only before drafting ([project mode](WORKFLOW.md#project-mode-and-onboarding)).
- **Every change runs in a worktree** on branch `aidlc/<change-id>` ([worktrees](WORKFLOW.md#worktrees)); `.worktreeinclude` carries `.env` and local settings into it.
- **Requirements are traceable.** The shapes come from [Kiro specs](https://kiro.dev/docs/specs/), adopted without Kiro's tooling ([traceability](WORKFLOW.md#traceability-from-requirement-to-check)).
- **Review reuses an existing reviewer** in a bounded loop ([review loop](WORKFLOW.md#review-loop-and-escalation), [rule](WORKFLOW.md#review-without-rebuilding-the-reviewer)); [review options](../.claude/skills/lbvs-aidlc-review/references/review-options.md) holds the provider recipes and the packet.
- **Shipping is a skill that always asks.** `/lbvs-aidlc-ship` stays model-invocable so the review and fix gates can hand off to it directly, a deliberate deviation from Claude Code's guidance to mark commit and deploy skills `disable-model-invocation: true` (decided 2026-09-17). The skill's own question is the barrier before any git command, and no flow policy reaches it without the engineer answering the review gate. Flip the frontmatter and `MANUAL_SKILLS` in `scripts/aidlc.py` together if that trade-off changes ([shipping](WORKFLOW.md#shipping-a-reviewed-change)).
- **Current docs, not training data.** Library APIs are resolved through the `context7` MCP first ([rule](WORKFLOW.md#current-documentation-first)).
- **Platform is pointed at, not duplicated.** `docs/platform/` names `Logicbroker/app-template` and the `lb-pipelines/app-delivery-kit-vs@1` orb; each adopting service records its own facts in `platform.md`. Delivery execution through CircleCI stays [deferred](../FUTURE_WORK.md#f4--delivery-integration-through-circleci).
- **Conventions default, never overwrite.** `templates/conventions/` plus `conventions [--apply]`: greenfield adopts the defaults on request, brownfield keeps its own.
- **Lessons carry confidence.** The lesson schema is borrowed from ECC `continuous-learning-v2`; the promotion rule is in [WORKFLOW.md](WORKFLOW.md#knowledge-stores).

## Distribution

One branch, `main`, one marketplace, two halves:

| Half | Where it lives | Who installs it |
| --- | --- | --- |
| Engine | plugins `lbvs-aidlc`, `lbvs-ecc`, `lbvs-aidlc-observer` from `.claude-plugin/marketplace.json` (generated `plugins/` trees committed here) | each engineer once (`claude plugin install`, `omp plugin install`), or the organisation through managed `extraKnownMarketplaces` and `enabledPlugins`; a repository's `.claude/settings.json` declaration tells a teammate what to run |
| Repository state | `aidlc.py install <repo> [--apply]`, refreshed by `sync` and `update` | once per repository, committed with the code: `REVIEW.md`, knowledge-store seeds, `changes/`, `.aidlc/manifest.json` |

```sh
# plugin route
claude plugin marketplace add mkhan-lb/lbvs-aidlc
claude plugin install lbvs-aidlc@lbvs-aidlc
```

The plugin does not carry a `CLAUDE.md` or `AGENTS.md` (the repository's own), the package-integrity hook and maintenance rule (this repository's) or `.worktreeinclude` (repository-owned). Regenerate with `python3 scripts/build_plugin.py` after changing any AIDLC skill, agent, hook, shared doc or glossary, in the same commit; `check` fails on drift.

## Repository layout

```text
.
├── AGENTS.md, CLAUDE.md, .omp/AGENTS.md   # shared instructions and their two importers
├── REVIEW.md                    # review policy
├── .mcp.json                    # context7, github, atlassian; no credentials
├── .worktreeinclude             # files copied into new worktrees
├── .claude/
│   ├── settings.json            # hook registrations; CE plugin declaration
│   ├── hooks/                   # the eleven scripts in the project configuration table
│   ├── rules/                   # path-scoped rules
│   ├── skills/                  # lbvs-aidlc*, the four imported skills, 38 ECC bundles
│   └── agents/                  # the six lbvs-aidlc-* agents
├── scripts/aidlc.py             # the helper
├── scripts/build_plugin.py      # generates plugins/, .omp/agents/, the manifests, docs/glossary/*-index.md
├── .claude-plugin/marketplace.json, plugins/   # the marketplace and its three generated plugins
├── templates/conventions/       # default .editorconfig, .pre-commit-config.yaml, ruff.toml, biome.json, CONVENTIONS.md
├── mcp-configs/                 # inactive upstream catalog
├── docs/                        # USAGE, REFERENCE, WORKFLOW, ARTIFACTS, PLUGINS, COMPATIBILITY, VERIFICATION, sources/, evidence/
│   ├── adr/, incidents/, security/, references/, playbooks/   # knowledge stores
│   ├── glossary/                # both glossaries, comparison guide, entry template, generated *-index.md
│   ├── platform/                # pointer layer; per-repo platform.md
│   └── vendor/                  # manifests, LICENSE and NOTICE files per import
├── .aidlc/                      # mode, style and glossary overrides; current pointer; fix/ markers (ignored)
└── changes/<change-id>/         # intent.md, spike.md, spec.md, plan.md, review.md, evidence.md, handoffs/
```

Other repository documents: [goals](../GOALS.md), [implementation plan](../IMPLEMENTATION_PLAN.md), [future work](../FUTURE_WORK.md), [plugins](PLUGINS.md), [coverage](COVERAGE.md), [dependencies](DEPENDENCIES.md), [measures](MEASURES.md), [compatibility](COMPATIBILITY.md), [prerequisites](PREREQUISITES.md), [verification](VERIFICATION.md), [source snapshot](sources/anthropic-playbook.md).
