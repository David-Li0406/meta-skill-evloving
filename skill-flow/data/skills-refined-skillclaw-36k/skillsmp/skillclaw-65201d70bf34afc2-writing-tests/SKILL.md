---
name: writing-tests
description: Use this skill when writing new tests, reviewing test quality, or improving test coverage by focusing on user-observable behavior with real dependencies.
---

# Writing Tests

**Core Philosophy:** Test user-observable behavior with real dependencies. Tests should survive refactoring when behavior is unchanged.

**Iron Laws:**

<IMPORTANT>
1. Test real behavior, not mock behavior.
2. Never add test-only methods to production code.
3. Never mock without understanding dependencies.
</IMPORTANT>

## Testing Trophy Model

Write tests in this priority order:

1. **Integration Tests (PRIMARY)** - Multiple units with real dependencies.
2. **E2E Tests (SECONDARY)** - Complete workflows across the stack.
3. **Unit Tests (RARE)** - Pure functions only (no dependencies).

**Default to integration tests.** Only drop to unit tests for pure utility functions.

## Pre-Test Workflow

BEFORE writing any tests, copy this checklist and track your progress:

```
Test Writing Progress:
- [ ] Step 1: Review project standards (check existing tests).
- [ ] Step 2: Understand behavior (what should it do? what can fail?).
- [ ] Step 3: Choose test type (Integration/E2E/Unit).
- [ ] Step 4: Identify dependencies (real vs mocked).
- [ ] Step 5: Write failing test first (TDD).
- [ ] Step 6: Implement minimal code to pass.
- [ ] Step 7: Verify coverage (happy path, errors, edge cases).
```

**Before writing any tests:**

1. **Review project standards** - Check existing test files, testing docs, or project conventions.
2. **Understand behavior** - What should this do? What can go wrong?
3. **Choose test type** - Integration (default), E2E (critical workflows), or Unit (pure functions).
4. **Identify dependencies** - What needs to be real vs mocked?

## Test Type Decision

```
Is this a complete user workflow?
  → YES: E2E test

Is this a pure function (no side effects/dependencies)?
  → YES: Unit test

Everything else:
  → Integration test (with real dependencies).
```

## Mocking Guidelines

**Default: Don't mock. Use real dependencies.**

### Only Mock These

- External HTTP/API calls.
- Time-dependent operations (timers, dates).
- Randomness (random numbers, UUIDs).
- File system I/O.
- Third-party services (payments, analytics, email).
- Network boundaries.

### Never Mock These

- Internal modules/packages.
- Database queries (use test database).
- Business logic.
- Data transformations.