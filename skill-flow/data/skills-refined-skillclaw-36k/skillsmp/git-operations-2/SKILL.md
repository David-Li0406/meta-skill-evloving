---
name: git-operations
description: Git repository operations including branching, committing, pushing, and viewing history. Use for version control tasks. Destructive operations require explicit approval.
license: MIT
compatibility: Requires git CLI installed and repository access
metadata:
  author: ximplicity
  version: "1.0"
  category: git
---

# Git Operations Skill

Version control operations for Git repositories.

## Allowed Operations

- Clone repositories
- Create branches
- Switch branches
- Commit changes
- Push to remote
- Pull from remote
- Fetch updates
- View status, log, diff

## Forbidden Operations

These require explicit user approval:

- Force push (`--force`)
- Rebase
- Reset `--hard`
- Delete remote branches
- Modify git hooks
- Change git config globally

## Constraints

- No direct commits to `main` or `master`
- Branch names must follow convention
- Commit messages must follow conventional commits

## Quick Branch Reference

```
<type>/<issue-id>-<short-description>

feature/PROJ-123-add-login
fix/PROJ-456-null-pointer
chore/update-dependencies
```

Types: `feature`, `fix`, `chore`, `docs`, `refactor`

For complete naming rules, see [BRANCH-NAMING.md](references/BRANCH-NAMING.md).

## Quick Commit Reference

```
<type>(<scope>): <description>

feat(auth): add login endpoint
fix(api): handle null response
docs(readme): update setup guide
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

For complete format, see [COMMIT-CONVENTIONS.md](references/COMMIT-CONVENTIONS.md).

## Safety Checks

Before any operation:
1. Verify working directory is clean
2. Verify on correct branch
3. Check for uncommitted changes

## Example Usage

```
Create branch feature/PROJ-123-user-auth
Commit changes with message "feat(auth): add login endpoint"
Push current branch to origin
Show git status and recent commits
```
