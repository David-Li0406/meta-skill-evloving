---
name: testing-anti-patterns
description: |
  Use when writing or changing tests, adding mocks, or tempted to add test-only methods to production code - prevents testing mock behavior and production pollution
  Triggers: "tests", "testing anti-patterns", "test mock behavior", "test-only methods", "mocking mistakes", "improve tests", "test best practices".
---

# Testing Anti-Patterns

## Overview

Tests must verify real behavior, not mock behavior. Mocks are a means to isolate, not the thing being tested.

**Core principle:** Test what the code does, not what the mocks do.

## The Iron Laws

```
1. NEVER test mock behavior
2. NEVER add test-only methods to production classes
3. NEVER mock without understanding dependencies
```

## Anti-Pattern 1: Testing Mock Behavior

**The violation:**

```typescript
// ❌ BAD: Testing that the mock exists
test('renders sidebar', () => {
  render(<Page />);
  expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
});
```

**Why wrong:** You're verifying the mock works, not that the component works.

**The fix:**

```typescript
// ✅ GOOD: Test real component
test('renders sidebar', () => {
  render(<Page />);  // Don't mock sidebar
  expect(screen.getByRole('navigation')).toBeInTheDocument();
});
```

### Gate Function

```
BEFORE asserting on any mock element:
  Ask: "Am I testing real behavior or just mock existence?"
  IF mock existence: STOP - Delete assertion or unmock
```

## Anti-Pattern 2: Test-Only Methods in Production

**The violation:**

```typescript
// ❌ BAD: destroy() only used in tests
class Session {
  async destroy() {  // Looks like production API!
    await this._workspaceManager?.destroyWorkspace(this.id);
  }
}
```

**Why wrong:** Production class polluted with test-only code.

**The fix:**

```typescript
// ✅ GOOD: Test utilities handle cleanup
// In test-utils/
export async function cleanupSession(session: Session) {
  const workspace = session.getWorkspaceInfo();
  if (workspace) {
    await workspaceManager.destroyWorkspace(workspace.id);
  }
}
```

## Anti-Pattern 3: Mocking Without Understanding

**The violation:**

```typescript
// ❌ BAD: Mock breaks test logic
test('detects duplicate', () => {
  vi.mock('ConfigWriter');  // Prevents config write test depends on!
  await addServer(config);
  await addServer(config);  // Should throw - but won't!
});
```

**Why wrong:** Mocked method had side effect test depended on.

**The fix:**

```typescript
// ✅ GOOD: Mock at correct level
test('detects duplicate', () => {
  vi.mock('SlowNetworkCall');  // Mock only the slow part
  await addServer(config);  // Config written
  await addServer(config);  // Duplicate detected ✓
});
```

### Gate Function

```
BEFORE mocking any method:
  1. What side effects does the real method have?
  2. Does this test depend on any of those side effects?
  3. Do I fully understand what this test needs?

  IF unsure: Run test with real implementation FIRST
```

## Anti-Pattern 4: Incomplete Mocks

**The violation:**

```typescript
// ❌ BAD: Partial mock
const mockResponse = {
  status: 'success',
  data: { userId: '123' }
  // Missing: metadata that downstream code uses
};
```

**The fix:**

```typescript
// ✅ GOOD: Mirror real API completely
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' },
  metadata: { requestId: 'req-789', timestamp: 1234567890 }
};
```

## Quick Reference

| Anti-Pattern | Fix |
|--------------|-----|
| Assert on mock elements | Test real component or unmock |
| Test-only methods in production | Move to test utilities |
| Mock without understanding | Understand dependencies first |
| Incomplete mocks | Mirror real API completely |
| Tests as afterthought | TDD - tests first |

## Red Flags

- Assertion checks for `*-mock` test IDs
- Methods only called in test files
- Mock setup is >50% of test
- Test fails when you remove mock
- Mocking "just to be safe"

## Integration

**Complementary skills:**

- **test-driven-development** - TDD prevents these anti-patterns
- **testing** - General testing best practices
