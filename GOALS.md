# AIDLC goals

Status: workflow-first scope, revised by the user on 16 September 2026 into the company AIDLC package (`lbvs-aidlc`).

## Purpose

Build the company AI-native development lifecycle for Claude Code based on [Anthropic's AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook) and the Claude Code best practices. Concentrate on how a change moves from a problem to a specified, planned, implemented, verified and reviewed result, using durable artifacts, stage gates and existing AI capabilities.

The earlier requirement to implement the entire playbook before anything else has been narrowed. The full source remains mapped for reference; evaluation infrastructure, configuration-regression gates, approval enforcement, delivery and maintenance automation are deliberately deferred, not current blockers. The knowledge the workflow produces — decisions, incidents, security records, lessons — is in scope now as plain Markdown the engineer confirms.

## Current workflow

`/aidlc [change-id]` → `intent.md` → `spec.md` → `plan.md` → build and ordinary verification → review findings → fixes and re-review, with a gate after every stage. The change ID is optional: the workflow resolves it from the branch, the machine-local `.aidlc/current` pointer or the only open change, and `python3 scripts/aidlc.py status` shows what exists; an ID may carry a ticket key as a prefix (`vs-1234-order-export`), and `/aidlc-ticket <KEY>` derives it from the Jira or GitHub record itself. `/aidlc-spike` answers a question that needs depth before intent or design. Bug fixes run through `/aidlc-fix` and leave `evidence.md`; brownfield repositories start with `/aidlc-onboard`.

An engineer steers the work and decides at each gate whether to continue. Where the engineer prefers less clicking, they state a flow policy for the run and a stage may advance itself — announced, interruptible, and only when the artifact was saved and read back, nothing is open, no check failed or was skipped and the next step is neither review, a commit-class action, nor build unless that policy includes build. The default remains confirm-each-stage. Artifacts carry context between sessions. Non-technical originators enter through optional Compound Engineering brainstorming with an engineer's help. We are not building an approval service, autonomous pipeline or new coding-agent platform.

## Goals

### G1 — Make the everyday workflow clear

Explain each activity's input, work, output and next action. Use the Anthropic artifact names and preserve the distinction between the problem, requirements/design, and implementation plan.

Success: an engineer can follow the [workflow guide](docs/WORKFLOW.md) without relying on hidden conversation history or external administration.

### G2 — Make artifacts useful, not bureaucratic

Keep intent, spec, plan and review notes together under one change ID. Record actual decisions, unresolved questions, scope changes and evidence. Update the affected artifacts when the engineer changes direction.

Success: another session can continue from the files. Drafting and local implementation do not require an external approval URL, a prescribed product-owner identity, or a remote integration.

### G3 — Reuse existing review capability

Investigate Claude Code's existing review features and first-party plugins, plus [Oh My Pi](https://github.com/can1357/oh-my-pi). Prefer a small artifact-aware handoff to an existing reviewer over a custom review engine.

Success: documented options distinguish local review, PR access, comment publication and hosted automation; exact commands, side effects and limitations are sourced. No silent plugin installation or remote posting.

### G4 — Keep real task verification

Use the application's existing tests, build, lint and runtime/visual checks as appropriate to the change. Report what actually ran and what did not.

Success: review receives evidence about the change. This is ordinary software verification, not an AI evaluation runner or a configuration-regression service.

### G5 — Keep the generic workflow adaptable

Use repository context and the engineer's task inputs without hardcoding company architecture, policies, identities or services. Detect greenfield versus brownfield at session start and let onboarding capture the repository's real conventions into a short `CLAUDE.md` and path-scoped rules on confirmation. Existing organisational rules and tool permissions still apply.

Success: the package works in a new repository and in an existing codebase without choosing a company reference application or configuring CI/admin accounts first.

### G6 — Close the bug-fix loop with evidence

Fix bugs failing-test-first, protect that test while the fix is written, and record reproduction, verification and references (Jira, PR, incident) in `evidence.md`. Offer one lesson afterwards.

Success: a reviewer can see the failing test existed before the fix and the agent could not rewrite it; repeated mistakes reach `AGENTS.md` or a rule through review; a defect that arrived through an alert leaves an incident record the next investigation can read.

### G7 — Keep what the workflow learns, in the right place

Record architecture decisions in `docs/adr/`, incidents in `docs/incidents/`, threat models and triaged security findings in `docs/security/`, and verified non-obvious lessons in `docs/solutions/` — each from a template, each written only after the engineer confirms, each read back. Design, spike, review and fix offer these records at the moment they become relevant; nothing is written automatically. A correction that keeps recurring becomes a rule in `AGENTS.md` or `.claude/rules/` instead of another record, and stale records are marked or superseded rather than trusted. The model is adapted from the team-knowledge chapter of AWS's [aidlc-workflows](https://github.com/awslabs/aidlc-workflows/blob/main/docs/harness-engineering/07-team-knowledge.md) and the ADR template shape of the sibling Logicbroker `shared-services-aidlc` repository, in our own words.

Success: a new session can find why a boundary exists, what broke before and what was decided about it without replaying old conversations, and no record claims a check or approval that did not happen.

## In scope now

- The `/aidlc` orchestrator with stage gates, an optional supervised auto-advance policy, change-ID resolution (branch, `.aidlc/current`, only open change), descriptive per-change worktrees named by the `WorktreeCreate` hook, project-mode detection and brownfield onboarding (`aidlc-onboard`, `aidlc-repo-scout`).
- Model- and user-invocable stage skills (`aidlc-intent` … `aidlc-review`, `aidlc-fix`, `aidlc-learn`), the entry helpers `aidlc-ticket` (Jira/GitHub intake, read-only) and `aidlc-spike` (time-boxed investigation into `spike.md`), three manual utilities (handoff, resume, ideate) and two scoped subagents — 15 `aidlc*` commands.
- The bug-fix evidence loop: failing test, `protect-tests.sh`, `.aidlc/fix/` marker, `changes/<id>/evidence.md`.
- Artifact continuity, explicit plan-save ownership, one-off durable lessons, candidate ideation, decision notes and practical usage recipes.
- Canonical `AGENTS.md` shared instructions with `CLAUDE.md` and `.omp/AGENTS.md` importing it; four hooks (`check-package`, `project-mode`, `protect-tests`, `worktree-create`) as the only deterministic guardrails.
- Stage-by-stage recommendations of bundled Claude Code skills and marketplace plugins in [docs/PLUGINS.md](docs/PLUGINS.md); nothing installed automatically. Non-technical entry through optional CE brainstorming; caveman opt-in at user scope for engineers only.
- The four knowledge stores (`docs/adr/`, `docs/incidents/`, `docs/security/`, `docs/solutions/`) with their indexes and templates; the imported `architecture-decision-records` and `doc-coauthoring` skills wired to them; ADR, threat-model, incident and security-finding offers in design, spike, review and fix, all confirmation-before-write.
- Project MCP declarations for `context7`, `github` and `atlassian` in `.mcp.json` (no credentials; Claude asks once per project), `doctor` reporting of tool presence and MCP authentication state, and `doctor --install` for missing optional tools (`graphify`, `codegraph`, `gh`).
- Concrete artifact-aware handoff to existing local reviewers, with prepared/partial/returned status and honest context coverage.
- Review → fix → re-review, with local findings by default.
- A worked local scenario and honest evidence of what was exercised.
- Complete standalone resource export to a new directory; existing-repository adoption remains an explicit reviewed merge, not an automatic installer or company rollout.
- The requested 37-skill ECC library, with pinned provenance, retained licensing, task-scoped adaptations and the inactive ECC MCP catalog kept as a reference snapshot (the live configuration is `.mcp.json`). Importing operational guidance does not activate the deferred services below.

## Deferred

- Evaluation runner and real-task evaluation corpus.
- Configuration-regression gates.
- Approval-boundary enforcement, approval services and managed-control rollout. The four bundled hooks are loop guardrails, not that framework.
- Unattended stage transitions and artifact-triggered jobs. The `/aidlc` gates stay in the engineer's session: they are either answered by the engineer or auto-advanced under a policy the engineer stated in that conversation, announced and interruptible; "proceed" is never inferred, never assumed from an unstated policy, and never applied to review or to commit, push, merge, publication or deployment.
- Delivery integration, with **CircleCI** as the intended later CI/CD platform.
- Maintenance automation: operational monitoring, scheduled hosted security scans and incident-channel integrations that would write into `docs/incidents/` and `docs/security/` without an engineer. The stores and the manual offers exist now; the feeds do not.
- Company-specific rollout, marketplace-plugin distribution of this package (tracked on a separate branch) and Kiro/spec-driven extensions.

Deferral does not remove existing repository protections or permit an agent to approve, merge, publish or deploy without the user's instruction.

## Current definition of done

1. The workflow, templates, orchestrator and skills agree on inputs, outputs, gates and handoffs.
2. An engineer can draft and refine artifacts using normal conversation decisions, without enforced external approval machinery.
3. The review approach reuses a documented existing capability and preserves spec/plan context.
4. Local scenarios demonstrate the changed workflow and ordinary verification; unexercised capabilities are explicitly identified.
5. Deferred work is recorded separately and is not demanded before local work can proceed.

Completion of this scope is not a claim that the complete six-stage operational playbook is deployed. See [implementation steps](IMPLEMENTATION_PLAN.md), [future work](FUTURE_WORK.md), [source coverage](docs/COVERAGE.md), and [verification](docs/VERIFICATION.md).
