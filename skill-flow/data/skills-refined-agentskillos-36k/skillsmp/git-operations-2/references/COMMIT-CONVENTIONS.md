# Conventional Commits Guide

Complete reference for writing standardized commit messages.

## Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

## Types

| Type | Description | Changelog Section |
|------|-------------|-------------------|
| `feat` | New feature | Features |
| `fix` | Bug fix | Bug Fixes |
| `docs` | Documentation only | Documentation |
| `style` | Formatting, no code change | Styles |
| `refactor` | Code change, no feature/fix | Code Refactoring |
| `perf` | Performance improvement | Performance |
| `test` | Adding tests | Tests |
| `build` | Build system changes | Build |
| `ci` | CI configuration | CI |
| `chore` | Maintenance | Chores |
| `revert` | Revert previous commit | Reverts |

## Scope

Optional context for the change:

```
feat(auth): add OAuth2 support
fix(api): handle null response
docs(readme): update installation steps
refactor(utils): extract validation helpers
```

Common scopes:
- Component names: `auth`, `api`, `ui`, `db`
- Layer names: `controller`, `service`, `model`
- Feature areas: `login`, `checkout`, `search`

## Description

- Use imperative mood: "add" not "added" or "adds"
- Lowercase first letter
- No period at the end
- Max 50 characters

### Good Examples
```
feat: add user authentication
fix: prevent race condition in cache
docs: clarify setup instructions
refactor: simplify error handling logic
```

### Bad Examples
```
feat: Added user authentication    # Past tense
fix: Fixes the bug.               # Capitalized, period
update                            # No type, too vague
WIP                               # Not descriptive
```

## Body

Optional detailed explanation:

```
fix(auth): prevent session timeout during refresh

The previous implementation did not extend the session
when the refresh token was used, causing unexpected
logouts for active users.

This change ensures the session TTL is reset on
each successful token refresh.
```

## Footer

### Breaking Changes

```
feat(api): change response format

BREAKING CHANGE: API responses now use camelCase
instead of snake_case for all field names.
```

### Issue References

```
fix(checkout): calculate tax correctly

Closes #123
Fixes PROJ-456
Refs #789
```

## Complete Examples

### Simple Commit
```
feat(cart): add quantity selector
```

### With Body
```
fix(payment): retry failed transactions

Add automatic retry logic for payment failures
caused by temporary network issues. Retries up
to 3 times with exponential backoff.
```

### Breaking Change
```
feat(api)!: require authentication for all endpoints

BREAKING CHANGE: All API endpoints now require a valid
JWT token in the Authorization header. Anonymous access
has been removed.

Migration guide: https://docs.example.com/auth-migration
```

### Multiple Issues
```
fix(validation): sanitize user input

- Escape HTML entities in text fields
- Validate email format before submission
- Trim whitespace from all inputs

Closes #123, #124
Fixes PROJ-456
```

## Validation Regex

```regex
^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z-]+\))?!?: .{1,50}$
```

## Pre-commit Hook

```bash
#!/bin/sh
commit_regex='^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z-]+\))?!?: .{1,50}'

if ! grep -qE "$commit_regex" "$1"; then
    echo "Invalid commit message format"
    echo "Expected: <type>(<scope>): <description>"
    exit 1
fi
```

## Quick Reference

```bash
# Feature
git commit -m "feat(auth): add social login"

# Bug fix
git commit -m "fix(api): handle empty response"

# Breaking change
git commit -m "feat(api)!: change endpoint structure"

# With issue reference
git commit -m "fix(ui): correct button alignment

Closes #123"
```
