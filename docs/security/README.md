# Security records

What belongs here, one topic per file:

- `threat-models/<service-or-boundary>.md` from [`threat-model-template.md`](threat-model-template.md): assets, trust boundaries, STRIDE threats, mitigations and residual risk. Write one when `lbvs-aidlc-design` introduces a new external interface, data store, credential or trust boundary; revisit it in the ADR that changes the boundary.
- `findings/YYYY-MM-DD-<source>.md`: results of `/security-review`, the `security-review` skill, dependency advisories or a hosted scan, with triage (fix now, schedule, accept with reason) and the change ID or PR that closed each item. Dismissals stay recorded so later scans can learn from them.
- `patches/` is not a folder: a security fix is an ordinary `/lbvs-aidlc-fix` change whose `evidence.md` links the finding here and the incident record when there was one.

Nothing in this directory is a control. Enforcement lives in CI, branch protection, hooks and managed settings; these files record what was decided and proven. Redact secrets, tokens and customer data before writing.

| Date | Record | Scope | Status |
| --- | --- | --- | --- |
