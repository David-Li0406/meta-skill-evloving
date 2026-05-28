---
name: nclaude-chat
description: Communicate with other Claude Code sessions via nclaude. Use when coordinating multi-agent tasks, sharing progress updates, requesting help from other sessions, or collaborating on parallel work.
allowed-tools: Bash, Read
---

# NClaude Chat Skill

Use this skill to send and receive messages between Claude Code sessions.

## When to Use
- Coordinating work across multiple Claude sessions
- Sharing progress updates with other agents
- Requesting information or assistance from another session
- Announcing task completion or blockers

## Commands

### Send a message
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/nclaude.py send "SESSION_ID" "Your message here"
```

### Read new messages
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/nclaude.py read "SESSION_ID"
```

### Read all messages (including previously read)
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/nclaude.py read "SESSION_ID" --all
```

### Check chat status
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/nclaude.py status
```

## Session ID
Use a descriptive session ID that identifies your role:
- `claude-frontend` - Working on frontend code
- `claude-backend` - Working on backend/API
- `claude-tests` - Running tests
- `claude-review` - Code review agent

Or use the `NCLAUDE_ID` environment variable if set.

## Message Format
Messages are logged as: `[TIMESTAMP] [SESSION_ID] MESSAGE`

## Example Workflow
1. Session A: `send "claude-api" "Starting API endpoint implementation for /users"`
2. Session B: `read "claude-frontend"` to see the message
3. Session B: `send "claude-frontend" "API ready at /api/users, please integrate"`
4. Session A: `read "claude-api"` to see the reply
