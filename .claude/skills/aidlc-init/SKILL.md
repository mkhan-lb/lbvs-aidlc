---
name: aidlc-init
description: Idempotent, report-first setup wizard for adopting AIDLC in a repository — doctor, mode and onboarding, platform facts, MCP/CE auth, code graph, repository-specific agents and skills (agent maker), ignore patterns; every write is confirmed.
when_to_use: Use when the user says "set up aidlc", "initialise this repo", "adopt aidlc here", "brownfield setup", "init", or "first time in this repository", or when no `.aidlc/mode`, repository CLAUDE.md or onboarding record exists yet.
---

# Set up AIDLC in this repository

Contract: docs/WORKFLOW.md. Paths are repository-root relative; bundled files are relative to this skill directory.

Every step reports first and writes nothing without an AskUserQuestion confirmation; every write is Read back. Rerunning is safe: a step whose result already exists says so and moves on. Never install plugins, change settings, store secrets, commit or push; never invent facts — cite a path or say unknown. In plan or read-only mode, return proposals labelled **not saved**.

## 0. Doctor

Run `python3 scripts/aidlc.py doctor`. Show which required tools (`python3`, `git`, `claude`) and optional tools (`graphify`, `codegraph`, `gh`, `omp`) are present, and the MCP auth state per server from `.mcp.json`. AskUserQuestion: "Run `doctor --install`" (installs only the listed optional tools with uv/pipx, npm or brew), "Skip".

## 1. Mode and onboarding

Run `python3 scripts/aidlc.py mode`.

**Brownfield:** invoke `aidlc-onboard` via the Skill tool and let it run to completion (scout report, `conventions` report, modernize/legacy choice, CLAUDE.md and rules drafts, `.aidlc/mode`, `docs/onboarding.md`). Keep its scout report for step 5, then return here.

**Greenfield:** run `python3 scripts/aidlc.py conventions` (report only) and AskUserQuestion: "Adopt default conventions (`conventions --apply`)", "Keep my own tooling", "Decide later". `--apply` copies only missing files from `templates/conventions/` and never overwrites. When the project needs cloud delivery, point to `docs/platform/README.md`: the app-template route fetches `AGENT-SETUP.md` with authenticated `gh api`, never a raw link.

## 2. Platform facts

Read `docs/platform/platform.md`. If it contains no bracketed `[...]` items, report it as filled. Otherwise, read-only, look for what the repository already tells you: `.circleci/config.yml` (orb pin, required check, approval holds), `deploy/*-values.yaml` (environments), `catalog-info.yaml` (service name, owner), `Taskfile.yml`/`Makefile` (commands). Show a diff that fills only the discoverable items and leaves the rest bracketed — never credentials, tokens or production URLs. AskUserQuestion: "Write platform.md", "Skip". On confirmation write it and Read back.

## 3. MCP and Compound Engineering

From the doctor output, state per server what still needs authentication: `atlassian` → OAuth via `/mcp` in Claude Code; `github` → `GITHUB_PERSONAL_ACCESS_TOKEN` (`gh auth token` prints one); `context7` optional (`CONTEXT7_API_KEY` raises rate limits); `codegraph` needs the binary and `codegraph init`. Then say whether any `compound-engineering:*` skill is in this session's catalog — decide from the catalog alone, never by searching the filesystem. If absent, give the command for the engineer to run: `claude plugin install compound-engineering@compound-engineering-plugin --scope project`, then `/reload-plugins`. Do not run it and do not write any token anywhere.

## 4. Code graph

If the `graphify` CLI is installed and `graphify-out/graph.json` is absent, AskUserQuestion: "Run `/graphify .`" (code-only extraction, local, no API key), "Skip". If graphify is missing, name `uv tool install graphifyy` and continue.

## 5. Repository-specific agents and skills (agent maker)

Using the scout report (brownfield) or a Glob of the top two directory levels plus `docs/` (greenfield), propose **at most three** candidates. For each give: name, one-sentence description, tools, which stage delegates to it and when, and why none of `aidlc-verifier`, `aidlc-repo-scout`, `aidlc-design-reviewer`, `aidlc-threat-modeler`, `aidlc-test-critic` or the bundled Explore/Plan subagents already covers it. Propose nothing when nothing qualifies.

Heuristics (cite the evidence for each):

- A large or vocabulary-heavy subsystem — at least 40 files, or its own glossary or `docs/` section — → read-only `<repo>-<area>-scout` that answers questions about that area for design and plan.
- A multi-step test, build or verify procedure documented in `CONTRIBUTING.md`, a task runner or CI — → Bash-capable `<repo>-checker` that runs only those documented commands, verbatim, and reports; verify and build delegate to it.
- Generated code with a generator present (OpenAPI, protobuf, ORM models, codegen scripts) — → read-only `<repo>-generated-guardian` that flags hand edits under generated paths for review and fix.
- A recurring multi-step procedure written down in docs (release, migration, data fix) — → a repository **skill** under `.claude/skills/<name>/SKILL.md`, not an agent; sketch its steps and stop there.

For each accepted agent, draft `.claude/agents/<name>.md` from [templates/agent.md](templates/agent.md), replacing every angle-bracket placeholder, keeping the body under 3 KB and the description to one sentence — plugin agents cost startup context on every session. AskUserQuestion per candidate: "Write `.claude/agents/<name>.md`", "Skip". Write only on confirmation and Read back; if the file exists, show the differences and never overwrite without a further confirmation.

Alternatives to mention once: `/init` with `CLAUDE_CODE_NEW_INIT=1` proposes CLAUDE.md, skills and hooks from Claude Code's own analysis; the official `skill-creator` and `plugin-dev` plugins help author skills and plugins by hand (do not install them here).

## 6. Ignore patterns

Read `.gitignore`. Check for lines covering `.claude/worktrees/`, `.aidlc/fix/`, `.aidlc/current` and `.codegraph/` (a `**/` prefix counts). Show the missing lines and AskUserQuestion: "Append missing lines", "Skip". Append only; Read back.

## 7. Summary and next step

List **Written** (paths), **Recommended** (installs, auth, plugins — for the engineer to do) and **Skipped**. Then AskUserQuestion exactly: "Start a change (/aidlc)", "Start from a ticket (/aidlc-ticket)", "Done". Invoke `aidlc` or `aidlc-ticket` via the Skill tool on the first two; otherwise end.

## Guardrails

- Existing `CLAUDE.md`, `AGENTS.md`, rules, `platform.md` content and `.gitignore` entries stay authoritative; add, never rewrite.
- Delegation adds no permissions: the agents you draft inherit this repository's settings and nothing more.
