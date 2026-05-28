---
name: git-commit-message
description:
  Generates descriptive commit messages by analyzing git diffs. Use when the
  user asks for help writing commit messages or reviewing staged changes.
---

# Commit Messages

- Imperative mood, concise, clear, descriptive
- Title: ≤70 chars (including type, scope, parens, colon, spaces)
- Multi-change: bulleted description, lines ≤72 chars
- Standard markdown only, no special characters
- Never include: co-authors, sign-offs, AI attribution
- Never use `git log` to infer style from history

## Formats

**Standard:**

```
title

description...
```

**Conventional:**

```
type(scope): subject

description...
```

Conventional rules:

- Infer type from changes; if unclear → ask
- Scope: user-provided, ticket ID (`[A-Z]{3}-[0-9]+`), or branch name (not
  main/master)
- If scope unavailable → ask

## Workflow

1. Check staged files; if none → ask to stage all modified
2. Use `git add .` (not individual files)
3. Generate message per format above
4. Display full message in chat (triple backticks)
5. Request user approval before committing
