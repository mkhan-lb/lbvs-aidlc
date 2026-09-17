# lbvs-aidlc

Company AIDLC package: an engineer-led workflow from Anthropic's AI-native SDLC playbook, exported as a repository template. Artifacts live in `changes/<change-id>/` (`intent.md`, `spike.md`, `spec.md`, `plan.md`, `evidence.md`, `review.md`); knowledge records in `docs/adr/`, `docs/incidents/`, `docs/security/`, `docs/references/`, `docs/solutions/`; platform pointers in `docs/platform/`. Contract: docs/WORKFLOW.md. Recipes: docs/USAGE.md. Scope: GOALS.md. Deferred work: FUTURE_WORK.md.

## Commands

- `python3 scripts/aidlc.py check` — required assets, local links and skill frontmatter. Package integrity only, not lifecycle verification.
- `python3 scripts/aidlc.py status` — every `changes/<id>/` with the stage artifacts present, the stage reached and the next one; marks the current change.
- `python3 scripts/aidlc.py current` — the change ID in play, resolved from the branch, `.aidlc/current` or the only change without `review.md`; exit 1 when nothing resolves.
- `python3 scripts/aidlc.py mode` — prints `AIDLC project mode: greenfield|brownfield`; `.aidlc/mode` overrides the heuristic.
- `python3 scripts/aidlc.py new <change-id>` — creates only `changes/<change-id>/intent.md`; never overwrites.
- `python3 scripts/aidlc.py doctor` — local prerequisites, optional tools (`graphify`, `codegraph`, `gh`, `omp`) and the auth each `.mcp.json` server needs; `--install` runs the `uv`/`pipx`, `npm` or `brew` installer for missing optional tools only. Connectivity and external services are not checked.
- `python3 scripts/aidlc.py package <new-dir>` — exports the standalone template; never overlays an existing repository or installs plugins.
- `python3 scripts/aidlc.py conventions` — compares the repository with `templates/conventions/` defaults (`.editorconfig`, `.pre-commit-config.yaml`, `ruff.toml`, `biome.json`, `CONVENTIONS.md`); `--apply` copies only the missing ones, never overwrites. Greenfield adopts; brownfield keeps its own.
- `python3 scripts/aidlc.py worktree` — the `WorktreeCreate` hook entrypoint; reads the requested name on stdin and prints the worktree path. Not for direct use.

- `.claude/skills/aidlc/` — the `/aidlc` orchestrator; it resolves the change, proposes the worktree, reads the project mode, asks Feature/change · Bug fix · Spike/investigation and runs the stages.
- `.claude/skills/aidlc-*/` — stage skills plus `aidlc-ticket` (Jira/GitHub intake → confirmed ID + seeded intent, read-only), `aidlc-spike` (time-boxed investigation → `spike.md`, never implements), `aidlc-fix` (bug evidence loop), `aidlc-onboard` (brownfield conventions), `aidlc-learn` (one durable lesson), `aidlc-ship` (clean review pass → commit, push `aidlc/<id>`, PR from `templates/pr-body.md`; asks exactly Commit, push and open PR · Commit only · Stop here; never merges). Manual-only utilities: `aidlc-handoff`, `aidlc-resume`, `aidlc-ideate`. 16 `aidlc*` commands.
- `.claude/skills/architecture-decision-records/`, `.claude/skills/doc-coauthoring/` — imported (ECC pin; anthropics/skills `34040c9c`), upstream text plus one AIDLC integration paragraph; the first writes `docs/adr/` after confirmation, the second drafts and saves nothing itself.
- `.claude/skills/<other>/` — optional ECC pattern library, pinned in docs/vendor/ecc/manifest.json (anthropics import in docs/vendor/anthropic-skills/). Reference material; it does not own artifacts or grant permissions.
- `docs/adr/`, `docs/incidents/`, `docs/security/`, `docs/references/` — knowledge stores: `README.md` index + template/log each (`template.md`, `template.md`, `threat-model-template.md`, `libraries.md`). Written only after AskUserQuestion confirmation and a Read-back; offered by design (ADR, threat model), spike (ADR), fix (incident, security finding); design/plan/build/fix add a `libraries.md` row when a Context7 lookup settled a real question; review flags an architectural change without an ADR as a finding.
- `docs/platform/` — pointer layer, not a copy: `README.md` names `Logicbroker/app-template` and the `lb-pipelines/app-delivery-kit-vs@1` orb (internal repos: authenticated `gh api`); `platform.md` holds this repository's facts, read by design and plan. `templates/conventions/` — defaults for `conventions --apply`.
- `.mcp.json` — `context7` (anonymous or `CONTEXT7_API_KEY` = `Bearer <key>`), `github` (`GITHUB_PERSONAL_ACCESS_TOKEN`), `atlassian` (OAuth via `/mcp`); no credentials in the file. `mcp-configs/` is an inactive upstream snapshot.
- `.claude/agents/` — `aidlc-verifier` (fresh-context checks, no fixes), `aidlc-repo-scout` (read-only conventions report), `aidlc-design-reviewer` (read-only READY / NOT READY on spec/plan before the design gate; a summary input, never approval), `aidlc-threat-modeler` (read-only STRIDE table when a threat-model offer is accepted). `.omp/agents/` mirrors all four.
- `.claude/settings.json` + `.claude/hooks/` — SessionStart: `check-package.sh`, `project-mode.sh`; PreToolUse: `protect-tests.sh` denies edits to paths listed in `.aidlc/fix/*.json`; WorktreeCreate: `worktree-create.sh` names worktrees `aidlc/<change-id>` instead of Claude Code's default.

## Working rules

- Start a change or bug fix with `/aidlc` — it resolves the ID (argument → branch → `.aidlc/current` → the only open change → asks) and proposes the worktree `aidlc/<change-id>`. IDs match `^[a-z0-9]+(-[a-z0-9]+)*$`; prefix the ticket key when there is one, e.g. `vs-1234-order-export`.
- Stages stop at a gate by default. When the engineer selects an auto-advance flow policy, a stage may continue only after saving and reading back its artifact with no open questions, no failed or missing required check and no pending CE review; review always asks, and implementation waits for the policy that includes build.
- After writing an artifact, Read the saved file back before reporting completion.
- Plan mode returns proposals; `aidlc-build` saves the confirmed plan to `changes/<change-id>/plan.md` before touching code. Native plan scratch is not the canonical plan.
- Bug fixes: reproduce, commit the failing test (asked in-flow), keep it protected while fixing, record `changes/<change-id>/evidence.md` with real Jira/PR references, then offer `/aidlc-learn`.
- No commits, pushes, new remotes, global settings changes, bypass-permissions flags or deployments without explicit authorisation in the conversation.
- Compound Engineering 3.26.3 is declared at project scope in `.claude/settings.json` (`extraKnownMarketplaces` + `enabledPlugins`); it installs after workspace trust and is still used only when explicitly selected (non-technical entry via `ce-brainstorm`). Caveman is per-engineer opt-in and not declared.
- Read `.compound-engineering/config.yaml` for `docs_root` before touching `solutions/` or `ideation/` stores; never probe the defaults speculatively.
- Report actual commands, results and limits. Keep this file short; add a rule only when a verified mistake recurs.

## Things Claude gets wrong here

- Importing a remembered summary of an ideation or plan instead of reading the saved file.
- Probing `docs/solutions` before reading the CE config root.
- Treating a write acknowledgement, handoff snapshot or review verdict as read-back or approval.
