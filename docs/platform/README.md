# Platform and delivery

This package is generic; the company's cloud infrastructure lives in two internal repositories that the stages read rather than duplicate:

| Repository | Role | How AIDLC uses it |
| --- | --- | --- |
| `Logicbroker/app-template` | GitHub template for new apps: `AGENTS.md`, `AGENT-SETUP.md` (agent-driven repo creation, Dockerfile, per-environment values, CircleCI wiring), `PLATFORM-CAPABILITIES.md`, `OPERATIONS.md`, `INTEGRATIONS.md`, `catalog-info.yaml`, examples for .NET, Go and Python. | **Greenfield:** `lbvs-aidlc-onboard` offers the app-template route before any AIDLC change; a service born from the template already carries its delivery shape. |
| `Logicbroker/app-delivery-kit` | Public CircleCI orb `lb-pipelines/app-delivery-kit-vs@1` (build/push to ECR or ACR, image vulnerability gate, k6 load test, Helm deploy/diff, PR preview, coverage floor, CodeArtifact login/publish, DORA events) plus the `central-app` Helm chart (Rollouts, HPA, PDB, ExternalSecrets, Datadog monitors, HTTPRoute). | **Design/plan:** deployment, observability and promotion changes are expressed as values files and pipeline config for this orb, never as hand-rolled infrastructure. |

Both repositories are internal: fetch their files with an authenticated `gh api repos/<owner>/<repo>/contents/<path> -H "Accept: application/vnd.github.raw+json"`; plain raw links 404. The agent needs the CircleCI, Datadog and GitHub MCP servers for pipeline, monitor and repository reads — app-template's setup walks through that.

## What every adopting repository records

Fill [`platform.md`](platform.md) once per service from these sources and keep it current; the stages read it before proposing infrastructure or deployment work:

- environments and the promotion path (dev → staging → prod, one image built on `main` and promoted unchanged; staging and prod behind CircleCI approval holds — a human decision, never auto-promoted),
- the pipeline (orb pin, jobs, the single required check), where values files live, and which checks gate each hold,
- observability identity (Datadog service tags, health/readiness contract, monitors that exist),
- secrets and identity (ExternalSecrets store, OIDC roles; never values),
- catalog metadata (`catalog-info.yaml`, promotion tier: internal tool vs product service),
- deployment authority: who approves a production hold and where that decision is recorded.

Nothing in this directory is a control. Branch protection, the `pr-gate` check, CircleCI holds and Kyverno policies enforce; these files tell the stages what exists so they design for it and do not invent alternatives. Delivery integration itself (running pipelines, promoting images) remains deferred work in `FUTURE_WORK.md`; the stages prepare reviewable configuration and evidence, and a human triggers delivery.
