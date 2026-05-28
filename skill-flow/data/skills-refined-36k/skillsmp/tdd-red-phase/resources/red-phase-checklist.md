# RED Phase Checklist
**Version:** {{VERSION}}

Quick reference for completing RED phase successfully.

## Before Writing Test

- [ ] Behavior to test is clearly identified
- [ ] Behavior is small and focused (one thing)
- [ ] Feature/behavior does not yet exist
- [ ] Test framework is configured and working

## Writing the Test

- [ ] Test name clearly describes behavior
- [ ] Test follows AAA structure (Arrange-Act-Assert)
- [ ] Test uses minimal, explicit test data
- [ ] Test has clear, specific assertions
- [ ] Test includes necessary imports and setup
- [ ] Test is complete and syntactically correct

## Executing the Test

- [ ] Test runs without syntax errors
- [ ] Test FAILS (does not pass)
- [ ] Test does not throw unexpected exceptions
- [ ] Failure message clearly indicates missing implementation

## Verifying Failure

- [ ] Failure reason is correct (feature missing, not test bug)
- [ ] Failure message is understandable
- [ ] Test fails for the RIGHT reason
- [ ] Confident test will pass once feature implemented

## Before Proceeding to GREEN

- [ ] Test failure verified and documented
- [ ] Ready to implement minimum code to pass test
- [ ] Proceed autonomously to GREEN phase

---

## Quick Diagnostics

**If test passes unexpectedly:**
→ Feature may already exist OR test is invalid
→ Review test logic, check for existing implementation

**If test throws errors:**
→ Test has bugs (syntax, imports, setup)
→ Fix test code before proceeding

**If failure message is unclear:**
→ Add descriptive assertion messages
→ Simplify test to one focused assertion

---

**Use this checklist for every RED phase iteration**
