# Code Review Report Format

YAML schema for structured review handoff and synthesis.

---

## Reviewer Report

Each reviewer outputs this structure:

```yaml
reviewer_report:
  reviewer: claude-opus | opencode-codex | gemini-3-pro

  gates:
    correctness:
      status: pass | fail
      issues:
        - "Logic error in X"
    style:
      status: pass | fail
      issues:
        - "Inconsistent naming"
    performance:
      status: pass | fail
      issues:
        - "N+1 query pattern"
    security:
      status: pass | fail
      issues:
        - "SQL injection risk"
    architecture:
      status: pass | fail
      issues:
        - "Tight coupling between X and Y"

  issues:
    - severity: critical | high | medium
      gate: correctness | style | performance | security | architecture
      area: logic | error_handling | type_safety | naming | formatting | efficiency | validation | secrets | coupling | testing
      location: "file:line"
      description: "Clear description of the issue"
      suggestion: "Actionable fix"

  strengths:
    - "Good error handling"
    - "Clear function names"
```

---

## Synthesized Report

Main agent produces this after merging reviewer reports:

```yaml
synthesized_report:
  reviewers: [claude-opus, opencode-codex, gemini-3-pro]

  gates:
    correctness:
      status: pass | fail
      failed_by: [claude-opus]
    style:
      status: pass | fail
      failed_by: []
    performance:
      status: pass | fail
      failed_by: []
    security:
      status: pass | fail
      failed_by: [claude-opus, gemini-3-pro]
    architecture:
      status: pass | fail
      failed_by: []

  issues:
    - id: C1
      severity: critical
      gate: security
      area: validation
      location: "src/db/query.py:45"
      description: "SQL injection via unsanitized user input"
      suggestion: "Use parameterized queries"
      found_by: [claude-opus, gemini-3-pro]

  strengths:
    - "Clear separation of concerns"
    - "Comprehensive error messages"

  summary:
    critical: 1
    high: 2
    medium: 3

  recommendation: ready_to_merge | address_issues
  next_action: "Commit/merge" | "Fix critical/high issues"
```

---

## Gate Status Values

| Status | Meaning |
|--------|---------|
| `pass` | No issues found for this gate |
| `fail` | One or more issues found |

---

## Issue Severity

| Severity | Definition | Action |
|----------|------------|--------|
| `critical` | Bugs, security issues, data corruption | Must fix before merge |
| `high` | Significant issues, unclear behavior | Should fix before merge |
| `medium` | Style issues, minor improvements | Can merge, follow-up |

---

## Issue Areas

| Area | Covers |
|------|--------|
| `logic` | Control flow, algorithms, conditionals |
| `error_handling` | Exceptions, error states, recovery |
| `type_safety` | Type correctness, nullability |
| `naming` | Variable, function, class names |
| `formatting` | Code layout, indentation, spacing |
| `efficiency` | Time/space complexity, caching |
| `validation` | Input checking, sanitization |
| `secrets` | Credentials, keys, tokens |
| `coupling` | Dependencies, interfaces |
| `testing` | Test coverage, testability |
