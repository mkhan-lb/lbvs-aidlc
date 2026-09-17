# Threat model: <service or boundary>

- Date: YYYY-MM-DD · Owners: · Related: change ID, ADR, Jira key
- Status: Draft | Reviewed | Superseded

## System and assets

What the component does, the data it holds or moves (classify it), the identities it trusts, and the dependencies it calls. A diagram or a short list of components is enough.

## Trust boundaries and entry points

Every place data or control crosses from less-trusted to more-trusted: public endpoints, queues, webhooks, admin tools, CI, third-party services, human operators.

## Threats (STRIDE)

| Threat | Category | Entry point | Impact | Likelihood | Mitigation | Residual risk / owner |
| --- | --- | --- | --- | --- | --- | --- |
| | Spoofing / Tampering / Repudiation / Information disclosure / Denial of service / Elevation of privilege | | | | | |

Only list threats you actually reasoned about; an empty row is better than an invented one.

## Decisions and follow-up

Mitigations to build (change IDs), risks accepted (who accepted, until when), and what would trigger a re-review. Link the ADR when a mitigation changes an architectural boundary.
