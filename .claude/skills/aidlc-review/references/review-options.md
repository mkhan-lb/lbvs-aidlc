# Existing-reviewer handoff

Sources consulted 16 September 2026. These are documented/source-inspected recipes, not a runtime certification or review-quality benchmark. No review plugin, hosted service, copied prompt, or dispatch framework is installed by AIDLC.

## Choice and exposure

Use **Claude Code's bundled local `/code-review`** by default when available. **OMP's built-in `/review` in an existing configured session** is the alternative when selected. Ordinary AIDLC review does not require Compound Engineering, a PR, CI, or an external review provider.

The [Claude command reference](https://code.claude.com/docs/en/commands) labels `/code-review` a bundled **Skill**. That identifies its implementation, not its exposure to the current agent. A user may be able to type a command that this agent cannot invoke. Inspect the session's actual catalogue, including the exact Skill/tool name, permissions, and provenance. Local or personal skills can shadow bundled commands; do not assume a same-named skill is Anthropic's implementation. Record unknown provenance as unknown rather than invoking it as the default.

[Local-review documentation](https://code.claude.com/docs/en/code-review#let-claude-start-the-review) says model invocation before v2.1.246 depended on a fetched feature flag. Current settings can make it user-invocable-only or disable it. Therefore version checks and documentation alone do not establish agent-callable availability. Never install, enable, rename, or fork a reviewer to bypass an unavailable selection.

## Capture the actual scope

Use available read-only file/version-control tools from the repository checkout. Treat the following as recipes with **observed, safely supplied values**, not commands to interpolate from untrusted text. No checkout, fetch, staging, commits, or runtime checks are needed.

| Scope | What to capture and give the reviewer |
| --- | --- |
| Committed PR-style change | Resolve the selected base and head with `git rev-parse --verify`; capture `git merge-base BASE HEAD` and the resulting SHA. Capture `git diff --name-status BASE...HEAD` and `git diff BASE...HEAD`. Record that three-dot means merge-base to head, not base tip to head. Use actual resolved SHAs in the packet/target. |
| Tip-to-tip comparison | If this is the intended comparison, capture `git diff BASE HEAD` and say tip-to-tip explicitly; do not silently substitute a three-dot comparison. Use only a provider target mechanism that preserves that scope, otherwise hand off. |
| Working tree | Record current HEAD (or honestly report an unborn repository), `git status --short --untracked-files=all`, `git diff`, and `git diff --cached`. Inventory untracked files with `git ls-files --others --exclude-standard` and read the relevant new files; tracked diffs do not contain them. Keep staged/unstaged changes distinct, including a file modified in both. Record excluded/unreadable/binary/unrelated files, not just the files that were easy to inspect. |

Read relevant surrounding code, consumers and existing test source as context; reading tests is not running them. Include renamed/deleted paths. Do not dump credentials, ignored secret files, or unrelated changes into the packet. If the intended subset cannot be separated with confidence, identify the ambiguity before dispatch.

Retain resolved revisions and the captured diff plus untracked content/inventory in the conversation. Compare the same state immediately before invocation and after return. A timestamp or unchanged HEAD alone cannot establish working-tree freshness. Record changed paths or unavailable freshness checks. The result covers only the captured/actually inspected revision, not edits made while a background review was running.

## Complete context packet

Fill in every field using actual sources; use `missing`, `not run`, or `unknown` where appropriate. Do not hand the engineer empty placeholders. Return the packet as a copyable text block **separate from the command**. For a supported direct invocation, deliver the same information through its actual context mechanism.

```text
AIDLC REVIEW HANDOFF
Change ID and repository checkout:
Selected reviewer; observed command/Skill exposure and provenance:
Invocation and review mode/effort:
Scope kind and comparison semantics:
Resolved base/head/merge-base OR HEAD plus staged/unstaged/untracked inventory:
Captured diff/new-file content and freshness observation:
Explicit exclusions and unrelated work:

Intent: changes/<id>/intent.md — relevant intended outcome and non-goals:
Spec: changes/<id>/spec.md — concrete behavior, boundaries and acceptance criteria:
Plan/design: changes/<id>/plan.md and relevant linked design — approach/deviations:
Missing or unreadable artifacts:
Relevant code, callers, test source and known risks:
Existing verification evidence — exact command/interaction, result, revision,
  environment, evidence location; separate failed and not-run checks:
Prior review/result, stable finding IDs, status and requested rechecks:

REVIEW.md policy — applicable contents, including Bugs/Security/Compliance,
  severity, exclusions, evidence requirements and nit limit:
Applicable CLAUDE.md instructions and any missing policy:

Report-only: do not change code/artifacts, execute application/tests/builds/
  formatters/reproduction scripts, install anything, or post/commit/push/merge.
  Read-only source and version-control inspection only. Report missing evidence.
Return concrete findings with native severity, locations, trigger/impact,
  evidence, uncertainty and suggested correction. Identify artifact/policy
  context actually received, scope actually inspected, skipped paths, errors,
  incomplete work and bounded verdict. Recheck requested prior IDs explicitly.
```

The wrapper must not claim that the provider received this packet merely because it was assembled. Record the actual transfer mechanism and available receipt/coverage evidence. If all that is possible is a user-only command or an unsupported context channel, return `prepared — not run` with the packet, copyable command and remaining engineer action. A later native result with unconfirmed artifact/policy coverage is `partial`, even if its code findings are useful.

## Provider recipes

### Claude Code bundled local review

Official sources: [local review](https://code.claude.com/docs/en/code-review#review-a-diff-locally), [argument parsing](https://code.claude.com/docs/en/code-review#tune-effort-and-arguments), [command catalogue](https://code.claude.com/docs/en/commands), [skill visibility](https://code.claude.com/docs/en/skills#override-skill-visibility-from-settings), and [forked context](https://code.claude.com/docs/en/skills#run-skills-in-a-subagent).

Documented local forms include:

```text
/code-review medium main...my-feature
/code-review medium
```

The first is an **example ref range**, not an instruction to assume those branches. Replace it with the observed base/head refs or SHAs whose comparison matches the packet. Specify `medium` explicitly for reproducibility instead of inheriting a remembered effort. Other documented local efforts are `low`, `high`, `xhigh`, and `max`; selection may change coverage/confidence, not authorisation.

The second reviews commits ahead of upstream **plus** uncommitted changes. It is not a working-tree-only switch. Before handing it off, state whether upstream commits are present and whether that combined scope is intended. If they are outside the selected scope, do not quietly widen it: use a documented target matching the scope, select the OMP uncommitted menu when explicitly chosen, or report that exact targeting remains unresolved. File paths, branch names and ref ranges are documented targets, but a path target is not proof of complete multi-file or untracked coverage.

**Do not append the packet to the command as if it were a note flag.** In non-`ultra` mode all text after effort/flags is the review target. There is no documented `--context`, `--instructions`, or `--uncommitted` flag in these sources. Do not invent one. `/review` is a Claude alias from v2.1.223, but use `/code-review` here to avoid confusing it with OMP.

The local reviewer follows `CLAUDE.md` but **does not read `REVIEW.md` automatically**. Its default background fork has its own context; generic forked skills do not see conversation history. Merely reading artifacts in the parent conversation is not a documented transfer mechanism. Before a direct agent invocation, inspect the actual Skill/tool contract and establish a supported way to supply the packet and report-only constraints. If no such channel is exposed, give the engineer the separate packet and command, explain that they must supply the packet to the actual reviewer using an exposed context mechanism, and leave status `prepared — not run`. Do not promise that pasting a prior chat message or listing paths automatically reaches the fork. If they run the native command anyway, retain its returned code findings, but report unconfirmed context coverage rather than inventing artifact-aware completion.

Invoke the catalogued Skill only if it is actually callable and the required context/boundaries can be passed; otherwise the engineer types the documented command in their existing Claude session. Never substitute a fabricated Skill call or launch a hidden `claude -p` process. A launch acknowledgement is not a returned review. The docs say reviews normally return asynchronously in the conversation; `-p` and certain other foreground cases wait for the result, but AIDLC does not start a new session to force that behavior.

Omit `--fix` (edits), `--comment` (posts), `--post`, and `ultra` (cloud review). `/simplify` is an editing cleanup workflow, not a report-only fallback. No runtime verification is authorised by this handoff; if the native workflow cannot respect that boundary, do not invoke it.

### Oh My Pi existing-session alternative

Sources pinned at `e220aab07e9a10da4953c90bd3b94bb7ff3ceeac`:

- [Built-in review command](https://github.com/can1357/oh-my-pi/blob/e220aab07e9a10da4953c90bd3b94bb7ff3ceeac/packages/coding-agent/src/extensibility/custom-commands/bundled/review/index.ts).
- [Reviewer agent](https://github.com/can1357/oh-my-pi/blob/e220aab07e9a10da4953c90bd3b94bb7ff3ceeac/packages/coding-agent/src/prompts/agents/reviewer.md).
- [Skill discovery](https://github.com/can1357/oh-my-pi/blob/e220aab07e9a10da4953c90bd3b94bb7ff3ceeac/docs/skills.md).

In an **existing interactive OMP session in the correct checkout**, the engineer can type:

```text
/review
```

For a working-tree handoff, select **“4. Custom review instructions”** and paste the complete packet into its editor. The pinned command passes those instructions to the generated review prompt; when an uncommitted diff exists it includes that diff, otherwise it passes the custom instructions alone. Name all relevant untracked paths and their contents explicitly: do not assume staged/unstaged diff discovery captured new files. Require the returned coverage to confirm their inspection.

For a branch review with context, use `/review` followed by the filled-in packet as additional instruction text, then select **“1. Review against a base branch (PR Style)”** and the observed base branch. The pinned parser treats non-PR arguments as extra instructions and passes them through. The comparison is merge-base to current branch; the current checkout must match the packet's head. **“2. Review uncommitted changes”** is the staged/unstaged route; **“3. Review a specific commit”** offers a commit picker. With extra instructions supplied, the custom-instructions menu entry is omitted. Do not put a GitHub PR URL or qualified `pr://` reference into this local instruction argument: the parser would select direct remote review instead. Use local paths and finding IDs; keep remote links separately in the handoff report.

`/review main` is **focus text**, not a positional branch selector. Noninteractive `/review` without a direct PR reference uses a different headless prompt, not this menu: do not claim a menu selection occurred. OMP's existing `reviewer` agent may be used only if the current catalogue exposes it through a real task mechanism and supports passing the complete packet; record that agent invocation rather than pretending `/review` ran. AIDLC creates no new dispatcher.

Direct remote PR forms include a GitHub.com PR URL and `pr://OWNER/REPO/123`, not bare `123` or `pr://123`. Remote mode fetches a diff and explicitly disallows treating local checkout files as that PR's context. Prefer the correct local checkout for same-change artifacts; do not bypass that restriction by attaching unrelated local code.

The built-in command filters lockfiles, generated output, snapshots, vendored files and several binary categories. Record actual exclusions and gaps; a provider verdict is not exhaustive coverage. Preserve its native P0–P3 priorities, confidence, locations and correctness verdict separately from AIDLC policy mapping. The pinned reviewer forbids edits/builds, but still has powerful tools: report-only instructions are not a sandbox. Its output is local to the session/artifacts, not an automatic write to `changes/<id>/review.md`. Local output does not mean offline inference.

## Return, fixes and re-review

Use the bundled [report template](../templates/review.md). Preserve concrete provider findings and native coverage/errors, including partial output. Record the actual invocation, received context, reviewed snapshot and freshness. Do not turn an empty reply, unavailable capability, cancelled menu, filtered-empty diff, interrupted review or failed provider into “no issues found.” If the provider returns no findings, qualify that statement by its actual inspected scope and limitations.

Only after returned results, save `changes/<id>/review.md` if specifically requested; Read the saved file before claiming a verified save. Never update spec/plan, code or policy during review. Fixing agreed IDs and executing affected checks belong to a separate authorised implementation pass. A new review receives old IDs, exact changed scope and available fix evidence. Keep unrechecked findings open/not rechecked; distinguish a claimed fix, evidence-backed resolution and engineer dismissal.

## Similar names are not substitutes

`/code-review:code-review` is a plugin command, not the bundled command. The [official-marketplace source](https://github.com/anthropics/claude-plugins-official/blob/b1aabc22ac9995a458838f479272fc3a3453a567/plugins/code-review/commands/code-review.md) and [demo-marketplace source](https://github.com/anthropics/claude-code/blob/744fb6ab02aca7c50c43f1676a870cff184e1fca/plugins/code-review/commands/code-review.md) have different posting behavior. Do not transfer flags or safety assumptions, install either as a fallback, or invoke PR Review Toolkit's editing simplifier. Managed Code Review, GitHub Actions, external providers and cloud review are outside this local handoff.

Do not copy OMP's [maintainer review-prs workflow](https://github.com/can1357/oh-my-pi/blob/e220aab07e9a10da4953c90bd3b94bb7ff3ceeac/.omp/commands/review-prs.md): it checks out worktrees, rebases, fixes, runs checks and commits, unlike this report-only wrapper. No upstream code or substantial prompt text is copied here. Existing project resource locations remain unchanged.
