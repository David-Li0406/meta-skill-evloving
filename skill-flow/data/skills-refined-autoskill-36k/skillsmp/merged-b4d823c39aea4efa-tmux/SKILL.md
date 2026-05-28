---
name: tmux
description: "Use this skill to remotely control tmux sessions for interactive CLIs (Python, gdb, etc.) by sending keystrokes and capturing pane output."
---

# tmux Skill

Use tmux as a programmable terminal multiplexer for interactive work. This skill is useful for running interactive REPLs, debugging applications, and automating terminal workflows.

## Core Concepts

- **Socket**: Use a private socket to avoid conflicts with personal tmux sessions. Default path: `${TMPDIR:-/tmp}/claude-tmux-sockets/claude.sock`.
- **Session Naming**: Use unique names for sessions to avoid conflicts.
- **Session States**: `running`, `idle`, `exited`.
- **Persistence**: Session information can be stored in a JSON file for tracking.

## Quickstart

1. **Create a Session**:
   ```bash
   SOCKET_DIR=${TMPDIR:-/tmp}/claude-tmux-sockets
   mkdir -p "$SOCKET_DIR"
   SOCKET="$SOCKET_DIR/claude.sock"
   SESSION=claude-python
   tmux -S "$SOCKET" new -d -s "$SESSION" -n shell
   ```

2. **Send Commands**:
   ```bash
   tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- 'python3 -q' Enter
   ```

3. **Capture Output**:
   ```bash
   tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200
   ```

4. **Monitor the Session**:
   After starting a session, always inform the user how to monitor it:
   ```
   To monitor this session yourself:
     tmux -S "$SOCKET" attach -t $SESSION
   ```

5. **Cleanup**:
   ```bash
   tmux -S "$SOCKET" kill-session -t "$SESSION"
   ```

## Sending Input Safely

Use the following command to send keystrokes safely:
```bash
tmux -S "$SOCKET" send-keys -t "$SESSION" -l -- "command" Enter
```
- Use `-l` for literal mode to avoid shell expansion issues.

## Watching Output

To capture recent history:
```bash
tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200
```

For continuous monitoring, consider using a helper script to poll for output.

## Synchronizing / Waiting for Prompts

Use timed polling to wait for specific prompts:
```bash
./scripts/wait-for-text.sh -s $SESSION -p '^>>>' -T 15
```

## Interactive Tool Recipes

- **Python REPL**: Start with `PYTHON_BASIC_REPL=1` to avoid issues with the interactive shell.
- **gdb**: Use `tmux ... send-keys -- 'gdb --quiet ./a.out' Enter` and manage breakpoints as needed.

## Cleanup

To clean up sessions:
```bash
tmux -S "$SOCKET" kill-session -t "$SESSION"
```
Or remove all sessions on a socket:
```bash
tmux -S "$SOCKET" list-sessions -F '#{session_name}' | xargs -r -n1 tmux -S "$SOCKET" kill-session -t
```

## Helper Scripts

### wait-for-text.sh
Polls a pane for a regex (or fixed string) with a timeout.

### find-sessions.sh
Lists tmux sessions, optionally filtered.

### safe-send.sh
Sends commands to tmux panes with automatic retries and readiness checks.

## Best Practices

- Always check for existing sessions before creating a new one to avoid conflicts.
- Use descriptive session names for clarity.
- Regularly clean up dead sessions to maintain a tidy environment.

## Troubleshooting

If you encounter issues:
- Verify session health with `./scripts/pane-health.sh`.
- Check for existing sessions with `./scripts/list-sessions.sh`.
- Ensure the tmux server is running and accessible.

This skill provides a robust framework for managing interactive terminal sessions using tmux, enhancing productivity and efficiency in terminal-based workflows.