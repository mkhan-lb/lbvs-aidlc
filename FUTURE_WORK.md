# Future work

Status: explicitly deferred by the user on 16 September 2026. None of the work below is a prerequisite for the current engineer workflow.

The active scope is in [GOALS.md](GOALS.md) and [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md). The full Anthropic playbook remains in [source coverage](docs/COVERAGE.md); deferral is a deliberate scope decision, not an assertion that these capabilities are implemented.

## F1 — Evaluation runner

**Goal:** assess the AI workflow against representative tasks when we choose to invest in this capability.

**Later steps:** select genuine tasks and accepted outcomes; define isolated execution and checks; run cases against agent/model/skill versions; retain results and costs; connect incident-derived cases when maintenance exists.

Do not build a runner or collect a 20–50-task corpus now. Normal tests for the software change remain in the active workflow. Each `/lbvs-aidlc-fix` evidence file carries an **eval seed suggestion** under Regression protection, and a confirmed `docs/incidents/` record links back to it, so that incidents already point at future eval cases.

The optional imported `eval-harness` and `gan-style-harness` skills provide guidance only. Their presence does not install a runner, create a corpus, establish gates or resume this workstream.

## F2 — Configuration-regression gates

**Goal:** detect and prevent harmful changes to AI configuration using an established evaluation process.

**Later steps:** decide which changes trigger evaluation; define meaningful thresholds and review responsibility; connect results to the chosen CI and merge process; exercise a real regressing configuration.

Do not build or require this gate now. It depends on a useful evaluation process, not merely a settings-file diff.

## F3 — Approval enforcement and managed controls

**Goal:** enforce the required organisational boundaries when that becomes part of the implementation scope.

**Later steps:** identify actual approval authorities; bind decisions to the relevant changes; integrate the existing review/release systems; implement scoped hooks or managed controls where needed; test missing, rejected, stale and bypassed decisions.

No approval service, external-signoff validation, signed receipt system, custom guardrail framework or managed-settings rollout is being built now. The four bundled hooks (`check-package.sh`, `project-mode.sh`, `protect-tests.sh`, `worktree-create.sh`) are loop guardrails for package integrity, mode context, failing-test protection and worktree naming—not approval controls. Ordinary engineer confirmation at the stage gates, the review loop's three-cycle stop, `/lbvs-aidlc-ship`'s always-asked commit/push/PR question, existing repository rules and tool permissions still apply. Deferral does not authorise auto-approval or auto-merge; `/lbvs-aidlc-ship` never merges, approves, enables auto-merge or edits branch protection.

## F4 — Delivery integration through CircleCI

**Goal:** connect reviewed work to the company's CI/CD using **CircleCI** through the `lb-pipelines/app-delivery-kit-vs@1` orb, not a new GitHub Actions delivery assumption.

**Now:** `/lbvs-aidlc-ship` takes a change whose review pass is clean to an open PR — commit with the Jira-key title, push `aidlc/<id>`, `gh pr create` from the bundled body template — and stops there. [`docs/platform/README.md`](docs/platform/README.md) points at the two internal repositories (`Logicbroker/app-template`, `Logicbroker/app-delivery-kit`; both need an authenticated `gh api`, raw links 404) and each adopting service records its own facts in `docs/platform/platform.md`, which design and plan read so that deployment, observability and promotion changes are expressed as orb values/pipeline config rather than hand-rolled infrastructure.

**Later steps:** inspect the existing CircleCI configuration; identify build/test/artifact and delivery jobs; define permitted AI assistance such as failure diagnosis or release-note preparation; connect credentials and environment access through the existing platform; exercise delivery/status/rollback in the appropriate environment.

Do not run pipelines, promote images, approve environment holds or request CircleCI credentials from the skills now; the PR is where the agent's part ends and a human's begins. GitHub PR review, if selected, is a code-review surface and does not imply GitHub Actions as the delivery platform.

## F5 — Maintenance and operational feedback

**Goal:** connect operational findings back to the workflow after delivery and operational scope are agreed.

**Now:** the durable records exist as plain Markdown that an engineer confirms — `docs/incidents/` (offered by `/lbvs-aidlc-fix` when a defect arrived through an alert or incident link), `docs/security/threat-models/` and `docs/security/findings/` (offered by `lbvs-aidlc-design` and `/lbvs-aidlc-fix`, or saved from a `/security-review` on request; the STRIDE draft comes from the read-only `lbvs-aidlc-threat-modeler` agent), `docs/adr/`, `docs/references/` (Context7 lookups that settled real questions) and `docs/solutions/` (lessons with confidence and observation counts). Nothing writes into them automatically.

