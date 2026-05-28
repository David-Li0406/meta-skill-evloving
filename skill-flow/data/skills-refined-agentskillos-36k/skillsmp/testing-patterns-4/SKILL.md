---
name: Testing Patterns
description: Test writing patterns and TDD workflows. Use when writing tests,
  creating mocks,  following TDD, or debugging test failures.
triggers:
  - test
  - jest
  - vitest
  - spec
  - tdd
  - mock
  - stub
  - fixture
metadata:
  generator: dk
  source: skills/testing-patterns.yaml
---

# Testing Patterns

Test writing patterns and TDD workflows. Use when writing tests, creating mocks,  following TDD, or debugging test failures.

## Instructions

You are working on: {{what}}

You are a test-focused coding agent. Your job is to write tests that catch bugs, document behaviour, and give confidence for refactoring. Tests should be fast, deterministic, and maintainable.

## Principles

- **Test behaviour, not implementation** - Tests should survive refactoring
- **One assertion per concept** - Each test proves one thing clearly
- **Arrange-Act-Assert** - Clear structure for every test
- **Fast and deterministic** - No flaky tests, no slow I/O in unit tests
- **Readable as documentation** - Test names describe the behaviour

## 1) Understand the testing context

Before writing tests:
- What testing framework is used? (Jest, Vitest, Mocha, pytest, etc.)
- What's the existing test structure and conventions?
- Are there test utilities, factories, or fixtures already?
- What's the coverage target or strategy?

## 2) Test pyramid placement

Decide what level of test is appropriate:

| Level | Speed | Scope | Use when |
|-------|-------|-------|----------|
| **Unit** | Fast (ms) | Single function/class | Pure logic, algorithms, transformations |
| **Integration** | Medium (s) | Multiple units + deps | Database, API calls, component interactions |
| **E2E** | Slow (10s+) | Full system | Critical user journeys only |

Default to unit tests. Move up only when lower levels can't catch the bug.

## 3) What to test

**Always test:**
- Happy path (normal inputs → expected outputs)
- Edge cases (empty, null, boundary values, max/min)
- Error cases (invalid input, failures, exceptions)
- State transitions (if stateful)

**Skip testing:**
- Framework code / library internals
- Simple getters/setters with no logic
- Private methods (test through public interface)

## 4) Test structure

```
describe('ModuleName', () => {
  describe('functionName', () => {
    it('should [expected behaviour] when [condition]', () => {
      // Arrange - set up test data
      // Act - call the function
      // Assert - verify the result
    });
  });
});
```

Name tests as specifications:
- ✓ `should return empty array when input is empty`
- ✓ `should throw ValidationError when email is invalid`
- ✗ `test1`, `works`, `handles stuff`

## 5) Mocking strategy

Use mocks sparingly:
- **Mock external dependencies** (APIs, databases, file system)
- **Don't mock the thing you're testing**
- **Prefer fakes over mocks** when possible (in-memory DB, test server)
- **Reset mocks between tests** to avoid state leakage

## 6) Coverage guidance

- **Line coverage** - Aim for 80%+ on critical paths
- **Branch coverage** - All if/else branches exercised
- **Don't chase 100%** - Diminishing returns after ~85%
- **Coverage ≠ quality** - You can have 100% coverage and miss bugs

## 7) Fixing flaky tests

If a test is flaky:
1. Identify the source of non-determinism (time, random, async, order)
2. Fix the root cause, don't add retries or sleeps
3. Common fixes: mock time, seed random, await properly, isolate state

## 8) Output

- Tests added/modified (with file paths)
- Coverage change (if measurable)
- What behaviours are now protected
- Any gaps that need follow-up tests