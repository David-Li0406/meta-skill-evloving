---
name: committing-code
description: Generates clear commit messages. Use when tasked to commit any code.
context: fork
allowed-tools:
  - Bash(git diff:*)
  - Bash(git diff)
  - Bash(git status:*)
  - Bash(git status)
  - Bash(git commit:*)
  - Bash(git log:*)
  - Bash(git add:*)
  - Bash(git add *)
  - Read
---

# Instructions

1. Run `git status` to see modified and untracked files
2. Run `git diff` to review unstaged changes
3. Stage relevant files with `git add <files>` or `git add .`
4. Run `git diff --staged` to confirm staged changes
5. Create the commit following the conventional format below

**Note:** use all `git` commands without the `-C <dir>` argument!

# Conventional Commit Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types

| Type | Purpose |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | Performance improvement |
| `test` | Adding or correcting tests |
| `chore` | Maintenance tasks |

## Breaking Changes

Indicate breaking changes with an exclamation mark after the type:
```
feat!: remove deprecated API endpoint
```

Or use a footer:
```
feat: redesign user authentication

BREAKING CHANGE: JWT tokens now expire after 1 hour
```

## Rules

- Keep subject line under 72 characters
- Use imperative mood: "add feature" not "added feature"
- Do not end subject with a period
- Separate subject from body with a blank line
- Use body to explain what and why, not how

## Example

```
feat(auth): add OAuth2 login support

Implement OAuth2 authentication flow with support for Google and GitHub
providers. This replaces the legacy session-based authentication.

Closes #123

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Footer

Always include at the end:
```
Co-Authored-By: Claude <noreply@anthropic.com>
```
