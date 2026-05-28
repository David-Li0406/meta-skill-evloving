---
name: Development
description: Implement features using strict test-driven development. Use for the DEVELOP phase of XP workflow.
---

# Development (TDD)

## Core Rules (Non-Negotiable)

1. **NEVER write production code without a failing test first**
2. One behaviour per test
3. Write minimum code to make the test pass
4. Run tests and verify green state before proceeding

## The TDD Cycle

```
🔴 RED    → Write ONE failing test
🟢 GREEN  → Write MINIMUM code to pass
✅ VERIFY → Run all tests, confirm green
```

## Detailed Steps

### 🔴 RED — Write a Failing Test

1. Identify the next behaviour to implement
2. Write a test that specifies that behaviour
3. Run the test — it MUST fail
4. If it passes, you've either:
   - Written the wrong test, or
   - The behaviour already exists

### 🟢 GREEN — Make It Pass

1. Write the simplest code that makes the test pass
2. Do not write more than necessary
3. Do not refactor yet
4. Run the test — it MUST pass

### ✅ VERIFY — Confirm Green State

1. Run ALL tests, not just the new one
2. All tests must pass
3. If any fail, fix before continuing

## What Counts as "Minimum Code"

- Hard-coded values are acceptable initially
- Duplication is acceptable initially
- "Ugly" code is acceptable initially
- Refactoring comes AFTER green using the refactoring skill

## Test Naming

Use descriptive names that document behaviour:

```scala
// Good
"return empty list when library has no books"
"return error when member not found"

// Bad
"test1"
"testGetBooks"
```

## Announcing Progress

```
🔴 RED → [behaviour being tested]
🟢 GREEN → Test passes
✅ VERIFY → All tests green
```

## Common Mistakes

- Writing production code before the test
- Writing multiple tests before making any pass
- Refactoring while still red
- Skipping the verify step
- Writing tests that test implementation, not behaviour
