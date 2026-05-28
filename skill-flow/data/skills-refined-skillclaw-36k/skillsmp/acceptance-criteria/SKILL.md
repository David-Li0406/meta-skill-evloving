---
name: acceptance-criteria
description: Defines measurable acceptance criteria using SMART principles and Given-When-Then format
---

# Acceptance Criteria

A technology-agnostic skill for defining clear, measurable acceptance criteria.

## Core Purpose

Transform requirements into verifiable acceptance criteria that:
- Are specific and unambiguous
- Can be objectively measured
- Guide implementation
- Enable evaluation

## Acceptance Criteria Format

### Given-When-Then (GWT)

```yaml
format: given_when_then
structure:
  given: "Initial context or precondition"
  when: "Action or trigger"
  then: "Expected outcome or result"

example:
  given: "User is logged in with valid credentials"
  when: "User clicks the 'Export' button"
  then: "System generates a CSV file with all user data"
```

### SMART Criteria

```yaml
specific:
  definition: "Clear and unambiguous"
  bad: "System should be fast"
  good: "API response time under 200ms for 95% of requests"

measurable:
  definition: "Quantifiable outcome"
  bad: "Good test coverage"
  good: "Test coverage >= 80%"

achievable:
  definition: "Technically feasible"
  check: "Can this be implemented with current resources?"

relevant:
  definition: "Aligned with business goals"
  check: "Does this contribute to user value?"

time_bound:
  definition: "Has clear completion point"
  check: "When is this considered done?"
```

## Criteria Categories

### Functional Criteria

```yaml
type: functional
focus: "What the system must do"

templates:
  - "User can [action] to [achieve outcome]"
  - "System [processes/calculates/displays] [data] when [trigger]"
  - "Given [state], when [action], then [result]"

examples:
  - criteria: "User can reset password via email"
    given: "User has registered email"
    when: "User requests password reset"
    then: "Reset link sent within 5 minutes"
```

### Non-Functional Criteria

```yaml
type: non_functional
focus: "How the system should perform"

categories:
  performance:
    - "Response time < 200ms"
    - "Supports 1000 concurrent users"

  security:
    - "All passwords hashed with bcrypt"
    - "No SQL injection vulnerabilities"

  reliability:
    - "99.9% uptime"
    - "Automatic failover within 30s"

  usability:
    - "Form can be completed in < 2 minutes"
    - "Error messages are descriptive"
```

### Quality Criteria

```yaml
type: quality
focus: "Code and implementation standards"

categories:
  code_standards:
    - "No linting errors"
    - "All functions documented"

  test_coverage:
    - "Unit test coverage >= 80%"
    - "All edge cases tested"

  maintainability:
    - "Cyclomatic complexity < 10"
    - "No duplicate code blocks"
```

## Criteria Generation Process

### Step 1: Extract Requirements

```yaml
from_user_request:
  - Identify explicit requirements
  - Infer implicit requirements
  - Note constraints

from_goals:
  - Map achievement indicators to criteria
  - Define verification methods
```

### Step 2: Transform to Criteria

```yaml
for_each_requirement:
  - Define specific outcome
  - Add measurable threshold
  - Specify verification method
  - Assign priority
```

### Step 3: Validate Criteria

```yaml
validation_checklist:
  - [ ] Is it specific enough to implement?
  - [ ] Can it be objectively measured?
  - [ ] Is it achievable with current resources?
  - [ ] Does it align with user value?
  - [ ] Is the scope bounded?
```

## Output Format

```yaml
acceptance_criteria:
  functional:
    - id: "AC-FUNC-001"
      description: "User login functionality"
      given: "User has valid credentials"
      when: "User submits login form"
      then: "User is authenticated and redirected to dashboard"
      priority: must
      verification: "Integration test"

  non_functional:
    - id: "AC-PERF-001"
      description: "Login response time"
      criterion: "Login completes within 2 seconds"
      threshold: "< 2000ms"
      priority: should
      verification: "Load test"

  quality:
    - id: "AC-QUAL-001"
      description: "Code coverage"
      criterion: "Test coverage for auth module"
      threshold: ">= 80%"
      priority: must
      verification: "Coverage report"
```

## Integration

### Used By Agents

```yaml
primary_users:
  - goal-clarifier: "Criteria generation"

secondary_users:
  - deliverable-evaluator: "Evaluation reference"
```
