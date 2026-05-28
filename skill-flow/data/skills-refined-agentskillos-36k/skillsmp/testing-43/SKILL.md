---
name: testing
description: Implements comprehensive test suite using Vitest for unit tests and Playwright for E2E tests with safety interception scenarios
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: development
---

## What I do

I maintain the test suite for the clinical pipeline. I write and run unit tests with Vitest (jsdom) and E2E tests with Playwright. I ensure >80% code coverage and specifically test "Safety Interception" scenarios.

## When to use me

Use this when:

- You need to write or run tests for the codebase
- You're verifying safety calibration triggers correctly
- You're debugging test failures or coverage gaps

## Key Concepts

- **Vitest**: Unit test framework with jsdom environment
- **Playwright**: E2E browser testing framework
- **Safety Interception**: Tests for low-confidence path routing
- **80% Coverage**: Minimum coverage requirement

## Source Files

- `tests/unit/*.test.ts`: Unit tests using Vitest
- `tests/e2e/*.spec.ts`: E2E tests using Playwright
- `tests/setup.ts`: Test polyfills and configuration
- `tests/components/*.test.tsx`: Component tests

## Code Patterns

- Unit tests: Import components, test in isolation
- E2E tests: Simulate complete user workflows
- Test setup: Polyfills for crypto, ResizeObserver

## Commands

```bash
npm run test              # Run all Vitest tests
npm run test -- path      # Run single test file
npx playwright test       # Run E2E tests
npx playwright test --ui  # Run E2E with UI mode
```

## Operational Constraints

- Maintain >80% coverage on all new code
- Write E2E scenarios for Safety Interception
- Never skip test failures - fix the code or the test
