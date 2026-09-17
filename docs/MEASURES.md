# Source measures

Source: [Anthropic playbook](https://claude.com/blog/the-ai-native-sdlc-playbook), preserved in [the source snapshot](sources/anthropic-playbook.md). IDs map to [coverage](COVERAGE.md).

These are source measurement definitions for possible later implementation, not current workflow requirements, observed benefits or fabricated results. There are thirteen explicit leading/lagging measurement blocks in the article. Collection infrastructure is outside the [current scope](../GOALS.md).

| ID | Leading indicators | Lagging indicators | Source evidence systems |
| --- | --- | --- | --- |
| P01 | First conversation to committed intent | Product-owner acceptance/survival rate; intent changes after first spec commit | Intent history and merge/closed review; conversation start must also be recorded because Git alone cannot establish it |
| D01 | Intent-to-spec commit elapsed time | Spec changes after the first plan commit | Linked artifact Git history |
| B01 | First-pass implementation merge share; plan approval to merged PR | Rework cycles; merged diff still matching plan | Plan approval and PR metadata/history |
| B03 | Repeated mistakes CLAUDE.md should prevent | New team member's time to first merged PR | Reviewed context corrections, join/start record and PR history |
| B04 | Policy-owner approval to updated skill merge | Review findings citing the policy | Policy approval and skill/review PR history |
| B06 | Concurrent sessions while review quality holds; steering versus waiting time | Merges per engineer per week alongside rework | Session telemetry and PR history; activity-time collection must be defined |
| T01 | First-pass CI success for agent-written changes | Review time per PR; change failure rate | CI, PR and incident records |
| T02 | Eval pass rate over time; incident-to-permanent-eval elapsed time | Regressions caught in CI versus production | Eval runs, CI and incident records |
| R01 | Time to first review; comments resolved without human branch edits | Defects/vulnerabilities caught before merge versus escaped | Review/PR history, actor provenance and incidents |
| R02 | Wait time per approval gate | Gate violations reaching production before/after hooks | Timestamped gate/request/decision records and incident tracker |
| R04 | Pipeline failures triaged without paging a human | DORA measures, not individually enumerated by the article | Pipeline/deployment logs and paging records |
| M01 | Band breach to intent in triage queue | Findings becoming merged fixes; repeat incidents of the same class | Detection timestamps/tier, triage, PRs and incidents |
| M02 | Repositories on a scan schedule; finding to proposed patch review | Scan-found vulnerabilities versus production/external reports; findings-per-scan trend | Scan history, PR metadata, incident tracker |

B02, B05, R03, M03, X01 and X02 have **no independent leading/lagging block**. R02's hook metrics follow the managed-settings example but are explicitly labelled as measures for the hooks. Do not assign new measures to those six IDs as if Anthropic prescribed them.

## Future collection contract

For each measurement, an adopting reference environment must record the linked change identity, relevant revision, source event and timestamp, actor/approval authority, evidence location and collection owner. Define denominators, observation windows and event attribution before computing rates. Keep model-generated findings separate from human decisions and deterministic check outcomes.

The source gives evidence systems and some directional expectations, not universal numeric targets or complete telemetry schemas. Verify which hook/session events the installed product actually exports; add an explicit collector where the required event is not emitted rather than claiming it is present automatically.

A successful local check demonstrates package behaviour, not lower change-failure rate or company productivity. Long-term outcomes require sustained operation of the selected reference environment. See [prerequisites](PREREQUISITES.md) for missing data sources and [verification](VERIFICATION.md) for what was actually exercised.
