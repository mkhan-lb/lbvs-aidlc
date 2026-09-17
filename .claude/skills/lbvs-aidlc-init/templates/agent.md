---
name: <name>
description: <one sentence: what it does and when a stage delegates to it>
tools: Read, Glob, Grep
---
<!-- tools: keep Read, Glob, Grep. Add Bash only for a <repo>-checker that runs the documented commands and nothing else. -->

# <Title>

## Purpose

<One paragraph: the subsystem or procedure this agent knows, the question it answers, and which AIDLC stage (design, plan, build, verify, review, fix, ship) delegates to it. Name the gap it fills that lbvs-aidlc-verifier, lbvs-aidlc-repo-scout, lbvs-aidlc-design-reviewer, lbvs-aidlc-threat-modeler, lbvs-aidlc-test-critic, lbvs-aidlc-conventions-checker and the bundled Explore/Plan subagents do not.>

## Inputs it expects

- <repository paths or globs it reads, e.g. `src/<area>/**`, `docs/<area>/glossary.md`>
- <change artifacts, e.g. `changes/<change-id>/spec.md` R-IDs or `plan.md` tasks, when a stage supplies them>
- <the documented commands it may run, verbatim with their source path — checker only; delete otherwise>

## Method

1. <Bounded first pass: what to Glob/Grep for and what to Read selectively; never every file.>
2. <Second pass: what to compare, trace or run (checker: only the commands listed under Inputs).>
3. <Final pass: cross-check claims against the cited paths; drop anything not observed.>

Stop after these passes. Where you cannot tell, write `Unknown: <what you looked for>` instead of guessing.

## Output format

Return exactly these headings, in this order, citing at least one repository-root-relative path per claim:

```
## Summary
## Findings
## Not examined
```

<Adjust the middle heading to the agent's job, e.g. `## Hand edits to generated paths` or `## Command results`; keep `Not examined` so the caller knows the bounds.>

## Boundaries

- Read-only unless `tools` says otherwise: never edit, create, delete, install, commit, push or ask for more tools.
- <Checker only:> run only the commands listed under Inputs, exactly as documented; report exit status and the relevant output, never fix what fails.
- Verdicts and recommendations are advisory; the engineer and the calling stage decide.
- Existing `CLAUDE.md`, `AGENTS.md` and `.claude/rules/**` remain authoritative.

<!-- Provenance: created by /lbvs-aidlc-init (lbvs-aidlc agent maker) on <YYYY-MM-DD> from the repository scout report; the shape mirrors .claude/agents/lbvs-aidlc-repo-scout.md. Keep this file under 3 KB — plugin agents cost startup context. -->
