---
name: linear-issue
description: Automate the complete Linear issue workflow - fetch issue, update status to In Progress, create branch, implement, test, create PR, and move to In Review
---

# Linear Issue Workflow

Automates the complete workflow for working on Linear issues: fetch issue, update status, create branch, implement, test, create PR, and mark for review.

## Usage

```
/linear-issue MEG-5
```

Or simply:

```
/linear-issue
```

(Will prompt you to select an issue)

## Workflow

This skill automates the following steps:

1. **Fetch Issue**: Get issue details from Linear
2. **Update to In Progress**: Move issue to "In Progress" state
3. **Create Branch**: Create a new git branch based on issue identifier and title
4. **Implement**: Guide implementation according to issue requirements
5. **Test**: Verify the implementation works correctly
6. **Create PR**: Create a GitHub pull request with issue details
7. **Update to In Review**: Move issue to "In Review" state and link PR

## Instructions

When this skill is invoked:

1. **Parse the issue identifier** from the arguments (e.g., "MEG-5"). If no argument provided, list recent backlog issues and ask user to select one.

2. **Fetch the issue details** from Linear using `mcp__linear__Linear_GetIssue` with the issue identifier.

3. **Update issue status to "In Progress"** using `mcp__linear__Linear_TransitionIssueState` with target state "In Progress".

4. **Create a git branch**:
   - Generate branch name from issue: `feature/MEG-5-short-description` (use kebab-case)
   - Run: `git checkout -b <branch-name>`
   - Confirm branch created successfully

5. **Review the issue details with the user**:
   - Display the issue title, description, and scope
   - Show the review checklist
   - Show files that will be changed
   - Ask user to confirm before proceeding with implementation

6. **Implement the feature**:
   - Follow the issue's objective and scope exactly
   - Use the TodoWrite tool to track implementation progress based on the issue's scope
   - Create/modify files as specified in the issue
   - Ensure code follows project conventions
   - Add proper error handling and type safety
   - Follow the review checklist items

7. **Test the implementation**:
   - Run relevant tests based on the issue's testing checklist
   - Verify no TypeScript errors: `bun run type-check` (if such script exists)
   - Test manually if needed
   - Ensure all success criteria are met
   - Fix any issues found during testing

8. **Commit the changes**:
   - Stage all changes: `git add .`
   - Create a descriptive commit message referencing the issue
   - Commit format: `feat(scope): description\n\nFixes MEG-X\n\nCo-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>`

9. **Push and create PR**:
   - Push branch: `git push -u origin <branch-name>`
   - Create PR using `gh pr create` with:
     - Title: Issue title
     - Body: Include issue summary, implementation notes, testing done, and link to Linear issue
     - Use format:
       ```
       ## Summary
       [Brief description of changes]

       ## Implementation
       [Key implementation details]

       ## Testing
       - [x] Testing item 1
       - [x] Testing item 2

       ## Review Checklist
       [Copy from issue]

       Closes [Linear issue URL]

       🤖 Generated with [Claude Code](https://claude.com/claude-code)
       ```

10. **Update issue to "In Review"**:
    - Use `mcp__linear__Linear_TransitionIssueState` with target state "In Review"
    - Add a comment to the Linear issue with the PR URL using `mcp__linear__Linear_AddComment`

11. **Confirm completion**:
    - Display summary of what was done
    - Show the PR URL
    - Show the updated Linear issue URL
    - Remind user that issue is now in review

## Error Handling

- If issue not found, list available backlog issues
- If branch already exists, ask user if they want to switch to it or create a new one
- If tests fail, fix issues before creating PR
- If PR creation fails, provide manual instructions
- If Linear state transition fails, continue but warn user to update manually

## Notes

- This skill assumes Linear states "In Progress" and "In Review" exist
- The skill will use fuzzy matching for state names if exact match fails
- Always verify implementation works before creating PR
- Never create PR with failing tests or TypeScript errors
