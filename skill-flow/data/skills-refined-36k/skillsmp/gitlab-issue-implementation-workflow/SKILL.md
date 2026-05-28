---
name: gitlab-issue-implementation-workflow
description: GitLab Flow workflow for implementing issues. Use when the user asks to work on a GitLab issue, fix an issue, implement an issue, or mentions an issue number to implement.
---

# GitLab Issue Implementation Workflow

Follow this workflow whenever working on a GitLab issue.

## Checklist

1. **Get issue details** - Fetch the issue description, labels, and comments from GitLab
2. **Update the issue status label** - Make sure the issue status label is set to "Doing" and the "To Do" label is removed
3. **Check for existing MR** - Search for merge requests linked to this issue
4. **Create implementation plan if needed** - If no MR exists, create a detailed, step by step and actionable plan for the implementation
5. **Create MR if needed** - If no MR exists, create one from the issue (this also creates the branch), use the plan as the MR description task list
6. **Sync local branch** - `git fetch` and `git checkout` the MR's source branch (use the exact branch name from the MR)
7. **Work on the task** - Implement the required changes
8. **Run quality checks** - Read the README to find the appropriate commands for linting/formatting
9. **Run tests** - Read the README to find the appropriate test command
10. **Commit changes** - Commit with an appropriate message
11. **Update MR task checkbox** - Check ONLY the corresponding task checkbox in the MR description
12. **Post MR comment** - Add a comment summarizing the work done

## Instructions

### Step 1: Get Issue Details
Use `mcp__wally-git_aerys_in__get_issue_by_id` to fetch the issue (includes description and labels).
Use `mcp__wally-git_aerys_in__list_issue_notes` to fetch the issue comments.

### Step 2: Check for Existing MR
Use `mcp__wally-git_aerys_in__search_repository_merge_requests` with the issue number in search_text.
Also check the issue description/notes for MR links.

### Step 3: Create MR if Needed
If no MR exists, use `mcp__wally-git_aerys_in__create_merge_request_from_issue`.
This creates both the MR and its source branch.

### Step 4: Sync Local Branch
Use the exact `source_branch` name from the MR object:
```bash
git fetch origin
git checkout <source_branch>
git pull origin <source_branch>  # if branch already existed locally
```

### Step 5: Work on the Task
Implement the changes as described in the issue.

### Step 6: Run Quality Checks
Read the project's README.md to identify the commands for:
- Code formatting checks
- Linting / static analysis

Run these commands and fix any issues before proceeding.

### Step 7: Run Tests
Read the project's README.md to identify the test command.
Run the tests - all must pass before committing.

### Step 8: Commit Changes
```bash
git add <files>
git commit -m "<type>(<scope>): <description>"
```

## CRITICAL: Post-Task Hooks

After EACH task completion, you MUST perform these actions:

### Step 9: Update MR Task Checkbox
Use `mcp__wally-git_aerys_in__update_merge_request` to update the MR description.

**STRICT RULES:**
- ONLY change `- [ ]` to `- [x]` for the ONE task you just completed
- Do NOT modify ANY other content in the description
- Do NOT add, remove, or edit any other text
- Do NOT reformat or restructure the description
- The update must be a minimal, surgical change to check one checkbox

### Step 10: Post MR Comment
Use `mcp__wally-git_aerys_in__post_merge_request_comment` to add a comment summarizing:
- What was done
- Files changed
- Any relevant details about the implementation

## Notes

- Always apply relevant labels to issues when working on them
- Add questions and answers as comments on the issue (per CLAUDE.md)
