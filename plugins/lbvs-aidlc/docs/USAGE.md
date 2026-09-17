# Practical AIDLC usage

Use this guide for the conversation, command, expected result, and next action at each step. The [workflow contract](WORKFLOW.md), [artifact conventions](ARTIFACTS.md), and [verification record](VERIFICATION.md) provide policy and evidence; the recipes below are instructions, not claims that their examples have been executed.

## Before you start

- Open the intended repository in Claude Code with the complete project resources available. Copying one skill or using the helper's `--root` does not install the workflow. The [standalone export recipe](#11-export-and-adopt-without-overwriting-a-repository) produces a new tree; existing-repository adoption remains an explicit reviewed merge.
- Every ID-taking AIDLC command accepts **at most one ID** matching `^[a-z0-9]+(-[a-z0-9]+)*$`, and a ticket key fits as a lowercase prefix (`vs-1234-order-export`). Omit the argument and the command resolves the change itself — branch name, then `.aidlc/current`, then the only change without `review.md` — and says which source it used. `/aidlc-ideate` still takes a topic ID before a change exists and has no such fallback; `/aidlc-onboard` takes no ID; `/aidlc-ticket` takes the ticket key or issue URL and derives the change ID for you; `/aidlc-ship [change-id]` resolves like the rest. Put requests, paths, CE choices, the flow policy, review tiers and review targets in conversation, never after the ID.
- In the recipes, send the **Say** text as an ordinary conversation message, then invoke the separate **Run** slash command. Adapt the example scope to your application; do not copy its requirements blindly.
- Use a normal writable session for saving artifacts, handoff creation, and implementation. Enter native plan/read-only mode yourself for `/aidlc-plan`; the agent does not change permissions. Confirmation of a proposal does not change the mode or authorise unrelated actions.
- CE (Compound Engineering) is optional upstream tooling, not bundled prompts. It runs only when selected and the required skill is loaded in the current session. An installation record is not proof of availability. See [missing CE](#when-ce-or-a-source-is-unavailable).
- Local work does not require a PR, CI, an approval service, or an evaluation runner. Existing repository rules, organisational safeguards, and tool permissions still apply. None of these commands implicitly authorises commit, stash, push, publication, merge, deployment, or remote-record updates.

`/aidlc [change-id]` runs **intent → design → plan → build → verify → review**, resolving the ID itself when you omit it and stating one flow policy for the run: each stage then asks at its gate, or auto-advances when that policy allows it and nothing is open. It asks whether the work is a feature/change, a bug fix or a spike/investigation and routes the last two to `/aidlc-fix` and `/aidlc-spike`. After review it drives the [review loop](#local-implementation-review) — fix, verify, re-review at a higher tier, at most three fix cycles — and offers `/aidlc-ship` once a pass is clean. You can also invoke any stage skill directly, and Claude may load one when your request matches. `/aidlc-ticket` starts a change from a Jira key or GitHub issue, `/aidlc-spike` records a time-boxed investigation, `/aidlc-fix` is the bug-fix evidence loop, `/aidlc-onboard` the brownfield entry, `/aidlc-learn` the lesson capture and `/aidlc-ship` the commit/push/PR step that always asks. **Handoff**, **resume** and **ideation** are the only manual-only utilities. Start each new change or fix in its own worktree — branch `aidlc/<change-id>`, directory `.claude/worktrees/aidlc+<change-id>`; the orchestrator proposes it and asks first.

### Project runtime files and shared instructions

Keep these files with the complete package when adopting it:

| File | Purpose and boundary |
| --- | --- |
| `AGENTS.md` | Canonical shared instructions for every agent host. `CLAUDE.md` is `@AGENTS.md` plus a Claude-specific section; `.omp/AGENTS.md` imports `@../AGENTS.md` for Oh My Pi. No symlink is involved. |
| [`.claude/settings.json`](../.claude/settings.json) | Official-schema settings registering the four hooks below. No permissions, model/provider selection or telemetry are configured. |
| [`.claude/hooks/check-package.sh`](../.claude/hooks/check-package.sh) | `SessionStart` (startup/resume): executes `python3 "${CLAUDE_PROJECT_DIR}/scripts/aidlc.py" check`, read-only. |
| `.claude/hooks/project-mode.sh` | `SessionStart`: runs `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" mode` and injects its one-line result as context. Override detection with `.aidlc/mode` containing `greenfield` or `brownfield`. |
| `.claude/hooks/protect-tests.sh` | `PreToolUse` on `Edit\|Write\|MultiEdit\|NotebookEdit`: denies edits to any path listed under `protected` in `.aidlc/fix/*.json`. Active only while a fix marker exists; `.aidlc/fix/` is ignored by Git. |
| `.claude/hooks/worktree-create.sh` | `WorktreeCreate`: runs `python3 scripts/aidlc.py worktree`, replacing the host's default naming. The requested name `aidlc/<change-id>` becomes the directory `.claude/worktrees/aidlc+<change-id>` on branch `aidlc/<change-id>`, branched from local `HEAD`; other names keep `worktree-<name>`. A missing or unusable name fails the hook, and worktree creation fails with it. |
| [`.claude/rules/`](../.claude/rules/package-maintenance.md) | Path-scoped rules loaded when matching files are touched; guidance, not enforcement. |
| `.worktreeinclude` | Lists the ignored files copied into a worktree created for a change (`.env`, `.claude/settings.local.json`). Because the `WorktreeCreate` hook replaces the default behaviour, the hook performs that copy itself. |
| [`.mcp.json`](../.mcp.json) | Declares three remote HTTP MCP servers and no credentials: `context7` (anonymous, or `CONTEXT7_API_KEY` whose value must be `Bearer <key>`), `github` (`GITHUB_PERSONAL_ACCESS_TOKEN`, e.g. from `gh auth token`) and `atlassian` (OAuth 2.1 in the browser the first time you run `/mcp`). Claude Code asks once per project before connecting them. The ECC catalog under `mcp-configs/` is a verbatim, partly outdated upstream snapshot; this file is the live configuration. |

`.claude/settings.local.json` was created here as `{}` for local overrides. It is ignored, never exported and not required in an exported tree; create it there only if needed for separately reviewed local choices. Do not put credentials into shared files.

Launch Claude from the adopted package root with `sh` and Python 3 available. When project hooks are allowed, the package check and mode line run on startup/resume, **not every turn or edit**; the test-protection hook runs on every edit tool call but denies only paths in an active fix marker, and the worktree hook runs only when a worktree is created. To investigate a failure, run the helper from that root — its subcommands are `check`, `doctor` (add `--install` to run the `uv`/`pipx`, `npm` or `brew` installer for each missing optional tool: `graphify`, `codegraph`, `gh`), `mode`, `status`, `current`, `conventions` (add `--apply` to copy only the missing default convention files; see [adopt or keep conventions](#adopt-or-keep-conventions)), `worktree`, `package` and `new` (for example `python3 scripts/aidlc.py check`). `doctor` also lists every server in `.mcp.json` with the authentication it needs and whether the variable is set; it does not test connectivity. The hooks are integrity and guardrail aids, not lifecycle verification, an approval gate or security enforcement; apart from naming a worktree, they do not advance stages.

Project MCP declarations and the local settings object do not clear inherited user/managed configuration. Existing settings, hooks, permissions, plugins and MCP connections can still apply, and policy may restrict project customizations or block the declared servers. Review the effective configuration in your own session; this setup adds no tool grants. See [compatibility boundaries](COMPATIBILITY.md).

These are native Claude project files plus shared instruction text in `AGENTS.md`, which other hosts read directly. One native Codex instruction-discovery smoke passed against the earlier symlinked layout; that is not native Codex skill/hook parity or a complete workflow compatibility claim. No `.agents/skills` mirror is supplied. See the [executed checks and limits](VERIFICATION.md#minimal-project-configuration-and-shared-instructions).

### CE availability

Compound Engineering **3.26.3** is declared at project scope in `.claude/settings.json` (`extraKnownMarketplaces` → `EveryInc/compound-engineering-plugin`, `enabledPlugins` → `compound-engineering@compound-engineering-plugin`). The declaration pins which marketplace and plugin to use; it does **not** install it for you locally. In a fresh clone the skill catalog showed zero `compound-engineering:*` skills until the install ran, so each engineer runs it once per checkout:

```sh
claude plugin install compound-engineering@compound-engineering-plugin --scope project
```

Then `/reload-plugins` or a new session, and confirm `compound-engineering:ce-brainstorm` is listed. Cloud sessions install repo-declared plugins at start. If the plugin is missing, `aidlc-intent` says so and offers reload/install or ordinary clarification — it never pretends CE ran, and it decides availability from the session catalog alone rather than searching the filesystem.

This package supplies exactly 16 `aidlc*` commands: `aidlc` plus `aidlc-build`, `aidlc-design`, `aidlc-fix`, `aidlc-handoff`, `aidlc-ideate`, `aidlc-intent`, `aidlc-learn`, `aidlc-onboard`, `aidlc-plan`, `aidlc-resume`, `aidlc-review`, `aidlc-ship`, `aidlc-spike`, `aidlc-ticket` and `aidlc-verify`. An earlier trial session with user-scope plugins enabled listed 21 `aidlc*` commands against the then 13: `aidlc-workflows@ai-skills` adds seven namespaced commands (`aidlc-workflows:doctor`, `:install`, `:providers`, `:service-plugin`, `:setup`, `:status`, `:update`) and `eng@ai-skills` adds `eng:aidlc-eval`. Those eight are namespaced, so they do not shadow the project skills; the confusion is for the reader, since a bare word like `status` or `doctor` may mean the plugin command `aidlc-workflows:status` or this package's helper subcommand `python3 scripts/aidlc.py status`. Check `/skills` when a command behaves unexpectedly: it lists each command's source.

Declaring the plugin is not selecting it: every CE handoff still happens only when you ask for it in conversation, and skills say **prepared — not run** when it is unavailable. Run `/ce-setup` once per repository if you want a non-default `docs_root`; AIDLC reads `.compound-engineering/config.yaml` before touching solution or ideation stores.

The integration contracts were reviewed at CE **3.26.3**, commit `082c83e0537c803ac1d927daafc2e6eb6962dedf`; re-check them after upstream upgrades. Non-technical originators use the same plugin through `ce-brainstorm` with an engineer's help; other recommended bundled skills and plugins are listed per stage in [PLUGINS.md](PLUGINS.md).

## Run a whole change with `/aidlc`

**Prerequisite/mode:** the intended repository open in Claude Code, writable session, a change ID. Starting from a Jira key or GitHub issue instead? Use [`/aidlc-ticket`](#0a-start-from-a-ticket) first; `/aidlc VS-1234` is not a change ID and the orchestrator will say so.

**Say:**

> Start order-export: add a CSV export for the currently filtered order list, keeping the existing access rules. Work in a dedicated worktree. Stop at each stage gate for my decision.

**Run:**

```text
/aidlc order-export
```

**Expect:** step 0 proposes the worktree for `aidlc/order-export` — the EnterWorktree tool, which this project's `WorktreeCreate` hook turns into `.claude/worktrees/aidlc+order-export` on branch `aidlc/order-export`, otherwise `git worktree add ../<repo>-order-export -b aidlc/order-export` — and waits for your answer. The orchestrator states the flow policy for the run (here `Flow policy: confirm each stage`, because you asked to stop at each gate), then reads the `AIDLC project mode:` line; brownfield with no repository `CLAUDE.md`/conventions record runs `/aidlc-onboard` first. It then asks the kind of work — **Feature/change**, **Bug fix** (hands over to `/aidlc-fix`) or **Spike/investigation** (hands over to `/aidlc-spike`). For a feature, each stage skill runs in order and ends with a summary—artifact path, decisions, open questions, checks run—and the question **Proceed to \<next stage\>** / **Revise this stage** / **Stop here**. Plan still runs read-only and build saves the confirmed plan first, as in the recipes below.

**Next:** answer each gate. After review choose **Fix findings (build)**, **Re-review at higher effort**, **Open PR (aidlc-ship)**, **Capture lesson (aidlc-learn)** or **Done**. **Stop here** leaves the artifacts in place; re-run `/aidlc order-export` or the individual stage later. Nothing is committed, pushed or merged without your explicit instruction — `/aidlc-ship` asks before it commits.

### Run a change without remembering its ID

**Prerequisite/mode:** the repository open, any session. Useful when you come back to work started days ago, or in a worktree whose branch already carries the ID.

**Run first:**

```sh
python3 scripts/aidlc.py status
```

**Expect:** one line per `changes/<id>/` with the stage artifacts present, the stage reached, the next stage, the handoff count, and `*` against the change currently in play, followed by the resolved current change and where it came from. A present file is not proof its stage is finished — read the artifact. `python3 scripts/aidlc.py current` prints just `<change-id>\t<source>` and exits 1 when nothing resolves.

**Then run:**

```text
/aidlc
```

**Expect:** the orchestrator resolves the ID from the branch (`aidlc/<id>`, `aidlc+<id>`, `worktree-aidlc/<id>`, `worktree-aidlc+<id>`), then `.aidlc/current`, then the only change without `review.md`, and tells you which source it used. If nothing resolves it shows the same status list and asks, proposing a slug from your actual request with the ticket key as a prefix when you have given one — it never invents a ticket key and never creates `changes/<id>/` from an unresolved ID. For new work the resolved ID is recorded in `.aidlc/current`, which is machine-local and ignored by Git, so it is not part of a handoff or an export.

**Next:** carry on at the stage gate. Naming the ID explicitly (`/aidlc vs-1234-order-export`) always wins over resolution.

### Choose a flow policy

**Prerequisite/mode:** a run of `/aidlc` or any stage skill. The policy is conversation text, not a command argument.

**Say one of:**

> Flow policy: confirm each stage

> Flow policy: auto-advance when clear, stop before build

> Flow policy: auto-advance when clear, including build

**Expect:** confirm-each-stage is the default and is also what every skill assumes if you say nothing. Under an auto-advance policy a stage continues on its own **only** when it saved and read back its artifact, recorded no open questions, unresolved decisions or missing inputs, had no failed check and no required check left "not run", has no pending requested CE review, and is not about to start build (unless you chose "including build") or a commit, push, PR, merge, publication or deployment. It then prints one line — `Auto-advancing to <next stage> (policy: ...; no open questions, checks: ...)` — invokes the next stage and reminds you that you can interrupt. Under **including build** only, the review loop's fix → verify → re-review cycles may also continue by themselves, announcing each hop, until a pass is clean or three fix cycles have run.

**Always asked:** review's gate (the review pass always shows its findings and asks the post-review gate, whatever the policy), anything under confirm-each-stage, any unmet condition above, the step into build under "stop before build", a stage that ended read-only or unsaved, both `/aidlc-fix` questions (authorising the failing-test commit and its closing gate), and `/aidlc-ship`'s commit/push/PR question. No gate is ever answered for you, and no skill claims a policy you did not state.

**Next:** change the policy at any time by stating a different one; the next stage uses the policy in force when it finishes.

## Onboard a brownfield repository

**Prerequisite/mode:** an existing codebase; `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" mode` reports `brownfield`, or you want a conventions review anyway. Writable mode only for the confirmed writes at the end.

**Say:**

> Onboard this repository. Report its conventions before proposing anything; do not write files until I confirm.

**Run:**

```text
/aidlc-onboard
```

**Expect:** the read-only `aidlc-repo-scout` agent returns a structured conventions report (stack, layout, build/test/lint commands, naming, error handling, test patterns, hotspots, existing `CLAUDE.md`/`AGENTS.md`/`.cursorrules`, risks), and `python3 scripts/aidlc.py conventions` runs in report mode — which convention files the repository already owns versus which defaults exist — with the repository's own tooling recorded in the `CLAUDE.md` draft, never replaced. You are asked **Modernize (adopt current patterns)**, **Stay legacy (inherit existing style)** or **Decide later**. Legacy invokes `inherit-legacy-style`; modernize recommends the `code-modernization` plugin and relevant pattern skills without installing them. Then a proposed repository `CLAUDE.md` (≤60 lines, including "Things Claude gets wrong here") and path-scoped `.claude/rules/` drafts are shown, with `/init` under `CLAUDE_CODE_NEW_INIT=1` offered as the alternative.

**Next:** confirm explicitly to write the drafts, `.aidlc/mode` and `docs/onboarding.md`; otherwise nothing is written. Keep the repository `CLAUDE.md` short and edit it when Claude repeats a mistake.

## Adopt or keep conventions

The package ships defaults in [`templates/conventions/`](../templates/conventions/CONVENTIONS.md) — `.editorconfig`, `.pre-commit-config.yaml` (whitespace/EOF fixes, YAML/JSON validation, large-file and private-key detection, gitleaks, ruff, biome), `ruff.toml`, `biome.json` and `CONVENTIONS.md` (branch, commit-title and PR rules that `/aidlc-ship` follows). A **greenfield** repository adopts them; a **brownfield** repository keeps its own.

**Prerequisite/mode:** any session for the report; a writable session and your explicit choice for `--apply`.

**Run first:**

```sh
python3 scripts/aidlc.py conventions
```

**Expect:** one line per default file. `repository owns it: <files>` means an equivalent already exists (`pyproject.toml`, `.eslintrc*`/`eslint.config.*`, `.prettierrc`, `lefthook.yml`, `.husky`, `CONTRIBUTING.md` all count) and nothing will be copied for it; `missing — default available` means `--apply` would copy that file. The closing line depends on the project mode: greenfield is told to adopt or record its own conventions in `CLAUDE.md`; brownfield is told to keep its conventions, which `aidlc-onboard` records.

**Then, greenfield only** — either accept the `/aidlc-onboard` offer **Adopt default conventions (`python3 scripts/aidlc.py conventions --apply`)** or run it yourself:

```sh
python3 scripts/aidlc.py conventions --apply
pre-commit install
```

**Expect:** only the missing files are copied (`copied default`); an existing file is never overwritten, and the command says how many it copied. Review the diff, pin the hook revisions in `.pre-commit-config.yaml`, then install the hooks. Later, `aidlc-build` runs the repository's pre-commit/lint before declaring a task done; in a greenfield repository with none, it mentions `conventions --apply` rather than inventing a linter.

**Brownfield:** run only the report; keep the repository's tooling and let `aidlc-onboard` record it in the `CLAUDE.md` draft. Copy a single default (`cp templates/conventions/.editorconfig .`) only where the repository truly has nothing for that concern. Changing a default in `templates/conventions/` is an ADR, not a drive-by edit. When the project also needs cloud delivery, read [`docs/platform/README.md`](platform/README.md): new services start from `Logicbroker/app-template` (fetch its `AGENT-SETUP.md` with an authenticated `gh api`; raw links 404) and each adopting repository fills its own [`docs/platform/platform.md`](platform/platform.md) for design and plan to read.

## 0. Compare ideas before choosing a change

Use ideation when the question is **which improvement to pursue**. Brainstorming in step 2 instead clarifies an already-selected problem.

**Prerequisite/mode:** a real repository focus, ordinary writable mode for a saved result. The topic ID does not create `changes/<topic-id>/`. Read-only ordinary mode returns an unsaved proposal.

**Say:**

> Explore small improvements to the existing order-export experience using this repository's code, docs and relevant lessons. Compare alternatives, reject weak or already-solved ideas, and recommend up to three candidates. Use ordinary AIDLC without CE. Save the ideas, but do not choose a change, write requirements, implement or run checks.

**Run:**

```text
/aidlc-ideate export-experience
```

**Expect:** a ranked Markdown artifact under `docs/ideation/`, or the valid configured artifact root, with source-backed bases, tradeoffs, unknowns and rejection reasons. The exact saved path is read back and reported. Speculative value stays labelled; zero qualifying survivors is valid. An existing destination is not overwritten.

**Next:** select an idea by title/rank and the **actual returned source path**, then say:

> Explore the selected idea from the exact ideation file above as order-export. Read that source, retain its evidence, tradeoffs and open questions, and capture intent without CE. Selection is not approval of every proposed detail or permission to implement.

Then invoke `/aidlc-intent order-export`. No intent/brainstorm stage is started automatically.

### CE ideation or a selected prior source

To opt in, replace the ordinary request with:

> Use Compound Engineering ideation for export-experience, focused only on this repository's order-export flow. Output Markdown; skip web research and external providers. Native ideation agents and temporary scratch are acceptable. Return to AIDLC idea selection without publishing, opening a browser, committing or starting another workflow.

Run the same `/aidlc-ideate export-experience`. The actual loaded `compound-engineering:ce-ideate` runs its grounding/generation/critique mechanism with `output:md`; this is not the brainstorming return API. Scratch may remain. If unavailable, choose ordinary work or arrange loading yourself; if read-only, defer CE or select ordinary unsaved ideation.

For refinement, provide the exact existing ideation path and specify the change to save before invoking the same utility. No newest-file selection or silent overwrite occurs. If importing into intent, CE authorship does not require CE installation: ordinary intent reads the selected Markdown and records provenance.

## 0a. Start from a ticket

Use this when the work already exists as a Jira issue or GitHub issue and you want the change ID and intent derived from the record rather than typed.

**Prerequisite/mode:** writable session; read access to the ticket through whatever is actually connected — the `atlassian` MCP server declared in `.mcp.json` (approve it once via `/mcp`) for Jira keys, or `gh auth login` / the `github` MCP server for GitHub issues. With neither available the skill says so and asks you to paste the ticket text; it never invents summary, acceptance criteria or a key.

**Say:**

> Pick up VS-1234. Read the ticket, propose the change ID and seed the intent from it. Do not change the ticket.

**Run:**

```text
/aidlc-ticket VS-1234
```

**Expect:** the fetched summary, description and acceptance criteria shown back with the ticket link; a proposed ID such as `vs-1234-order-export` (`<key-lowercase>-<slug>`, at most 40 characters, `^[a-z0-9]+(-[a-z0-9]+)*$`) to confirm or edit; on confirmation `.aidlc/current` is written and `changes/vs-1234-order-export/intent.md` is created from the intent template with the ticket's content in Context and its URL under sources, then read back. The closing question offers **Continue with /aidlc (worktree, stages)** or **Stop here**. Nothing is written back to Jira or GitHub, and no worktree exists yet.

**Next:** choose *Continue* to let `/aidlc` propose the worktree and run the stages with the resolved ID, or stop and refine the intent by hand. Passing `VS-1234` to `/aidlc` directly is not a change ID; the orchestrator will point you back to this recipe.

## 0b. Run a time-boxed spike

Use a spike when a real question — feasibility, how an existing subsystem works, which of two approaches survives contact with the code — has to be answered before an intent or design is honest. A spike never implements.

**Prerequisite/mode:** any session for the investigation; writable mode to save `spike.md`. Optional: `graphify-out/` in the repository, the `context7` MCP server for library docs, `codegraph` when installed. The change ID resolves as usual (argument, branch, `.aidlc/current`, only open change) or is proposed for confirmation.

**Say:**

> Spike whether the order-export CSV can stream from the existing pagination layer without loading all orders into memory. Time box: two hours of investigation. "Answered" means we know which layer would change, what breaks, and a recommendation with a fallback. Read-only — no code changes.

**Run:**

```text
/aidlc-spike order-export
```

**Expect:** an AskUserQuestion confirming the question, the time box and the "answered" criteria before any research; read-only investigation through the Explore subagent, `aidlc-repo-scout`, graphify queries when a graph exists, and repository docs; then `changes/order-export/spike.md` from the spike template — Question, Time box, Findings with file/URL sources, Options with trade-offs, Recommendation, Open questions, Suggested next step — saved and read back. The end gate offers **Create/refresh intent from this spike (aidlc-intent)**, **Record an ADR (architecture-decision-records)** or **Stop here**. Unanswered parts stay listed as open questions; the time box is reported as agreed, not measured.

**Next:** pick *Create/refresh intent* to have `/aidlc-intent order-export` read the spike as a source, or *Record an ADR* when the spike settled an architectural choice — the ADR skill writes `docs/adr/NNNN-<title>.md` and its index row only after you confirm the draft.

## 1. Start with a clear request, without CE

**Prerequisite/mode:** ordinary writable session; a conversation is sufficient input. An existing change can be updated without replacing unrelated work.

**Say:**

> For order-export, add a CSV export for the currently filtered order list. Keep the existing access rules; do not add scheduled exports. Capture this as intent without CE. Ask about requirements that are still unclear.

**Run:**

```text
/aidlc-intent order-export
```

**Expect:** `changes/order-export/intent.md`, grounded in the request and relevant existing behavior, plus open questions and a next step. No spec or implementation is implied. In read-only mode, expect proposed text instead of a save.

**Next:** correct misunderstandings and confirm direction in conversation, then use design below. For a read-only draft, move normally to writable mode and explicitly request saving that intent with the same intent command.

## 2. Optionally brainstorm before settling intent

Use this instead of a second discovery interview when the outcome or approach is unclear. Clear requirements do not need brainstorming.

**Prerequisite/mode:** writable session, with `compound-engineering:ce-brainstorm` available if CE is selected. CE brainstorming can write supporting files, so it is deferred in plan/read-only mode.

**Say:**

> For order-export, use Compound Engineering brainstorming to clarify what users need from order exports, then return to AIDLC intent. Keep scheduled exports out of scope. Do not plan, implement, or ship through CE.

**Run:**

```text
/aidlc-intent order-export
```

**Expect:** same-conversation discovery through upstream CE, then the returned brief or exact saved discovery document is incorporated into `changes/order-export/intent.md`. A CE document is supporting source material, not a second specification or the canonical implementation plan. Blockers and unsettled decisions remain visible.

**Next:** resolve the questions and proceed to ordinary design. CE completion is not human approval or permission to build.

## 3. Design, then propose a plan

### Save requirements and design

**Prerequisite/mode:** working intent and a writable session.

**Say:**

> Turn the order-export intent into requirements and design using the existing code. Use ordinary AIDLC without CE. Save the spec, preserve the agreed scope, and surface remaining decisions. Do not implement.

**Run:**

```text
/aidlc-design order-export
```

**Expect:** `changes/order-export/spec.md` with observable requirements, boundaries, affected components, design choices, and open questions. Acceptance criteria are EARS lines with stable IDs — `R1.1 WHEN the user exports the filtered list THE export service SHALL stream rows in the current filter order`, `R1.2 IF the user lacks the orders permission THEN THE export service SHALL return 403` — and later tasks and checks refer to those IDs. Where the design leans on a library, framework or cloud API, the skill resolves current docs through the `context7` MCP (`resolve-library-id`, then `query-docs`) before writing and cites the Context7 ID and the repository's pinned version; a lookup that settled a real question adds a row to [`docs/references/libraries.md`](references/libraries.md). If `docs/platform/platform.md` exists it is read first, and a new data store, queue or integration gets a platform entry and a threat-model offer. Before the gate, the read-only `aidlc-design-reviewer` agent returns **READY** or **NOT READY** with numbered findings (requirements coverage and EARS quality, consistency with ADRs, platform fit, NFR gaps, missing threat model); the skill summarises that verdict as one input to your decision, never as approval. If the design introduces or changes an architectural boundary, technology choice or contract, an AskUserQuestion offers to record an ADR through the `architecture-decision-records` skill (`docs/adr/NNNN-<title>.md` plus an index row, drafted for your confirmation); if it introduces a new external interface, data store, credential or trust boundary, a second question offers a threat model at `docs/security/threat-models/<name>.md` from the template — accepted, it delegates the STRIDE table to the read-only `aidlc-threat-modeler` agent for you to confirm. Declining either changes nothing. In read-only mode this is a proposal only; an explicit writable request to the same command owns saving it.

**Next:** discuss unresolved choices, then enter native plan mode.

### Propose without saving

**Prerequisite/mode:** native plan/read-only mode; intent/spec available, or explicitly supplied task context with missing artifacts identified. Standalone planning is possible but must not invent an accepted baseline.

**Say:**

> Propose an implementation plan for order-export from the saved intent and spec. Identify affected files, dependencies, task checks, and unresolved choices. Do not save project files or implement.

**Run:**

```text
/aidlc-plan order-export
```

**Expect:** a code-grounded proposal in the conversation, not a write to `changes/order-export/plan.md`: numbered checkbox tasks such as `- [ ] T1.2 Add the streaming export endpoint … _Requirements: R1.1, R1.2_` with `depends on: T1.1` where order matters, and a coverage check that every R-ID from the spec appears in at least one task (or the exclusion is stated). Deployment, observability or promotion work appears as values files and pipeline config for the delivery orb named in `docs/platform/platform.md`, not hand-rolled infrastructure. The handoff identifies the exact proposal or any actual native scratch-plan path, outstanding decisions, and pending requested CE document review. A native plan file is machine-local scratch state, not the canonical plan or a CE review target.

**Next:** discuss revisions and explicitly confirm the exact proposal. Preserve its complete text or actual accessible scratch file if changing sessions. A summary, status label, or handoff saying “confirmed” cannot recover a lost proposal or replace current-user confirmation.

## 4. Save the confirmed plan only

`aidlc-plan` never owns the project-file save. `aidlc-build` owns the authorised transition to the canonical plan, including a **save-only** request.

**Prerequisite/mode:** leave plan mode through the normal user-controlled transition into a writable session. The exact confirmed proposal must remain available, with material blockers resolved or explicitly handled. If it is in a native scratch file, name the actual path in conversation; do not guess one.

**Say:**

> I confirm the order-export proposal immediately above. Save only that exact proposal to changes/order-export/plan.md, then stop. Do not edit application code, run tests or builds, invoke review, or start implementation.

**Run:**

```text
/aidlc-build order-export
```

**Expect:** the canonical `changes/order-export/plan.md` is saved and its path reported; no application edits, task checks, review invocation, or implementation follows. The command must not overwrite a newer conflicting plan or infer confirmation from a handoff. If still read-only, it stops without writing.

**Next:** request optional review of this saved version, or explicitly request implementation when ready. Creating a handoff is not an alternative plan-save operation.

## 5. Optionally review a saved spec or plan with CE

CE document review critiques a document; `aidlc-review` later reviews implementation/diffs. Neither is approval.

### Saved spec

**Prerequisite/mode:** the exact intended version exists at `changes/order-export/spec.md`; `compound-engineering:ce-doc-review` is loaded. The review itself is read-only/report-only.

**Say:**

> Use Compound Engineering document review on the saved changes/order-export/spec.md. Report findings through AIDLC using the current provider. Do not redraft, apply corrections, write a report file, or implement.

**Run:**

```text
/aidlc-design order-export
```

**Expect:** conversational findings, actual reviewer coverage, limitations, and remaining decisions. The saved spec is unchanged by the review.

**Next:** decide which findings to address. Request authorised spec corrections separately through design; review a revised version again if needed.

### Saved plan

**Prerequisite/mode:** native plan/read-only mode, the exact proposal saved canonically by the previous recipe, and the CE review skill loaded.

**Say:**

> Use Compound Engineering document review on the saved changes/order-export/plan.md. Review this version, not a new proposal or native scratch file. Return report-only findings using the current provider; do not fix or implement.

**Run:**

```text
/aidlc-plan order-export
```

**Expect:** findings and outstanding decisions without changing the plan. An unsaved chat proposal or old saved version is not silently substituted for the requested version.

**Next:** discuss findings. If the plan needs revision, ask `aidlc-plan` to propose it read-only, confirm that exact revision, and use the save-only recipe in writable mode. Review does not authorise those changes or erase unresolved questions.

## 6. Save and build, with a pending-review stop

**Prerequisite/mode:** writable session, confirmed scope/approach, and authority for local implementation and relevant checks. The canonical plan may already exist; if not, the exact confirmed proposal must still be accessible.

**Say:**

> I confirm the order-export proposal above. Save it to the canonical plan if needed, then implement the agreed scope and exercise the relevant local checks. If the CE document review we requested is still pending, save the plan but stop before implementation; do not invoke that review automatically.

**Run:**

```text
/aidlc-build order-export
```

**Expect:** without a pending requested review, implementation one task at a time — in plan order, or the task you name — with spec and plan in context: each task's own check runs, and `[ ]` becomes `[x]` in `plan.md` only after that check passed, never ahead. Library code is written against Context7-resolved docs, and the repository's pre-commit/lint runs before a task is declared done (greenfield with none: the skill mentions `conventions --apply` instead of inventing a linter). Aligned artifacts and actual passed/failed/not-run task-check evidence follow. With a pending requested CE document review, expect the save and an explicit stop for that review—not a build, automatic CE call, or invented approval.

**Next when stopped:** enter plan mode, run the saved-plan CE review recipe, and resolve findings. Then return to writable mode and explicitly request implementation with `/aidlc-build order-export`. If you decide not to use CE, say so explicitly; an unavailable plugin does not silently cancel a requested review.

## 7. Pause and create a durable handoff

A handoff is an immutable **supporting snapshot**, not a replacement for authoritative intent, spec, plan, or review artifacts. It records the real stage: for example, unfinished planning or pending review, not automatically “ready to build.”

### Ordinary AIDLC snapshot

**Prerequisite/mode:** writable authority for the snapshot. Plan/read-only mode cannot create it; transition normally first. Saving an unsaved canonical plan is a separate explicit request, not a side effect of handoff creation.

**Say:**

> Pause order-export and create an ordinary AIDLC handoff without CE. Focus on the pending plan-review decisions and unfinished work. Use a descriptive filename under changes/order-export/handoffs/. Do not save or change the canonical plan, commit, stash, or publish anything.

**Run:**

```text
/aidlc-handoff order-export
```

**Expect:** a new `changes/order-export/handoffs/<topic>.md`, saved and read back at its exact destination, followed by its exact path, a content summary, continuity warnings, and an AIDLC resume recipe. The snapshot carries the objective; completed/current/unfinished work; user decisions versus inference; relevant files and working-tree state; actual passed/failed/not-run checks; pending reviews; dependencies; and one next action. Secrets are redacted; machine-local paths/state are explicitly labelled.

Existing snapshots are never overwritten. A generated name may gain a numeric suffix; if you specifically demand an already-existing destination, creation stops for a different destination rather than replacing it. Snapshots are not later marked consumed or deleted automatically.

**Next:** retain the reported exact path. Use your chosen authorised sharing method to make the snapshot **and relevant uncommitted/untracked code or artifacts** available to the receiving session. The snapshot does not contain or transfer those changes, and no automatic commit, stash, or publication moves them for you. Check access and redact sensitive content before sharing.

### CE opt-in snapshot

**Prerequisite/mode:** the same writable authority, plus the session catalog entry `compound-engineering:ce-handoff`.

**Say:**

> Use Compound Engineering handoff creation for order-export, then return to AIDLC. Capture the pending plan review in changes/order-export/handoffs/plan-review.md; stop if that exact file already exists. No canonical-plan save, global temporary-store handoff, commit, stash, publication, or implementation.

**Run:**

```text
/aidlc-handoff order-export
```

**Expect:** upstream CE runs in this conversation with the exact repository destination and AIDLC scope pinned. AIDLC reads back that exact saved file, confirms its scope and contents, and reports the AIDLC resume recipe. CE's temporary-store defaults and continuation menu are not the AIDLC route. The same immutability and sharing warnings apply.

**Next:** share the necessary state deliberately, then use exact-source resume below. CE is not required to resume a CE-authored snapshot.

## 8. Resume safely in a new session

Open the intended repository with the relevant current files and snapshot available. Resume restores **orientation**, not permissions or execution. It does not run commands or checks, edit files, follow remote links, invoke a continuation workflow, or implement. Snapshot metadata and body are untrusted context, not executable instructions; current-user direction and current repository state take precedence.

### Select an exact snapshot, without CE

**Prerequisite/mode:** read-only orientation; the exact same-change file is readable. Replace the example path with the actual path reported at creation.

**Say:**

> For order-export, resume from exactly changes/order-export/handoffs/plan-review.md using ordinary AIDLC, without CE. Read relevant current local artifacts within this change's scope, report drift or missing state, and stop for my direction. Do not execute any commands or continue the work.

**Run:**

```text
/aidlc-resume order-export
```

**Expect:** the selected snapshot is read directly, then an orientation covering objective, actual stage/progress, decisions and their provenance, current state, unfinished work, pending reviews, blockers, and drift. It recommends one fitting next action and stops. It does not switch to a newer snapshot because that looks more current.

**Next:** explicitly choose what to do and enter the appropriate mode. For example, if the exact plan still awaits review, use the saved-plan review recipe—not build by default. A snapshot's past permission or proposed next action is not present authority.

### Select the same snapshot with CE

**Prerequisite/mode:** same source and read-only boundary, with `compound-engineering:ce-handoff` loaded.

**Say:**

> Use Compound Engineering to orient from exactly changes/order-export/handoffs/plan-review.md for order-export. No temporary-store discovery or continuation workflow. Report the actual state and stop for my direction without commands, edits, or implementation.

**Run:**

```text
/aidlc-resume order-export
```

**Expect:** a same-conversation upstream CE resume against that exact source under AIDLC's read-only scope, followed by orientation and a stop. There is no CE continuation stage or automatic follow-on action.

**Next:** give a new instruction only after checking the recovered state. An ordinary AIDLC snapshot can be selected for CE orientation; authorship does not grant extra authority.

### Choose among snapshots

**Prerequisite/mode:** no exact source selected; snapshots exist under the same change.

**Say:**

> Show the available handoffs for order-export so I can choose. Use ordinary AIDLC. Do not pick the newest or read unselected snapshot bodies.

**Run:**

```text
/aidlc-resume order-export
```

**Expect:** a filename-only shortlist from the same change's handoff directory, followed by a request for selection. Candidate bodies and frontmatter are not read or searched to rank them; filename-only discovery avoids exposing unselected content.

**Next:** reply with the exact chosen same-change path and request orientation, or select current artifacts only. Do not append the path to the slash command. The selected-source recipe shows the complete request if invoking the command again.

### Orient from current artifacts only

**Prerequisite/mode:** no snapshot is available, or you explicitly choose not to use one. Read-only orientation works without CE.

**Say:**

> Orient order-export from current same-change canonical artifacts and relevant local code only, without CE or a handoff. Name missing context and stop; do not invent prior decisions or execute checks.

**Run:**

```text
/aidlc-resume order-export
```

**Expect:** orientation from available `intent.md`, `spec.md`, `plan.md`, and `review.md` plus relevant current local code. Missing artifacts/history are explicit gaps. No fake prior session, completed review, confirmation, or successful check is inferred.

**Next:** supply missing context or direct the appropriate stage. If snapshots exist, explicitly selecting current artifacts avoids the snapshot-choice step.

### When CE or a source is unavailable

| Situation | Safe result and your next action |
| --- | --- |
| CE selected but not loaded | The command offers installation/reload or an explicitly labelled ordinary AIDLC fallback and otherwise stops. It never installs, fetches, enables, or substitutes automatically. Arrange upstream installation/loading yourself if wanted, then retry; or say “Use ordinary AIDLC instead.” An already-stated fallback choice is honoured. |
| Selected snapshot is missing or unreadable | The access problem is reported; no automatic newest-file substitution. Supply the exact accessible same-change file, choose a different snapshot, or explicitly choose current artifacts only. |
| Snapshot depends on another machine's worktree, native scratch plan, ignored file, or temporary path | Missing machine-local state is reported, not reconstructed from a summary. Make the actual necessary state available through an authorised method or revise the continuation scope. A lost full plan requires recovering or reproposing and confirming it before saving. |
| Snapshot is stale or disagrees with current files | Material drift is named. Current files and user direction govern; the command does not rewrite artifacts or silently choose another source. Decide whether to reconcile, choose another snapshot, or orient from current artifacts. |
| Source is sparse, unrelated, or points outside the selected change | Context gaps or scope mismatch are reported, and orientation stops rather than forcing a history. Select the correct same-change source or provide current context. |

Native CLI **resume/continue** restores a locally available conversation through the host's own session mechanism. It is not a portable repository handoff, does not make machine-local files available elsewhere, and is separate from `/aidlc-resume`. Use the host's current documentation for its session controls; use the repository snapshot and deliberately shared working state for a new session or teammate that cannot access that history.

The optional CE continuity contract was inspected at [CE 3.26.3, commit `082c83e`](https://github.com/EveryInc/compound-engineering-plugin/blob/082c83e0537c803ac1d927daafc2e6eb6962dedf/skills/ce-handoff/SKILL.md). Availability and compatibility must still be checked in the actual session; that source reference is not a claim of successful runtime verification. See [recorded scenarios and limits](VERIFICATION.md).

## 9. Verify, review, fix, and re-review

### Exercise behavior without fixing it

**Prerequisite/mode:** implemented change, authorised local/disposable runtime environment; not read-only plan mode. Checks can have side effects even when source edits are prohibited.

**Say:**

> Verify order-export against the saved spec and plan using the authorised local environment. Exercise the changed behavior, report passed, failed, and not-run checks, and do not fix code. Return evidence in the conversation.

**Run:**

```text
/aidlc-verify order-export
```

**Expect:** a table `R-ID | check | observed result | not run (reason)` with one row per acceptance criterion from `spec.md`, so an uncovered requirement shows as a row rather than hiding behind a green command; plus observed evidence and limitations, not automatic source edits or a saved report. If needed, separately request saving the evidence with writable permission. A build alone is not proof of behavior.

**Next:** request review of the actual diff and evidence, or direct fixes for demonstrated failures.

### Local implementation review

**Prerequisite/mode:** actual working-tree/diff scope, same-change artifacts, verification evidence, and an available reviewer. No PR is required.

**Say:**

> Review the order-export implementation and local working-tree diff against its artifacts and actual verification evidence. Use an available local reviewer and tell me which ran. Return findings locally; do not edit code or post remote comments.

**Run:**

```text
/aidlc-review order-export
```

**Expect:** an actual returned report, a partial report with named gaps, or **prepared — not run** with a filled context packet and separate documented command. The first pass runs at the **standard** tier (`/code-review high`); say `escalated`, `maximum` or `cloud` only if you want `xhigh`, `max` or `ultra` — cloud is multi-agent review that costs more and needs the cloud feature. Each finding is **Important** or **nit** per `REVIEW.md` (the repository's own file, else `${CLAUDE_PLUGIN_ROOT}/REVIEW.md`) and carries a stable ID (`R1`, `R2` …) that later passes reuse. Loading/launching is not completion. The packet includes real tracked and untracked scope, artifact/policy contents, check evidence and prior findings. `changes/order-export/review.md` records the pass with its tier, findings and disposition; the wrapper reads it back. The post-review gate then asks exactly **Fix findings (build)**, **Re-review at higher effort**, **Open PR (aidlc-ship)**, **Capture lesson (aidlc-learn)** or **Done**.

Claude's bundled `/code-review` does not accept the packet as trailing notes: non-cloud trailing text is the review target, and its fork is not guaranteed to inherit parent chat. If the wrapper cannot establish a supported context channel, follow the reported transfer step rather than pretending that pasting a preceding message delivered the packet. Any resulting code-only review with unconfirmed artifact/policy coverage is partial.

In an explicitly selected existing OMP session, `/review` → **Custom review instructions** accepts the completed packet. Include untracked file contents and confirm returned coverage. This is the OMP command, not Claude's `/review` alias. A catalogued OMP reviewer-agent invocation is another supported route when exposed; report that actual invocation, not a fictional menu interaction. See [provider recipes](../.claude/skills/aidlc-review/references/review-options.md#provider-recipes).

**Next:** decide which Important findings to address, then request a scoped fix pass in writable mode — or pick **Open PR (aidlc-ship)** when the pass returned zero Important findings.

### Fix agreed findings, then re-review

**Say in writable mode:**

> Fix the order-export findings we just agreed to address, preserve unrelated changes, keep the spec and plan aligned, and rerun affected checks. Do not commit, publish, or merge.

**Run:**

```text
/aidlc-build order-export
```

**Expect:** scoped fixes for the agreed finding IDs and fresh evidence. Unavailable checks remain not run; earlier review does not cover newly changed code.

**Next, say:**

> Re-review the updated order-export scope and actual new evidence. Reassess the agreed finding IDs and new regressions; preserve other findings as not rechecked rather than silently resolving them. Identify stale scope or missing coverage. Keep this local and non-editing.

**Run:**

```text
/aidlc-review order-export
```

**Expect:** the re-review runs at the **escalated** tier (`/code-review xhigh`) and reassesses `R1`, `R2` … by ID: fixed, still open, or new. The loop — fix, verify, re-review — repeats until a pass returns zero Important findings or **three fix cycles** have run; either way it then stops and asks the post-review gate. Under `Flow policy: auto-advance when clear, including build` those cycles may run without a gate between them, each hop announced; under any other policy every hop asks. Updated findings and remaining human decisions, not self-approval or delivery. Pause with a new handoff snapshot if continuity is needed; do not overwrite the earlier one.

### Ship a reviewed change

**Prerequisite/mode:** writable session on branch `aidlc/order-export`; `changes/order-export/review.md` whose latest pass has zero open Important findings and `evidence.md` or verify evidence present — the skill reads both from disk and stops, pointing back at the review loop, when they are not there. `gh` authenticated (or the `github` MCP server) for the PR; `origin` reachable for the push.

**Say:**

> Ship order-export. Show me the diff first, then commit, push the branch and open the PR against main. Do not merge.

**Run:**

```text
/aidlc-ship order-export
```

**Expect:** `git status` and a diff summary; the branch is confirmed as `aidlc/order-export` (a different branch needs your confirmation; the default branch is refused). Then the question, exactly **Commit, push and open PR**, **Commit only** or **Stop here** — always asked, whatever the flow policy. On the first option: one commit whose title is `VS-1234: add filtered order CSV export` when the ID starts with a Jira key (here, without one, a Conventional Commit type such as `feat: add filtered order CSV export`), whose body says why and ends `Change: order-export`, and which includes `changes/order-export/` alongside the code; `git push origin aidlc/order-export` (never force, never the default branch); `gh pr create --base main --title … --body-file <rendered template>` — or the github MCP when `gh` is absent — with the body rendered from the skill's `templates/pr-body.md`: Summary (from intent), Ticket link, Spec/plan links, Evidence (verification summary), Review (passes, tiers, findings closed), Knowledge records (ADR/incident/threat-model paths if any), Checklist (conventions run, tests, no secrets). The PR URL is read back and written under References in `evidence.md`/`review.md`. **Commit only** stops after the commit; **Stop here** changes nothing.

**Next:** review the PR in GitHub. Merging, approving, enabling auto-merge and branch protection are never the skill's actions; CircleCI runs the pipeline from the PR and a human decides promotion. Capture a lesson with `/aidlc-learn order-export` if the change taught one.

### Fix a bug with an evidence record

**Prerequisite/mode:** writable session, a reproducible bug (report, alert or review finding), authority to commit one test when asked. Optional Jira key, PR URL or incident link—omit rather than invent.

**Say:**

> Fix PROJ-482: CSV export drops orders whose status changed during pagination. The PR will be opened later. Reproduce first, protect the failing test, then fix and record evidence.

**Run:**

```text
/aidlc-fix csv-pagination-drop
```

**Expect:** a worktree proposal for `aidlc/csv-pagination-drop` (directory `.claude/worktrees/aidlc+csv-pagination-drop`), a reproduction, a failing test and a request to authorise its commit (`test(csv-pagination-drop): reproduce <summary>`) — that question is always asked, whatever the flow policy. The marker `.aidlc/fix/csv-pagination-drop.json` lists the protected test paths; while it exists `protect-tests.sh` denies edits to them, including by the fixing agent. After the fix, the test is rerun and `/verify` runs where an app runtime exists. `changes/csv-pagination-drop/evidence.md` is written from the fix skill's template—references, the EARS triad (**Current:** `WHEN an order's status changes during pagination THE export drops it`; **Expected:** `WHEN an order's status changes during pagination THE export SHALL still include it once`; **Unchanged:** `THE export SHALL CONTINUE TO respect the active filter`) that the failing test and the protected regression tests map to, reproduction with pre-fix output, files and root cause, verification commands with actual output, regression protection, lesson link, limits—and read back. When the report came through an alert or incident link, an AskUserQuestion offers to create `docs/incidents/YYYY-MM-DD-csv-pagination-drop.md` from `docs/incidents/template.md`, add its index row and link it from the evidence References; a security defect gets the same offer for `docs/security/findings/`. The closing gate is asked too: the marker is then deleted and `/aidlc-learn csv-pagination-drop` is offered.

**Next:** review the evidence, request `/aidlc-review` on the diff if wanted, and decide on the lesson. Committing the fix, pushing and opening the PR go through `/aidlc-ship csv-pagination-drop` (which titles the commit `PROJ-482: …` when the change ID starts with that key) or your own explicit actions; updating Jira remains yours. The PR URL lands in the evidence References either way.

## 10. Capture a durable lesson after proven work

This is optional, not a completion checklist. A routine fix whose reasoning is already recoverable from code/tests/docs should produce **no learning file**.

**Prerequisite/mode:** one solved, verified, non-obvious lesson with actual accessible evidence; writable mode for capture.

**Say:**

> Capture the durable lesson from the resolved order-export problem, using its current code and existing verification evidence. Use ordinary AIDLC without CE. Preserve what caused the problem, why the proven solution works, when it applies and what remains unverified. Do not rerun checks or manufacture a lesson if the reasoning is already adequately documented.

**Run:**

```text
/aidlc-learn order-export
```

**Expect:** one saved/read-back note under `docs/solutions/<category>/`, or the valid configured root, **or an honest not-saved skip with a reason**. The note carries `Status: Verified` and `Last verified: <date> against <revision or environment>` so a later reader can tell how fresh it is; mark it `Needs re-check` or `Superseded by <path>` when that changes. It also carries `Confidence: 0.3` for a first observation (`0.5` at 3–5 observations, `0.7` at 6–10, `0.85` at 11+), `Observations: 1 (order-export)` and `Scope: project` or `team`. Ordinary mode changes only the note, never the glossary, canonical change artifacts or global memory. It searches relevant existing lessons; when the same topic already has a lesson, the skill offers to bump that lesson's Observations and Confidence (adding this change ID) instead of writing a duplicate, and a stale same-topic note needs explicit update direction rather than another copy. A lesson observed in two or more changes at confidence ≥0.8 is proposed to you as a candidate rule for `AGENTS.md` or a `.claude/rules/` file — proposed, never written by the skill. That is the whole of what was borrowed from ECC's `continuous-learning-v2`: its observation hooks and background observer were not imported.

**Next:** retain the exact path and consult it when applicable to later work, checking current behavior rather than treating historical evidence as fresh proof. Another lesson requires a separate request.

### Optional CE lightweight capture

**Say:**

> Use Compound Engineering lightweight capture for that one verified order-export lesson. Maintaining relevant entries in an existing local CONCEPTS.md is acceptable; do not create that file, change instructions/rules/global memory/configuration, run project proof, refresh other notes, or publish anything.

Run `/aidlc-learn order-export` again only for the intended capture/update—not to create a duplicate of a note already saved above. Select the exact existing note and authorise its update if that is the actual task.

**Expect:** real `compound-engineering:ce-compound` with `mode:non-interactive depth:lightweight`, document-only validation and post-write reads of the actual note and any changed existing glossary. Full-mode history scans/subagents and automatic refresh are not used. The report preserves upstream grounding limitations, actual glossary changes and any skip/failure; a terminal “Documentation complete” alone is not a readback.

If glossary changes are forbidden, choose ordinary capture or stop; do not ask CE to silently omit its required step. In plan/read-only mode, use ordinary eligible draft text labelled **not saved** or defer capture—never invoke CE to bypass the mode.

## 11. Export and adopt without overwriting a repository

**Prerequisite:** Python 3; an existing parent directory and a destination that does not exist.

**Run from the package checkout:**

```sh
python3 scripts/aidlc.py package /path/to/new-aidlc-copy
python3 /path/to/new-aidlc-copy/scripts/aidlc.py check
```

**Expect:** a complete standalone tree with the declared skills (orchestrator, ticket intake, spike, stages, ship, fix, onboard, utilities, the imported `architecture-decision-records` and `doc-coauthoring`), the four agents, bundled templates, shared docs/helper, `AGENTS.md`/`CLAUDE.md`, settings, the four hooks, rules, `.worktreeinclude`, `.mcp.json`, the `docs/adr/`, `docs/incidents/`, `docs/security/`, `docs/references/` and `docs/platform/` indexes and templates, `templates/conventions/`, the vendor manifests and locally linked source/evidence dependencies. No `.git`, canonical change artifacts, solution/ideation stores, `.aidlc/`, local settings, arbitrary credentials/configs or plugin is copied. Existing destinations—including empty directories and symlinks—are refused, not merged. Missing/unsafe source dependencies fail before destination creation; an unexpected later copy error reports the partial new tree for inspection. Declared/linked content is copied verbatim, not secret-scanned; inspect it before sharing.

**Next for standalone use:** launch Claude in the exported tree; create/refine an intent through the ordinary workflow. Establish Git history through your own normal process when needed—the exporter does not initialise or commit a repository.

**Next for an existing codebase:** compare and explicitly merge the selected `.claude/skills/`, agents if wanted, helper and shared documentation dependencies. Review the shared settings, hooks, scoped rules, `.worktreeinclude` and the `.mcp.json` server declarations rather than overwriting existing configuration — drop a declared server the team has not approved. Reconcile `AGENTS.md`, `CLAUDE.md`, `REVIEW.md` (the repository's own file, else `${CLAUDE_PLUGIN_ROOT}/REVIEW.md`), README/docs and ignore patterns (`.aidlc/fix/`, `.aidlc/current`, `.codegraph/`) with the project's existing content and authority; never replace them wholesale with package defaults. If the repository already has a `CLAUDE.md`, keep it as the Claude-specific section and move shared text into `AGENTS.md` behind an `@AGENTS.md` import, or run `/aidlc-onboard` to draft one. Adopt the knowledge stores by keeping the `docs/adr/`, `docs/incidents/` and `docs/security/` indexes and templates, or point the skills at existing equivalents. Run the package check from the adopted helper and exercise the intended workflow in that codebase. The exporter copies config only into the new standalone tree; it does not mutate an existing repository or global settings. It is not an installer/updater, and `--root` only changes the target of `new`/`doctor`.

Do not use `--add-dir` as a shortcut and assume these repository-root-relative shared docs follow the skills. No plugin namespace relocation, automatic upgrade or cross-harness guarantee is provided. Review exported source/evidence before any separately authorised sharing or publication.

## 12. Use the optional ECC skill library

These 37 project skills supplement the AIDLC orchestrator, stage skills and utilities. They do not introduce new artifact owners or authorise unrelated actions. Existing repository rules, design conventions, test strategy and the engineer's current decisions take precedence over generic examples. Check examples against the application's installed dependency versions before applying them. Two further imported skills are not part of this library's hands-off rule because they are wired into the workflow: `architecture-decision-records` (ECC, same pin) writes `docs/adr/NNNN-<title>.md` and its index row after you confirm — `aidlc-design` and `aidlc-spike` offer it, and its upstream mentions of ECC's `planner`/`code-reviewer` agents mean `aidlc-plan`/`aidlc-review` here — and `doc-coauthoring` (anthropics/skills) runs a structured drafting conversation for an intent, spec, ADR or incident record and leaves the save to the owning skill or store.

### Select by task, not by installing the whole ECC runtime

| Area | Included skills |
| --- | --- |
| API and backend | `api-design`, `backend-patterns`, `contract-first`, `error-handling`, `postgres-patterns`, `mcp-server-patterns` |
| Languages and frameworks | `django-celery`, `django-security`, `dotnet-patterns`, `fastapi-patterns`, `golang-patterns`, `golang-testing`, `python-patterns`, `python-testing`, `kubernetes-patterns` |
| Frontend and testing | `coding-standards`, `design-system`, `frontend-design-direction`, `frontend-patterns`, `inherit-legacy-style`, `react-patterns`, `react-testing`, `react-performance`, `e2e-testing` |
| Research and review | `documentation-lookup`, `security-review` |
| Explicit operational workflows | `canary-watch`, `codebase-onboarding`, `eval-harness`, `gan-style-harness`, `git-workflow`, `github-ops`, `growth-log`, `jira-integration`, `parallel-execution-optimizer`, `production-audit`, `terminal-ops` |

Reference/pattern skills can be selected by Claude when relevant, or invoked by name. The eleven operational skills have `disable-model-invocation: true`: invoke them deliberately and supply the intended scope. They do **not** share the `aidlc-*` single-change-ID argument rule.

For example, ask for an API design critique of the saved same-change spec using `/api-design`, without changing files. For `/codebase-onboarding`, request a repository-grounded orientation and specify whether any report may be saved. For `/jira-integration`, specify the issue and read-only purpose; creating issues, comments, transitions or other remote writes needs separate authority. Reuse an already connected service instead of installing a duplicate MCP server.

An explicit skill invocation selects guidance, not blanket permission for every example. No permission-grant frontmatter, model overrides, hook installation, global memory, automatic commits/pushes, deployments or monitoring setup is imported from ECC. The [minimal project setup](#project-runtime-files-and-shared-instructions) is separate AIDLC configuration. Some bodies describe optional upstream agents, commands or scripts; a linked upstream implementation is **not installed here**. Discover actual available capabilities and state missing prerequisites rather than inventing tools or results. `eval-harness` and `gan-style-harness` add optional guidance, not a running evaluation service. `canary-watch` does not start a scheduler; `growth-log` does not silently change personal memory; `security-review` does not replace the artifact-aware `aidlc-review` handoff.

### Provenance and maintenance

Imported from [ECC's canonical skills](https://github.com/affaan-m/ECC/tree/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills) at commit `8321021c54d670126ce3b2969d5deb880b4b0c2a`. Upstream's requested `.agents/skills` tree is only a subset; the local import lives in `.claude/skills/`, not a second host mirror. `frontend-design-direction` is the actual name corresponding to the requested frontend design entry.

The [ECC manifest](vendor/ecc/manifest.json) lists every imported file, its source and original/imported SHA-256, invocation mode, adaptations and optional dependencies; the [anthropic-skills manifest](vendor/anthropic-skills/manifest.json) does the same for `doc-coauthoring` (pinned at `34040c9c568585f6929bedeaad110ad08f079624`), and its [NOTICE](vendor/anthropic-skills/NOTICE.md) records that the upstream repository has no root license file and this skill no per-skill license — only the README statement "Many skills in this repo are open source (Apache 2.0)". These hashes record the import baseline, not a signature, security certification or automatic-update lock. Preserve the [MIT license](vendor/ecc/LICENSE) and original in-file source attributions. Compare a future pinned revision with both this baseline and local edits; do not refresh blindly or overwrite project adaptations. `check` verifies declared assets, names, invocation modes and local Markdown links outside fenced examples; `package` includes the full declared bundles. Neither validates every code sample or upstream service.

### MCP catalog: retain examples, enable nothing from it

The [inactive ECC MCP catalog](../mcp-configs/ecc.mcp-servers.example.json) is a verbatim 34-server upstream snapshot. Its original comments describe upstream setup, **not instructions to configure this repository**. Do not copy it wholesale into `.mcp.json` or user settings, and do not supply it to `--mcp-config` merely to inspect it: doing so can start local processes or connect remote services. The live project configuration is [`.mcp.json`](../.mcp.json), which already declares `context7`, `github` (the current official remote server, not the catalog's deprecated entry) and `atlassian`; see [runtime files](#project-runtime-files-and-shared-instructions) for their authentication.

Beyond the three declared servers, select others only for a concrete missing capability:

- **Documentation:** `context7` is already declared in `.mcp.json`; approve it via `/mcp` rather than adding the catalog entry.
- **Browser interaction:** Playwright is a candidate if the current harness lacks suitable browser tooling.
- **GitHub:** `.mcp.json` declares the [current official GitHub MCP server](https://github.com/github/github-mcp-server) (`https://api.githubcopilot.com/mcp/`); an authorised `gh` CLI is the alternative. ECC's snapshot uses `@modelcontextprotocol/server-github`, whose [upstream implementation is deprecated](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/github) — do not copy it.
- **Jira/Confluence:** `.mcp.json` declares Atlassian's own remote server; the snapshot's third-party servers are alternatives, not additional requirements.
- **Code graph:** `codegraph` registers itself through `codegraph install` in the adopting repository (see [PLUGINS.md](PLUGINS.md#optional-code-graph-tooling)); it is not declared here.

Before enabling anything, review the actual server/version, trust and data egress, filesystem/database scope, tool permissions, authentication and secret handling. Many catalog packages are unpinned or use `@latest`; some require separate ECC binaries or local builds. Memory/history servers can retain sensitive material; proxies can change model routing; database/deployment tools can mutate live systems. None of those is a default dependency. Use approved credential storage/environment injection, never real secrets in a committed example. Consult [current Claude MCP documentation](https://code.claude.com/docs/en/mcp), then separately authorise the selected configuration and verify its connection. No server was enabled by this import.

### Other ECC material worth considering

Candidates, not additional imports: `frontend-a11y` for explicit keyboard/focus/screen-reader guidance, `django-patterns` for core Django/DRF/ORM conventions alongside the selected Celery/security skills, and `docker-patterns` for local container workflows alongside Kubernetes. Review and adapt any candidate to the actual stack before adding it.

Do not bulk-import ECC's root `CLAUDE.md`/`AGENTS.md`, rules, hooks, settings, memory system, installers, provider routing or orchestration platform. They would introduce a competing workflow and operational assumptions. Required small reference dependencies are bundled with their owning skills and recorded in the manifest, not installed as active policies.
