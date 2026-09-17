---
name: canary-watch
description: Use this skill to monitor and verify a deployed URL after releases — checks HTTP endpoints, SSE streams, static assets, console errors, and performance regressions after deploys, merges, or dependency upgrades. Smoke / canary / post-deploy verification.
metadata:
  origin: ECC
disable-model-invocation: true
---

**AIDLC integration:** See [optional ECC skill library](../../../docs/USAGE.md#12-use-the-optional-ecc-skill-library). Existing project conventions and canonical AIDLC artifacts prevail. Skill use is not authority for installs, commits, remote writes, deployment or global/session changes. Invoke manually. Select the target URL/endpoints, credentials and a bounded check window; sustained monitoring, notifications and saved logs require separate authorization.

# Canary Watch — Post-Deploy Monitoring

## When to Use

- After deploying to production or staging
- After merging a risky PR
- When you want to verify a fix actually fixed it
- Continuous monitoring during a launch window
- After dependency upgrades

## How It Works

Checks a user-selected deployed URL for regressions. Default to one pass. A sustained watch requires an explicitly selected duration, interval, request limit and stop condition, plus an existing supervised runtime that can enforce them. If that capability is unavailable, stop and report the limitation; do not create a scheduler, hook or detached service.

Discover the actual HTTP, browser, network and performance tools exposed in this session before use. Do not assume a monitoring executable exists. Restrict requests to approved URLs/endpoints and safe interactions; do not submit forms, trigger jobs, or change production data. Bound SSE connections by timeout and close them after the requested initial event/heartbeat. Report unsupported checks and absent baselines as not measured; never infer healthy status from skipped checks.

### What It Watches

```
1. HTTP Status — is the page returning 200?
2. Console Errors — new errors that weren't there before?
3. Network Failures — failed API calls, 5xx responses?
4. Performance — LCP/CLS/INP regression vs baseline?
5. Content — did key elements disappear? (h1, nav, footer, CTA)
6. API Health — are critical endpoints responding within SLA?
7. Static Assets — are JS, CSS, image, and font requests returning 2xx/3xx with expected content types?
8. SSE Streams — do event-stream endpoints connect and receive an initial event or heartbeat?
```

### Watch Modes

The slash-command examples below describe manual skill arguments, not a bundled CLI or scheduler. Use only the checks and tools actually available.

**Quick check** (default): single pass, report results
```
/canary-watch https://myapp.com
```

**Sustained watch**: check every N minutes for M hours
```
/canary-watch https://myapp.com --interval 5m --duration 2h
```

**Diff mode**: compare staging vs production
```
/canary-watch --compare https://staging.myapp.com https://myapp.com
```

### Alert Thresholds

```yaml
critical:  # immediate alert
  - HTTP status != 200
  - Console error count > 5 (new errors only)
  - LCP > 4s
  - API endpoint returns 5xx
  - Static asset returns 4xx/5xx
  - SSE endpoint cannot connect or drops before first heartbeat

warning:   # flag in report
  - LCP increased > 500ms from baseline
  - CLS > 0.1
  - New console warnings
  - Response time > 2x baseline
  - Static asset content type changed unexpectedly
  - SSE heartbeat latency > 2x baseline

info:      # log only
  - Minor performance variance
  - New network requests (third-party scripts added?)
```

### Notifications

When a critical threshold is crossed, report it in the current response. Desktop notifications and Slack/Discord webhooks are optional side effects requiring explicit destination/content authorization and an already available capability. Save logs only to a user-approved project-local artifact path, with credentials and sensitive payloads redacted; never write a global home-directory log automatically.

## Output

```markdown
## Canary Report — myapp.com — 2026-03-23 03:15 PST

### Status: HEALTHY ✓

| Check | Result | Baseline | Delta |
|-------|--------|----------|-------|
| HTTP | 200 ✓ | 200 | — |
| Console errors | 0 ✓ | 0 | — |
| LCP | 1.8s ✓ | 1.6s | +200ms |
| CLS | 0.01 ✓ | 0.01 | — |
| API /health | 145ms ✓ | 120ms | +25ms |
| Static assets | 42/42 ✓ | 42/42 | — |
| SSE /events | connected ✓ | connected | +80ms heartbeat |

### No regressions detected. Deploy is clean.
```

## Integration

Optional companion: [upstream browser-qa](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/browser-qa/SKILL.md) for pre-deploy verification. It is not bundled here and its command/tool availability is not assumed. This import adds no PostToolUse hook, CI job or automatic post-push check. Propose CI integration only as a separate user-requested change under the project deployment policy.
