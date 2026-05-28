---
name: test-runner
description: Automated test execution before commits to prevent broken code from entering the repository. Use when user wants to run tests, is about to commit, or before creating a PR.
version: 2.0.0
allowed-tools:
  - Read
  - Bash(pytest, python)
plan_mode_required: false
trigger_keywords:
  - test
  - tests
  - pytest
  - run tests
  - before commit
---

# Test Runner

**Mission**: Zero Broken Commits - no code committed if tests fail.

---

## Current Test Results (Auto-Executed)

### Test Suite Output
```
!`python -m pytest tests/ -v --tb=short 2>&1 | tail -80`
```

### Test Count Summary
```
!`python -m pytest tests/ --co -q 2>&1 | tail -5`
```

---

## Analysis Instructions

Based on the test results above:

### If ALL TESTS PASSED:
```markdown
## ✅ All Tests Passed

**Summary:** [X] tests passed in [Y]s
**Status:** Safe to commit ✅
```

### If TESTS FAILED:
```markdown
## ❌ Tests Failed

**Summary:** [X] passed, [Y] failed

**Failed Tests:**
1. `test_file.py::test_name` - Line [N]
   - Error: [error message]

**Status:** ⚠️ DO NOT COMMIT - Fix tests first

**Next Steps:**
1. Review failed test at [file:line]
2. Fix the issue
3. Run tests again: `/test-runner`
```

---

## Constraints

**DO NOT:**
- Modify test code - only run and report
- Modify source code - only report results
- Skip failing tests - all must pass
- Recommend committing with failures

**ALWAYS:**
- Report all failures with file paths and line numbers
- Block commit if tests fail
- Show execution time

---

## Coverage Report (On Request)

If user asks for coverage:
```bash
python -m pytest --cov=src --cov-report=term-missing -v
```

---

## Troubleshooting

For common issues, see [troubleshooting.md](reference/troubleshooting.md)

---

## Integration

Works with:
- **preflight-check**: Tests run as part of preflight
- **pr-helper**: Tests must pass before PR creation
- **CI (test.yml)**: Validates in clean environment after push

```
Code changes → test-runner ✅ → commit → push → CI validates
```
