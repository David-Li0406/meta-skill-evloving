---
name: tmux
description: Terminal orchestration via tmux. Use for long-running processes, server management, parallel terminal sessions, and background task monitoring.
---

# Tmux Skill

## When to Load This Skill

- Running long-running processes (servers, watchers)
- Managing multiple terminal sessions
- Background task execution
- Parallel command execution
- Process monitoring

---

## Session Management

### Create Named Session

```bash
# Create new session
tmux new-session -d -s "omo-dev"

# Run command in session
tmux send-keys -t "omo-dev" "npm run dev" Enter
```

### List Sessions

```bash
tmux list-sessions
```

### Attach to Session

```bash
tmux attach -t "omo-dev"
```

### Kill Session

```bash
tmux kill-session -t "omo-dev"
```

---

## Session Naming Convention

Use `omo-{purpose}` pattern for OpenCode-managed sessions:

| Session | Purpose |
|---------|---------|
| `omo-dev` | Development server |
| `omo-test` | Test watcher |
| `omo-build` | Build process |
| `omo-db` | Database |
| `omo-logs` | Log tailing |

---

## Common Workflows

### Start Development Server

```bash
# Kill existing if any
tmux kill-session -t "omo-dev" 2>/dev/null || true

# Create fresh session
tmux new-session -d -s "omo-dev"
tmux send-keys -t "omo-dev" "cd /path/to/project && npm run dev" Enter
```

### Check Server Output

```bash
# Capture last 50 lines
tmux capture-pane -t "omo-dev" -p -S -50
```

### Run Parallel Tasks

```bash
# Create session with multiple windows
tmux new-session -d -s "omo-work"
tmux send-keys -t "omo-work" "npm run typecheck" Enter

tmux new-window -t "omo-work"
tmux send-keys -t "omo-work" "npm run lint" Enter

tmux new-window -t "omo-work"
tmux send-keys -t "omo-work" "npm run test" Enter
```

### Monitor Background Process

```bash
# Send command
tmux send-keys -t "omo-build" "npm run build" Enter

# Wait and check output
sleep 5
tmux capture-pane -t "omo-build" -p -S -20
```

---

## Window & Pane Management

### Create Windows

```bash
# New window in session
tmux new-window -t "omo-dev"

# New window with name
tmux new-window -t "omo-dev" -n "logs"
```

### Split Panes

```bash
# Horizontal split
tmux split-window -h -t "omo-dev"

# Vertical split
tmux split-window -v -t "omo-dev"
```

### Send Keys to Pane

```bash
# Send to specific pane
tmux send-keys -t "omo-dev:0.1" "tail -f logs.txt" Enter
```

---

## Process Control

### Send Interrupt (Ctrl+C)

```bash
tmux send-keys -t "omo-dev" C-c
```

### Send EOF (Ctrl+D)

```bash
tmux send-keys -t "omo-dev" C-d
```

### Kill Pane

```bash
tmux kill-pane -t "omo-dev:0.1"
```

---

## Best Practices

1. **Always use named sessions** with `omo-` prefix
2. **Check if session exists** before creating
3. **Capture output** for verification evidence
4. **Clean up sessions** when done
5. **Use separate sessions** for unrelated tasks

---

## Integration with OpenCode

```bash
# Start server in background
tmux new-session -d -s "omo-server" "npm run dev"

# Verify it started
sleep 3
OUTPUT=$(tmux capture-pane -t "omo-server" -p -S -10)
echo "$OUTPUT" | grep -q "Server started" && echo "✅ Server running"

# When done
tmux kill-session -t "omo-server"
```
