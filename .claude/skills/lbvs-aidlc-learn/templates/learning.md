# Learning: {{change_id}} — descriptive lesson title

- Status: Verified | Needs re-check | Superseded by <path>
- Last verified: YYYY-MM-DD against <revision or environment>
- Confidence: 0.3 (1–2 observations) | 0.5 (3–5) | 0.7 (6–10) | 0.85 (11+)
- Observations: <count>; change IDs: {{change_id}}
- Scope: project | team

Capture one solved, verified lesson whose reasoning is not readily recoverable from code, tests or existing docs. This is supporting knowledge, not a second spec, plan, rule or approval record. Readers weight every lesson equally, so keep one topic per file and mark a lesson **Needs re-check** rather than leaving a stale one to mislead. Replace the descriptive title, fill only supported content and remove these drafting instructions. If the lesson does not qualify, save nothing.

Confidence follows the observation count above and is only raised when the same lesson is re-observed in another change (`lbvs-aidlc-learn` offers the bump instead of writing a duplicate). Promotion rule: a lesson observed in at least 2 changes with Confidence ≥ 0.8 is a candidate rule for `AGENTS.md` or `.claude/rules/`; the skill proposes it to the engineer and never writes those files itself.

## Problem and durable insight

What actually happened, in which area and conditions? Explain the non-obvious insight and why losing it would plausibly cause recurrence, material risk or substantial rediscovery. A routine change summary is not a lesson.

## Root cause and proven solution

Explain the demonstrated cause or, for a knowledge lesson, the explanatory constraint behind the solution. Describe what worked and why; include only essential examples. Distinguish observed facts, user reports and inferences. Include a failed approach only if actually attempted and useful to the reasoning; do not invent a debugging history.

## Verification and evidence

Name the existing check or observation, exact scope and known outcome, with its source. Distinguish historical passed/failed results, user-reported results and checks not run. State what proves the solution and what the evidence does not establish. Do not represent this capture or document readback as a new test run, deployment or merge confirmation.

## Recurrence and applicability

Explain when to apply this lesson, the practical prevention step and remaining recurrence risk. Preserve caveats, environment/version limits and counterexamples where known; avoid a universal rule from one incident. Unresolved limitations stay visible rather than becoming claimed successes.

## Sources and related knowledge

Link relevant existing `changes/{{change_id}}/` artifacts, current defining source and actual verification evidence, with useful sections or line locations where known. Name missing/unavailable evidence explicitly. Include a related learning only when actually read, explaining the distinction; do not duplicate an existing same-topic lesson. Necessary conversation-only observations must be attributed with enough context to understand their limits. Redact secrets and unrelated personal information.

For an explicitly authorised update, preserve the existing path, useful structure and unrelated content; record the actual update date and what new evidence changed. Optional corpus metadata may be retained, but never claim CE authorship unless CE actually ran.
