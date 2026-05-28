---
name: session-management-help
description: Use this skill to display help for the session management system, including available commands and best practices.
---

## Session Management Commands

The session system helps document development work for future reference.

### Available Commands:

- `/session-start [name]` - Start a new session with an optional name.
- `/session-update [notes]` - Add notes to the current session.
- `/session-end` - End the session with a comprehensive summary.
- `/session-list` - List all session files.
- `/session-current` - Show the current session status.
- `/session-resume [filename]` - Resume a previous session.
- `/session-help` - Show this help.

### How It Works:

1. Sessions are markdown files in `.claude/sessions/`.
2. Files use the `YYYY-MM-DD-HHMM-name.md` format.
3. Only one session can be active at a time.
4. Sessions track progress, issues, solutions, and learnings.

### Best Practices:

- Start a session when beginning significant work.
- Update regularly with important changes or findings.
- End with a thorough summary for future reference.
- Review past sessions before starting similar work.

### Example Workflow:

```
/session-start refactor-auth
/session-update Added Google OAuth restriction
/session-update Fixed Next.js 15 params Promise issue
/session-end
```

### Quick Example

```bash
/skill:session:help
# Displays complete session management documentation
```