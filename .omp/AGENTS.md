@../AGENTS.md

## Oh My Pi

- Skills, agents and hooks under `.claude/` are discovered by omp's `claude` provider; invoke the orchestrator as `/skill:aidlc <change-id>` and read any skill with `skill://<name>`.
- Sticky hard rules live in `.omp/RULES.md`; do not restate them elsewhere.
- Use the `task` tool with `aidlc-repo-scout`/`aidlc-verifier` prompts for read-only scouting and fresh-context verification.
