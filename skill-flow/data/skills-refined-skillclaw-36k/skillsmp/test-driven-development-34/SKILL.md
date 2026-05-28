---
name: test-driven-development
description: "Use for ALL code changes - new features, bug fixes, refactoring. Write the test first, watch it fail, then write minimal code to pass."
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (ask user first):**
- Throwaway prototypes
- Generated code
- Configuration files

Thinking "skip TDD just this once"? Stop. That's rationalization.

## Red-Green-Refactor

```
┌─────────────────────────────────────────────────────────┐
│  RED           →        GREEN         →      REFACTOR  │
│  Write failing      Minimal code           Clean up    │
│  test               to pass                            │
└─────────────────────────────────────────────────────────┘
                           ↑                     │
                           └─────────────────────┘
                              Stay GREEN
```

### RED - Write Failing Test
1. Write test for ONE behavior
2. Test MUST fail (not compile error - real failure)
3. Failure message should be clear

### Verify RED - Watch It Fail
1. Run the test
2. Verify it fails FOR THE RIGHT REASON
3. If wrong failure, fix test first

### GREEN - Minimal Code
1. Write ONLY code to make test pass
2. No extra features
3. No "while I'm here" additions
4. Ugly is OK - refactor comes next

### Verify GREEN - Watch It Pass
1. Run the test
2. Verify ALL tests still pass
3. If anything fails, fix immediately

### REFACTOR - Clean Up
1. Improve code quality
2. Keep tests GREEN
3. Run tests after EVERY change

## Good Tests

- **Fast** - Milliseconds, not seconds
- **Isolated** - No shared state between tests
- **Repeatable** - Same result every run
- **Self-validating** - Pass or fail, no interpretation
- **Timely** - Written before production code

## Red Flags - STOP and Start Over

| You're Doing This | Do This Instead |
|-------------------|-----------------|
| Writing code first | Delete it, write test |
| Test passes immediately | Test is wrong, fix it |
| Multiple behaviors in one test | Split into separate tests |
| Test depends on other tests | Isolate properly |
| "I'll add tests later" | No. Stop. Test first. |

## Testing Anti-Patterns

Avoid:
- **Testing implementation** - Test behavior, not internals
- **Brittle tests** - Don't assert on things that shouldn't matter
- **Slow tests** - Mock external dependencies
- **Flaky tests** - No randomness, no timing dependencies
- **Test pollution** - Clean up after yourself

## Final Rule

**When in doubt, write another test.**
