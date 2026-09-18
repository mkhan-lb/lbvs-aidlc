---
name: gan-style-harness
description: "GAN-inspired Generator-Evaluator agent harness for building high-quality applications autonomously. Based on Anthropic's March 2026 harness design paper. Use when a feature should be built autonomously through generator and evaluator iteration until it clears a quality bar."
metadata:
  origin: ECC-community
disable-model-invocation: true
---

**AIDLC integration.** See [the optional ECC skill library](../../../docs/USAGE.md#12-use-the-optional-ecc-skill-library). Existing project conventions and canonical AIDLC artifacts prevail. Skill use is not authority for installs, commits, remote writes, deployment, or global/session changes. Invoke manually for the selected feature, agreed iteration limit, rubric and permitted local changes. This imports a design pattern, not an autonomous harness, agents or commands. Existing AIDLC planning/reviewer workflows and canonical artifacts remain authoritative; a score is not approval to ship.

# GAN-Style Harness Skill

> Inspired by [Anthropic's Harness Design for Long-Running Application Development](https://www.anthropic.com/engineering/harness-design-long-running-apps) (March 24, 2026)

A multi-agent design pattern that separates **generation** from **evaluation**, creating an adversarial feedback loop. This imported skill contains guidance only: it does not register agents, launch processes, or implement an orchestrator.

## Core Insight

> When asked to evaluate their own work, agents are pathological optimists — they praise mediocre output and talk themselves out of legitimate issues. But engineering a **separate evaluator** to be ruthlessly strict is far more tractable than teaching a generator to self-critique.

This is the same dynamic as GANs (Generative Adversarial Networks): the Generator produces, the Evaluator critiques, and that feedback drives the next iteration.

## When to Use

- Building complete applications from a one-line prompt
- Frontend design tasks requiring high visual quality
- Full-stack projects that need working features, not just code
- Any task where "AI slop" aesthetics are unacceptable
- Projects where you want to invest $50-200 for production-quality output

## When NOT to Use

- Quick single-file fixes (use standard `claude -p`)
- Tasks with tight budget constraints (<$10)
- Simple refactoring (use de-sloppify pattern instead)
- Tasks that are already well-specified with tests (use TDD workflow)

## Architecture

```
                    ┌─────────────┐
                    │   PLANNER   │
                    │  (Sonnet)   │
                    └──────┬──────┘
                           │ Product Spec
                           │ (features, sprints, design direction)
                           ▼
              ┌────────────────────────┐
              │                        │
              │   GENERATOR-EVALUATOR  │
              │      FEEDBACK LOOP     │
              │                        │
              │  ┌──────────┐          │
              │  │GENERATOR │--build-->│──┐
              │  │ (Sonnet) │          │  │
              │  └────▲─────┘          │  │
              │       │                │  │ live app
              │    feedback             │  │
              │       │                │  │
              │  ┌────┴─────┐          │  │
              │  │EVALUATOR │<-test----│──┘
              │  │ (Sonnet) │          │
              │  │+Playwright│         │
              │  └──────────┘          │
              │                        │
              │   5-15 iterations      │
              └────────────────────────┘
```

## The Three Agents

These are roles, not guaranteed installed agent types. Discover actual available agents, tool schemas and browser capabilities before delegation; stop the unavailable path and report gaps rather than inventing an agent or successful evaluation. Use the user-selected session/provider configuration: upstream model names, environment variables and cost estimates below are reference examples, not overrides or measured guarantees.

### 1. Planner Agent

**Role:** Product manager — expands a brief prompt into a full product specification.

**Key behaviors:**
- Proposes a specification within the selected scope; a larger multi-feature or multi-sprint expansion needs user agreement
- Defines user stories, technical requirements, and visual design direction
- Can propose ambitious options, but does not silently expand the agreed requirements
- Produces evaluation criteria that the Evaluator will use later

**Upstream model example:** Sonnet; `GAN_PLANNER_MODEL` belongs to the optional upstream runner, not this skill. Do not change the selected session model.

### 2. Generator Agent

**Role:** Developer — implements features according to the spec.

**Key behaviors:**
- Works in structured sprints (or continuous mode with newer models)
- Negotiates a "sprint contract" with the Evaluator before writing code
- Uses full-stack tooling: React, FastAPI/Express, databases, CSS
- Respects the existing working tree; commits, staging and other version-control mutations need separate authority
- Reads Evaluator feedback and incorporates it in next iteration

**Upstream model example:** Sonnet; `GAN_GENERATOR_MODEL` belongs to the optional upstream runner, not this skill. Do not change the selected session model.

### 3. Evaluator Agent

**Role:** QA engineer — tests the live running application, not just code.

**Key behaviors:**
- Uses **Playwright MCP** to interact with the live application
- Clicks through features, fills forms, tests API endpoints
- Scores against four criteria (configurable):
  1. **Design Quality** — Does it feel like a coherent whole?
  2. **Originality** — Custom decisions vs. template/AI patterns?
  3. **Craft** — Typography, spacing, animations, micro-interactions?
  4. **Functionality** — Do all features actually work?
- Returns structured feedback with scores and specific issues
- Is engineered to be **ruthlessly strict** — never praises mediocre work

**Upstream model example:** Sonnet; `GAN_EVALUATOR_MODEL` belongs to the optional upstream runner, not this skill. Do not change the selected session model.

## Evaluation Criteria

The default four criteria, each scored 1-10:

```markdown
## Evaluation Rubric

### Design Quality (weight: 0.3)
- 1-3: Generic, template-like, "AI slop" aesthetics
- 4-6: Competent but unremarkable, follows conventions
- 7-8: Distinctive, cohesive visual identity
- 9-10: Could pass for a professional designer's work

### Originality (weight: 0.2)
- 1-3: Default colors, stock layouts, no personality
- 4-6: Some custom choices, mostly standard patterns
- 7-8: Clear creative vision, unique approach
- 9-10: Surprising, delightful, genuinely novel

### Craft (weight: 0.3)
- 1-3: Broken layouts, missing states, no animations
- 4-6: Works but feels rough, inconsistent spacing
- 7-8: Polished, smooth transitions, responsive
- 9-10: Pixel-perfect, delightful micro-interactions

### Functionality (weight: 0.2)
- 1-3: Core features broken or missing
- 4-6: Happy path works, edge cases fail
- 7-8: All features work, good error handling
- 9-10: Bulletproof, handles every edge case
```

### Scoring

- **Weighted score** = sum of (criterion_score * weight)
- **Pass threshold** = 7.0 (configurable)
- **Max iterations** = 15 (configurable, typically 5-15 sufficient)

## Usage

### Manual use in AIDLC

1. Select the canonical feature artifacts, permitted edits/checks, iteration limit and rubric with the user. Reuse the existing plan; do not create a competing product spec.
2. Use an actually available implementation/reviewer route, keeping generator and evaluator roles separate. Supply the real requirements, changes and prior feedback through the supported context channel. If independent evaluation is unavailable, stop and report that gap.
3. Run only authorized checks against the chosen local/test surface. Browser availability is not permission to submit production forms, create records or make purchases. Starting a server and writing feedback must be in the selected scope.
4. Record observed evidence, failed/not-run checks and rubric scores; a prompt, shell comment, launch or generated report is not proof that the evaluator ran. Reuse AIDLC review artifacts and save only when requested.
5. Make approved fixes and repeat within the agreed limit. Stop at the threshold, iteration limit, unavailable capability or plateau; return remaining issues for a user decision. No automatic commit, deployment, context reset or provider reconfiguration.

The following command/script/CLI examples are **optional upstream-only usage**, not installed entry points. References: [gan-build command](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/commands/gan-build.md), [gan-design command](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/commands/gan-design.md), [GAN shell runner](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/gan-harness.sh), and the [planner](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/agents/gan-planner.md), [generator](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/agents/gan-generator.md) and [evaluator](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/agents/gan-evaluator.md) agents. They are not required for the manual procedure above and must not be installed or run implicitly. The upstream shell runner includes automatic Git initialization and commit prompts; it is not an AIDLC-safe default. Discover real interfaces and obtain separate scope before selecting any external runner.

### Via Command

```bash
# Full three-agent harness
/project:gan-build "Build a project management app with Kanban boards, team collaboration, and dark mode"

# With custom config
/project:gan-build "Build a recipe sharing platform" --max-iterations 10 --pass-threshold 7.5

# Frontend design mode (generator + evaluator only, no planner)
/project:gan-design "Create a landing page for a crypto portfolio tracker"
```

### Via Shell Script

```bash
# Basic usage
./scripts/gan-harness.sh "Build a music streaming dashboard"

# With options
GAN_MAX_ITERATIONS=10 \
GAN_PASS_THRESHOLD=7.5 \
GAN_EVAL_CRITERIA="functionality,performance,security" \
./scripts/gan-harness.sh "Build a REST API for task management"
```

### Via Claude Code (upstream illustrative sequence)

The `PLANNER_PROMPT.md` and `EVALUATOR_PROMPT.md` names below are illustrative user-supplied prompt files, not bundled resources. The role descriptions and rubric above provide manual guidance; do not assume these filenames or a CLI/browser tool interface exists. These examples do not authorize model changes or unattended permission grants.

```bash
# Step 1: Plan
claude -p --model sonnet "You are a Product Planner. Read PLANNER_PROMPT.md. Expand this brief into a full product spec: 'Build a Kanban board app'. Write spec to spec.md"

# Step 2: Generate (iteration 1)
claude -p --model sonnet "You are a Generator. Read spec.md. Implement Sprint 1. Start the dev server on port 3000."

# Step 3: Evaluate (iteration 1)
claude -p --model sonnet "You are an Evaluator. Read EVALUATOR_PROMPT.md. Test the live app at http://localhost:3000. Score against the rubric. Write feedback to feedback-001.md"

# Step 4: Generate (iteration 2 — reads feedback)
claude -p --model sonnet "You are a Generator. Read spec.md and feedback-001.md. Address all issues. Improve the scores."

# Repeat steps 3-4 until pass threshold met
```

## Evolution Across Model Capabilities

The harness should simplify as models improve. Following Anthropic's evolution:

### Stage 1 — Weaker Models (Sonnet-class)
- Full sprint decomposition required
- Context resets between sprints (avoid context anxiety)
- 2-agent minimum: Initializer + Coding Agent
- Heavy scaffolding compensates for model limitations

### Stage 2 — Capable Models (Opus 4.5-class)
- Full 3-agent harness: Planner + Generator + Evaluator
- Sprint contracts before each implementation phase
- 10-sprint decomposition for complex apps
- Context resets still useful but less critical

### Stage 3 — Frontier Models (Opus 4.6-class)
- Simplified harness: single planning pass, continuous generation
- Evaluation reduced to single end-pass (model is smarter)
- No sprint structure needed
- Automatic compaction handles context growth

> **Key principle:** Every harness component encodes an assumption about what the model can't do alone. When models improve, re-test those assumptions. Strip away what's no longer needed.

## Configuration

### Environment Variables

Upstream runner reference only: none of these variables is read or set by this imported skill. Inspect the optional runner's actual implementation before use; a documented variable is not proof that the runner consumes it.

| Variable | Default | Description |
|----------|---------|-------------|
| `GAN_MAX_ITERATIONS` | `15` | Maximum generator-evaluator cycles |
| `GAN_PASS_THRESHOLD` | `7.0` | Weighted score to pass (1-10) |
| `GAN_PLANNER_MODEL` | `sonnet` | Model for planning agent |
| `GAN_GENERATOR_MODEL` | `sonnet` | Model for generator agent |
| `GAN_EVALUATOR_MODEL` | `sonnet` | Model for evaluator agent |
| `GAN_EVAL_CRITERIA` | `design,originality,craft,functionality` | Comma-separated criteria |
| `GAN_DEV_SERVER_PORT` | `3000` | Port for the live app |
| `GAN_DEV_SERVER_CMD` | `npm run dev` | Command to start dev server |
| `GAN_PROJECT_DIR` | `.` | Project working directory |
| `GAN_SKIP_PLANNER` | `false` | Skip planner, use spec directly |
| `GAN_EVAL_MODE` | `playwright` | `playwright`, `screenshot`, or `code-only` |

### Evaluation Modes

| Mode | Tools | Best For |
|------|-------|----------|
| `playwright` | Browser MCP + live interaction | Full-stack apps with UI |
| `screenshot` | Screenshot + visual analysis | Static sites, design-only |
| `code-only` | Tests + linting + build | APIs, libraries, CLI tools |

## Anti-Patterns

1. **Evaluator too lenient** — If the evaluator passes everything on iteration 1, your rubric is too generous. Tighten scoring criteria and add explicit penalties for common AI patterns.

2. **Generator ignoring feedback** — Ensure feedback is passed as a file, not inline. The generator should read `feedback-NNN.md` at the start of each iteration.

3. **Infinite loops** — Always set `GAN_MAX_ITERATIONS`. If the generator can't improve past a score plateau after 3 iterations, stop and flag for human review.

4. **Evaluator testing superficially** — The evaluator must use Playwright to **interact** with the live app, not just screenshot it. Click buttons, fill forms, test error states.

5. **Evaluator praising its own fixes** — Never let the evaluator suggest fixes and then evaluate those fixes. The evaluator only critiques; the generator fixes.

6. **Context exhaustion** — Surface the limitation and let the user select supported session controls; this skill does not authorize SDK configuration or context resets.

## Results: What to Expect

Upstream illustrative comparison attributed to Anthropic, not reproduced or verified by this import; it is not a guarantee of cost, quality or production readiness:

| Metric | Solo Agent | GAN Harness | Improvement |
|--------|-----------|-------------|-------------|
| Time | 20 min | 4-6 hours | 12-18x longer |
| Cost | $9 | $125-200 | 14-22x more |
| Quality | Barely functional | Production-ready | Phase change |
| Core features | Broken | All working | N/A |
| Design | Generic AI slop | Distinctive, polished | N/A |

**The tradeoff is clear:** ~20x more time and cost for a qualitative leap in output quality. This is for projects where quality matters.

## References

- [Anthropic: Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Original paper by Prithvi Rajasekaran
- [Epsilla: The GAN-Style Agent Loop](https://www.epsilla.com/blogs/anthropic-harness-engineering-multi-agent-gan-architecture) — Architecture deconstruction
- [Martin Fowler: Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) — Broader industry context
- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/) — OpenAI's parallel work
