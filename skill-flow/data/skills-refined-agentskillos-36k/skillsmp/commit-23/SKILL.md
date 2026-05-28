---
name: commit
description: Commit changes, save work, create git commit. Use when done coding, ready to commit, need to save progress, or "commit this". Creates conventional commit messages focused on why, not what.
argument-hint: Optional message hint or --amend flag
disable-model-invocation: true
---

# Commit Changes

Create a high-quality commit with a message that captures the intent, not just the mechanics.

## Process

### 1. Analyze Changes

Run in parallel:

```bash
git diff --cached              # Staged changes (or git diff if nothing staged)
git status                     # What's changed
git log --oneline -5           # Match repository style
```

### 2. Understand the Why

Before writing the message, identify:

- **What problem does this solve?**
- **Why was this change necessary?**
- **What decision was made?** (if alternatives existed)

The diff shows *what* changed. The message explains *why*.

### 3. Draft Message

```
type(scope): concise summary in imperative mood

Optional body explaining WHY this change was made.
Not what changed (the diff shows that), but why.

Co-Authored-By: Claude <noreply@anthropic.com>
```

### 4. Refine and Commit

Before committing, verify:

- Type accurately reflects the change
- Summary is specific, not vague
- Every word earns its place
- Imperative mood ("add" not "added")
- Under 72 characters

```bash
git add [files]  # Stage if needed
git commit -m "..."
```

## Commit Types

| Type | Use For |
|------|---------|
| `feat` | New feature or functionality |
| `fix` | Bug fix |
| `refactor` | Code restructuring (no behavior change) |
| `docs` | Documentation only |
| `chore` | Maintenance, dependencies, config |
| `test` | Adding or modifying tests |
| `perf` | Performance improvements |

## Message Quality

**Good**: Explains intent
```
feat(auth): add rate limiting to login endpoint

Prevents brute-force attacks by limiting attempts per IP.
```

**Bad**: Just describes the diff
```
feat(auth): add rate limiter middleware and config
```

**Good**: Specific
```
fix(api): handle null response from payment provider
```

**Bad**: Vague
```
fix(api): fix bug
```

## When to Add a Body

Add a body when:
- The *why* isn't obvious from the summary
- You chose between multiple approaches
- There's important context for future readers
- Breaking changes need explanation

## Scope Guidelines

Include scope when changes focus on a specific module. Skip when changes span multiple areas or scope is obvious from context.

```
feat(auth): add OAuth2 provider
fix(api): handle null response
refactor(database): normalize user schema
chore: update dependencies
```

## Key Principles

- **Why over what**: The diff shows what; the message explains why
- **Concise**: Every word must earn its place
- **Imperative**: "add feature" not "added feature"
- **Specific**: "fix login validation" not "fix bug"
- **Match style**: Check `git log` and follow existing patterns
