---
name: git-workflow
description: Manages git operations and conventional commits for Merge E-Commerce
trigger: "git operations OR commit changes OR create branch OR show status"
allowed-tools:
  - Bash(git status)
  - Bash(git diff)
  - Bash(git add)
  - Bash(git commit)
  - Bash(git log)
  - Bash(git branch)
  - Bash(git checkout)
  - Bash(git push)
  - Bash(git pull)
  - Bash(git stash)
  - Read
  - Glob
---

# Git Workflow Manager

Manages git operations following project conventions for the Merge E-Commerce Backend.

## Trigger Conditions

- User says "commit changes"
- User says "create branch"
- User says "show git status"
- User says "prepare release"
- Before/after code changes

## Conventional Commits

### Format
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| **feat** | New feature | `feat(api): add product search endpoint` |
| **fix** | Bug fix | `fix(domain): handle negative stock edge case` |
| **docs** | Documentation | `docs(readme): update API documentation` |
| **style** | Formatting | `style(api): fix indentation in controllers` |
| **refactor** | Code restructuring | `refactor(app): split large mapping profile` |
| **perf** | Performance | `perf(query): add index for product search` |
| **test** | Tests | `test(domain): add unit tests for Order aggregate` |
| **build** | Build system | `build(docker): update base image to .NET 9` |
| **ci** | CI/CD | `ci(github): add caching to workflow` |
| **chore** | Maintenance | `chore(deps): update NuGet packages` |
| **revert** | Revert commit | `revert: feat(api): add product endpoint` |

### Scopes (Project-Specific)

| Scope | Description | Affected Paths |
|-------|-------------|----------------|
| **api** | API layer | `Merge.API/Controllers/`, `Merge.API/Middleware/` |
| **app** | Application layer | `Merge.Application/` |
| **domain** | Domain layer | `Merge.Domain/Entities/`, `Merge.Domain/ValueObjects/` |
| **infra** | Infrastructure | `Merge.Infrastructure/` |
| **test** | Test files | `Merge.Tests/` |
| **auth** | Authentication | Auth-related files |
| **product** | Product module | Product-related files |
| **order** | Order module | Order-related files |
| **user** | User module | User-related files |
| **cart** | Cart module | Cart-related files |
| **payment** | Payment module | Payment-related files |
| **shipping** | Shipping module | Shipping-related files |
| **deps** | Dependencies | `*.csproj`, `Directory.Packages.props` |
| **docker** | Docker | `Dockerfile`, `docker-compose.yml` |
| **config** | Configuration | `appsettings*.json` |

### Examples

```bash
# Feature: New endpoint
git commit -m "feat(api): add product search endpoint

- Implement full-text search with PostgreSQL
- Support filtering by category, price range
- Add pagination with cursor-based navigation

Closes #123"

# Bug fix
git commit -m "fix(domain): prevent negative stock quantity

Guard against negative values in Product.UpdateStock()
Throws DomainException for invalid quantities

Fixes #456"

# Refactoring
git commit -m "refactor(app): extract product mapping to dedicated profile

- Move ProductMappingProfile from CommonMappings
- Add reverse mapping for updates
- Improve null handling in mappings"

# Performance improvement
git commit -m "perf(infra): add composite index for order queries

CREATE INDEX ix_orders_user_status ON orders(user_id, status)
Improves GetUserOrders query by 85%"

# Breaking change
git commit -m "feat(api)!: change product endpoint response format

BREAKING CHANGE: ProductDto now uses camelCase property names
Migration guide: Update frontend to use new property names"

# Multiple scopes
git commit -m "feat(api,domain): implement product variants

- Add ProductVariant entity
- Create variant management endpoints
- Include variants in product details"
```

## Branch Naming Convention

### Format
```
<type>/<ticket>-<short-description>
```

### Types

| Type | Purpose | Example |
|------|---------|---------|
| `feature/` | New feature | `feature/MERGE-123-product-search` |
| `fix/` | Bug fix | `fix/MERGE-456-order-calculation` |
| `hotfix/` | Production fix | `hotfix/MERGE-789-payment-crash` |
| `refactor/` | Code improvement | `refactor/MERGE-101-clean-services` |
| `release/` | Release prep | `release/v2.5.0` |
| `docs/` | Documentation | `docs/MERGE-202-api-docs` |
| `test/` | Test additions | `test/MERGE-303-order-tests` |

### Commands

```bash
# Create feature branch
git checkout -b feature/MERGE-123-product-search

# Create from specific branch
git checkout -b feature/MERGE-123-product-search origin/develop

# List branches
git branch -a

# Delete local branch
git branch -d feature/MERGE-123-product-search

# Delete remote branch
git push origin --delete feature/MERGE-123-product-search
```

## Git Workflow

### 1. Starting New Work

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/MERGE-123-new-feature

