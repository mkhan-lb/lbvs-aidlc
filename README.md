# lbvs-aidlc

An AI-native development lifecycle for engineers using Claude Code. It turns "ask Claude to write some code" into a repeatable path — **intent → design → plan → build → verify → review → ship** — where every stage leaves a file you can read, every gate is a question you answer, and nothing is committed, pushed or deployed unless you choose it.

Based on [Anthropic's AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook), with requirement traceability borrowed from [Kiro specs](https://kiro.dev/docs/specs/). Works in Claude Code; also loads in Oh My Pi, and its shared instructions are read by Codex and Copilot Chat.

## What you get

- **17 slash commands** (`/lbvs-aidlc*`): one orchestrator, the stage skills, a bug-fix loop, ticket intake, a time-boxed spike, a setup wizard, shipping, onboarding and lessons.
- **6 subagents** that work in a fresh context and report back: a Bash-capable verifier, a pre-PR conventions checker that runs only the repository's documented commands, and four read-only critics (repository scout, design reviewer, threat modeler, test critic).
- **5 small hooks**: package check (silent when it passes) and project-mode line at session start, protection of a failing test while you fix the bug, descriptive worktree names (`aidlc/vs-1234-order-export`) and safe worktree removal that keeps uncommitted work.
- **Repository context that is read, not re-derived**: a committed repository profile (`docs/repo-profile.md`), the company glossary (`docs/glossary/` — Logicbroker and Virtualstock), playbooks for repeatable procedures, and platform facts. Stages read these first and scout only what is missing or stale.
- **Knowledge stores** that fill up as you work: ADRs, incidents, threat models, library references, lessons, playbooks — all Markdown, all written only after you confirm.
- **A Python helper**, `scripts/aidlc.py`, with no dependencies: `doctor`, `check`, `mode`, `status`, `profile`, `conventions`, `package` and friends.
- Optional extras: 38 vendored [ECC](https://github.com/affaan-m/ECC) pattern skills, ADR and doc-coauthoring skills, Compound Engineering brainstorming for non-engineers, MCP declarations for Context7, GitHub and Jira.

Everything Claude does here is advisory instruction plus your confirmation. The skills are not security controls; your repository's permissions, branch protection and CI still apply.

## Install

**New service** — export a standalone tree and start there:

```sh
git clone https://github.com/mkhan-lb/lbvs-aidlc && cd lbvs-aidlc
python3 scripts/aidlc.py package /path/to/new-service
cd /path/to/new-service && claude
```

**Existing repository** — install the plugin (namespaced commands, nothing overwritten):

```sh
claude plugin marketplace add mkhan-lb/lbvs-aidlc
claude plugin install lbvs-aidlc@lbvs-aidlc
# then, inside the repository:  /lbvs-aidlc:lbvs-aidlc-init
```

The plugin carries the skills, all six agents, the project-mode and test-protection hooks, the helper and the shared docs. It does not carry a `CLAUDE.md`, the ECC library, the package-integrity hook, the worktree hook or `.omp/` (so Oh My Pi gets skills only). To put the assets into an existing repository instead — which every host then reads on checkout — run `python3 scripts/aidlc.py install ../<repo>` and, after the report, `--apply`; `sync` updates later ([recipe](docs/USAGE.md#11-install-into-an-existing-repository-or-export-a-new-one)).

Before the first session, `python3 scripts/aidlc.py doctor` tells you which optional tools and MCP credentials are present and how to get the missing ones.

## Set up a repository: `/lbvs-aidlc-init`

Run once per repository. It reports first and writes only what you confirm, so it is safe to run again later.

| Step | What Claude does | What it asks you |
| --- | --- | --- |
| 0 | Runs `doctor`; shows tools and MCP auth state | *Run `doctor --install`* or *Skip* |
| 1 | Detects greenfield or brownfield. Brownfield hands over to `/lbvs-aidlc-onboard` (scout report, conventions report, modernize vs stay-legacy, a `CLAUDE.md` draft) | Greenfield: *Adopt default conventions (`python3 scripts/aidlc.py conventions --apply`)*, *Keep my own tooling* or *Decide later* |
| 2 | Reads `.circleci/config.yml`, `deploy/`, `catalog-info.yaml`, `Taskfile.yml` to fill `docs/platform/platform.md` | *Write platform.md* or *Skip*; unknowns stay bracketed |
| 3 | Explains what still needs auth: Jira via `/mcp`, GitHub via `GITHUB_PERSONAL_ACCESS_TOKEN`, Context7 optional; whether Compound Engineering is installed | Nothing — it never installs or stores secrets |
| 4 | Offers a local code graph when graphify is installed | *Run `/graphify .`* or *Skip* |
| 5 | **Proposes up to three repository-specific agents or skills** (below) | Per candidate: *Write `.claude/agents/<name>.md`* or *Skip*; drafts from a bundled template |
| 6 | Checks `.gitignore` for worktree, fix-marker and code-graph paths | *Append missing lines* or *Skip* |
| 7 | Summary: written / recommended / skipped | *Start a change (/lbvs-aidlc)*, *Start from a ticket (/lbvs-aidlc-ticket)*, *Done* |

**Do you need more agents?** Usually not — the bundled six plus Claude Code's own Explore and Plan agents cover most repositories, and every agent description costs context at startup. Step 5 proposes one only when the repository shows a reason for it:

- a large or vocabulary-heavy subsystem (≥ 40 files, or its own glossary/docs) → a read-only `<repo>-<area>-scout`;
- a documented multi-step test/build/verify procedure → a Bash-capable `<repo>-checker` that runs exactly those commands and reports;
- generated code with its generator present → a read-only `<repo>-generated-guardian` that flags hand edits under generated paths;
- a recurring written procedure (release, migration, data fix) → a repository **skill**, not an agent.

Each proposal says why the existing agents do not already cover it. Alternatives it mentions: Claude Code's `/init` with `CLAUDE_CODE_NEW_INIT=1`, and the official `skill-creator` and `plugin-dev` plugins.

## Your first change

A typical exchange (wording illustrative; the choices are the real ones):

```text
you:     /lbvs-aidlc vs-1234-order-export
claude:  Flow policy for this run?
         [Confirm each stage] [Auto-advance when clear, stop before build] [Auto-advance when clear, including build]
claude:  No worktree exists for vs-1234-order-export. Create one on branch aidlc/vs-1234-order-export?
         [Create worktree] [Continue in place]
claude:  What kind of work is this change?
         [Feature/change] [Bug fix] [Spike/investigation]
```

Then each stage runs, saves its file under `changes/vs-1234-order-export/`, reads it back and stops at a **gate**:

```text
claude:  Intent saved: changes/vs-1234-order-export/intent.md
         Decisions: export is CSV only; nightly, not on demand.  Open questions: retention period?
         [Proceed to design] [Revise this stage] [Stop here]
```

| Stage | Produces | Worth knowing |
| --- | --- | --- |
| intent | `intent.md` — problem, outcome, scope, open questions | Start from a Jira key instead: `/lbvs-aidlc-ticket VS-1234` reads the issue and writes a sourced intent. |
| design | `spec.md` — acceptance criteria as EARS lines with IDs (`R1.1: WHEN … THE system SHALL …`) | Library APIs are looked up through Context7 first. The `lbvs-aidlc-design-reviewer` agent returns READY / NOT READY before the gate. Offers an ADR or threat model when the design warrants one. |
| plan | `plan.md` — checkbox tasks `T1.2 … _Requirements: R1.1_` | Every requirement must appear in a task; the skill checks. |
| build | code, one task at a time; ticks `[x]` after that task's own check passes | Runs the repository's pre-commit/lint before calling a task done. |
| verify | a table `R-ID | check | observed result | not run (reason)` | Offers `lbvs-aidlc-test-critic` to critique the tests. Never fixes code. |
| review | `review.md` — findings with stable IDs, **Important** or **nit** | Uses the bundled `/code-review`. Then asks exactly: *Fix findings (build)*, *Re-review at higher effort*, *Open PR (lbvs-aidlc-ship)*, *Capture lesson (lbvs-aidlc-learn)*, *Done*. |
| ship | commit `VS-1234: …`, push `aidlc/<id>`, PR from a template | `/lbvs-aidlc-ship` first runs `lbvs-aidlc-conventions-checker` (documented lint/test commands, diff vs conventions, commit hygiene, glossary drift). Clean: asks exactly *Commit, push and open PR* / *Commit only* / *Stop here*. Important findings: *Fix findings first (lbvs-aidlc-build)* / *Ship anyway: commit, push and open PR* / *Stop here*, and the PR body lists what was accepted. Never merges. |

**The review loop.** Important findings go back to build with their IDs, then verify, then a re-review one effort tier up (`high` → `xhigh`). After three fix cycles it always stops and asks, whatever the flow policy.

**Under auto-advance** a stage moves on by itself only when its file was saved and read back with no open questions, no failed or missing check and no pending review; it announces every hop. Review always shows its findings; commits, pushes and PRs always ask.

**No IDs to remember.** `/lbvs-aidlc` alone works out the change from the branch, then `.aidlc/current`, then the only open change. `python3 scripts/aidlc.py status` lists every change and the stage it has reached.

## Fixing a bug

```text
you:     /lbvs-aidlc-fix vs-1301-duplicate-invoice
claude:  Symptom: two invoices for order 8812 (Sentry link). Reproducing…
         Failing test committed: tests/test_invoice.py::test_single_invoice_per_order  (protected until the fix lands)
         Cause: retry path re-runs the issue step. Fix proposed in services/invoice.py — apply?
```

The failing test is committed — with your authorisation — **before** the fix and the `protect-tests` hook denies edits to it while the fix is in progress. The result is `changes/<id>/evidence.md` — Current / Expected / *SHALL CONTINUE TO* behaviour, the reproduction, the fix, Jira/PR/incident links — followed by an offer to record an incident (if it came from an alert) and a lesson (`/lbvs-aidlc-learn`).

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
| `/lbvs-aidlc-onboard` | An existing codebase needs conventions recorded before the first change. |
| `/lbvs-aidlc-learn <change-id>` | You learned something non-obvious worth keeping (with a confidence score). |
| `/lbvs-aidlc-handoff`, `/lbvs-aidlc-resume <change-id>` | Pausing work and picking it up later (manual only). |
| `/lbvs-aidlc-ideate <topic-id>` | Comparing directions before a change exists (manual only). |

Change IDs match `^[a-z0-9]+(-[a-z0-9]+)*$`; prefix your ticket key so branches and commits carry it. Claude may also load a stage skill on its own when your request matches — the gates still apply. Commands and agents carry the `lbvs-aidlc-` prefix so they never collide with other AIDLC packages you may have loaded; the branch prefix `aidlc/<id>` and `.aidlc/` state directory keep their short names.

## The agents

| Agent | Tools | Called by |
| --- | --- | --- |
| `lbvs-aidlc-verifier` | Read, Glob, Grep, Bash | verify — fresh-context behavioural check against spec and plan |
| `lbvs-aidlc-repo-scout` | read-only | onboard, spike — structured conventions report |
| `lbvs-aidlc-design-reviewer` | read-only | design — READY / NOT READY on `spec.md`/`plan.md` against intent, ADRs, platform, EARS coverage |
| `lbvs-aidlc-threat-modeler` | read-only | design — STRIDE table when a threat-model offer is accepted |
| `lbvs-aidlc-test-critic` | read-only | verify, review — tests vs requirement IDs, coupling, missing failure cases, flaky patterns |
| `lbvs-aidlc-conventions-checker` | read-only + Bash for documented commands | ship — runs the profile's lint/format/test commands verbatim, checks the diff against conventions, commit titles, generated paths and glossary terms |

All verdicts are advisory input to the stage summary, never approvals. `/lbvs-aidlc-init` can add repository-specific ones.

**Why not a persona per role, like the AWS AI-DLC?** Its fourteen agents (architect, product, developer, quality, operations, …) mostly carry a *viewpoint*; here those viewpoints live in the stage skills, which run in the main conversation where you can steer them. A separate agent is worth its startup context only when it needs a **fresh context** (so it cannot be swayed by the session that wrote the code), a **bounded tool set** (the checker may run commands; the critics may not), or **repository-specific knowledge** too large to load every session — which is what `/lbvs-aidlc-init` proposes when a repository shows the need.

## What accumulates

| Store | Holds | Filled by |
| --- | --- | --- |
| `changes/<id>/` | intent, spec, plan, evidence, review, handoffs — the record of one change | every stage |
| `docs/adr/` | architecture decisions | design, spike (offer) |
| `docs/incidents/`, `docs/security/` | incident records, threat models, security findings | fix, design (offer) |
| `docs/references/libraries.md` | which library pages answered real questions, with gotchas | design, plan, build, fix |
| `docs/solutions/` | one verified lesson per file with Confidence / Observations / Scope | `/lbvs-aidlc-learn` |
| `docs/platform/platform.md` | this repository's environments, orb pin, deployment authority | you, via `/lbvs-aidlc-init` |
| `docs/repo-profile.md` | stack, commands, conventions, generated paths, ownership — with `Last verified: <date> at <commit>`; `python3 scripts/aidlc.py profile` says fresh or stale | `/lbvs-aidlc-onboard`, `/lbvs-aidlc-init` (scout report, written on confirmation) |
| [`docs/glossary/`](docs/glossary/README.md) | the Logicbroker and Virtualstock glossaries: term, aliases, evidence, sources pinned to a commit, review state; each links its Confluence review copy | domain owners via Confluence, copied back in a reviewed PR; stages flag *new terms* and offer an entry |
| `docs/playbooks/` | repeatable procedures (release, migration, data fix) with steps, verification, rollback and a `Runs` count; a Verified playbook run three times is proposed as a repository skill | spike (*Save as playbook*), learn; plan cites them, build follows them |

A lesson seen in two or more changes at confidence ≥ 0.8 is *proposed* as a rule for `AGENTS.md` — never written automatically.

## Status

Verified natively: the commands load in Claude Code (also namespaced from the plugin) and Oh My Pi; all hooks fire; `/lbvs-aidlc` resolves the change, asks the flow policy and creates the worktree; a driven trial ran the intent stage with Compound Engineering brainstorming. Details and limits in [docs/VERIFICATION.md](docs/VERIFICATION.md).

**Not yet driven end to end — the next thing to do:** one real change through `/lbvs-aidlc-ticket <VS key>` → design → plan → build → verify → review → `/lbvs-aidlc-ship` in a repository where Jira is authenticated. That single run exercises the review loop, the reviewer, test-critic and conventions-checker agents, Context7 lookups, EARS tracing and shipping, none of which has been observed live yet. `/lbvs-aidlc-init`, `/lbvs-aidlc-onboard` writing a repository profile, a playbook saved from a spike, and `/lbvs-aidlc-fix` on a real defect are also untested in a native session.

## Learn more

- [docs/USAGE.md](docs/USAGE.md) — step-by-step recipes for each situation.
- [docs/REFERENCE.md](docs/REFERENCE.md) — every command, agent, hook, store, host and design decision in full; the helper CLI; export and plugin distribution.
- [docs/WORKFLOW.md](docs/WORKFLOW.md) and [docs/ARTIFACTS.md](docs/ARTIFACTS.md) — the contract the skills follow and the files they write.
- [docs/PLUGINS.md](docs/PLUGINS.md) — optional plugins, MCP servers and Compound Engineering.
- [GOALS.md](GOALS.md), [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md), [FUTURE_WORK.md](FUTURE_WORK.md) — scope and what is deferred.

## License

[MIT](LICENSE). Skills imported from ECC keep their upstream [MIT license](docs/vendor/ecc/LICENSE) and in-file attributions; `doc-coauthoring` from anthropics/skills carries the licensing statement recorded in [NOTICE.md](docs/vendor/anthropic-skills/NOTICE.md); the agents adapted from AWS aidlc-workflows are attributed in [docs/vendor/aws-aidlc/NOTICE.md](docs/vendor/aws-aidlc/NOTICE.md); the [playbook snapshot](docs/sources/anthropic-playbook.md) is reference material, not relicensed.
