# Verification record

Date: 16 September 2026. This record preserves earlier source-map/helper checks and records the later workflow-only scope update separately. The full operational Anthropic lifecycle is not verified or complete, and its deferred integrations are not current workflow blockers. See [current goals](../GOALS.md) and the [workflow](WORKFLOW.md).

## Initial local environment (before the Claude upgrade)

- Installed Claude Code: `2.1.270` (`claude --version`).
- `claude auth status --text` reports authenticated Team access; product entitlements, administration and unattended credentials were not established by that check. Account identifiers are intentionally omitted.
- `gh auth status` reports authentication available; no repository was selected/created remotely and no remote policy was modified.
- `git init -b main` created a local repository. No commits, pushes or remote operations were performed.
- `python3 scripts/aidlc.py doctor` exited 0 and found Python 3, Git, Claude Code and this repository. Its output explicitly left external authorities, CI, deployment and incident integrations unchecked.

## Executed artifact-helper scenarios

The real `scripts/aidlc.py` process was invoked with Python 3 against temporary directories outside the project. This exercised the program, not a mock or a source-text assertion.

| Scenario | Observation |
| --- | --- |
| `new smoke-change` in an existing temporary root | Exit 0. Only `changes/smoke-change/intent.md` created; draft status retained; identity substituted. No premature spec or plan created. |
| Repeat the same creation | Exit 1. Original intent byte digest unchanged. |
| IDs containing traversal, uppercase, repeated/trailing hyphens, Unicode or spaces | All six inputs rejected with exit 1. No escaped destination created. |
| `changes` symlink pointing to another directory | Exit 1; no write in the linked destination. |
| `--help` | Exit 0 with the actual operations listed. |

All temporary scenario directories were removed. No generated smoke change was retained in the repository. The helper's validation is not an adversarial multi-user filesystem security boundary; it prevents ordinary invalid paths, symlinked storage and accidental overwrite without pretending to grant approval.

## Package and source integrity

`python3 scripts/aidlc.py check` exited 0: all 25 required assets were present and local links resolved. In a disposable copy, adding a broken local link and removing a required asset each produced exit 1 with a specific error. The original package was not changed by those failure scenarios.

The source snapshot's byte digest matches the SHA-256 recorded in COVERAGE.md. This establishes capture integrity, not the correctness of every claim made by the article. Source prerequisite and current-product disagreements are retained explicitly.

## Historical native discovery and intake, before scope revision

A bounded read-only `claude -p` planning invocation completed, but its asynchronous tool delivery truncated the JSON result and provided no retrievable output artifact. The result content therefore was not used to claim that skill behaviour passed. A completed process alone is not proof of correct output.

Subsequent bounded runs captured complete events in memory. [Sanitised native evidence](evidence/native-smoke.json) records:

- Claude Code discovered all six `aidlc-*` skills and the `aidlc-verifier` agent.
- With one valid ID and no problem statement/approval supplied, `/aidlc-intent smoke-intent` asked for the missing origin, problem, outcome, scope and product owner. Exit 0; only Read calls occurred. The absent working intent was reported rather than invented. No persistence or acceptance was claimed.
- A malformed slash-command argument containing an ID plus multiline prose was rejected as a combined invalid ID. That run also attempted an unavailable personal skill and an unavailable Write tool; both failed. The model incorrectly attributed the personal-skill requirement to repository CLAUDE.md. This is recorded as a limitation, not a clean draft-generation pass or evidence that advisory instructions enforce read-only behaviour.

Both runs exposed only Read/Skill tools and used no configured MCP servers. Use one ID as the slash-command argument and supply intake context in a separate conversation turn. Native discovery and this intake scenario do not prove the other skills, accepted-artifact progression, or the verifier's runtime behaviour.

## Earlier unverified full-playbook capabilities

- A real product owner accepting an intent/spec or an engineer accepting a production change plan.
- Policy-specific skill triggering against owned company standards.
- Automatic permission modes, enforced hooks, administrator-managed settings, sandbox/network/credential boundaries, or authenticated release approval.
- A reference application's build, bug reproduction, visual behaviour, or deployment/rollback.
- Worktree isolation on committed project history or the verifier exercising a real application.
- A genuine 20–50-task eval corpus, CI execution, configuration-regression gate, or incident-derived eval.
- Remote AI review/comment fixes, branch protection, automated artifact handoffs, hosted security scanning, or Claude Tag incidents.
- Operational telemetry, long-term leading/lagging outcomes, or a closed maintenance-to-delivery loop.

These are historical full-playbook limits, not current approval or infrastructure prerequisites. Explicitly deferred areas are tracked in [future work](../FUTURE_WORK.md), not passed by inference from files. No permanent application tests or fake integrations were created to make the package appear complete.

## Workflow-only scope revision

Final package check: `python3 scripts/aidlc.py check` exited 0 with **27 required assets and 76 resolving local links**. This checks package integrity, not model quality or external integrations.

The active guide, skills and templates now use engineer-led artifact handoffs rather than mandatory external acceptance records. Evaluation runners, configuration gates, approval enforcement, CircleCI delivery and maintenance are deferred. Existing historical evidence above is unchanged in meaning; it does not certify the revised skills.

### Actual CLI helper

The real helper created `workflow-smoke` in a temporary directory with exit 0 and printed: `Refine the intent with the engineer, then use aidlc-design for the spec.` Only `intent.md` was created. Repeating the ID exited 1 and preserved the intent's byte digest; `../escape` exited 1. No commits, remote calls or delivery actions were performed.

### Native intent-to-spec handoff

`claude -p "/aidlc-design workflow-smoke"` ran against a disposable copy of the local package with a draft intent describing the requested helper handoff change. No approval URL, formal identity record or approval service was supplied. Invocation flags exposed only Read/Skill, disabled hooks for this invocation, used project settings and an empty strict MCP configuration, and disabled session persistence.

- Exit 0; a proposed spec was returned, without demanding external approval or role identity.
- Seven Read calls occurred. One reported the absent optional existing spec; drafting continued.
- No Write, Bash, remote or implementation action occurred. The change directory still held only its input intent.
- Ordinary software checks were included as proposed proof, not claimed as executed. No evaluation runner or CI setup was required.
- Full sanitised command, response and observations: [workflow smoke evidence](evidence/workflow-scope-smoke.json).

