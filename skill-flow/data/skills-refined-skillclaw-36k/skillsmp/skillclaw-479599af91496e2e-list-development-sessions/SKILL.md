---
name: list-development-sessions
description: Use this skill when you need to list all development sessions in a readable format, including details about the active session.
---

# Skill body

List all development sessions by following these steps:

1. Check if the `.claude/sessions/` directory exists.
2. List all `.md` files in the directory, excluding hidden files and `.current-session`.
3. For each session file:
   - Show the filename.
   - Extract and display the session title.
   - Show the date/time of the session.
   - Display the first few lines of the overview if available.
4. If the `.claude/sessions/.current-session` file exists, highlight which session is currently active.
5. Sort the sessions by most recent first.

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