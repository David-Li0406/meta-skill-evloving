# Atomic Commits Examples

## Single-File Changes

### Simple Feature
```bash
# Changed: api/routes/users.py (added new endpoint)

git add api/routes/users.py
git commit -m "feat(api): add endpoint to list user preferences"
```

### Bug Fix
```bash
# Changed: core/database.py (fixed connection leak)

git add core/database.py
git commit -m "fix(db): close connections on query timeout"
```

### Documentation
```bash
# Changed: README.md

git add README.md
git commit -m "docs: add deployment instructions for kubernetes"
```

## Multi-File, Single Concern

### Feature Spanning Multiple Files
```bash
# Changed:
#   - models/notification.py (new model)
#   - services/notification_service.py (new service)
#   - api/routes/notifications.py (new endpoint)

git add models/notification.py services/notification_service.py api/routes/notifications.py
git commit -m "feat(notifications): add push notification system"
```

### Refactoring Across Files
```bash
# Changed:
#   - services/auth.py (extracted function)
#   - services/token_validator.py (new file with extracted code)
#   - services/__init__.py (updated exports)

git add services/
git commit -m "refactor(auth): extract token validation to dedicated module"
```

## Splitting Changes Into Atomic Commits

### Scenario: Feature + Refactoring + Tests

**Bad (one big commit):**
```bash
git add .
git commit -m "add user preferences with refactoring and tests"
```

**Good (atomic commits):**
```bash
# Commit 1: Preparatory refactoring
git add services/user_service.py
git commit -m "refactor(users): extract preference handling to separate method"

# Commit 2: Core feature
git add models/preference.py api/routes/preferences.py services/preference_service.py
git commit -m "feat(users): add user preference management"

# Commit 3: Tests
git add tests/test_preferences.py tests/fixtures/preferences.py
git commit -m "test(users): add preference management tests"
```

### Scenario: Bug Fix + Style Fix

**Bad:**
```bash
git add .
git commit -m "fix bug and format code"
```

**Good:**
```bash
# Commit 1: Style (separate, non-functional change)
git add -p  # Stage only formatting changes
git commit -m "style(auth): apply black formatting"

# Commit 2: Bug fix (the actual fix)
git add auth/token.py
git commit -m "fix(auth): handle expired refresh tokens correctly"
```

### Scenario: Dependency Update + Code Changes

**Bad:**
```bash
git add .
git commit -m "upgrade fastapi and update code"
```

**Good:**
```bash
# Commit 1: Dependency update
git add requirements.txt pyproject.toml
git commit -m "build(deps): upgrade fastapi to 0.100.0"

# Commit 2: Code adaptations
git add api/
git commit -m "refactor(api): adapt to fastapi 0.100 API changes"
```

## Breaking Changes

### API Breaking Change
```bash
# Changed authentication method

git add api/middleware/auth.py api/routes/users.py
git commit -m "feat(api)!: migrate from API key to JWT authentication

BREAKING CHANGE: All endpoints now require Bearer token.
API key authentication is no longer supported.

Migration guide:
1. Generate JWT token via /auth/token
2. Include 'Authorization: Bearer <token>' header
3. Remove X-API-Key header from requests"
```

### Database Schema Change
```bash
git add migrations/versions/001_add_preferences.py models/user.py
git commit -m "feat(db)!: add preferences column to users table

BREAKING CHANGE: Requires database migration.
Run 'alembic upgrade head' before deploying."
```

## Complex Real-World Scenarios

### Feature: Add Search Functionality

```bash
# Step 1: Infrastructure
git add core/embeddings.py
git commit -m "feat(core): add embedding generation utility"

# Step 2: Database support
git add migrations/versions/002_add_vector_column.py
git commit -m "feat(db): add vector column for semantic search"

# Step 3: Search service
git add services/search_service.py
git commit -m "feat(search): implement vector similarity search"

# Step 4: API endpoint
git add api/routes/search.py
git commit -m "feat(api): add search endpoint"

# Step 5: Tests
git add tests/test_search.py tests/fixtures/search_data.py
git commit -m "test(search): add search functionality tests"

# Step 6: Documentation
git add docs/search.md
git commit -m "docs(search): add search API documentation"
```

### Hotfix: Production Bug

```bash
# Quick fix with minimal changes
git add core/database.py
git commit -m "fix(db): prevent connection pool exhaustion under load

Pool was not releasing connections on timeout.
Added explicit cleanup in finally block."
```

### Chore: Repository Maintenance

```bash
# Separate housekeeping commits
git add .gitignore
git commit -m "chore: ignore IDE-specific files"

git add .pre-commit-config.yaml
git commit -m "chore: configure pre-commit hooks"

git add pyproject.toml
git commit -m "chore: add black and isort configuration"
```

## Interactive Staging with git add -p

When a file contains multiple logical changes:

```bash
# File has both a bug fix and a new feature
git add -p path/to/file.py

# Git will show hunks one by one:
# Stage this hunk [y,n,q,a,d,s,e,?]?
#   y - stage this hunk
#   n - don't stage
#   s - split into smaller hunks
#   e - manually edit hunk

# After staging bug fix hunks:
git commit -m "fix(module): handle edge case in parser"

# Stage remaining feature hunks:
git add -p path/to/file.py
git commit -m "feat(module): add streaming support"
```

## Commit Message Bodies

### When to Include Body

Include body for:
- Complex changes needing explanation
- Non-obvious decisions
- Breaking changes
- Bug fixes with root cause analysis

### Format
```
feat(api): add rate limiting to public endpoints

Implement token bucket algorithm with configurable limits.
Default: 100 requests/minute for authenticated users,
10 requests/minute for anonymous.

Closes #123
```

### Bug Fix with Context
```
fix(db): resolve deadlock in concurrent transactions

Root cause: Multiple transactions acquiring locks in
different orders on user and preferences tables.

Solution: Enforce consistent lock ordering by always
acquiring user lock before preferences lock.

Affects: User preference update operations
Tested: 10k concurrent requests with no deadlocks
```
