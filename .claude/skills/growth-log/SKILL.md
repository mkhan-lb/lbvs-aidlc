---
name: growth-log
description: "Use after a complex task, failure, or when reviewing what was learned. Teaches how to write growth logs that extract reusable patterns — not diary entries."
metadata:
  version: 1.1.0
  origin: ECC
disable-model-invocation: true
---

**AIDLC integration.** See [the optional ECC skill library](../../../docs/USAGE.md#12-use-the-optional-ecc-skill-library). Existing project conventions and canonical AIDLC artifacts prevail. Skill use is not authority for installs, commits, remote writes, deployment, or global/session changes. Invoke manually for one selected, solved and verified non-obvious lesson. Existing /aidlc-learn lifecycle and artifact conventions govern saving, reuse and updates; do not create a parallel learning store, global memory, session mutation or remote note automatically.

# Growth Log Skill

> **The problem:** Most people write "fixed a bug in X" as a learning log. That's a diary entry, not a learning artifact. A real growth log extracts the *pattern* so you recognize it next time.
>
> **This skill teaches:** How to write learning entries that compound across sessions. Works with any note-taking system — Markdown files, Notion, Obsidian, plain text. Templates are generic; adapt to your setup.

## When to Select Manually

- After completing a complex task (multi-file, new feature, architecture change)
- After a failure, mistake, or "that was harder than expected" moment
- When you want to review what you've learned over a period

**When NOT to activate:** Trivial changes (typo fixes, single-line tweaks, config value changes with no debugging). The threshold: *did this task involve debugging, redoing, rollback, or a non-obvious decision?* If yes → consider a user-selected /aidlc-learn capture after the lesson is solved and verified. If no → skip. No automatic post-task write is implied.

## The Three Rules

### Rule 1: Failures > Achievements

A failure is nutritionally denser than a success. One bug that took 2 hours to find teaches more than 3 features that worked first try.

**Bad:** "Successfully implemented the login flow."
**Good (web dev):** "Login flow: a session cookie was not sent on a cross-site request. Pattern: check observed cookie attributes, browser policy and the authentication flow before choosing an appropriate SameSite/CSRF policy. Signal to recognize: authentication fails only across site boundaries."
**Good (data pipeline):** "CSV import counted logically empty records as valid. Pattern: define and test what counts as an empty record before validating row counts. Signal to recognize: parsed-row counts disagree with the meaningful records in a fixture."

### Rule 2: The Bole Principle (伯乐原则)

Before writing a new entry, ask: *"Is this fundamentally the same as something I already recorded?"*

Same root cause, different symptom → **reuse** the existing lesson; propose a merge only with explicit update direction. New root cause → consider a new user-selected entry.

**How to check:** Search existing entries for keywords from your root cause before writing. If you find an adequate match, reuse it rather than creating a duplicate. If it is stale or needs a new example, propose a scoped update and wait for explicit update direction.

**Example:** "Forgot to update the output index after creating a file" and "Forgot to update skill ratings after a task" — same root cause (no automatic capture trigger). Merge into one entry about "post-task capture gaps."

### Rule 3: Must Be Transferable

Every entry must answer: *"Next time I face a similar situation, what do I do differently?"*

If you can't write that sentence, you haven't extracted the pattern yet.

**How to extract a pattern from a concrete event:**
1. State what happened in one sentence
2. Ask "why?" iteratively until you reach root cause (usually 3-5 whys)
3. Generalize: "What class of problem is this?" (not "Chrome 128 bug" but "browser default change breaking existing behavior")
4. Formulate as: "Next time I see [signal], I will [action]."
5. Name the signal: what specific observable tells you this pattern is active?

## Entry Template

**Scope:** One entry per distinct root cause. Typical length: 4-8 sentences. If it takes >2 minutes to write, you're narrating events. If <30 seconds, you haven't gone deep enough.

```markdown
## [Title: the pattern, not the event]

### Context
- What was I trying to do?
- What went wrong / what worked surprisingly well?

### Root Cause / Core Insight
- The underlying mechanism, not just the symptom

### The Pattern (transferable)
- Next time [similar situation], I will [specific action].
- Signal to recognize: [what observable tells me this pattern is active?]

### Related
- [entry-name](../path/to/related-entry.md)
```

## Entry Types

All four types use the template above. The type determines which sections carry the most weight:

| Type | When to Use | Emphasis | Example Title |
|------|------------|----------|---------------|
| **Failure** | Something broke, needed debugging, or required rework | Root Cause | "Config inheritance ≠ behavior inheritance across sessions" |
| **Methodology** | A repeatable process emerged from the work | Context / Pattern | "PPT → open-book exam study guide: three-layer structure" |
| **Pattern Discovery** | A reusable insight about tools, systems, or thinking | Pattern section | "PR description template: describe the gap, not the feature" |
| **Capability Change** | A measurable skill improvement | Context (before vs after) | "Git: from clone/push to independent PR with 12 commits" |

## Quality Checklist

Before finalizing a growth log entry:

- [ ] Does the title name the *pattern*, not the event?
- [ ] Is there a "Next time I will..." sentence?
- [ ] Is the "Signal to recognize" specific enough to trigger the pattern next time?
- [ ] Did I search existing entries for duplicates before writing? (Bole Principle)
- [ ] Is the root cause distinguished from the symptom?
- [ ] Are related memories cross-linked?
- [ ] Is the entry 4-8 sentences? Shorter = too shallow; longer = narrating events.

## Anti-Patterns

- Avoid: "Fixed bug in payment module" (event, not pattern)
- Avoid: Copying the git commit message verbatim (commits describe what changed; logs extract why it matters)
- Avoid: Writing an entry for every commit (only when a pattern emerges)
- Avoid: Skipping the transferable sentence (without it, it's just a diary — this is non-negotiable)
- Avoid: Duplicating the same pattern under different titles (violates Bole Principle — search before writing)

## Storage

For AIDLC, use the existing /aidlc-learn workflow and its configured solution-artifact root; do not create a parallel growth store or write global memory. The following upstream storage patterns are optional alternatives only when explicitly selected outside that lifecycle:
- Markdown files in a `growth-log/` directory (one file per day: `YYYY-MM-DD.md`)
- A dedicated section in Notion, Obsidian, or your note-taking app
- Plain text files with a consistent naming convention

Follow the existing project convention. Remote note creation, publication or global memory changes require separately selected scope and actual available tools; a learning request alone does not authorize them.

## If You Use Delivery Gate

The optional upstream [delivery-gate skill](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/delivery-gate/SKILL.md) and [Stop hook](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/delivery-gate/hooks/quality-gate.py) describe timestamp-based enforcement. Neither is bundled, installed or active here; do not add a hook or enforce learning as a completion gate. This skill teaches *what to write* — so the file that delivery-gate checks actually contains useful patterns, not empty timestamps.

```
Task completes → delivery-gate checks: was the learning file touched today?
  → Stale (no file modified): block — "what did you learn?"
  → Fresh (file touched): pass — this skill ensures the content is useful
```

Having enforcement without methodology → empty entries. Having methodology without enforcement → forgotten captures. Each is independently useful; together they close the loop.