# Work on changes...
```

### 2. During Development

```bash
# Check status
git status

# Stage specific files
git add Merge.API/Controllers/ProductsController.cs
git add Merge.Application/Products/Commands/

# Stage all changes
git add -A

# Commit with conventional message
git commit -m "feat(api): add product creation endpoint"

# Push to remote
git push -u origin feature/MERGE-123-new-feature
```

### 3. Keeping Up to Date

```bash
# Fetch latest changes
git fetch origin

# Rebase on main (preferred for clean history)
git rebase origin/main

# Or merge (if conflicts are complex)
git merge origin/main

# Handle conflicts if any
git status
# Fix conflicts in files
git add <resolved-files>
git rebase --continue
# or
git commit -m "merge: resolve conflicts with main"
```

### 4. Before Pull Request

```bash
# Run tests
dotnet test

# Run build
dotnet build

# Check for uncommitted changes
git status

# Squash commits if needed (interactive rebase)
git rebase -i HEAD~3

# Force push after rebase (only on feature branches!)
git push --force-with-lease

# Create PR
gh pr create --title "feat(api): add product search" --body "..."
```

### 5. After PR Merged

```bash
# Switch to main
git checkout main

# Pull latest
git pull origin main

# Delete local feature branch
git branch -d feature/MERGE-123-new-feature

# Prune remote tracking branches
git fetch --prune
```

## Useful Git Commands

### Viewing History

```bash
# View recent commits
git log --oneline -10

# View commits with graph
git log --oneline --graph --all -20

# View commits by author
git log --author="Adem" --oneline -10

# View changes in commit
git show abc123

# View file history
git log --follow -p Merge.API/Controllers/ProductsController.cs
```

### Comparing Changes

```bash
# View unstaged changes
git diff

# View staged changes
git diff --staged

# Compare branches
git diff main..feature/MERGE-123

# Compare specific file between branches
git diff main..feature/MERGE-123 -- Merge.API/Controllers/ProductsController.cs
```

### Stashing

```bash
# Stash current changes
git stash

# Stash with message
git stash push -m "WIP: product validation"

# List stashes
git stash list

# Apply latest stash
git stash pop

# Apply specific stash
git stash apply stash@{1}

# Drop stash
git stash drop stash@{0}

# Clear all stashes
git stash clear
```

### Undoing Changes

```bash
# Discard unstaged changes in file
git checkout -- Merge.API/Controllers/ProductsController.cs

# Unstage file
git reset HEAD Merge.API/Controllers/ProductsController.cs

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes) - DANGEROUS
git reset --hard HEAD~1

# Revert a commit (creates new commit)
git revert abc123
```

### Tagging

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# List tags
git tag -l

# Push tags
git push origin --tags

# Delete tag
git tag -d v1.0.0
git push origin --delete v1.0.0
```

## Pre-commit Checklist

Before committing:

```bash
# 1. Check what will be committed
git status
git diff --staged

# 2. Verify code compiles
dotnet build --no-restore

# 3. Run tests
dotnet test --no-build

# 4. Check for secrets
grep -rn "password.*=.*\"" --include="*.cs" | grep -v Test
grep -rn "connectionstring.*=.*\"" --include="*.cs" -i

# 5. Format check (if using dotnet format)
dotnet format --verify-no-changes

# 6. Commit with meaningful message
git commit -m "feat(scope): description"
```

## Commit Message Generation

### Analyzing Changes

```bash
# Get list of changed files
git diff --name-only HEAD

# Get change statistics
git diff --stat HEAD

# Get detailed diff
git diff HEAD
```

### Auto-generating Message

Based on changes:
1. **New files** in `Controllers/` → `feat(api)`
2. **Modified** handler files → check if fix or feat
3. **New test files** → `test(scope)`
4. **Config changes** → `chore(config)` or `build`
5. **Multiple scopes** → use most significant or combine

## Release Workflow

```bash
# 1. Create release branch
git checkout -b release/v2.5.0 main

# 2. Update version numbers
# Edit Directory.Build.props, CHANGELOG.md

# 3. Commit version bump
git commit -m "chore(release): bump version to 2.5.0"

# 4. Create PR to main
gh pr create --title "Release v2.5.0" --base main

# 5. After merge, tag release
git checkout main
git pull
git tag -a v2.5.0 -m "Release v2.5.0"
git push origin v2.5.0

# 6. Merge back to develop (if using gitflow)
git checkout develop
git merge main
git push
```

## Troubleshooting

### Common Issues

```bash
# Fix "detached HEAD"
git checkout main

# Fix merge conflicts
git status  # See conflicted files
# Edit files to resolve conflicts
git add <resolved-files>
git commit

# Abort merge
git merge --abort

# Abort rebase
git rebase --abort

# Fix accidentally committed to wrong branch
git stash
git checkout correct-branch
git stash pop
git add -A
git commit -m "message"
```
