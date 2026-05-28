---
name: coding-agent
description: Use this skill when you need to run Codex CLI, Claude Code, OpenCode, or Pi Coding Agent programmatically via a background process.
---

# Skill body

## ⚠️ PTY Mode Required!

Coding agents (Codex, Claude Code, Pi) are **interactive terminal applications** that need a pseudo-terminal (PTY) to work correctly. Without PTY, you'll get broken output, missing colors, or the agent may hang.

**Always use `pty:true`** when running coding agents:

```bash
# ✅ Correct - with PTY
bash pty:true command:"codex exec 'Your prompt'"

# ❌ Wrong - no PTY, agent may break
bash command:"codex exec 'Your prompt'"
```

### Bash Tool Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `command` | string | The shell command to run |
| `pty` | boolean | **Use for coding agents!** Allocates a pseudo-terminal for interactive CLIs |
| `workdir` | string | Working directory (agent sees only this folder's context) |
| `background` | boolean | Run in background, returns sessionId for monitoring |
| `timeout` | number | Timeout in seconds (kills process on expiry) |
| `elevated` | boolean | Run on host instead of sandbox (if allowed) |

### Process Tool Actions (for background sessions)

| Action | Description |
|--------|-------------|
| `list` | List all running/recent sessions |
| `poll` | Check if session is still running |
| `log` | Get session output (with optional offset/limit) |
| `write` | Send raw data to stdin |
| `submit` | Send data + newline (like typing and pressing Enter) |
| `send-keys` | Send key tokens or hex bytes |
| `paste` | Paste text (with optional bracketed mode) |
| `kill` | Terminate the session |

---

## Quick Start: One-Shot Tasks

For quick prompts/chats, create a temp git repo and run:

```bash
# Quick chat (Codex needs a git repo!)
SCRATCH=$(mktemp -d) && cd $SCRATCH && git init && codex exec "Your prompt here"

# Or in a real project - with PTY!
bash pty:true workdir:~/Projects/myproject command:"codex exec 'Add error handling to the API calls'"
```

**Why git init?** Codex refuses to run outside a trusted git directory. Creating a temp repo solves this for scratch work.

---

## The Pattern: workdir + background + pty

For longer tasks, use background mode with PTY:

```bash
# Start agent in target directory
```