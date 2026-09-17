# Local inputs and deferred integration prerequisites

Current workflow inputs are the engineer's task, relevant repository context and an authorised coding session. Actual implementation/verification additionally needs the project's applicable commands and runtime dependencies. Missing task facts may need clarification; an evaluation corpus, approval service, company role directory or CI account is not required to draft, plan or review locally. See the [workflow](WORKFLOW.md) and [current scope](../GOALS.md).

The external register below is retained for the broader playbook's **deferred integrations**, not as a startup checklist. It does not grant access or authorise changes to a company environment.

## Observed locally

Checked on 16 September 2026:

- Python 3, Git, Make, Node/npm, GitHub CLI and Claude Code are installed.
- Claude Code reports version 2.1.270 and an authenticated Team account. Authentication does not prove Security, Tag, managed-settings or model entitlements.
- GitHub CLI authentication is available. No remote repository has been selected or created for this project, and no account/organisation details or tokens are recorded here.
- A local Git repository is initialised for this package. No commit, push, remote creation or branch protection has been performed by this implementation session.

Use `python3 scripts/aidlc.py doctor` for the local checks. It deliberately does not test external authorities or expose credentials.

## Deferred integration decisions and access

| ID | Prerequisite | Who supplies it | Dependent work | Current state |
| --- | --- | --- | --- | --- |
| E01 | Authoritative remote repository, review workflow, named code owners, branch protection and formal approval records | Repository owner | Future remote review and approval integration, R04, committed worktree history | Not configured. GitHub is a source example for PR hosting; later delivery is CircleCI. Local review needs neither a remote nor new branch protection. |
| E02 | Named originator, product owner, engineer, policy owners, service owner, security lead and release authority | Adopting organisation | P01, D01, B01, release and incident decisions | Roles documented; identities and actual approvals not supplied. |
| E03 | Authoritative security, compliance, brand/UX and engineering policy applicable to the reference application | Policy owners | D01, B04, B05, R01–R03 | No company policy is invented for the generic baseline. A policy skill must name its actual source and owner. |
| E04 | Representative application, executable checks and 20–50 genuine historical tasks with accepted outcomes | Reference-project owner | Future T02 corpus and full-cycle proof | Use the current task's real checks now. No application selection or task corpus is required merely to build the generic workflow. |
| E05 | Approved model access for unattended jobs, funding limits, protected CI credentials and isolated runner environment | Platform owner | T02, R01, R04, M01 | Local interactive authentication exists; CI/service access is not configured. |
| E06 | Administrative deployment of managed settings, network/credential policy and sandbox enforcement | Platform/IT/security | R02, R03, unattended execution | Not deployed. Repository files cannot enforce organisation-wide controls. |
| E07 | Non-production reference deployment, approved deploy/status/rollback tools, permission tiers and release approval authority | Service/release owner | R04, M01, end-to-end demonstration | No target environment or runbook supplied. No deployment or rollback attempted. |
| E08 | Metrics store, metric choice, stable baseline, trigger route and triage owner | Service/platform owner | M01 | No metric source or operational baseline supplied. The source's example thresholds are not company policy. |
| E09 | Claude Security subscription/feature access, repository connection, scanner seats, usage funding and administration | Security/platform owner | M02 | Entitlement and installation not verified. Keep existing static/dependency checks; model scans are additional. |
| E10 | Claude Tag availability, supported incident workspace, Claude/Slack administration, routines, funding and permitted data handling | Platform/on-call owner | M03 | No workspace connection or entitlement verified. Do not substitute a generic chat bot and claim the Tag play is implemented. |
| E11 | Evidence storage, retention/access decisions and measurement collection | Engineering/platform owner | Operational audit and every source measure | Local evidence is recorded in VERIFICATION.md; no remote telemetry or audit store configured. |

These inputs become relevant when their integration is resumed under [future work](../FUTURE_WORK.md). They are deliberately deferred, not current workflow blockers. Existing policies still apply where relevant; do not invent missing policies, identities or approvals.

## Future control authority

- **Repository guidance:** CLAUDE.md, skills, templates and REVIEW.md guide behaviour. Agents and engineers can edit these; they are not hard authorisation boundaries.
- **Repository hooks:** useful for the local inner loop, but insufficient as organisation-wide controls. A hook must use verified input/output semantics and cannot trust an editable status field or arbitrary environment variable as release approval.
- **Managed controls:** deployed by the administrator outside the agent-writable project; confirm effective configuration, supported keys and exceptions on the actual installed version.
- **External controls:** branch protection, reviewer identity, CI secret separation, deployment authorisation and network isolation must be exercised at the authoritative platform.

If enforcement is resumed, do not copy the article's substring-based production hook into service as a general command authoriser. It illustrates the gate, not complete shell parsing or trusted identity verification. No new authorisation mechanism is being implemented now.

## Source versus current product documentation

The [source snapshot](sources/anthropic-playbook.md) fixes the intended plays, not current product syntax or entitlement. [Compatibility notes](COMPATIBILITY.md) identify where the article's worked examples need current documentation or offer weaker guarantees than their prose implies.

No managed policy or automatic permission mode is installed merely by using this package. Missing access prevents that specific external operation; it does not prevent unrelated artifact work or local review, and it is never reported as a passing integration test.
