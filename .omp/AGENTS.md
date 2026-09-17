@../AGENTS.md

## Oh My Pi

- Skills under `.claude/skills/` are discovered by omp's `claude` provider: `/skill:aidlc [change-id]` starts a change; read any skill with `skill://<name>`. Manual-only skills are hidden from the list but still run via `/skill:<name>`.
- Task agents come from `.omp/agents/` (`aidlc-verifier`, `aidlc-repo-scout`); each defers to its `.claude/agents/` definition. omp does not read `.claude/agents/` directly.
- `.omp/hooks/pre/aidlc-guards.ts` replaces the Claude shell hooks here: it injects the `AIDLC project mode:` line on the first turn and blocks `edit`/`write` on tests listed in `.aidlc/fix/*.json`. omp has no `WorktreeCreate` equivalent, so create worktrees with `git worktree add ../<repo>-<change-id> -b aidlc/<change-id>`.
- Sticky hard rules live in `.omp/RULES.md`; do not restate them elsewhere.
