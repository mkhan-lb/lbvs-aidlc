# AIDLC goals

Status: workflow-first scope, revised by the user on 16 September 2026 into the company AIDLC package (`lbvs-aidlc`).

## Purpose

Build the company AI-native development lifecycle for Claude Code based on [Anthropic's AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook) and the Claude Code best practices. Concentrate on how a change moves from a problem to a specified, planned, implemented, verified and reviewed result, using durable artifacts, stage gates and existing AI capabilities.

The earlier requirement to implement the entire playbook before anything else has been narrowed. The full source remains mapped for reference; evaluation infrastructure, configuration-regression gates, approval enforcement, delivery and maintenance are deliberately deferred, not current blockers.

## Current workflow

`/aidlc <change-id>` → `intent.md` → `spec.md` → `plan.md` → build and ordinary verification → review findings → fixes and re-review, with a user-confirmed gate after every stage. Bug fixes run through `/aidlc-fix` and leave `evidence.md`; brownfield repositories start with `/aidlc-onboard`.

An engineer steers the work and decides at each gate whether to continue. Artifacts carry context between sessions. Non-technical originators enter through optional Compound Engineering brainstorming with an engineer's help. We are not building an approval service, autonomous pipeline or new coding-agent platform.

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

Success: a reviewer can see the failing test existed before the fix and the agent could not rewrite it; repeated mistakes reach `AGENTS.md` or a rule through review.

## In scope now

- The `/aidlc` orchestrator with stage gates, worktree-per-change, project-mode detection and brownfield onboarding (`aidlc-onboard`, `aidlc-repo-scout`).
- Model- and user-invocable stage skills (`aidlc-intent` … `aidlc-review`, `aidlc-fix`, `aidlc-learn`), three manual utilities (handoff, resume, ideate) and two scoped subagents.
- The bug-fix evidence loop: failing test, `protect-tests.sh`, `.aidlc/fix/` marker, `changes/<id>/evidence.md`.
- Artifact continuity, explicit plan-save ownership, one-off durable lessons, candidate ideation, decision notes and practical usage recipes.
- Canonical `AGENTS.md` shared instructions with `CLAUDE.md` and `.omp/AGENTS.md` importing it; three hooks (`check-package`, `project-mode`, `protect-tests`) as the only deterministic guardrails.
- Stage-by-stage recommendations of bundled Claude Code skills and marketplace plugins in [docs/PLUGINS.md](docs/PLUGINS.md); nothing installed automatically. Non-technical entry through optional CE brainstorming; caveman opt-in at user scope for engineers only.
- Concrete artifact-aware handoff to existing local reviewers, with prepared/partial/returned status and honest context coverage.
- Review → fix → re-review, with local findings by default.
- A worked local scenario and honest evidence of what was exercised.
- Complete standalone resource export to a new directory; existing-repository adoption remains an explicit reviewed merge, not an automatic installer or company rollout.
- The requested 37-skill ECC library, with pinned provenance, retained licensing, task-scoped adaptations and inactive MCP configuration examples. Importing operational guidance does not activate the deferred services below.

## Deferred

- Evaluation runner and real-task evaluation corpus.
- Configuration-regression gates.
- Approval-boundary enforcement, approval services and managed-control rollout. The three bundled hooks are loop guardrails, not that framework.
- Unattended stage transitions and artifact-triggered jobs; the `/aidlc` gates are user-answered, and "proceed" is never inferred.
- Delivery integration, with **CircleCI** as the intended later CI/CD platform.
- Maintenance, operational monitoring, scheduled security scans and incident integrations.
- Company-specific rollout, marketplace-plugin distribution of this package (tracked on a separate branch) and Kiro/spec-driven extensions.

Deferral does not remove existing repository protections or permit an agent to approve, merge, publish or deploy without the user's instruction.

## Current definition of done

1. The workflow, templates, orchestrator and skills agree on inputs, outputs, gates and handoffs.
2. An engineer can draft and refine artifacts using normal conversation decisions, without enforced external approval machinery.
3. The review approach reuses a documented existing capability and preserves spec/plan context.
4. Local scenarios demonstrate the changed workflow and ordinary verification; unexercised capabilities are explicitly identified.
5. Deferred work is recorded separately and is not demanded before local work can proceed.

Completion of this scope is not a claim that the complete six-stage operational playbook is deployed. See [implementation steps](IMPLEMENTATION_PLAN.md), [future work](FUTURE_WORK.md), [source coverage](docs/COVERAGE.md), and [verification](docs/VERIFICATION.md).
