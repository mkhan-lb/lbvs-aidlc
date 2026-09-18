# Playbooks

Repeatable procedures this repository has actually run — a release, a migration, a data fix, a recovery — written so the next run needs no rediscovery. Playbooks hold **procedures**; a lesson in `docs/solutions/` holds one insight; an ADR in `docs/adr/` holds a decision; a rule in `.claude/rules/` holds a recurring correction. Stages read this index per [docs/WORKFLOW.md#repository-context](../WORKFLOW.md#repository-context) before scouting.

| Playbook | Trigger | Status | Runs | Last verified |
| --- | --- | --- | --- | --- |

## Rules

- **One file per procedure**, `docs/playbooks/<kebab-title>.md`, copied from [`template.md`](template.md) with every angle-bracket placeholder replaced; keep its `Trigger` paragraph and this row's Trigger cell in sync.
- **Where playbooks come from.** `lbvs-aidlc-spike` offers "Save as playbook" when its answer is a repeatable procedure of at least three ordered steps; `lbvs-aidlc-learn` offers "Save as playbook instead" when a lesson is procedural. Both write `Status: Draft`, `Runs: 0`, `Sources` pointing at the spike or evidence, and this row — on confirmation and Read back only.
- **How playbooks are used.** `lbvs-aidlc-plan` cites a matching playbook in the task (`_Playbook: docs/playbooks/<name>.md_`); `lbvs-aidlc-build` follows its steps and, after the task's check passes, offers to bump `Runs` and append the change ID. A step that no longer works is fixed in the playbook within the same change, never worked around silently.
- **Status.** `Draft` until one run has followed the steps as written and passed `Verification`, then `Verified` with the date and revision or environment. When a better procedure replaces it, set `Superseded by <path>` and keep the file. Lower `Verified` back to `Draft` when a run finds a step wrong.
- **Promotion.** `Runs` at least 3 and `Verified` → `/lbvs-aidlc-init` step 6 proposes a repository skill `.claude/skills/<repo>-<playbook>/SKILL.md`; it is proposed to the engineer, never auto-written, and the playbook stays as the skill's source.
- **Grounding.** Every step names how to verify it worked; never invent commands, outputs or environments. Pitfalls link the lesson that taught them; Sources link the spike, evidence, change IDs or ADRs the procedure came from. Secrets, tokens and production URLs never appear here.
