# Review record: {{change_id}}

Change ID: {{change_id}}
Latest pass: <N> · tier <standard / escalated / maximum / cloud> · execution status <prepared — not run / running / returned / partial / failed>
Open Important findings: <count or 0> · fix cycles used: <n> of 3

Report findings and actual evidence, not approval. Follow `${CLAUDE_PLUGIN_ROOT}/docs/WORKFLOW.md`, `REVIEW.md` (the repository's own file, else `${CLAUDE_PLUGIN_ROOT}/REVIEW.md`), and `${CLAUDE_PLUGIN_ROOT}/skills/lbvs-aidlc-review/references/review-options.md`. Use this shape in conversation; persist to `changes/{{change_id}}/review.md` only when specifically requested after review results return. Preparation alone is not an executed review. Keep the review report-only; do not run the application/checks, fix code, publish, or install anything.

## Same-change intent and policy

- `changes/{{change_id}}/intent.md`: intended outcome and non-goals actually supplied:
- `changes/{{change_id}}/spec.md`: acceptance criteria (`R<n>.<m>` EARS lines) and boundaries supplied:
- `changes/{{change_id}}/plan.md` and linked design: approach, decisions and deviations supplied:
- Relevant `CLAUDE.md` instructions and applicable `REVIEW.md` (the repository's own file, else `${CLAUDE_PLUGIN_ROOT}/REVIEW.md`) contents supplied, including Bugs/Security/Compliance, severity, exclusions and evidence requirements:
- Missing/unreadable artifacts, unknown policy and unconfirmed provider context coverage:

Do not claim automatic policy/artifact discovery. Separate what the wrapper read from what the reviewer actually received or inspected.

## Verification evidence

Recorded by `lbvs-aidlc-verify` (or the fix loop) before review; coverage by requirement, not just by command.

| R-ID | Check (command / interaction) | Exercised revision and environment | Observed result | Status (pass / fail / not run — reason) |
| --- | --- | --- | --- | --- |

Only record execution supported by actual evidence; reading test source is not executing tests. A build alone is not behavioral proof. Note where evidence is stale or does not exercise the reviewed scope.

## Pass 1

Repeat this whole section for every pass (`## Pass 2`, …), appending below the previous one; never rewrite or delete an earlier pass. Re-reviews after a fix pass run at **escalated** unless the engineer chose a higher tier.

### Reviewer and execution

- Tier and exact command (`standard` = `/code-review high`, `escalated` = `/code-review xhigh`, `maximum` = `/code-review max`, `cloud` = `/code-review ultra`):
- Selected provider and identity/provenance actually observed; exposure in this session (model-invocable Skill / supported command or agent / user-only command / unavailable / unknown):
- Execution status: prepared — not run / running / returned / partial / failed; started/returned time and native result/session reference:
- Context delivery mechanism; evidence the reviewer received the packet, artifacts and `REVIEW.md` (the repository's own file, else `${CLAUDE_PLUGIN_ROOT}/REVIEW.md`) policy (or unconfirmed):
- Errors, interrupted work, denied permissions and missing prerequisites:
- If not run: separate copyable provider command and complete filled-in handoff packet; exact engineer action still required. Do not label this as findings.

### Revision reviewed and coverage

- Scope kind and semantics: merge-base-to-head / tip-to-tip / staged + unstaged + untracked / explicitly identified subset:
- Actual base/head/merge-base SHAs, or working-tree HEAD/unborn state:
- Captured tracked diff and staged/unstaged path inventory; renamed/deleted paths; untracked content supplied:
- Unchanged supporting files and callers inspected; provider-reported inspected paths:
- Excluded, filtered, unreadable, binary, unrelated or otherwise unreviewed paths; reason for each gap:
- Scope freshness (current / stale / unknown): state comparison at preparation, invocation and return; later edits not covered:

An unchanged HEAD or timestamp alone does not establish working-tree freshness. No-findings text applies only to actual inspected scope; partial, failed, unavailable or stale coverage is not a clean bill.

### Findings

Finding IDs are stable across passes: `R1, R2 …` in first-seen order. A later pass reuses the ID for the same finding and appends new numbers; never renumber. Preserve the concrete returned findings, not a count. Repeat this block per finding:

#### R<n> — <native title>

- Native finding text (trigger, impact and reasoning), verbatim:
- Native severity/priority, category and confidence, where supplied:
- File/line range or artifact location in the reviewed snapshot:
- Provider's evidence/reproduction and stated uncertainty; proposed versus executed reproduction:
- Recommended correction/question:
- AIDLC policy mapping: Bugs / Security / Compliance; **Important** / **nit**; any disagreement with the provider explained:
- Requirement ID(s) or intended behavior affected:
- Disposition: open / fixed / accepted — or fix claimed — not re-reviewed / not rechecked:
- Disposition evidence (re-review assessment reference) and who made any acceptance decision:

If no findings were returned, quote the provider's bounded result and its actual coverage; retain the native verdict, explanation and confidence separately — a "correct" verdict is not approval. If no provider result exists, write `no provider result`, not `no findings`. An ADR gap is a Compliance finding with its own ID, never a blocker.

### Wrapper observations

Separately labelled artifact-alignment observations made during reconciliation; do not attribute them to the provider. Mismatches with intended behavior, stale artifacts, unresolved decisions, questions and unknowns. Preserve native findings even when the wrapper disagrees.

### Checks run since the previous pass

| R-ID | Check or interaction | Exercised revision and environment | Actual result | Evidence reference | Executed / failed / proposed / not run |
| --- | --- | --- | --- | --- | --- |

The review pass itself runs nothing. For fixes performed in a separately authorised build pass, include pre-fix evidence when available and the post-fix result; never manufacture a historical failure.

## Fix and re-review history

| Finding ID | Pass first seen | Prior disposition | Agreed fix / engineer acceptance reason | Fix pass scope and check evidence | Re-review pass and returned assessment | Current disposition |
| --- | --- | --- | --- | --- | --- | --- |

Identify the separate authorisation for each fix pass; this report authorises none. A claimed fix is `fixed` only when a returned re-review assessment and evidence support it. Findings outside a re-review's scope stay `not rechecked`; a no-findings response must not silently resolve them. After **3 fix cycles**, or when a pass returns zero Important findings, the loop stops and the engineer decides.

## Remaining risk and engineer handoff

Blockers, unreviewed behavior, missing evidence/context and concrete next actions. Human review and repository safeguards remain; this report grants no merge, release or posting authority.

## References

Only links supplied by the user or read back from a tool (`gh`, git log, Atlassian MCP): PR URL recorded by `lbvs-aidlc-ship`, ticket, ADR/incident/threat-model paths. Never guess a URL.

If saving was requested: record the destination and report actual post-write Read confirmation in the conversation. A Write acknowledgement alone does not verify persistence; a failed read-back is an unverified save. Saving does not expand reviewed scope.
