---
name: lbvs-aidlc-onboard
description: Onboard AIDLC onto an existing codebase by scouting its conventions, choosing modernize or stay-legacy with the user, and proposing a repository CLAUDE.md, path-scoped rules and a docs/repo-profile.md that are written only on confirmation.
when_to_use: Use when the project mode is brownfield and no repository CLAUDE.md or conventions record exists yet, when the mode is greenfield and default conventions have not been offered, or when the user says "onboard", "brownfield", "existing codebase", "conventions", "what does this repo do", or "set up Claude for this repo".
---

# Onboard an existing codebase

Contract: docs/WORKFLOW.md. Paths are repository-root relative; bundled files are relative to this skill directory.

Steps 1-4 are read-only, except the greenfield `conventions --apply` in step 1, run only on the user's explicit choice. Recommendations are not permission to act.

## 1. Establish mode

Read the `AIDLC project mode:` line from session context, or run `python3 scripts/aidlc.py mode`. If `.aidlc/mode` and `docs/onboarding.md` exist, summarise the recorded decision and ask whether to refresh it before scouting.

**Greenfield:** say so and, unless the user wants a full onboarding pass, do only this: run `python3 scripts/aidlc.py conventions` (report only) and use AskUserQuestion with exactly "Adopt default conventions (`python3 scripts/aidlc.py conventions --apply`)", "Keep my own tooling", "Decide later". Run `--apply` only on the first choice; it copies missing defaults from `templates/conventions/` and never overwrites. For cloud delivery, point to `docs/platform/README.md` (the app-template route fetches `AGENT-SETUP.md` via authenticated `gh api`, never a raw link; `platform.md` is filled once per service). Then stop.

**Brownfield:** run `python3 scripts/aidlc.py conventions` (report only) so step 4 records the conventions files the repository owns; never apply defaults over an existing repository. If `docs/repo-profile.md` exists, run `python3 scripts/aidlc.py profile`: `fresh` → skip step 2 and take the digest from the profile unless the user asks for a re-scout; `stale` or `missing` → scout.

## 2. Scout (delegate)

Use the Agent tool to run `lbvs-aidlc-repo-scout` with this brief: "Report on this repository per your report format. Prioritise the commands, conventions, existing agent instructions and knowledge stores." plus the `profile` output and the `skipped` list from `.aidlc/manifest.json` when they exist. The scout is read-only and returns its fixed headings.

Before delegating, if `graphify` is installed and `graphify-out/graph.json` is absent, offer (AskUserQuestion: "Build a code graph first", "Skip") to run `/graphify .` (local, no API key) so the scout can cite `graphify-out/GRAPH_REPORT.md`. Never install it; if missing, note `uv tool install graphifyy` in the digest.

Spot-check two or three cited paths with Read; drop claims that do not hold. Digest: stack, commands, conventions, hotspots, existing instructions, knowledge stores.

## 3. Decide direction

Use the AskUserQuestion tool with exactly these options:

- **Modernize (adopt current patterns)**
- **Stay legacy (inherit existing style)**
- **Decide later**

Record the answer for step 5; never proceed on an assumed one.

**Stay legacy** → invoke the `inherit-legacy-style` skill via the skill route. Its style note is advisory; pass it the scout's Conventions and Hotspots as exemplars and return here.

**Modernize** → recommend the official `code-modernization` plugin (the user installs it via `/plugin`; never install). Then list only the bundled pattern skills that match the detected stack (e.g. `coding-standards`, `error-handling`, `python-patterns`, `react-patterns`, `postgres-patterns`, `security-review`), confirming each exists under `.claude/skills/`; one line each on why it applies; do not invoke them now.

**Decide later** → skip both; note the open decision in the drafts.

## 4. Draft instructions (proposal only)

Draft a repository `CLAUDE.md` of at most 60 lines: project one-liner; `## Commands` (build, test, lint, run, verbatim from the scout, paths verified); `## Conventions` (existing tooling per `conventions` — formatter, linter, pre-commit, editorconfig — cited by path; defaults only where a file is absent, never overwriting); `## Architecture` (directory → purpose, frozen or generated areas); `## Things Claude gets wrong here` (seeded from hotspots and convention conflicts; the team adds an entry per repeated mistake). If a `CLAUDE.md` exists, draft additions and mark what is new; never rewrite existing policy. Cloud-deployed repository: add a one-line pointer to `docs/platform/platform.md`, noting whether it is filled.

Draft path-scoped `.claude/rules/<topic>.md` files only where a convention applies to a subtree (e.g. `paths: ["src/api/**"]`), one topic per file, each under 30 lines.

Draft `docs/repo-profile.md` from the [profile template](templates/repo-profile.md) and the scout report. Header lines exactly: `# Repository profile: <repository>`, `Last verified: <YYYY-MM-DD> at <full commit sha>` (`git rev-parse HEAD`), `Manifests: <files the scout found, space-separated>`, `Profiled by: lbvs-aidlc-repo-scout via /lbvs-aidlc-onboard`. Identity names the glossary under `docs/glossary/`; other sections hold cited facts or `Unknown`. Knowledge stores: one row per store the scout found (`docs/adr/`, `docs/decisions/`, `ADR*`, `.claude/knowledge/`, `RUNBOOK*` …) and the manifest's `skipped` seeds; a store the repository lacks keeps the package-default row. An existing profile gets only changed sections and header updated; store rows change only where their directories did.

Show the drafts. Offer `/init` (`CLAUDE_CODE_NEW_INIT=1`) as the alternative when the user prefers Claude Code's generated baseline, trimmed afterwards.

## 5. Confirm and write

Use AskUserQuestion with exactly "Write CLAUDE.md, rules and repo profile", "Write repo profile only", "Do not write". In plan or read-only mode, return the drafts labelled **not saved; draft only** and stop.

Only on confirmation:

1. Write the confirmed files; Read each back against its draft.
2. Write `.aidlc/mode` containing exactly `brownfield` (or `greenfield` when the user overrode detection).
3. Write `docs/onboarding.md`: date, detected mode, direction chosen (modernize/legacy/undecided), scout digest, files written, skills or plugins recommended, open questions.

Declined: write nothing; the drafts stay in the conversation.

## 6. Hand back

Summarise what was written (`CLAUDE.md`, rules, `docs/repo-profile.md`), what was only recommended, and the open decision under "Decide later". Invoked by the orchestrator: return control so it starts `lbvs-aidlc-intent`; otherwise suggest `/lbvs-aidlc <change-id>` for the first change.

## Guardrails

- Never invent commands, versions or conventions; cite the scout's paths or say unknown.
- Existing `CLAUDE.md`, `AGENTS.md`, rules and `.cursorrules` remain authoritative; propose, never override.
- No plugin installs, hooks, settings edits, commits or pushes from this skill.
