---
name: parallel-execution-optimizer
description: Use when the user wants a task done much faster through parallel work, concurrent agents, batched tool calls, isolated worktrees, or many independent verification lanes without losing correctness.
license: MIT
metadata:
  origin: ECC
disable-model-invocation: true
---

**AIDLC integration:** See [optional ECC skill library](../../../docs/USAGE.md#12-use-the-optional-ecc-skill-library). Existing project conventions and canonical AIDLC artifacts prevail. Skill use is not authority for installs, commits, remote writes, deployment or global/session changes. Invoke manually. Select the task, independent lanes and allowed write surfaces; delegation does not expand permissions or authorize worktrees, services, remote changes or deployment.

# Parallel Execution Optimizer

Use this skill when speed comes from doing independent work at the same time:
repo inspection, file reads, API checks, browser checks, build/test lanes,
deploy readbacks, or multi-worktree implementation passes.

## Capability and authority boundary

Discover the host's actual concurrent tool, subagent, process-supervision and worktree capabilities first; names and APIs vary. This skill supplies no orchestrator or worker runtime. If a required capability is unavailable, report that lane blocked or use a user-accepted serial plan; do not invent tool calls, install a runtime, bypass permission prompts or change model/session settings. Carry the same user-authorized scope into every lane and name one integration owner. A read-only request stays read-only in every agent.

## Core Pattern

Turn urgency into a dependency graph before acting.

1. Define the objective and done signal.
2. Split work into lanes.
3. Mark each lane as parallel, sequential, or gated.
4. Run independent reads/checks together.
5. Keep writes isolated by file, worktree, branch, service, or dataset.
6. Merge only after evidence shows the lanes are compatible.
7. End with a verification table, not a vague speed claim.

## Lane Matrix

Before a large push, write a compact matrix:

```text
Lane | Can run in parallel? | Write surface | Risk | Verification
Repo scan | yes | none | low | rg/git status outputs
Backend patch | maybe | src/api | medium | unit tests
Frontend patch | maybe | app/components | medium | browser screenshot
Deploy readback | after build | remote service | high | live URL + logs
```

Only run lanes in parallel when their write surfaces do not collide.

## Execution Rules

- Batch file reads, searches, status checks, and metadata queries.
- Use isolated worktrees for large unrelated implementation lanes only when creation and cleanup of their branches/directories is authorized. Never remove pre-existing worktrees or user work.
- Use existing supervised sessions for authorized long-running work; inspect commands for writes, network access and resource conflicts first. Builds/tests may share caches, ports or databases despite separate source files. Backfills and deploys require separate explicit authorization, not merely a lane in the matrix. Observe completion and stop only processes owned by this task.
- If a lane discovers a blocker that changes the plan, pause dependent lanes
  and update the matrix.
- Never let a background process outlive the turn unless the user explicitly
  asked for a continuing service.
- Do not parallelize destructive commands, migrations, writes to the same table,
  or live customer-impacting deploys without an explicit gate.

## Output Shape

Use this when reporting:

```text
Parallel execution result:
- Lanes run: 5
- Lanes completed: 4
- Blocked lane: deploy readback, waiting on DNS propagation
- Fast path found: batched repo scan + focused tests
- Verification: lint pass, unit pass, live smoke pass
```

## Failure Modes

- More concurrency that creates conflicting edits.
- Benchmarking the tool instead of the task.
- Treating "fast" as done before correctness is proven.
- Forgetting to poll running sessions.
- Hiding skipped checks behind a success summary.