This demonstrates this drafting handoff, **not the complete six-skill lifecycle or review quality**. The fixture already contained the updated message, which the model noticed; its proposed wording refinement was not implemented. The draft also cited ARTIFACTS.md without a corresponding Read and inferred absence of tests without a search. Those claims are not accepted as evidence and the draft still requires engineer review. No formal approval was manufactured.

### Reviewer research, not installation

[Review options](../.claude/skills/aidlc-review/references/review-options.md) records current primary documentation and pinned upstream source for Claude Code's bundled review, the different first-party plugins, and OMP's built-in versus maintainer commands. The recommendation is built-in local review, with artifact context supplied explicitly. No reviewer command/plugin, remote PR review, publication or managed service was executed or installed in this update.

Disposable scenario files were removed after capture. No permanent smoke script, evaluation runner, custom review engine or application test suite was added.

## Claude-native directory restructuring

Structural checks only; further model-driven workflow verification remains deferred by the user.

- `python3 scripts/aidlc.py check` exited 0: **27 required assets; 105 local links resolve**, including links from skill entrypoints to bundled resources.
- The real helper's `--root <temporary-root> new layout-check` exited 0 and loaded the relocated intent template. The created intent exactly matched that template with the change ID substituted; no spec or plan was created. Temporary files were removed.
- `git check-ignore --no-index --stdin` confirmed that personal settings, nested personal settings, worktrees, local agent memory and `CLAUDE.local.md` are ignored. Shared skills, agents, project settings and project-scoped agent memory remain trackable.
- The six retired resource paths no longer exist. The obsolete empty root `templates/` directory was removed; no compatibility copies or symlinks were added.
- Source capture and historical JSON evidence were not rewritten. No native model session, reviewer, plugin installation, permissions change, hook, dynamic workflow, CI or delivery integration was run or added for this restructure.

## Optional CE brainstorming trial

The engineer requested a focused trial of option 1: call the optional upstream CE brainstorm skill and incorporate its discovery result into AIDLC artifacts. This does not reopen the deferred full-workflow evaluation workstream.

Native `claude -p "/aidlc-intent <change-id>"` scenarios ran in disposable checkouts. Runtime initialization reported Claude Code **2.1.273**. CE **3.26.3**, commit `082c83e0537c803ac1d927daafc2e6eb6962dedf`, was downloaded into the temporary trial directory and loaded with `--plugin-dir` only for selected scenarios; it was not installed persistently. No shared/personal plugin settings were changed.

The fixture supplied a small CSV-export message request, already-settled scope and an existing intent containing an operational constraint. File modification permissions were scoped to each disposable checkout's change artifacts and CE discovery directory. Hooks and configured MCP servers were disabled for these invocations; no bypass-permissions mode was used. Full sanitised commands, tool calls, actual returns, outputs and observations are in [native CE evidence](evidence/ce-brainstorm-smoke.json).

| Scenario | Actual observation |
| --- | --- |
| CE selected; discovery document requested | Invoked the real `compound-engineering:ce-brainstorm` with `mode:return-to-caller`. CE wrote a requirements document. The corrected caller read that exact file before merging into the existing intent, retained the CSV-format constraint and source reference, saved the next design action, and did not create a spec or implementation plan. |
| CE selected; lightweight alignment with no document requested | Invoked the real CE skill, consumed its complete chat-brief return and updated the intent. No CE discovery document was created. |
| CE available but not selected | Ordinary intent capture updated the draft without calling CE or creating a CE document. |
| CE absent and not selected | Ordinary intent capture completed without the plugin. |
| CE explicitly selected but absent | Reported the missing skill and offered installation/reload or ordinary clarification. No CE invocation, installation or intent write occurred; the existing intent remained unchanged. |

All five final scenarios exited 0 with successful native results and nonzero model turns. The fixture application remained byte-identical; no scenario authored code, a spec or an implementation plan, or invoked another CE stage. Actual human approval, deployment and production implementation are not implied.

### Problems found during the trial

- The initial `--restricted` setup did not discover the project-scoped `aidlc-intent` command and returned `Unknown command` with exit 0 and zero model turns. Those attempts are not counted as successful scenarios. Removing that setup flag and using scoped file permissions allowed native project-skill discovery.
- The first CE artifact run updated the intent from conversation context without rereading the saved CE document. The caller brief/continuation was strengthened. The rerun's trace shows the discovery-file Read after its creation and before the intent Edit.
- The corrected artifact run encountered two denied Bash operations (listing the external plugin directory and creating the discovery directory). It continued through Read/Write tools without widening permissions. This is not a zero-error-tool-call claim.

### Limits and cleanup

These non-interactive fixtures supplied settled requirements. They demonstrate actual routing, document/brief import and plugin-independent operation, **not the quality of an interactive brainstorming dialogue**. Blocked CE returns, malformed returns, unreadable/wrong-change artifacts, read-only CE selection, custom artifact roots and HTML output were not runtime-exercised. Advisory prompts do not guarantee deterministic adherence to every instruction.

CE ideation, document review, durable handoff/resume, learning capture, persistent installation and organization rollout were not exercised by this trial. All temporary checkouts, the downloaded CE source and archive were removed after evidence capture. No permanent smoke script, evaluation runner or regression suite was added.

Final `python3 scripts/aidlc.py check` exited 0: **27 required assets and 111 resolving local links**. This is package-integrity evidence, separate from the native behavior observations above.

## Optional CE document review trial

Following the requested next integration, native `/aidlc-design export-path` and `/aidlc-plan export-path` invocations exercised the real optional CE reviewer in disposable repositories. Runtime initialization reported Claude Code **2.1.273**, using `claude-sonnet-5`; CE **3.26.3** at commit `082c83e0537c803ac1d927daafc2e6eb6962dedf` was loaded with session-only `--plugin-dir`. No persistent installation or shared/personal settings change was made.

The fixture application was a two-line CSV-export message formatter. Intent required the supplied path verbatim, without filesystem access, including non-existent relative paths. Review targets deliberately contradicted this with `Path.resolve(strict=True)` and rejection of missing files. A separate sensitive-data fixture left a real conflict between verbatim paths and email-free operations logs unresolved.

