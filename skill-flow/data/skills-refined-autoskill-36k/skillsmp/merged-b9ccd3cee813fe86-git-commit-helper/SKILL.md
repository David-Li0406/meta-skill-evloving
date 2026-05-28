---
name: git-commit-helper
description: Use this skill to generate well-structured git commit messages following Conventional Commits standards and to create commits based on staged changes.
---

# Git Commit Helper

## Overview

This skill assists in generating descriptive commit messages by analyzing staged changes and following Conventional Commits format. It can also automate the staging and committing process.

## Quick Start

1. **Review Staged Changes**:
   ```bash
   git diff --staged
   ```

2. **Generate Commit Message**:
   - Analyze the changes and determine the appropriate type (e.g., `feat`, `fix`, `docs`, etc.).
   - Write a concise description (under 72 characters).

3. **Commit Changes**:
   ```bash
   git commit -m "type(scope): description" -m "Detailed explanation if necessary"
   ```

## Commit Message Format

Follow the Conventional Commits format:

```
<type>(<scope>): <description>

[optional body]
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semicolons)
- **refactor**: Code restructuring without behavior change
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Scopes

Optional. Use when it adds clarity. Examples: `api`, `ui`, `auth`, `db`.

### Breaking Changes

Indicate breaking changes clearly with a `!` suffix:
```
feat(api)!: change response format
```

## Workflow

1. **Check for Staged Changes**:
   - Run `git diff --cached --name-status`.
   - If staged files exist, proceed to commit using the staged set.

2. **Stage Changes if None are Staged**:
   - Use a script to stage tracked changes and selectively stage untracked files.

3. **Compose a Commit Message**:
   - Format:
     - Title line: `type(scope): short summary`
     - Body: 2-6 bullet points describing the most important changes.

4. **Commit without Confirmation**:
   - Use multi-line message via repeated `-m` flags.

## Best Practices

- **Atomic Commits**: One logical change per commit.
- **Test Before Commit**: Ensure code works.
- **Reference Issues**: Include issue numbers if applicable.
- **Keep it Focused**: Don't mix unrelated changes.
- **Write for Humans**: Future you will read this.

## Commit Message Checklist

- [ ] Type is appropriate (feat/fix/docs/etc.)
- [ ] Scope is specific and clear
- [ ] Summary is under 72 characters
- [ ] Summary uses imperative mood
- [ ] Body explains WHY not just WHAT
- [ ] Breaking changes are clearly marked
- [ ] Related issue numbers are included

## Examples

**Feature Commit:**
```
feat(auth): add JWT authentication

Implement JWT-based authentication system with:
- Login endpoint with token generation
- Token validation middleware
- Refresh token support
```

**Bug Fix:**
```
fix(api): handle null values in user profile

Prevent crashes when user profile fields are null.
Add null checks before accessing nested properties.
```

**Refactor:**
```
refactor(database): simplify query builder

Extract common query patterns into reusable functions.
Reduce code duplication in database layer.
```