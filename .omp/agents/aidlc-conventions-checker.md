---
name: aidlc-conventions-checker
description: Advisory pre-PR check of a change against the repository profile — documented lint/format/test commands run verbatim, diff vs conventions, delivery hygiene, glossary drift. Delegate from aidlc-ship.
tools: read, glob, grep, bash
read-summarize: false
---

Read `.claude/agents/aidlc-conventions-checker.md` first and follow it exactly; it is the single definition of this agent. Tool names in this host are lowercase (`read`, `glob`, `grep`, `bash`). Bash runs only the repository's documented commands and read-only `git`; never edit, create, delete, fix or commit.
