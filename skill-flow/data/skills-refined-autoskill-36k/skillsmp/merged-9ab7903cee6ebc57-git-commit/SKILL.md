---
name: git-commit
description: Use this skill when you need to create a git commit with a meaningful message, follow conventional commit guidelines, or seek guidance on commit message formatting.
---

# Git Commit Workflow

This skill provides a structured approach to creating git commits with well-crafted messages.

## Commit Process

1. Run `git status` and `git diff --staged` to review changes.
2. If there are no staged changes, ask the user what to stage or stage all with `git add -A`.
3. Analyze the changes and determine the appropriate commit type based on the nature of the modifications.
4. Write a concise commit message that:
   - Starts with a verb (e.g., Add, Fix, Update, Remove, Refactor).
   - Summarizes the "why" of the changes, not just the "what".
   - Keeps the first line under 50 characters.
5. Create the commit using the message.
6. Display the commit hash upon completion.

## Commit Message Structure

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

| Type       | Description                                         |
|------------|-----------------------------------------------------|
| `feat`     | New feature or capability added                     |
| `fix`      | Bug fix                                             |
| `docs`     | Documentation only changes                          |
| `style`    | Formatting, whitespace, semicolons (no code change)|
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test`     | Adding or correcting tests                          |
| `chore`    | Maintenance tasks, build process, dependencies     |

## Writing Good Commit Messages

### Guidelines

- Use imperative mood (e.g., "Add feature" not "Added feature").
- Keep the subject line under 50 characters.
- Do not end the subject line with a period.
- Include a blank line between the subject and body.
- The body should explain what and why, not how.

### Examples

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

## Breaking Changes

Mark breaking changes with an exclamation mark (!) after type/scope or include `BREAKING CHANGE:` in the footer.

```
feat!: remove deprecated API endpoints
feat(api)!: change response format to JSON:API
```