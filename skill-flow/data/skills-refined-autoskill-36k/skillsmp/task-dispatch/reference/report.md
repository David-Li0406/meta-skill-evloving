# Report Format Reference

YAML report schemas for structured handoff between subagents.

## Why YAML Reports

- **Structured parsing** - Main agent can reliably extract data
- **Consistent handoff** - Tester → Implementer → Reviewer
- **Clear status** - Success, gap, blocked states
- **Evidence-based** - Actual outputs, not claims

---

## Tester Report

```yaml
tester_report:
  # Status: did tester successfully write tests?
  status: success | gap

  # List of test files created
  test_files:
    - path: tests/test_feature.py
      tests:
        - test_name_1
        - test_name_2
        - test_name_3

  # Actual test failure output (proves RED state)
  failure_output: |
    FAILED tests/test_feature.py::test_name_1
    AssertionError: Expected True but got None

    FAILED tests/test_feature.py::test_name_2
    ModuleNotFoundError: No module named 'src.feature'

    2 failed in 0.05s

  # If status=gap, explain why tests couldn't be written
  gap_reason: null | |
    Cannot write tests because:
    - [ambiguity 1]
    - [ambiguity 2]
    Need clarification on: [questions]
```

### Tester Status Values

| Status | Meaning | Next Step |
|--------|---------|-----------|
| `success` | Tests written and failing | Dispatch implementer |
| `gap` | Cannot write meaningful tests | Consult spec, ask user, re-dispatch |

---

## Implementer Report

```yaml
implementer_report:
  # Status: did implementer make tests pass?
  status: success | blocked

  # List of implementation files created/modified
  implementation_files:
    - path: src/feature.py

  # Actual test pass output (proves GREEN state)
  test_output: |
    tests/test_feature.py::test_name_1 PASSED
    tests/test_feature.py::test_name_2 PASSED
    tests/test_feature.py::test_name_3 PASSED

    3 passed in 0.15s

  # If used AskUserQuestion, record Q&A
  clarifications:
    - question: "Should X be configurable?"
      answer: "Yes, via constructor parameter"

  # If status=blocked, explain why
  blocked_reason: null | |
    Cannot implement because:
    - [blocker]
    Possible resolution: [suggestion]
```

### Implementer Status Values

| Status | Meaning | Next Step |
|--------|---------|-----------|
| `success` | Tests passing | Proceed to review |
| `blocked` | Cannot make tests pass | Investigate blocker, re-dispatch |

---

## Reviewer Report

```yaml
reviewer_report:
  # Overall batch status
  overall_status: approved | changes_requested

  # Which tasks were reviewed
  tasks_reviewed:
    - T001
    - T002
    - T003

  # Issues found, by severity
  issues:
    - task: T001
      severity: critical | important | minor
      description: "Clear description of issue"
      suggested_fix: "Actionable suggestion"
      file: path/to/file.py  # optional
      line: 42               # optional

  # Positive observations
  strengths:
    - "Good test coverage"
    - "Clean code structure"

  # Summary assessment
  overall_assessment: |
    Brief summary of batch quality.
    Which tasks are ready, which need fixes.
```

### Reviewer Status Values

| Status | Meaning | Next Step |
|--------|---------|-----------|
| `approved` | All tasks meet requirements | Mark complete, next batch |
| `changes_requested` | Issues need fixing | Dispatch fix subagent(s) |

### Issue Severity

| Severity | Definition | Action |
|----------|------------|--------|
| `critical` | Blocks progress, breaks build/tests | Fix immediately |
| `important` | Affects quality, missing coverage | Fix before next batch |
| `minor` | Style, naming, improvements | Note for later |

---

## Fix Report

```yaml
fix_report:
  # Did fixes succeed?
  status: success | failed

  # What was fixed
  fixes_applied:
    - issue: "Missing null check"
      fix: "Added validation at line 42"
    - issue: "Unclear variable name"
      fix: "Renamed x to retry_count"

  # Test output after fixes
  test_output: |
    5 passed in 0.20s

  # If status=failed, explain
  failure_reason: null | |
    Could not fix because: [reason]
```

---

## Report Flow

```
Task Start
    │
    ▼
TESTER
    │
    ├─ status: success ──► tester_report with test_files, failure_output
    │                           │
    │                           ▼
    │                      IMPLEMENTER
    │                           │
    │                           ├─ status: success ──► implementer_report
    │                           │                           │
    │                           │                           ▼
    │                           │                      REVIEWER (batch)
    │                           │                           │
    │                           │                           ├─ approved ──► Done
    │                           │                           │
    │                           │                           └─ changes_requested
    │                           │                                   │
    │                           │                                   ▼
    │                           │                              FIX SUBAGENT
    │                           │                                   │
    │                           │                                   ▼
    │                           │                              fix_report
    │                           │
    │                           └─ status: blocked ──► Investigate, re-dispatch
    │
    └─ status: gap ──► Consult spec, ask user, re-dispatch tester
```

---

## Parsing Reports

Main agent should:

1. Look for YAML code blocks in subagent output
2. Parse the appropriate `*_report` structure
3. Check `status` field first
4. Handle success/failure paths accordingly
5. Pass reports to next phase (tester → implementer → reviewer)
