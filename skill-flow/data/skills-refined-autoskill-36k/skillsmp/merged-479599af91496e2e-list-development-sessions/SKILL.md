---
name: list-development-sessions
description: Use this skill to list all development sessions in a structured format.
---

# List Development Sessions

List all development sessions by following these steps:

1. Check if the `.claude/sessions/` directory exists.
2. List all `.md` files (excluding hidden files and `.current-session`).
3. For each session file:
   - Show the filename.
   - Extract and show the session title.
   - Show the date/time.
   - Show the first few lines of the overview if available.
4. If `.claude/sessions/.current-session` exists, highlight which session is currently active.
5. Sort sessions by most recent first.

## Quick Example

```bash
/skill:session:list
# Output:
# Sessions Directory: .claude/sessions/
# Total Sessions: <total_sessions>
# Active: <active_session>
#
# Recent sessions:
# - <session_1>
# - <session_2>
# - <session_3>
```

Present the information in a clean, readable format.