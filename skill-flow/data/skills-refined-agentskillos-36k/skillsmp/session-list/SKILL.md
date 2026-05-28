---
name: session-list
description: List all past development sessions in reverse chronological order.
---

# List all development sessions

## Steps

1. List all `.md` files in `.claude/sessions/` directory
2. Exclude `.current-session` from the list
3. Sort by filename in reverse chronological order (newest first)

## Display format

```text
Sessions:
- 2024-01-15-1430-feature-auth.md (Completed)
- 2024-01-14-0900-bugfix-login.md (Completed)
- 2024-01-13-1600-refactor-api.md (Completed)
```

If no sessions exist, inform user and suggest `/session-start`.
