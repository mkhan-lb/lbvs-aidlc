# Practical AIDLC usage

Use this guide for the conversation, command, expected result, and next action at each step. The [workflow contract](WORKFLOW.md), [artifact conventions](ARTIFACTS.md), and [verification record](VERIFICATION.md) provide policy and evidence; the recipes below are instructions, not claims that their examples have been executed.

## Before you start

- Open the intended repository in Claude Code with the complete project resources available. Copying one skill or using the helper's `--root` does not install the workflow. The [standalone export recipe](#11-export-and-adopt-without-overwriting-a-repository) produces a new tree; existing-repository adoption remains an explicit reviewed merge.
- Every ID-taking AIDLC command accepts **exactly one ID** matching `^[a-z0-9]+(-[a-z0-9]+)*$`. Use a change ID such as `order-export`, except `/aidlc-ideate`, which takes a topic ID before a change exists; `/aidlc-onboard` takes no ID. Put requests, paths, CE choices and review targets in conversation, never after the ID.
- In the recipes, send the **Say** text as an ordinary conversation message, then invoke the separate **Run** slash command. Adapt the example scope to your application; do not copy its requirements blindly.
- Use a normal writable session for saving artifacts, handoff creation, and implementation. Enter native plan/read-only mode yourself for `/aidlc-plan`; the agent does not change permissions. Confirmation of a proposal does not change the mode or authorise unrelated actions.
- CE (Compound Engineering) is optional upstream tooling, not bundled prompts. It runs only when selected and the required skill is loaded in the current session. An installation record is not proof of availability. See [missing CE](#when-ce-or-a-source-is-unavailable).
- Local work does not require a PR, CI, an approval service, or an evaluation runner. Existing repository rules, organisational safeguards, and tool permissions still apply. None of these commands implicitly authorises commit, stash, push, publication, merge, deployment, or remote-record updates.

`/aidlc <change-id>` runs **intent → design → plan → build → verify → review** with a stage gate after each stage; you can also invoke any stage skill directly, and Claude may load one when your request matches. `/aidlc-fix` is the bug-fix evidence loop, `/aidlc-onboard` the brownfield entry and `/aidlc-learn` the lesson capture. **Handoff**, **resume** and **ideation** are the only manual-only utilities. Start each new change or fix in its own worktree (`aidlc/<change-id>`); the orchestrator proposes it and asks first.

### Project runtime files and shared instructions

Keep these files with the complete package when adopting it:

| File | Purpose and boundary |
| --- | --- |
| `AGENTS.md` | Canonical shared instructions for every agent host. `CLAUDE.md` is `@AGENTS.md` plus a Claude-specific section; `.omp/AGENTS.md` imports `@../AGENTS.md` for Oh My Pi. No symlink is involved. |
| [`.claude/settings.json`](../.claude/settings.json) | Official-schema settings registering the three hooks below. No permissions, model/provider selection or telemetry are configured. |
| [`.claude/hooks/check-package.sh`](../.claude/hooks/check-package.sh) | `SessionStart` (startup/resume): executes `python3 "${CLAUDE_PROJECT_DIR}/scripts/aidlc.py" check`, read-only. |
| `.claude/hooks/project-mode.sh` | `SessionStart`: runs `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" mode` and injects its one-line result as context. Override detection with `.aidlc/mode` containing `greenfield` or `brownfield`. |
| `.claude/hooks/protect-tests.sh` | `PreToolUse` on `Edit\|Write\|MultiEdit\|NotebookEdit`: denies edits to any path listed under `protected` in `.aidlc/fix/*.json`. Active only while a fix marker exists; `.aidlc/fix/` is ignored by Git. |
| [`.claude/rules/`](../.claude/rules/package-maintenance.md) | Path-scoped rules loaded when matching files are touched; guidance, not enforcement. |
| `.worktreeinclude` | Copies `.env` and `.claude/settings.local.json` into worktrees created for a change. |
| [`.mcp.json`](../.mcp.json) | Exactly `{"mcpServers":{}}`; no project server connections. The ECC catalog remains a separate inactive example. |

`.claude/settings.local.json` was created here as `{}` for local overrides. It is ignored, never exported and not required in an exported tree; create it there only if needed for separately reviewed local choices. Do not put credentials into shared files.

Launch Claude from the adopted package root with `sh` and Python 3 available. When project hooks are allowed, the package check and mode line run on startup/resume, **not every turn or edit**; the test-protection hook runs on every edit tool call but denies only paths in an active fix marker. To investigate a failure, run `python3 scripts/aidlc.py check` or `mode` from that root. The hooks are integrity and guardrail aids, not lifecycle verification, an approval gate or security enforcement; they do not advance stages.

An empty project MCP map and local settings object do not clear inherited user/managed configuration. Existing settings, hooks, permissions, plugins and MCP connections can still apply, and policy may restrict project customizations. Review the effective configuration in your own session; this setup adds no tool grants or server connections. See [compatibility boundaries](COMPATIBILITY.md).

These are native Claude project files plus shared instruction text in `AGENTS.md`, which other hosts read directly. One native Codex instruction-discovery smoke passed against the earlier symlinked layout; that is not native Codex skill/hook parity or a complete workflow compatibility claim. No `.agents/skills` mirror is supplied. See the [executed checks and limits](VERIFICATION.md#minimal-project-configuration-and-shared-instructions).

### CE availability

Compound Engineering **3.26.3** is declared at project scope in `.claude/settings.json` (`extraKnownMarketplaces` → `EveryInc/compound-engineering-plugin`, `enabledPlugins` → `compound-engineering@compound-engineering-plugin`). After you trust the workspace, Claude Code installs it; run `/reload-plugins` or start a new session, then confirm `compound-engineering:ce-brainstorm` appears in the skill catalog. Cloud sessions install repo-declared plugins at start. The same declaration travels with an exported tree; delete both keys there to opt out.

Declaring the plugin is not selecting it: every CE handoff still happens only when you ask for it in conversation, and skills say **prepared — not run** when it is unavailable. Run `/ce-setup` once per repository if you want a non-default `docs_root`; AIDLC reads `.compound-engineering/config.yaml` before touching solution or ideation stores.

The integration contracts were reviewed at CE **3.26.3**, commit `082c83e0537c803ac1d927daafc2e6eb6962dedf`; re-check them after upstream upgrades. Non-technical originators use the same plugin through `ce-brainstorm` with an engineer's help; other recommended bundled skills and plugins are listed per stage in [PLUGINS.md](PLUGINS.md).

## Run a whole change with `/aidlc`

**Prerequisite/mode:** the intended repository open in Claude Code, writable session, a change ID.

**Say:**

> Start order-export: add a CSV export for the currently filtered order list, keeping the existing access rules. Work in a dedicated worktree. Stop at each stage gate for my decision.

**Run:**

```text
/aidlc order-export
```

**Expect:** step 0 proposes the worktree `aidlc/order-export` (EnterWorktree when available, otherwise `git worktree add ../<repo>-order-export -b aidlc/order-export`) and waits for your answer. The orchestrator then reads the `AIDLC project mode:` line; brownfield with no repository `CLAUDE.md`/conventions record runs `/aidlc-onboard` first. Each stage skill runs in order and ends with a summary—artifact path, decisions, open questions, checks run—and the question **Proceed to \<next stage\>** / **Revise this stage** / **Stop here**. Plan still runs read-only and build saves the confirmed plan first, as in the recipes below.

**Next:** answer each gate. After review choose **Fix findings (build)**, **Capture lesson (aidlc-learn)** or **Done**. **Stop here** leaves the artifacts in place; re-run `/aidlc order-export` or the individual stage later. Nothing is committed, pushed or merged without your explicit instruction.

## Onboard a brownfield repository

**Prerequisite/mode:** an existing codebase; `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" mode` reports `brownfield`, or you want a conventions review anyway. Writable mode only for the confirmed writes at the end.

**Say:**

> Onboard this repository. Report its conventions before proposing anything; do not write files until I confirm.

**Run:**

```text
/aidlc-onboard
```

**Expect:** the read-only `aidlc-repo-scout` agent returns a structured conventions report (stack, layout, build/test/lint commands, naming, error handling, test patterns, hotspots, existing `CLAUDE.md`/`AGENTS.md`/`.cursorrules`, risks). You are asked **Modernize (adopt current patterns)**, **Stay legacy (inherit existing style)** or **Decide later**. Legacy invokes `inherit-legacy-style`; modernize recommends the `code-modernization` plugin and relevant pattern skills without installing them. Then a proposed repository `CLAUDE.md` (≤60 lines, including "Things Claude gets wrong here") and path-scoped `.claude/rules/` drafts are shown, with `/init` under `CLAUDE_CODE_NEW_INIT=1` offered as the alternative.

**Next:** confirm explicitly to write the drafts, `.aidlc/mode` and `docs/onboarding.md`; otherwise nothing is written. Keep the repository `CLAUDE.md` short and edit it when Claude repeats a mistake.

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

**Expect:** `changes/order-export/spec.md` with observable requirements, boundaries, affected components, design choices, and open questions. In read-only mode this is a proposal only; an explicit writable request to the same command owns saving it.

**Next:** discuss unresolved choices, then enter native plan mode.

### Propose without saving

**Prerequisite/mode:** native plan/read-only mode; intent/spec available, or explicitly supplied task context with missing artifacts identified. Standalone planning is possible but must not invent an accepted baseline.

**Say:**

> Propose an implementation plan for order-export from the saved intent and spec. Identify affected files, dependencies, task checks, and unresolved choices. Do not save project files or implement.

**Run:**

```text
/aidlc-plan order-export
```

**Expect:** a code-grounded proposal in the conversation, not a write to `changes/order-export/plan.md`. The handoff identifies the exact proposal or any actual native scratch-plan path, outstanding decisions, and pending requested CE document review. A native plan file is machine-local scratch state, not the canonical plan or a CE review target.

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

**Expect:** without a pending requested review, implementation, aligned artifacts, and actual passed/failed/not-run task-check evidence. With a pending requested CE document review, expect the save and an explicit stop for that review—not a build, automatic CE call, or invented approval.

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

**Expect:** observed evidence and limitations, not automatic source edits or a saved report. If needed, separately request saving the evidence with writable permission. A build alone is not proof of behavior.

**Next:** request review of the actual diff and evidence, or direct fixes for demonstrated failures.

### Local implementation review

**Prerequisite/mode:** actual working-tree/diff scope, same-change artifacts, verification evidence, and an available reviewer. No PR is required.

**Say:**

> Review the order-export implementation and local working-tree diff against its artifacts and actual verification evidence. Use an available local reviewer and tell me which ran. Return findings locally; do not edit code or post remote comments.

**Run:**

```text
/aidlc-review order-export
```

**Expect:** an actual returned report, a partial report with named gaps, or **prepared — not run** with a filled context packet and separate documented command. Loading/launching is not completion. The packet includes real tracked and untracked scope, artifact/policy contents, check evidence and prior findings. Save `changes/order-export/review.md` only on request after results return; the wrapper reads it back.

Claude's bundled `/code-review` does not accept the packet as trailing notes: non-cloud trailing text is the review target, and its fork is not guaranteed to inherit parent chat. If the wrapper cannot establish a supported context channel, follow the reported transfer step rather than pretending that pasting a preceding message delivered the packet. Any resulting code-only review with unconfirmed artifact/policy coverage is partial.

In an explicitly selected existing OMP session, `/review` → **Custom review instructions** accepts the completed packet. Include untracked file contents and confirm returned coverage. This is the OMP command, not Claude's `/review` alias. A catalogued OMP reviewer-agent invocation is another supported route when exposed; report that actual invocation, not a fictional menu interaction. See [provider recipes](../.claude/skills/aidlc-review/references/review-options.md#provider-recipes).

**Next:** decide which findings to address, then request a scoped fix pass in writable mode.

### Fix agreed findings, then re-review

**Say in writable mode:**

> Fix the order-export findings we just agreed to address, preserve unrelated changes, keep the spec and plan aligned, and rerun affected checks. Do not commit, publish, or merge.

**Run:**

```text
/aidlc-build order-export
```

**Expect:** scoped fixes and fresh evidence. Unavailable checks remain not run; earlier review does not cover newly changed code.

**Next, say:**

> Re-review the updated order-export scope and actual new evidence. Reassess the agreed finding IDs and new regressions; preserve other findings as not rechecked rather than silently resolving them. Identify stale scope or missing coverage. Keep this local and non-editing.

**Run:**

```text
/aidlc-review order-export
```

**Expect:** updated findings and remaining human decisions, not self-approval or delivery. Pause with a new handoff snapshot if continuity is needed; do not overwrite the earlier one.

### Fix a bug with an evidence record

**Prerequisite/mode:** writable session, a reproducible bug (report, alert or review finding), authority to commit one test when asked. Optional Jira key, PR URL or incident link—omit rather than invent.

**Say:**

> Fix PROJ-482: CSV export drops orders whose status changed during pagination. The PR will be opened later. Reproduce first, protect the failing test, then fix and record evidence.

**Run:**

```text
/aidlc-fix csv-pagination-drop
```

**Expect:** a worktree proposal (`aidlc/csv-pagination-drop`), a reproduction, a failing test and a request to authorise its commit (`test(csv-pagination-drop): reproduce <summary>`). The marker `.aidlc/fix/csv-pagination-drop.json` lists the protected test paths; while it exists `protect-tests.sh` denies edits to them, including by the fixing agent. After the fix, the test is rerun and `/verify` runs where an app runtime exists. `changes/csv-pagination-drop/evidence.md` is written from the fix skill's template—references, reproduction with pre-fix output, files and root cause, verification commands with actual output, regression protection, lesson link, limits—and read back. The marker is then deleted and `/aidlc-learn csv-pagination-drop` is offered.

**Next:** review the evidence, request `/aidlc-review` on the diff if wanted, and decide on the lesson. Committing the fix itself, opening the PR and updating Jira remain your explicit actions; add the PR URL to the evidence afterwards.

## 10. Capture a durable lesson after proven work

This is optional, not a completion checklist. A routine fix whose reasoning is already recoverable from code/tests/docs should produce **no learning file**.

**Prerequisite/mode:** one solved, verified, non-obvious lesson with actual accessible evidence; writable mode for capture.

**Say:**

> Capture the durable lesson from the resolved order-export problem, using its current code and existing verification evidence. Use ordinary AIDLC without CE. Preserve what caused the problem, why the proven solution works, when it applies and what remains unverified. Do not rerun checks or manufacture a lesson if the reasoning is already adequately documented.

**Run:**

```text
/aidlc-learn order-export
```

**Expect:** one saved/read-back note under `docs/solutions/<category>/`, or the valid configured root, **or an honest not-saved skip with a reason**. Ordinary mode changes only the note, never the glossary, canonical change artifacts or global memory. It searches relevant existing lessons; an adequate duplicate is reused, and a stale same-topic note needs explicit update direction rather than another copy.

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

**Expect:** a complete standalone tree with the declared skills (orchestrator, stages, fix, onboard, utilities), agents, bundled templates, shared docs/helper, `AGENTS.md`/`CLAUDE.md`, settings, the three hooks, rules, `.worktreeinclude`, the empty `.mcp.json` and locally linked source/evidence dependencies. No `.git`, canonical change artifacts, solution/ideation stores, `.aidlc/`, local settings, arbitrary credentials/configs or plugin is copied. Existing destinations—including empty directories and symlinks—are refused, not merged. Missing/unsafe source dependencies fail before destination creation; an unexpected later copy error reports the partial new tree for inspection. Declared/linked content is copied verbatim, not secret-scanned; inspect it before sharing.

**Next for standalone use:** launch Claude in the exported tree; create/refine an intent through the ordinary workflow. Establish Git history through your own normal process when needed—the exporter does not initialise or commit a repository.

**Next for an existing codebase:** compare and explicitly merge the selected `.claude/skills/`, agents if wanted, helper and shared documentation dependencies. Review the shared settings, hooks, scoped rules, `.worktreeinclude` and empty MCP map rather than overwriting existing configuration. Reconcile `AGENTS.md`, `CLAUDE.md`, `REVIEW.md` (the repository's own file, else `${CLAUDE_PLUGIN_ROOT}/REVIEW.md`), README/docs and ignore patterns (`.aidlc/fix/`) with the project's existing content and authority; never replace them wholesale with package defaults. If the repository already has a `CLAUDE.md`, keep it as the Claude-specific section and move shared text into `AGENTS.md` behind an `@AGENTS.md` import, or run `/aidlc-onboard` to draft one. Run the package check from the adopted helper and exercise the intended workflow in that codebase. The exporter copies config only into the new standalone tree; it does not mutate an existing repository or global settings. It is not an installer/updater, and `--root` only changes the target of `new`/`doctor`.

Do not use `--add-dir` as a shortcut and assume these repository-root-relative shared docs follow the skills. No plugin namespace relocation, automatic upgrade or cross-harness guarantee is provided. Review exported source/evidence before any separately authorised sharing or publication.

## 12. Use the optional ECC skill library

These 37 project skills supplement the AIDLC orchestrator, stage skills and utilities. They do not introduce new artifact owners or authorise unrelated actions. Existing repository rules, design conventions, test strategy and the engineer's current decisions take precedence over generic examples. Check examples against the application's installed dependency versions before applying them.

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

The [manifest](vendor/ecc/manifest.json) lists every imported file, its source and original/imported SHA-256, invocation mode, adaptations and optional dependencies. These hashes record the import baseline, not a signature, security certification or automatic-update lock. Preserve the [MIT license](vendor/ecc/LICENSE) and original in-file source attributions. Compare a future pinned revision with both this baseline and local edits; do not refresh blindly or overwrite project adaptations. `check` verifies declared assets, names, invocation modes and local Markdown links outside fenced examples; `package` includes the full declared bundles. Neither validates every code sample or upstream service.

### MCP catalog: retain examples, enable nothing

The [inactive ECC MCP catalog](../mcp-configs/ecc.mcp-servers.example.json) is a verbatim 34-server upstream snapshot. Its original comments describe upstream setup, **not instructions to configure this repository**. Do not copy it wholesale into `.mcp.json` or user settings, and do not supply it to `--mcp-config` merely to inspect it: doing so can start local processes or connect remote services.

Select servers only for a concrete missing capability:

- **Documentation:** Context7 is a candidate if the existing documentation tools are insufficient.
- **Browser interaction:** Playwright is a candidate if the current harness lacks suitable browser tooling.
- **GitHub:** prefer the [current official GitHub MCP server](https://github.com/github/github-mcp-server) or an existing authorised CLI. ECC's snapshot uses `@modelcontextprotocol/server-github`, whose [upstream implementation is deprecated](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/github).
- **Jira/Confluence:** prefer the already connected approved Atlassian integration; the snapshot's third-party servers are alternatives, not additional requirements.

Before enabling anything, review the actual server/version, trust and data egress, filesystem/database scope, tool permissions, authentication and secret handling. Many catalog packages are unpinned or use `@latest`; some require separate ECC binaries or local builds. Memory/history servers can retain sensitive material; proxies can change model routing; database/deployment tools can mutate live systems. None of those is a default dependency. Use approved credential storage/environment injection, never real secrets in a committed example. Consult [current Claude MCP documentation](https://code.claude.com/docs/en/mcp), then separately authorise the selected configuration and verify its connection. No server was enabled by this import.

### Other ECC material worth considering

Candidates, not additional imports: `frontend-a11y` for explicit keyboard/focus/screen-reader guidance, `django-patterns` for core Django/DRF/ORM conventions alongside the selected Celery/security skills, and `docker-patterns` for local container workflows alongside Kubernetes. Review and adapt any candidate to the actual stack before adding it.

Do not bulk-import ECC's root `CLAUDE.md`/`AGENTS.md`, rules, hooks, settings, memory system, installers, provider routing or orchestration platform. They would introduce a competing workflow and operational assumptions. Required small reference dependencies are bundled with their owning skills and recorded in the manifest, not installed as active policies.
