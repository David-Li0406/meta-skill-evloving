---
name: create-pull-request
description: Use this skill when creating a pull request to ensure clarity and ease of review.
---

# Skill body

1. **Prepare the Branch:**
   - Ensure you are on a feature branch (NEVER the main branch). If not, stop and ask for guidance.
   - Confirm that all workspace changes have been committed. If not, stop and ask for guidance.
   - Verify that the branch is pushed and that origin and local are in sync.

2. **Analyze Changes:**
   - Call the `fetch_feature_branch` tool to get the current branch's changes. If there are no changes, stop.

3. **Create PR Title:**
   - Write a clear, descriptive title that explains what the PR accomplishes. If applicable, prepend the title with the Linear issue ID in square brackets.

4. **Create PR Description:**
   - Write a concise description focused on essential information:
     - **Summary:** A short paragraph explaining what changed and why.
     - **Changes:** A bulleted list of key modifications.
   - Avoid including implementation details, acceptance criteria, test plans, or lists of changed files/lines.

5. **Present for Review:**
   - Show the proposed PR title and body to the user. Ask if they would like to proceed or make changes.

6. **Create the Pull Request:**
   - After user approval, push commits using `git push`.
   - Create the PR using: `gh pr create --web --title "<title>" --body "<description>"`.