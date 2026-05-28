---
name: test-driven-development
description: Use this skill when implementing features, fixing bugs, or refactoring code by following the RED-GREEN-REFACTOR cycle.
---

# Test-Driven Development (TDD)

## Core Principle

Write tests BEFORE writing implementation code. Follow the RED → GREEN → REFACTOR cycle.

## When to Use This Skill

- Adding new features
- Fixing bugs
- Refactoring existing code

## The Iron Law

**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**

Writing tests after code is NOT TDD. It's test-after-development (TAD) and misses TDD's benefits.

## Why TDD?

**Benefits:**
- Catches bugs early (before they exist)
- Forces you to think through design
- Creates better APIs (you're the first user)
- Provides a safety net for refactoring
- Documentation through examples
- Higher confidence in changes

## The RED → GREEN → REFACTOR Cycle

### 🔴 RED: Write a Failing Test

1. Think about what you want the code to do.
2. Write a test that describes that behavior.
3. Run the test - it MUST fail.
4. Confirm it fails for the RIGHT reason.

### 🟢 GREEN: Make the Test Pass

1. Write the MINIMAL code to make the test pass.
2. Don't worry about perfect code yet.
3. Just make it green.

### 🔵 REFACTOR: Improve the Code

1. Now that the test passes, improve the code.
2. Remove duplication and improve naming.
3. Keep tests passing.

## Verification Checklist

Before marking work complete:

- [ ] Every new function has a test.
- [ ] Watched each test fail before implementing.
- [ ] Wrote minimal code to pass each test.
- [ ] All tests pass.
- [ ] Output pristine (no errors, warnings).