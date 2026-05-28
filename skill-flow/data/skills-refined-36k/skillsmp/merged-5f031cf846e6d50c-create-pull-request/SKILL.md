---
name: create-pull-request
description: Use this skill when creating a pull request to ensure clarity and conciseness.
---

# Creating Pull Requests

Your job is to create a clean, concise pull request that's easy to understand and review.

## Process

1. **Check Branch Status:**
   - Ensure you are on a feature branch (NEVER the main branch). If not, stop and ask the user for guidance.
   - Confirm all workspace changes have been committed. If not, stop and ask the user for guidance.
   - Verify that the branch is pushed and that origin and local are in sync.

2. **Analyze Changes:**
   - Call the `fetch_feature_branch` tool to get the current branch's changes. If there are no changes, stop.

3. **Check for Linear Issue:**
   - Run `./scripts/extract-issue-from-current-branch.sh` to check if the current branch has a Linear issue ID. If it outputs an issue ID, fetch the Linear issue using the Linear MCP.

4. **Create PR Title:**
   - Write a clear, descriptive title that explains what the PR accomplishes. If there's a Linear issue, prepend the title with the issue ID in square brackets.

5. **Create PR Description:**
   - Write a concise description focused on essential information. Use the following structure:
     - **Summary:** Short paragraph explaining what changed and why.
     - **Changes:** Bulleted list of key modifications.
   - Be brief and avoid implementation details, acceptance criteria, test plans, or lists of changed files/lines.
   - If there are key concerns (e.g., backwards compatibility issues or risky code changes), create a **Key Concerns** section in the description.

6. **Present for Review:**
   - Show the proposed PR title and body to the user. Ask if they'd like to proceed or make changes.

7. **Create PR:**
   - After user approval, push commits: `git push`.
   - Create the PR using: `gh pr create --web --title "<title>" --body "<description>"`.