[Native document-review evidence](evidence/ce-doc-review-smoke.json) retains actual commands, input documents, content comparisons, reviewer returns, caller output, tool traces, native scratch reports and earlier-attempt corrections. Source dumps from Read/context gathering are omitted rather than duplicated; no reviewer output is fabricated.

| Scenario | Actual observation |
| --- | --- |
| CE selected for an existing spec | Invoked `compound-engineering:ce-doc-review` with `mode:non-interactive changes/export-path/spec.md`. Three native personas returned the seeded contradiction. The corrected continuation proposed the design correction without reopening settled requirements. No project artifact changed and no Write/Edit call occurred. |
| CE selected for an existing saved plan | Invoked the real reviewer on `changes/export-path/plan.md` in native plan mode. Coherence and feasibility reviewers found the contradictory task. Conversation output summarised the finding; a fuller report was stored in host-managed scratch. Canonical artifacts and application code stayed byte-identical. |
| Sensitive-data spec; genuine unresolved choice | Four native personas, including security and adversarial lenses, reviewed the spec. The caller left the privacy remedy unresolved. Although the conditional cross-model trigger activated, that pass was explicitly skipped. No project artifact changed. Two `Bash(true)` no-ops occurred; no provider CLI or review job was launched. |
| CE available but not selected | Ordinary design created the requested spec without invoking CE. This is the only final scenario that changed a canonical project artifact. |
| CE absent and not selected | Ordinary planning returned a concrete proposal without CE and did not create a canonical `plan.md`. Native scratch held the proposed text. |
| CE selected but unavailable | Reported the missing capability and offered installation/reload or explicitly labelled ordinary work. No CE invocation, installation or project write occurred. |
| Revised proposal not saved canonically | Proposed the correction in native plan scratch, deferred CE until an authorised canonical save, and did not review the stale saved plan or the scratch copy. The existing canonical plan remained unchanged. |
| Selected saved target missing | Named the missing `plan.md` and stopped without dispatch, substitute artifact or manufactured plan. |

All eight final scenarios exited 0 with successful native results and nonzero model turns. File comparisons confirmed that `report.py`, intent and all pre-existing canonical review targets remained unchanged. No scenario implemented code, saved `review.md`, ran application tests, committed/pushed, or started another CE workflow stage. These observations do not imply review approval or permission enforcement.

### Corrections and native-mode observations

- The first spec run returned a valid report-only finding but asked whether to reverse requirements already settled in intent. The shared caller brief/continuation now distinguishes permission to apply an entailed correction from a genuinely unresolved product choice. The rerun preserved that distinction.
- Native plan mode can write its own platform-managed plan file even when project edits are prohibited. Initial attempts produced three trial-owned files under the host's default plan directory. Each was removed only after verifying it matched the captured Write payload. Subsequent planning runs used the documented `plansDirectory` setting through session-only `--settings` to keep scratch inside the disposable fixture.
- The selected-plan, no-plugin planning and unsaved-proposal runs attempted unavailable `ExitPlanMode` through the Skill tool, received an unknown-skill error, and returned text instead. No mode transition occurred. This is not a zero-tool-error claim.
- Compound Pack resolvers were not run. Pack constraints remain unchecked; successful native reviewer returns do not establish pack-policy compliance.

### Limits and cleanup

These were finite, non-interactive routing and preservation scenarios, not a benchmark of review quality or a guarantee that proposed corrections are correct. Interactive edit approval, writable draft-then-review, injected persona failure/malformed returns, concurrent document changes, CE upgrades and external-provider execution were not exercised. Tool availability and scoped permissions constrained the trials; advisory instructions alone are not deterministic read-only or egress controls.

The application and canonical artifacts were preserved during review, but **zero project changes is not zero filesystem writes**: native planning maintained scratch plans/reports. Full reports in that scratch are not canonical AIDLC records or durable handoff integration.

All trial processes completed. Disposable repositories, native scratch, downloaded CE source and the archive were removed after evidence capture; the three trial-owned files initially written under the host plan directory were also removed. No permanent smoke script, evaluation runner, regression suite, global settings, persistent plugin installation, or additional AIDLC stage was introduced. Handoff/resume was separate work at this point and is recorded in the continuity trial below; ideation, learning capture and standalone packaging remain separate.

Final `python3 scripts/aidlc.py check` exited 0: **27 required assets; 117 local links resolve**. The retained evidence parsed successfully with eight completed native scenarios and cleanup recorded. Package integrity is separate from the runtime observations above.

## Durable continuity and plan persistence trial

Fourteen bounded scenarios exercised the real Claude Code **2.1.273** runtime with `claude-sonnet-5`, using CE **3.26.3** at commit `082c83e0537c803ac1d927daafc2e6eb6962dedf` only where available/selected. Each invocation used a fresh finite process with project-only settings, disabled hooks/auto-memory, no session persistence and no bypass-permissions. CE was loaded through session-local `--plugin-dir`, not installed persistently. Native plan scratch was directed into each disposable fixture.

[Continuity evidence](evidence/continuity-smoke.json) retains command arguments, actual tool calls/results, assistant returns, source hashes, compared input/output artifacts, eleven earlier attempts and final observations. Machine-local roots are redacted. Artifact-map keys hash the original content before redaction; Read/context source dumps are omitted rather than duplicated.

