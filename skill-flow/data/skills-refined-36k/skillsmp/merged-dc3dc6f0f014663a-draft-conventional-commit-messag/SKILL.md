---
name: draft-conventional-commit-message
description: Use this skill to draft a conventional commit message based on the user's code changes and git diff output.
---

# Draft Conventional Commit Message

This skill drafts conventional commit messages that accurately summarize code changes based on the provided change summary and git diff output.

## When to Use This Skill

- User asks to commit code changes
- User requests a commit message draft
- User wants to create a conventional commit message
- Before committing changes to version control

## Requirements

- Use the Conventional Commits format: `type(scope): summary`
- Supported types include: `bump`, `feat`, `fix`, `docs`, `refactor`, `test`, `ci`, `chore`, `perf`, and `revert`
- Use the imperative mood in the summary (e.g., "Add", "Fix", "Refactor")
- Keep the summary under 72 characters
- If there are breaking changes, include a `BREAKING CHANGE:` footer
- Always use English

## Instructions

1. Run the `git diff` command to show both unstaged and staged full diffs.
2. Analyze the git diff output to identify the type of change and determine the scope of changes and affected components.
3. Draft a clear, concise commit message following the Conventional Commits format.
4. Ensure each commit represents one atomic task only, focusing on a single logical change with a short, clear message.

### Atomic Commits - One Task Per Commit

- Create separate commits for different types of changes (feature vs bugfix vs docs vs refactor).
- Avoid multi-line commit messages that describe multiple unrelated changes.

**Examples**:
- Instead of: "Add feature X and feature Y" → Create two commits: `feat: add feature X`, `feat: add feature Y`
- Instead of: "Fix bug A and bug B" → Create two commits: `fix: resolve bug A`, `fix: resolve bug B`

Do not include content such as:
```
Generated with xx
Co-Authored-By: xxx
```