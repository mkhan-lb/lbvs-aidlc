# Spec: {{change_id}}

Status: draft
Change ID: {{change_id}}

Content boundary: docs/ARTIFACTS.md#content-boundary — repository-relative paths, no session references, no workflow or machine narrative.

Describe the requirements and design for the working intent. Follow `docs/WORKFLOW.md`; this artifact does not grant permissions or create an approval gate.

## Context and inputs

Link `changes/{{change_id}}/intent.md` and relevant inspected code, source records, or supplied designs. Summarise known task decisions and assumptions. Use actual sources; no external approval record is required. When `docs/platform/platform.md` exists, note the platform facts this change relies on.

Library and API references: for each library, framework, SDK or cloud API the design depends on, cite the Context7 ID and the repository's pinned version (or the official docs URL when Context7 was unavailable). Rows added to `docs/references/libraries.md` by this change: list or `none`.

## Requirements (EARS)

Number each requirement and write its acceptance criteria as EARS lines with stable IDs `R<n>.<m>`; plan tasks cite them as `_Requirements: R1.1, R2.3_` and verification reports coverage per ID. Never renumber an ID once a plan cites it; retire it with a note instead. Trace each requirement to the intent or a recorded decision. Do not add unrelated scope.

Patterns:

- `WHEN <event> THE <system> SHALL <response>` — event-driven
- `IF <condition> THEN THE <system> SHALL <response>` — unwanted behaviour or guarded condition
- `WHILE <state> THE <system> SHALL <response>` — state-driven
- `THE <system> SHALL <response>` — ubiquitous

### R1. <requirement title> — from intent: <section or decision>

- R1.1 WHEN <event> THE <system> SHALL <response>
- R1.2 IF <condition> THEN THE <system> SHALL <response>

### R2. <requirement title>

- R2.1 THE <system> SHALL <response>

Cover boundaries and failure cases as their own lines. Non-functional requirements (performance, security, operability) use the same notation.

## Design

Explain how the change fits the existing system: affected components, interactions, data/interfaces, and user experience. Describe meaningful alternatives and why this approach is proposed. For UI work, identify supplied designs or the behavior and appearance to compare during verification. Deployment, observability and promotion changes are values files and pipeline config for the `lb-pipelines/app-delivery-kit-vs@1` orb; a new data store, queue or external integration is named here, added to `docs/platform/platform.md`, and gets a threat-model offer.

## Constraints and exclusions

Glossary terms: list each term this change introduces that the session's `[aidlc-glossary]` index lacks, with a one-line definition, and offer an entry from `docs/glossary/template.md`; otherwise write `none`.

Carry forward the intent's scope and actual compatibility, security, UX, or other organisational constraints. Cite relevant policy where applicable; do not invent standards or claim unavailable material was checked.

## Open questions and risks

Record unresolved requirements, trade-offs, assumptions, and likely failure modes. State what needs engineer input and why. Preserve unanswered intent questions rather than manufacturing resolution.

## Proof expectations

Describe the ordinary software tests, runtime observations, and visual comparisons that would demonstrate the requirements, referencing R-IDs so the plan can map tasks and verification can report coverage per requirement. These are expectations for the plan, not executed results or an AI evaluation suite.

## Decision notes (optional)

Summarise useful conversation decisions and their reasons. Ask about material unresolved choices; no named-approver, signature, immutable revision, or external review form is required by this workflow.

## Handoff and changes

Discuss the proposal with the engineer, then use it with the intent in plan mode to prepare `changes/{{change_id}}/plan.md`. Update the spec when requirements or design change and revisit affected plan tasks; do not silently leave implementation based on stale requirements.
