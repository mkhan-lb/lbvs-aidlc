# Future work

Status: explicitly deferred by the user on 16 September 2026. None of the work below is a prerequisite for the current engineer workflow.

The active scope is in [GOALS.md](GOALS.md) and [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md). The full Anthropic playbook remains in [source coverage](docs/COVERAGE.md); deferral is a deliberate scope decision, not an assertion that these capabilities are implemented.

## F1 — Evaluation runner

**Goal:** assess the AI workflow against representative tasks when we choose to invest in this capability.

**Later steps:** select genuine tasks and accepted outcomes; define isolated execution and checks; run cases against agent/model/skill versions; retain results and costs; connect incident-derived cases when maintenance exists.

Do not build a runner or collect a 20–50-task corpus now. Normal tests for the software change remain in the active workflow. Each `/aidlc-fix` evidence file carries an **eval seed suggestion** under Regression protection so that incidents already point at future eval cases.

The optional imported `eval-harness` and `gan-style-harness` skills provide guidance only. Their presence does not install a runner, create a corpus, establish gates or resume this workstream.

## F2 — Configuration-regression gates

**Goal:** detect and prevent harmful changes to AI configuration using an established evaluation process.

**Later steps:** decide which changes trigger evaluation; define meaningful thresholds and review responsibility; connect results to the chosen CI and merge process; exercise a real regressing configuration.

Do not build or require this gate now. It depends on a useful evaluation process, not merely a settings-file diff.

## F3 — Approval enforcement and managed controls

**Goal:** enforce the required organisational boundaries when that becomes part of the implementation scope.

**Later steps:** identify actual approval authorities; bind decisions to the relevant changes; integrate the existing review/release systems; implement scoped hooks or managed controls where needed; test missing, rejected, stale and bypassed decisions.

No approval service, external-signoff validation, signed receipt system, custom guardrail framework or managed-settings rollout is being built now. The three bundled hooks (`check-package.sh`, `project-mode.sh`, `protect-tests.sh`) are loop guardrails for package integrity, mode context and failing-test protection—not approval controls. Ordinary engineer confirmation at the stage gates, existing repository rules and tool permissions still apply. Deferral does not authorise auto-approval or auto-merge.

## F4 — Delivery integration through CircleCI

**Goal:** connect reviewed work to the company's CI/CD using **CircleCI**, not a new GitHub Actions delivery assumption.

**Later steps:** inspect the existing CircleCI configuration; identify build/test/artifact and delivery jobs; define permitted AI assistance such as failure diagnosis or release-note preparation; connect credentials and environment access through the existing platform; exercise delivery/status/rollback in the appropriate environment.

Do not create delivery workflows or request CircleCI credentials now. GitHub PR review, if selected, is a code-review surface and does not imply GitHub Actions as the delivery platform.

## F5 — Maintenance and operational feedback

**Goal:** connect operational findings back to the workflow after delivery and operational scope are agreed.

**Later steps:** choose real signals and owners; establish deterministic triggers and response scope; investigate findings; create new intent or reviewed fixes; consider hosted scans and incident-channel tooling; verify outcomes and preserve lessons.

Monitoring, scheduled security scans, Claude Tag and other incident integrations remain deferred. The existing incident template and source research are retained for later use, not active prerequisites.

Likewise, imported `canary-watch` and `production-audit` guidance does not enable monitoring, schedule jobs, grant production access or perform incident/notification integration.

## F6 — Unattended artifact handoffs

**Goal:** automate transitions once the manual workflow is useful and understood.

**Later steps:** choose explicit trigger conditions; define which revisions and instructions travel between stages; integrate existing execution and review mechanisms; handle failed, superseded and ambiguous inputs; prove the real integration.

For now, `/aidlc` runs the stages but a user answers every gate; "Proceed" is never inferred. No event bus, polling service or custom orchestration platform is needed.

## F7 — Company adoption and spec-driven additions

**Goal:** adapt the working generic flow to company conventions and evaluate useful additions from [Kiro specs](https://kiro.dev/docs/specs/).

**Later steps:** add actual architecture and engineering context; clarify existing ownership and sources of truth; trial the workflow on ordinary work; provide examples/training; compare Kiro requirements/design/tasks with the existing intent/spec/plan chain; adopt additions only where they reduce ambiguity or rework without duplicating records.

**Marketplace distribution** of this package (a `.claude-plugin/marketplace.json` repository pinned through `extraKnownMarketplaces`/`enabledPlugins` or managed settings) is tracked on a **separate branch**; the supported distribution today is the repo-template export. `docs/PLUGINS.md` recommends bundled skills and official plugins per stage but installs nothing.

Using Oh My Pi's existing review capability is being researched now; adopting it as a company-wide coding platform or porting the whole workflow to it is not implied.

## F8 — Non-technical intent route at scale

**Goal:** let originators without Claude Code contribute intent.

**Now:** non-technical originators use optional Compound Engineering brainstorming (`ce-brainstorm`) with an engineer, and the brief becomes the intent source. **Later:** evaluate the playbook's claude.ai/Cowork route—a shared, version-controlled intent home written through a GitHub connector—and decide who may write to it. Caveman remains opt-in at user scope for engineers only and is never recommended for non-technical readers.

## Re-entry rule

Resume a deferred area only when it is explicitly selected. State the goal, dependencies, implementation work and verification required at that time. Do not label deferred work as a blocker for drafting, planning, local implementation or review today.
