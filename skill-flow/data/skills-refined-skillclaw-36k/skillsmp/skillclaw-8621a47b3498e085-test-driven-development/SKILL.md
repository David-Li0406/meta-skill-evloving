---
name: test-driven-development
description: Use this skill when implementing features or fixing bugs to enforce the RED-GREEN-REFACTOR cycle, ensuring tests fail before writing production code.
---

# Test-Driven Development (TDD)

**Iron Law:** "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"

## When to Use

Use this skill when:
- Writing new features
- Fixing bugs (write a test that reproduces the bug first)
- Refactoring code (tests verify behavior preservation)
- Implementing API endpoints or business logic
- Creating UI components with testable behavior

## Rigidity Level

**LOW FREEDOM** - Follow these exact steps in order. Do not adapt. Violating the letter of the rules is violating the spirit of the rules.

## The Process

### 1. RED - Write a Failing Test

**Objective:** Specify desired behavior through a test that fails.

**Steps:**
1. Write one minimal test showing what should happen.
2. Define expected behavior clearly.
3. Use real code (avoid mocks unless unavoidable).
4. Run the test and verify it fails (if it passes, you didn't test new behavior).

### 2. GREEN - Write Minimal Code

**Objective:** Implement the simplest code necessary to pass the test.

**Steps:**
1. Write the minimal code required to make the test pass.
2. Do not add features that the test does not require.
3. Avoid refactoring other code at this stage.

### 3. REFACTOR - Clean Up Code

**Objective:** Improve the code while ensuring all tests still pass.

**Steps:**
1. Refactor the code for clarity and efficiency.
2. Run all tests to confirm they still pass.

## Quick Reference

| Phase | Action | Command Example | Expected Result |
|-------|--------|-----------------|-----------------|
| **RED** | Write failing test | `go test ./...` | FAIL (feature missing) |
| **Verify RED** | Confirm correct failure | Check error message | "function not found" or assertion fails |
| **GREEN** | Write minimal code | Implement feature | Test passes |
| **Verify GREEN** | All tests pass | `go test ./...` | All green, no warnings |
| **REFACTOR** | Clean up code | Improve while green | Tests still pass |

## Red Flags (Violation Indicators)

Watch for these patterns that indicate TDD violations:
- Implementation first: Writing production code before any test exists.
- Tests after promise: Planning to write tests later.
- Same purpose rationalization: Claiming manual testing is equivalent.
- Skipping "simple" code: Avoiding tests for "obvious" logic.
- Happy path only: Writing tests only for success cases.
- No test for changes: Modifying code without adding corresponding tests.
- "Just a small fix": Bypassing TDD for quick fixes.

If you find yourself saying "I'll test this after I get it working," you're violating TDD.