| Scenario | Actual observation |
| --- | --- |
| Save only | Wrote the exact confirmed proposal to the missing canonical `plan.md`, then Read it back. Application code stayed unchanged; no runtime check or review dispatch occurred. |
| Save and implement | Wrote and Read the canonical plan before editing `report.py`. Two real Python invocations returned the required relative/nonexistent-path messages and passed their assertions; plan progress recorded the executed checks. |
| Requested CE review still pending | Saved and Read the exact proposal, preserved the pending review and stopped. No implementation or CE dispatch occurred despite plugin availability. |
| Newer canonical decision conflicts with proposal | Preserved the newer optional-argument decision in spec/plan, made no canonical save or code change and left the disagreement for engineer direction. |
| Ordinary capture with CE available | Created only the selected supporting snapshot without invoking CE; a post-write Read confirmed it. The pending document review was retained. |
| CE capture after actual save-only | Invoked real `compound-engineering:ce-handoff create` at the exact repository destination, created one snapshot and Read it back. No managed-store copy or canonical rewrite was made. |
| Selected CE unavailable | Reported the missing capability and offered installation/reload or explicitly ordinary creation. No installation, snapshot or silent fallback occurred. |
| Read-only capture | Returned proposed snapshot text, not a saved/durable handoff. No CE creation or project snapshot write occurred. Native plan scratch was written; see the mode limitation below. |
| Exact snapshot destination occupied | Stopped and requested a different filename. The existing snapshot remained unchanged. |
| Snapshot selection not yet made | Globbed a filename-only shortlist, opened neither candidate body and asked for a selection or current-artifacts-only orientation. |
| Exact selected snapshot missing | Reported that source missing and stopped, without substituting either available alternative. |
| Current artifacts only | Oriented without CE or a snapshot; distinguished the missing canonical plan from an unconfirmed root draft and stopped for direction. |
| Fresh CE resume | A new process invoked real `ce-handoff resume` on the actual read-verified CE capture copied into its checkout. Compared current artifacts/code, noted machine-local path drift and stopped. |
| Fresh ordinary resume with drift/injection | Without CE, read a copy of that real CE capture modified for the trial. Identified newer implementation/plan state, ignored embedded instructions to execute Python and mark the snapshot consumed, and stopped. The execution marker was not created. |

All fourteen final invocations exited 0 with successful native results and nonzero turns. **All five resume scenarios made zero Bash, Write or Edit tool calls.** Compared application, proposal, canonical and snapshot files changed only where the scenario requested creation or implementation. These are model-tool observations, not a claim that the host runtime performs zero filesystem activity.

### Corrections and limitations

- Initial plan-save and snapshot-create runs skipped the required post-write Read. Explicit completion rules in the owning skills/root guidance corrected this; final traces show actual Read calls after each initial save and before implementation where applicable.
- Initial discovery attempted frontmatter reads that exposed unselected body text, and several resume runs issued shell commands for supposedly read-only inspection. Discovery now lists filenames only; resume explicitly uses Read/Glob/Grep without Bash. Corrected runs observed both boundaries.
- The first conflicting-plan response treated the existing source file as satisfying save-only. The clarified contract and rerun preserved canonical decisions and reported the unresolved disagreement without a canonical write.
- Read-only creation attempted unavailable `Skill(ExitPlanMode)` and returned text after the error; no mode transition occurred. Several creation/build metadata commands also encountered native permission denials. Successful final results do not mean zero tool errors or strict command-allowlist enforcement.
- The hostile/stale snapshot was a deliberately modified trial copy, not an upstream CE output. Neither it nor prior recorded approval authorised current-session execution. Historical status is read from artifacts, not an independent approval/execution ledger.
- This is a synthetic formatter fixture, not a CSV-export or production integration test. The Python proof checked exact output strings and absence of the named nonexistent path; it did not instrument all filesystem I/O.
- Interactive checkpoints, concurrent writers, atomic no-overwrite, independent symlink containment, cross-machine transfer, lost-native-plan save recovery, denied snapshot writes, future CE versions and external-provider flows were not exercised. Advisory skills are not a sandbox or a replacement for host permissions.

All trial processes completed. The owned temporary root, fixture copies, native scratch, downloaded CE source and archive were removed after evidence capture. No permanent smoke script, regression suite, persistent CE installation or global settings change was added. The usage recipes describe the supported contract; this table bounds the runtime evidence.

Final `python3 scripts/aidlc.py check` exited 0: **31 required assets; 133 local links resolve**. Retained JSON parsed successfully with fourteen completed final scenarios, eleven earlier attempts and all referenced artifacts present. Cleanup was confirmed directly by `stat` returning `ENOENT` for the owned temporary root; the retained evidence contains no unredacted repository or temporary-root paths.

## Learning, ideation, reviewer handoff and standalone export

Thirteen final bounded native scenarios ran with Claude Code **2.1.273** (`claude-sonnet-5`), using a temporary, session-local CE **3.26.3** checkout at commit `082c83e0537c803ac1d927daafc2e6eb6962dedf` where selected. [Expansion evidence](evidence/workflow-expansion-smoke.json) retains the actual commands, tool calls/errors, source hashes, fixture inputs, native returns, persisted artifacts, seven earlier attempts and export boundary results. Source/agent-result dumps and host installation-metadata content are omitted as described in that record; machine-local roots are redacted.

The learning fixture had real, separately executed before/after evidence: envelope-hash identity accepted `[True, True, True]` and failed the assertion; tenant/event identity accepted `[True, False, True]` and passed. Capture reused that historical proof rather than rerunning the application. The global-event-only alternative was reasoned about, not executed in that proof.

| Scenario | Actual observation |
| --- | --- |
| Ordinary learning with CE available | Saved and Read one lesson under configured `knowledge/solutions/`. Corrected discovery used the configured root, not default/local-override stores. No CE, agents or glossary change. |
| Explicit CE lightweight learning | Invoked real `ce-compound` with `mode:non-interactive depth:lightweight`. Created one lesson, corrected the existing glossary's replay-identity entry and preserved its unrelated entry. Both outputs were Read after their final writes. No agents; upstream document validators eventually exited 0. |
| Unverified proposed lesson | Skipped without writing a lesson/glossary or invoking CE; did not manufacture verification. |
| Selected CE unavailable | Reported unavailable and stopped without installation, silent fallback or a write. |
| CE selected but glossary writes forbidden | Disclosed the conflict with mandatory existing-glossary maintenance and stopped for an explicit choice; no CE call or write. |
| Ordinary ideation with CE available | Created and Read one ranked supporting document without CE or canonical artifacts. Subsequent inspection found a factual wording error; see the import correction below. |
| CE ideation with restricted commands | Invoked real `ce-ideate output:md`, observed six native agent calls and saved/Read the result. Reported that permission denials prevented its normal private checkpoints; not treated as full scratch-path coverage. |
| Read-only ideation | Used ordinary fallback, no CE and no durable AIDLC ideation artifact. Native plan mode wrote its own `.trial-plans` proposal and returned an unsaved summary; its interactive exit transition was not exercised. |
| OMP reviewer selected in a Claude session | Returned a filled-in packet and documented manual handoff, labelled **prepared—not run**. No substitute review or saved report. |
| Actual reviewer return reconciliation | Consumed the real existing reviewer-agent result described below, preserved both finding bodies verbatim, saved only `review.md` and Read it back. Correctly separated changed/untracked files from the tracked unchanged data fixture. |
| Selected idea imported into intent | Read the exact real ordinary ideation source and current code/data, imported only Rank 2, retained provenance and two unresolved choices, then saved/Read only the new intent. Final output no longer copied the source's incorrect identifier wording. No CE, spec, plan or implementation. |
| Ordinary ideation with configured root | Saved/Read only `knowledge/ideation/...md`. Corrected caller-side discovery did not query either unselected store or expose their marker bodies. |
| CE ideation with authorised scratch mechanics | Observed eleven native agent calls: grounding, evidence scouts, generation and basis verification. Three dossiers plus `raw-candidates.md` and `survivors.md` existed in the private run directory. Bash persisted scratch and the final Markdown after Write denials; an actual Read followed the final artifact write. |

