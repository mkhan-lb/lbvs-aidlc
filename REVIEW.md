# Review policy

Source: [Anthropic's AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook), AI in the PR review loop.

## Passes

Review the identified diff or working-tree scope against the available intent, spec, plan and applicable repository policies. A local review does not require a PR or approval service. Tag findings by pass:

- **Bugs:** incorrect behaviour, broken edge cases, regressions, concurrency or error-handling failures.
- **Security:** injection, authorisation gaps, exposed credentials or personal data, unsafe execution, and bypassable controls.
- **Compliance:** mismatches with the current spec and plan, applicable policy or design principles. Check that implementation changes did not silently leave the artifacts stale, and that a new or changed architectural boundary, technology choice or contract has a matching record under `docs/adr/` (a gap is a finding, never a blocker). Do not flag deliberately deferred lifecycle infrastructure as a defect in this workflow.

Each actionable finding identifies severity, affected file/line or artifact, the failure scenario, evidence, and a proposed correction. Separate demonstrated failures from hypotheses needing reproduction. Report missing context instead of asserting compliance with an unknown policy.

## Important versus nit

Important findings would break behaviour, leak data, weaken a required control, or breach an applicable policy. Style and naming are nits unless they cause such a failure. Report at most five nits and summarise the remainder. Skip generated files and issues already deterministically enforced by CI; cite CI failures without duplicating them as novel findings.

## Verification and review loop

Inspect actual check results, relevant runtime evidence, and the full change. A green package-integrity check is not proof of application correctness or operational readiness. Check that a fix did not weaken the test that demonstrated the original defect.

After changes, re-review the affected revision and resolve findings with evidence. Repeated mistakes inform reviewed updates to CLAUDE.md or the relevant skill. Check whether the change makes existing context stale. The tech lead periodically tunes review signal and nit volume as described by the source.

## Existing reviewer and engineer handoff

Use an existing review capability, supplying the artifact and verification context rather than implementing a new review engine. [Review options](.claude/skills/aidlc-review/references/review-options.md) distinguishes built-in commands, plugins and hosted services, including their posting behavior.

The reviewer reports findings; the engineer decides what to fix. Keep findings local by default, then verify fixes and re-review the changed result. Do not approve, publish comments, merge or release unless explicitly instructed and permitted. Existing repository rules remain in force, but this package does not implement or require a new approval boundary.

No remote review service, plugin, branch protection or delivery integration is configured merely by adding this file. Missing future infrastructure does not block local review.
