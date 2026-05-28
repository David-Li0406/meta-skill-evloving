---
name: coders
description: Spawn AI coding assistants (Claude, Gemini, Codex, OpenCode) in isolated tmux sessions with git worktrees, Redis coordination, and session persistence. Use when you need to run multiple AI agents in parallel, coordinate multi-agent workflows, or isolate work in separate git branches.
allowed-tools: Bash(node:*), Bash(tmux:*)
---

# Coders - Multi-Agent Development Assistant

Spawn and manage AI coding assistants in isolated tmux sessions with optional git worktrees, Redis-based coordination, and automatic session recovery.

## Quick Start

### Spawn a new session

```bash
${CLAUDE_PLUGIN_ROOT}/bin/coders spawn claude --task "Implement OAuth authentication"
```

CLI alternative (outside Claude Code):
```bash
./bin/coders spawn claude --task "Implement OAuth authentication"
```

### With a git worktree

```bash
${CLAUDE_PLUGIN_ROOT}/bin/coders spawn claude --task "Fix login bug" --worktree fix/login-bug
```

### List active sessions

```bash
${CLAUDE_PLUGIN_ROOT}/bin/coders list
```

### Attach to a session

```bash
tmux attach -t coder-SESSION_ID
```

Press `Ctrl+B` then `D` to detach.

## Features

✨ **Multi-Agent Support**: Spawn Claude, Gemini, Codex, or OpenCode in parallel
🌲 **Git Worktrees**: Isolate work in separate branches without switching
🔄 **Session Persistence**: Save and restore sessions across reboots
📡 **Redis Coordination**: Inter-agent messaging and heartbeat monitoring
📊 **Web Dashboard**: Monitor all sessions in real-time
🎯 **Smart Naming**: Auto-generate session names from task descriptions
🔁 **Recursive Loop**: Automatically execute tasks from todolist with promise-based coordination

## Available Commands

All commands use the skill syntax:

- `/coders:spawn` - Spawn a new AI session
- `/coders:list` - List active sessions
- `/coders:loop` - Start recursive task loop from todolist
- `/coders:promises` - Check completion status of all sessions
- `/coders:attach` - Attach to a session
- `/coders:kill` - Kill a session
- `/coders:promise` - Publish completion summary (use when task is done)
- `/coders:snapshot` - Save all sessions
- `/coders:restore` - Restore saved sessions
- `/coders:orchestrator` - Start orchestrator session
- `/coders:dashboard` - Open web dashboard

## Common Workflows

### Basic Usage

```bash
# Spawn Claude for a simple task
/coders:spawn claude --task "Review the authentication code"

# Spawn Gemini for research
/coders:spawn gemini --task "Research WebSocket best practices"

# Check what's running
/coders:list
```

### Multi-Agent Development

```bash
# Start orchestrator to coordinate agents
/coders:orchestrator

# Inside orchestrator, spawn specialized agents
/coders:spawn claude --task "Implement API endpoints" --worktree backend/api
/coders:spawn gemini --task "Research API security"
/coders:spawn claude --task "Write tests" --worktree backend/tests

# Monitor everything
/coders:dashboard
```

### Spawning in Different Directories

**IMPORTANT:** By default, sessions run in your current directory. Use `--cwd` to spawn in a different project:

```bash
# Spawn in a specific project directory
/coders:spawn claude --cwd ~/Dev/flp/vega --task "Fix the API bug"

# Spawn in another project while staying in your current directory
/coders:spawn gemini --cwd ~/projects/frontend --task "Review React components"
```

### Git Worktree Isolation

```bash
# Work on multiple features in parallel
/coders:spawn claude --task "Add OAuth" --worktree feature/oauth
/coders:spawn claude --task "Build dashboard" --worktree feature/dashboard

# Each session has its own isolated git worktree
```

### Recursive Task Loop

```bash
# Automatically execute all tasks from a todolist
/coders:loop --todolist ~/project/todolist.txt --cwd ~/project

# Use opus for complex tasks
/coders:loop --todolist tasks.txt --cwd ~/project --model claude-opus-4

# Run 2 tasks in parallel
/coders:loop --todolist tasks.txt --cwd ~/project --max-concurrent 2

# Stop if any task is blocked
/coders:loop --todolist tasks.txt --cwd ~/project --stop-on-blocked

# Preview what would be executed
/coders:loop --todolist tasks.txt --cwd ~/project --dry-run
```