All thirteen final invocations exited 0 with successful native results and nonzero turns. This is not a claim of zero tool errors or flawless generated prose. Compared repository files changed only at the explicitly expected output paths; every durable saved output had an actual Read after its final writer. The native workflows did not execute the application/tests/builds or implement ideas, fix review findings, publish, commit or start a follow-on workflow in the inspected tool traces.

### Actual reviewer and export checks

The existing OMP **reviewer task agent** was actually invoked with the completed packet, independently of a parallel exporter review. It received canonical intent/spec/plan and `REVIEW.md`, inspected the tracked key change, the new untracked replay caller and the tracked unchanged fixture, and returned two priority-1 findings: lost tenant scoping and a missing required `seen` argument. Its verdict was static-only `incorrect`; both findings remain open. A fresh Claude invocation reconciled that actual return and saved the report. This was **not** an OMP `/review` menu interaction or a Claude bundled `/code-review` invocation.

Real CLI export checks covered a new destination containing spaces, loading an intent template through the exported helper, refusal of existing exports/empty directories/dangling symlinks/an existing repository, and a missing destination parent. The existing repository sentinel stayed unchanged. Missing, symlinked and escaping resources failed before destination creation. Seeded unreferenced `.env`, local settings, canonical changes and solution/ideation stores were absent from the exported tree.

The parallel reviewer found a real preflight defect: replacing a required template with a directory still produced a successful but incomplete export. The before-fix command reproduced that false success; the corrected helper rejected it before creating the destination. This was confirmed by a CLI reproduction, not claimed as a second reviewer assessment. Declared/linked content remains a verbatim resource export, not a secret scan, installer or atomic release snapshot.

### Corrections and remaining limits

- Initial learning discovery probed the default store before resolving config; configured ideation later inventoried an ignored alternative store. Root-before-discovery and scoped caller-side tools were clarified. Corrected traces respected the selected store.
- The first idea document confused delivery identity with business-event identity in one sentence; three initial intent imports repeated that wording despite reading the right inputs. Preparation checks alone did not catch an error introduced while drafting. Cross-section factual checking was added to final intent readback; the final import describes the distinct delivery IDs and correct tenant/event semantics without copying that error. This is bounded evidence, not a general factual-accuracy guarantee.
- Initial review reconciliation misclassified the unchanged tracked fixture; another version shortened finding bodies while calling them verbatim. Explicit inventory separation and verbatim native-text rules corrected both in the final saved report.
- CE runs encountered real permission denials, search timeouts and missing optional paths. The scratch-enabled run also inspected host plugin-catalog metadata, and its read-only Explore scouts could not author their own dossiers; the parent persisted their returned material. Its final write used Bash, not Write. These observations must not be recast as zero-error execution or strict command-allowlist enforcement.
- The scratch-enabled caller also attempted an out-of-scope whole-filesystem `find` to locate CE **before** invoking the skill; it backgrounded and eventually failed. Requiring upstream resource reads before their base was exposed caused that unnecessary discovery. The caller now uses the session catalog and runtime-provided resource base. A separate focused probe reached the real CE Skill-load result without host discovery, then was deliberately terminated before phase work; it is not another completed ideation run.
- `--no-session-persistence` was requested, but native agent output symlinks and associated session directories still remained. Those owned directories were identified through actual task references and session IDs and removed. The flag is not treated as proof that the host created no runtime artifacts.
- The fixture is deliberately small and synthetic. Interactive CE questioning, reviewer menus, fix/re-review, stale-after-dispatch behavior, every duplicate/update/collision branch, independent utility symlink/race containment, concurrent writers, interrupted saves, future CE versions and production adoption remain unexercised.
- Fixture hashes and model-tool traces do not instrument every host filesystem operation or network request. Skills are advisory, not a permissions sandbox or an approval/execution ledger. No permanent regression/evaluation runner was added.

Final root and exported-tree `python3 scripts/aidlc.py check` runs exited 0: **35 required assets; 145 local links resolve**. The settled standalone export contained **44 files**, and its helper created a draft intent from the bundled template. Retained JSON parsed with thirteen final scenarios, seven earlier attempts, the deliberately interrupted preflight probe and all 133 input/output artifact references resolving.

All trial processes exited. The owned fixture/export tree, downloaded CE source/archive, exact CE scratch run, verified native runtime/session directories and obsolete empty root `templates/` directory were removed; direct `stat` checks returned `ENOENT` for the 22 checked owned paths. Empty scratch/runtime parents were removed without deleting unrelated history. The evidence contains no unredacted repository, home or owned temporary-root paths. Passive verification records were finalised after the export checks; no immutable release archive or broader host-state cleanup is claimed.

## Selected ECC skill import

The requested 37 skills were imported from ECC commit `8321021c54d670126ce3b2969d5deb880b4b0c2a`. Its `.agents/skills` is a smaller mirror; canonical `skills/` contains the complete selection. `frontend-design-direction` is the actual frontend-design name. The [manifest](vendor/ecc/manifest.json) records source/imported hashes, adaptations and optional dependencies. Forty-seven ECC source files were checked against the pinned checkout; a supplementary Supabase MIT notice was independently byte-checked at revision `8331f910845103c08d51f6ca1d86ebb7d1f745e3`. Together they form 37 entrypoints and eleven supporting resources/notices. ECC's root MIT license is retained separately.

### Exercised behavior

