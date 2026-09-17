# Playbook: <title>

Status: Draft | Verified | Superseded by <path>
Last verified: <YYYY-MM-DD> at <revision or environment>
Runs: <count> (<change IDs, comma-separated; none for a new playbook>)

## Trigger

<One paragraph: the situation that calls for this procedure and how to recognise it — the same text as the Trigger cell in docs/playbooks/README.md.>

## Preconditions

- <Access, tools, environment state or artifacts that must exist before step 1; cite the path or say how to check>

## Steps

1. <Action, with the exact command or file when there is one.> Verify: <what you observe when it worked>.
2. <Action.> Verify: <observable result>.
3. <Action.> Verify: <observable result>.

## Verification

<How to confirm the whole procedure succeeded end to end: command, output or surface to inspect, and what "good" looks like.>

## Rollback

<How to undo or recover if a step fails or verification does not pass; say "not reversible" when that is the truth and what to do instead.>

## Pitfalls

- <Known failure or surprise, with a link to the lesson in docs/solutions/<category>/<topic>.md that recorded it>

## Sources

- <changes/<change-id>/spike.md, changes/<change-id>/evidence.md, change IDs, docs/adr/<file> — where this procedure came from>

## Promotion

Runs at least 3 and Status Verified → propose a repository skill `.claude/skills/<repo>-<playbook>/SKILL.md` via `/aidlc-init` step 5; proposed to the engineer, never auto-written. Skill proposed: <no | yes — path or date>.
