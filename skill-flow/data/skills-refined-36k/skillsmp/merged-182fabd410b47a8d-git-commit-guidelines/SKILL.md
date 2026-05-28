---
name: git-commit-guidelines
description: Use this skill when you need to create a commit, write a commit message, or seek guidance on conventional commit formats and best practices.
---

# Git Commit Guidelines

This skill provides comprehensive guidance for writing well-structured commit messages following the Conventional Commits specification.

## Commit Workflow

1. Run `git status` and `git diff` to analyze changes.
2. If there are unstaged changes to include, stage them with `git add`.
3. Check recent commits with `git log --oneline -5` for style reference.
4. Determine the appropriate commit type based on the nature of changes.
5. Write a concise commit message in imperative mood.
6. Create the commit.

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Commit Types

| Type       | Description                                             |
|------------|---------------------------------------------------------|
| `feat`     | New feature or capability added                         |
| `fix`      | Bug fix                                                 |
| `docs`     | Documentation only changes                              |
| `style`    | Formatting, whitespace, semicolons (no code change)    |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test`     | Adding or correcting tests                              |
| `chore`    | Maintenance tasks, build process, dependencies         |

## Writing Good Commit Messages

### Description Guidelines

- Use imperative mood ("add feature" not "added feature").
- Keep the subject line under 50 characters when possible.
- Do not end the subject with a period.
- Focus on the "what" and "why", not the "how".
- Include a blank line between the subject and body.

### Examples

**Good:**

```
feat(auth): add user authentication endpoint

Implement Google and GitHub OAuth providers.
Closes #123
```

**Bad:**

```
Updated the login page to support OAuth
```

## Breaking Changes

Mark breaking changes with an exclamation mark (!) after type/scope:

```
feat!: remove deprecated API endpoints
```

Or include `BREAKING CHANGE:` in the footer:

```
feat: update authentication flow

BREAKING CHANGE: JWT tokens now expire after 1 hour instead of 24 hours
```