# Incident and maintenance records

One file per real incident or maintenance finding: `YYYY-MM-DD-short-title.md`, from [`template.md`](template.md). The record holds evidence, human triage, authorised actions and verified outcome — never an implied recovery. `/aidlc-fix` offers to create one when the defect arrived through an alert or incident link, and links the record from `changes/<change-id>/evidence.md`.

Each closed record should point to its fix (change ID, PR), any wider `intent.md` it spawned, the regression test or eval that now guards it, and a lesson under `docs/solutions/` when one qualified. Unresolved questions stay visible; do not turn them into completed lessons. The live incident channel or ticket remains the authoritative timeline; this file is the durable, reviewable summary the next investigation reads first.

| Date | Title | Services | Status | Follow-up |
| --- | --- | --- | --- | --- |
