---
name: current-session-status
description: Use this skill when you need to check the current status of your active session, including time, modified files, and TODO items.
---

# Skill body

Show the current session status by:

1. Check if `.claude/sessions/.current-session` exists.
2. If no active session, inform the user and suggest starting one.
3. If an active session exists:
   - Show session name and filename.
   - Calculate and show duration since start.
   - Show last few updates.
   - Show current goals/tasks.
   - Remind the user of available commands.

## Example Output

```bash
Active Session: 2026-01-27-1430-fyp-interim-report
Current Time: 16:52:30
Files Modified: 3 files changed
TODO Status: 12 items
```

## Commands

- **Current Time**: `!date '+%H:%M:%S'`
- **Active Session**: `!cat .claude/sessions/.current-session 2>/dev/null || echo "None"`
- **Files Modified**: `!git status --short 2>/dev/null || echo "Not in git repo"`
- **TODO Status**: `!cat TODO.md 2>/dev/null | grep -E '^\- \[(x| )\]' | wc -l || echo "No TODO.md"` items