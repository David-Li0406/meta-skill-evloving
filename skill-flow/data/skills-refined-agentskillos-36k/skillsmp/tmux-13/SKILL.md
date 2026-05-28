---
name: tmux
description: Manage tmux sessions, windows, and panes for terminal multiplexing. Use when running long processes, managing multiple terminals, or executing commands in background sessions.
compatibility: opencode
metadata:
  workflow: terminal
---

## What I do

- Create and manage tmux sessions for background processes
- Execute commands in persistent terminal sessions
- Capture output from running processes
- Manage parallel terminal workspaces

## When to use me

Use this when running long-running processes, managing multiple terminals, or executing commands that need to persist beyond the current session.

## Session Management

### Check Existing Sessions First

Always check before creating new sessions:

```bash
tmux list-sessions 2>/dev/null || echo "No sessions"
```

### Create or Attach

```bash
# Create new session
tmux new-session -d -s "session-name"

# Attach to existing
tmux attach-session -t "session-name"

# Create if not exists, attach if exists
tmux new-session -A -s "session-name"
```

## Executing Commands

### Run Command in Session

```bash
# Send command to session
tmux send-keys -t "session-name" "your-command" Enter

# Send to specific window
tmux send-keys -t "session-name:window-name" "command" Enter

# Send to specific pane
tmux send-keys -t "session-name:0.0" "command" Enter
```

### Capture Output

```bash
# Capture pane contents
tmux capture-pane -t "session-name" -p

# Capture with history (last 1000 lines)
tmux capture-pane -t "session-name" -p -S -1000
```

## Window and Pane Management

```bash
# New window in session
tmux new-window -t "session-name" -n "window-name"

# Split pane horizontally
tmux split-window -h -t "session-name"

# Split pane vertically
tmux split-window -v -t "session-name"

# List windows
tmux list-windows -t "session-name"

# List panes
tmux list-panes -t "session-name"
```

## Common Patterns

### Background Process

```bash
# Start process in background session
tmux new-session -d -s "build" && \
tmux send-keys -t "build" "npm run build" Enter
```

### Check Process Status

```bash
# Capture output to see if process completed
tmux capture-pane -t "build" -p | tail -20
```

### Cleanup

```bash
# Kill specific session
tmux kill-session -t "session-name"

# Kill all sessions
tmux kill-server
```

## Best Practices

1. **Name sessions descriptively**: Use meaningful names like `dev`, `build`, `logs`
2. **Check before creating**: Always verify session doesn't exist first
3. **Capture output**: Use `capture-pane` to verify command results
4. **Clean up**: Kill sessions when work is complete
5. **Chain commands**: Use `&&` to ensure proper sequencing
