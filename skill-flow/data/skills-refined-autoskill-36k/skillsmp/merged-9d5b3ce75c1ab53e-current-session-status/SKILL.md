---
name: current-session-status
description: Use this skill to display the current active session status, including goals, recent progress, and project status.
---

## Show Current Session Status

### Steps

1. Check if `.claude/sessions/.current-session` exists.
2. If no active session exists, inform the user and suggest starting one with `/session-start`.
3. If an active session exists:
   - Read the session file and display the session name and filename.
   - Calculate and show the duration since the session started.
   - Display the current time.
   - Show the status of modified files.
   - Display the TODO status.
   - List current goals/tasks.
   - Remind the user of available commands.

### Display Format

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

Current Time: HH:MM:SS
Files Modified: [number] files changed
TODO Status: [number] items
```

### Example Output

```bash
/skill:session:current
# Output:
# Active Session: 2026-01-27-1430-fyp-interim-report
# Current Time: 16:52:30
# Files Modified: 3 files changed
# TODO Status: 12 items
```

Keep the output concise and informative.