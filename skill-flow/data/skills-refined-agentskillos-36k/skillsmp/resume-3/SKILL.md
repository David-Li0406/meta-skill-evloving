---
name: resume
description: Resume a previous development session
argument-hint: <filename>
allowed-tools: Bash, Read, Write
---

## Quick Example

```bash
/skill:session:resume 2026-01-25-1100-prolog-lab-setup
# Output:
# Resuming: 2026-01-25-1100-prolog-lab-setup
# Start Time: 2026-01-25 11:00:00
# Elapsed: 42h 52m
# Last Update: Configured Neovim LSP for Prolog
```

## Current Context

**Current Time**: !`date '+%Y-%m-%d %H:%M:%S'`
**Active Session**: !`cat .claude/sessions/.current-session 2>/dev/null || echo "None"`
**Available Sessions**: !`ls -1 .claude/sessions/*.md 2>/dev/null | wc -l || echo "0"` sessions

---

Resume a previous development session by:

1. Check if $ARGUMENTS contains a session filename
2. If no filename provided, list available sessions and ask user to specify one
3. Verify the session file exists in `.claude/sessions/`
4. If session file exists:
   - Display the session filename and title
   - Show the session overview (start time, initial goals)
   - Calculate and show elapsed time since session started
   - Show last few updates from the session file
   - Update `.claude/sessions/.current-session` to contain this filename
   - Confirm the session has been resumed
5. If session file doesn't exist, show error and list available sessions

Present the information in a clear, concise format.