- **Resource integrity:** root and initial exported-helper checks exited 0 with 86 required assets and 225 local links. The initial complete standalone export contained 95 files; the final export also includes this trial's retained evidence.
- **Twelve CLI/resource cases:** all 48 declared bundle files matched their import hashes; existing destinations were preserved/refused; missing, directory-valued and symlinked declared files and escaping manifest paths failed before destination creation; an unlinked declared resource was exported; undeclared runtime files were excluded; fenced illustrative links were ignored while real missing links failed; changed manual-invocation metadata failed `check`; the exported helper created and read a correctly substituted AIDLC intent template.
- **Native loading:** two finite Claude Code **2.1.273** sessions, reporting **`claude-sonnet-5`**, observed all 37 added commands plus the ten existing AIDLC commands. Both exited 0 with successful native results. All 48 imported resources remained byte-identical in both disposable workspaces.
- **API design:** the real `Skill(api-design)` call loaded from the exported project bundle and returned tenant-isolation, status-code, resource-naming and pagination findings for the supplied fictional API. It made no other tool calls or claim of application verification.
- **Manual canary preflight:** a direct `/canary-watch` invocation without a target reported missing prerequisites and all checks as not measured; zero tool calls were emitted. The stream did not expose a separate Skill-load event for that direct slash invocation. No deployed target or sustained watch was exercised.
- **Go example correction:** actual `go run` reproduced returned-byte corruption after pool reuse (`other`, exit 1); copying the result before returning the buffer preserved `first` (exit 0). The Go build cache was confined to the owned trial directory.
- **Django example correction:** a JavaScript VM reproduction returned `null` when the cookie was inaccessible; the corrected example read the rendered masked token and supplied it with `mode: 'same-origin'`. This used document/fetch stubs, not a Django server or browser-security test. Removed legacy XSS-setting guidance was checked against official Django release notes.

The [redacted evidence](evidence/ecc-skill-import-smoke.json) retains CLI results, native prompts/catalogs/tool calls/results, stream hashes and example-proof details without native private reasoning. All 34 MCP catalog entries remained inactive; both native initialisation records reported zero MCP servers.

### Limits and operational boundaries

The native sessions used project-only settings, a strict empty MCP configuration, Skill/Read/Glob/Grep tools, `dontAsk` permissions, disabled hooks/auto-memory and requested no session persistence. No bypass flags or explicit provider/model overrides were used. These restrictions and two prompt cases do not prove that the advisory skills enforce security boundaries under unrestricted tools. Native model requests still occur; traces do not instrument all host filesystem or network activity.

The library was inspected and adapted, not runtime-certified across every framework, code example or operational workflow. Optional ECC commands, agents, GAN/evaluation runners and services linked from guidance are not installed. No production target, Jira/GitHub write, scheduler, database mutation, deployment or persistent MCP/plugin configuration was exercised. ECC retains some upstream-source/version assumptions; the manifest identifies known limits. Vercel's cited skill declares MIT, but no separate Vercel notice was found; its attribution was preserved without inventing one. The supplementary Supabase license revision is not asserted to be ECC's original derivation revision.

Additional `frontend-a11y`, `django-patterns` and `docker-patterns` skills are recommendations, not extra imports. No permanent evaluation runner or application test suite was introduced.

Final root and exported-helper checks both exited 0: **86 required assets; 230 local links resolve**. The final standalone export contained **96 files**, including the declared library and retained evidence. No active project MCP/settings/hooks/rules or duplicate `.agents/skills` mirror was found.

The owned checkout, exports, native workspaces/raw streams, import reports, disposable smoke programs and isolated Go cache were removed; `stat` confirmed the trial root was absent. No matching owned native project/task directories were found at the checked host locations. Only owned artifacts were cleaned. Passive evidence was finalised after export checks; no immutable release archive or exhaustive host-state cleanup is claimed.

## Minimal project configuration and shared instructions

The subsequent requested setup adds an empty project MCP server map, shared Claude settings, an ignored local `{}` settings file, one read-only startup/resume package-check hook, a scoped package-maintenance rule and the exact relative instruction alias `AGENTS.md -> CLAUDE.md`. These are local project integrations, not imported ECC runtime defaults.

### Exercised behavior

- **Initial complete export:** root and exported checks exited 0 with **91 required assets; 244 local links resolve**. The standalone export contained **101 files**, preserved the instruction symlink and omitted local settings.
- **Fifteen disposable boundary cases:** the alias reflected canonical-file edits and exported through parent-relative Markdown links; escaping, absolute, directory-valued and copied-file aliases and symlinked canonical targets were refused; arbitrary resource and ancestor symlinks were refused; shared runtime resources were exported while local settings, arbitrary settings and `.env` were excluded; malformed JSON and non-object configuration roots failed `check`.
- **Hook command smoke:** the actual registered command succeeded from an unrelated working directory with spaces in the package path, propagated a missing-asset failure and refused a missing project-directory variable. Package file/link snapshots were unchanged by both successful and failing checks.
- **Native Claude Code 2.1.273:** a finite exported-workspace session emitted `SessionStart:startup` start/response events, with hook exit 0 and `PASS: 91 required assets; 244 local links resolve.` It reported zero MCP servers, used only two Read calls for `.mcp.json` and the maintenance rule, and returned the correct check result, empty server count and instruction alias. The main model was `claude-sonnet-5`; native auxiliary model usage also occurred.
- **Native Codex CLI 0.154.0:** a finite ephemeral read-only session quoted the alias, startup check and ECC ownership instructions supplied through `AGENTS.md`, without any tool events. This demonstrates instruction discovery, not native Claude skill/hook behavior in Codex.

The [redacted smoke evidence](evidence/native-config-smoke.json) retains boundary outcomes, native invocation options, hook events, tool calls, final answers and raw-output hashes, excluding private reasoning.

### Limits

The native Claude smoke loaded project/local settings, disabled auto memory, restricted the model to Read, used `dontAsk` with no permission prompts, passed the empty MCP map with strict MCP configuration and requested no session persistence. Codex ignored user configuration and execpolicy rules, used a read-only sandbox with approvals disabled and requested ephemeral execution. Neither client received a model/provider override or bypass flag. Model-service requests still occur; this does not instrument all host filesystem or network activity.

