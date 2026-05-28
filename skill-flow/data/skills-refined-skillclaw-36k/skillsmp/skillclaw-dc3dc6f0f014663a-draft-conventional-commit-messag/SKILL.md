---
name: draft-conventional-commit-message
description: Use this skill when you need to draft a conventional commit message based on code changes.
---

# Skill body

Draft a conventional commit message that matches the change summary provided by the user.

## Requirements
- Use the Conventional Commits format: `type(scope): summary`.
- Use the imperative mood in the summary (for example, "Add", "Fix", "Refactor").
- The supported types are `bump`, `feat`, `fix`, `docs`, `refactor`, `test`, `ci`, `chore`, `perf`, and `revert`.
- Keep the summary under 72 characters.
- If there are breaking changes, include a `BREAKING CHANGE:` footer.
- Always use English.

## Instructions
1. Run the `git diff` command to show both unstaged and staged changes.
2. Analyze the output to identify the type of change (e.g., feat, fix, etc.) and the scope of the changes.
3. Draft a clear and concise commit message following the Conventional Commits format.
4. Ensure that each commit represents one atomic task only, avoiding multi-line messages that describe multiple unrelated changes.

## Examples
- Instead of: "Add feature X and feature Y" → Create two commits: `feat: add feature X`, `feat: add feature Y`.
- Instead of: "Fix bug A and bug B" → Create two commits: `fix: resolve bug A`, `fix: resolve bug B`.