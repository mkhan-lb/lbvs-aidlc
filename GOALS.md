# AIDLC goals

Status: workflow-first scope, revised by the user on 16 September 2026 into the company AIDLC package (`lbvs-aidlc`).

## Purpose

Build the company AI-native development lifecycle for Claude Code based on [Anthropic's AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook) and the Claude Code best practices. Concentrate on how a change moves from a problem to a specified, planned, implemented, verified and reviewed result, using durable artifacts, stage gates and existing AI capabilities.

The earlier requirement to implement the entire playbook before anything else has been narrowed. The full source remains mapped for reference; evaluation infrastructure, configuration-regression gates, approval enforcement, delivery and maintenance automation are deliberately deferred, not current blockers. The knowledge the workflow produces — decisions, incidents, security records, lessons — is in scope now as plain Markdown the engineer confirms.

## Current workflow

`/lbvs-aidlc [change-id]` → `intent.md` → `spec.md` → `plan.md` → build and ordinary verification → review findings → fixes and re-review → `/lbvs-aidlc-ship`, with a gate after every stage. Acceptance criteria carry stable IDs (`R1.1`) from spec to plan tasks to the verification table, so review sees what is covered. The change ID is optional: the workflow resolves it from the branch, the machine-local `.aidlc/current` pointer or the only open change, and `python3 scripts/aidlc.py status` shows what exists; an ID may carry a ticket key as a prefix (`vs-1234-order-export`), and `/lbvs-aidlc-ticket <KEY>` derives it from the Jira or GitHub record itself. `/lbvs-aidlc-spike` answers a question that needs depth before intent or design. Bug fixes run through `/lbvs-aidlc-fix` and leave `evidence.md`; brownfield repositories start with `/lbvs-aidlc-onboard`; a change whose review pass is clean ships through `/lbvs-aidlc-ship`, which asks before committing and never merges.

An engineer steers the work and decides at each gate whether to continue. Where the engineer prefers less clicking, they state a flow policy for the run and a stage may advance itself — announced, interruptible, and only when the artifact was saved and read back, nothing is open, no check failed or was skipped and the next step is neither review, a commit-class action, nor build unless that policy includes build. Under the policy that includes build, the review loop's fix → verify → re-review cycles may also continue by themselves, at most three times before it stops and asks. The default remains confirm-each-stage. Artifacts carry context between sessions. Non-technical originators enter through optional Compound Engineering brainstorming with an engineer's help. We are not building an approval service, autonomous pipeline or new coding-agent platform.

## Goals

### G1 — Make the everyday workflow clear

Explain each activity's input, work, output and next action. Use the Anthropic artifact names and preserve the distinction between the problem, requirements/design, and implementation plan.

Success: an engineer can follow the [workflow guide](docs/WORKFLOW.md) without relying on hidden conversation history or external administration.

### G2 — Make artifacts useful, not bureaucratic

Keep intent, spec, plan and review notes together under one change ID. Record actual decisions, unresolved questions, scope changes and evidence. Update the affected artifacts when the engineer changes direction.

Success: another session can continue from the files. Drafting and local implementation do not require an external approval URL, a prescribed product-owner identity, or a remote integration.

### G3 — Reuse existing review capability

Investigate Claude Code's existing review features and first-party plugins, plus [Oh My Pi](https://github.com/can1357/oh-my-pi). Prefer a small artifact-aware handoff to an existing reviewer over a custom review engine, and bound the loop: tiers named for the bundled `/code-review` effort levels (standard `high`, escalated `xhigh`, maximum `max`, cloud `ultra`), findings classified Important or nit with stable IDs, re-review after each fix pass, and a hard stop after three fix cycles.

Success: documented options distinguish local review, PR access, comment publication and hosted automation; exact commands, side effects and limitations are sourced; an engineer can see from `review.md` which pass ran at which tier and which findings closed. No silent plugin installation or remote posting.

### G4 — Keep real task verification

Use the application's existing tests, build, lint and runtime/visual checks as appropriate to the change. Report what actually ran and what did not.

Success: review receives evidence about the change. This is ordinary software verification, not an AI evaluation runner or a configuration-regression service.

### G5 — Keep the generic workflow adaptable

Use repository context and the engineer's task inputs without hardcoding company architecture, policies, identities or services. Detect greenfield versus brownfield at session start and let onboarding capture the repository's real conventions into a short `CLAUDE.md` and path-scoped rules on confirmation. Existing organisational rules and tool permissions still apply.

Success: the package works in a new repository and in an existing codebase without choosing a company reference application or configuring CI/admin accounts first.

### G6 — Close the bug-fix loop with evidence

Fix bugs failing-test-first, protect that test while the fix is written, and record the EARS triad (Current / Expected / Unchanged), reproduction, verification and references (Jira, PR, incident) in `evidence.md`. Offer one lesson afterwards.

Success: a reviewer can see the failing test existed before the fix and the agent could not rewrite it, and which `SHALL CONTINUE TO` line each regression test defends; repeated mistakes reach `AGENTS.md` or a rule through review; a defect that arrived through an alert leaves an incident record the next investigation can read.

### G7 — Keep what the workflow learns, in the right place

Record architecture decisions in `docs/adr/`, incidents in `docs/incidents/`, threat models and triaged security findings in `docs/security/`, the library documentation that settled real questions in `docs/references/`, and verified non-obvious lessons in `docs/solutions/` — each from a template, each written only after the engineer confirms, each read back. `docs/platform/` sits beside them as a pointer layer to the company platform repositories, filled once per adopting service. Design, spike, review and fix offer these records at the moment they become relevant; nothing is written automatically. Lessons carry `Confidence`, `Observations` and `Scope`; a lesson observed in two or more changes at confidence ≥0.8 is proposed as a rule candidate, never auto-written. A correction that keeps recurring becomes a rule in `AGENTS.md` or `.claude/rules/` instead of another record, and stale records are marked or superseded rather than trusted. The model is adapted from the team-knowledge chapter of AWS's [aidlc-workflows](https://github.com/awslabs/aidlc-workflows/blob/main/docs/harness-engineering/07-team-knowledge.md) and the ADR template shape of the sibling Logicbroker `shared-services-aidlc` repository, in our own words; the lesson schema borrows from ECC's `continuous-learning-v2`, whose hooks and background observer were deliberately not imported.

Success: a new session can find why a boundary exists, what broke before and what was decided about it without replaying old conversations, and no record claims a check or approval that did not happen.

### G8 — Ship without a shortcut

Turn a clean review pass into a commit, a pushed `aidlc/<change-id>` branch and a pull request through one skill that reads its preconditions from disk, shows the diff, asks exactly three options, titles the commit with the Jira key when the change carries one, commits the `changes/<change-id>/` artifacts with the code and renders the PR body from a template with the evidence and review summary. It never merges, approves, enables auto-merge or edits branch protection; pipelines and promotion remain with CircleCI and a human.

Success: the PR a reviewer opens already links the ticket, spec, plan, verification evidence and review passes, and nothing reached `origin` without the engineer choosing it in that conversation.

### G9 — Design against current docs and the real platform

Resolve library, framework, SDK and cloud APIs through Context7 before designing, planning, implementing or fixing against them, and cite the ID and pinned version in the artifact. Point at the company platform (`Logicbroker/app-template`, the `lb-pipelines/app-delivery-kit-vs@1` orb) through `docs/platform/` rather than copying it, and express deployment and observability changes as orb configuration. Ship default conventions that a greenfield repository can adopt with one command and a brownfield repository keeps its own.

Success: no artifact relies on a remembered API signature; a new data store, queue or integration has a `platform.md` entry and a threat-model offer; `python3 scripts/aidlc.py conventions` never overwrites a file the repository already owns.

## In scope now

- The `/lbvs-aidlc` orchestrator with stage gates, an optional supervised auto-advance policy, change-ID resolution (branch, `.aidlc/current`, only open change), descriptive per-change worktrees named by the `WorktreeCreate` hook, project-mode detection and brownfield onboarding (`lbvs-aidlc-onboard`, `lbvs-aidlc-repo-scout`), and the bounded review loop (tiers, Important/nit, stable finding IDs, three fix cycles).
- Model- and user-invocable stage skills (`lbvs-aidlc-intent` … `lbvs-aidlc-review`, `lbvs-aidlc-fix`, `lbvs-aidlc-learn`), the entry helpers `lbvs-aidlc-ticket` (Jira/GitHub intake, read-only) and `lbvs-aidlc-spike` (time-boxed investigation into `spike.md`), the exit helper `lbvs-aidlc-ship` (commit, push, PR; always asks; never merges), the setup wizard `lbvs-aidlc-init`, three manual utilities (handoff, resume, ideate) and six scoped subagents (`lbvs-aidlc-verifier`, `lbvs-aidlc-repo-scout`, `lbvs-aidlc-design-reviewer`, `lbvs-aidlc-threat-modeler`, `lbvs-aidlc-test-critic`, `lbvs-aidlc-conventions-checker`, each with an `.omp/agents/` counterpart) — 17 `lbvs-aidlc*` commands.
- Kiro-derived traceability: EARS acceptance criteria with stable R-IDs in `spec.md`, `_Requirements:_` trace lines on plan tasks, one task at a time in build with ticks only after the task's check, a per-requirement verification table, and the EARS triad in `evidence.md` (ideas credited to [Kiro specs](https://kiro.dev/docs/specs/); no Kiro tooling).
- The Context7 step in design, plan, build and fix, with `docs/references/libraries.md` as the log of lookups that settled real questions.
- The `docs/platform/` pointer layer (app-template route, app-delivery-kit orb, per-repository `platform.md`) and the conventions defaults in `templates/conventions/` with `python3 scripts/aidlc.py conventions [--apply]` — greenfield adopts, brownfield keeps.
- The bug-fix evidence loop: failing test, `protect-tests.sh`, `.aidlc/fix/` marker, `changes/<id>/evidence.md`.
- Artifact continuity, explicit plan-save ownership, one-off durable lessons, candidate ideation, decision notes and practical usage recipes.
- Canonical `AGENTS.md` shared instructions with `CLAUDE.md` and `.omp/AGENTS.md` importing it; four hooks (`check-package`, `project-mode`, `protect-tests`, `worktree-create`) as the only deterministic guardrails.
- Stage-by-stage recommendations of bundled Claude Code skills and marketplace plugins in [docs/PLUGINS.md](docs/PLUGINS.md); nothing installed automatically. Non-technical entry through optional CE brainstorming; caveman opt-in at user scope for engineers only.
- The five knowledge stores (`docs/adr/`, `docs/incidents/`, `docs/security/`, `docs/references/`, `docs/solutions/`) with their indexes and templates, plus `docs/platform/`; the imported `architecture-decision-records` and `doc-coauthoring` skills wired to them; ADR, threat-model, incident and security-finding offers in design, spike, review and fix, all confirmation-before-write; lessons with `Confidence`/`Observations`/`Scope` and the proposed-never-written promotion rule.
- Project MCP declarations for `context7`, `github` and `atlassian` in `.mcp.json` (no credentials; Claude asks once per project), `doctor` reporting of tool presence and MCP authentication state, and `doctor --install` for missing optional tools (`graphify`, `codegraph`, `gh`).
- Concrete artifact-aware handoff to existing local reviewers, with prepared/partial/returned status and honest context coverage.
- Review → fix → re-review, with local findings by default.
- A worked local scenario and honest evidence of what was exercised.
- Complete standalone resource export to a new directory, and `install`/`sync` into an existing repository — report first, never overwriting, never touching the repository-owned instruction and settings files, never committing; the engineer reviews and commits the result. Company rollout remains separate.
- The requested 37-skill ECC library, with pinned provenance, retained licensing, task-scoped adaptations and the inactive ECC MCP catalog kept as a reference snapshot (the live configuration is `.mcp.json`). Importing operational guidance does not activate the deferred services below.

## Deferred

- Evaluation runner and real-task evaluation corpus.
- Configuration-regression gates.
- Approval-boundary enforcement, approval services and managed-control rollout. The four bundled hooks are loop guardrails, not that framework.
- Unattended stage transitions and artifact-triggered jobs. The `/lbvs-aidlc` gates stay in the engineer's session: they are either answered by the engineer or auto-advanced under a policy the engineer stated in that conversation, announced and interruptible; "proceed" is never inferred, never assumed from an unstated policy, and never applied to review or to commit, push, merge, publication or deployment.
- Delivery execution, with **CircleCI** through the `app-delivery-kit` orb as the intended later CI/CD platform: running pipelines, promoting images and approving environment holds. `/lbvs-aidlc-ship` stops at the open PR; `docs/platform/` only records what exists.
- Maintenance automation: operational monitoring, scheduled hosted security scans and incident-channel integrations that would write into `docs/incidents/` and `docs/security/` without an engineer. The stores and the manual offers exist now; the feeds do not.
- Company-specific rollout and training. Marketplace-plugin distribution (the committed `plugins/` tree, [docs/REFERENCE.md#distribution](docs/REFERENCE.md#distribution)) and the Kiro-derived spec additions are adopted, not deferred.

Deferral does not remove existing repository protections or permit an agent to approve, merge, publish or deploy without the user's instruction.

## Current definition of done

1. The workflow, templates, orchestrator and skills agree on inputs, outputs, gates and handoffs.
2. An engineer can draft and refine artifacts using normal conversation decisions, without enforced external approval machinery.
3. The review approach reuses a documented existing capability and preserves spec/plan context.
4. Local scenarios demonstrate the changed workflow and ordinary verification; unexercised capabilities are explicitly identified.
5. Deferred work is recorded separately and is not demanded before local work can proceed.

Completion of this scope is not a claim that the complete six-stage operational playbook is deployed. See [implementation steps](IMPLEMENTATION_PLAN.md), [future work](FUTURE_WORK.md), [source coverage](docs/COVERAGE.md), and [verification](docs/VERIFICATION.md).
