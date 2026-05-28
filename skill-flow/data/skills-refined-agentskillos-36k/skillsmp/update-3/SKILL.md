---
name: update
description: Update the current development session with progress notes
argument-hint: [notes]
allowed-tools: Bash, Read, Write
disable-model-invocation: true
---

## Update Context

**Timestamp**: !`date '+%Y-%m-%d %H:%M:%S'`
**Active Session**: !`cat .claude/sessions/.current-session 2>/dev/null || echo "None"`

**Git Snapshot**:
- Changes: !`git status --porcelain 2>/dev/null | wc -l || echo "0"` files
- Branch: !`git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "Not in git repo"`
- Last commit: !`git log -1 --oneline 2>/dev/null || echo "No commits"`

**TODO Progress**: !`cat TODO.md 2>/dev/null | grep -c '^\- \[x\]' || echo "0"` completed

---

Update the current development session by:

1. Check if `.claude/sessions/.current-session` exists to find the active session
2. If no active session, inform user to start one with `/session-start`
3. If session exists, append to the session file with:
   - Current timestamp
   - The update: $ARGUMENTS (or if no arguments, summarize recent activities)
   - Git status summary:
     * Files added/modified/deleted (from `git status --porcelain`)
     * Current branch and last commit
   - Todo list status:
     * Number of completed/in-progress/pending tasks
     * List any newly completed tasks
   - Any issues encountered
   - Solutions implemented
   - Code changes made

Keep updates concise but comprehensive for future reference.

Example format:
```
### Update - 2025-06-16 12:15 PM

**Summary**: Implemented user authentication

**Git Changes**:
- Modified: app/middleware.ts, lib/auth.ts
- Added: app/login/page.tsx
- Current branch: main (commit: abc123)

**Todo Progress**: 3 completed, 1 in progress, 2 pending
- ✓ Completed: Set up auth middleware
- ✓ Completed: Create login page
- ✓ Completed: Add logout functionality

**Details**: [user's update or automatic summary]
```
