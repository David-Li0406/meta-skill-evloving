---
name: tmux-dev
description: Manage development servers running in tmux. Use when starting, stopping, or monitoring dev servers (npm, go, python, docker, etc.). Triggers on requests like "start the dev server", "check if the server is running", "show server logs", "stop the backend", or any dev server lifecycle management.
---

# tmux-dev

Manage dev servers as windows in a single `dev` tmux session. Window names are auto-generated from directory + command.

## Commands

```bash
tmux-dev start <command>       # Start or restart (requires approval)
tmux-dev stop <name>           # Stop a window
tmux-dev status <name>         # Check running/exited
tmux-dev logs <name> [lines]   # View logs (default: 50)
tmux-dev list                  # List all with status
```

## Workflow

1. Run `tmux-dev list` to see existing servers
2. Start servers from project directory: `cd /path/to/project && tmux-dev start npm run dev`
3. Name is auto-generated: `projectdir-npm-dev`
4. Check health with `status`, view output with `logs`
5. Re-running `start` with same command restarts the server

## Output Format

**start** outputs `WINDOW_NAME: <name>` for parsing, then streams 10s of logs.

**status** outputs: `<name>: running` or `<name>: exited (code N)`

**list** outputs:
```
Dev server windows (session: dev):
  myapp-npm                      running
  backend-go                     exited (code 1)
```
