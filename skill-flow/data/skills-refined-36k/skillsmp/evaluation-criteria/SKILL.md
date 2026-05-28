---
name: evaluation-criteria
description: Defines evaluation criteria and scoring methodologies for deliverable assessment
---

# Evaluation Criteria

A technology-agnostic skill for defining how deliverables should be evaluated.

## Core Purpose

Establish consistent, objective criteria for:
- Assessing deliverable quality
- Scoring against requirements
- Making pass/fail determinations
- Providing constructive feedback

## Evaluation Dimensions

### Completeness

```yaml
dimension: completeness
question: "Is everything required present?"

criteria:
  functionality:
    - "All specified functions implemented"
    - "All user stories addressed"
    - "All acceptance criteria met"

  coverage:
    - "All edge cases handled"
    - "All error paths covered"
    - "All integrations connected"

  documentation:
    - "Required documentation present"
    - "API documentation complete"
    - "Comments where needed"

scoring:
  pass: "100% of must-have items present"
  fail: "Any must-have item missing"
```

### Correctness

```yaml
dimension: correctness
question: "Does it work correctly?"

criteria:
  functional:
    - "Business logic accurate"
    - "Calculations correct"
    - "Data transformations valid"

  behavioral:
    - "Expected outputs produced"
    - "Error handling appropriate"
    - "Edge cases handled correctly"

  integration:
    - "External systems connected"
    - "Data flows correctly"
    - "APIs respond correctly"

scoring:
  pass: "All tests pass, no logic errors"
  fail: "Any test failure or logic error"
```

### Quality

```yaml
dimension: quality
question: "Is it well-built?"

criteria:
  code_standards:
    - "Follows project conventions"
    - "No linting errors"
    - "Consistent formatting"

  architecture:
    - "Follows design patterns"
    - "Proper separation of concerns"
    - "Dependencies managed correctly"

  maintainability:
    - "Code is readable"
    - "Complexity manageable"
    - "No code smells"

scoring:
  pass: "No critical issues, minimal major issues"
  fail: "Critical issues present"
```

### Security

```yaml
dimension: security
question: "Is it secure?"

criteria:
  vulnerabilities:
    - "No SQL injection"
    - "No XSS vulnerabilities"
    - "No CSRF vulnerabilities"

  authentication:
    - "Proper auth checks"
    - "Secure password handling"
    - "Session management correct"

  data_protection:
    - "Sensitive data encrypted"
    - "PII handled correctly"
    - "Audit logging present"

scoring:
  pass: "No security vulnerabilities found"
  fail: "Any security vulnerability present"
```

### Performance

```yaml
dimension: performance
question: "Does it perform well?"

criteria:
  response_time:
    - "API response < 200ms (95th percentile)"
    - "Page load < 3 seconds"

  resource_usage:
    - "Memory usage reasonable"
    - "CPU usage efficient"
    - "No memory leaks"

  scalability:
    - "Handles expected load"
    - "No N+1 queries"
    - "Caching implemented where needed"

scoring:
  pass: "Meets performance thresholds"
  fail: "Below performance thresholds"
```

## Scoring System

### Severity Classification

```yaml
severity_levels:
  critical:
    definition: "Must fix before acceptance"
    examples:
      - "Security vulnerability"
      - "Data corruption risk"
      - "Core functionality broken"
    impact: "Automatic FAIL"

  major:
    definition: "Should fix before acceptance"
    examples:
      - "Logic errors"
      - "Missing tests"
      - "Performance issues"
    impact: "Accumulate to threshold"

  minor:
    definition: "Can fix later"
    examples:
      - "Style improvements"
      - "Documentation gaps"
      - "Minor optimizations"
    impact: "Noted but not blocking"
```

### Pass/Fail Determination

```yaml
pass_criteria:
  all_of:
    - "No critical issues"
    - "Critical dimensions pass (completeness, correctness, security)"
  threshold:
    - "Major issues <= 3"
    - "Overall score >= 80%"

fail_criteria:
  any_of:
    - "Any critical issue present"
    - "Critical dimension fails"
    - "Major issues > 5"
    - "Overall score < 60%"
```

## Output Format

```yaml
evaluation:
  overall_verdict: PASS|FAIL
  overall_score: <0-100>

  dimensions:
    completeness:
      score: <0-100>
      status: PASS|FAIL
      issues: [...]

    correctness:
      score: <0-100>
      status: PASS|FAIL
      issues: [...]

    quality:
      score: <0-100>
      status: PASS|FAIL
      issues: [...]

    security:
      score: <0-100>
      status: PASS|FAIL
      issues: [...]

    performance:
      score: <0-100>
      status: PASS|FAIL
      issues: [...]

  issue_summary:
    critical: <count>
    major: <count>
    minor: <count>

  feedback:
    - "<actionable feedback item>"
```

## Integration

### Used By Agents

```yaml
primary_users:
  - deliverable-evaluator: "Core evaluation methodology"
  - quality-reviewer: "Quality assessment"
```
