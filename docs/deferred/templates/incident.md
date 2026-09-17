# Incident or maintenance finding: {{change_id}}

Status: draft
Change ID: {{change_id}}

Use this draft to retain evidence, decisions and lessons from a real incident or maintenance finding. Do not imply that detection, investigation, remediation, approval or recovery has happened. The draft status describes this document, not the service's health or the incident's operational state.

## Record and trigger

- Author/responsible service owner or on-call engineer: name actual identities and distinguish automated or agent contributions.
- Source work item/incident/finding: system, ID, URL, revision and actual event timestamp with timezone.
- Authority: name the system/record URL holding the incident or finding, whether this document is authoritative or a linked working summary, and the synchronised revision. Preserve the incident channel/thread when that is the audit trail.
- Affected services, users and environments: define scope, observed impact and exclusions; record unknowns explicitly.
- Related release: link the deployed revision, release/pipeline record and deployment time when known. Do not infer causation from timing alone.

## Observations and evidence

Record the actual signal, observation window, baseline, queried data and durable evidence links. Separate facts, hypotheses and confidence.

- Control-band trigger: identify the deterministic detector/configuration revision, breached rule, tier and allowed response; do not let the diagnosis choose its own permissions.
- Scheduled scan: identify the scanned repository/revision, run time, validation result and supplied confidence rating; distinguish an unvalidated hypothesis from a reported finding.
- Channel/ticket trigger: link the initiating message and the requests, diagnosis and subsequent decisions in their original thread.

Use only the applicable trigger details. Do not invent model confidence, thresholds, monitoring services or scan output.

## Investigation and risks

Record the investigated hypotheses, actual read-only checks and observations, their timestamps and actor identities. Link any independent deterministic or adversarial confidence check, its outcome, and escalation when applicable to a headless loop. State what remains unknown, possible alternative causes, and the risks of acting or not acting.

## Human triage and action authority

Record actual service-owner/on-call triage as fix now, schedule, or dismiss, with named human, timestamp, rationale, exact reviewed incident/finding revision and external review/thread URL. Route product-facing findings to the product owner; preserve dismissals so future detection or scans can learn from them.

For every proposed action, identify the existing authorised route: reviewed PR or a specifically pre-approved runbook. Record the exact action/runbook revision, environment, limits, named human authoriser, timestamp and external authorisation URL when approval exists. Production release authorisation remains with the release authority. A channel request, local status edit, or agent diagnosis is not blanket permission to act.

## Actions and outcome verification

Keep proposals separate from executed actions. For each actual action, record actor identity, time, target environment/revision, governing authorisation, result and tool/pipeline evidence. Link rollback execution and its prior rehearsal evidence where relevant.

Record follow-up measurements against the baseline, the observation window, and the person or tool that verified the outcome. Do not claim recovery from a successful command alone; link the metric or behavior evidence and the confirmation in the incident thread. Preserve failed attempts and remaining impact.

## Lessons and next cycle

Capture evidence-backed causes, contributing conditions, and lessons in version control so later investigations can read them. Link any existing lessons record instead of creating an untraceable competing copy.

- Bounded fix: link the PR, code-owner review, tested/merged revisions and release record.
- Wider finding: link a new `intent.md` with its change ID, evidence and proposed outcome; it goes through normal product-owner acceptance, spec and plan decisions.
- Incident or vulnerability fix released: link the resulting regression eval, its provenance and actual execution evidence when available. Record its absence honestly until it exists.
- Follow-up policy, repository-context, detection-band or runbook changes: link the responsible record and actual review, without claiming approval on a human's behalf.

Retain links from the original change/release to this finding and from this finding to its follow-up change. Unresolved questions remain visible rather than becoming completed lessons.
