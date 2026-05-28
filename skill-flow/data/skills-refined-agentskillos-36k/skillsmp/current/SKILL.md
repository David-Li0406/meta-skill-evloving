---
name: current
description: Show the current session status
allowed-tools: Bash, Read
---

## Live Project Status

**Current Time**: !`date '+%H:%M:%S'`
**Active Session**: !`cat .claude/sessions/.current-session 2>/dev/null || echo "None"`
**Files Modified**: !`git status --short 2>/dev/null || echo "Not in git repo"`
**TODO Status**: !`cat TODO.md 2>/dev/null | grep -E '^\- \[(x| )\]' | wc -l || echo "No TODO.md"` items

---

Show the current session status by:

1. Check if `.claude/sessions/.current-session` exists
2. If no active session, inform user and suggest starting one
3. If active session exists:
   - Show session name and filename
   - Calculate and show duration since start
   - Show last few updates
   - Show current goals/tasks
   - Remind user of available commands

Keep the output concise and informative.
