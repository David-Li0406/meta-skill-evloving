---
name: git
description: Execute Git commands including status, diff, log, branch, checkout, merge, and stash operations
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: version-control
---

## What I do

I execute Git commands to manage source code versioning. I can show repository status, display changes, view commit history, manage branches, merge code, and stash uncommitted work.

## When to use me

Use this when:

- You need to check repository status or changes
- You're creating or switching branches
- You need to merge branches or resolve conflicts
- You're staging and committing changes
- You need to stash work temporarily

## Common Commands

```bash
git status              # Show working tree status
git diff                # Show unstaged changes
git diff --staged       # Show staged changes
git log --oneline       # Show commit history
git branch -a           # List all branches
git checkout <branch>   # Switch to branch
git checkout -b <name>  # Create and switch to new branch
git merge <branch>      # Merge branch into current
git stash               # Stash uncommitted changes
git stash pop           # Apply stashed changes
```

## Source Files

- `.git/` directory: Git repository data
- `package.json`: May contain git-related scripts

## Code Patterns

- Always verify current branch before operations
- Use `git status` before commit to review changes
- Check `git log` to understand commit history
- Use `git diff` to review modifications

## Operational Constraints

- Never force push to main/master without explicit user request
- Warn user before destructive operations (reset, clean)
- Follow repository's branch naming conventions
- Use conventional commit message format
