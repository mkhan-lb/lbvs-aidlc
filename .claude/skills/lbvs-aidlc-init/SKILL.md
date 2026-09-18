---
name: lbvs-aidlc-init
description: Set up AIDLC in a repository with an idempotent, report-first wizard — doctor, mode and onboarding, platform facts, MCP/CE auth, code graph, observer plugin, agent maker, ignore patterns; every write is confirmed.
when_to_use: Use when the user says "set up aidlc", "initialise this repo", "adopt aidlc here", "init", or "first time in this repository", or when no `.aidlc/mode`, repository CLAUDE.md or onboarding record exists yet.
---

# Set up AIDLC in this repository

Contract: docs/WORKFLOW.md. Paths are repository-root relative; bundled files relative to this skill directory.

Every step reports first and writes nothing without an AskUserQuestion confirmation; every write is Read back. Rerunning is safe: a step whose result exists says so and moves on. Never install plugins, change settings, store secrets, commit or push; never invent facts — cite a path or say unknown. In plan or read-only mode return proposals labelled **not saved**.

## 0. Doctor

Run `python3 scripts/aidlc.py doctor`. Show which required tools (`python3`, `git`, `claude`) and optional tools (`graphify`, `codegraph`, `gh`, `omp`) are present, and the MCP auth state per `.mcp.json` server. AskUserQuestion: "Run `doctor --install`" (installs only those optional tools with uv/pipx, npm or brew), "Skip".

## 1. Mode and onboarding

Run `python3 scripts/aidlc.py mode`.

**Brownfield:** invoke `lbvs-aidlc-onboard` via the skill route to completion (scout and `conventions` reports, modernize/legacy choice, CLAUDE.md, rules and `docs/repo-profile.md` drafts, `.aidlc/mode`, `docs/onboarding.md`). If `python3 scripts/aidlc.py profile` prints `fresh`, onboarding skips its scout and works from `docs/repo-profile.md`; say so. Keep the profile or scout report for step 6 and return here.

**Greenfield:** run `python3 scripts/aidlc.py conventions` (report only); AskUserQuestion: "Adopt default conventions (`python3 scripts/aidlc.py conventions --apply`)", "Keep my own tooling", "Decide later". `--apply` copies only missing files from `templates/conventions/`, never overwriting. For cloud delivery point to `docs/platform/README.md`: the app-template route fetches `AGENT-SETUP.md` with authenticated `gh api`, never a raw link.

## 2. Platform facts

Read `docs/platform/platform.md`. If it has no bracketed `[...]` items, report it as filled. Otherwise read, without writing, what the repository already tells you: `.circleci/config.yml` (orb pin, required check, approval holds), `deploy/*-values.yaml` (environments), `catalog-info.yaml` (service, owner), `Taskfile.yml`/`Makefile` (commands). Show a diff filling only the discoverable items, the rest left bracketed — never credentials, tokens or production URLs. AskUserQuestion: "Write platform.md", "Skip". On confirmation write and Read back.

## 3. MCP and Compound Engineering

From the doctor output, state per server what still needs authentication: `atlassian` → OAuth via `/mcp`; `github` → `GITHUB_PERSONAL_ACCESS_TOKEN` (from `gh auth token`); `context7` optional (`CONTEXT7_API_KEY` raises limits); `codegraph` needs its binary and `codegraph init`. Then say whether any `compound-engineering:*` skill is in this session's catalog — decided from the catalog alone, never by searching the filesystem. If absent, give the engineer `claude plugin install compound-engineering@compound-engineering-plugin --scope project`, then `/reload-plugins`. Run nothing; write no token anywhere.

## 4. Code graph

If `graphify` is installed and `graphify-out/graph.json` is absent, AskUserQuestion: "Run `/graphify .`" (local, code-only, no API key), "Skip". If missing, name `uv tool install graphifyy` and continue.

## 5. Continuous learning observer (off)

Say whether the `lbvs-aidlc-observer@lbvs-aidlc` plugin is enabled — a `continuous-learning-v2` skill in the catalog, judged as in step 3. If not, AskUserQuestion: "Enable the observer plugin (prints the enable command; data stays under ~/.local/share/ecc-homunculus, includes tool inputs/outputs)", "Leave off". On the first, print `claude plugin enable lbvs-aidlc-observer@lbvs-aidlc` (Claude Code) or `omp plugin enable` (Oh My Pi). Run and write nothing either way; `/lbvs-aidlc-learn` stays the per-change lesson.

## 6. Repository-specific agents and skills (agent maker)

From the scout report (brownfield) or a Glob of the top two levels plus `docs/` (greenfield), propose **at most three** candidates, each with name, one-sentence description, tools, the stage that delegates to it, and why none of the six `lbvs-aidlc-*` agents (`verifier`, `repo-scout`, `design-reviewer`, `threat-modeler`, `test-critic`, `conventions-checker`) or the bundled Explore/Plan subagents already covers it. Propose nothing if nothing qualifies.

Heuristics (cite evidence for each):

- A subsystem of ≥ 40 files or with its own glossary or `docs/` section → read-only `<repo>-<area>-scout` answering design and plan questions about it.
- A test, build or verify procedure documented in `CONTRIBUTING.md`, a task runner or CI → Bash-capable `<repo>-checker` running only those commands verbatim and reporting; verify and build delegate to it.
- Generated code with its generator present (OpenAPI, protobuf, ORM, codegen) → read-only `<repo>-generated-guardian` flagging hand edits under generated paths for review and fix.
- A documented recurring procedure (release, migration, data fix) → a repository **skill** at `.claude/skills/<name>/SKILL.md`, not an agent; sketch its steps and stop.
- A `docs/playbooks/` entry with Status Verified and Runs ≥ 3 → a repository skill `.claude/skills/<repo>-<playbook>/SKILL.md` sourced from it; never auto-written.

For each accepted agent, draft `.claude/agents/<name>.md` from [templates/agent.md](templates/agent.md), replacing every `<placeholder>`; body under 3 KB, description one sentence. AskUserQuestion per candidate: "Write `.claude/agents/<name>.md`", "Skip". Write only on confirmation, Read back; if it exists, show the diff and overwrite only on a further confirmation.

Mention once: `/init` with `CLAUDE_CODE_NEW_INIT=1` proposes CLAUDE.md, skills and hooks from Claude Code's own analysis; the official `skill-creator`/`plugin-dev` plugins help author skills and plugins (not installed here).

## 7. Ignore patterns

Read `.gitignore`. Check for lines covering `.claude/worktrees/`, `.aidlc/fix/`, `.aidlc/current` and `.codegraph/` (a `**/` prefix counts). Show missing lines; AskUserQuestion: "Append missing lines", "Skip". Append only, Read back.

## 8. Summary and next step

List **Written** (paths), **Recommended** (installs, auth, plugins — the engineer's) and **Skipped**. Then AskUserQuestion exactly: "Start a change (/lbvs-aidlc)", "Start from a ticket (/lbvs-aidlc-ticket)", "Done". Invoke `lbvs-aidlc` or `lbvs-aidlc-ticket` via the skill route for the first two; otherwise end.

## Guardrails

- Existing `CLAUDE.md`, `AGENTS.md`, rules, `platform.md` content and `.gitignore` entries stay authoritative; add, never rewrite.
- Delegation adds no permissions: drafted agents inherit this repository's settings and nothing more.
