---
name: vitest
# prettier-ignore
description: Use when writing or modifying Vitest tests to follow best practices for test structure, assertions, mocking, and coverage
---

# Vitest Testing

## Quick Start

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('MyModule', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should handle basic case', () => {
    expect(myFunction('input')).toBe('expected');
  });

  it('should throw on invalid input', () => {
    expect(() => myFunction(null)).toThrow('Invalid input');
  });
});
```

## Core Patterns

- **Structure**: `describe` for grouping, `it` for individual tests
- **Assertions**: `expect(value).toBe()`, `.toEqual()`, `.toMatchObject()`, `.toThrow()`
- **Async**: `async/await` or return Promise; use `vi.waitFor()` for polling
- **Mocking**: `vi.fn()`, `vi.spyOn()`, `vi.mock('module')`
- **Setup/Teardown**: `beforeEach`, `afterEach`, `beforeAll`, `afterAll`
- **Snapshots**: `expect(value).toMatchSnapshot()`, update with `-u` flag

## Best Practices

- One assertion concept per test (multiple expects OK if testing same behavior)
- Use descriptive test names: "should [action] when [condition]"
- Avoid test interdependence; each test should be isolated
- Mock external dependencies (APIs, file system, time)
- Use `vi.useFakeTimers()` for time-dependent tests

## Reference Files

- [references/assertions.md](references/assertions.md) - Complete assertion API
- [references/mocking.md](references/mocking.md) - Mocking strategies
- [references/async.md](references/async.md) - Async testing patterns
