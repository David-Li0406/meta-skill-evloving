---
name: test-driven-development
description: Use this skill when implementing features or fixing bugs to enforce the RED-GREEN-REFACTOR cycle, requiring tests to fail before writing code.
---

# Test-Driven Development (TDD)

## Overview

Write the test first, watch it fail, then write minimal code to pass. If you didn't watch the test fail, you don't know if it tests the right thing.

## Rigidity Level

LOW FREEDOM - Follow these exact steps in order. Do not adapt. Violating the letter of the rules is violating the spirit of the rules.

## Quick Reference

| Phase | Action | Command Example | Expected Result |
|-------|--------|-----------------|-----------------|
| **RED** | Write failing test | `go test ./...` | FAIL (feature missing) |
| **Verify RED** | Confirm correct failure | Check error message | "function not found" or assertion fails |
| **GREEN** | Write minimal code | Implement feature | Test passes |
| **Verify GREEN** | All tests pass | `go test ./...` | All green, no warnings |
| **REFACTOR** | Clean up code | Improve while green | Tests still pass |

**Iron Law:** NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring with behavior changes
- Any production code

**Exceptions (ask your human partner):**
- Throwaway prototypes (will be deleted)
- Generated code
- Configuration files

Thinking "skip TDD just this once"? Stop. That's rationalization.

## The Process

### 1. RED - Write Failing Test

Write one minimal test showing what should happen.

**Requirements:**
- Test one behavior only ("and" in name? Split it)
- Clear name describing behavior
- Use real code (no mocks unless unavoidable)

### 2. Verify RED - Watch It Fail

**MANDATORY. Never skip.**

Run the test and confirm:
- Test **fails** (not errors with syntax issues)
- Failure message is expected ("function not found" or assertion fails)
- Fails because feature missing (not typos)

**If test passes:** You're testing existing behavior. Fix the test.
**If test errors:** Fix syntax error, re-run until it fails correctly.

### 3. GREEN - Write Minimal Code

Write simplest code to pass the test. Nothing more.

**Key principle:** Don't add features the test doesn't require. Don't refactor other code. Don't "improve" beyond the test.

### 4. Verify GREEN - Watch It Pass

**MANDATORY.**

Run tests and confirm:
- New test passes
- All other tests still pass
- No errors or warnings

**If test fails:** Fix code, not test.
**If other tests fail:** Fix now before proceeding.

### 5. REFACTOR - Clean Up

**Only after green:**
- Remove duplication
- Improve names
- Extract helpers

Keep tests green. Don't add behavior.

### 6. Commit

After green, commit the increment:

```bash
git add path/to/test.go path/to/implementation.go
git commit -m "feat(module): add feature description"
```

### 7. Repeat

Next failing test for next feature.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test **fail** before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass with no warnings
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

**Can't check all boxes?** You skipped TDD. Start over.

## Integration

**This skill is called by:**
- `gambit:executing-plans` (when implementing tasks)
- `gambit:fixing-bugs` (write failing test reproducing bug)

**This skill calls:**
- `gambit:verification` (running tests to verify)

## Final Rule

```
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without your human partner's permission.