# Workflow-first implementation plan

Status: rescaled by explicit user direction on 16 September 2026, then extended the same day into the company AIDLC restructure below. The earlier full-playbook checklist is superseded.

## Scope decision

Build the engineer workflow and artifact handoffs now, together with the plain-Markdown knowledge stores (`docs/adr/`, `docs/incidents/`, `docs/security/`, `docs/solutions/`) that the workflow writes into on confirmation. Research and reuse an existing review capability. Defer evaluation runners, configuration-regression gates, approval enforcement, delivery (**CircleCI later**) and maintenance automation — hosted scans, monitoring and incident-channel integration. Normal code tests, human judgement and existing repository safeguards remain.

The original source map, compatibility research and prior verification are retained as reference. Their external-service requirements are not blockers for the current work.

## Step 1 — Align the workflow and artifacts

**Goal:** make the process usable without approval or operational infrastructure.

- [x] Document intent → spec → plan → implementation/verification → review → fix/re-review.
- [x] Define the useful input/output and next engineer action at each activity.
- [x] Simplify templates and skills to use ordinary conversation decisions; remove enforced external approval/identity/revision prerequisites.
- [x] Keep artifacts together and update them when scope, requirements or approach change.
- [x] Keep source, current scope and deferred capability clearly distinguished across repository guidance.

**Complete when:** the guide, templates, skills and prerequisites tell the same story and do not require CI, an evaluation corpus, approval services or a reference company repository to begin.

## Step 2 — Select a reusable review path

**Goal:** use existing review tools instead of implementing another review engine.

- [x] Inspect current Claude Code built-in and first-party review options, including actual command/prompt behavior.
- [x] Inspect Oh My Pi's built-in review and repository-maintainer review commands separately.
- [x] Record local-versus-PR scope, required access, side effects, licence/reuse constraints and sourced invocation details.
- [x] Recommend the smallest manual-first route; distinguish a recommendation from installation or verified runtime integration.
- [x] Keep the AIDLC review wrapper focused on supplying intent/spec/plan, collecting findings and routing fixes.

**Complete when:** an engineer knows which existing reviewer to use and what it will do, without needing CI or a hosted review service. Nothing is installed, published or merged implicitly.

## Step 3 — Initial local checks (historical)

**Goal:** prove the changed behavior rather than infer it from written prompts.

- [x] Run package checks after the scope update.
- [x] Exercise an artifact-to-next-step scenario without an external approval record and confirm the skill can work from real task context.
- [x] Confirm normal verification remains in the workflow while evaluation infrastructure and enforcement remain out of scope.
- [x] Record exactly which skills/scenarios ran and which reviewer integrations were only researched.

**Complete when:** the executed scenario, actual outputs and remaining limitations are recorded. A local scenario is not presented as a live PR integration or production lifecycle demonstration.

Broader behavioral workflow verification remains deferred by the user. The historical checks above do not require another end-to-end example. The explicitly requested optional CE integration trials below are focused exceptions, not a reopened evaluation workstream.

## Completed prerequisite — Claude-native file structure

The package now follows the official Claude directory conventions. Completed layout changes:

- Keep root `CLAUDE.md` and `.claude/agents/`; both already use documented locations.
- Bundle active templates with their owning `.claude/skills/<name>/SKILL.md` files and reviewer references with the review skill.
- Retain shared project documentation and `changes/<id>/` artifacts outside Claude's runtime/configuration directories.
- Keep the incident template as a template rather than inventing an active maintenance skill (it sat in a deferred-templates folder until the knowledge-store pass below made it `docs/incidents/template.md`).
- Update every current reference, helper resource path and personal-state ignore rule. Retain historical source/evidence as recorded.
- Checked layout, links and helper resource loading only. That restructuring did not run another model-driven workflow or add empty settings, hooks, rules or dynamic workflow scripts.

Plan-to-build persistence, durable entry/resume, learning, ideation, existing-reviewer handoff and standalone export are now integrated below. No new evaluation, approval, delivery or maintenance infrastructure is implied.

## Completed trial — optional CE brainstorming

The engineer selected option 1: keep AIDLC artifacts, invoke the optional upstream CE skill, and consume its discovery output rather than copying prompts. Repository onboarding is the rollout target; no organization enforcement is configured.

