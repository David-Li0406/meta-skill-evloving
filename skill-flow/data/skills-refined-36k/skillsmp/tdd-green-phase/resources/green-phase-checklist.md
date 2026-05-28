# GREEN Phase Checklist
**Version:** {{VERSION}}

Quick reference for completing GREEN phase successfully.

## Before Implementing

- [ ] RED phase complete with verified failing test
- [ ] Test requirements clearly understood
- [ ] Minimum implementation approach identified
- [ ] No plans to add untested features

## Writing Implementation

- [ ] Code implements exactly what test requires
- [ ] Implementation is minimal (YAGNI principle)
- [ ] No features beyond test scope added
- [ ] Code is clear and understandable
- [ ] Implementation is complete (no placeholders)

## Executing the Test

- [ ] Implementation runs without errors
- [ ] Target test now PASSES (green)
- [ ] Implementation code is syntactically correct
- [ ] No unexpected side effects

## Regression Check

- [ ] Full test suite executed (if available)
- [ ] All existing tests still pass
- [ ] No regressions introduced
- [ ] All tests are green

## Before Proceeding to REFACTOR

- [ ] Test is green and verified
- [ ] Implementation is minimal but complete
- [ ] No broken tests exist
- [ ] Ready for refactoring analysis
- [ ] Proceed autonomously to REFACTOR phase

---

## Quick Diagnostics

**If test still fails:**
→ Implementation incomplete or incorrect
→ Review test expectations, revise implementation

**If other tests break:**
→ Regression introduced
→ Fix implementation to keep all tests green

**If implementation seems too simple:**
→ That's OK! Simplest thing that works is correct
→ Future tests will drive additional complexity

---

## YAGNI Reminders

- Don't add "might need later" features
- Don't optimize prematurely
- Don't create abstractions before third use
- Trust that tests will drive future features

---

**Use this checklist for every GREEN phase iteration**
