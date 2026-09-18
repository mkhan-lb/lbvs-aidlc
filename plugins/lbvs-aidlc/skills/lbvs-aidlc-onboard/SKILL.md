---
name: lbvs-aidlc-onboard
description: Onboard AIDLC onto an existing codebase by scouting its conventions, choosing modernize or stay-legacy with the user, and proposing a repository CLAUDE.md, path-scoped rules and a docs/repo-profile.md that are written only on confirmation.
when_to_use: Use when the project mode is brownfield and no repository CLAUDE.md or conventions record exists yet, when the mode is greenfield and default conventions have not been offered, or when the user says "onboard", "brownfield", "existing codebase", "conventions", "what does this repo do", or "set up Claude for this repo".
---

# Onboard an existing codebase

Contract: ${CLAUDE_PLUGIN_ROOT}/docs/WORKFLOW.md. Paths are repository-root relative; bundled files are relative to this skill directory.

Everything before step 5 is read-only, except the greenfield `conventions --apply` in step 1, which runs only on the user's explicit choice. Recommendations are not permission to act.

## 1. Establish mode

Read the `AIDLC project mode:` line from session context, or run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" mode`. If `.aidlc/mode` and `docs/onboarding.md` already exist, summarise the recorded decision and ask whether to refresh it before scouting.

**Greenfield:** say so and, unless the user wants a full onboarding pass, do only this: run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" conventions` (report only) and use AskUserQuestion with exactly "Adopt default conventions (`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" conventions --apply`)", "Keep my own tooling", "Decide later". Run `--apply` only on the first choice; it copies missing defaults from `templates/conventions/` and never overwrites. When the project needs cloud delivery, point to `docs/platform/README.md`: the app-template route fetches `AGENT-SETUP.md` via authenticated `gh api` (never a raw link); `docs/platform/platform.md` is filled once per service. Then stop.

**Brownfield:** run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" conventions` (report only) so step 4 can record the conventions files the repository already owns; never apply defaults over an existing repository. If `docs/repo-profile.md` exists, run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" profile`: `fresh` → skip step 2 and take the digest from the profile unless the user asks for a re-scout; `stale` or `missing` → scout.

## 2. Scout (delegate)

Use the Agent tool to run `lbvs-aidlc-repo-scout` with this brief: "Report on this repository per your report format. Prioritise the commands, conventions and existing agent instructions." plus the `profile` output when a profile exists. The scout is read-only and returns its fixed headings (Stack … Recommendations).

Before delegating, if `graphify` is installed and `graphify-out/graph.json` is absent, offer (AskUserQuestion: "Build a code graph first", "Skip") to run `/graphify .` (local, no API key) so the scout can cite `graphify-out/GRAPH_REPORT.md`. Never install it; if missing, note `uv tool install graphifyy` in the digest and continue.

Read the report. Spot-check two or three cited paths with Read; drop claims that do not hold. Present a short digest (stack, commands, conventions, hotspots, existing instructions).

## 3. Decide direction

Use the AskUserQuestion tool with exactly these options:

- **Modernize (adopt current patterns)**
- **Stay legacy (inherit existing style)**
- **Decide later**

Record the answer for step 5. Do not proceed on an assumed answer.

**Stay legacy** → invoke the `inherit-legacy-style` skill via the skill route. Its style note is advisory; pass it the scout's Conventions and Hotspots for exemplar files and return here.

**Modernize** → recommend the official `code-modernization` plugin (do not install it; the user installs via `/plugin`). Then list only the bundled pattern skills that match the detected stack (e.g. `coding-standards`, `error-handling`, `api-design`, `python-patterns`, `react-patterns`, `golang-patterns`, `dotnet-patterns`, `postgres-patterns`, `kubernetes-patterns`, `security-review`), confirming each exists under `${CLAUDE_PLUGIN_ROOT}/skills/`; one line each on why it applies; do not invoke them now.

**Decide later** → skip both; note the open decision in the drafts.

## 4. Draft instructions (proposal only)

Draft a repository `CLAUDE.md` of at most 60 lines: project one-liner; `## Commands` (build, test, lint, run, verbatim from the scout, paths verified); `## Conventions` (existing tooling per `conventions` — formatter, linter, pre-commit, editorconfig — cited by path; defaults only where a file is absent, never overwriting); `## Architecture` (directory → purpose, frozen or generated areas); `## Things Claude gets wrong here` (seed from hotspots and convention conflicts; the team adds an entry whenever Claude repeats a mistake). If a `CLAUDE.md` exists, draft additions and mark what is new; never rewrite existing policy. When the repository deploys to the cloud, add a one-line pointer to `docs/platform/platform.md` and note whether it is filled.

Draft path-scoped `.claude/rules/<topic>.md` files only where a convention applies to a subtree (e.g. `paths: ["src/api/**"]`), one topic per file, each under 30 lines.

Draft `docs/repo-profile.md` from the [profile template](templates/repo-profile.md) and the scout report. Header lines exactly: `# Repository profile: <repository>`, `Last verified: <YYYY-MM-DD> at <full commit sha>` (`git rev-parse HEAD`), `Manifests: <manifest files the scout found, space-separated>`, `Profiled by: lbvs-aidlc-repo-scout via /lbvs-aidlc-onboard`. Identity names the glossary under `docs/glossary/`; other sections hold cited facts or `Unknown`. An existing profile gets only changed sections and header updated.

Show the drafts in the conversation. Offer `/init` (`CLAUDE_CODE_NEW_INIT=1`) as the alternative if the user prefers Claude Code's generated baseline, then trimming it.

## 5. Confirm and write

Use AskUserQuestion with exactly "Write CLAUDE.md, rules and repo profile", "Write repo profile only", "Do not write". In plan or read-only mode, return the drafts labelled **not saved; draft only** and stop.

Only on confirmation:

1. Write the confirmed files. Read each back and confirm the content matches its draft.
2. Write `.aidlc/mode` containing exactly `brownfield` (or `greenfield` only if the user overrode the detection).
3. Write `docs/onboarding.md`: date, detected mode, direction chosen (modernize / legacy / undecided), scout digest, files written, skills or plugins recommended, open questions.

If the user declines, write nothing and leave the drafts in the conversation.

## 6. Hand back

Summarise what was written (`CLAUDE.md`, rules, `docs/repo-profile.md`), what was only recommended, and the open decision if "Decide later" was chosen. If the orchestrator invoked this skill, return control so it can start `lbvs-aidlc-intent`; otherwise suggest `/lbvs-aidlc <change-id>` for the first change.

## Guardrails

- Never invent commands, versions or conventions; cite the scout's paths or say unknown.
- Existing `CLAUDE.md`, `AGENTS.md`, rules and `.cursorrules` remain authoritative; propose, do not override.
- No plugin installs, hooks, settings edits, commits or pushes from this skill.
