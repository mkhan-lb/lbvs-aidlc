# Evidence: {{change_id}}

Content boundary: ${CLAUDE_PLUGIN_ROOT}/docs/ARTIFACTS.md#content-boundary — repository-relative paths, no session references, no workflow or machine narrative.

Record what was actually observed while fixing `{{change_id}}`. Fill each section with facts from this session; write `none` or `not run` rather than inventing a value. Remove these drafting instructions before saving.

## Change ID

`{{change_id}}`

## Summary

One or two sentences: the observed defect, who reported it, and the user-visible outcome after the fix.

## References

Optional. Only links supplied by the user or read from an available tool (`gh`, Atlassian MCP, git log). Never guess a key or URL.

- Jira: key/URL or `none`
- PR: URL or `none`
- Incident/alert: link or `none`

## Defect (EARS triad)

Three lines the reproduction and regression tests map to. Keep the wording stable once a test cites it.

- Current: `WHEN <event> THE <system> <incorrect behaviour observed>`
- Expected: `WHEN <event> THE <system> SHALL <correct response>` (the failing test in Reproduction checks this)
- Unchanged: `THE <system> SHALL CONTINUE TO <behaviour that must not regress>` — one line per neighbouring behaviour the Verification section re-checks

## Reproduction

- Steps: exact commands or interactions that showed the defect
- Environment: kind and versions (container image, language/framework versions, isolated test database) — no machine names or temp paths
- Failing test: repository-relative path (the file protected by `.aidlc/fix/{{change_id}}.json`); when a reproduction commit was made, its SHA
- Pre-fix output: verbatim failing output or exit status, with the command that produced it

## Fix

- Files changed: repository-relative paths
- Root cause: what was actually wrong and why the change resolves it (observed, not assumed)
- Library/API references: Context7 ID and the repository's pinned version for any library, framework, SDK or cloud API the fix touched (or the official docs URL when Context7 was unavailable); `docs/references/libraries.md` rows added/updated, or `none`

## Verification

- Expected: command and actual output showing the Expected line now holds, with exit status
- Unchanged: for each `SHALL CONTINUE TO` line, the check run and its result, or `not run` with the reason
- Other commands and actual output: suite/lint runs after the fix, with exit status and relevant output
- `/verify` observations: what the bundled verification did against the running app, or `not run` with the reason (no runtime, tool unavailable)
- Screenshots / recordings: repository-relative paths for UI changes, or `none`

## Regression protection

- Test kept: path of the reproduction test now passing, and where it runs (suite, CI job) if known
- Protection verified: the hook refused a no-op edit before the fix (yes/no)
- Eval seed suggestion: a one-line candidate case for the team eval set, or `none`

## Lesson link

`docs/solutions/<category>/<topic>.md` when `/lbvs-aidlc-learn {{change_id}}` saved one, otherwise `none`.

## Limits

Checks not run, environments not covered, assumptions still open, and anything the evidence above does not establish. Workflow or tooling limitations belong in the package repository, not here; at most one pointer line.
