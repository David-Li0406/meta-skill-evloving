---
name: execution
description: Main orchestration skill for executing approved fix plans
---

# Execution Skill

This is the main orchestration skill that coordinates the entire fix implementation process after a plan has been approved.

## Purpose

Execute approved fix plans by coordinating all other skills (git-operations, tdd-workflow, code-review) to implement, test, and commit the fix.

## When to Use

- After a plan has been approved via `@agent approve` comment
- When an execution task is received from the planning agent
- For implementing any approved code changes

## Prerequisites

1. Approved PLAN.md exists in the PR
2. Repository access via Git
3. Test framework is configured in the project

## Process

### Step 1: Setup Workspace
Using **git-operations** skill:
1. Clone the repository (if not already cloned)
2. Checkout the PR branch
3. Pull latest changes
4. Verify clean working state

### Step 2: Read and Parse Plan
1. Fetch PLAN.md from the PR
2. Parse implementation steps
3. Identify affected files
4. Identify test requirements

### Step 3: Execute TDD Workflow
Using **tdd-workflow** skill:

**RED Phase:**
1. Write failing tests as specified in plan
2. Run tests to verify they fail
3. Commit tests: `test: add tests for [issue]`

**GREEN Phase:**
1. Implement the fix as specified in plan
2. Make minimal changes to pass tests
3. Run tests to verify they pass
4. Commit fix: `fix: [description] ([issue-key])`

### Step 4: Verification
Using **code-review** skill:
1. Run full test suite
2. Run linters and type checks
3. Perform self-review of changes
4. Ensure no regressions

### Step 5: Commit and Push
Using **git-operations** skill:
1. Stage all changes
2. Create commits with conventional messages
3. Push to PR branch
4. Verify push succeeded

### Step 6: Update External Systems
1. Comment on PR with implementation summary
2. Mark PR as ready for review (remove draft)
3. Update Jira ticket status to "In Review"
4. Send Slack notification (if configured)

## Output Format

```json
{
  "status": "success|failed",
  "steps_completed": [
    "workspace_setup",
    "plan_parsed",
    "tests_written",
    "fix_implemented",
    "tests_passing",
    "code_reviewed",
    "committed",
    "pushed",
    "jira_updated",
    "slack_notified"
  ],
  "commits": [
    {
      "sha": "abc123",
      "message": "test: add tests for null check in auth service"
    },
    {
      "sha": "def456",
      "message": "fix: add null check for user session (PROJ-123)"
    }
  ],
  "test_results": {
    "total": 150,
    "passed": 150,
    "failed": 0,
    "skipped": 2
  },
  "pr_url": "https://github.com/org/repo/pull/123",
  "errors": []
}
```

## Error Handling

| Error | Action |
|-------|--------|
| Plan unclear | Comment on PR asking for clarification |
| Tests fail after fix | Report failure, do NOT force a fix |
| Merge conflicts | Report conflict, request human intervention |
| CI fails | Report CI failure with logs |

## Important

- **Follow the plan exactly** - don't improvise or add scope
- **If tests fail, report failure** - don't force a fix
- **Use conventional commit messages** - `fix:`, `test:`, `feat:`
- **Always run tests before marking complete**
- **If blocked, report the blocker clearly**
