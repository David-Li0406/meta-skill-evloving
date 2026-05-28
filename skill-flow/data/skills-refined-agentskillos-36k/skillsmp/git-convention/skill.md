---
name: git-convention
description: MANDATORY for all git operations. Enforces git commit message conventions. STRICTLY REQUIRED when user asks to commit changes or generate commit messages. DO NOT manually run git commands, always delegate to this skill. Ensures consistent commit message format, auto-generates conventional commits.
---

# Git Commit Message Convention

Follow these rules when generating git commit messages.

## Format

All commit messages must be in English and follow this format:

1.  **Header**: The first line should contain the change type (feat/fix/chore/build/ci...) and a summary.
2.  **Body**: The second line must be empty (required only if Details are present).
3.  **Details**: Subsequent lines should use a numbered list to describe specific changes. **OMIT** this section (and the empty Body line) if there is only one change point.

## Example

### Multiple Changes

```
feat: add new feature for display control

1. Add DisplayController class
2. Update configuration parsing logic
3. Add unit tests for new functionality
```

### Single Change

```
fix: correct typo in README
```

## Command Line Usage

When performing the commit via command line:

- For **multiple changes**, use a single `-m` flag with an open quote to create a multi-line message. Press `Enter` to create new lines (including the required empty line after the header) and close the quote at the end.
- For **single change**, use a standard single-line commit message.

```bash
# Multiple changes
git commit -m "feat: add new feature for display control

1. Add DisplayController class
2. Update configuration parsing logic"

# Single change
git commit -m "fix: correct typo in README"
```

## When to Use

- When the user asks to commit changes.
- When generating a commit message for a pull request or commit.

## Constraints

- **DO NOT** execute `git push` automatically after committing. Wait for explicit user instruction to push.