The loop feature:
- Parses your todolist and executes uncompleted tasks sequentially
- Monitors completion promises to know when to spawn the next task
- Automatically switches from Claude to Codex when approaching usage limits
- Marks tasks as complete in the todolist file after each success
- Runs in background while orchestrator remains interactive

### Session Persistence

```bash
# Before shutting down
/coders:snapshot

# After reboot
/coders:restore
```

## Redis Coordination

Enable Redis for inter-agent messaging and monitoring:

```bash
/coders:spawn claude --task "Build frontend" --redis redis://localhost:6379 --enable-heartbeat
```

Agents can:
- Send messages to each other via pub/sub
- Publish heartbeats for dashboard monitoring
- Resources are automatically cleaned up when sessions end

## Task Completion & Promises

**IMPORTANT**: When spawned sessions complete their tasks, they MUST publish a completion promise to notify the orchestrator and dashboard:

```bash
# When task is complete
/coders:promise "Implemented user authentication with JWT tokens"

# If blocked and can't proceed
/coders:promise "Blocked waiting for API credentials" --status blocked

# If work is done but needs review
/coders:promise "PR ready for review" --status needs-review
```

**Why this matters:**
- The orchestrator can track which sessions are done
- The dashboard shows completion status clearly
- Follow-up tasks can be spawned automatically
- Blocked tasks are visible for manual intervention

**Best practices:**
- Publish promise immediately when task is done (don't wait)
- Include specific details about what was accomplished
- If partially done, list what's complete and what's remaining
- For blocked tasks, clearly state what's needed to unblock

## Documentation

- **[API Reference](reference.md)** - Complete API documentation for programmatic usage
- **[Examples](examples.md)** - Real-world scenarios and code examples
- **Command docs** - Each command has its own detailed documentation

## Session Management

### Auto-Generated Names

Session names are automatically generated from task descriptions:

```bash
/coders:spawn claude --task "Review the Linear project"
# Creates: coder-claude-linear-project
```

### Manual Naming

```bash
/coders:spawn claude --task "Fix bug" --name my-custom-name
# Creates: coder-my-custom-name
```

### Communicating with Sessions

**Attach (recommended):**
```bash
tmux attach -t coder-SESSION_ID
# Work inside the session
# Ctrl+B then D to detach
```

**Send messages remotely:**
```bash
tmux send-keys -t coder-SESSION_ID "your message"
sleep 0.5
tmux send-keys -t coder-SESSION_ID C-m
```

**Check output:**
```bash
tmux capture-pane -t coder-SESSION_ID -p | tail -20
```

## Options Reference

### spawn command options:

- `tool` - AI tool: `claude`, `gemini`, `codex`, `opencode` (default: `claude`)
  - **Note**: Use `claude` for Claude Code (not `sonnet`, `opus`, or `haiku`)
  - Model selection is done via `--model` flag, not the tool name
- `--task` - Task description (required)
- `--name` - Custom session name (optional, auto-generated if omitted)
- `--model` - Model identifier passed to the tool CLI (optional)
- `--cwd` - Working directory for the session (default: current directory)
- `--worktree` - Git branch for worktree (optional)
- `--base-branch` - Base branch for worktree (default: `main`)
- `--prd` - PRD/spec file path to include as context (optional)
- `--redis` - Redis URL for coordination (optional)
- `--enable-heartbeat` - Enable heartbeat publishing (optional)

## Requirements

- **tmux** - Required for session management
- **Redis** - Required for coordination and heartbeat monitoring
- **git** - For worktree support (optional)
- **Node.js 18+** - Runtime

## Tips

1. **Use `--cwd` to spawn in different projects** - Sessions default to your current directory. Always specify `--cwd ~/path/to/project` when you want a session to work in a different codebase.
2. **Use the orchestrator** for complex multi-agent workflows
3. **Save snapshots regularly** to preserve session state
4. **Use worktrees** to avoid branch switching conflicts
5. **Enable Redis heartbeat** for production-like agent monitoring
6. **Use the dashboard** to monitor multiple sessions visually

## Troubleshooting

### Session not found
```bash
/coders:list  # Verify session exists
tmux list-sessions | grep coder-  # Check tmux directly
```

### Worktree already exists
```bash
git worktree list  # List worktrees
git worktree remove ../worktrees/BRANCH  # Remove stale worktree
```

### Redis connection failed
```bash
redis-server  # Start Redis
# or
docker run -d -p 6379:6379 redis:latest
```

## See Also

- [Reference](reference.md) - Full API documentation
- [Examples](examples.md) - Usage examples and patterns
