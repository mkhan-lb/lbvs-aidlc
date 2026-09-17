# Engineering conventions (defaults)

These are the defaults a **greenfield** repository starts from. A **brownfield** repository keeps its own conventions; `aidlc-onboard` records them in the repository `CLAUDE.md` and `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py" conventions` reports which files exist instead of overwriting them. Change a default here only through an ADR.

## Formatting and linting

- `.editorconfig` is the source of truth for whitespace; formatters follow it.
- Python: `ruff` (lint + format), settings in `ruff.toml`; tests may use `assert`.
- JavaScript/TypeScript: `biome` (lint + format + import order), settings in `biome.json`; `any` is an error.
- Other stacks use the stack's standard formatter and linter (`gofmt`/`golangci-lint`, `dotnet format`) configured in the repository, not in this package.
- Never suppress a lint failure without a comment naming the reason and the condition for removing the suppression.

## Pre-commit

`.pre-commit-config.yaml` runs whitespace/EOF fixes, YAML/JSON validation, large-file and private-key detection, `gitleaks`, `ruff` and `biome`. Install with `pre-commit install`; CI should run `pre-commit run --all-files` as part of the required check so local skips do not pass review.

## Commits, branches and pull requests

- Branch `aidlc/<change-id>` per change, where the change ID starts with the Jira key when one exists (`vs-1234-order-export`).
- Commit title: imperative, under 72 characters, prefixed with the Jira key when one exists (`VS-1234: add order export`); otherwise a Conventional Commits type (`feat:`, `fix:`, `docs:`…). Body says why, not what.
- One reviewable change per PR; no unrelated cleanup, generated-output edits or secrets. The PR body links `changes/<change-id>/` artifacts and the ticket; `evidence.md` carries the verification.
- Agents prepare commits and PRs only when a human explicitly asks and never merge, push to protected branches or approve their own work.

## Tests

- Behaviour changes ship with a focused test that asserts an observable outcome; bug fixes ship with the failing reproduction test first (`/aidlc-fix`).
- Prefer the repository's existing runner and layout; generated code is proven by the generator's own tests, not by hand-written assertions on its output.
