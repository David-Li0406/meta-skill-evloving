---
name: committing-and-generating-commit-messages
description: Use this skill when creating commits, suggesting commit messages, or amending commits in a Git repository.
---

# Instructions

1. Run `git status` to see modified and untracked files.
2. Run `git diff` to review unstaged changes.
3. Stage relevant files with `git add <files>` or `git add .`.
4. Run `git diff --staged` to confirm staged changes.
5. Suggest or create a commit message adhering to the conventional commit format below.

## Conventional Commit Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Common Types

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
| `ci` | Changes to CI/CD configuration |

### Scope (optional)

The scope specifies what part of the codebase is affected (e.g., `feat(auth):`, `fix(api):`). Use when it adds clarity; omit when the change is global or obvious.

### Subject Line

- Use present tense with imperative mood ("add feature" not "added feature").
- Keep under 72 characters.
- Do not capitalize the first letter after the colon.
- Do not end with a period.

### Body (optional)

- Separate from the subject with a blank line.
- Explain what and why, not how.
- Wrap at 72 characters.
- Can include multiple paragraphs.

### Example

```
feat(auth): add OAuth2 login support

Implement OAuth2 authentication flow with support for Google and GitHub
providers. This replaces the legacy session-based authentication.
```

## Fixup and Amend Commits

### `amend!` Commit Format

When creating an `amend!` commit to update both the content and commit message of a target commit:

1. **First line**: Identifies the target commit using `amend!` prefix.
2. **Second line**: Blank line.
3. **Third line**: The NEW subject line (even if unchanged from original).
4. **Fourth line onwards**: The new commit message body.

**Example:**
```
amend! fix: old commit message subject

fix: new commit message subject

New commit message body explaining the changes.
```

### `fixup!` Commits

For `fixup!` commits (content changes only, no message update), just use:
```
fixup! original commit subject

A concise description of the changes made in the fixup. This message will be
discarded when the fixup is applied, so it is only for the benefit of the
developer and the reviewer.
```

## Best Practices

- Match the existing commit message style in the repository (check `git log`).
- Write for the team; explain the "why" in a way that stands alone without conversation context.
- Avoid referencing conversations or including attribution in commit messages.

**Bad examples:**
- "Using Option B approach as discussed"
- "Removed oldFunction since we decided it wasn't needed"