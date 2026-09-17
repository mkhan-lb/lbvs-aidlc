## Summary

<Two to four sentences from `changes/{{change_id}}/intent.md`: the problem, the outcome delivered, and explicit non-goals. No invented scope.>

Change: `{{change_id}}`

## Ticket

<Jira key and URL only when genuinely known (key in the change ID, `intent.md` References, or read from the Atlassian MCP); otherwise `none`.>

## Spec / plan

- Spec: `changes/{{change_id}}/spec.md`
- Plan: `changes/{{change_id}}/plan.md`
- Design/ADR links: <paths, or `none`>

## Evidence

<Verification summary copied from the `## Verification evidence` table in `changes/{{change_id}}/review.md` or from `changes/{{change_id}}/evidence.md`, by requirement.>

| R-ID | Check | Observed result | Status |
| --- | --- | --- | --- |

Not run: <checks and reasons, or `none`>

## Review

| Pass | Tier / command | Findings (IDs) | Disposition |
| --- | --- | --- | --- |

Open Important findings: 0 (required to ship). Accepted findings and the engineer's reason: <IDs, or `none`>.

Accepted conventions findings (lbvs-aidlc-conventions-checker, shipped anyway with the engineer's reason): <K-IDs with one-line reason each, or `none`>.

## Knowledge records

- ADR: <`docs/adr/NNNN-*.md` or `none`>
- Incident: <`docs/incidents/…` or `none`>
- Threat model: <`docs/security/threat-models/…` or `none`>
- Lesson: <`docs/solutions/…` or `none`>

## Checklist

- [ ] Repository conventions / pre-commit run: <result, or `not run — reason`>
- [ ] Tests relevant to the change run: <result>
- [ ] No secrets, credentials or `.env` content in the diff
- [ ] `changes/{{change_id}}/` artifacts committed with the code
- [ ] Spec, plan and code agree (no stale artifact)

<This body is rendered by `lbvs-aidlc-ship` from real artifacts. Never tick a box or cite a result that was not observed; write `none` or `not run` instead.>
