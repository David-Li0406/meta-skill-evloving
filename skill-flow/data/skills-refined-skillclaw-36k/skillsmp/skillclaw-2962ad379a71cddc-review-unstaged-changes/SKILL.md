---
name: review-unstaged-changes
description: Use this skill when you need to review uncommitted changes in your codebase and suggest improvements.
---

# Skill body

1. Run `git status` to see which files have uncommitted changes.
2. Run `git diff` to view the actual changes made to the files.
3. For each modified file, analyze the following:
   - Is the change correct and complete?
   - Are there any potential bugs?
   - Does it adhere to project conventions?
   - Are there any security concerns?
   - Is error handling adequate?
4. Summarize your findings, including:
   - What looks good
   - Any concerns or suggestions for improvement
   - Recommended next steps (e.g., test, commit, or make further changes)