---
name: draft-commit-message
description: Draft a conventional commit message when the user asks for help writing a commit message.
metadata:
  short-description: Draft an informative commit message.
---

Draft a conventional commit message that matches the change summary provided by the user.

## Requirements
- Use the Conventional Commits format: `type(scope): summary`.
- Use the imperative mood in the summary (for example, "Feat", "Fix", "Refactor").
- The supported types are `bump`, `feat`, `fix`, `docs`, `refactor`, `test`, `ci`, `chore`, `perf`, and `revert`.
- Keep the summary under 72 characters.
- If there are breaking changes, include a `BREAKING CHANGE:` footer.
- Always use English.

## Script
- Run `.codex/skills/draft-commit-message/scripts/git-diff.sh` to show both unstaged and staged full diffs.
- Pass optional file paths or flags as args, e.g. `.codex/skills/draft-commit-message/scripts/git-diff.sh <path>`.
- Output order is unstaged diff first, then staged diff; add separators if needed.

## When to load references
- Detailed technical reference: `.codex/skills/draft-commit-message/references/REFERENCE.md`.
