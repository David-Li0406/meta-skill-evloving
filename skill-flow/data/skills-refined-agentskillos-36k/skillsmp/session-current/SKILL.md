---
name: session-current
description: Show the current active session status including goals and recent progress.
---

# Show current session status

## Steps

1. Check if `.claude/sessions/.current-session` exists
2. If no: Inform user no session is active and suggest `/session-start`
3. If yes: Read the session file and display status

## Display format

```text
Session: [name]
Started: YYYY-MM-DD HH:MM
Status: In Progress

Goals:
- [x] Completed goal
- [~] In progress goal
- [ ] Pending goal

Recent Progress:
- HH:MM - Latest update
- HH:MM - Previous update
```
