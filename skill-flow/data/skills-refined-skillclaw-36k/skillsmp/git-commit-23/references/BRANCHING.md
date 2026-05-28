# Git Branching Strategy

Guide for Git branching strategy.

## Overview

This project uses a feature branch workflow with specific naming conventions for organized development.

## Branch Types

### Main Branches

| Branch | Purpose | Protected |
|--------|---------|-----------|
| `main` / `master` | Production code | ✅ Yes |
| `develop` / `dev` | Integration branch for features | ✅ Yes |

### Feature Branches

Create feature branches from `develop` or `main`:

```bash
# Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/user-authentication

# Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/dashboard-updates
```

### Bugfix Branches

Create bugfix branches for critical fixes:

```bash
# Create bugfix branch
git checkout develop
git pull origin develop
git checkout -b bugfix/login-timeout

# Create hotfix branch for production issue
git checkout main
git pull origin main
git checkout -b hotfix/security-patch
```

## Branch Naming Conventions

### Feature Branches

Pattern: `feature/{description}`

```
✅ Good Examples:
feature/user-authentication
feature/dashboard-updates
feature/agent-execution-metrics
feature/analytics-reports

❌ Bad Examples:
new-feature
authentication
feature
feat-user-auth
```

### Bugfix Branches

Pattern: `bugfix/{description}` or `hotfix/{description}`

```
✅ Good Examples:
bugfix/login-timeout
bugfix/memory-leak
hotfix/security-patch
hotfix/critical-fix

❌ Bad Examples:
fix
bug
fix-login
patch
```

### Release Branches

Pattern: `release/{version}`

```
✅ Good Examples:
release/v1.0.0
release/v2.1.0

❌ Bad Examples:
release
v1.0.0
release-1.0.0
```

## Workflow: Feature Development

### 1. Create Feature Branch

```bash
# Start from develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/user-authentication
```

### 2. Work on Feature

```bash
# Make changes
# Write code
# Run tests
# Commit with proper format
git add .
git commit -m "feat: add user authentication service"
```

### 3. Sync with Develop

```bash
# Periodically sync with develop
git fetch origin
git rebase origin/develop

# Or merge develop into feature
git merge origin/develop
```

### 4. Push Feature Branch

```bash
# Push to remote
git push origin feature/user-authentication
```

### 5. Create Pull Request

```bash
# Create PR from feature to develop
# Use GitHub UI or GitHub CLI:
gh pr create --base develop --head feature/user-authentication
```

### 6. Merge to Develop

```bash
# After PR review and approval
# Squash merge to develop
# Or merge commit, depending on team preference
```

### 7. Delete Feature Branch

```bash
# Delete local branch
git branch -d feature/user-authentication

# Delete remote branch
git push origin --delete feature/user-authentication
```

## Workflow: Bugfix

### For Bugs in Development

```bash
# Create bugfix from develop
git checkout develop
git pull origin develop
git checkout -b bugfix/login-timeout

# Fix the bug
git add .
git commit -m "fix(api): resolve login timeout issue"

# Push and create PR
git push origin bugfix/login-timeout
gh pr create --base develop --head bugfix/login-timeout
```

### For Bugs in Production (Hotfix)

```bash
# Create hotfix from main
git checkout main
git pull origin main
git checkout -b hotfix/security-patch

# Fix the bug
git add .
git commit -m "fix(security): patch vulnerability"

# Push and create PR to main
git push origin hotfix/security-patch
gh pr create --base main --head hotfix/security-patch

# Also merge to develop after fix
```

## Workflow: Release

### 1. Create Release Branch

```bash
# From develop
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# Update version number
# Update changelog
```

### 2. Test Release Branch

```bash
# Run all tests
npm test

# Check for issues
# Fix any bugs found
```

### 3. Merge to Main

```bash
# Merge release to main
git checkout main
git merge release/v1.0.0

# Tag release
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin main --tags
```

### 4. Merge to Develop

```bash
# Merge release back to develop
git checkout develop
git merge release/v1.0.0
git push origin develop
```

### 5. Delete Release Branch

```bash
git branch -d release/v1.0.0
git push origin --delete release/v1.0.0
```

## Branch Protection Rules

### Protected Branches

Typically protected branches:
- `main` / `master`: Production
- `develop`: Integration

### Protection Rules

| Rule | Description |
|------|-------------|
| Require PR reviews | Must have at least 1 approval |
| Require status checks | All tests must pass |
| Require branches to be up to date | Must sync before merge |
| Restrict who can push | Only maintainers can push directly |

## Common Git Commands

### Branch Management

```bash
# List all branches
git branch -a

# List local branches
git branch

# List remote branches
git branch -r

# Create new branch
git checkout -b feature/new-feature

# Delete local branch
git branch -d feature/new-feature

# Delete remote branch
git push origin --delete feature/new-feature

# Rename branch
git branch -m old-name new-name
```

### Syncing

```bash
# Fetch all branches
git fetch --all

# Pull latest changes
git pull origin main

# Sync with remote
git pull --rebase origin main

# Rebase on top of develop
git rebase origin/develop
```

### Merging

```bash
# Merge branch into current
git merge feature/new-feature

# Squash merge (single commit)
git merge --squash feature/new-feature

# Merge with no fast-forward
git merge --no-ff feature/new-feature
```

### Divergence

```bash
# Check if branch is ahead/behind
git status

# See commits unique to branch
git log develop..feature/new-feature

# See commits unique to develop
git log feature/new-feature..develop
```

## Best Practices

1. **Branch from Appropriate Base**: Feature from develop, hotfix from main
2. **Descriptive Names**: Use feature/bugfix/hotfix prefixes
3. **Frequent Commits**: Commit small, logical changes
4. **Commit Message Format**: Follow Conventional Commits
5. **Sync Regularly**: Rebase or merge with base branch often
6. **Clean Up**: Delete merged branches
7. **Pull Requests**: Use PRs for all merges to protected branches
8. **Code Review**: All changes must be reviewed before merge
9. **Tests**: Ensure all tests pass before creating PR
10. **Update Documentation**: Update docs when needed

## Finding Branches

```bash
# List all branches
git branch -a

# List feature branches
git branch -a | grep feature/

# List bugfix branches
git branch -a | grep bugfix/

# List remote branches
git branch -r

# See which branches are merged
git branch --merged

# See which branches are unmerged
git branch --no-merged

# View commit history of branch
git log feature/new-feature --oneline -10
```

## Troubleshooting

### Merge Conflicts

```bash
# When merging and conflicts occur:
git merge feature/new-feature

# Resolve conflicts manually in files
git add resolved-file.ts
git commit -m "merge: resolve conflicts"
```

### Diverged Branches

```bash
# When branch and remote have diverged:
git pull origin main

# Choose strategy:
# 1. Merge: git pull origin main (default)
# 2. Rebase: git pull --rebase origin main
# 3. Reset: git reset --hard origin/main
```

### Orphaned Branches

```bash
# Find branches that aren't on remote
git branch --no-contains origin/main

# Clean up old branches
git branch -d old-feature-branch
```

## Related Skills

- **`git-commit`** - Commit message format and hooks
- **`testing`** - Test execution before PR
- **`biome`** - Code quality checks in hooks
