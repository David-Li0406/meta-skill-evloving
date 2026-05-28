---
name: git-operations
description: Handle all Git operations for code changes
---

# Git Operations Skill

This skill handles all Git operations required for implementing and committing code changes.

## Purpose

Execute Git operations reliably and consistently, following best practices for branching, committing, and pushing code changes.

## When to Use

- Setting up workspace for a new task
- Creating feature branches
- Committing code changes
- Pushing to remote
- Updating PRs

## Available Operations

### 1. Clone Repository
```bash
git clone <repository-url> <workspace-path>
cd <workspace-path>
```

### 2. Checkout Branch
```bash
# Checkout existing branch
git checkout <branch-name>

# Create and checkout new branch
git checkout -b <new-branch-name>
```

### 3. Pull Latest Changes
```bash
git fetch origin
git pull origin <branch-name>
```

### 4. Create Feature Branch
```bash
# Branch naming convention
fix/sentry-<issue-id>     # For Sentry-triggered fixes
fix/<jira-key>-<summary>  # For Jira-triggered fixes
feat/<feature-name>       # For new features
```

### 5. Stage and Commit
```bash
git add <files>
git commit -m "<type>: <description>"
```

### 6. Push to Remote
```bash
git push origin <branch-name>

# Force push if needed (after rebase)
git push --force-with-lease origin <branch-name>
```

## Commit Convention

Use **Conventional Commits** format:

| Type | Description | Example |
|------|-------------|---------|
| `fix:` | Bug fix | `fix: handle null user session` |
| `feat:` | New feature | `feat: add password reset flow` |
| `test:` | Adding tests | `test: add auth service tests` |
| `docs:` | Documentation | `docs: update API documentation` |
| `refactor:` | Code refactoring | `refactor: extract auth logic` |
| `chore:` | Maintenance | `chore: update dependencies` |

### Commit Message Format
```
<type>: <short description> (<issue-key>)

[optional body]

[optional footer]
```

**Examples:**
```
test: add tests for null check in auth service

- Add test for expired session handling
- Add test for missing user object

Refs: PROJ-123
```

```
fix: add null check for user session (PROJ-123)

The session object could be undefined when the user's
session expires. This adds a guard clause to prevent
the null pointer exception.

Co-authored-by: AI Agent <ai-agent@company.com>
```

## Process

### Workspace Setup Flow
```
1. Check if workspace exists
   ├─ Yes: Pull latest changes
   └─ No: Clone repository

2. Checkout feature branch
   ├─ Exists: Checkout and pull
   └─ New: Create from main/master

3. Verify clean state
   └─ No uncommitted changes
```

### Commit Flow
```
1. Run tests (verify passing)
2. Stage specific files (not git add .)
3. Create commit with conventional message
4. Verify commit succeeded
```

### Push Flow
```
1. Verify local branch is ahead of remote
2. Push to origin
3. If conflict: Report and request intervention
4. Verify push succeeded
```

## Output Format

```json
{
  "operation": "setup|commit|push",
  "status": "success|failed",
  "details": {
    "repository": "org/repo",
    "branch": "fix/sentry-PROJ-123",
    "commits": ["abc123", "def456"],
    "pushed": true
  },
  "errors": []
}
```

## Error Handling

| Error | Action |
|-------|--------|
| Clone failed | Check credentials, report error |
| Merge conflict | Report conflict, do NOT auto-resolve |
| Push rejected | Pull latest, report if still failing |
| Authentication failed | Report credential issue |

## Important

- **NEVER force push without `--force-with-lease`**
- **NEVER commit directly to main/master**
- **ALWAYS use specific file staging, not `git add .`**
- **ALWAYS verify tests pass before committing**
- **Include issue key in commit messages**
