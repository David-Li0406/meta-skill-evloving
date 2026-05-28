# REFACTOR Phase Checklist
**Version:** {{VERSION}}

Quick reference for completing REFACTOR phase successfully.

## Before Refactoring

- [ ] GREEN phase complete with all tests passing
- [ ] Claude Code has analyzed code for opportunities
- [ ] ASSISTANT has evaluated refactoring suggestions
- [ ] Decision made: refactor OR skip
- [ ] If refactoring: specific improvements identified

## If Refactoring

- [ ] Refactoring scope is small and focused
- [ ] One refactoring at a time planned
- [ ] All tests are currently GREEN
- [ ] Refactoring won't change behavior
- [ ] No new features being added

## Applying Refactoring

- [ ] Refactored code is clear and improved
- [ ] Code structure or naming enhanced
- [ ] Duplication eliminated (if applicable)
- [ ] Logic simplified (if applicable)
- [ ] Changes are minimal and focused

## Testing After Refactoring

- [ ] Full test suite executed
- [ ] ALL tests still PASS (green)
- [ ] No test failures
- [ ] No test errors
- [ ] No behavioral changes introduced

## If Tests Break

- [ ] IMMEDIATE ROLLBACK performed
- [ ] Tests returned to green state
- [ ] Decision made: skip refactoring OR try smaller change
- [ ] Tests remain green before proceeding

## Before Proceeding to Next Feature

- [ ] Refactoring complete OR intentionally skipped
- [ ] All tests are green
- [ ] Code quality improved OR preserved
- [ ] Ready to start next RED phase
- [ ] Proceed autonomously to next behavior or story completion

---

## Quick Diagnostics

**If refactoring breaks tests:**
→ ROLLBACK IMMEDIATELY
→ Tests must stay green
→ Try smaller refactoring or skip

**If refactoring seems risky:**
→ Skip for now
→ Defer to future session
→ Tests stay green

**If unsure about refactoring value:**
→ Skip refactoring
→ Don't refactor for sake of refactoring
→ Code is good enough

---

## When to Skip Refactoring

- Premature abstraction (only one use case)
- Code already clear enough
- High risk, low value improvement
- Over-engineering suggested
- Time constraints

---

## Refactoring Principles

**Do:**
- Small incremental changes
- Test after each change
- Rollback if tests break
- Improve clarity and maintainability

**Don't:**
- Add new features during refactoring
- Change behavior
- Accept broken tests
- Big bang refactorings

---

**Use this checklist for every REFACTOR phase iteration**
