---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code
---

# Test-Driven Development (TDD)

## Testing Strategy

### Test Types
1. **Unit Tests**: Business logic, utilities, helpers.
2. **Component Tests**: UI component behavior (rendering, props).
3. **Integration Tests**: Feature flows and service interactions.
4. **E2E Tests**: Critical user journeys (login, checkout, etc.).

### Testing Tools
- **Unit/Component**: Jest, React Testing Library (RTL), Flutter Test.
- **E2E**: Detox (React Native), Appium, or Flutter Integration Test.
- **Coverage**: Aim for **80% minimum** code coverage.

### Test Structure
- **Naming**: Use descriptive test names that explain the *scenario* and *expected result*.
- **AAA Pattern**: Follow **Arrange** (setup), **Act** (execute), **Assert** (verify).
- **Mocking**: Mock external dependencies (APIs, DBs) to isolate the unit under test.
- **Scenarios**: Test happy paths, edge cases, and error scenarios.

### What to Test
- **Rendering**: Components render correctly with different props/states.
- **Interactions**: Tap, swipe, text input, form submission.
- **Integration**: API calls (mocked) and data parsing.
- **Navigation**: Correct screens are pushed/popped.
- **Logic**: State management reducers/providers and form validation.

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions:**
- Throwaway prototypes
- Generated code
- Configuration files

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

## Red-Green-Refactor

1. **RED:** Write one minimal test showing what should happen. Run it. Confirm it fails for the right reason.
2. **GREEN:** Write simplest code to pass the test. Run it. Confirm it passes.
3. **REFACTOR:** Clean up code. Confirm tests still pass.

## Good Tests

- **Minimal:** One thing per test.
- **Clear:** Name describes behavior.
- **Shows intent:** Demonstrates desired API.

## Why Order Matters

Tests written after implementation:
- Might test wrong thing
- Might test implementation, not behavior
- Might miss edge cases you forgot
- You never saw it catch the bug

**Test-first forces you to see the test fail, proving it actually tests something.**

## Common Rationalizations (Ignore These)

- "Too simple to test" -> Simple code breaks.
- "I'll test after" -> Proof of nothing.
- "I already manually tested" -> Ad-hoc, not repeatable.
- "Deleting implementation is wasteful" -> Keeping unverified code is technical debt.

## Red Flags - STOP and Start Over

- Code before test
- Test after implementation
- Test passes immediately
- Can't explain why test failed
- "I already manually tested it"

**All of these mean: Delete code. Start over with TDD.**

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