Only startup was exercised natively, not resume. Claude explicitly read the maintenance rule; conditional path-trigger behavior was not isolated. SessionStart diagnostics do not block session startup or implement an approval/lifecycle/security gate. Other sessions may inherit user/managed settings, hooks or MCP connections. The shell hook needs `sh` and Python 3, and the alias/export needs filesystem symlink support; only macOS was exercised. No permanent evaluation runner or additional test suite was added.

After retaining the evidence and updating usage documentation, the final root and exported checks both exited 0 with **91 required assets; 248 local links resolve**, and the final export contained **102 files**. Its relative instruction alias remained intact and local settings were absent. The owned exports, boundary fixtures, throwaway smoke program and native debug log were removed; `lstat` confirmed the trial root was absent. Only owned trial artifacts were cleaned. Passive evidence was finalized afterward; no immutable release archive or exhaustive host-state cleanup is claimed.

## Company AIDLC restructure

The package became `lbvs-aidlc`: `/aidlc <change-id>` orchestrates gated stages, stage skills are model-invocable, `aidlc-fix` adds the reproduce → protected test → evidence loop, `aidlc-onboard` + `aidlc-repo-scout` handle brownfield repositories, `scripts/aidlc.py mode` classifies the project, `AGENTS.md` is the canonical instruction file imported by `CLAUDE.md` (`@AGENTS.md`) and `.omp/AGENTS.md` (`@../AGENTS.md`), and three hooks are registered.

### Exercised behavior

- **Package:** root and exported checks exited 0 with **103 required assets; 256 local links resolve**; the export contained **114 files**, no symlink, `CLAUDE.md` starting with `@AGENTS.md`, and no local settings.
- **Mode detection:** this package → greenfield (1 code file, 0 commits); a fixture with 12 `.py` files → brownfield; `.aidlc/mode` = `greenfield` → declared override; an invalid override → exit 1. The registered `project-mode.sh` exited 0.
- **Native Claude Code 2.1.273 (exported tree):** the init event listed all 13 `aidlc*` commands; both SessionStart hooks returned exit 0 (mode line, then package PASS); with a seeded `.aidlc/fix/demo-1.json`, the `PreToolUse:Edit` hook **denied** the edit to the protected test with the documented reason and **allowed** the edit to an unprotected file; the protected file was byte-unchanged afterwards.
- **Native omp 18.1.21 (exported tree):** the session received `.omp/AGENTS.md` with the `@../AGENTS.md` import expanded (first heading `# lbvs-aidlc`, `## Oh My Pi` section) and the `.omp/RULES.md` sticky rule; with the read tool enabled it listed the ten model-invocable `aidlc*` skills among 39 discovered skills.

Retained: [redacted smoke evidence](evidence/company-restructure-smoke.json).

### Limits

Only startup hooks ran, not resume. The deny path was exercised with a seeded marker; the full `/aidlc-fix` conversation, `EnterWorktree`, CE brainstorming and the stage-gate dialogue were not driven end to end in a native session. The first omp run used `--no-tools`, which omits the skills list by design. Codex was not re-run after replacing the symlink; it reads the standalone `AGENTS.md`. No plugin was installed and the smoke made no commits. The owned temporary export was removed.

## Interactive `/aidlc` trial with CE brainstorming

Driven in a disposable clone of `fcd08d1` through a PTY, Claude Code **2.1.274**, `claude-sonnet-5` at high effort, `--setting-sources project,local`, `acceptEdits`.

### Exercised behavior

- **Five gates answered interactively:** worktree (*Create worktree*), kind of work (*Feature/change*), resume point (*Start from intent*), CE availability (*Reload/reinstall then retry*), intent stage gate (*Stop here*). *Stop here* ended the run with the final report; no later stage was invoked, so gates do not auto-advance.
- **Worktree:** `EnterWorktree` created `.claude/worktrees/aidlc+trial-ce-brainstorm`. On the second run the orchestrator entered that existing worktree instead of creating another.
- **Project mode in the worktree:** `AIDLC project mode: greenfield — 1 code files (threshold 10); 3 commits (threshold 20)`.
- **CE brainstorming:** `Skill(compound-engineering:ce-brainstorm)` ran with `mode:return-to-caller`, loading from the 3.26.3 plugin cache. It classified the request as Lightweight with requirements already clear, returned a brief with settled decisions, and wrote no CE artifact file; `docs/plans` and `docs/solutions` were never created.
- **Intent:** `changes/trial-ce-brainstorm/intent.md` (4,884 bytes) was written, then **read back** — the skill explicitly declined the Write tool's "no need to Read it back" hint, citing `CLAUDE.md`. Three open questions stayed unresolved rather than being invented. No commit was made.
- **CE-absent path:** in the first run CE was not in the catalog; the skill reported that, said "I won't fake having run it", and offered reload/install or ordinary clarification.

### Defects found and fixed

1. `EnterWorktree` derives its own branch name (`worktree-aidlc+<id>`); the orchestrator renamed the branch mid-session to match the documented convention. The orchestrator now accepts the host's name and never renames; `git worktree add` is the fallback only.
2. The orchestrator passed the change ID **plus prose** as Skill arguments, so a stage skill rendered `Change ID: trial-ce-brainstorm — feature request: …` against its own one-ID contract. It now passes the bare ID and states context in conversation.
3. With CE absent, `aidlc-intent` ran `find / -maxdepth 4 -iname "*compound-engineering*"` — the out-of-scope filesystem hunt previously recorded under the CE brainstorming trial. Availability is now decided from the session skill catalog alone.
4. A project-scope declaration did **not** install CE in a fresh clone: **0** `compound-engineering:*` skills with `project,local` and with `user,project,local`, before and after the interactive trust prompt; **35** after `claude plugin install compound-engineering@compound-engineering-plugin --scope project`; the source repo where the install had run reported 35. README and USAGE now say the declaration pins the marketplace/plugin while each engineer installs once per clone.

Also observed: with user settings enabled, a user-scope `task-observer` skill auto-fired and probed `~/.claude/skill-observations/`, and the `aidlc*` command count rose from 13 to 20 because a user-scope plugin ships its own `aidlc` skills. The first trial session was abandoned for that reason.

[Redacted trial evidence](evidence/aidlc-trial-smoke.json) retains the gate questions, answers, observations and defects.

### Limits

