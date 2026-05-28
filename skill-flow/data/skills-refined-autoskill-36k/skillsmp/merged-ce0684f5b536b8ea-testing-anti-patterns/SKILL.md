---
name: testing-anti-patterns
description: Use this skill when writing or changing tests, adding mocks, or tempted to add test-only methods to production code. It helps ensure tests verify real behavior and avoid common pitfalls in testing practices.
---

# Testing Anti-Patterns

## Overview

Tests must verify real behavior, not mock behavior. Mocks are a means to isolate, not the thing being tested.

**Core principle:** Test what the code does, not what the mocks do.

**Following strict TDD prevents these anti-patterns.**

## When to Use This Skill

Activate this skill when:
- **Writing or changing tests** - Verify tests cover real behavior.
- **Adding mocks** - Ensure mocking is necessary and correct.
- **Reviewing test failures** - Check if mock behavior is the issue.
- **Tempted to add test-only methods** - STOP and reconsider.
- **Tests feel overly complex** - Sign of over-mocking.

## The Iron Laws

```
1. NEVER test mock behavior
2. NEVER add test-only methods to production classes
3. NEVER mock without understanding dependencies
4. NEVER create incomplete mocks
5. NEVER treat tests as afterthought
```

## Core Anti-Pattern Categories

### 1. Testing Mock Behavior
Asserting on mock elements instead of real behavior. 
**Fix:** Test real component or don't mock it.

### 2. Test-Only Methods in Production
Methods in production classes only used by tests. 
**Fix:** Move to test utilities.

### 3. Mocking Without Understanding
Mocking without understanding dependencies/side effects. 
**Fix:** Understand first, mock minimally.

### 4. Incomplete Mocks
Partial mocks missing fields downstream code needs. 
**Fix:** Mirror complete API structure.

### 5. Tests as Afterthought
Implementation "complete" without tests. 
**Fix:** TDD - write test first.

## Quick Detection Checklist

Run this checklist before committing any test:

**Language-agnostic checks:**
```
□ Am I asserting on mock behavior instead of real behavior?
  → If yes: STOP - Test real behavior or unmock.

□ Does this method only exist for tests?
  → If yes: STOP - Move to test utilities.

□ Do I fully understand what I'm mocking?
  → If no: STOP - Run with real implementation first, then mock minimally.

□ Is my mock missing fields the real API has?
  → If yes: STOP - Mirror complete API structure.

□ Did I write implementation before test?
  → If yes: STOP - Delete implementation, write test first (TDD).

□ Is mock setup >50% of test code?
  → If yes: Consider integration test with real components.
```

## The Bottom Line

**Mocks are tools to isolate, not things to test.**

Testing mock behavior indicates a problem. Fix: Test real behavior or question why mocking is necessary.

**TDD prevents these patterns.** Write test first → Watch fail → Minimal implementation → Pass → Refactor.

## Key Reminders

1. **Mocks isolate, don't prove** - Test real code, not mocks.
2. **Production ignores tests** - No test-only methods.
3. **Understand before mocking** - Know dependencies and side effects.
4. **Complete mocks only** - Mirror full API structure.
5. **Tests ARE implementation** - Not optional afterthought.

## Red Flags - STOP

**STOP immediately when:**
- **Testing mock behavior**
- **Adding test-only methods**
- **Mocking without understanding**
- **Incomplete mocks**
- **Tests as afterthought**

**When mocks become too complex:** Consider integration tests with real components. Often simpler and more valuable.

## Integration with Other Skills

**Prerequisite:** Test-Driven Development skill - TDD prevents anti-patterns (recommended for complete workflow).
**Complementary:** Verification-Before-Completion skill - Tests = done (ensures proper testing discipline).
**Domain-specific:** webapp-testing, backend-testing for framework patterns (see skill library if available).