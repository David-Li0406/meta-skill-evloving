---
name: list
description: List all development sessions
allowed-tools: Bash, Read
---

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

List all development sessions by:

1. Check if `.claude/sessions/` directory exists
2. List all `.md` files (excluding hidden files and `.current-session`)
3. For each session file:
   - Show the filename
   - Extract and show the session title
   - Show the date/time
   - Show first few lines of the overview if available
4. If `.claude/sessions/.current-session` exists, highlight which session is currently active
5. Sort by most recent first

Present in a clean, readable format.
