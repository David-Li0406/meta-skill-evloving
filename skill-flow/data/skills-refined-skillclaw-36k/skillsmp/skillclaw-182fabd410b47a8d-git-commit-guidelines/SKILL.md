---
name: git-commit-guidelines
description: Use this skill when you need guidance on writing commit messages, including formatting, style, and best practices for conventional commits.
---

# Git Commit Guidelines

This skill provides comprehensive guidance for writing conventional commit messages.

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Commit Types

| Type       | Description                                         |
|------------|-----------------------------------------------------|
| `feat`     | New feature or capability added                     |
| `fix`      | Bug fix                                             |
| `docs`     | Documentation only changes                          |
| `style`    | Formatting changes, no code change                  |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test`     | Adding or correcting tests                          |
| `chore`    | Maintenance tasks, build process, dependencies     |

## Commit Workflow

1. Run `git status` and `git diff` to analyze changes.
2. Stage changes with `git add` if necessary.
3. Check recent commits with `git log --oneline -5` for style reference.
4. Determine the appropriate commit type based on the nature of changes.
5. Write a concise commit message in imperative mood.
6. Create the commit.

## Writing Good Commit Messages

### Subject Line Guidelines

- Keep the subject line under 50 characters.
- Use imperative mood (e.g., "Add feature" not "Added feature").
- Do not end the subject line with a period.
- Include a blank line between the subject and body.

### Body Guidelines

- The body should explain the "what" and "why" of the changes, not the "how".

## Examples

**Good:**
```
feat(auth): add OAuth2 login support

Implement Google and GitHub OAuth providers.
Closes #123
```

**Bad:**
```
Updated the login page to support OAuth
```