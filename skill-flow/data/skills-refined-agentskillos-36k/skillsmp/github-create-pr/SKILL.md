---
name: github-create-pr
description: Creates a pull request from the current branch to the main branch.
---

# Create Pull Request

## Instructions
1. Check current branch and ensure it's not main/master
2. Check for uncommitted changes and warn if present
3. Get the diff between current branch and main branch
4. Review recent commits on this branch to understand the changes
5. Create a PR with:
   - Clear, descriptive title
   - Summary of changes in the body
   - Test plan section
6. Push the branch if needed and create the PR using `gh pr create`
