---
paths:
  - "scripts/aidlc.py"
  - ".claude/**/*"
  - ".omp/**/*"
  - ".mcp.json"
  - "AGENTS.md"
  - "CLAUDE.md"
---
# Package maintenance

- `AGENTS.md` is the canonical shared instruction file; `CLAUDE.md` starts with `@AGENTS.md` and `.omp/AGENTS.md` with `@../AGENTS.md`. Never duplicate the text or reintroduce symlinks; `check` rejects both.
- Declare every new skill, agent, hook, template or shared config in `scripts/aidlc.py` `REQUIRED_ASSETS`/`SKILLS`; export copies only declared and linked resources. Never export `.claude/settings.local.json`, `.aidlc/fix/`, credentials or arbitrary configs.
- Only `lbvs-aidlc-handoff`, `lbvs-aidlc-resume` and `lbvs-aidlc-ideate` carry `disable-model-invocation: true`; every other AIDLC skill is model- and user-invocable with a `when_to_use` line. No skill may set `allowed-tools`, `hooks`, `model`, `agent` or `context`.
- `.claude/agents/<name>.md` is the single definition of a bundled agent: frontmatter `name`, `description` (one sentence, says when to delegate), `tools`; the body is a self-contained system prompt under 3 KB. `.omp/agents/<name>.md` repeats the description verbatim and defers to it.
- Register hooks in `.claude/settings.json`; files in `.claude/hooks/` do not autoload. Hooks stay deterministic and narrow: package check and project mode at startup/resume, worktree naming on `WorktreeCreate`, test protection only while `.aidlc/fix/*.json` exists.
- Require native-runtime evidence for discovery and hook behavior; helper checks are not approval, lifecycle or security guarantees.
