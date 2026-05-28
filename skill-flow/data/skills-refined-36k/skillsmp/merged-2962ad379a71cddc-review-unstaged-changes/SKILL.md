---
name: review-unstaged-changes
description: Use this skill to review uncommitted changes in your codebase and suggest improvements.
---

# Review Unstaged Changes

1. Run `git status` to see the current unstaged and staged changes.
2. Run `git diff` to view the actual changes made.
3. For each modified file, analyze:
   - Is the change correct and complete?
   - Are there any potential bugs?
   - Does it follow project conventions?
   - Are there any security concerns?
   - Is error handling adequate?
4. Provide a summary that includes:
   - What looks good
   - Any concerns or suggestions
   - Recommended next steps (test, commit, or make changes)