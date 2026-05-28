# Branch Naming Conventions

Complete guide to branch naming standards and patterns.

## Standard Format

```
<type>/<issue-id>-<short-description>
```

### Examples
```
feature/PROJ-123-add-user-login
fix/PROJ-456-null-pointer-exception
chore/update-dependencies
docs/PROJ-789-api-documentation
refactor/PROJ-101-extract-auth-service
```

## Branch Types

| Type | Purpose | Example |
|------|---------|---------|
| `feature` | New functionality | `feature/PROJ-123-shopping-cart` |
| `fix` | Bug fixes | `fix/PROJ-456-login-error` |
| `hotfix` | Urgent production fixes | `hotfix/PROJ-789-security-patch` |
| `chore` | Maintenance tasks | `chore/update-node-version` |
| `docs` | Documentation only | `docs/api-reference` |
| `refactor` | Code restructuring | `refactor/PROJ-101-auth-module` |
| `test` | Test additions | `test/PROJ-202-unit-tests` |
| `release` | Release preparation | `release/v1.2.0` |

## Naming Rules

### Required
- Lowercase only
- Use hyphens to separate words
- Include issue ID when applicable
- Keep description under 50 characters

### Forbidden
- Spaces or special characters
- Uppercase letters
- Underscores (use hyphens)
- Generic names like "fix" or "update"

## Validation Regex

```regex
^(feature|fix|hotfix|chore|docs|refactor|test|release)\/([A-Z]+-\d+-)?[a-z0-9-]+$
```

## Good vs Bad Examples

| Good | Bad | Why |
|------|-----|-----|
| `feature/PROJ-123-add-login` | `feature/AddLogin` | Use lowercase, include issue |
| `fix/PROJ-456-fix-null-ptr` | `bugfix` | Include type, issue, description |
| `chore/update-deps` | `chore/update_dependencies` | Use hyphens not underscores |
| `release/v2.0.0` | `release-2.0` | Use forward slash separator |

## Issue ID Patterns

| Project Style | Pattern | Example |
|---------------|---------|---------|
| Jira | `PROJ-123` | `feature/PROJ-123-description` |
| GitHub | `#123` or `gh-123` | `fix/gh-123-bug-description` |
| No tracker | Omit ID | `chore/update-dependencies` |

## Branch Lifecycle

```
1. Create from main/develop
   git checkout -b feature/PROJ-123-new-feature

2. Work on feature
   git commit -m "feat: implement feature"

3. Push to remote
   git push -u origin feature/PROJ-123-new-feature

4. Create PR → Merge → Delete branch
```

## Protected Branches

Never commit directly to:
- `main` / `master`
- `develop`
- `release/*`

These require pull requests.

## Quick Reference

```bash
# Create feature branch
git checkout -b feature/PROJ-123-description

# Create fix branch
git checkout -b fix/PROJ-456-bug-description

# Create from specific base
git checkout -b feature/PROJ-123-feature develop
```
