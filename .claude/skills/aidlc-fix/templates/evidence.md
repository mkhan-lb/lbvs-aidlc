# Evidence: {{change_id}}

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

## Reproduction

- Steps: exact commands or interactions that showed the defect
- Failing test: repository-relative path (the file protected by `.aidlc/fix/{{change_id}}.json`)
- Pre-fix output: verbatim failing output or exit status, with the command that produced it

## Fix

- Files changed: repository-relative paths
- Root cause: what was actually wrong and why the change resolves it (observed, not assumed)

## Verification

- Commands and actual output: each check run after the fix, with exit status and relevant output
- `/verify` observations: what the bundled verification did against the running app, or `not run` with the reason (no runtime, tool unavailable)
- Screenshots / recordings: repository-relative or artifact paths for UI changes, or `none`

## Regression protection

- Test kept: path of the reproduction test now passing, and where it runs (suite, CI job) if known
- Eval seed suggestion: a one-line candidate case for the team eval set, or `none`

## Lesson link

`docs/solutions/<category>/<topic>.md` when `/aidlc-learn {{change_id}}` saved one, otherwise `none`.

## Limits

Checks not run, environments not covered, assumptions still open, and anything the evidence above does not establish.