- [x] Add explicit opt-in CE discovery to `aidlc-intent` while preserving ordinary plugin-independent clarification.
- [x] Use CE's in-session `mode:return-to-caller` contract, preserve blockers and prior decisions, read a returned document before import, and retain AIDLC artifact authority.
- [x] Exercise the real pinned CE plugin in disposable native Claude sessions: document return, brief return, installed-but-not-selected, no-plugin baseline and selected-but-unavailable.
- [x] Keep code, spec/implementation-plan creation, CE autonomous shipping and persistent plugin settings outside the trial.

The first artifact run exposed an import-from-conversation shortcut; the caller continuation was strengthened and the rerun read the saved CE document before merging. [Verification](docs/VERIFICATION.md#optional-ce-brainstorming-trial) records the exact coverage and limitations. This is not an interactive brainstorming-quality evaluation or proof of every error branch.

Document review, durable continuity, ideation and one-off learning are integrated separately below. The six AIDLC stages and deferred operational scope remain unchanged; ideation, learning, handoff and resume are four manual utilities, not new stages.

## Completed integration — optional CE document review

- [x] Add explicit CE document-review selection to `aidlc-design` and `aidlc-plan`, sharing one caller contract in the workflow guide.
- [x] Invoke the real upstream `ce-doc-review` in non-interactive mode against the exact saved same-change artifact; no copied reviewer prompts or custom orchestrator.
- [x] Require report-only, current-provider/native review; keep proposed corrections separate from edit permission and preserve genuinely unresolved choices.
- [x] Preserve ordinary design/planning without CE; stop on unavailable capability or missing targets rather than silently substituting.
- [x] Defer review of an unsaved proposal until an authorised save instead of reviewing stale or native scratch content.
- [x] Exercise eight bounded native scenarios, including saved spec/plan reviews, sensitive-data review, skipped/absent CE, unavailable selection, missing target and an unsaved revised plan.

The first spec-review handoff reopened a requirement already settled in intent. The caller continuation was corrected; the rerun recommended the entailed design fix without reopening that requirement. Native plan mode also exposed its host-managed scratch-file exception, now distinguished from canonical AIDLC artifact saves. [Verification](docs/VERIFICATION.md#optional-ce-document-review-trial) records observed findings, unchanged project artifacts, native tool errors and limits. No persistent CE installation or new enforcement system was added.

Plan-to-build persistence, durable continuity, ideation, learning capture and standalone repository packaging are integrated separately below; they are not implied by document review.

## Completed integration — usage and durable continuity

- [x] Add practical [usage recipes](docs/USAGE.md) for ordinary work, optional CE, proposal saving, pausing, resuming and missing/stale inputs.
- [x] Give `aidlc-build` explicit canonical-save ownership: an exact confirmed proposal, save-only or save-and-implement direction, post-write readback, newer-decision protection and pending-review preservation.
- [x] Add manual `aidlc-handoff` and `aidlc-resume` utilities while retaining the six lifecycle stages and existing canonical artifacts.
- [x] Store immutable supporting snapshots under the selected change; ordinary creation/resume needs no CE installation.
- [x] Integrate actual optional upstream `ce-handoff` creation at an exact repository destination and fresh-session resume from an explicitly selected source.
- [x] Keep resume orientation-only: filename-only candidate selection, current-state comparison, untrusted historical content, no command execution or writes, and a stop for current-user direction.
- [x] Exercise fourteen bounded native scenarios, including actual save-and-build execution, both snapshot creators, fresh CE/ordinary resumes, drift, hostile snapshot instructions and unavailable/read-only/collision paths.

Initial runs exposed skipped post-write reads and discovery that inspected unselected bodies or issued shell commands. The affected contracts were tightened and rerun. [Continuity verification](docs/VERIFICATION.md#durable-continuity-and-plan-persistence-trial) records the observed results and native-mode limitations. These are focused local trials, not a new evaluation runner, security boundary, approval ledger or production lifecycle demonstration.

## Completed integration — learning, ideation, reviewers and export

- [x] Add ordinary one-off learning capture from proven, non-obvious work, with qualification, duplicate handling, configured-root selection and actual persisted readback.
- [x] Offer explicitly selected real CE lightweight capture, including its mandatory update-only maintenance of an existing local glossary; no rules/global-memory bootstrap or automatic next workflow.
- [x] Add ordinary and optional real CE repository-grounded ideation before a change is selected, with ranked ideas, evidence limits, rejection reasons and manual selection.
- [x] Import only the engineer-selected saved idea into ordinary intent, retaining provenance and unresolved choices while checking claims against current source/data.
- [x] Supply complete artifact/policy context to an actually available existing reviewer, or return a filled-in handoff labelled prepared—not run. Preserve native findings, execution/coverage/freshness and stable IDs during authorised report saving.
- [x] Add a standalone `package` export to a nonexistent destination, following declared/local resource links without overlaying existing repository instructions or copying runtime stores.
- [x] Extend practical usage recipes and shared guidance without introducing a new lifecycle stage, installer, review engine, evaluation runner or approval service.

Focused native/CLI trials and their limitations are recorded in [verification](docs/VERIFICATION.md). These include genuine upstream calls and an actual existing reviewer-agent invocation, not an assertion that user-only review menus, every re-review branch or production adoption have been exercised.

## Completed integration — selected ECC skill library

- [x] Import all 37 requested canonical ECC skills at commit `8321021c54d670126ce3b2969d5deb880b4b0c2a`, resolving the smaller `.agents/skills` mirror and `frontend-design-direction` naming.
- [x] Retain full selected guidance, eleven supporting resources/notices, ECC licensing and per-file source/import hashes in the [manifest](docs/vendor/ecc/manifest.json).
- [x] Keep 26 reference skills discoverable and eleven operational skills explicitly invoked; remove active permission/runtime coupling and preserve AIDLC/project authority.
- [x] Retain the 34-server MCP catalog as an inactive example, identify deprecated/optional dependencies and document selective adoption in the [usage guide](docs/USAGE.md#12-use-the-optional-ecc-skill-library).
- [x] Include the complete declared library in package checks/export without copying ECC active settings, runtime stores or the ECC platform.
- [x] Exercise native API-design/manual-canary prompts, resource/export boundaries and corrected example defects; record exact results and limits in [verification](docs/VERIFICATION.md#selected-ecc-skill-import).

This adds optional skills, not an evaluation service, monitoring system, installer, permission framework or company rollout. Additional skill candidates are recommendations only.

## Completed integration — minimal project setup and shared instructions

- Add shared `.claude/settings.json` with the official schema and only a `SessionStart` startup/resume hook, a 10-second timeout and `sh "${CLAUDE_PROJECT_DIR}/.claude/hooks/check-package.sh"`.
- Keep the hook read-only: `set -eu`, require `CLAUDE_PROJECT_DIR`, and execute the Python helper's `check`. This is package integrity, not per-edit/turn checks, lifecycle verification, approval or security enforcement.
- Supply `.mcp.json` as `{"mcpServers":{}}` and create ignored `.claude/settings.local.json` as `{}` here (historical; the MCP map now declares `context7`, `github` and `atlassian` — see **Project MCP** below). No tool grants, model/provider selection or telemetry are added; inherited user/managed configuration can still apply.
- Add narrowly path-scoped `.claude/rules/package-maintenance.md`, linked from root instructions for explicit consultation by other hosts.
- Share root instructions through the exact relative symlink `AGENTS.md -> CLAUDE.md` (historical; superseded by the canonical `AGENTS.md` + `@AGENTS.md` import in the restructure below).
- Explicitly package shared settings/hook/rule and the MCP map; exclude local settings and arbitrary credentials/configs. Export does not mutate existing repository/global settings; adoption remains a reviewed merge.
- Keep this native AIDLC setup separate from the pinned ECC guidance import. No `.agents/skills` mirror, native Codex skill/hook parity or proven Codex compatibility is claimed.

Fifteen disposable boundary cases, native Claude startup-hook execution and native Codex instruction discovery passed. [Verification](docs/VERIFICATION.md#minimal-project-configuration-and-shared-instructions) records commands, results and limits; resume, isolated conditional rule triggering and full Codex workflow parity were not exercised. Historical import hashes, scope descriptions and executed records remain historical.

## Current implementation — company AIDLC restructure

Repository to be published as `lbvs-aidlc`. Contract for this pass; completion is recorded in [verification](docs/VERIFICATION.md), not here.

- **Orchestrator.** `/aidlc [change-id]` starts or continues a change: it resolves the change ID, states the run's flow policy, proposes the `aidlc/<change-id>` worktree and asks; reads the project mode; for brownfield without a repository `CLAUDE.md`/conventions record invokes `aidlc-onboard`; then runs intent → design → plan → build → verify → review. Every stage ends with a summary and either an AskUserQuestion gate (**Proceed to \<next stage\>** / **Revise this stage** / **Stop here**) or an announced auto-advance permitted by the stated policy; only those two routes invoke the next skill via the Skill tool. After review: **Fix findings (build)** / **Capture lesson (aidlc-learn)** / **Done**.
- **Skill invocability.** `aidlc`, `aidlc-intent`, `aidlc-design`, `aidlc-plan`, `aidlc-build`, `aidlc-verify`, `aidlc-review`, `aidlc-fix`, `aidlc-onboard`, `aidlc-learn`, `aidlc-ticket`, `aidlc-spike` are model- and user-invocable with a one-sentence outcome `description` and a `when_to_use` trigger line. Only `aidlc-handoff`, `aidlc-resume`, `aidlc-ideate` keep `disable-model-invocation: true`. No AIDLC skill uses `allowed-tools`, `hooks`, `model`, `agent` or `context` frontmatter. The package supplies 15 `aidlc*` commands.
- **Skill size.** Each `SKILL.md` body targets ≤ 5 KB (hard cap 7 KB). Repeated boilerplate preambles are replaced by one line: "Contract: docs/WORKFLOW.md. Paths are repository-root relative; bundled files are relative to this skill directory." Preserved contracts: exact-ID validation `^[a-z0-9]+(-[a-z0-9]+)*$`, post-write Read-back of saved artifacts, no invented approvals/metrics, plan mode returns proposals not saves, no commit/push/deploy without explicit authorisation, optional CE handoffs described by linking to the workflow guide.
- **Fix loop.** `/aidlc-fix <change-id>`: reproduce → failing test → authorised commit `test(<change-id>): reproduce <summary>` → marker `.aidlc/fix/<change-id>.json` `{"change_id", "protected": [...]}` → fix under `protect-tests.sh` (PreToolUse `Edit|Write|MultiEdit|NotebookEdit`, denies edits to protected paths while any marker exists) → test + `/verify` when a runtime exists → `changes/<change-id>/evidence.md` from `.claude/skills/aidlc-fix/templates/evidence.md` → delete marker → offer `/aidlc-learn`. `.aidlc/fix/` is gitignored.
- **Onboarding.** `.claude/agents/aidlc-repo-scout.md` is read-only (`Read, Glob, Grep`) and returns a structured conventions report. `/aidlc-onboard` delegates to it, asks Modernize / Stay legacy / Decide later, routes legacy to `inherit-legacy-style` and modernize to a `code-modernization` recommendation, proposes a ≤60-line repository `CLAUDE.md` with "Things Claude gets wrong here" and path-scoped `.claude/rules/` drafts (recommending `/init` with `CLAUDE_CODE_NEW_INIT=1` as the alternative), and writes them plus `.aidlc/mode` and `docs/onboarding.md` only on explicit confirmation.
- **Project mode.** `python3 scripts/aidlc.py mode` prints one line `AIDLC project mode: greenfield|brownfield — <reasons>`; `.aidlc/mode` overrides. `project-mode.sh` (SessionStart) injects it.
- **Shared instructions.** `AGENTS.md` is canonical; `CLAUDE.md` = `@AGENTS.md` + Claude-specific section; `.omp/AGENTS.md` imports `@../AGENTS.md`. The symlink and its export exception are removed. `.worktreeinclude` copies `.env` and `.claude/settings.local.json` into worktrees.
- **Worktree naming.** A `WorktreeCreate` hook (`.claude/hooks/worktree-create.sh` → `python3 scripts/aidlc.py worktree`) replaces Claude Code's default naming. `EnterWorktree` with the name `aidlc/<change-id>` yields the directory `.claude/worktrees/aidlc+<change-id>` on branch exactly `aidlc/<change-id>`, branched from local `HEAD`; a ticket key may prefix the ID (`aidlc/vs-1234-order-export`). Other names keep `worktree-<name>`. Because the hook replaces the default behaviour it performs the `.worktreeinclude` copy itself; an existing worktree directory is reused; a missing or unusable name fails the hook and therefore fails worktree creation. No host-side worktree marker is written, so Claude Code's worktree sweep does not manage these trees and removal is `git worktree remove`.
- **Change-ID resolution.** `python3 scripts/aidlc.py status` lists each `changes/<id>/` with the stage artifacts present, the stage reached, the next stage, the handoff count and a marker on the current change; `python3 scripts/aidlc.py current` prints `<change-id>\t<source>` and exits 1 when nothing resolves. Resolution order: branch name (`aidlc/<id>`, `aidlc+<id>`, `worktree-aidlc/<id>`, `worktree-aidlc+<id>`), then `.aidlc/current` (machine-local, gitignored), then the only change without `review.md`. Every ID-taking skill takes a valid `$ARGUMENTS` first, falls back to `current` and names the source, treats trailing prose as context behind a leading valid token, and otherwise asks — proposing a request-derived slug with a known ticket key as prefix, never inventing one and never creating `changes/<id>/` from an unresolved ID. `aidlc-ideate` keeps its topic ID with no fallback.
- **Flow policy.** The orchestrator states exactly one policy per run: `Flow policy: confirm each stage` (default, and the assumption when none is stated), `Flow policy: auto-advance when clear, stop before build`, or `Flow policy: auto-advance when clear, including build`. Each stage still summarises first. Auto-advance requires all of: an auto policy; the artifact saved and read back this run; no open questions, unresolved decisions or missing inputs; no failed check and no required check "not run"; no pending requested CE review; the next stage is not `aidlc-build` unless the policy includes build; and the next step is not a commit, push, PR, merge, publication or deployment. It then prints `Auto-advancing to <next stage> (policy: <policy>; no open questions, checks: <summary>)`, invokes the next stage with the bare ID and states that the engineer can interrupt. It always asks under confirm-each-stage, at `aidlc-review`, when any condition is unmet, when implementation would start under "stop before build", and when a stage ended read-only or unsaved; `aidlc-fix` always asks its failing-test commit question and its closing gate. No gate is answered for the engineer and no unstated policy is claimed.
- **Helper and export.** Subcommands are `check`, `doctor` (`--install`), `new`, `mode`, `status`, `current`, `worktree` and `package`: `check` validates the skills, agents, hooks, frontmatter rules, both vendor manifests and the knowledge-store indexes/templates; `doctor` reports `python3`/`git`/`claude`, the optional tools `graphify`, `codegraph`, `gh`, `omp`, and for each server in `.mcp.json` its authentication kind and whether the variable is set — `--install` runs the `uv`/`pipx`, `npm` or `brew` installer for each missing optional tool and never installs plugins or changes settings; `package` exports them together with `.worktreeinclude`, `.mcp.json`, the knowledge-store indexes/templates and the vendor manifests; `mode`, `status`, `current` and `worktree` back the project-mode line, ID resolution and the worktree hook. Four hooks are registered (`check-package`, `project-mode`, `protect-tests`, `worktree-create`). Distribution remains repo-template export.
- **Project MCP.** `.mcp.json` declares `context7` (`https://mcp.context7.com/mcp`; anonymous, optional `CONTEXT7_API_KEY` whose value includes `Bearer `), `github` (`https://api.githubcopilot.com/mcp/`; `GITHUB_PERSONAL_ACCESS_TOKEN` required, `gh auth token`) and `atlassian` (`https://mcp.atlassian.com/v2/mcp`; OAuth 2.1 via `/mcp` on first use), with no credentials in the file. Claude prompts once per project before connecting. The ECC catalog under `mcp-configs/` stays a verbatim upstream snapshot with an outdated GitHub entry; `.mcp.json` is the live configuration. `.codegraph/` is gitignored.
- **Ticket intake.** `/aidlc-ticket <TICKET-KEY or issue URL>` fetches the record read-only through whatever is available (Atlassian MCP `getJiraIssue` for Jira keys; `gh issue view` or the github MCP for GitHub issues; otherwise asks for pasted text, never invents content), derives `<key-lowercase>-<slug>` (≤ 40 chars, `^[a-z0-9]+(-[a-z0-9]+)*$`), confirms it, writes `.aidlc/current`, creates `changes/<id>/intent.md` from the intent template with summary, description, acceptance criteria and link in Context and sources, reads it back and offers **Continue with /aidlc (worktree, stages)** / **Stop here**. Never writes back to Jira/GitHub. `/aidlc` given a ticket key points at `/aidlc-ticket`.
- **Spike.** `/aidlc-spike [change-id]` follows the ID-resolution contract; agrees the question, the time box and what "answered" means by AskUserQuestion; investigates read-only (Explore, `aidlc-repo-scout`, graphify when present, docs); writes `changes/<id>/spike.md` from the bundled `templates/spike.md` (Question, Time box, Findings with sources, Options with trade-offs, Recommendation, Open questions, Suggested next step) with Read-back; never implements or changes code; end gate **Create/refresh intent from this spike (aidlc-intent)** / **Record an ADR (architecture-decision-records)** / **Stop here**. Orchestrator Step 2 asks **Feature/change** / **Bug fix** / **Spike/investigation**.
- **Imported skills.** `doc-coauthoring` from anthropics/skills at `34040c9c568585f6929bedeaad110ad08f079624` (`skills/doc-coauthoring/SKILL.md`; the repository has no root LICENSE and the skill no per-skill LICENSE.txt — NOTICE and manifest record only the README's "Many skills in this repo are open source (Apache 2.0)") and `architecture-decision-records` from ECC at the existing pin (`skills/architecture-decision-records/SKILL.md`). Both model-invocable; upstream text kept; one added "AIDLC integration" paragraph after the frontmatter (paths, confirmation-before-write, no invented content, `planner`/`code-reviewer` → `aidlc-plan`/`aidlc-review`); `when_to_use` added only if absent; upstream and imported SHA-256 recorded in `docs/vendor/ecc/manifest.json` and `docs/vendor/anthropic-skills/manifest.json` (same `schema_version: 1` shape).
- **Knowledge stores.** `docs/adr/` (`NNNN-short-title.md`, `README.md` index, `template.md`), `docs/incidents/` (`YYYY-MM-DD-short-title.md`, `README.md`, `template.md`), `docs/security/` (`README.md`, `threat-model-template.md`, `threat-models/<name>.md`, `findings/YYYY-MM-DD-<source>.md`) and `<root>/solutions/` via `aidlc-learn` (template now carries `Status` and `Last verified`). Writing any record requires explicit confirmation (AskUserQuestion) and a Read-back. Knowledge versus rule: a recurring correction becomes a rule in `AGENTS.md`/`.claude/rules/`, not a record. Model adapted from AWS aidlc-workflows' team-knowledge chapter and the sibling Logicbroker `shared-services-aidlc` ADR template shape, in our own words.
- **Stage wiring.** `aidlc-design` offers an ADR (architectural boundary, technology choice or contract) and a threat model (new external interface, data store, credential or trust boundary) by AskUserQuestion, never automatically; `aidlc-review` adds the Compliance check "architectural change without ADR" as a finding, not a blocker; `aidlc-fix` offers `docs/incidents/YYYY-MM-DD-<slug>.md` from the template linked from `evidence.md` when the symptom arrived through an alert/incident link, and a `docs/security/findings/` record for security defects. All SKILL.md files stay ≤ 7 KB.
- **Documentation.** README, WORKFLOW, USAGE, ARTIFACTS, COMPATIBILITY, COVERAGE reflect the above, including the knowledge stores, MCP declarations, `doctor --install`, codegraph positioning against graphify and the ticket/spike recipes; [PLUGINS.md](docs/PLUGINS.md) lists bundled skills and marketplace plugins per stage as recommendations only. Non-technical entry is optional CE brainstorming; caveman is opt-in at user scope; the 37 ECC library skills are untouched.

## Deferred work and historical progress

[Future work](FUTURE_WORK.md) owns the explicitly deferred areas. [Coverage](docs/COVERAGE.md) preserves the full source inventory and [verification](docs/VERIFICATION.md) preserves earlier local checks; neither is a claim that the complete playbook is implemented.

Earlier source mapping, templates, six workflow skills, review guidance, the verifier and the local draft helper are retained and reused. The previous count of 40 blocked full-lifecycle items is no longer the current work queue. Operational prerequisites become relevant only when their deferred area is resumed.
