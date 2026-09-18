---
name: terminal-ops
description: Evidence-first repo execution workflow for ECC. Use when the user wants a command run, a repo checked, a CI failure debugged, or a narrow fix pushed with exact proof of what was executed and verified.
metadata:
  origin: ECC
disable-model-invocation: true
---

**AIDLC integration:** See [optional ECC skill library](../../../docs/USAGE.md#12-use-the-optional-ecc-skill-library). Existing project conventions and canonical AIDLC artifacts prevail. Skill use is not authority for installs, commits, remote writes, deployment or global/session changes. Invoke manually. Select the repository and inspect/fix/verify/push mode; command execution, installs, commits and pushes stay within separately authorized scope.

# Terminal Ops

Use this when the user wants real repo execution: run commands, inspect git state, debug CI or builds, make a narrow fix, and report exactly what changed and what was verified.

This skill is intentionally narrower than general coding guidance. It is an operator workflow for evidence-first terminal execution.

## Skill Stack

These are optional companion references, not an instruction to invoke additional workflows or assume their commands exist. Discover whether an installed skill is available and appropriate before selecting it:

- [upstream verification-loop](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/verification-loop/SKILL.md) (optional upstream reference) for exact proving steps after changes
- [upstream tdd-workflow](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/tdd-workflow/SKILL.md) (optional upstream reference) when the right fix needs regression coverage
- [upstream security-review](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/security-review/SKILL.md) (optional upstream reference) when secrets, auth, or external inputs are involved
- [github-ops](../github-ops/SKILL.md) (optional manual companion) when the task depends on CI runs, PR state, or release status
- [upstream knowledge-ops](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/knowledge-ops/SKILL.md) (optional upstream reference) when the verified outcome needs to be captured into durable project context

## When to Use

- user says "fix", "debug", "run this", "check the repo", or "push it"
- the task depends on command output, git state, test results, or a verified local fix
- the answer must distinguish changed locally, verified locally, committed, and pushed

## Guardrails

- discover available terminal/process tools and actual repo scripts before executing; if missing, stop with the specific unavailable capability rather than inventing a command or installing tools
- inspect commands for local writes, secrets, network calls and deployment hooks; authorization to inspect is not authorization to fix, install, commit, push or trigger remote workflows
- never bypass permission prompts or change global/session settings; stop only task-owned processes and save evidence only to an authorized project-local artifact
- existing AIDLC verification artifacts remain canonical; do not substitute upstream skill outcomes for project gates

- inspect before editing
- stay read-only if the user asked for audit/review only
- prefer repo-local scripts and helpers over improvised ad hoc wrappers
- do not claim fixed until the proving command was rerun
- do not claim pushed unless the branch actually moved upstream

## Workflow

### 1. Resolve the working surface

Settle:

- exact repo path
- branch
- local diff state
- requested mode:
  - inspect
  - fix
  - verify
  - push

### 2. Read the failing surface first

Before changing anything:

- inspect the error
- inspect the file or test
- inspect git state
- use any already-supplied logs or context before re-reading blindly

### 3. Keep the fix narrow

Solve one dominant failure at a time:

- use the smallest useful proving command first
- only escalate to a bigger build/test pass after the local failure is addressed
- if a command keeps failing with the same signature, stop broad retries and narrow scope

### 4. Report exact execution state

Use exact status words:

- inspected
- changed locally
- verified locally
- committed
- pushed
- blocked

## Output Format

```text
SURFACE
- repo
- branch
- requested mode

EVIDENCE
- failing command / diff / test

ACTION
- what changed

STATUS
- inspected / changed locally / verified locally / committed / pushed / blocked
```

## Pitfalls

- do not work from stale memory when the live repo state can be read
- do not widen a narrow fix into repo-wide churn
- do not use destructive git commands
- do not ignore unrelated local work

## Verification

- the response names the proving command or test
- git-related work names the repo path and branch
- any push claim includes the target branch and exact result
