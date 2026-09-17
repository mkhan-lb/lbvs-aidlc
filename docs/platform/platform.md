# Platform facts for this repository

Status: template — replace every bracketed item or delete the row; never record credentials, tokens or production URLs. Last verified: YYYY-MM-DD by <owner>.

## Service identity

- Service name and `catalog-info.yaml` component: [name]
- Promotion tier: [internal-tool (dev only) | product-service (dev → staging → prod)]
- Owning team / on-call: [team, channel]

## Environments and promotion

| Environment | Cluster / target | Gate | Checks required before the next hold |
| --- | --- | --- | --- |
| dev | [EKS dev via app-delivery-kit] | none | deploy, smoke |
| staging | [ ] | CircleCI approval hold | [deploy, smoke, load test] |
| prod | [ ] | CircleCI approval hold — human decision | [ ] |

## Pipeline

- Orb pin: `lb-pipelines/app-delivery-kit-vs@1` (major only) · config: `.circleci/config.yml`
- Required check: [`pr-gate` or the repository's single required check]
- Values files: `deploy/<env>-values.yaml` · image built once on `main`

## Observability and health

- Datadog service/env/version tags: [ ] · dashboards/monitors: [links]
- Health and readiness endpoints: [paths] · SLOs that exist: [ ]

## Secrets and identity

- Secret store and ExternalSecrets path: [ ] · OIDC roles: [ ] — names only, never values.

## Change rules the stages must respect

- Infrastructure changes are values/pipeline changes for the orb; no hand-rolled Terraform/Helm unless an ADR says otherwise.
- Data stores, queues and external integrations added by a change need an entry here and a threat model under `docs/security/threat-models/`.
- Production promotion is approved by [role] at the CircleCI hold; the decision is recorded in [where].
