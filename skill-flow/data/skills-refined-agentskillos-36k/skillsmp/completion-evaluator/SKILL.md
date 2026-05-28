---
name: completion-evaluator
description: Evaluates task completion against acceptance criteria and determines pass/fail verdicts
---

# Completion Evaluator

A technology-agnostic skill for evaluating deliverables against acceptance criteria and achievement indicators.

## Core Purpose

Provide objective, evidence-based evaluation of deliverables to determine:
- Whether acceptance criteria are met
- Pass/fail verdicts with justification
- Specific feedback for improvements
- Next action recommendations

## Evaluation Framework

### Achievement Indicator Categories

```yaml
completeness_indicators:
  description: "What must be present in the deliverable"
  examples:
    - "All required functions implemented"
    - "Error handling present"
    - "Edge cases covered"
    - "Documentation included"

quality_indicators:
  description: "How the deliverable should be built"
  examples:
    - "Code follows project standards"
    - "Test coverage meets threshold"
    - "No security vulnerabilities"
    - "Performance within limits"

functionality_indicators:
  description: "What the deliverable must do"
  examples:
    - "Business logic correct"
    - "User acceptance criteria met"
    - "Integration points working"
    - "No regressions introduced"
```

### Evaluation Process

```yaml
step_1_load_context:
  actions:
    - "Read acceptance criteria/indicators"
    - "Identify all criteria to evaluate"
    - "Prepare evaluation checklist"

step_2_evaluate_each_indicator:
  for_each_criterion:
    - "Gather evidence from deliverable"
    - "Compare to threshold/target"
    - "Determine PASS/FAIL"
    - "Document evidence"

step_3_calculate_verdict:
  rules:
    all_pass: "Overall PASS"
    any_fail: "Overall FAIL"
    note: "No CONDITIONAL - binary verdict only"

step_4_determine_next_action:
  if_pass:
    - "Deliverable accepted"
    - "Return to workflow-orchestrator"
  if_fail:
    - "Identify failed indicators"
    - "Determine responsible agent"
    - "Provide specific feedback"
```

## Indicator Evaluation

### Evidence Requirements

```yaml
evidence_types:
  code_presence:
    method: "File/function existence check"
    example: "Function X exists in file Y"

  test_results:
    method: "Test execution output"
    example: "All 15 tests pass"

  static_analysis:
    method: "Linter/analyzer output"
    example: "No errors in cs-check"

  coverage_metrics:
    method: "Coverage tool output"
    example: "82% line coverage"

  performance_metrics:
    method: "Benchmark results"
    example: "Response time: 150ms"

  manual_verification:
    method: "Code review observations"
    example: "Error handling present in all external calls"
```

### Threshold Comparison

```yaml
threshold_types:
  boolean:
    example: "Feature X implemented: true"
    pass_if: "value == expected"

  numeric:
    example: "Test coverage >= 80%"
    pass_if: "value >= threshold"

  count:
    example: "Critical bugs == 0"
    pass_if: "count <= max_allowed"

  presence:
    example: "Documentation exists"
    pass_if: "file/section exists"
```

## Verdict Generation

### Pass Criteria

```yaml
pass_requirements:
  - "ALL completeness indicators PASS"
  - "ALL quality indicators PASS"
  - "ALL functionality indicators PASS"
  - "No critical issues found"

pass_verdict:
  overall: "PASS"
  action: "Proceed to commit/completion"
  delegate_to: "workflow-orchestrator"
```

### Fail Criteria

```yaml
fail_triggers:
  - "ANY indicator fails"
  - "Critical issue found"
  - "Blocking problem identified"

fail_verdict:
  overall: "FAIL"
  action: "Return for rework"
  delegate_to: "<agent responsible for failed area>"
  feedback: "<specific issues and remediation>"
```

## Iteration Management

### Iteration Tracking

```yaml
iteration_limits:
  max_iterations: 3
  focus_by_iteration:
    iteration_1: "Critical issues"
    iteration_2: "Major improvements"
    iteration_3: "Final polish"

escalation:
  trigger: "After 3 failed iterations"
  action: "Consult user for decision"
  options:
    - "Accept current state"
    - "Modify requirements"
    - "Abandon task"
```

### Feedback Quality

```yaml
feedback_requirements:
  specific:
    bad: "Code quality issues"
    good: "Missing error handling in getUserById() at line 45"

  actionable:
    bad: "Improve test coverage"
    good: "Add tests for edge case: null user input in login()"

  prioritized:
    bad: "Fix all issues"
    good: "Critical: SQL injection at line 23; Major: Missing validation"

  agent_assigned:
    bad: "Fix the code"
    good: "code-developer: Add input validation to processPayment()"
```

## Output Format

```yaml
evaluation_result:
  overall_verdict: PASS|FAIL

  indicator_results:
    completeness:
      - indicator: "All required functions implemented"
        status: PASS|FAIL
        evidence: "<proof>"
        target: "<what was required>"
        actual: "<what was achieved>"

    quality:
      - indicator: "Code follows standards"
        status: PASS|FAIL
        evidence: "<proof>"
        target: "<standard>"
        actual: "<measurement>"

    functionality:
      - indicator: "Business logic correct"
        status: PASS|FAIL
        evidence: "<proof>"
        target: "<expected behavior>"
        actual: "<observed behavior>"

  summary:
    passed_count: <number>
    failed_count: <number>
    pass_rate: "<percentage>"

  feedback:
    critical:
      - issue: "<description>"
        location: "<file:line>"
        remediation: "<how to fix>"
        assign_to: "<agent>"

    major:
      - issue: "<description>"
        location: "<file:line>"
        remediation: "<how to fix>"
        assign_to: "<agent>"

    minor:
      - issue: "<description>"
        suggestion: "<improvement>"

  next_action:
    action: complete|rework
    reason: "<why>"
    assigned_agent: "<agent for rework>"
    specific_tasks:
      - "<task 1>"
      - "<task 2>"

  iteration:
    current: <number>
    max: 3
    escalate_if_exceeded: true
```

## Evaluation Checklist Template

```yaml
checklist:
  completeness:
    - [ ] All specified functions exist
    - [ ] Error handling implemented
    - [ ] Edge cases covered
    - [ ] Required documentation present

  quality:
    - [ ] Code follows project standards
    - [ ] No linting errors
    - [ ] Test coverage adequate
    - [ ] No security vulnerabilities

  functionality:
    - [ ] Core business logic works
    - [ ] Acceptance criteria met
    - [ ] No regressions introduced
    - [ ] Integration points functional
```

## Integration

### Used By Agents

```yaml
primary_users:
  - deliverable-evaluator: "Core evaluation skill"

secondary_users:
  - workflow-orchestrator: "Completion checks"
  - quality-reviewer: "Quality assessment"
```

### Acceptance Criteria Sources

```yaml
criteria_sources:
  from_goal_clarifier:
    when: "All tasks"
    format: "Structured acceptance criteria"

  from_user_request:
    when: "Explicit criteria provided"
    format: "User-defined acceptance criteria"

  default_indicators:
    when: "No explicit criteria provided"
    use: "Standard quality checklist"
```

## Best Practices

1. **Evidence-Based**: Every verdict must cite specific evidence
2. **Objective**: Apply same standards consistently
3. **Actionable Feedback**: Every failure includes remediation path
4. **Clear Assignments**: Failed areas specify responsible agent
5. **Iteration Awareness**: Track progress across iterations
6. **Escalation Ready**: Know when to involve user
