@AGENTS.md

## Claude Code

- `/aidlc <change-id>` orchestrates the stages and asks before each transition. Enter a worktree with the `EnterWorktree` tool (branch `aidlc/<change-id>`) when the checkout is not already dedicated to the change.
- `python3 scripts/aidlc.py mode` runs at session start; when it reports brownfield and no conventions are recorded, run `/aidlc-onboard` before the first change.
- `protect-tests.sh` denies `Edit`/`Write` on reproduction tests listed in `.aidlc/fix/<change-id>.json`. If a protected test is itself wrong, ask the engineer to delete the marker rather than working around the hook.
- Package maintenance guidance is path-scoped in `.claude/rules/package-maintenance.md`. Personal overrides belong in `.claude/settings.local.json`, which is ignored and never exported.
