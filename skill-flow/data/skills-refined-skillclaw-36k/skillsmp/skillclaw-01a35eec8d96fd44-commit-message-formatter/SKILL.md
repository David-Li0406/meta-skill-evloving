---
name: commit-message-formatter
description: Use this skill when you need to write Git commit messages that adhere to the Conventional Commits specification, ensuring clarity and consistency in your commit history.
---

# Commit Message Formatter

When writing commit messages, follow these guidelines to ensure they conform to the Conventional Commits specification.

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

## Commit Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (e.g., formatting)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to CI/CD configuration
- **revert**: Reverts a previous commit
- **security**: Fixes related to security vulnerabilities

## Guidelines

1. **Subject Line**:
   - Should be no longer than 72 characters (50 characters is ideal).
   - Use imperative mood (e.g., "Add feature" not "Added feature").
   - Do not capitalize the first letter.
   - Do not end with a period.
   - Separate the subject from the body with a blank line.

2. **Body**:
   - Provide additional context about the change.
   - Explain the "what" and "why" of the change, not the "how".
   - Start with a blank line after the subject.

3. **Footer**:
   - Use for referencing issues or breaking changes.

## Examples

### Good Examples
```
feat(auth): add OAuth2 login support

Implement OAuth2 authentication flow to allow users to log in with their Google or GitHub accounts.

Closes #123
```

### Bad Examples
```
updated stuff
```

By following these guidelines, you can create meaningful and standardized commit messages that enhance the clarity of your project's history.