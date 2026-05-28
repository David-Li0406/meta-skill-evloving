---
name: committing-and-generating-commit-messages
description: Use this skill when creating clear and consistent commit messages following conventional commit conventions.
---

# Instructions

1. Run `git status` to see modified and untracked files.
2. Run `git diff` to review unstaged changes.
3. Stage relevant files with `git add <files>` or `git add .`.
4. Run `git diff --staged` to confirm staged changes.
5. Review recent commit messages with `git log` to match the repository's existing style.
6. Suggest a commit message adhering to the conventional commit format below.

## Conventional Commit Format

```
<type>(<optional scope>): <subject>

[optional body]

[optional footer(s)]
```

### Common Types:
- **feat**: A new feature (user-facing functionality)
- **fix**: A bug fix
- **docs**: Documentation changes only
- **style**: Code style changes (formatting, missing semicolons, etc.) - no logic changes
- **refactor**: Code changes that neither fix bugs nor add features
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Changes to build process, dependencies, or tooling
- **ci**: Changes to CI/CD configuration

### Guidelines for Commit Messages:
- Use present tense with imperative mood: "add feature" not "added feature".
- Keep the subject line under 72 characters.
- Do not capitalize the first letter after the colon.
- Do not end the subject with a period.
- Separate the subject from the body with a blank line.
- Use the body to explain what and why, not how.
- Wrap the body at 72 characters and can include multiple paragraphs.

### Example:
```
feat(auth): add OAuth2 login support

Implement OAuth2 authentication flow with support for Google and GitHub
providers. This replaces the legacy session-based authentication.

Closes #123

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Fixup and Amend Commits:
When creating an `amend!` commit to update both the content AND commit message of a target commit:
1. **First line**: Identifies the target commit using `amend!` prefix.
2. **Second line**: Blank line.
3. **Third line**: The NEW subject line (even if unchanged from original).
4. **Fourth line onwards**: The new commit message body.

**Example:**
```
amend! fix: old commit message
```