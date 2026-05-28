---
name: resume-development-session
description: Use this skill when you want to resume a previous development session by specifying its filename.
---

# Skill body

Resume a previous development session by following these steps:

1. Check if the argument contains a session filename.
2. If no filename is provided, list available sessions and prompt the user to specify one.
3. Verify that the session file exists in the `.claude/sessions/` directory.
4. If the session file exists:
   - Display the session filename and title.
   - Show the session overview, including start time and initial goals.
   - Calculate and display the elapsed time since the session started.
   - Show the last few updates from the session file.
   - Update `.claude/sessions/.current-session` to contain this filename.
   - Confirm that the session has been resumed.
5. If the session file does not exist, display an error message and list available sessions.

Present the information in a clear, concise format.