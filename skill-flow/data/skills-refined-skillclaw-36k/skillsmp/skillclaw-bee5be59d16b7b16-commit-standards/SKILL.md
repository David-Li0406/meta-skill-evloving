---
name: commit-standards
description: Use this skill when you need to format commit messages according to conventional standards for clarity and consistency.
---

# Commit Message Standards

> **Language**: [English](../../../../../skills/claude-code/commit-standards/SKILL.md) | 中文

**Version**: 1.0.0  
**Last Updated**: 2025-12-24  
**Scope**: Claude Code Skills

## Purpose

This skill ensures adherence to conventional commit standards, allowing for consistent and meaningful commit messages.

## Quick Reference

### Basic Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

| English | Usage |
|---------|-------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code refactoring (no functional change) |
| `docs` | Documentation only changes |
| `style` | Formatting changes (no code logic change) |
| `test` | Adding or updating tests |
| `perf` | Performance improvements |
| `build` | Changes to the build system or dependencies |
| `ci` | CI/CD process changes |
| `chore` | Maintenance tasks |
| `revert` | Reverting a previous commit |
| `security` | Security vulnerability fixes |

### Subject Line Rules

1. **Length**: ≤72 characters (50 is ideal)
2. **Tense**: Imperative mood (use "Add feature" instead of "Added feature")
3. **Capitalization**: Capitalize the first letter
4. **No Period**: Do not end with a period

## Detailed Guidelines

For complete standards, refer to:
- [Conventional Commits Guide](./conventional-commits.md)
- [Language Options](./language-options.md)

## Examples

### ✅ Good Examples

```
feat(auth): Add OAuth2 Google login support
fix(api): Resolve memory leak in user session cache
refactor(database): Extract query builder to separate class
docs(readme): Update installation instructions for Node 20
```

### ❌ Bad Examples

```
fixed bug                    # Too vague, no scope
feat(auth): added google login  # Past tense
Update stuff.                # Vague, with a period
WIP                          # Not descriptive
```

## Body Content Guidelines

Use the body to explain the **reason (WHY)** for the change:

```
fix(api): Resolve race condition in concurrent user updates

Why this occurred:
- Two simultaneous PUT requests could overwrite each other
- No optimistic locking implemented

What this fix does:
- Add version field to User model
- Return 409 Conflict if version mismatch

Fixes #789
```

## Breaking Changes

Be sure to document breaking changes in the footer:

```
feat(api): Change user endpoint response format

BREAKING CHANGE: User API response format changed

Migration guide:
1. Update API clients to remove .data wrapper
2. Use created_at instead of createdAt
```

## Issue References

```
Closes #123    # Automatically closes the issue
Fixes #456     # Automatically closes the issue
Refs #789      # Links but does not close
```

---

## Configuration Detection

This skill supports project-specific language configurations.

### Detection Order

1. Check the "Commit Message Language" section in `CONTRIBUTING.md`
2. If found, use the specified option (English / 中文 / Bilingual)
3. If not found, **default to English** for maximum tool compatibility

### Initial Setup

If no configuration is found and the context is unclear:

1. Ask the user: "This project has not configured a commit message language preference. Which option would you like to use? (English / 中文 / Bilingual)"
2. After the user selects, suggest recording it in `CONTRIBUTING.md`:

```markdown
## Commit Message Language Preference
```