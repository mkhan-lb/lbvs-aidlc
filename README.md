# lbvs-aidlc

An AI-native development lifecycle for engineers who use Claude Code. It replaces "ask Claude to write some code" with a fixed path: intent, design, plan, build, verify, review, ship. Every stage leaves a file you can read. Every gate is a question you answer. Nothing is committed, pushed or deployed unless you choose it.

The lifecycle follows [Anthropic's AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook). Requirement traceability comes from [Kiro specs](https://kiro.dev/docs/specs/). It runs in Claude Code and in Oh My Pi; Codex and Copilot Chat read its shared instructions.

## What you get

- 17 slash commands (`/lbvs-aidlc*`): one orchestrator, the stage skills, a bug-fix loop, ticket intake, a time-boxed spike, a setup wizard, shipping, onboarding and lessons.
- 6 subagents that work in a fresh context and report back: a verifier with Bash, a pre-PR conventions checker that runs only the repository's documented commands, and four read-only critics (repository scout, design reviewer, threat modeler, test critic).
- 11 hooks. At session start: the package check (silent when it passes), the project-mode line, a scaffold-version check, the reply style (caveman lite by default; `.aidlc/style` sets `full`, `ultra` or `off`) and the company glossary index (one line per term, about 10 KB; the company comes from `.aidlc/glossary` or the profile's `Company:` line, `off` silences it). On every edit: protection of a failing test while you fix its bug, and the content boundary on `changes/**` and lessons. On `gh` and `git push`: a confirmation prompt before a pull request opens or merges or a force-push runs. On `/lbvs-aidlc*`: one bare change ID or nothing. On worktree creation and removal: descriptive names (`aidlc/vs-1234-order-export`) and removal that keeps uncommitted work.
- Repository context that is read, not re-derived: a committed repository profile (`docs/repo-profile.md`) with a knowledge-store table, the company glossary (`docs/glossary/`, Logicbroker and Virtualstock, with a generated index that the session-start hook injects), playbooks for repeatable procedures, and platform facts. Stages read these first and scout only what is missing or stale.
- Knowledge stores that fill as you work: ADRs, incidents, threat models, library references, lessons, playbooks. All Markdown, all written only after you confirm.
- A Python helper, `scripts/aidlc.py`, with no dependencies: `doctor`, `check`, `mode`, `status`, `profile`, `conventions`, `lint-artifacts`, `install`, `sync`, `update`. It is on the Bash PATH as `aidlc` while the plugin is enabled.
- Optional extras: 37 [ECC](https://github.com/affaan-m/ECC) pattern skills as a second plugin, the ADR, doc-coauthoring, unslop and caveman skills, Compound Engineering brainstorming for non-engineers, MCP declarations for Context7, GitHub and Jira, and a continuous-learning observer that ships disabled.

Everything Claude does here is instruction plus your confirmation. The skills are not security controls. Your repository's permissions, branch protection and CI still apply.

## Install

The engine is a plugin. A repository holds only its own state. The same two steps apply to a new repository and an existing one.

Step 1, the plugin, once per engineer. Claude Code and Oh My Pi read the same marketplace:

```sh
claude plugin marketplace add mkhan-lb/lbvs-aidlc
claude plugin install lbvs-aidlc@lbvs-aidlc          # skills, agents, hooks, helper, docs
claude plugin install lbvs-ecc@lbvs-aidlc            # optional: 37 reference skills
# Oh My Pi
omp plugin marketplace add mkhan-lb/lbvs-aidlc && omp plugin install --scope project lbvs-aidlc@lbvs-aidlc
```

Step 2, the scaffold, once per repository, from a checkout of this package:

```sh
python3 scripts/aidlc.py install ../my-service          # report
python3 scripts/aidlc.py install ../my-service --apply  # REVIEW.md, knowledge-store seeds, .aidlc/manifest.json
```

The report also prints what only you may write: the plugin declaration for `.claude/settings.json` (`extraKnownMarketplaces` and `enabledPlugins`, so a teammate without the plugin is told what to install), the `.gitignore` lines, and one pointer line for `AGENTS.md` or `CLAUDE.md`. Commit the result, then run `/lbvs-aidlc:lbvs-aidlc-init` in the repository. Later, `aidlc update` inside the repository refreshes the seeds, and plugin updates arrive by version through the marketplace. A third plugin, `lbvs-aidlc-observer`, installs disabled and turns on only when you ask. The [recipe](docs/USAGE.md#11-install-the-plugin-and-scaffold-a-repository) has the details.

Before the first session, `python3 scripts/aidlc.py doctor` lists the optional tools and MCP credentials that are present and how to get the missing ones.

## Set up a repository: `/lbvs-aidlc-init`

Run it once per repository. It reports first and writes only what you confirm, so a second run is safe.

| Step | What Claude does | What it asks you |
| --- | --- | --- |
| 0 | Runs `doctor`; shows tools and MCP auth state | *Run `doctor --install`* or *Skip* |
| 1 | Detects greenfield or brownfield. Brownfield hands over to `/lbvs-aidlc-onboard` (scout report, conventions report, modernize or stay legacy, a `CLAUDE.md` draft, the knowledge-store table) | Greenfield: *Adopt default conventions (`python3 scripts/aidlc.py conventions --apply`)*, *Keep my own tooling* or *Decide later* |
| 2 | Reads `.circleci/config.yml`, `deploy/`, `catalog-info.yaml` and `Taskfile.yml` to fill `docs/platform/platform.md` | *Write platform.md* or *Skip*; unknowns stay bracketed |
| 3 | Says what still needs auth: Jira via `/mcp`, GitHub via `GITHUB_PERSONAL_ACCESS_TOKEN`, Context7 optional; whether Compound Engineering is installed | Nothing. It never installs or stores secrets |
| 4 | Offers a local code graph when graphify is installed | *Run `/graphify .`* or *Skip* |
| 5 | Reports whether the observer plugin is enabled | *Enable the observer plugin* (prints the command) or *Leave off* |
| 6 | Proposes up to three repository-specific agents or skills (below) | Per candidate: *Write `.claude/agents/<name>.md`* or *Skip*; drafts come from a bundled template |
| 7 | Checks `.gitignore` for worktree, fix-marker and code-graph paths | *Append missing lines* or *Skip* |
| 8 | Summary: written, recommended, skipped | *Start a change (/lbvs-aidlc)*, *Start from a ticket (/lbvs-aidlc-ticket)*, *Done* |

Do you need more agents? Usually not. The bundled six plus Claude Code's own Explore and Plan agents cover most repositories, and every agent description costs context at startup. Step 6 proposes one only when the repository shows a reason:

- a large or vocabulary-heavy subsystem (40 files or more, or its own glossary or docs): a read-only `<repo>-<area>-scout`;
- a documented multi-step test, build or verify procedure: a `<repo>-checker` with Bash that runs exactly those commands and reports;
- generated code with its generator present: a read-only `<repo>-generated-guardian` that flags hand edits under generated paths;
- a recurring written procedure (release, migration, data fix): a repository skill, not an agent.

Each proposal says why the existing agents do not already cover it. It also names the alternatives: Claude Code's `/init` with `CLAUDE_CODE_NEW_INIT=1`, and the official `skill-creator` and `plugin-dev` plugins.

## Your first change

A typical exchange. The wording is illustrative; the choices are the real ones.

```text
you:     /lbvs-aidlc vs-1234-order-export
claude:  Flow policy for this run?
         [Confirm each stage] [Auto-advance when clear, stop before build] [Auto-advance when clear, including build]
claude:  No worktree exists for vs-1234-order-export. Create one on branch aidlc/vs-1234-order-export?
         [Create worktree] [Continue in place]
claude:  What kind of work is this change?
         [Feature/change] [Bug fix] [Spike/investigation]
```

Each stage then runs, saves its file under `changes/vs-1234-order-export/`, reads it back and stops at a gate:

```text
claude:  Intent saved: changes/vs-1234-order-export/intent.md
         Decisions: export is CSV only; nightly, not on demand.  Open questions: retention period?
         [Proceed to design] [Revise this stage] [Stop here]
```

| Stage | Produces | Worth knowing |
| --- | --- | --- |
| intent | `intent.md`: problem, outcome, scope, open questions | To start from a Jira key instead, `/lbvs-aidlc-ticket VS-1234` reads the issue and writes a sourced intent. |
| design | `spec.md`: acceptance criteria as EARS lines with IDs (`R1.1: WHEN … THE system SHALL …`) | Library APIs are looked up through Context7 first. The `lbvs-aidlc-design-reviewer` agent returns READY or NOT READY before the gate. The stage offers an ADR or a threat model when the design warrants one. |
| plan | `plan.md`: checkbox tasks `T1.2 … _Requirements: R1.1_` | Every requirement must appear in a task; the skill checks. |
| build | code, one task at a time; ticks `[x]` after that task's own check passes | Runs the repository's pre-commit or lint before it calls a task done. |
| verify | a table `R-ID | check | observed result | not run (reason)` | Offers `lbvs-aidlc-test-critic` to critique the tests. Never fixes code. |
| review | `review.md`: findings with stable IDs, **Important** or **nit** | Uses the reviewer the host exposes (Claude Code's `/code-review`, or Oh My Pi's `reviewer` agent). Then asks exactly: *Fix findings (build)*, *Re-review at higher effort*, *Open PR (lbvs-aidlc-ship)*, *Capture lesson (lbvs-aidlc-learn)*, *Done*. |
| ship | commit `VS-1234: …`, push `aidlc/<id>`, PR from a template | `/lbvs-aidlc-ship` first runs `lbvs-aidlc-conventions-checker` (documented lint and test commands, diff against conventions, commit hygiene, glossary drift, content boundary). When clean it asks exactly *Commit, push and open PR*, *Commit only* or *Stop here*. With Important findings it asks *Fix findings first (lbvs-aidlc-build)*, *Ship anyway: commit, push and open PR* or *Stop here*, and the PR body lists what was accepted. It never merges. |

The review loop. Important findings go back to build with their IDs, then to verify, then to a re-review one effort tier up. After three fix cycles it always stops and asks, whatever the flow policy.

Under auto-advance a stage moves on by itself only when its file was saved and read back with no open questions, no failed or missing check and no pending review. It announces every hop. Review always shows its findings. Opening a pull request always asks.

You do not have to remember IDs. `/lbvs-aidlc` alone works out the change from the branch, then from `.aidlc/current`, then from the only open change. `python3 scripts/aidlc.py status` lists every change and the stage it has reached.

## Fixing a bug

```text
you:     /lbvs-aidlc-fix vs-1301-duplicate-invoice
claude:  Symptom: two invoices for order 8812 (Sentry link). Reproducing…
         Failing test committed: tests/test_invoice.py::test_single_invoice_per_order  (protected until the fix lands)
         Cause: retry path re-runs the issue step. Fix proposed in services/invoice.py. Apply?
```

The failing test is committed before the fix when you say so; that is the one commit allowed before ship. The `protect-tests` hook denies edits to the test while the fix is in progress, and the skill probes the hook before it starts. The result is `changes/<id>/evidence.md` with the Current, Expected and *SHALL CONTINUE TO* behaviour, the reproduction, the fix and the Jira, PR and incident links. The skill then offers an incident record when the symptom came from an alert, and a lesson through `/lbvs-aidlc-learn`.

## The commands

| Command | Use it when |
| --- | --- |
| `/lbvs-aidlc [change-id]` | Starting or continuing any change. Routes bug fixes and spikes. |
| `/lbvs-aidlc-init` | First time in a repository; setting up tools, platform facts and repository-specific agents. |
| `/lbvs-aidlc-ticket <KEY or URL>` | The work starts from a Jira issue or GitHub issue. |
| `/lbvs-aidlc-spike [change-id]` | A question needs a time-boxed, read-only investigation before intent or design. |
| `/lbvs-aidlc-intent`, `-design`, `-plan`, `-build`, `-verify`, `-review <change-id>` | Running one stage on its own. |
| `/lbvs-aidlc-fix <change-id>` | A defect: reproduce, protect the failing test, fix, record evidence. |
| `/lbvs-aidlc-ship [change-id]` | The review pass is clean and you want a commit, push and PR. |
| `/lbvs-aidlc-onboard` | An existing codebase needs its conventions and knowledge stores recorded before the first change. |
| `/lbvs-aidlc-learn <change-id>` | You learned something non-obvious worth keeping, with a confidence score. |
| `/lbvs-aidlc-handoff`, `/lbvs-aidlc-resume <change-id>` | Pausing work and picking it up later (manual only). |
| `/lbvs-aidlc-ideate <topic-id>` | Comparing directions before a change exists (manual only). |

Change IDs match `^[a-z0-9]+(-[a-z0-9]+)*$`. Prefix your ticket key so branches and commits carry it. Claude may also load a stage skill on its own when your request matches; the gates still apply. Commands and agents carry the `lbvs-aidlc-` prefix so they never collide with other AIDLC packages you may have loaded. The branch prefix `aidlc/<id>` and the `.aidlc/` state directory keep their short names.

## The agents

| Agent | Tools | Called by |
| --- | --- | --- |
| `lbvs-aidlc-verifier` | Read, Glob, Grep, Bash | verify: fresh-context behavioural check against spec and plan |
| `lbvs-aidlc-repo-scout` | read-only | onboard, spike: structured conventions report and the knowledge-store table |
| `lbvs-aidlc-design-reviewer` | read-only | design: READY or NOT READY on `spec.md` and `plan.md` against intent, ADRs, platform and EARS coverage |
| `lbvs-aidlc-threat-modeler` | read-only | design: STRIDE table when a threat-model offer is accepted |
| `lbvs-aidlc-test-critic` | read-only | verify, review: tests against requirement IDs, coupling, missing failure cases, flaky patterns |
| `lbvs-aidlc-conventions-checker` | read-only plus Bash for documented commands | ship: runs the profile's lint, format and test commands verbatim; checks the diff against conventions, commit titles, generated paths, glossary terms and the content boundary |

All verdicts are input to the stage summary, never approvals. `/lbvs-aidlc-init` can add repository-specific agents.

Why not a persona per role, as the AWS AI-DLC does? Its fourteen agents (architect, product, developer, quality, operations and others) mostly carry a viewpoint. Here those viewpoints live in the stage skills, which run in the main conversation where you can steer them. A separate agent earns its startup context in three cases: it needs a fresh context so the session that wrote the code cannot sway it; it needs a bounded tool set (the checker may run commands, the critics may not); or it holds repository-specific knowledge too large to load every session, which is what `/lbvs-aidlc-init` proposes when a repository shows the need.

## What accumulates

| Store | Holds | Filled by |
| --- | --- | --- |
| `changes/<id>/` | intent, spec, plan, evidence, review, handoffs: the record of one change | every stage |
| `docs/adr/` | architecture decisions | design, spike (offer) |
| `docs/incidents/`, `docs/security/` | incident records, threat models, security findings | fix, design (offer) |
| `docs/references/libraries.md` | which library pages answered real questions, with gotchas | design, plan, build, fix |
| the repository's lesson store (`docs/solutions/` by default) | one verified lesson per file with Confidence, Observations and Scope | `/lbvs-aidlc-learn` |
| `docs/platform/platform.md` | this repository's environments, orb pin, deployment authority | you, via `/lbvs-aidlc-init` |
| `docs/repo-profile.md` | stack, commands, conventions, generated paths, ownership, knowledge stores, with `Last verified: <date> at <commit>`; `python3 scripts/aidlc.py profile` says fresh or stale | `/lbvs-aidlc-onboard`, `/lbvs-aidlc-init` (scout report, written on confirmation) |
| [`docs/glossary/`](docs/glossary/README.md) | the Logicbroker and Virtualstock glossaries: term, aliases, evidence, sources pinned to a commit, review state; each links its Confluence review copy | domain owners via Confluence, copied back in a reviewed PR; stages flag new terms and offer an entry |
| `docs/playbooks/` | repeatable procedures (release, migration, data fix) with steps, verification, rollback and a `Runs` count; a Verified playbook run three times is proposed as a repository skill | spike (*Save as playbook*), learn; plan cites them, build follows them |

A repository that already keeps one of these stores in its own form records that in the profile's knowledge-store table, and the skills write there instead. A lesson seen in two or more changes at confidence 0.8 or higher is proposed as a rule for `AGENTS.md`, never written automatically.

## Status

Verified natively: the commands load in Claude Code and Oh My Pi; the plugin's agents, skills and guard extension load from the marketplace under Oh My Pi; `/lbvs-aidlc` resolves the change, asks the flow policy and creates the worktree; one real defect (SO2-1386 in the-edge) ran through `/lbvs-aidlc-fix`, review with Oh My Pi's reviewer and `/lbvs-aidlc-ship` to an open pull request. Details and limits are in [docs/VERIFICATION.md](docs/VERIFICATION.md).

Not yet driven end to end: a feature change through `/lbvs-aidlc-ticket`, design, plan, build, verify and review in a repository where Jira is authenticated; `/lbvs-aidlc-init` and `/lbvs-aidlc-onboard` writing a repository profile; a playbook saved from a spike; the hooks executing inside a Claude Code session (they were exercised with hook-shaped input only).

## Learn more

- [docs/USAGE.md](docs/USAGE.md): step-by-step recipes for each situation.
- [docs/REFERENCE.md](docs/REFERENCE.md): every command, agent, hook, store, host and design decision; the helper CLI; plugins and scaffold.
- [docs/WORKFLOW.md](docs/WORKFLOW.md) and [docs/ARTIFACTS.md](docs/ARTIFACTS.md): the contract the skills follow and the files they write.
- [docs/PLUGINS.md](docs/PLUGINS.md): optional plugins, MCP servers and Compound Engineering.
- [GOALS.md](GOALS.md), [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md), [FUTURE_WORK.md](FUTURE_WORK.md): scope and what is deferred.

## License

[MIT](LICENSE). Skills imported from ECC keep their upstream [MIT license](docs/vendor/ecc/LICENSE) and in-file attributions. `doc-coauthoring` from anthropics/skills carries the licensing statement recorded in [NOTICE.md](docs/vendor/anthropic-skills/NOTICE.md). `unslop` from cursor/plugins keeps its [MIT license](docs/vendor/cursor-plugins/LICENSE); `caveman` from JuliusBrussee/caveman keeps its [MIT license](docs/vendor/caveman/LICENSE) (only the MIT `skills/` part was copied). The agents adapted from AWS aidlc-workflows are attributed in [docs/vendor/aws-aidlc/NOTICE.md](docs/vendor/aws-aidlc/NOTICE.md). The [playbook snapshot](docs/sources/anthropic-playbook.md) is reference material, not relicensed.
