# Spec: {{change_id}}

Status: draft
Change ID: {{change_id}}

Describe the requirements and design for the working intent. Follow `${CLAUDE_PLUGIN_ROOT}/docs/WORKFLOW.md`; this artifact does not grant permissions or create an approval gate.

## Context and inputs

Link `changes/{{change_id}}/intent.md` and relevant inspected code, source records, or supplied designs. Summarise known task decisions and assumptions. Use actual sources; no external approval record is required.

## Requirements and outcomes

Define observable behavior, including relevant boundaries and failure cases. Give requirements useful references for the plan and review, and connect them to the intent. Do not add unrelated scope.

## Design

Explain how the change fits the existing system: affected components, interactions, data/interfaces, and user experience. Describe meaningful alternatives and why this approach is proposed. For UI work, identify supplied designs or the behavior and appearance to compare during verification.

## Constraints and exclusions

Carry forward the intent's scope and actual compatibility, security, UX, or other organisational constraints. Cite relevant policy where applicable; do not invent standards or claim unavailable material was checked.

## Open questions and risks

Record unresolved requirements, trade-offs, assumptions, and likely failure modes. State what needs engineer input and why. Preserve unanswered intent questions rather than manufacturing resolution.

## Proof expectations

Describe the ordinary software tests, runtime observations, and visual comparisons that would demonstrate the requirements. These are expectations for the plan, not executed results or an AI evaluation suite.

## Decision notes (optional)

Summarise useful conversation decisions and their reasons. Ask about material unresolved choices; no named-approver, signature, immutable revision, or external review form is required by this workflow.

## Handoff and changes

Discuss the proposal with the engineer, then use it with the intent in plan mode to prepare `changes/{{change_id}}/plan.md`. Update the spec when requirements or design change and revisit affected plan tasks; do not silently leave implementation based on stale requirements.
