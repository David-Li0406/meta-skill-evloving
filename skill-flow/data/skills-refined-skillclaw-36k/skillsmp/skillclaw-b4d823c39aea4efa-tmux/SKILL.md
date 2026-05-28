---
name: tmux
description: Use this skill when you need to control interactive terminal applications (like Python REPL, gdb, etc.) via tmux sessions by sending keystrokes and capturing output.
---

# tmux Skill

## Core Concepts

- **Socket**: Use a private socket to avoid conflicts with personal tmux sessions. Default path is `${TMPDIR:-/tmp}/tmux-sockets`.
- **Session Naming**: Use unique names for sessions to avoid conflicts. Format: `session-name`.
- **Session States**: Sessions can be `running`, `idle`, or `exited`.
- **Persistence**: Optionally track sessions in a JSON file for easy management.

## Quickstart

1. **Create a Socket Directory**:
   ```bash
   SOCKET_DIR=${TMPDIR:-/tmp}/tmux-sockets
   mkdir -p "$SOCKET_DIR"
   SOCKET="$SOCKET_DIR/tmux.sock"
   ```

2. **Create a New Session**:
   ```bash
   SESSION=my-session
   tmux -S "$SOCKET" new -d -s "$SESSION" -n shell
   ```

3. **Send Commands**:
   ```bash
   tmux -S "$SOCKET" send-keys -t "$SESSION" "python3 -q" Enter
   ```

4. **Capture Output**:
   ```bash
   tmux -S "$SOCKET" capture-pane -p -t "$SESSION":0.0
   ```

5. **Monitor the Session**:
   After starting a session, always print the following command for the user:
   ```bash
   echo "To monitor this session: tmux -S \"$SOCKET\" attach -t $SESSION"
   ```

6. **Cleanup**:
   ```bash
   tmux -S "$SOCKET" kill-session -t "$SESSION"
   ```

## Tips

- Use `-x` and `-y` options to set pane size for consistency.
- Always check for existing sessions to avoid name conflicts before creating a new one.
- Use helper scripts for session management, such as listing or cleaning up sessions.

## Example Usage

```bash
# Check existing sessions
./scripts/list-sessions.sh

# Create a new Python REPL session
./scripts/create-session.sh -n my-python-session --python

# Send a command to the session
./scripts/safe-send.sh -s my-python-session -c "print(2 + 2)" -w ">>>"

# Clean up dead sessions
./scripts/cleanup-sessions.sh
```