---
name: github-commit
description: Create, amend, and manage Git commits with gh CLI including status checks and commit message validation
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: version-control
---

## What I do

I create and manage Git commits using the GitHub CLI (`gh`). I stage changes, draft commit messages, validate against conventions, and push commits to remote repositories.

## When to use me

Use this when:

- You're ready to commit staged changes
- You need to amend a commit you just made
- You want to validate commit messages before committing
- You're pushing commits to GitHub

## Common Workflow

```bash
git status                    # Review changes first
git diff --staged             # Verify staged changes
git commit -m "type(scope): description"  # Commit
git push                      # Push to remote
```

## Key Concepts

- **Commit Message Format**: `<type>(<scope>): <description>`
- **Types**: feat, fix, docs, style, refactor, test, chore
- **Scope**: Optional component or file area
- **Body/Footer**: For detailed descriptions and breaking changes

## Source Files

- `.github/` directory: May contain commit templates
- `package.json`: May contain commit-related scripts

## Code Patterns

- Always review `git status` and `git diff` before committing
- Use conventional commit format
- Include issue numbers in footer (e.g., Fixes #123)
- Push after successful commit

## Operational Constraints

- Never commit without reviewing changes first
- Don't amend pushed commits (unless explicitly requested)
- Use clear, descriptive commit messages
- Follow repository's commit conventions
