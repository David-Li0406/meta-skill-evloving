---
name: session-help
description: Show help for the session management system. Use when user asks about sessions or how to track their work.
---

# Session Management Help

The session system helps document development work for future reference.

## Available Commands

- `/session-start [name]` - Start a new session with optional name
- `/session-end` - End session with comprehensive summary
- `/session-current` - Show current session status
- `/session-list` - List all past sessions
- `/session-help` - Show this help

## How It Works

1. Sessions are markdown files in `.claude/sessions/`
2. Files use `YYYY-MM-DD-HHMM-name.md` format
3. Only one session can be active at a time
4. Progress is tracked automatically when session is active

## Goal Status

- `[ ]` - Pending
- `[~]` - In progress
- `[x]` - Completed

## Example Workflow

```bash
/session-start refactor-auth
... work on tasks ...
/session-current
... continue working ...
/session-end
```
