---
name: test-implementer
description: Test execution patterns, failure classification, and result analysis
hooks:
  SessionStart:
    - type: command
      command: |
        if command -v yq &> /dev/null && [ -f ".claude/config.yaml" ]; then
          echo "=== Testing Rules ==="
          yq -o=json '.testing' .claude/config.yaml 2>/dev/null || true
          echo "=== Testing Constraints ==="
          yq -o=json '.constraints.testing' .claude/config.yaml 2>/dev/null || true
          yq -o=json '.constraints.business_rules' .claude/config.yaml 2>/dev/null || true
        fi
---

# Test Implementer

A technology-agnostic skill for test execution and result analysis.

## Test Execution Patterns

### Execution Strategy

```yaml
strategy: progressive_execution
description: "Run tests in order of feedback speed"

phases:
  1_unit_tests:
    description: "Fast, isolated tests"
    run_first: true
    fail_fast: true
    typical_duration: "seconds"

  2_integration_tests:
    description: "Component interaction tests"
    run_if: "Unit tests pass"
    fail_fast: false
    typical_duration: "seconds to minutes"

  3_system_tests:
    description: "Full system tests"
    run_if: "Integration tests pass"
    fail_fast: false
    typical_duration: "minutes"

  4_e2e_tests:
    description: "End-to-end user flows"
    run_if: "System tests pass"
    fail_fast: false
    typical_duration: "minutes to hours"
```

### Test Selection

```yaml
selection_patterns:
  changed_files:
    description: "Run tests affected by changes"
    approach:
      - "Identify modified files"
      - "Find tests that import/use those files"
      - "Run only affected tests"

  smoke_tests:
    description: "Critical path verification"
    use_when: "Quick validation needed"
    coverage: "Core functionality only"

  full_suite:
    description: "All tests"
    use_when:
      - "Pre-merge validation"
      - "Release preparation"
      - "Periodic verification"
```

## Failure Classification

### Error vs Failure

```yaml
classification:
  ERROR:
    description: "Test couldn't complete execution"
    causes:
      - "Missing dependencies"
      - "Configuration issues"
      - "Environment problems"
      - "Syntax/compilation errors"
    action: "Fix infrastructure before debugging test"

  FAILURE:
    description: "Test ran but assertion didn't pass"
    causes:
      - "Code behavior doesn't match expectation"
      - "Business logic incorrect"
      - "Edge case not handled"
    action: "Debug production code or update test"
```

### Failure Categories

```yaml
failure_categories:
  assertion_failure:
    pattern: "Expected X but got Y"
    analysis:
      - "Is the expected value correct?"
      - "Is the production code wrong?"
      - "Has the requirement changed?"

  exception_failure:
    pattern: "Unexpected exception thrown"
    analysis:
      - "What triggered the exception?"
      - "Is the exception handling missing?"
      - "Is the test data invalid?"

  timeout_failure:
    pattern: "Test exceeded time limit"
    analysis:
      - "Is there an infinite loop?"
      - "Is external service slow/unavailable?"
      - "Is the timeout too short?"

  setup_failure:
    pattern: "Fixture/setup failed"
    analysis:
      - "Is the database schema current?"
      - "Are required services running?"
      - "Is the test data valid?"
```

## Result Analysis

### Result Summary Format

```yaml
result_summary:
  overview:
    total: <number>
    passed: <number>
    failed: <number>
    errors: <number>
    skipped: <number>
    duration: <seconds>

  failure_details:
    - test: "<test name>"
      type: "ERROR|FAILURE"
      message: "<error message>"
      location: "<file:line>"
      category: "<assertion|exception|timeout|setup>"

  recommendations:
    - action: "<what to do>"
      reason: "<why>"
      priority: "high|medium|low"
```

### Trend Analysis

```yaml
trend_indicators:
  flaky_tests:
    detection: "Same test passes/fails without code changes"
    action: "Investigate race conditions or external dependencies"

  slow_tests:
    detection: "Test duration increasing over time"
    action: "Profile and optimize or parallelize"

  cascading_failures:
    detection: "Many tests fail from single cause"
    action: "Fix root cause first"
```

## Test Environment Management

### Environment Verification

```yaml
environment_checks:
  pre_execution:
    - "Test database accessible?"
    - "Required services running?"
    - "Environment variables set?"
    - "Test fixtures available?"

  isolation:
    - "Tests don't share state?"
    - "Database reset between tests?"
    - "No external side effects?"

  cleanup:
    - "Test data removed after run?"
    - "Temporary files deleted?"
    - "Mock servers stopped?"
```

### Docker Test Environment

```yaml
docker_patterns:
  compose_test:
    description: "Use docker-compose for test environment"
    structure:
      - "docker-compose.test.yml"
      - "Test-specific configuration"
      - "Isolated network"

  commands:
    full_run: "docker compose -f docker-compose.test.yml up --abort-on-container-exit"
    specific: "TEST_ONLY=<path> docker compose -f docker-compose.test.yml up"
    cleanup: "docker compose -f docker-compose.test.yml down -v"
```

## Reporting Patterns

### Test Report Structure

```yaml
report_structure:
  summary:
    - "Pass/fail ratio"
    - "Duration"
    - "Coverage (if available)"

  failures:
    - "Grouped by category"
    - "Ordered by priority"
    - "With actionable context"

  next_steps:
    - "Specific actions to take"
    - "Which agent should handle"
    - "Estimated complexity"
```

### Handoff to Debugger

```yaml
debugger_handoff:
  when: "Failures detected AND category is FAILURE"
  provide:
    - "Failed test list"
    - "Error messages and stack traces"
    - "Test input data"
    - "Expected vs actual results"

  exclude:
    - "Passing test details"
    - "Irrelevant log entries"
    - "Unrelated file contents"
```

## Integration

### Used By Agents

```yaml
primary_users:
  - test-executor: "Test execution and analysis"

secondary_users:
  - test-failure-debugger: "Failure investigation"
  - code-developer: "Test-driven development"
```
