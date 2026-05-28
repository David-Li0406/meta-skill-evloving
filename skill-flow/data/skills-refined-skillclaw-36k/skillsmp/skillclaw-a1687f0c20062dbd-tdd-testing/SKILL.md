---
name: tdd-testing
description: Use this skill when implementing features, fixing bugs, or adding test coverage by following Test-Driven Development (TDD) principles.
---

# Testing Guidelines

Follow TDD (Test-Driven Development) for all features and bug fixes. **Always write failing tests first.**

## TDD Workflow

1. **Write a failing test** that describes the expected behavior.
2. **Run the test** to confirm it fails (red).
3. **Write the minimum code** to make the test pass.
4. **Run the test** to confirm it passes (green).
5. **Refactor** while keeping tests green.

### When to Apply TDD

- **Bug fix**: Write a test that reproduces the bug first.
- **New feature**: Write a test showing the feature doesn't exist yet.
- **Refactoring**: Ensure tests exist before changing code.

## Test Types

| When                    | Test Type   | Framework  | Location                              |
| ----------------------- | ----------- | ---------- | ------------------------------------- |
| Apps/UI features        | E2E         | Playwright | `apps/{app}/e2e/`                     |
| Data functions (Prisma) | Integration | Vitest     | `apps/{app}/src/data/` or `packages/` |
| Utils/helpers           | Unit        | Vitest     | `packages/{pkg}/*.test.ts`            |

## E2E Testing (Playwright)

### Core Principle: Test User Behavior

Test what users see and do, not implementation details. If your test breaks when you refactor CSS or rename a class, it's testing the wrong thing.

### Preventing Flaky Tests

**CRITICAL: Run new tests multiple times before considering them done.** Flaky tests often pass 90% of the time but fail intermittently. After writing a new E2E test:

```bash
# Run the test 5+ times to catch flakiness
for i in {1..5}; do pnpm e2e -- -g "test name" --reporter=line; done
```

**High-risk scenarios that commonly cause flakiness:**

| Scenario                         | Risk                          | Prevention                                         |
| -------------------------------- | ----------------------------- | -------------------------------------------------- |
| Clicking dropdown/menu items     | Animations cause instability  | Wait for item visibility, use `force: true`        |
| Actions that trigger navigation  | Page reload detaches elements | Use `waitForLoadState` or `waitForURL` after click |
| Form submissions                 | Async save operations         | Ensure proper handling of async behavior            |