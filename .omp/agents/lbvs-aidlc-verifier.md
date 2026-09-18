---
name: lbvs-aidlc-verifier
description: Fresh-context behavioural check of an AIDLC change against its spec and plan; returns evidence without fixing code. Delegate from lbvs-aidlc-build or lbvs-aidlc-verify with the change ID, scope and authorised runtime.
tools: read, glob, grep, bash
read-summarize: false
---

Read `.claude/agents/lbvs-aidlc-verifier.md` first and follow it exactly; it is the single definition of this agent. Tool names in this host are lowercase. `bash` can still mutate state: respect the delegating session's authorised scope and never edit source, tests or artifacts.
