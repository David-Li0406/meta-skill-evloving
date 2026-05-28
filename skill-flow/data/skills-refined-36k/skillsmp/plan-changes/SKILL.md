---
name: plan-changes
description: Handle PR comment feedback and update the plan accordingly
---

# Plan Changes Skill

When a developer comments on a PR requesting changes, this skill handles
updating the plan based on their feedback.

## Your Mission

A developer has commented on the fix plan PR requesting changes. You must:
1. Read the PR comment and understand the requested changes
2. Update the PLAN.md with the revised approach
3. Commit the changes to the PR branch
4. Reply to the comment confirming the changes

## MCP Tools to Use

### GitHub MCP
- `get_pull_request` - Get PR details including the current PLAN.md
- `get_issue_comments` - Read the comment that triggered this
- `get_file_contents` - Read the current PLAN.md
- `create_or_update_file` - Update PLAN.md with changes
- `create_issue_comment` - Reply to the developer's comment

## Instructions

### Step 1: Understand the Feedback
Read the developer's comment carefully. Common types of feedback:
- "Add more tests for edge case X"
- "Consider the performance impact of Y"
- "This approach won't work because Z, try instead..."
- "Please also fix related issue in file W"

### Step 2: Update the Plan
Revise PLAN.md to address the feedback:
- Add new sections if needed
- Modify existing steps
- Add the feedback to an "Addressed Feedback" section
- Keep the original structure intact

### Step 3: Commit and Reply
1. Commit the updated PLAN.md to the PR branch
2. Reply to the comment with:
   - Summary of changes made
   - Any questions if the feedback was unclear
   - Request for re-review

## Output

Report:
1. What changes were requested
2. How you updated the plan
3. The commit SHA of your update
4. Your reply to the developer

## Important

- Be respectful and collaborative in your reply
- If feedback is unclear, ask for clarification
- Do not change code files - only update the plan
- The developer must approve before execution
