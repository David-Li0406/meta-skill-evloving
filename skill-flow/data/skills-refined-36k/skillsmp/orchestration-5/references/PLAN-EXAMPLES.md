# Execution Plan Examples

Complete examples of multi-step workflow plans.

## Plan Structure

```yaml
plan:
  id: "plan-unique-id"
  name: "Human-readable name"
  description: "What this plan accomplishes"
  steps:
    - id: "step-1"
      skill: "skill-name"
      action: "action-name"
      params: {}
      rollback: {}
      dependsOn: []
```

## Example: Implement Feature

```yaml
plan:
  id: "implement-feature-001"
  name: "Implement User Authentication"
  description: "Create branch, update Jira, implement feature, create PR"

  steps:
    - id: "create-branch"
      skill: "git-operations"
      action: "create-branch"
      params:
        name: "feature/PROJ-123-user-auth"
        base: "main"
      rollback:
        action: "delete-branch"
        params:
          name: "feature/PROJ-123-user-auth"

    - id: "update-jira-start"
      skill: "jira-write"
      action: "transition"
      params:
        issue: "PROJ-123"
        transition: "Start Progress"
      dependsOn: ["create-branch"]
      rollback:
        action: "transition"
        params:
          issue: "PROJ-123"
          transition: "To Do"

    - id: "implement-code"
      skill: "code-generation"
      action: "implement"
      params:
        specification: "User authentication with JWT"
      dependsOn: ["update-jira-start"]
      # No automatic rollback for code changes

    - id: "run-tests"
      skill: "test-execution"
      action: "run-all"
      params:
        coverage: true
      dependsOn: ["implement-code"]

    - id: "create-pr"
      skill: "pr-creation"
      action: "create"
      params:
        title: "feat(auth): add user authentication"
        base: "main"
        head: "feature/PROJ-123-user-auth"
      dependsOn: ["run-tests"]
      rollback:
        action: "close"
```

## Example: Bug Fix Workflow

```yaml
plan:
  id: "bug-fix-002"
  name: "Fix Critical Bug"
  description: "Hotfix workflow for production issue"

  steps:
    - id: "create-hotfix"
      skill: "git-operations"
      action: "create-branch"
      params:
        name: "hotfix/PROJ-456-critical-fix"
        base: "main"

    - id: "update-jira"
      skill: "jira-write"
      action: "update"
      params:
        issue: "PROJ-456"
        priority: "Highest"
        labels: ["hotfix", "production"]
      dependsOn: ["create-hotfix"]

    - id: "transition-progress"
      skill: "jira-write"
      action: "transition"
      params:
        issue: "PROJ-456"
        transition: "Start Progress"
      dependsOn: ["update-jira"]

    - id: "apply-fix"
      skill: "code-generation"
      action: "fix-bug"
      params:
        issue: "PROJ-456"
      dependsOn: ["transition-progress"]

    - id: "verify-fix"
      skill: "test-execution"
      action: "run-specific"
      params:
        pattern: "**/auth/**"
      dependsOn: ["apply-fix"]
```

## Example: Sprint Planning

```yaml
plan:
  id: "sprint-setup-003"
  name: "Setup Sprint 10"
  description: "Move issues to sprint and update statuses"

  steps:
    - id: "move-stories"
      skill: "jira-write"
      action: "move-to-sprint"
      params:
        sprint: 10
        issues: ["PROJ-101", "PROJ-102", "PROJ-103"]

    - id: "update-sprint-goal"
      skill: "jira-write"
      action: "update-sprint"
      params:
        sprintId: 10
        goal: "Complete authentication module"
      dependsOn: ["move-stories"]

    - id: "notify-team"
      skill: "notification"
      action: "send"
      params:
        channel: "#dev-team"
        message: "Sprint 10 is ready for planning"
      dependsOn: ["update-sprint-goal"]
```

## Parallel Execution

```yaml
plan:
  id: "parallel-001"
  name: "Parallel Validation"
  parallel: true  # Enable parallel execution

  steps:
    # These run in parallel (no dependencies)
    - id: "lint"
      skill: "code-quality"
      action: "lint"

    - id: "unit-tests"
      skill: "test-execution"
      action: "run-unit"

    - id: "type-check"
      skill: "code-quality"
      action: "typecheck"

    # This waits for all above
    - id: "integration-tests"
      skill: "test-execution"
      action: "run-integration"
      dependsOn: ["lint", "unit-tests", "type-check"]
```

## Conditional Steps

```yaml
steps:
  - id: "check-coverage"
    skill: "test-execution"
    action: "run-coverage"
    output: "coverage_result"

  - id: "fail-if-low"
    skill: "orchestration"
    action: "assert"
    condition: "coverage_result.percentage >= 80"
    onFail: "abort"
    dependsOn: ["check-coverage"]
```
