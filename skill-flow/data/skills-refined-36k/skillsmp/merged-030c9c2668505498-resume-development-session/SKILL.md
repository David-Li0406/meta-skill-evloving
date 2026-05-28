---
name: resume-development-session
description: Use this skill to resume a previous development session by specifying a session filename.
---

## Quick Example

```bash
/skill:session:resume <filename>
# Output:
# Resuming: <filename>
# Start Time: <start_time>
# Elapsed: <elapsed_time>
# Last Update: <last_update>
```

## Current Context

**Current Time**: !`date '+%Y-%m-%d %H:%M:%S'`
**Active Session**: !`cat .claude/sessions/.current-session 2>/dev/null || echo "None"`
**Available Sessions**: !`ls -1 .claude/sessions/*.md 2>/dev/null | wc -l || echo "0"` sessions

---

Resume a previous development session by:

1. Check if `$ARGUMENTS` contains a session filename.
2. If no filename is provided, list available sessions and ask the user to specify one.
3. Verify the session file exists in `.claude/sessions/`.
4. If the session file exists:
   - Display the session filename and title.
   - Show the session overview (start time, initial goals).
   - Calculate and show elapsed time since the session started.
   - Show last few updates from the session file.
   - Update `.claude/sessions/.current-session` to contain this filename.
   - Confirm the session has been resumed.
5. If the session file doesn't exist, show an error and list available sessions.

Present the information in a clear, concise format.