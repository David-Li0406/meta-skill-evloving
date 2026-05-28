---
name: unstaged-reviews
description: reviews uncommitted changes and suggests improvements
allowed-tools: Bash, Grep, Glob, Read, mcp__deepwiki, mcp__ide__getDiagnostics, mcp__gitkraken
---

# /unstaged-reviews

1. Run `git status` to see what's changed
2. Run `git diff` to see the actual changes
3. For each modified file, analyze:
   - Is the change correct and complete?
   - Are there any potential bugs?
   - Does it follow project conventions?
   - Are there any security concerns?
   - Is error handling adequate?
4. Provide a summary with:
   - What looks good
   - Any concerns or suggestions
   - Recommended next steps (test, commit, or make changes)
