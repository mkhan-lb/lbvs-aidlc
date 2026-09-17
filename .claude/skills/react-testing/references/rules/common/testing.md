> AIDLC reference only: this bundled ECC rule is not installed as a project rule. Existing project conventions and canonical AIDLC artifacts prevail; use within the selected task, without automatic installs, CI changes, hooks, or session changes.

# Testing Requirements

## Illustrative Test Coverage Target: 80%

The existing project’s coverage policy prevails; this reference does not install a CI gate.

Test types to select according to the changed behavior and existing project policy:
1. **Unit Tests** - Individual functions, utilities, components
2. **Integration Tests** - API endpoints, database operations
3. **E2E Tests** - Critical user flows (framework chosen per language)

## Test-Driven Development

When test-first work is appropriate under project conventions:
1. Write test first (RED)
2. Run test - it should FAIL
3. Write minimal implementation (GREEN)
4. Run test - it should PASS
5. Refactor (IMPROVE)
6. Verify the relevant behavior and the project’s coverage policy

## Troubleshooting Test Failures

1. Investigate inline, or use the optional upstream tdd-guide only if actually available and authorized
2. Check test isolation
3. Verify mocks are correct
4. Fix implementation, not tests (unless tests are wrong)

## Agent Support

- [tdd-guide](https://github.com/affaan-m/everything-claude-code/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/agents/tdd-guide.md) (optional, upstream-only) - optional test-first guidance; no assumed agent availability

## Test Structure (AAA Pattern)

Prefer Arrange-Act-Assert structure for tests:

```typescript
test('calculates similarity correctly', () => {
  // Arrange
  const vector1 = [1, 0, 0]
  const vector2 = [0, 1, 0]

  // Act
  const similarity = calculateCosineSimilarity(vector1, vector2)

  // Assert
  expect(similarity).toBe(0)
})
```

### Test Naming

Use descriptive names that explain the behavior under test:

```typescript
test('returns empty array when no markets match query', () => {})
test('throws error when API key is missing', () => {})
test('falls back to substring search when Redis is unavailable', () => {})
```
