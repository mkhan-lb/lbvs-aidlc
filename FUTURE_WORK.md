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

**Now — advisory checks, not gates:** the read-only `lbvs-aidlc-design-reviewer` returns READY / NOT READY before the design gate, `lbvs-aidlc-test-critic` critiques tests when verify offers it, and `lbvs-aidlc-conventions-checker` reruns the repository's documented commands and compares the diff with `docs/repo-profile.md` before `/lbvs-aidlc-ship` asks its question ([pre-PR check](docs/WORKFLOW.md#pre-pr-conventions-check)). Their findings change the shape of a question the engineer answers; none approves, blocks or enforces.

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

**Adopted — repository context and knowledge stores:** the committed `docs/repo-profile.md` (with `python3 scripts/aidlc.py profile` freshness), the company glossaries under `docs/glossary/`, the `docs/playbooks/` procedure store and the `docs/adr/` decision store now hold the architecture and engineering context, ownership and sources of truth that stages read before scouting ([repository context](docs/WORKFLOW.md#repository-context), [knowledge stores](docs/WORKFLOW.md#knowledge-stores)). Filling them for each adopting repository is ordinary `/lbvs-aidlc-onboard` and review work, not deferred infrastructure.

**Adopted — marketplace distribution:** the committed `plugins/lbvs-aidlc/` tree on `main` publishes this package as a Claude Code plugin (`claude plugin marketplace add mkhan-lb/lbvs-aidlc`; the former `plugin-marketplace` branch was merged 2026-09-18), pinnable per repository through `extraKnownMarketplaces`/`enabledPlugins` or fleet-wide through managed settings ([distribution](docs/REFERENCE.md#distribution)); the repo-template export remains the primary route. `docs/PLUGINS.md` recommends bundled skills and official plugins per stage but installs nothing.

**Later steps:** trial the workflow on ordinary work ([next trial](IMPLEMENTATION_PLAN.md#next-trial)); provide examples/training; decide company-wide pinning of the recommended plugins.

Using Oh My Pi's existing review capability is being researched now; adopting it as a company-wide coding platform or porting the whole workflow to it is not implied. Likewise, ECC's `continuous-learning-v2` contributed its lesson schema (confidence ladder, observation count, scope, promotion threshold) and is now vendored complete at the pin — Pre/PostToolUse observation hooks, background Haiku observer scripts, instinct CLI — but off by default: this package registers no hook and writes no settings; `/lbvs-aidlc-init` reports whether the separate `lbvs-aidlc-observer@lbvs-aidlc` plugin (`defaultEnabled: false`) is enabled and prints the enable command, nothing more. The engineer who enables it accepts that the model calls run in the background on their account and that the observation log records tool inputs and outputs under `~/.local/share/ecc-homunculus/`, outside the repository. It does not replace `/lbvs-aidlc-learn`; instincts stay personal until promoted through review.

## F8 — Non-technical intent route at scale

**Goal:** let originators without Claude Code contribute intent.

**Now:** non-technical originators use optional Compound Engineering brainstorming (`ce-brainstorm`) with an engineer, and the brief becomes the intent source. **Later:** evaluate the playbook's claude.ai/Cowork route—a shared, version-controlled intent home written through a GitHub connector—and decide who may write to it. Caveman remains opt-in at user scope for engineers only and is never recommended for non-technical readers.

## F9 — Host-native stage dispatch in Oh My Pi (resolved 2026-09-17)

**Observed:** during the SO2-1386 ticket-intake trial on 17 September 2026, intake saved and read back the intent in the-edge, but the subsequent orchestrator stopped because it required a literal `Skill` tool and explicitly prohibited continuing without it. The Oh My Pi session exposed the stage skills through `skill://` reads, not a `Skill` invocation tool.

**Resolution:** the contract now names a host-neutral [skill route](docs/WORKFLOW.md#skill-route) — the Skill tool in Claude Code; `/skill:<name> <id>` or a `skill://<name>` read in Oh My Pi — and every stage skill invokes the next one "via the skill route". A skill absent from the host catalogue is unavailable; one exposed through another route is not. The same trial surfaced the fixes recorded alongside: the [content boundary](docs/ARTIFACTS.md#content-boundary) and `lint-artifacts`, the single [reproduction commit](docs/WORKFLOW.md#reproduction-commit), the PR back-link commit, the protection probe and per-repository marker lookup in both hooks, source-identity recording for container runtimes, the lesson-store rule and tier recording for reviewers without an effort argument.

**Still open from the trial:** the OMP session's `AIDLC project mode:` line describes the session root, not a sibling target repository; a stage that targets another checkout should compute the mode for that root (`python3 scripts/aidlc.py --root <target> mode`). Not yet verified end to end: ticket → orchestrator → stage handover in Oh My Pi with a target repository different from the package checkout, now that the route is defined.

## F10 — Trial artifacts already shipped

**Observed:** the SO2-1386 change in `Virtualstock/the-edge` ([PR #9357](https://github.com/Virtualstock/the-edge/pull/9357)) was shipped before the content boundary existed. Its `changes/so2-1386-product-patch-500/` files carry machine paths, session references and workflow narrative (33 `lint-artifacts` hits), and a lesson was written to a new `docs/solutions/` tree although the-edge keeps its knowledge in `.claude/knowledge/`.

**Deferred by the engineer (2026-09-17):** leave the PR as the record of the first trial; clean it in a follow-up commit on the same branch once the templates and lint have landed here. Whether the Docker worktree/container fact belongs in the-edge's `.claude/knowledge/operations.md` or only in this package is undecided.

## F11 — Plugin engine and thin repository scaffold (branch `plugin-engine`)

**Decided 2026-09-18 (option A).** Claude Code is the primary host, so the AIDLC engine moves out of adopting repositories and into versioned plugins served from this repository's `.claude-plugin/marketplace.json`, which Oh My Pi reads as well: `lbvs-aidlc` (17 skills, six agents, `hooks/hooks.json`, `bin/aidlc`, shared docs), `lbvs-ecc` (the 38 reference skills, opt-in per repository) and `lbvs-aidlc-observer` (continuous-learning-v2, `defaultEnabled: false`). `install` shrinks to a scaffold of repository state — `REVIEW.md`, knowledge-store seeds where no store exists, `docs/repo-profile.md` through onboarding, `.aidlc/manifest.json`, `changes/`, `.gitignore` lines and the `.claude/settings.json` plugin declaration — and `package` retires. Hooks carry the rules that can be mechanical: a PR guard that asks before `gh pr create|merge` or a force-push (plain commit and push stay with the host's permission flow, so an allow rule or auto mode covers them), a content-boundary guard on `changes/**` and lesson writes, a bare-ID guard on `/lbvs-aidlc*` prompt expansion (Claude only), and a scaffold-freshness line at session start.

**Sequence:** (1) spike — install the plugin into a scratch repository under Oh My Pi and confirm agents (tool-name casing) and the guard extension load from the plugin cache; if not, the scaffold writes `.omp/` for those repositories; (2) `build_plugin.py` emits the three plugins and a `package.json` with `omp.extensions`; (3) scaffold `install`, retire `package`; (4) hooks in both hosts; (5) docs. Implemented on branch `plugin-engine` (spike passed natively under Oh My Pi: plugin agents, extension hooks, artifact and PR guards from the generated plugin); `main` keeps the in-repo install until that branch is merged. Two earlier same-day decisions are reversed by this one: "keep `package`" and "always include ECC in install".

## Re-entry rule

Resume a deferred area only when it is explicitly selected. State the goal, dependencies, implementation work and verification required at that time. Do not label deferred work as a blocker for drafting, planning, local implementation or review today.
