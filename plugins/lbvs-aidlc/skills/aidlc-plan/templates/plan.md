# Plan: {{change_id}}

Status: draft
Change ID: {{change_id}}

Prepare this proposal read-only before implementation. An engineer without the conversation should be able to carry it out. Follow `${CLAUDE_PLUGIN_ROOT}/docs/WORKFLOW.md`; save only after the normal authorised transition out of plan mode.

## Context and inputs

Link `changes/{{change_id}}/intent.md` and `changes/{{change_id}}/spec.md`, relevant source files, and the inspected code revision or working-tree scope. Summarise the task and known decisions. If an upstream artifact is absent, identify the supplied context and gap rather than inventing it. When `docs/platform/platform.md` exists, name the platform facts (environments, orb pin, values files, observability tags) the plan relies on.

Library and API references: Context7 ID and the repository's pinned version for each library, framework, SDK or cloud API the tasks touch (or the official docs URL when Context7 was unavailable); `docs/references/libraries.md` rows to add or update, or `none`.

## Files and tasks

Name real paths and the change to each, including implementation, relevant tests, and documentation. Note generated or protected paths and existing repository constraints. Deployment, observability and promotion work is values files and pipeline config for the `lb-pipelines/app-delivery-kit-vs@1` orb; a new data store, queue or integration adds a `docs/platform/platform.md` entry.

Write tasks as numbered checkboxes. Each task ends with the spec requirement IDs it satisfies and, where relevant, its dependency; every `R<n>.<m>` in `spec.md` appears in at least one task or its exclusion is stated below the list. Build ticks `[x]` only after the task's own check passed; never tick ahead.

- [ ] T1.1 <task: file(s) and change> — check: <command or observation> _Requirements: R1.1_
- [ ] T1.2 <task> — check: <…> _Requirements: R1.1, R1.2_ depends on: T1.1
- [ ] T2.1 <task> — check: <…> _Requirements: R2.1_

Uncovered R-IDs and why: `none` or list.

## Order of work

List steps and dependencies in execution order. Separate genuinely independent work from shared-file tasks that must run serially. Keep the plan proportionate to the change; do not invent people, services, or orchestration.

## Alternatives and exclusions

Explain meaningful alternatives and trade-offs. Preserve exclusions. Raise proposed changes to requirements for engineer discussion rather than treating this plan as permission to expand scope.

## Risks and open questions

Identify what could break, the riskiest step, compatibility concerns, and unresolved task choices. Apply existing organisational rules where relevant without introducing new approval infrastructure.

## Proof

For each requirement ID, name the command or scenario, required environment/data, and expected observable result. Verify reports this table with observed results:

| R-ID | Check (command / scenario) | Expected result | Environment / data |
| --- | --- | --- | --- |
| R1.1 | <command or interaction> | <observable outcome> | <local, fixture, browser> |

- Bug fixes: a reproducing check, available pre-fix evidence, and the post-fix behavior the regression check should establish; the `SHALL CONTINUE TO` lines name the regression checks.
- UI work: the actual surface and visual comparison with supplied designs or agreed requirements.
- Other behavior: relevant software tests and runtime checks, including neighboring flows where regression is plausible.

Keep proposed checks separate from executed results. Report unavailable checks and their specific impact honestly. This is task verification, not an AI evaluation runner or a requirement to configure CI.

## Engineer checkpoint and decision notes

Discuss the approach and unresolved choices with the engineer before implementation. Confirmation may come from the current request or conversation; record useful decisions optionally, without inventing formal approval or demanding an external reference.

## Implementation handoff and updates

After confirmation and a normal authorised writable transition, use `aidlc-build` with the exact confirmed proposal to save `changes/{{change_id}}/plan.md`. Distinguish **save only** from **save and implement**; the former must stop without application changes or test/build execution. If CE document review is requested and still pending for this proposal, save first, review this exact canonical version, then return findings for engineer direction before implementation.

Record the current implementation/proposal scope, meaningful completed and unfinished work, pending reviews or decisions, actual verification and what remains unverified, and the next engineer action. Keep proposed checks separate from observed outcomes; do not infer permission from these notes. Update this live plan when implementation changes, preserving reasons and human decisions. Ask before material scope or design changes and update the spec when its contract changes.

Hand the diff and actual test/runtime evidence to review. Link `changes/{{change_id}}/review.md` or real PR findings when available, then fix and re-review. For a requested pause, a snapshot under `changes/{{change_id}}/handoffs/` points to this state without becoming another live plan. A future resume checks current artifacts/code and stops for direction. Plan confirmation or an old handoff is not permission to push, approve, merge or deploy.
