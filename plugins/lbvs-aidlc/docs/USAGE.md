# Practical AIDLC usage

Each recipe gives what to say, what to run, what to expect and what to do next; the rules live in [WORKFLOW.md](WORKFLOW.md) and the file conventions in [ARTIFACTS.md](ARTIFACTS.md). The examples use a fictional `order-export` change and have not been executed as written.

## Before you start

- Open the intended repository in Claude Code with the whole package installed; copying one skill or pointing the helper's `--root` elsewhere does not install the workflow. Install the plugin once, then scaffold the repository ([section 11](#11-install-the-plugin-and-scaffold-a-repository)).
- Every ID-taking command accepts at most one ID and resolves the change itself when you omit it ([change IDs](WORKFLOW.md#change-ids-you-do-not-have-to-remember)). Put requests, paths, CE choices and the flow policy in conversation, never after the ID.
- Send the **Say** text as an ordinary message, then invoke the **Run** slash command. Use a writable session to save artifacts; enter native plan or read-only mode yourself for `/lbvs-aidlc-plan`, because no skill changes permissions.
- CE (Compound Engineering) is optional and runs only when you select it and its skill is loaded ([CE availability](#ce-availability), [when CE or a source is unavailable](#when-ce-or-a-source-is-unavailable)).
- No command commits, pushes, merges or deploys on its own; `/lbvs-aidlc-ship` asks first ([decisions without an approval service](WORKFLOW.md#decisions-without-an-approval-service)).

`/lbvs-aidlc [change-id]` runs the stages in the order [the loop](WORKFLOW.md#the-loop) gives and stops at each gate unless your [flow policy](WORKFLOW.md#stage-gates-and-the-flow-policy) lets it continue; the [skill route](WORKFLOW.md#skill-route) says which skill starts a ticket, spike, bug fix, onboarding, lesson or PR.

### Project runtime files and shared instructions

**Prerequisite.** Launch Claude from the adopted package root with `sh` and Python 3 on PATH. [REFERENCE.md](REFERENCE.md#project-configuration) lists every project file and hook; [WORKFLOW.md](WORKFLOW.md#skills-agents-and-hooks) states what the hooks guarantee. Under Oh My Pi the guard extension runs the same scripts.

**Run.**

```sh
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" check
```

**Expect.** Silence on a pass; in this repository the same check runs at session start. The plugin registers seven hook scripts, `protect-tests.sh`, `pr-guard.sh`, `artifact-guard.sh`, `argument-guard.sh`, `scaffold-check.sh`, `style-mode.sh` and `glossary-context.sh`, plus the helper's `mode` line; this repository adds `worktree-create.sh` and `worktree-remove.sh`. At startup and resume you see, in order, the `AIDLC project mode:` line, the scaffold check, the reply-style block and the `[aidlc-glossary]` block ([use the company glossary](#use-the-company-glossary)).

**Next.** When a hook reports a failure, run the [helper](REFERENCE.md#helper) subcommand it names from the same root. Project declarations do not clear inherited user or managed configuration, so review your effective settings ([host compliance](COMPATIBILITY.md#host-compliance)).

### CE availability

**Prerequisite.** Compound Engineering **3.26.3** is declared at project scope in `.claude/settings.json` (`extraKnownMarketplaces` and `enabledPlugins`). The declaration pins the marketplace and plugin; it does not install them.

**Run, once per checkout.**

```sh
claude plugin install compound-engineering@compound-engineering-plugin --scope project
```

**Expect.** After `/reload-plugins` or a new session, `/skills` lists `compound-engineering:ce-brainstorm`. When the plugin is missing, `lbvs-aidlc-intent` says so and offers reload, install or ordinary clarification; every skill decides availability from the session catalog, never the filesystem, and reports `prepared — not run` rather than pretend CE ran.

**Next.** Declaring the plugin selects nothing; ask for each CE step in conversation. Run `/ce-setup` once per repository for a non-default `docs_root`. The 18 `lbvs-aidlc*` commands are in [REFERENCE.md](REFERENCE.md#commands) and the bundled skills and plugins per stage in [PLUGINS.md](PLUGINS.md#stage-table). The integration contracts were reviewed at CE 3.26.3, commit `082c83e0537c803ac1d927daafc2e6eb6962dedf`.

## Run a whole change with `/lbvs-aidlc`

**Prerequisite.** The repository open in Claude Code, a writable session and a change ID. From a Jira key or GitHub issue, run [`/lbvs-aidlc-ticket`](#0a-start-from-a-ticket) first; `/lbvs-aidlc VS-1234` is not a change ID and the orchestrator says so.

**Say.**

> Start order-export: add a CSV export for the currently filtered order list, keeping the existing access rules. Work in a dedicated worktree. Stop at each stage gate for my decision.

**Run.**

```text
/lbvs-aidlc order-export
```

**Expect.** Step 0 proposes the [worktree](WORKFLOW.md#worktrees) for `aidlc/order-export` and waits. The orchestrator states the flow policy (here `Flow policy: confirm each stage`), reads the `AIDLC project mode:` line ([project mode](WORKFLOW.md#project-mode-and-onboarding)) and asks the kind of work, **Feature/change**, **Bug fix** or **Spike/investigation**, handing the last two to `/lbvs-aidlc-fix` and `/lbvs-aidlc-spike`. Each stage ends with a summary and the question **Proceed to \<next stage\>** / **Revise this stage** / **Stop here**.

**Next.** Answer each gate. After review choose **Fix findings (build)**, **Re-review at higher effort**, **Open PR (lbvs-aidlc-ship)**, **Capture lesson (lbvs-aidlc-learn)** or **Done** ([review loop](WORKFLOW.md#review-loop-and-escalation)).

### Run a change without remembering its ID

**Run first.**

```sh
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" status
```

**Expect.** One line per `changes/<id>/` with the artifacts present, the stage reached and the next stage, then the resolved current change and its source.

**Then run.**

```text
/lbvs-aidlc
```

**Expect.** The orchestrator resolves the ID in the [documented order](WORKFLOW.md#change-ids-you-do-not-have-to-remember) and says which source it used. When nothing resolves it shows the status list and asks. `.aidlc/current` is machine-local and ignored by Git.

**Next.** Carry on at the stage gate. Naming the ID (`/lbvs-aidlc vs-1234-order-export`) always wins.

### Choose a flow policy

**Prerequisite.** A run of `/lbvs-aidlc` or any stage skill. The policy is conversation text, not an argument.

**Say one of.**

> Flow policy: confirm each stage

> Flow policy: auto-advance when clear, stop before build

> Flow policy: auto-advance when clear, including build

**Expect.** Confirm each stage is the default. When a stage may continue on its own, the `Auto-advancing to <next stage> (...)` line it prints and the gates that are always asked are in [flow policy](WORKFLOW.md#stage-gates-and-the-flow-policy).

**Next.** State a different policy at any time; the next stage uses the policy in force when it finishes.

## Set up a repository (`/lbvs-aidlc-init`)

**Prerequisite.** The adopting repository open with the whole package present (`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" check` passes); writable mode only for the confirmed writes. Rerunning is safe.

**Say.**

> Set up AIDLC in this repository. Report what you find at each step and ask before writing anything; do not install plugins or store tokens.

**Run.**

```text
/lbvs-aidlc-init
```

**Expect.** Nine report-first steps, Doctor (0) to Summary (8), each ending in an AskUserQuestion wherever it would write, every written file read back; the steps and their option labels are in [repository setup](WORKFLOW.md#repository-setup-with-lbvs-aidlc-init). In read-only mode every step returns proposals labelled **not saved**.

**Next.** Pick **Start a change (/lbvs-aidlc)** or **Start from a ticket (/lbvs-aidlc-ticket)**, or **Done** and complete the Recommended items (`/mcp` for Atlassian, the token for GitHub, the plugin install), then rerun `/lbvs-aidlc-init` to see the auth state change.

## Onboard a brownfield repository

**Prerequisite.** An existing codebase; `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" mode` reports `brownfield`, or you want a conventions review anyway. Writable mode only for the confirmed writes.

**Say.**

> Onboard this repository. Report its conventions before proposing anything; do not write files until I confirm.

**Run.**

```text
/lbvs-aidlc-onboard
```

**Expect.** The read-only `lbvs-aidlc-repo-scout` returns a conventions report and a draft `docs/repo-profile.md`. You are asked **Modernize (adopt current patterns)**, **Stay legacy (inherit existing style)** or **Decide later**, then shown a proposed repository `CLAUDE.md` and `.claude/rules/` drafts ([project mode and onboarding](WORKFLOW.md#project-mode-and-onboarding)).

**Next.** Confirm explicitly to write the drafts, the profile, `.aidlc/mode` and `docs/onboarding.md`; otherwise nothing is written.

## Adopt or keep conventions

**Prerequisite.** Any session for the report; a writable session for `--apply`. The default files and the greenfield-adopts, brownfield-keeps rule are in [platform and conventions](WORKFLOW.md#platform-and-conventions).

**Run first.**

```sh
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" conventions
```

**Expect.** One line per default file, `repository owns it: <files>` or `missing — default available`, and a closing line that depends on the project mode.

**Then, greenfield only.** Accept the onboarding offer **Adopt default conventions (`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" conventions --apply`)** or run it yourself:

```sh
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" conventions --apply
pre-commit install
```

**Expect.** Only missing files are copied (`copied default`); an existing file is never overwritten.

**Next.** Review the diff and pin the hook revisions in `.pre-commit-config.yaml` before installing the hooks.

## Repository context: profile, glossary, playbooks

Stages read these three committed sources before scouting or asking, in the order [repository context](WORKFLOW.md#repository-context) gives.

### Keep a repository profile

**Prerequisite.** Any session for the check; a writable session and `/lbvs-aidlc-onboard` to write or refresh.

**Run.**

```sh
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" profile
```

**Expect.** Exactly one line, `profile: missing`, `profile: fresh` or `profile: stale (<n> manifest commits since <rev>)`, from the header lines alone. Stage skills run the same check and act on the result as [repository context](WORKFLOW.md#repository-context) says.

**Next, when stale or missing.**

> Refresh the repository profile. Re-scout only the sections the changed manifests affect, show me the diff against docs/repo-profile.md, and write it only when I confirm.

```text
/lbvs-aidlc-onboard
```

The rerun re-derives only the changed sections and the header and closes with **Write CLAUDE.md, rules and repo profile** / **Write repo profile only** / **Do not write**.

### Use the company glossary

**Prerequisite.** The `lbvs-aidlc` plugin or this repository checkout. The glossary files under [`docs/glossary/`](glossary/README.md) and the verbatim-terms rule are in [repository context](WORKFLOW.md#repository-context).

**Run.**

```sh
printf virtualstock > .aidlc/glossary
```

Use `logicbroker` for a Logicbroker repository, or run [`/lbvs-aidlc-onboard`](#onboard-a-brownfield-repository) and let the hook read the `Company:` line of the profile it writes.

**Expect.** On the first turn of the next session a `[aidlc-glossary]` block with one line per term (term, aliases, domain, first sentence of the definition), the glossary's naming traps and the path of the full glossary file. The intent and spec templates ask for terms the change introduces that the index lacks, each with a one-line definition and an offered entry from [`docs/glossary/template.md`](glossary/template.md), or `none`. During any stage you can still say:

> Use the Virtualstock glossary terms verbatim in the spec and the code identifiers. Flag anything you would have to name yourself.

**Next.** `off` in `.aidlc/glossary` or `AIDLC_GLOSSARY=off` silences the block. Do not hand-edit `docs/glossary/*-index.md`; `scripts/build_plugin.py` regenerates both indexes from the glossaries and the package check fails when an index differs from its source. A **new term** is added only on your confirmation and lands in the same PR as the change; the [pre-PR conventions check](WORKFLOW.md#pre-pr-conventions-check) repeats the drift check.

### Save and follow a playbook

**Prerequisite.** A spike whose answer is a repeatable procedure, or a procedural lesson; a writable session ([knowledge stores](WORKFLOW.md#knowledge-stores)).

**Say, at the spike end gate or during `/lbvs-aidlc-learn`.**

> The steps we just ran to backfill order exports for one tenant will recur. Save them as a playbook with the checks we used after each step and the rollback we agreed. Link the spike and evidence as sources.

**Expect.** The spike gate gains **Save as playbook** and `/lbvs-aidlc-learn` step 4 offers **Save as playbook instead**. Either writes `docs/playbooks/<kebab-title>.md` with `Status: Draft`, `Runs: 0` and Sources, plus the index row, only on confirmation and read back.

**Next.** A playbook with `Runs ≥ 3` and `Status: Verified` is a promotion candidate that `/lbvs-aidlc-init` step 6 proposes as a repository skill, written only on confirmation.

## 0. Compare ideas before choosing a change

Use ideation when the question is which improvement to pursue; brainstorming in step 2 clarifies a selected problem ([compare directions](WORKFLOW.md#compare-directions-before-intent)).

**Prerequisite.** A real repository focus and writable mode for a saved result. The topic ID does not create `changes/<topic-id>/`.

**Say.**

> Explore small improvements to the existing order-export experience using this repository's code, docs and relevant lessons. Compare alternatives, reject weak or already-solved ideas, and recommend up to three candidates. Use ordinary AIDLC without CE. Save the ideas, but do not choose a change, write requirements, implement or run checks.

**Run.**

```text
/lbvs-aidlc-ideate export-experience
```

**Expect.** A ranked Markdown artifact under `docs/ideation/`, or the configured root, with source-backed bases, trade-offs, unknowns and rejection reasons; the saved path is read back. Zero qualifying survivors is a valid result.

**Next.** Select an idea by title or rank and the returned path, then say:

> Explore the selected idea from the exact ideation file above as order-export. Read that source, retain its evidence, tradeoffs and open questions, and capture intent without CE. Selection is not approval of every proposed detail or permission to implement.

Then invoke `/lbvs-aidlc-intent order-export`. No stage starts automatically.

### CE ideation or a selected prior source

**Say instead.**

> Use Compound Engineering ideation for export-experience, focused only on this repository's order-export flow. Output Markdown; skip web research and external providers. Native ideation agents and temporary scratch are acceptable. Return to AIDLC idea selection without publishing, opening a browser, committing or starting another workflow.

**Run** the same `/lbvs-aidlc-ideate export-experience`.

**Expect.** The loaded `compound-engineering:ce-ideate` runs with `output:md`; scratch may remain. If it is unavailable, choose ordinary work or arrange loading yourself ([optional CE discovery](WORKFLOW.md#optional-compound-engineering-discovery)).

**Next.** To refine, give the exact existing ideation path and name the change to save ([select the exact saved input](WORKFLOW.md#select-the-exact-saved-input)).

## 0a. Start from a ticket

**Prerequisite.** A writable session and read access to the ticket through the `atlassian` MCP server (approve it once via `/mcp`) for Jira keys, or `gh auth login` or the `github` MCP server for GitHub issues. With neither, the skill asks you to paste the ticket text.

**Say.**

> Pick up VS-1234. Read the ticket, propose the change ID and seed the intent from it. Do not change the ticket.

**Run.**

```text
/lbvs-aidlc-ticket VS-1234
```

**Expect.** The fetched summary, description and acceptance criteria; a proposed ID such as `vs-1234-order-export` ([change IDs](WORKFLOW.md#change-ids-you-do-not-have-to-remember)) to confirm or edit; on confirmation `.aidlc/current` and `changes/vs-1234-order-export/intent.md`, read back. The closing question offers **Continue with /lbvs-aidlc (worktree, stages)** or **Stop here**. Nothing is written back to the tracker.

**Next.** Choose **Continue** to let `/lbvs-aidlc` propose the worktree and run the stages, or stop and refine the intent by hand.

## 0b. Run a time-boxed spike

**Prerequisite.** A question about feasibility, an existing subsystem or a choice between approaches that must be answered before an intent or design is honest; writable mode to save `spike.md`. A spike never implements.

**Say.**

> Spike whether the order-export CSV can stream from the existing pagination layer without loading all orders into memory. Time box: two hours of investigation. "Answered" means we know which layer would change, what breaks, and a recommendation with a fallback. Read-only, no code changes.

**Run.**

```text
/lbvs-aidlc-spike order-export
```

**Expect.** An AskUserQuestion confirming the question, the time box and the "answered" criteria; read-only investigation; then `changes/order-export/spike.md` ([artifacts](ARTIFACTS.md#current-artifacts-and-placement)), saved and read back. The end gate offers **Create/refresh intent from this spike (lbvs-aidlc-intent)**, **Record an ADR (architecture-decision-records)**, **Save as playbook** when the answer is a repeatable procedure, or **Stop here**.

**Next.** Pick **Create/refresh intent** to have `/lbvs-aidlc-intent order-export` read the spike as a source, or **Record an ADR** when the spike settled an architectural choice; the ADR is written after you confirm the draft.

## 1. Start with a clear request, without CE

**Prerequisite.** An ordinary writable session; a conversation is enough input.

**Say.**

> For order-export, add a CSV export for the currently filtered order list. Keep the existing access rules; do not add scheduled exports. Capture this as intent without CE. Ask about requirements that are still unclear.

**Run.**

```text
/lbvs-aidlc-intent order-export
```

**Expect.** `changes/order-export/intent.md`, grounded in the request and existing behaviour, with open questions and a next step. In read-only mode, proposed text instead of a save.

**Next.** Correct misunderstandings and confirm the direction, then design.

## 2. Optionally brainstorm before settling intent

**Prerequisite.** An unclear outcome or approach ([optional CE discovery](WORKFLOW.md#optional-compound-engineering-discovery)); a writable session with `compound-engineering:ce-brainstorm` loaded, because CE brainstorming can write supporting files.

**Say.**

> For order-export, use Compound Engineering brainstorming to clarify what users need from order exports, then return to AIDLC intent. Keep scheduled exports out of scope. Do not plan, implement, or ship through CE.

**Run.**

```text
/lbvs-aidlc-intent order-export
```

**Expect.** Same-conversation discovery through CE, then the returned brief is incorporated into `changes/order-export/intent.md` as supporting source material ([CE discovery input](ARTIFACTS.md#optional-ce-discovery-input)).

**Next.** Resolve the open questions and proceed to design. CE completion is not approval.

## 3. Design, then propose a plan

### Save requirements and design

**Prerequisite.** A working intent and a writable session.

**Say.**

> Turn the order-export intent into requirements and design using the existing code. Use ordinary AIDLC without CE. Save the spec, preserve the agreed scope, and surface remaining decisions. Do not implement.

**Run.**

```text
/lbvs-aidlc-design order-export
```

**Expect.** `changes/order-export/spec.md` with observable requirements, boundaries, design choices and open questions; acceptance criteria are EARS lines with stable IDs such as `R1.1 WHEN the user exports the filtered list THE export service SHALL stream rows in the current filter order` ([traceability](WORKFLOW.md#traceability-from-requirement-to-check)). The read-only `lbvs-aidlc-design-reviewer` returns **READY** or **NOT READY** with numbered findings, and an AskUserQuestion offers an ADR or a threat model when the design warrants one ([knowledge stores](WORKFLOW.md#knowledge-stores)).

**Next.** Discuss unresolved choices, then enter native plan mode.

### Propose without saving

**Prerequisite.** Native plan or read-only mode; intent and spec available, or explicitly supplied task context with missing artifacts named.

**Say.**

> Propose an implementation plan for order-export from the saved intent and spec. Identify affected files, dependencies, task checks, and unresolved choices. Do not save project files or implement.

**Run.**

```text
/lbvs-aidlc-plan order-export
```

**Expect.** A code-grounded proposal in the conversation, not a write to `changes/order-export/plan.md`, with numbered checkbox tasks such as `- [ ] T1.2 Add the streaming export endpoint … _Requirements: R1.1, R1.2_` and a check that every R-ID appears in a task. A native plan file is machine-local scratch, not the canonical plan ([saving a plan](WORKFLOW.md#saving-a-plan-before-implementation)).

**Next.** Discuss revisions and confirm the exact proposal. Keep its complete text if you change sessions; a handoff saying "confirmed" cannot recover a lost proposal.

## 4. Save the confirmed plan only

**Prerequisite.** A writable session; `lbvs-aidlc-build` owns the save ([saving a plan](WORKFLOW.md#saving-a-plan-before-implementation)). The exact confirmed proposal must still be available; if it lives in a native scratch file, name the path.

**Say.**

> I confirm the order-export proposal immediately above. Save only that exact proposal to changes/order-export/plan.md, then stop. Do not edit application code, run tests or builds, invoke review, or start implementation.

**Run.**

```text
/lbvs-aidlc-build order-export
```

**Expect.** `changes/order-export/plan.md` saved and its path reported; no application edits, task checks, review or implementation. The command does not overwrite a newer conflicting plan or infer confirmation from a handoff.

**Next.** Request an optional review of this saved version, or request implementation.

## 5. Optionally review a saved spec or plan with CE

CE document review critiques a document and is not approval ([optional CE document review](WORKFLOW.md#optional-ce-document-review)).

### Saved spec

**Prerequisite.** The intended version exists at `changes/order-export/spec.md` and `compound-engineering:ce-doc-review` is loaded.

**Say.**

> Use Compound Engineering document review on the saved changes/order-export/spec.md. Report findings through AIDLC using the current provider. Do not redraft, apply corrections, write a report file, or implement.

**Run.**

```text
/lbvs-aidlc-design order-export
```

**Expect.** Conversational findings, reviewer coverage, limitations and remaining decisions. The saved spec is unchanged.

**Next.** Decide which findings to address and request the corrections separately through design.

### Saved plan

**Prerequisite.** Native plan or read-only mode, the plan saved by the previous recipe, and the CE review skill loaded.

**Say.**

> Use Compound Engineering document review on the saved changes/order-export/plan.md. Review this version, not a new proposal or native scratch file. Return report-only findings using the current provider; do not fix or implement.

**Run.**

```text
/lbvs-aidlc-plan order-export
```

**Expect.** Findings and outstanding decisions without a change to the plan; no other version is substituted for the requested one.

**Next.** If the plan needs revision, ask `lbvs-aidlc-plan` to propose it read-only, confirm that revision and use the save-only recipe.

## 6. Save and build, with a pending-review stop

**Prerequisite.** A writable session, confirmed scope and approach, and authority for local implementation and checks.

**Say.**

> I confirm the order-export proposal above. Save it to the canonical plan if needed, then implement the agreed scope and exercise the relevant local checks. If the CE document review we requested is still pending, save the plan but stop before implementation; do not invoke that review automatically.

**Run.**

```text
/lbvs-aidlc-build order-export
```

**Expect.** Without a pending review, implementation one task at a time; each task's own check runs and `[ ]` becomes `[x]` in `plan.md` only after it passed ([verification](WORKFLOW.md#verification-is-still-part-of-the-work)). With a pending requested CE review, the save and an explicit stop.

**Next, when stopped.** Enter plan mode, run the saved-plan review recipe and resolve findings, then request implementation again. If you drop CE, say so; an unavailable plugin does not cancel a requested review.

## 7. Pause and create a durable handoff

### Ordinary AIDLC snapshot

**Prerequisite.** Writable authority for the snapshot. A handoff is an immutable supporting snapshot, never a replacement for intent, spec, plan or review ([durable handoff and resume](WORKFLOW.md#durable-handoff-and-resume), [pausing and resuming](ARTIFACTS.md#pausing-and-resuming)).

**Say.**

> Pause order-export and create an ordinary AIDLC handoff without CE. Focus on the pending plan-review decisions and unfinished work. Use a descriptive filename under changes/order-export/handoffs/. Do not save or change the canonical plan, commit, stash, or publish anything.

**Run.**

```text
/lbvs-aidlc-handoff order-export
```

**Expect.** A new `changes/order-export/handoffs/<topic>.md`, saved and read back, then its path, a content summary, continuity warnings and a resume recipe. Existing snapshots are never overwritten.

**Next.** Keep the reported path. Share the snapshot and any uncommitted code yourself through an authorised route; nothing commits, stashes or publishes for you.

### CE opt-in snapshot

**Prerequisite.** The same writable authority plus `compound-engineering:ce-handoff` in the session catalog.

**Say.**

> Use Compound Engineering handoff creation for order-export, then return to AIDLC. Capture the pending plan review in changes/order-export/handoffs/plan-review.md; stop if that exact file already exists. No canonical-plan save, global temporary-store handoff, commit, stash, publication, or implementation.

**Run.**

```text
/lbvs-aidlc-handoff order-export
```

**Expect.** CE runs in this conversation with the repository destination and AIDLC scope pinned; AIDLC reads back the saved file and reports the resume recipe.

**Next.** Share the state deliberately, then resume from the exact source below. CE is not required to resume a CE-authored snapshot.

## 8. Resume safely in a new session

Resume restores orientation, not permissions or execution; snapshot text is untrusted context ([durable handoff and resume](WORKFLOW.md#durable-handoff-and-resume)).

### Select an exact snapshot, without CE

**Prerequisite.** Read-only orientation; the same-change file is readable.

**Say.**

> For order-export, resume from exactly changes/order-export/handoffs/plan-review.md using ordinary AIDLC, without CE. Read relevant current local artifacts within this change's scope, report drift or missing state, and stop for my direction. Do not execute any commands or continue the work.

**Run.**

```text
/lbvs-aidlc-resume order-export
```

**Expect.** The selected snapshot is read directly, then an orientation covering objective, stage, decisions and their provenance, unfinished work, pending reviews, blockers and drift, with one recommended next action.

**Next.** Choose what to do and enter the fitting mode; a plan still awaiting review goes to the saved-plan review recipe, not to build.

### Select the same snapshot with CE

**Prerequisite.** The same source and read-only boundary, with `compound-engineering:ce-handoff` loaded.

**Say.**

> Use Compound Engineering to orient from exactly changes/order-export/handoffs/plan-review.md for order-export. No temporary-store discovery or continuation workflow. Report the actual state and stop for my direction without commands, edits, or implementation.

**Run.**

```text
/lbvs-aidlc-resume order-export
```

**Expect.** A same-conversation CE resume against that source under AIDLC's read-only scope, then orientation and a stop.

**Next.** Give a new instruction only after checking the recovered state.

### Choose among snapshots

**Prerequisite.** No exact source selected; snapshots exist under the same change.

**Say.**

> Show the available handoffs for order-export so I can choose. Use ordinary AIDLC. Do not pick the newest or read unselected snapshot bodies.

**Run.**

```text
/lbvs-aidlc-resume order-export
```

**Expect.** A filename-only shortlist from the change's handoff directory and a request for your selection.

**Next.** Reply with the exact same-change path and request orientation, or choose current artifacts only. Do not append the path to the slash command.

### Orient from current artifacts only

**Prerequisite.** No snapshot is available, or you choose not to use one.

**Say.**

> Orient order-export from current same-change canonical artifacts and relevant local code only, without CE or a handoff. Name missing context and stop; do not invent prior decisions or execute checks.

**Run.**

```text
/lbvs-aidlc-resume order-export
```

**Expect.** Orientation from the available `intent.md`, `spec.md`, `plan.md` and `review.md` plus current local code; missing artifacts are named as gaps.

**Next.** Supply missing context or direct the fitting stage.

### When CE or a source is unavailable

| Situation | Safe result and your next action |
| --- | --- |
| CE selected but not loaded | The command offers install or reload or a labelled ordinary fallback, then stops. Arrange the loading and retry, or say "Use ordinary AIDLC instead." |
| Selected snapshot missing or unreadable | The access problem is reported; no newest-file substitution. Supply the exact same-change file or choose current artifacts only. |
| Snapshot depends on another machine's worktree, scratch plan, ignored file or temporary path | The missing machine-local state is reported, not reconstructed. Make it available or revise the scope; a lost plan is reproposed and confirmed before saving. |
| Snapshot stale or disagreeing with current files | Drift is named; current files and your direction govern. |
| Source sparse, unrelated or outside the selected change | The gap is reported and orientation stops. Select the correct same-change source. |

The host's own resume or continue restores a local conversation and is separate from `/lbvs-aidlc-resume`. The CE continuity contract was inspected at [CE 3.26.3, commit `082c83e`](https://github.com/EveryInc/compound-engineering-plugin/blob/082c83e0537c803ac1d927daafc2e6eb6962dedf/skills/ce-handoff/SKILL.md).

## 9. Verify, review, fix, and re-review

### Exercise behavior without fixing it

**Prerequisite.** An implemented change and an authorised local or disposable runtime; not read-only plan mode, because checks can have side effects.

**Say.**

> Verify order-export against the saved spec and plan using the authorised local environment. Exercise the changed behavior, report passed, failed, and not-run checks, and do not fix code. Return evidence in the conversation.

**Run.**

```text
/lbvs-aidlc-verify order-export
```

**Expect.** A table `R-ID | check | observed result | not run (reason)` with one row per acceptance criterion in `spec.md` ([traceability](WORKFLOW.md#traceability-from-requirement-to-check)); no source edits and no saved report. You are then asked exactly **Critique the tests (lbvs-aidlc-test-critic)** / **Skip**; the critic's `C<n>` findings are input to review and block nothing ([verification](WORKFLOW.md#verification-is-still-part-of-the-work)).

**Next.** Request review of the diff and evidence, or direct fixes for demonstrated failures.

### Local implementation review

**Prerequisite.** The working-tree diff, the same-change artifacts, verification evidence and an available reviewer. No PR is required.

**Say.**

> Review the order-export implementation and local working-tree diff against its artifacts and actual verification evidence. Use an available local reviewer and tell me which ran. Return findings locally; do not edit code or post remote comments.

**Run.**

```text
/lbvs-aidlc-review order-export
```

**Expect.** A returned report, a partial report with named gaps, or `prepared — not run` with a filled context packet. The first pass runs at the **standard** tier; say `escalated`, `maximum` or `cloud` for a higher one ([review loop and tiers](WORKFLOW.md#review-loop-and-escalation)). Each finding is **Important** or **nit** with a stable ID (`R1`, `R2` …); `changes/order-export/review.md` records the pass ([evidence and review](ARTIFACTS.md#evidence-and-review)); the post-review gate asks the options listed under [run a whole change](#run-a-whole-change-with-lbvs-aidlc). How the packet reaches Claude's `/code-review` or Oh My Pi's `/review` is in [review without rebuilding the reviewer](WORKFLOW.md#review-without-rebuilding-the-reviewer).

**Next.** Decide which Important findings to address and request a scoped fix pass, or pick **Open PR (lbvs-aidlc-ship)** when the pass returned zero Important findings.

### Fix agreed findings, then re-review

**Say, in writable mode.**

> Fix the order-export findings we just agreed to address, preserve unrelated changes, keep the spec and plan aligned, and rerun affected checks. Do not commit, publish, or merge.

**Run.**

```text
/lbvs-aidlc-build order-export
```

**Expect.** Scoped fixes for the agreed finding IDs and fresh evidence; the earlier review does not cover newly changed code.

**Next, say.**

> Re-review the updated order-export scope and actual new evidence. Reassess the agreed finding IDs and new regressions; preserve other findings as not rechecked rather than silently resolving them. Identify stale scope or missing coverage. Keep this local and non-editing.

**Run.**

```text
/lbvs-aidlc-review order-export
```

**Expect.** The re-review runs at the **escalated** tier and reassesses `R1`, `R2` … by ID as fixed, still open or new. When the loop stops, how many fix cycles it allows and which policy lets the hops run without a gate are in [review loop and escalation](WORKFLOW.md#review-loop-and-escalation).

### Ship a reviewed change

**Prerequisite.** A writable session on branch `aidlc/order-export`; `changes/order-export/review.md` whose latest pass has zero open Important findings and `evidence.md` or verify evidence on disk; `gh` authenticated or the `github` MCP server for the PR; `origin` reachable.

**Say.**

> Ship order-export. Show me the diff first, then commit, push the branch and open the PR against main. Do not merge.

**Run.**

```text
/lbvs-aidlc-ship order-export
```

**Expect.** `git status` and a diff summary; the branch confirmed as `aidlc/order-export`; the [pre-PR conventions check](#pre-pr-conventions-check); then one question, whatever the flow policy. With no open Important K-finding the options are exactly **Commit, push and open PR**, **Commit only** or **Stop here**; with an Important K-finding they are exactly **Fix findings first (lbvs-aidlc-build)**, **Ship anyway: commit, push and open PR** or **Stop here**. The commit title, push rules and PR body are in [shipping a reviewed change](WORKFLOW.md#shipping-a-reviewed-change).

**Next.** Review the PR in GitHub; merging, approving and branch protection are never the skill's actions. Capture a lesson with `/lbvs-aidlc-learn order-export` if the change taught one.

### Pre-PR conventions check

**Prerequisite.** The ship recipe above, which runs this check between the diff summary and its commit question; there is no separate command. Best with a fresh `docs/repo-profile.md`; without one the checker falls back to `CLAUDE.md`, `CONVENTIONS.md`, `.pre-commit-config.yaml` and `.editorconfig` and says so under `Not examined:`.

**Expect.** A report headed `**Checker:** lbvs-aidlc-conventions-checker` in the ship summary with the four passes described in [pre-PR conventions check](WORKFLOW.md#pre-pr-conventions-check), findings `K1`, `K2` … with severity, `file:line` and the smallest fix, the commands table and `Not examined:`. The report stays in the conversation.

**Next.** **Fix findings first (lbvs-aidlc-build)** runs a scoped fix pass on the K-IDs you name and returns to `/lbvs-aidlc-ship`; **Ship anyway** records the accepted K-findings in the PR body. A command that failed because the profile is stale is a reason to [refresh the profile](#keep-a-repository-profile), not to edit the command.

### Fix a bug with an evidence record

**Prerequisite.** A writable session, a reproducible bug (report, alert or review finding) and authority to commit one test when asked.

**Say.**

> Fix PROJ-482: CSV export drops orders whose status changed during pagination. The PR will be opened later. Reproduce first, protect the failing test, then fix and record evidence.

**Run.**

```text
/lbvs-aidlc-fix csv-pagination-drop
```

**Expect.** A [worktree](WORKFLOW.md#worktrees) proposal for `aidlc/csv-pagination-drop`, a reproduction, a failing test and a request to authorise its commit (`test(csv-pagination-drop): reproduce <summary>`), always asked ([reproduction commit](WORKFLOW.md#reproduction-commit)). The marker `.aidlc/fix/csv-pagination-drop.json` lists the protected test paths, which `protect-tests.sh` refuses to edit while it exists. After the fix, `changes/csv-pagination-drop/evidence.md` is written and read back ([bug-fix evidence loop](WORKFLOW.md#bug-fix-evidence-loop)); an alert or incident link brings an offer of an incident record, a security defect one for `docs/security/findings/`. The closing gate deletes the marker and offers `/lbvs-aidlc-learn csv-pagination-drop`.

**Next.** Review the evidence, request `/lbvs-aidlc-review` if wanted, then ship with `/lbvs-aidlc-ship csv-pagination-drop`. Updating Jira stays yours.

## 10. Capture a durable lesson after proven work

**Prerequisite.** One solved, verified, non-obvious lesson with accessible evidence; writable mode for the capture. A routine fix whose reasoning is already in code, tests or docs produces no learning file ([capture one lesson](WORKFLOW.md#capture-one-non-obvious-lesson)).

**Say.**

> Capture the durable lesson from the resolved order-export problem, using its current code and existing verification evidence. Use ordinary AIDLC without CE. Preserve what caused the problem, why the proven solution works, when it applies and what remains unverified. Do not rerun checks or manufacture a lesson if the reasoning is already adequately documented.

**Run.**

```text
/lbvs-aidlc-learn order-export
```

**Expect.** One saved and read-back note under `docs/solutions/<category>/`, or the configured root, or an honest not-saved skip with a reason. The note's header lines, the offer to bump an existing same-topic lesson and the rule that promotes a repeated lesson to a candidate `AGENTS.md` or `.claude/rules/` entry are in [knowledge stores](WORKFLOW.md#knowledge-stores).

**Next.** Keep the path and consult the note later, checking current behaviour rather than treating old evidence as fresh proof.

### Optional CE lightweight capture

**Say.**

> Use Compound Engineering lightweight capture for that one verified order-export lesson. Maintaining relevant entries in an existing local CONCEPTS.md is acceptable; do not create that file, change instructions/rules/global memory/configuration, run project proof, refresh other notes, or publish anything.

**Run** `/lbvs-aidlc-learn order-export` again only for the intended capture or update, not to duplicate a saved note.

**Expect.** `compound-engineering:ce-compound` with `mode:non-interactive depth:lightweight`, document-only validation and post-write reads of the note and any changed glossary.

**Next.** If glossary changes are forbidden, choose ordinary capture or stop. In read-only mode, use draft text labelled **not saved** or defer.

## 11. Install the plugin and scaffold a repository

The engine is a plugin; a repository holds only its own state. New or existing repository, the steps are the same ([distribution](REFERENCE.md#distribution)).

### The plugin, once per engineer

```sh
claude plugin marketplace add mkhan-lb/lbvs-aidlc
claude plugin install lbvs-aidlc@lbvs-aidlc        # skills as /lbvs-aidlc:*, six agents, hooks, `aidlc` on PATH
claude plugin install lbvs-ecc@lbvs-aidlc          # optional: the 37 reference skills
```

Oh My Pi reads the same marketplace: `omp plugin marketplace add mkhan-lb/lbvs-aidlc && omp plugin install --scope project lbvs-aidlc@lbvs-aidlc`; project scope writes `.omp/plugins/installed_plugins.json`, which you commit. Under Oh My Pi the guard extension prepends the plugin's `bin/` directory to PATH, so `aidlc <subcommand>` resolves in the bash tool. The plugin installs the seven hook scripts and the helper's `mode` line listed under [runtime files](#project-runtime-files-and-shared-instructions). Updates arrive by version: `/plugin marketplace update` then `/reload-plugins`, or `omp plugin upgrade`.

### The scaffold, once per repository

**Prerequisite.** Python 3 and the repository checked out beside this package. Report first, write on `--apply`.

```sh
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" install ../my-service
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" install ../my-service --apply
```

**Expect.** The report lists every file it would `write`, `keep` or `skip` and the five repository-owned files it never touches, each with what to merge; `--apply` also writes `.aidlc/manifest.json` ([plugins and the repository scaffold](REFERENCE.md#plugins-and-the-repository-scaffold)). Nothing from the engine lands in the repository.

**Next.** Merge the hints and commit in the repository (the helper never commits), then run `/lbvs-aidlc:lbvs-aidlc-init` there ([set up a repository](#set-up-a-repository-lbvs-aidlc-init)).

### Refresh the scaffold later

From inside the repository, `aidlc update` (`--apply` to write) clones the package recorded in the manifest and runs its `sync`; `--from ../the-aidlc` uses a local checkout. From the package checkout, `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" sync ../my-service [--apply]`. The status words and exit codes are in [plugins and the repository scaffold](REFERENCE.md#plugins-and-the-repository-scaffold). Neither command commits.

### The observer (off)

`lbvs-aidlc-observer@lbvs-aidlc` installs disabled with the marketplace. `/lbvs-aidlc-init` reports its state and prints `claude plugin enable lbvs-aidlc-observer@lbvs-aidlc` (`omp plugin enable` under Oh My Pi) when you choose to turn it on. Once enabled it records every tool call's inputs and outputs under `${XDG_DATA_HOME:-~/.local/share}/ecc-homunculus/`, outside every repository; it is distinct from `/lbvs-aidlc-learn`.

## 12. Use the optional ECC skill library

These 38 project skills supplement the orchestrator, stage skills and utilities. They introduce no artifact owners and authorise nothing; repository rules and your current decisions take precedence over their generic examples, which you check against the application's installed dependency versions. `architecture-decision-records` and `doc-coauthoring` are imported separately and wired into the workflow ([imported skills](REFERENCE.md#imported-skills)).

### Select by task, not by installing the whole ECC runtime

| Area | Included skills |
| --- | --- |
| API and backend | `api-design`, `backend-patterns`, `contract-first`, `error-handling`, `postgres-patterns`, `mcp-server-patterns` |
| Languages and frameworks | `django-celery`, `django-security`, `dotnet-patterns`, `fastapi-patterns`, `golang-patterns`, `golang-testing`, `python-patterns`, `python-testing`, `kubernetes-patterns` |
| Frontend and testing | `coding-standards`, `design-system`, `frontend-design-direction`, `frontend-patterns`, `inherit-legacy-style`, `react-patterns`, `react-testing`, `react-performance`, `e2e-testing` |
| Research and review | `documentation-lookup`, `security-review` |
| Explicit operational workflows | `canary-watch`, `codebase-onboarding`, `continuous-learning-v2`, `eval-harness`, `gan-style-harness`, `git-workflow`, `github-ops`, `growth-log`, `jira-integration`, `parallel-execution-optimizer`, `production-audit`, `terminal-ops` |

Claude may select a reference or pattern skill when relevant, or you invoke it by name. The twelve operational skills carry `disable-model-invocation: true`, so you invoke them deliberately with the intended scope; they do not share the `lbvs-aidlc-*` single-ID argument rule. `continuous-learning-v2` is imported complete but off by default; its observer is the separate plugin in [section 11](#the-observer-off).

Invoking a skill selects guidance, not permission for every example. Ask `/api-design` for a critique of the saved spec without changing files, or `/jira-integration` for a read-only look at a named issue. The import activates no permission grants, hook registrations, global memory, automatic commits or deployments; skill bodies that mention upstream agents, commands or scripts describe things not installed here.

### Provenance and maintenance

The pin, the manifests, the licence notes and the rule for refreshing an import against local adaptations are in [imported skills](REFERENCE.md#imported-skills) and [optional ECC skill library](REFERENCE.md#optional-ecc-skill-library). `check` verifies declared assets, names, invocation modes and local Markdown links outside fenced examples; `package` includes the full declared bundles.

### MCP catalog: retain examples, enable nothing from it

The [inactive ECC MCP catalog](../mcp-configs/ecc.mcp-servers.example.json) is a verbatim 34-server upstream snapshot whose comments describe upstream setup, not this repository. Do not copy it into `.mcp.json` or user settings, and do not pass it to `--mcp-config` to inspect it, because that can start local processes or connect remote services. The live configuration is [`.mcp.json`](../.mcp.json) ([MCP servers](REFERENCE.md#mcp-servers)); the catalog's `@modelcontextprotocol/server-github` is deprecated, and `codegraph` registers itself through `codegraph install` ([code graph tooling](PLUGINS.md#optional-code-graph-tooling)). Before enabling any other server, review its version, data egress, filesystem and database scope, tool permissions and secret handling; many catalog packages are unpinned or use `@latest`.

### Other ECC material worth considering

Candidates, not imports: `frontend-a11y`, `django-patterns` and `docker-patterns`. Adapt any candidate to the actual stack before adding it. Do not bulk-import ECC's root `CLAUDE.md`, `AGENTS.md`, rules, hooks, settings, memory system, installers, provider routing or orchestration platform; they would introduce a competing workflow.