**Later steps:** choose real signals and owners; establish deterministic triggers and response scope; investigate findings; create new intent or reviewed fixes; consider hosted scans and incident-channel tooling that would populate those stores; verify outcomes and preserve lessons.

Monitoring, scheduled hosted security scans, Claude Tag and other incident integrations remain deferred. The incident template now lives at `docs/incidents/template.md` as an active knowledge-store template, not a deferred artifact; the source research is retained for later use, not as an active prerequisite.

Likewise, imported `canary-watch` and `production-audit` guidance does not enable monitoring, schedule jobs, grant production access or perform incident/notification integration.

## F6 — Unattended artifact handoffs

**Goal:** automate transitions once the manual workflow is useful and understood.

**Later steps:** choose explicit trigger conditions; define which revisions and instructions travel between stages; integrate existing execution and review mechanisms; handle failed, superseded and ambiguous inputs; prove the real integration.

For now, `/lbvs-aidlc` runs the stages but a user answers every gate; "Proceed" is never inferred. No event bus, polling service or custom orchestration platform is needed.

## F7 — Company adoption and spec-driven additions

**Goal:** adapt the working generic flow to company conventions and evaluate useful additions from [Kiro specs](https://kiro.dev/docs/specs/).

**Adopted — Kiro-derived traceability (ideas, not tooling):** the comparison of Kiro's requirements/design/tasks with the intent/spec/plan chain is done and five additions are in the skills and templates, credited to [kiro.dev/docs/specs](https://kiro.dev/docs/specs/): EARS acceptance criteria with stable IDs `R<n>.<m>` in `spec.md` (`WHEN … THE <system> SHALL …`, `IF … THEN …`, `WHILE …`, ubiquitous, and `SHALL CONTINUE TO` for bug fixes); `_Requirements: R…_` trace lines and `depends on:` on numbered `plan.md` tasks, with a coverage check that every R-ID has a task; one task at a time in build, ticked only after its check passes; a per-requirement verification table (`R-ID | check | observed result | not run`); and the Current / Expected / Unchanged triad in `evidence.md`. Not adopted: Kiro's run-all task waves, property-based test generation and spec hooks — tooling-bound, or new enforcement outside the current scope. See [traceability](docs/WORKFLOW.md#traceability-from-requirement-to-check).

**Adopted — conventions defaults:** `templates/conventions/` and `python3 scripts/aidlc.py conventions [--apply]` give a greenfield repository a starting point and leave a brownfield repository's own tooling untouched.

**Later steps:** add actual architecture and engineering context beyond the `docs/platform/` pointers; clarify existing ownership and sources of truth; trial the workflow on ordinary work; provide examples/training.

**Marketplace distribution** of this package (a `.claude-plugin/marketplace.json` repository pinned through `extraKnownMarketplaces`/`enabledPlugins` or managed settings) is tracked on a **separate branch**; the supported distribution today is the repo-template export. `docs/PLUGINS.md` recommends bundled skills and official plugins per stage but installs nothing.

Using Oh My Pi's existing review capability is being researched now; adopting it as a company-wide coding platform or porting the whole workflow to it is not implied. Likewise, ECC's `continuous-learning-v2` contributed only its lesson schema (confidence ladder, observation count, scope, promotion threshold); its Pre/PostToolUse observation hooks, background Haiku observer daemon and observation log were deliberately not imported and are not queued here — the observer is off by default upstream, the model calls run in the background on the engineer's account, and the log is a telemetry-like record of tool inputs and outputs outside the repository.

## F8 — Non-technical intent route at scale

**Goal:** let originators without Claude Code contribute intent.

**Now:** non-technical originators use optional Compound Engineering brainstorming (`ce-brainstorm`) with an engineer, and the brief becomes the intent source. **Later:** evaluate the playbook's claude.ai/Cowork route—a shared, version-controlled intent home written through a GitHub connector—and decide who may write to it. Caveman remains opt-in at user scope for engineers only and is never recommended for non-technical readers.

## Re-entry rule

Resume a deferred area only when it is explicitly selected. State the goal, dependencies, implementation work and verification required at that time. Do not label deferred work as a blocker for drafting, planning, local implementation or review today.
