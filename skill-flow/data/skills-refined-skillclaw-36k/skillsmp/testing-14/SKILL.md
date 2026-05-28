---
name: testing
description: Guidelines for running and writing unit and E2E tests. Use this when asked to run tests, write tests, debug test failures, or verify code changes. Also use this before performing any merge commands or pushing code.
---

# Testing Guidelines

## Core Philosophy

### Test Core Functionality, Not Everything

- Focus on critical user paths and essential business logic
- Prioritize tests that catch regressions in key features
- Avoid over-testing trivial functionality or implementation details
- Ask: "If this breaks, will users notice?" - if yes, test it

### Tests Must Pass Before Commit/Merge

- All existing tests must pass before committing changes
- Never skip or disable tests without explicit justification
- Broken tests block merges - fix them, don't ignore them
- Run the full test suite, not just tests for changed code

### Tests Are Production Code

- Apply the same code quality standards to tests as production code
- Use clear, descriptive names that explain what is being tested
- Keep tests maintainable, readable, and well-organized
- Include type hints, proper formatting, and meaningful comments
- Refactor tests when they become brittle or hard to understand

## Running Tests

**Always use the provided shell scripts:**

```bash
# Linux/macOS/Codespaces
./scripts/run-server-tests.sh    # Unit tests (backend)
./scripts/run-e2e-tests.sh       # E2E tests (frontend)

# Windows (PowerShell)
.\scripts\run-server-tests.ps1   # Unit tests (backend)
.\scripts\run-e2e-tests.ps1      # E2E tests (frontend)
```

These scripts handle environment setup, dependencies, and proper configuration.

## Before Creating New Tests

1. **Check existing coverage** - avoid duplication
2. **Review existing test patterns** - follow established conventions
3. **Identify the right test type** - unit for logic, E2E for user flows

## Test Quality Standards

- **Deterministic** - Same result every run, no flaky tests
- **Independent** - No dependencies between tests
- **Fast** - Optimize for quick feedback loops
- **Focused** - One logical assertion per test
- **Descriptive** - Test names should read like specifications

## Pre-Commit Checklist

1. Run unit tests: `./scripts/run-server-tests.sh` (or `.\scripts\run-server-tests.ps1` on Windows)
2. Run E2E tests (if UI changed): `./scripts/run-e2e-tests.sh` (or `.\scripts\run-e2e-tests.ps1` on Windows)
3. Verify new functionality has appropriate test coverage
4. Confirm no tests were broken or skipped
