# Review record: {{change_id}}

Change ID: {{change_id}}
Execution status: prepared — not run / running / returned / partial / failed
Scope freshness: current / stale / unknown

Report findings and actual evidence, not approval. Follow `${CLAUDE_PLUGIN_ROOT}/docs/WORKFLOW.md`, `REVIEW.md` (the repository's own file, else `${CLAUDE_PLUGIN_ROOT}/REVIEW.md`), and `.claude/skills/aidlc-review/references/review-options.md`. Use this shape in conversation; persist to `changes/{{change_id}}/review.md` only when specifically requested after review results return. Preparation alone is not an executed review. Keep the review report-only; do not run the application/checks, fix code, publish, or install anything.

## Reviewer and execution

- Selected provider and identity/provenance actually observed:
- Exposure observed in this session: model-invocable Skill / supported command or agent / user-only command / unavailable / unknown:
- Actual invocation, effort/menu choice, and checkout (or `not invoked` with reason):
- Context delivery mechanism; evidence the reviewer received the packet, artifacts and `REVIEW.md` (the repository's own file, else `${CLAUDE_PLUGIN_ROOT}/REVIEW.md`) policy (or unconfirmed):
- Started/returned time and actual native result/session reference, if present:
- Errors, interrupted work, denied permissions and missing prerequisites:
- If not run: separate copyable provider command and complete filled-in handoff packet; exact engineer action still required. Do not label this section as findings.

## Scope snapshot and coverage

- Scope kind and semantics: merge-base-to-head / tip-to-tip / staged + unstaged + untracked / explicitly identified subset:
- Actual base/head/merge-base SHAs, or working-tree HEAD/unborn state:
- Captured tracked diff and staged/unstaged path inventory; renamed/deleted paths:
- Untracked path/content inventory supplied, and paths actually reviewed:
- Unchanged supporting files inspected (separate from the changed/untracked inventory):
- Provider-reported inspected paths and surrounding callers/source:
- Excluded, filtered, unreadable, binary, unrelated or otherwise unreviewed paths; reason for each gap:
- State comparison at preparation, invocation and return; changed paths/revisions or unavailable comparison:
- What this result covers now; any stale scope or unreviewed later edits:

An unchanged HEAD or timestamp alone does not establish working-tree freshness. No-findings text applies only to actual inspected scope; partial, failed, unavailable or stale coverage is not a clean bill.

## Same-change intent and policy

- `changes/{{change_id}}/intent.md`: intended outcome and non-goals actually supplied:
- `changes/{{change_id}}/spec.md`: relevant behavior, boundaries and acceptance criteria supplied:
- `changes/{{change_id}}/plan.md` and linked design: approach, decisions and deviations supplied:
- Prior `review.md`/native result and stable finding IDs supplied:
- Relevant `CLAUDE.md` instructions and applicable `REVIEW.md` (the repository's own file, else `${CLAUDE_PLUGIN_ROOT}/REVIEW.md`) contents supplied, including Bugs/Security/Compliance, severity, exclusions and evidence requirements:
- Missing/unreadable artifacts, unknown policy and unconfirmed provider context coverage:

Do not claim automatic policy/artifact discovery. Separate what the wrapper read from what the reviewer actually received or inspected.

## Native provider findings

Preserve the concrete returned findings, not just a count or generic summary. Repeat this block for each finding and retain stable IDs across re-reviews:

### {{finding_id}} — {{native_title}}

- Native finding text (trigger, impact and reasoning):
- Native severity/priority, category and confidence, where supplied:
- File/line range or artifact location in the reviewed snapshot:
- Provider's evidence/reproduction and stated uncertainty; distinguish a proposed reproduction from an executed one:
- Recommended correction/question:
- AIDLC policy mapping: Bugs / Security / Compliance; important / nit; explanation of any disagreement with the provider:
- Relevant requirement or intended behavior:
- Disposition: open / fix claimed — not re-reviewed / resolved / not rechecked / dismissed with reason:
- Disposition evidence and who made any dismissal decision:

If no findings were returned, quote or faithfully retain the provider's bounded result and identify its actual coverage. Retain the native overall verdict, explanation and confidence separately; a “correct” verdict is not approval. If no provider result exists, write `no provider result`, not `no findings`.

## Wrapper observations and unanswered questions

Separately label artifact-alignment observations made during reconciliation; do not attribute them to the provider. Identify mismatches with intended behavior, stale artifacts, unresolved decisions, questions and unknowns. Preserve native findings even when the wrapper disagrees, explaining the difference rather than silently suppressing them.

## Existing verification evidence

| Check or interaction | Exercised revision/scope and environment | Actual result | Evidence reference | Executed previously / failed / proposed / not run |
| --- | --- | --- | --- | --- |

Only record execution supported by actual evidence. Reading test source is not executing tests. This review pass runs no tests, application, builds, formatters or reproduction scripts. For fixes performed in a separately authorised implementation pass, include actual pre-fix evidence when available and the post-fix result; never manufacture a historical failure. Note where evidence is stale or does not exercise the reviewed scope.

## Fix and re-review history

| Finding ID | Prior disposition and scope | Agreed fix / engineer dismissal | New scope and actual check evidence | Returned re-review assessment | Current disposition / unrechecked limitation |
| --- | --- | --- | --- | --- | --- |

Identify the separate authorisation for any fix pass; this report does not authorise fixes. Record the new invocation/result and old/new snapshots. Recheck affected prior IDs and new regressions in the changed scope. A claimed fix is not resolved until the returned re-review assessment and evidence support it. Keep findings outside that scope explicitly not rechecked; a no-findings response must not silently resolve them.

## Remaining risk and engineer handoff

State blockers, unreviewed behavior, missing evidence/context and concrete next actions. Retain human review and repository safeguards; this report grants no merge, release or posting authority.

If saving was requested: record the destination and report actual post-write Read confirmation in the conversation. A Write acknowledgement alone does not verify persistence. A failed read-back is an unverified save, not success; saving the report does not expand reviewed scope.
