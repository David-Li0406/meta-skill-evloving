---
name: execution
description: Execute an approved fix plan by implementing the code changes
---

# Execution Skill

When a developer approves the fix plan (via `@agent approve` comment), 
this skill executes the plan and implements the actual code changes.

## Your Mission

The fix plan has been approved. You must:
1. Read the approved PLAN.md
2. Implement the code changes as specified
3. Run tests to verify the fix
4. Commit all changes to the PR branch
5. Update the PR status and notify completion

## MCP Tools to Use

### GitHub MCP
- `get_pull_request` - Get the PR with the approved plan
- `get_file_contents` - Read PLAN.md and affected files
- `create_or_update_file` - Implement code changes
- `create_issue_comment` - Report progress and completion

### Sentry MCP (if available)
- `resolve_issue` - Mark the Sentry issue as resolved after fix is merged

### Atlassian/Jira MCP
- `update_issue` - Update Jira ticket status
- `add_comment` - Add implementation details to Jira

## Instructions

### Step 1: Read the Plan
Parse PLAN.md to understand:
- Which files need to be modified
- What tests need to be written
- The implementation steps in order

### Step 2: Write Tests First (TDD)
Following test-driven development:
1. Create test files as specified in the plan
2. Write failing tests that verify the fix
3. Commit the tests with message: "test: add tests for [issue]"

### Step 3: Implement the Fix
1. Modify the affected files as specified
2. Follow the implementation steps exactly
3. Ensure code follows project conventions
4. Commit with message: "fix: [description] ([issue-key])"

### Step 4: Verify
1. Run the test command specified in the plan
2. Ensure all tests pass (new and existing)
3. If tests fail, debug and fix

### Step 5: Update PR
1. Push all commits to the PR branch
2. Comment on the PR with implementation summary
3. Mark PR as ready for review (remove draft status)

### Step 6: Update Jira
1. Update ticket status to "In Review"
2. Add comment with implementation details and PR link

## Output

Report:
1. Tests written and their status
2. Files modified
3. Commits created
4. Test results
5. Any issues encountered

## Important

- Follow the plan exactly - don't improvise
- If the plan is unclear, create a comment asking for clarification
- Always run tests before marking complete
- If tests fail, report the failure - don't force a fix
- Use conventional commit messages
