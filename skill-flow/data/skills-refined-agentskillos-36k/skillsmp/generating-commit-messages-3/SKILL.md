---
name: generating-commit-messages
description: "Generates clear commit messages following conventional commit conventions. Use when creating commits, suggesting commit messages, amending commits, creating fixup commits, or any operation involving git commit messages."
---

# Generating Commit Messages

## Instructions

1. Run `git log` to see recent commit messages and match the repository's existing commit message style
2. Run `git diff --staged` to see the changes being committed
3. Suggest a commit message adhering to conventional commit message conventions

## Conventional Commit Format

Use the conventional commit format: `<type>(<scope>): <subject>`

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

### Scope (optional):
- The scope specifies what part of the codebase is affected (e.g., `feat(auth):`, `fix(api):`)
- Use when it adds clarity, omit when the change is global or obvious

### Subject line:
- Use present tense with imperative mood ("add feature" not "added feature")
- Don't capitalize first letter after the colon
- No period at the end
- Keep under 72 characters

### Body (optional):
- Separate from subject with a blank line
- Explain what and why, not how
- Wrap at 72 characters
- Can include multiple paragraphs

### Example:
```
feat(router): add support for nested routes

Implements nested routing to allow for more complex application structures.
This enables parent-child route relationships and hierarchical navigation.
```

## Best practices

- Use present tense with the imperative mood
- Explain what and why, not how
- Match the existing commit message style in the repository (check `git log`)

## Fixup and Amend Commits

### `amend!` Commit Format

When creating an `amend!` commit to update both the content AND commit message of a target commit:

1. **First line**: Identifies the target commit using `amend!` prefix
2. **Second line**: Blank line
3. **Third line**: The NEW subject line (even if unchanged from original)
4. **Fourth line onwards**: The new commit message body

**Example:**
```
amend! fix: old commit message subject

fix: new commit message subject

New commit message body explaining the changes.
```

**IMPORTANT**: Even if the subject line isn't changing, you must still include it again after the blank line. The first line with `amend!` is only used to identify the target commit during `git rebase --autosquash`.

### `fixup!` Commits

For `fixup!` commits (content changes only, no message update), just use:
```
fixup! original commit subject

A concise description of the changes made in the fixup. This message will be
discarded when the fixup is applied, so it is only for the benefit of the
developer and the reviewer.
```

## Audience Awareness

When writing commit messages:

- **Never reference our conversation** - Don't mention "Option A/B", "as discussed", "per your request", etc. Write for developers who won't have seen our chat.
- **Write for the team** - Commits will be read by other developers. Explain the "why" in a way that stands alone without our conversation context.
- Do not include Claude Code attribution in commit messages.

**Bad examples:**
- "Using Option B approach as discussed"
- "Removed oldFunction since we decided it wasn't needed"
- ```
  🤖 Generated with [Claude Code](https://claude.com/claude-code)

  Co-Authored-By: Claude <noreply@anthropic.com>
  ```
