---
name: lbvs-aidlc-conventions-checker
description: Advisory pre-PR check of a change against the repository profile — documented lint/format/test commands run verbatim, diff vs conventions, delivery hygiene, glossary drift. Delegate from lbvs-aidlc-ship.
tools: read, glob, grep, bash
read-summarize: false
---

Read `.claude/agents/lbvs-aidlc-conventions-checker.md` first and follow it exactly; it is the single definition of this agent. Tool names in this host are lowercase. `bash` can still mutate state: respect the delegating session's authorised scope and never edit source, tests or artifacts.
