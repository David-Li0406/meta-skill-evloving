---
name: test-driven-development
description: Use this skill when implementing any feature or bugfix, before writing implementation code. Enforces a test-first discipline with a strict red-green-refactor cycle.
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass. If you didn't watch the test fail, you don't know if it tests the right thing.

**Core principle:** 

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

## The RED-GREEN-REFACTOR Cycle

### 1. RED - Write a Failing Test First
- Write the smallest test that fails for the right reason.
- The test should fail because the feature doesn't exist yet.
- Run the test and verify it fails.

### 2. GREEN - Make It Pass (Minimum Code)
- Write the minimum code to make the test pass.
- Don't write more than necessary; avoid premature optimization and refactoring.

### 3. REFACTOR - Improve the Code
- Clean up the code after it passes.
- Remove duplication, improve naming, and extract methods/functions.
- Ensure all tests still pass after refactoring.

## Forbidden Rationalizations

If you catch yourself thinking any of the following, STOP:
- "This is just a simple function."
- "I'll write tests after."
- "Let me just get it working first."
- "This doesn't need a test."
- "I'll test it manually."
- "The test is obvious."
- "I'm just exploring."

## Good Tests Are:
- **Fast** - Tests should run in milliseconds.
- **Isolated** - No dependencies between tests.
- **Repeatable** - Same result every time.
- **Self-validating** - Pass or fail, no interpretation.
- **Timely** - Written before the code.

## Test Structure (Arrange-Act-Assert):
```javascript
// Arrange - Set up the test conditions
const input = createTestInput();

// Act - Execute the code under test
const result = functionUnderTest(input);

// Assert - Verify the expected outcome
expect(result).toBe(expectedValue);
```

## When to Use This Skill
- Starting any new feature.
- Fixing any bug (write a test that reproduces the bug first).
- Refactoring existing code (ensure tests exist first).
- Any code change that could break existing functionality.

## YAGNI (You Aren't Gonna Need It)
- Don't write code you don't need yet.
- Avoid speculative features and premature optimization.

## DRY (Don't Repeat Yourself)
- Focus on making it work first (GREEN), then make it right (REFACTOR).
- Duplication is acceptable temporarily; remove it during refactor.

## Commit Strategy
- Commit after each GREEN.
- Commit after each REFACTOR.
- Small, frequent commits; each commit should pass all tests.

## Verification Checklist
Before marking work complete:
- [ ] Every new function/method has a test.
- [ ] Watched each test fail before implementing.
- [ ] Each test failed for the expected reason (feature missing, not typo).
- [ ] Wrote minimal code to pass each test.
- [ ] All tests pass.
- [ ] Output pristine (no errors, warnings).
- [ ] Tests use real code (mocks only if unavoidable).
- [ ] Edge cases and errors covered.

Can't check all boxes? You skipped TDD. Start over.

## Debugging Integration
If a bug is found, write a failing test reproducing it. Follow the TDD cycle to ensure the test proves the fix and prevents regression.

## Final Rule
```
Production code → test exists and failed first
Otherwise → not TDD
```
No exceptions without the user's permission.