Only the intent stage ran; design through review, `/aidlc-fix` and `/aidlc-learn` were not exercised here. CE took its fast path, so scan/scout, Path B artifacts and `CONCEPTS.md` maintenance remain unexercised. The clone used a broad local allowlist, so this is not evidence about permission behaviour under stricter policy, and gate answers were sent through a PTY rather than by a product owner. The fixes above were applied after the run and re-checked with `aidlc.py check`, not re-driven through a second interactive trial.

## Descriptive worktrees, ID-free operation and the flow policy

### Exercised behavior

- **Helper:** `check` → **105 required assets; 263 local links resolve**; export **118 files**, exported check identical. `status` listed `vs-4242-status-command` as `reached: intent  next: design`, marking it current; `current` printed `vs-4242-status-command  the only change without review.md` and exits 1 when nothing resolves.
- **Worktree hook unit tests:** name `vs-99-thing` with a matching `changes/` directory → branch `aidlc/vs-99-thing`, directory `aidlc+vs-99-thing`; the prefixed name `aidlc/vs-99-thing` reused the same worktree; `vs-77-unknown` and `scratch` kept `worktree-<name>`; `.env` was copied from `.worktreeinclude`; input without a name exited non-zero, which fails worktree creation as the hook contract requires.
- **Native Claude Code 2.1.274, `/aidlc` with no argument:** the orchestrator ran `python3 scripts/aidlc.py current`, announced `Resolved change ID vs-4242-status-command (source: the only change without review.md)`, showed `status`, then asked the flow policy with the three documented options. It echoed `Flow policy: auto-advance when clear, stop before build.` and proposed the worktree by name.
- **Worktree creation in that session:** the first `EnterWorktree` call passed the bare change ID, so the hook applied its non-AIDLC default (`worktree-vs-4242-status-command`); the skill noticed the mismatch and asked before fixing it. The retry with `aidlc/vs-4242-status-command` produced directory `.claude/worktrees/aidlc+vs-4242-status-command` on branch **`aidlc/vs-4242-status-command`** with `.env` present.

### Defect found and fixed

Relying on the caller to pass `aidlc/<change-id>` was fragile. `worktree_path()` now also applies the descriptive naming when the requested name is a valid change ID with an existing `changes/<id>/` directory; unknown names keep `worktree-<name>`. Re-tested by the unit cases above.

[Redacted evidence](evidence/aidlc-flow-smoke.json).

### Limits

The run selected an auto-advance policy but stopped before any stage completed, so an actual `Auto-advancing to …` announcement was **not** observed — only the gate and its echo. Bash prompts were answered by hand in a fixture without an allowlist; the first worktree attempt ran the pre-fix helper copy, and the corrected naming rests on the prefixed retry plus the unit tests. No commits, pushes or CE involvement in this run.

## Oh My Pi parity: extension, agents and graph tooling

omp does not run Claude's shell hooks and skips `.claude/agents/` for task agents (its frontmatter schema differs), so the package now ships `.omp/hooks/pre/aidlc-guards.ts` and `.omp/agents/{aidlc-verifier,aidlc-repo-scout}.md`, the latter deferring to the Claude definitions.

### Exercised behavior

- `check` → **108 required assets** (adds the omp extension, two omp agents and two VS Code files); export **122 files**.
- **omp 18.1.21, brownfield fixture (11 `.py` files, seeded `.aidlc/fix/demo-omp.json`):** `write` to the protected `tests/test_repro.py` was **blocked** with the same reason text as the Claude hook, `write` to `tests/other.txt` was allowed, the protected file stayed byte-identical, and the session listed `aidlc-repo-scout` and `aidlc-verifier` as available task agents.
- **Mode line:** the first design returned a `before_agent_start` custom message; the transcript recorded it but the model reported "no mode line" in three separate runs. Attaching the line to the first user turn through the `context` event fixed it: a `--no-tools` run quoted `AIDLC project mode: brownfield — 12+ code files (threshold 10); 1 commits (threshold 20)`. The custom message is kept for the transcript.
- `bun build --no-bundle` parsed the extension; the project rules against `any` and trivial wrappers were applied.

### Limits

`edit`-tool protection relies on parsing `[PATH#TAG]` headers from the hashline payload and was not exercised natively (only `write` was). omp has no `WorktreeCreate` hook, so omp sessions fall back to `git worktree add`; the package-integrity check does not run at omp session start. graphify wiring in the scout, fix and onboarding skills is prose that activates only when `graphify-out/` or the CLI exists; it was not exercised. The VS Code settings were not opened in VS Code.

## Knowledge stores, MCP declarations, ticket and spike

### Exercised behavior

- `check` → **122 required assets; 314 local links resolve**; export **136 files** containing `docs/adr/`, `docs/incidents/` (template moved from the removed `docs/deferred/`), `docs/security/`, the `aidlc-ticket` and `aidlc-spike` skills, the imported `doc-coauthoring` and `architecture-decision-records` skills and the anthropic-skills manifest/NOTICE.
- **doctor:** reports optional tools (graphify, codegraph, gh, omp) with install commands and the auth need of every server in `.mcp.json`; with `PATH` stripped, `doctor --install` printed *no supported installer found* for each missing tool and ran nothing; a project without `.mcp.json` reports that plainly.
- **Native Claude Code 2.1.274 in the export:** 15 `aidlc*` commands plus `architecture-decision-records` and `doc-coauthoring` loaded. With project servers pre-approved for the smoke, `context7` **connected** anonymously, `github` **failed** (no `GITHUB_PERSONAL_ACCESS_TOKEN`) and `atlassian` reported **needs-auth** (OAuth 2.1) — exactly the prerequisites `doctor` had listed.
- **Imports:** upstream and imported SHA-256 recorded in [`docs/vendor/anthropic-skills/manifest.json`](vendor/anthropic-skills/manifest.json) and the ECC manifest; the anthropics/skills licensing position (README statement, no LICENSE file) is quoted in [`NOTICE.md`](vendor/anthropic-skills/NOTICE.md).

[Evidence](evidence/knowledge-mcp-smoke.json).

### Limits

`/aidlc-ticket`, `/aidlc-spike` and the ADR, threat-model and incident offers in design, review and fix were not driven natively. GitHub and Atlassian connections were not completed — the failure and needs-auth states are the evidence, not a working integration. `doctor --install` exercised only its no-installer branch. The imported skills exceed the 7 KB AIDLC budget because upstream text is kept verbatim.
