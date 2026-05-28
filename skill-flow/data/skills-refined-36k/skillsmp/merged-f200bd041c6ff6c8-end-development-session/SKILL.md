---
name: end-development-session
description: Use this skill to end the current development session and document a comprehensive summary of the work completed.
---

## Session End Context

**End Time**: !`date '+%Y-%m-%d %H:%M:%S'`  
**Active Session**: !`cat .claude/sessions/.current-session 2>/dev/null || echo "None"`  
**Final Git Status**: !`git status --short 2>/dev/null || echo "Not in git repo"`  
**TODO Summary**: !`cat TODO.md 2>/dev/null || echo "No TODO.md"`  

---

End the current development session by following these steps:

1. Check `.claude/sessions/.current-session` for the active session.
2. If no active session exists, inform the user that there's nothing to end.
3. If a session exists, append a comprehensive summary including:
   - Session duration
   - Git summary:
     * Total files changed (added/modified/deleted)
     * List all changed files with change type
     * Number of commits made (if any)
     * Final git status
   - TODO summary:
     * Total tasks completed/remaining
     * List all completed tasks
     * List any incomplete tasks with status
   - Key accomplishments
   - All features implemented
   - Problems encountered and solutions
   - Breaking changes or important findings
   - Dependencies added/removed
   - Configuration changes
   - Deployment steps taken
   - Lessons learned
   - What wasn't completed
   - Tips for future developers
4. Clear the contents of the `.claude/sessions/.current-session` file (do not remove it).
5. Inform the user that the session has been documented.

The summary should be thorough enough that another developer (or AI) can understand everything that happened without reading the entire session.

## Quick Example

```bash
/skill:end-development-session
# Output:
# Session: 2026-01-27-1430-fyp-interim-report
# Duration: 2h 45m
# Git changes: 3 files, 2 commits
# Tasks completed: 6/8
# Session archived
```