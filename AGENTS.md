# lbvs-aidlc

Company AIDLC package: an engineer-led workflow from Anthropic's AI-native SDLC playbook, exported as a repository template. Artifacts live in `changes/<change-id>/` (`intent.md`, `spec.md`, `plan.md`, `evidence.md`, `review.md`). Contract: docs/WORKFLOW.md. Recipes: docs/USAGE.md. Scope: GOALS.md. Deferred work: FUTURE_WORK.md.

## Commands

- `python3 scripts/aidlc.py check` — required assets, local links and skill frontmatter. Package integrity only, not lifecycle verification.
- `python3 scripts/aidlc.py mode` — prints `AIDLC project mode: greenfield|brownfield`; `.aidlc/mode` overrides the heuristic.
- `python3 scripts/aidlc.py new <change-id>` — creates only `changes/<change-id>/intent.md`; never overwrites.
- `python3 scripts/aidlc.py doctor` — local prerequisites; external services are not checked.
- `python3 scripts/aidlc.py package <new-dir>` — exports the standalone template; never overlays an existing repository or installs plugins.

## Layout

- `.claude/skills/aidlc/` — `/aidlc <change-id>` orchestrator. Stages: intent → design → plan → build → verify → review, each ending with an explicit confirmation gate.
- `.claude/skills/aidlc-*/` — stage skills plus `aidlc-fix` (bug evidence loop), `aidlc-onboard` (brownfield conventions), `aidlc-learn` (one durable lesson). Manual-only utilities: `aidlc-handoff`, `aidlc-resume`, `aidlc-ideate`.
- `.claude/skills/<other>/` — optional ECC pattern library, pinned in docs/vendor/ecc/manifest.json. Reference material; it does not own artifacts or grant permissions.
- `.claude/agents/` — `aidlc-verifier` (fresh-context checks, no fixes), `aidlc-repo-scout` (read-only conventions report).
- `.claude/settings.json` + `.claude/hooks/` — SessionStart: `check-package.sh`, `project-mode.sh`; PreToolUse: `protect-tests.sh` denies edits to paths listed in `.aidlc/fix/*.json`.
- `REVIEW.md` — review policy. `docs/PLUGINS.md` — bundled Claude Code skills and official plugins to use per stage. `scripts/aidlc.py` — standard-library helper with no approval, network-write or deployment powers.

## Working rules

- Start every change or bug fix with `/aidlc <change-id>` on a dedicated branch/worktree `aidlc/<change-id>`. IDs match `^[a-z0-9]+(-[a-z0-9]+)*$`.
- A stage advances only when the engineer confirms at its gate. Never invent decisions, approvals, stakeholders, metrics, test results or deployment evidence.
- After writing an artifact, Read the saved file back before reporting completion.
- Plan mode returns proposals; `aidlc-build` saves the confirmed plan to `changes/<change-id>/plan.md` before touching code. Native plan scratch is not the canonical plan.
- Bug fixes: reproduce, commit the failing test (asked in-flow), keep it protected while fixing, record `changes/<change-id>/evidence.md` with real Jira/PR references, then offer `/aidlc-learn`.
- No commits, pushes, new remotes, global settings changes, bypass-permissions flags or deployments without explicit authorisation in the conversation.
- Compound Engineering is an optional, explicitly selected plugin (non-technical entry via `ce-brainstorm`); caveman is per-engineer opt-in. This package installs neither.
- Read `.compound-engineering/config.yaml` for `docs_root` before touching `solutions/` or `ideation/` stores; never probe the defaults speculatively.
- Report actual commands, results and limits. Keep this file short; add a rule only when a verified mistake recurs.

## Things Claude gets wrong here

- Importing a remembered summary of an ideation or plan instead of reading the saved file.
- Probing `docs/solutions` before reading the CE config root.
- Treating a write acknowledgement, handoff snapshot or review verdict as read-back or approval.
