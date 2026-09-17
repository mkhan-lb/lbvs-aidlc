# Spike: {{change_id}}

Status: draft
Change ID: {{change_id}}

Record a time-boxed investigation. Replace instructions with what was actually observed; do not invent sources, measurements or decisions. Follow `${CLAUDE_PLUGIN_ROOT}/docs/WORKFLOW.md`. This record informs an intent, spec or ADR — it approves nothing and changes no code.

## Question

State the single question this spike answers, why it matters now and who asked it. Note what "answered" was agreed to mean before the investigation started.

## Time box

Agreed budget (wall-clock or effort), start and end, and whether the box was respected. If it ran out, say what remained uninvestigated rather than filling the gap.

## Findings

Observed facts only, each with its source: repository path and line range, `graphify` `source_location`, documentation URL, command run with verbatim output, or the conversation. Separate observation from inference and mark inferences as such. Findings that could not be confirmed are listed as unconfirmed, not omitted.

## Options

For each realistic option: what it is, what it depends on, its trade-offs (effort, risk, reversibility, operational impact) and the evidence above that supports or weakens it. Include "do nothing" when it is a real option.

## Recommendation

The option the investigator recommends and the reasoning, stated as a recommendation for the engineer to accept, reject or defer. If the evidence does not support a recommendation, say so.

## Open questions

What remains unknown, why it could not be answered within the box, and what it would take to answer it.

## Suggested next step

One of: create or refresh `changes/{{change_id}}/intent.md` (`lbvs-aidlc-intent`), record an architecture decision (`architecture-decision-records` → `docs/adr/`), a further spike with a narrower question, or stop. Name the artifact that would receive this record's conclusions.
