---
name: git-commit-conventional
description: Use this skill when creating git commits, writing commit messages, or following version control workflows.
---

# Git Commit Conventional Skill

## Overview

This skill helps generate well-formatted commit messages following the Conventional Commits specification, ensuring clear and readable project history.

## When to Use This Skill

Use this skill when:

- Creating git commits
- Writing conventional commit messages
- Working with staged changes that need to be committed
- Preparing a new version or release (SemVer)
- Updating the project `CHANGELOG.md`

## Critical Rules

- **ALWAYS** follow the **Conventional Commits** format: `type(scope): subject`
- **NEVER** write subjects in past tense ("fixed", "added"); use imperative mood ("fix", "add")
- **ALWAYS** keep the title at **50 characters** or fewer
- **ALWAYS** add a `BREAKING CHANGE:` footer for backward-incompatible changes
- **NEVER** bundle multiple logical changes into one commit; keep them atomic and focused
- **NEVER STAGE OR UNSTAGE FILES WITHOUT EXPLICIT PERMISSION**

## Commit Message Format

### Structure

```text
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Allowed Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc.)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `build`: Changes that affect the build system or external dependencies
- `ci`: Changes to CI configuration files and scripts
- `chore`: Other changes that don't modify src or test files

### Subject Rules

- Use strict **imperative mood** ("add" not "added", "fix" not "fixed").
- Max 50 characters.
- No period at the end.
- Lowercase first letter.

## Workflow

1. **Check Staged Changes**: Use `git status` to identify staged and unstaged files. If nothing is staged, ask the user for permission to stage files.
2. **Read Staged Diff**: Use `git diff --cached` to analyze what changes are staged.
3. **Analyze Intent**: Determine the purpose of the changes.
4. **Draft Message**: Apply the formatting rules to create a commit message.
5. **Review**: Ensure the message adheres to the rules (length, mood, etc.).

## Commit Message Examples

### Feature Commit

```text
feat(agents): add agent versioning support

Implement agent version tracking and add version comparison endpoint.

Co-authored-by: John Doe <john@example.com>
```

### Bug Fix Commit

```text
fix(webapi): resolve NaN flowId in metrics

Validate flowId before processing and add error logging for invalid IDs.

Fixes #123
```

### Breaking Change

```text
feat(agents): restructure agent configuration model

BREAKING CHANGE: Agent configuration now uses new model. Migration required for existing agents.
```

## Best Practices

- **Atomic Commits**: Each commit should contain related changes that serve a single purpose.
- **Descriptive Messages**: Explain **what** changed and **why**.
- **Consistent Formatting**: Follow the conventional commits specification and maintain proper line wrapping (72 characters).

## Testing Your Commit

Before committing, verify:

1. [ ] Type is from the allowed list
2. [ ] Description is in imperative mood
3. [ ] Description is lowercase
4. [ ] No trailing period on description
5. [ ] Breaking changes marked with `!` or footer
6. [ ] AI attribution included (if applicable)
7. [ ] Body explains WHY not HOW
8. [ ] Using `--signoff` flag

## Related Skills

- `/git-committer-atomic` - Plan atomic commits