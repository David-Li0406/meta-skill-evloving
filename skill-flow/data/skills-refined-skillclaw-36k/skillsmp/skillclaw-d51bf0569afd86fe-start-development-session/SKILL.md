---
name: start-development-session
description: Use this skill when you want to initiate a new development session and track your progress.
---

# Skill body

Start a new development session by creating a session file in `.claude/sessions/` with the format `YYYY-MM-DD-HHMM-$ARGUMENTS.md` (or just `YYYY-MM-DD-HHMM.md` if no name is provided).

The session file should begin with:
1. **Title**: Session name and timestamp.
2. **Overview Section**: Include the start time.
3. **Goals Section**: Ask the user for goals if they are not clear.
4. **Progress Section**: An empty section ready for updates.

After creating the file, create or update `.claude/sessions/.current-session` to track the active session filename.

Confirm the session has started and remind the user they can:
- Update it with `/session-update`
- End it with `/session-end`

## Quick Example

```bash
/session:start ml-assignment-review
# Session created: 2026-01-27-0945-ml-assignment-review.md
# Active session set to: .claude/sessions/2026-01-27-0945-ml-assignment-review.md
```

## Current Project State

**Working Directory**: !`pwd`  
**Git Branch**: !`git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "Not in git repo"`  
**Git Status**: !`git status --short 2>/dev/null | head -5 || echo "No changes"`  
**Last Commit**: !`git log -1 --oneline 2>/dev/null || echo "No commits"`  

## Session Context

**Date/Time**: !`date '+%Y-%m-%d %H:%M:%S (%A)'`  
**Week Number**: !`date +%V`  
**Active Session**: !`cat .claude/sessions/.current-session 2>/dev/null || echo "None"`  

## Memory Status

**Global Memory**: !`cat ~/.claude/memory.md 2>/dev/null | head -20 || echo "No global memory"`  
**Local Memory**: !`cat .claude/memory.md 2>/dev/null | head -20 || echo "No local memory"`