# TDD Failure Diagnostic Flowchart
**Version:** {{VERSION}}

Quick decision tree for diagnosing and recovering from unexpected test behaviors.

## Primary Decision: Which Phase?

```
Test behaved unexpectedly
         ↓
  What phase are you in?
         ↓
┌────────┼────────┬────────┐
RED     GREEN    REFACTOR  OTHER
↓        ↓         ↓        ↓
```

---

## RED Phase Diagnostics

**Expected:** Test should FAIL
**Problem:** Test PASSES or ERRORS

### If Test Passes (Should Fail)

```
Test passes unexpectedly
         ↓
Check: Does feature already exist?
         ↓
    ┌────┴────┐
   YES       NO
    ↓         ↓
Delete    Check test
impl.     logic
    ↓         ↓
Verify    Is assertion
fails     correct?
         ↓
    ┌────┴────┐
   YES       NO
    ↓         ↓
Other    Fix test
issue    assertion
         ↓
      Revise
      test
```

**Recovery:** ASSISTANT provides corrected test

### If Test Errors (Should Fail Cleanly)

```
Test throws error/exception
         ↓
Check: Syntax error?
         ↓
    ┌────┴────┐
   YES       NO
    ↓         ↓
Fix      Check imports/
syntax   setup
    ↓         ↓
   Fix test code
         ↓
    Run again
```

**Recovery:** ASSISTANT fixes test code

---

## GREEN Phase Diagnostics

**Expected:** Test should PASS
**Problem:** Test still FAILS

### If Test Still Fails

```
Test fails after implementation
         ↓
Read failure message carefully
         ↓
What does it say?
         ↓
┌─────────┼─────────┬─────────┐
Logic    Type      Missing
error    mismatch  feature
↓        ↓         ↓
Fix      Fix       Add
logic    types     impl.
         ↓
    Run test again
         ↓
    ┌────┴────┐
   PASS      FAIL
    ↓         ↓
  GREEN    Revise
  phase    impl.
  done     again
```

**Recovery:** ASSISTANT provides corrected implementation

### If Other Tests Break

```
Target test passes BUT other tests fail
         ↓
Regression introduced
         ↓
Which tests broke?
         ↓
Review what changed
         ↓
Fix implementation to satisfy all tests
         ↓
Run full suite
         ↓
All green? → GREEN phase done
```

**Recovery:** ASSISTANT revises implementation to fix regressions

---

## REFACTOR Phase Diagnostics

**Expected:** Tests stay GREEN
**Problem:** Tests FAIL after refactoring

### If Tests Break

```
Tests fail after refactoring
         ↓
IMMEDIATE ACTION: ROLLBACK
         ↓
Undo refactoring changes
         ↓
Run tests
         ↓
All green again?
         ↓
    ┌────┴────┐
   YES       NO
    ↓         ↓
Decide    Fix
next     rollback
action   first
    ↓
┌────┼────┬────┐
Skip  Try  Fix
      smaller test
      refactor (if brittle)
         ↓
   Proceed safely
```

**Recovery:** Rollback, then decide on smaller refactoring or skip

---

## Inconsistent Test Results

**Problem:** Test passes sometimes, fails other times

### Diagnosis Flow

```
Test has inconsistent results
         ↓
Run test alone (isolated)
         ↓
Does it still fail inconsistently?
         ↓
    ┌────┴────┐
   YES       NO
    ↓         ↓
Internal  Test order
issue     dependency
    ↓         ↓
Check:    Fix test
- Timing  isolation
- Random  - Setup
  data    - Teardown
- Async   - Shared
  ops       state
         ↓
    Fix and verify consistency
```

**Recovery:** Ensure test isolation and determinism

---

## General Recovery Procedure

### Rollback to Previous State

```
Issue detected (tests broken, wrong path)
         ↓
Restore previous code state (git checkout or undo)
         ↓
Run tests to verify green
         ↓
Resume TDD cycle:
- Try different approach
- Skip change
- Proceed to next behavior
```

---

## Quick Reference Table

| Phase    | Expected | Actual        | Action                    |
|----------|----------|---------------|---------------------------|
| RED      | FAIL     | PASS          | Revise test (invalid)     |
| RED      | FAIL     | ERROR         | Fix test (bug in test)    |
| GREEN    | PASS     | FAIL          | Revise impl (incomplete)  |
| GREEN    | PASS     | Others FAIL   | Fix regression            |
| REFACTOR | All PASS | Any FAIL      | ROLLBACK immediately      |

---

## Emergency Procedure

**When completely confused:**

1. STOP
2. ROLLBACK to last known green state
3. Run full test suite
4. Verify all green
5. Start fresh from clean state
6. Proceed more carefully

---

**Use this flowchart whenever tests behave unexpectedly**
