---
name: pr
description: This skill should be used when the user asks to "create a PR", "open a pull request", "submit for review", or wants to push their branch and create a GitHub pull request.
---

# /pr

Create a GitHub pull request for the current branch.

## Instructions

1. Check current branch with `git branch --show-current`
2. If on main, ask user to create a feature branch first
3. Push the branch if not already pushed: `git push -u origin HEAD`
4. Run `git log main..HEAD` to see commits in this branch
5. Create PR with `gh pr create`:
   - Title: concise summary of the change
   - Body: bullet points of what changed and why
6. Return the PR URL
