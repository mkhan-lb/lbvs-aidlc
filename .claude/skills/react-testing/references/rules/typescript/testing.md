---
paths:
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.js"
  - "**/*.jsx"
---

> AIDLC reference only: this bundled ECC rule is not installed as a project rule. Existing project conventions and canonical AIDLC artifacts prevail; use within the selected task, without automatic installs, CI changes, hooks, or session changes.

# TypeScript/JavaScript Testing

> This file extends [common/testing.md](../common/testing.md) with TypeScript/JavaScript specific content.

## E2E Testing

Use the project’s existing E2E framework for critical user flows; **Playwright** is the upstream example, not a migration requirement.

## Agent Support

- [e2e-runner](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/agents/e2e-runner.md) (optional, upstream-only) - Playwright E2E testing specialist; do not assume it is available
