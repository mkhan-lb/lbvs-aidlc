---
name: eval-harness
description: Formal evaluation framework for Claude Code sessions implementing eval-driven development (EDD) principles. Use when a Claude Code workflow needs a formal eval before it is trusted or changed.
metadata:
  origin: ECC
disable-model-invocation: true
---

**AIDLC integration.** See [the optional ECC skill library](../../../docs/USAGE.md#12-use-the-optional-ecc-skill-library). Existing project conventions and canonical AIDLC artifacts prevail. Skill use is not authority for installs, commits, remote writes, deployment, or global/session changes. Invoke manually for the selected eval/task scope only; agree checks and any local report writes first. This is guidance, not an installed runner or release gate. Existing AIDLC verification/review artifacts and lifecycle remain authoritative.

# Eval Harness Skill

A reference workflow for evaluating Claude Code sessions using eval-driven development (EDD) principles. This skill alone supplies no execution engine, containment boundary, command registration, or scheduled maintenance.

## When to Activate

- Setting up eval-driven development (EDD) for AI-assisted workflows
- Defining pass/fail criteria for Claude Code task completion
- Measuring agent reliability with pass@k metrics
- Creating regression test suites for prompt or agent changes
- Benchmarking agent performance across model versions

## Philosophy

Eval-Driven Development treats evals as the "unit tests of AI development":
- Define expected behavior BEFORE implementation
- Run evals continuously during development
- Track regressions with each change
- Use pass@k metrics for reliability measurement

## Eval Types

### Capability Evals
Test if Claude can do something it couldn't before:
```markdown
[CAPABILITY EVAL: feature-name]
Task: Description of what Claude should accomplish
Success Criteria:
  - [ ] Criterion 1
  - [ ] Criterion 2
  - [ ] Criterion 3
Expected Output: Description of expected result
```

### Regression Evals
Ensure changes don't break existing functionality:
```markdown
[REGRESSION EVAL: feature-name]
Baseline: SHA or checkpoint name
Tests:
  - existing-test-1: PASS/FAIL
  - existing-test-2: PASS/FAIL
  - existing-test-3: PASS/FAIL
Result: X/Y passed (previously Y/Y)
```

## Grader Types

### 1. Code-Based Grader
Deterministic checks using code:
```bash
# Check if file contains expected pattern
grep -q "export function handleAuth" src/auth.ts && echo "PASS" || echo "FAIL"

# Check if tests pass
npm test -- --testPathPattern="auth" && echo "PASS" || echo "FAIL"

# Check if build succeeds
npm run build && echo "PASS" || echo "FAIL"
```

### 2. Model-Based Grader
Use Claude to evaluate open-ended outputs:
```markdown
[MODEL GRADER PROMPT]
Evaluate the following code change:
1. Does it solve the stated problem?
2. Is it well-structured?
3. Are edge cases handled?
4. Is error handling appropriate?

Score: 1-5 (1=poor, 5=excellent)
Reasoning: [explanation]
```

### 3. Human Grader
Flag for manual review:
```markdown
[HUMAN REVIEW REQUIRED]
Change: Description of what changed
Reason: Why human review is needed
Risk Level: LOW/MEDIUM/HIGH
```

## Metrics

### pass@k
"At least one success in k attempts"
- pass@1: First attempt success rate
- pass@3: Success within 3 attempts
- Typical target: pass@3 > 90%

### pass^k
"All k trials succeed"
- Higher bar for reliability
- pass^3: 3 consecutive successes
- Use for critical paths

## Eval Workflow

### 1. Define (Before Coding)
```markdown
## EVAL DEFINITION: feature-xyz

### Capability Evals
1. Can create new user account
2. Can validate email format
3. Can hash password securely

### Regression Evals
1. Existing login still works
2. Session management unchanged
3. Logout flow intact

### Success Metrics
- pass@3 > 90% for capability evals
- pass^3 = 100% for regression evals
```

### 2. Implement
Write code to pass the defined evals.

### 3. Evaluate
```bash
# Run capability evals
[Run each capability eval, record PASS/FAIL]

# Run regression evals
npm test -- --testPathPattern="existing"

# Generate report
```

### 4. Report
```markdown
EVAL REPORT: feature-xyz
========================

Capability Evals:
  create-user:     PASS (pass@1)
  validate-email:  PASS (pass@2)
  hash-password:   PASS (pass@1)
  Overall:         3/3 passed

Regression Evals:
  login-flow:      PASS
  session-mgmt:    PASS
  logout-flow:     PASS
  Overall:         3/3 passed

Metrics:
  pass@1: 67% (2/3)
  pass@3: 100% (3/3)

Status: READY FOR REVIEW
```

## Integration Patterns

The `/eval` examples below are optional upstream command syntax, not commands installed by this library. The pinned [legacy eval command shim](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/legacy-command-shims/commands/eval.md) is reference-only. First discover actual available commands/tools and their documented interfaces; if absent, stop that integration path and report it. The Define → Implement → Evaluate → Report workflow above can be performed manually with existing authorized project checks. Shell comments, bracketed steps and sample reports are illustrative, not executable graders or evidence of a run.

### Pre-Implementation
```
/eval define feature-name
```
Creates eval definition file at `.claude/evals/feature-name.md`

### During Implementation
```
/eval check feature-name
```
Runs current evals and reports status

### Post-Implementation
```
/eval report feature-name
```
Generates full eval report

## Eval Storage

Use the project's existing AIDLC artifact conventions for the selected change. The following upstream layout is an optional example, not authority to create another artifact store:
```
.claude/
  evals/
    feature-xyz.md      # Eval definition
    feature-xyz.log     # Eval run history
    baseline.json       # Regression baselines
```

## Best Practices

1. **Define evals BEFORE coding** - Forces clear thinking about success criteria
2. **Run evals frequently** - Catch regressions early
3. **Track pass@k over time** - Monitor reliability trends
4. **Use code graders when possible** - Deterministic > probabilistic
5. **Human review for security** - Never fully automate security checks
6. **Keep evals fast** - Slow evals don't get run
7. **Version evals with code** - Evals are first-class artifacts

## Example: Adding Authentication

```markdown
## EVAL: add-authentication

### Phase 1: Define (10 min)
Capability Evals:
- [ ] User can register with email/password
- [ ] User can login with valid credentials
- [ ] Invalid credentials rejected with proper error
- [ ] Sessions persist across page reloads
- [ ] Logout clears session

Regression Evals:
- [ ] Public routes still accessible
- [ ] API responses unchanged
- [ ] Database schema compatible

### Phase 2: Implement (varies)
[Write code]

### Phase 3: Evaluate
Run: /eval check add-authentication

### Phase 4: Report
EVAL REPORT: add-authentication
==============================
Capability: 5/5 passed (pass@3: 100%)
Regression: 3/3 passed (pass^3: 100%)
Status: SHIP IT
```

## Local Framework Utilities

The mechanical utilities exist only in the optional upstream [eval-harness source directory](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/lib/eval-harness) with the [CLI entry point](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/scripts/eval-harness.js); neither is bundled or installed here. The command below is an upstream-checkout example, not an available AIDLC command. These utilities are not required for the manual evaluation workflow. Do not fetch, install or execute them as a side effect of loading this skill:

```sh
node scripts/eval-harness.js example
```

- Capsule: hash-linked journal with five lineages and local integrity checks.
- Inspection: source digests, validated variant paths, and syntactic warnings.
- Replay: declared tools and content-addressed fixtures. Missing fixtures fail
  closed; SE3 and above are refused in replay. Record mode invokes the registered
  implementation, so only register trusted functions.
- Receipt: offline verification of capsule and artifact bytes, with named checks.
- Retrospective preparation: `node scripts/eval-harness.js capsule group <dir> [<dir> ...]`
  groups 1 to 100 explicitly selected, verified local capsule snapshots from one
  task family by declared harness version. Repeated snapshots count once;
  conflicting identities or invalid capsules reject the whole report. This is
  read-only record counting, with no new rollouts, scores or promotion. Use small,
  quiescent capsules. Payloads, directory arguments and raw run/capsule IDs are
  omitted, but task-family/version labels are verbatim and digest references are
  linkable; review them before sharing. Operational validation remains pending.

Candidate execution is disabled on every OS because no verified OS containment
backend is implemented. `gate run`, `runGate`, `runVariant`, direct child launch,
and the retired effect preload refuse with `gate.isolation_required`. No trust
flag or caller-supplied executor can bypass the refusal. The example records
that refusal and inspects source without executing or scoring it.

Do not present static warnings, a capsule receipt, or successful utility tests
as candidate containment or promotion evidence. A future gate requires an
independently reviewed OS boundary, protected checker and audit channels, and
fatal baseline rejection. See the pinned upstream [framework architecture](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/docs/architecture/eval-harness-frameworks.md).

## Product Evals (v1.8)

Use product evals when behavior quality cannot be captured by unit tests alone.

### Grader Types

1. Code grader (deterministic assertions)
2. Rule grader (regex/schema constraints)
3. Model grader (LLM-as-judge rubric)
4. Human grader (manual adjudication for ambiguous outputs)

### pass@k Guidance

- `pass@1`: direct reliability
- `pass@3`: practical reliability under controlled retries
- `pass^3`: stability test (all 3 runs must pass)

Recommended thresholds:
- Capability evals: pass@3 >= 0.90
- Regression evals: pass^3 = 1.00 for release-critical paths

### Eval Anti-Patterns

- Overfitting prompts to known eval examples
- Measuring only happy-path outputs
- Ignoring cost and latency drift while chasing pass rates
- Allowing flaky graders in release gates

### Minimal Eval Artifact Layout

Optional upstream example only; do not replace or duplicate canonical AIDLC verification/review artifacts. A sample `SHIP IT` status is illustrative and never authorizes deployment.

- `.claude/evals/<feature>.md` definition
- `.claude/evals/<feature>.log` run history
- `docs/releases/<version>/eval-summary.md` release snapshot
