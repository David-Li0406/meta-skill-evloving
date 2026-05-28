# Vibe Report Formats

## Output Files

| File | Purpose |
|------|---------|
| `reports/vibe-report.json` | Full JSON findings |
| `reports/vibe-junit.xml` | CI integration (JUnit XML) |
| `.agents/assessments/{date}-vibe-validate-{target}.md` | Knowledge artifact |

---

## JSON Report Structure

```json
{
  "summary": {
    "critical": 0,
    "high": 2,
    "medium": 5,
    "low": 1,
    "total": 8
  },
  "prescan": [
    {
      "id": "P4",
      "pattern": "Invisible Undone",
      "severity": "HIGH",
      "file": "services/auth/main.py",
      "line": 42,
      "message": "TODO marker"
    }
  ],
  "semantic": [
    {
      "id": "FAITH-001",
      "category": "docstrings",
      "severity": "HIGH",
      "file": "services/auth/main.py",
      "function": "validate_token",
      "message": "Docstring claims validation but no raise/return False"
    }
  ]
}
```

---

## JUnit XML Format

For CI integration:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="vibe-validate" tests="8" failures="7" errors="1">
  <testsuite name="prescan" tests="3" failures="3">
    <testcase name="P4-services/auth/main.py:42" classname="prescan.invisible_undone">
      <failure message="TODO marker" type="HIGH"/>
    </testcase>
  </testsuite>
  <testsuite name="semantic" tests="5" failures="4">
    <testcase name="FAITH-001-validate_token" classname="semantic.docstrings">
      <failure message="Docstring mismatch" type="HIGH"/>
    </testcase>
  </testsuite>
</testsuites>
```

---

## Assessment Artifact Format

Saved to `.agents/assessments/`:

```yaml
---
date: 2025-01-03
type: Assessment
assessment_type: vibe-validate
scope: recent
target: HEAD~1..HEAD
status: PASS_WITH_WARNINGS
severity: HIGH
findings:
  critical: 0
  high: 2
  medium: 5
  low: 1
  total: 8
tags: [assessment, vibe-validate, validation, recent]
---

# Vibe Validation: recent

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH | 2 |
| MEDIUM | 5 |
| LOW | 1 |

## Critical Findings

None.

## High Findings

1. **P4** `services/auth/main.py:42` - TODO marker
2. **FAITH-001** `validate_token()` - Docstring mismatch

## Recommendations

1. Complete or remove TODO at services/auth/main.py:42
2. Update validate_token() docstring to match implementation
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success, no CRITICAL findings |
| 1 | Argument/usage error |
| 2 | CRITICAL findings detected |
| 3 | HIGH findings detected (no CRITICAL) |
