---
name: deliverable-validator
description: Validates deliverables against specifications and provides verification evidence
---

# Deliverable Validator

A technology-agnostic skill for validating that deliverables meet specifications.

## Core Purpose

Verify deliverables by:
- Checking against specifications
- Running validation checks
- Gathering evidence
- Documenting compliance

## Validation Types

### Existence Validation

```yaml
type: existence
description: "Verify required elements exist"

checks:
  files:
    - "Required files present"
    - "Directory structure correct"
    - "No missing dependencies"

  functions:
    - "Required functions implemented"
    - "Required classes present"
    - "Interfaces implemented"

  documentation:
    - "README exists"
    - "API docs present"
    - "Comments where required"

evidence:
  method: "File/code presence check"
  output: "List of present/missing items"
```

### Behavioral Validation

```yaml
type: behavioral
description: "Verify correct behavior"

checks:
  tests:
    - "All tests pass"
    - "No regressions"
    - "Edge cases covered"

  integration:
    - "APIs respond correctly"
    - "Data flows properly"
    - "External systems connect"

  business_logic:
    - "Calculations correct"
    - "Rules enforced"
    - "Workflows complete"

evidence:
  method: "Test execution, manual verification"
  output: "Test results, observation logs"
```

### Quality Validation

```yaml
type: quality
description: "Verify quality standards met"

checks:
  static_analysis:
    - "No linting errors"
    - "No type errors"
    - "No security warnings"

  code_review:
    - "Standards compliance"
    - "Pattern adherence"
    - "Best practices followed"

  metrics:
    - "Coverage threshold met"
    - "Complexity within limits"
    - "Performance acceptable"

evidence:
  method: "Tool output, review observations"
  output: "Analysis reports, metrics"
```

### Specification Validation

```yaml
type: specification
description: "Verify against requirements"

checks:
  criteria_compliance:
    - "All acceptance criteria addressed"
    - "Thresholds met"
    - "Evidence available"

  acceptance_criteria:
    - "All criteria verifiable"
    - "Given-When-Then satisfied"
    - "Edge cases handled"

evidence:
  method: "Acceptance criteria checklist verification"
  output: "Compliance matrix"
```

## Validation Process

### Step 1: Gather Specifications

```yaml
sources:
  - "Acceptance criteria document"
  - "User requirements"
  - "Project standards"

action: "Create validation checklist from specifications"
```

### Step 2: Execute Validations

```yaml
for_each_validation:
  - "Run appropriate check"
  - "Capture evidence"
  - "Record result (PASS/FAIL)"
  - "Note any issues"
```

### Step 3: Compile Evidence

```yaml
evidence_types:
  automated:
    - "Test results"
    - "Linter output"
    - "Coverage reports"

  manual:
    - "Code review notes"
    - "Behavioral observations"
    - "Integration test results"
```

### Step 4: Generate Report

```yaml
report_contents:
  - "Validation summary"
  - "Detailed results"
  - "Evidence references"
  - "Issues found"
  - "Recommendations"
```

## Validation Checklist Template

```yaml
checklist:
  existence:
    - [ ] All required files present
    - [ ] All required functions implemented
    - [ ] Dependencies satisfied

  behavior:
    - [ ] All tests pass
    - [ ] Expected outputs verified
    - [ ] Error handling works

  quality:
    - [ ] No linting errors
    - [ ] Standards followed
    - [ ] Coverage adequate

  specification:
    - [ ] Achievement indicators satisfied
    - [ ] Acceptance criteria met
    - [ ] No regressions
```

## Output Format

```yaml
validation_report:
  overall_status: VALID|INVALID

  validations:
    existence:
      status: PASS|FAIL
      items_checked: <count>
      items_passed: <count>
      missing:
        - "<missing item>"

    behavioral:
      status: PASS|FAIL
      tests_run: <count>
      tests_passed: <count>
      failures:
        - test: "<test name>"
          reason: "<failure reason>"

    quality:
      status: PASS|FAIL
      checks_run: <count>
      issues:
        - type: "<issue type>"
          location: "<file:line>"
          description: "<issue>"

    specification:
      status: PASS|FAIL
      criteria_checked: <count>
      criteria_met: <count>
      gaps:
        - criterion: "<criterion>"
          status: "<gap description>"

  evidence:
    - type: "<evidence type>"
      source: "<file or command>"
      result: "<summary>"

  issues_found:
    critical: [...]
    major: [...]
    minor: [...]

  recommendation: "<next action>"
```

## Integration

### Used By Agents

```yaml
primary_users:
  - deliverable-evaluator: "Validation execution"
  - quality-reviewer: "Quality validation"
```
