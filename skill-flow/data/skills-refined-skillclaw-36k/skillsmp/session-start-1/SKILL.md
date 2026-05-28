---
name: session-start
description: Start a new development session to track work progress. Use when user wants to begin tracking their work, or suggest at conversation start when no active session exists.
argument-hint: "[session-name]"
---

# Start a new development session

## Before starting

Check if `.claude/sessions/.current-session` already exists. If yes, inform user a session is already active.

## Session creation

Create a session file in `.claude/sessions/` with format `YYYY-MM-DD-HHMM-$ARGUMENTS.md` (or `YYYY-MM-DD-HHMM.md` if no name provided).

The session file should contain:

```markdown
# Session: [name] - YYYY-MM-DD HH:MM

## Overview

- **Started**: YYYY-MM-DD HH:MM
- **Status**: In Progress

## Goals

- [ ] Goal 1 (ask user for goals if not clear)

## Progress

## Notes
```

After creating the file, write the filename to `.claude/sessions/.current-session`.

## Confirmation

Confirm the session has started and remind user:

- Update progress: automatic (or `/session-update [notes]`)
- End session: `/session-end`
- Check status: `/session-current`
