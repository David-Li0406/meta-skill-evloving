---
name: list-development-sessions
description: Use this skill to list all development sessions and highlight the currently active session.
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

Present the output in a clean, readable format.

## Quick Example

```bash
/skill:session:list
# Output:
# Sessions Directory: .claude/sessions/
# Total Sessions: 12
# Active: 2026-01-27-1430-fyp-interim-report
#
# Recent sessions:
# - 2026-01-27-1430-fyp-interim-report
# - 2026-01-26-0945-ml-assignment-review
# - 2026-01-25-1100-prolog-lab-setup
```