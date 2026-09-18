# lbvs-aidlc

Company AIDLC package from Anthropic's AI-native SDLC playbook, exported as a repository template. Contract: docs/WORKFLOW.md. Recipes: docs/USAGE.md. Every command, agent, hook, store, host and design decision: docs/REFERENCE.md. Scope: GOALS.md; deferred work: FUTURE_WORK.md. Change artifacts live in `changes/<change-id>/`; knowledge records in `docs/adr/`, `docs/incidents/`, `docs/security/`, `docs/references/`, `docs/solutions/`, `docs/playbooks/`; platform facts in `docs/platform/platform.md`.

## Commands

- `python3 scripts/aidlc.py check` — required assets, local links, skill frontmatter and the size rules (AIDLC skill ≤ 7168 bytes, orchestrator ≤ 7788; agent body ≤ 3 KB with a matching `.omp/agents` description; this file ≤ 60 lines). Package integrity only, not lifecycle verification.
- `python3 scripts/aidlc.py status` — every `changes/<id>/` with the stage artifacts present, the stage reached and the next one; marks the current change.
- `python3 scripts/aidlc.py lint-artifacts [--root <repo>] [<change-id>]` — flags machine paths and session references (`artifact://`, `agent://`, `/Users/…`, `/tmp/…`) in `changes/<id>/` and `docs/solutions/`, one `path:line` per hit, exit 1 on any; the [content boundary](docs/ARTIFACTS.md#content-boundary) made mechanical. Run by `lbvs-aidlc-review` before its read-back and by the conventions checker before ship.
- `python3 scripts/aidlc.py current` — the change ID in play, resolved from the branch, `.aidlc/current` or the only change without `review.md`; exit 1 when nothing resolves.
- `python3 scripts/aidlc.py mode` — prints `AIDLC project mode: greenfield|brownfield`; `.aidlc/mode` overrides the heuristic.
- `python3 scripts/aidlc.py new <change-id>` — creates only `changes/<change-id>/intent.md`; never overwrites.
- `python3 scripts/aidlc.py doctor` — local prerequisites, optional tools (`graphify`, `codegraph`, `gh`, `omp`) and the auth each `.mcp.json` server needs; `--install` runs the `uv`/`pipx`, `npm` or `brew` installer for missing optional tools only. Connectivity and external services are not checked.
- `python3 scripts/aidlc.py package <new-dir>` — exports the standalone template; never overlays an existing repository or installs plugins.
- `python3 scripts/aidlc.py conventions` — compares the repository with `templates/conventions/` defaults; `--apply` copies only the missing ones, never overwrites. Greenfield adopts; brownfield keeps its own.
- `python3 scripts/aidlc.py install <repo> [--apply]` / `sync <repo> [--apply]` / `update [--from <pkg>] [--apply]` — put the AIDLC assets into an existing repository and update them later (`update` runs inside the adopter and clones the source recorded in `.aidlc/manifest.json`): report first; never overwrites a differing file; skips our index/template for a knowledge store the repository already keeps; never creates or overwrites `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `.claude/settings.json`, `.mcp.json`, `.worktreeinclude`, `.omp/AGENTS.md`, `.omp/config.yml` (prints merge hints instead); never commits. This — not `--root` from the package checkout — is how a repository adopts the workflow.
- `python3 scripts/aidlc.py profile` — prints `profile: missing|fresh|stale (<n> manifest commits since <rev>)` for `docs/repo-profile.md`; refresh with `/lbvs-aidlc-onboard`.
- `python3 scripts/aidlc.py worktree` / `worktree-remove` — the `WorktreeCreate` / `WorktreeRemove` hook entrypoints; read the hook JSON on stdin. Not for direct use.
- `python3 scripts/build_plugin.py` — regenerates the committed Claude Code plugin under `plugins/lbvs-aidlc/` from the sources; run it in the same commit as any change to an AIDLC skill, agent, hook or shared doc. `check` runs `--check` and fails on drift.

## Working rules

- Start a change or bug fix with `/lbvs-aidlc` — it resolves the ID (argument → branch → `.aidlc/current` → the only open change → asks) and proposes the worktree `aidlc/<change-id>`. IDs match `^[a-z0-9]+(-[a-z0-9]+)*$`; prefix the ticket key when there is one, e.g. `vs-1234-order-export`. Pass only the bare ID as a slash-command argument; state context, flow policy and CE choices in conversation.
- After writing an artifact, Read the saved file back before reporting completion.
- Plan mode returns proposals; `lbvs-aidlc-build` saves the confirmed plan to `changes/<change-id>/plan.md` before touching code. Native plan scratch is not the canonical plan.
- No commits, pushes, new remotes, global settings changes, bypass-permissions flags or deployments without explicit authorisation in the conversation. Only `/lbvs-aidlc-ship` commits, pushes and opens a PR — plus, after the PR exists, one `docs(<id>): record PR #<n>` commit under the same choice — and only after the engineer picks that option. The single exception before ship is the fix loop's [reproduction commit](docs/WORKFLOW.md#reproduction-commit): the failing test alone, on "Commit now".
- `changes/<id>/` ships to the adopting repository: repository-relative paths, environment by kind and version, decisions not transcript, nothing about how the workflow, hooks or the workstation behaved — that goes in `FUTURE_WORK.md` here. Lessons go to the store the repository already names (`CLAUDE.md`, `docs/repo-profile.md`), never a new `docs/solutions/`.
- Compound Engineering 3.26.3 is declared at project scope in `.claude/settings.json` (`extraKnownMarketplaces` + `enabledPlugins`) but the declaration does not install it: each engineer runs `claude plugin install compound-engineering@compound-engineering-plugin --scope project` once per clone. Use CE only when explicitly selected; decide availability from the session skill catalog, never by searching the filesystem. Caveman is per-engineer opt-in and not declared.
- Read `.compound-engineering/config.yaml` for `docs_root` before touching `solutions/` or `ideation/` stores; never probe the defaults speculatively.
- `Logicbroker/app-template` and `Logicbroker/app-delivery-kit` are internal repositories: fetch files with an authenticated `gh api repos/<owner>/<repo>/contents/<path>`; raw links 404.
- `.mcp.json` holds no credentials: `context7` is anonymous or `CONTEXT7_API_KEY` = `Bearer <key>` (literal prefix), `github` needs `GITHUB_PERSONAL_ACCESS_TOKEN`, `atlassian` authenticates by OAuth via `/mcp`. `mcp-configs/` is an inactive upstream snapshot — never load it with `--mcp-config`.
- Report actual commands, results and limits. Keep this file short; add a rule only when a verified mistake recurs.

## Things Claude gets wrong here

- Importing a remembered summary of an ideation or plan instead of reading the saved file.
- Probing `docs/solutions` before reading the CE config root.
- Treating a write acknowledgement, handoff snapshot, agent verdict or review pass as read-back or approval.
- Appending prose to a slash-command argument; every stage validates a single bare ID.
