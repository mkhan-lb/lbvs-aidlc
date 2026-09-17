---
name: inherit-legacy-style
description: Legacy-project style inheritance skill. Use when the user types /inherit-legacy-style, or when onboarding an AI coding agent onto a hand-written legacy project and you need to prevent "style drift" (the model imposing its pretrained mainstream idioms onto the project). Language- and framework-agnostic — it aligns meta-architecture only, not syntax. Its findings are advisory within the selected task; existing project instructions remain authoritative. Do NOT use for pure research or one-off questions unrelated to code-style alignment.
metadata:
  origin: community
---

**AIDLC integration:** Follow the [optional ECC skill library guidance](../../../docs/USAGE.md#12-use-the-optional-ecc-skill-library). Existing project conventions and canonical AIDLC artifacts prevail. Skill use is not authority for installs, commits, remote writes, deployment, or global/session changes. Style discovery is advisory within the selected task. Writing style notes requires explicit scope and existing project/AIDLC artifact locations; do not install hooks or change CLAUDE.md, settings, or session behavior.

# Inherit Legacy Style

Prevents AI code style drift in legacy projects by scanning the codebase for implicit conventions across 4 meta-architecture dimensions, resolving conflicts with the user one at a time, and crystallizing the consensus into an advisory style note in the existing project/AIDLC artifact location (`.ai-style-rules.md` only if explicitly selected). Fully language- and framework-agnostic.

## When to Activate

- User types `/inherit-legacy-style`
- User mentions onboarding AI onto a hand-written legacy project
- User is worried about AI-generated code "drifting" from existing project conventions
- User wants to extract and codify their project's implicit coding rules

## When to Use

Use this skill when you need to preserve legacy project style and prevent AI-generated style drift. See **When to Activate** above for trigger conditions.

## Prerequisites

- Git (recommended; non-Git projects fall back to file timestamps for incremental mode)
- Read access for discovery; separate authorization for writing the selected style-note artifact. Discover available file/search tools first and stop if unavailable. No settings, hook, or CLAUDE.md changes are part of this skill.

## Workflow

### Step 0 — Auto-Detect Mode

Check the existing project style artifact (use `.ai-style-rules.md` only if already adopted or explicitly selected). The filename below is an example, not a requirement:

| File exists? | Mode |
|---|---|
| No | **Branch A — First-time Full-Scan** |
| Yes | **Branch B — Incremental Sniff** |

Announce the mode in one line and proceed — never ask the user to pick.

### Branch A — First-time Full-Scan

**1. Measure scale, pick a scanning tier**

```bash
git ls-files | grep -cE '\.(js|ts|jsx|tsx|vue|py|go|rs|java|kt|rb|php|cs|swift|c|cpp|h)$'
```

| Tier | Source files | Strategy |
|---|---|---|
| Small | ≲ 50 | Full close-read every source |
| Medium | 50–500 | Infra layer = full read; business layer = sample 2–3 per dimension |
| Large | ≳ 500 | Strict sampling + budget cap; `--stat` summary first, then targeted reads |

**2. Scan along 4 dimensions**

1. **File Anatomy** — in-file declaration order (imports → types → main logic → helpers → export)
2. **State & Control Flow** — naming conventions for async state, pagination, flags
3. **Infrastructure** — where cross-cutting utils live (interceptors, formatters, middleware)
4. **Error Handling** — try/catch vs global interceptor vs Result return; null-check habits

**3. Apply signal-threshold noise reduction**

Before interrupting the user, evaluate signal strength:

- **Weak signal** → auto-suppress: minority <5% AND count <10 → majority wins, minority goes to DONTs
- **Strong signal** → grill: near-even split, or semantic fork on a core dimension
- **Small-project exception**: sources ≲50, "3 vs 2" is NOT a majority → grill it

**4. Resolve conflicts one at a time (Grilling Protocol)**

For each strong-signal conflict, present exactly ONE question with 4 options:

> Evidence: `pathA` uses style X, `pathB` uses style Y
> WARNING: Risk: mixing both fractures the project style
> Choose: `1` follow X  `2` follow Y  `3` this is evolution, update rules  `4` I have a new rule

Suspend until the user answers, then proceed to the next conflict. Never stack questions.

**5. If writing is in scope, update the selected advisory style artifact** with three sections:
- **[Golden Files]** — real exemplar paths annotated with what they demonstrate
- **[Naming & State-Control Rules]** — concrete, checkable conventions
- **[DONTs]** — anti-patterns that must not propagate

**6. Return scoped style guidance**

Summarize the selected exemplars and any unresolved conflicts. Keep the artifact manually referenced within the selected task. Do not install persistent hooks, edit `CLAUDE.md` or `settings.json`, or change global/session behavior. Any future policy integration is a separate explicitly authorized task, not an enforcement option of this skill.

### Branch B — Incremental Sniff

1. Read existing `.ai-style-rules.md`; if it has a commit fingerprint, `git diff <last_hash> HEAD --stat` to pinpoint delta
2. Read recent Git changes (`git log -3 --stat` → inspect suspect files on demand)
3. For oversized diffs (>hundreds of files): `--stat` summary only + sample the largest changes
4. Compare new code against recorded rules → conflicts go through Grilling Protocol
5. Append evolution log at the end of `.ai-style-rules.md` (never overwrite old rules)

### Scoped Application

Apply the accepted exemplars within the selected task, subject to canonical project instructions. When useful, provide a concise visible summary of the exemplar followed and DONTs avoided; do not mandate private reasoning disclosures or persistent per-turn behavior.

## How It Works

This skill auto-detects whether it's a first-time or incremental run via `.ai-style-rules.md` presence:

- **First-time (Branch A)** — Measures project scale, scans codebase across 4 meta-architecture dimensions (File Anatomy, State & Control Flow, Infrastructure, Error Handling), applies signal-threshold noise reduction to suppress weak conflicts, resolves strong-signal conflicts one-at-a-time with the user, generates `.ai-style-rules.md` with Golden Files / Naming Rules / DONTs, and returns scoped guidance without installing hooks.
- **Incremental (Branch B)** — Reads existing rules, checks recent Git diffs for new or conflicting patterns, runs the same one-at-a-time grilling protocol for any conflicts found, and appends evolution logs without overwriting existing rules.
- **Scoped Application** — Use accepted exemplars for the selected task; existing project instructions remain authoritative.

## Output Specification

- The explicitly selected existing project/AIDLC style artifact (with commit fingerprint + scale tier where appropriate); `.ai-style-rules.md` is an optional filename, not a new authority
- No changes to `CLAUDE.md`, hooks, settings, or global/session configuration
- Evolution logs appended as `### [YYYY-MM-DD] Style Evolution Log` entries

## Anti-Patterns

- FAIL: Do NOT skip the scale measurement step — sampling a 30-file project "starves" it; full-scanning a 5,000-file repo blows up
- FAIL: Do NOT stack multiple conflict questions at once — grilling is strictly one-at-a-time
- FAIL: Do NOT overwrite old rules in incremental mode — always append evolution logs
- FAIL: Do NOT install enforcement hooks or change project/session configuration as part of style discovery
- FAIL: Do NOT judge syntax or tech-stack quality — this skill aligns meta-architecture only
- FAIL: Do NOT copy bugs from exemplar files — reuse structure, flag defects

## Best Practices

- Announce the detected mode (first-time vs incremental) and scale tier in one line before scanning
- For large projects, read `--stat` summaries first, then targeted `Read` on suspect files
- Let the signal threshold handle noise — a 843-vs-8 naming split should auto-resolve without user interruption
- When in doubt about signal strength, lean toward asking
- Manually reference scoped style notes; any policy integration requires a separate explicitly authorized task

## Related Skills

- Optional upstream-only host suggestions: `init` and `simplify` in the [original ECC guidance](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/inherit-legacy-style/SKILL.md); they are not bundled skills or guaranteed host commands. Discover availability before use, and do not initialize policy files as part of this skill.
- [code-review](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/commands/code-review.md) (optional, upstream-only) — review diffs for correctness and style issues

## Examples

1. **First-time onboarding**
   - User: "Help me onboard AI to this older codebase without changing its style."
   - Action: Run Branch A full-scan → measure scale → scan 4 dimensions → grill conflicts → write the selected style artifact only when authorized → return scoped guidance without hooks.

2. **Incremental update after team changes**
   - User: "We added a new module; keep existing style rules intact."
   - Action: Run Branch B incremental sniff → compare Git deltas to recorded rules → grill any new conflicts → append evolution log without overwriting.

3. **Applying DONTs within a selected task**
   - User: "Make sure all new code stays consistent with the project's rules."
   - Action: Read the accepted style artifact for the selected task → reuse exemplar patterns and avoid DONTs → summarize relevant compliance when useful, without installing hooks or changing session behavior.
