---
name: tmux
description: Use when managing terminal processes - starting dev servers, reading logs from other panes, sending commands to panes, or deciding between tmux pane vs CC background process. Triggers on "start server", "check logs", "run in background", "new pane", "dev server".
---

# tmux

Terminal multiplexer - persistent sessions with splits and windows.

## When to Use tmux Pane vs CC Background Process

| User Need | Use |
|-----------|-----|
| Real-time visibility of logs (dev server, build output) | tmux pane |
| Might interact with process | tmux pane |
| Just need to know when done / final result | CC background process |

**Default:** Dev servers and processes that emit logs user is developing against → **tmux pane**.

## Reading Pane Output

1. Discover pane layout: `tmux list-panes`
2. Capture with appropriate depth:
   ```bash
   tmux capture-pane -t :.1 -p -S -50  # last 50 lines from pane 1
   ```

Target format: `-t session:window.pane`
* `:.1` = current session, current window, pane 1
* `:.2` = pane 2, etc.

## Starting Processes in New Panes

See [sending-commands reference](./reference/sending-commands.md) for:
* Creating new panes and sending commands
* Starting dev servers
* send-keys patterns

## Directory-Based Sessions

Use `t` command to attach/create session named after current directory:

```bash
cd ~/projects/myapp && t   # → Session: myapp
cd ~/projects/dotfiles && t # → Session: dotfiles
```

Creates new session if none exists, attaches if it does. Use this for starting work in a project.

## Quick Reference

| Task              | Command                               |
| ----------------- | ------------------------------------- |
| Session for dir   | `t`                                   |
| List panes        | `tmux list-panes`                     |
| Capture pane      | `tmux capture-pane -t :.N -p -S -100` |
| Split vertical    | `tmux split-window -h`                |
| Send command      | `tmux send-keys -t :.N "cmd" Enter`   |
| New session       | `tmux new -s name`                    |
| List sessions     | `tmux ls`                             |
| Kill session      | `tmux kill-session -t name`           |

## Maintenance

Sessions accumulate. Periodically clean up:

```bash
tmux ls                        # see all sessions
tmux kill-session -t old-proj  # kill one
tmux kill-server               # kill all
```

## References

* [Config](./reference/config.md) - locations, tpm-redux, dotfiles setup
* [Sending Commands](./reference/sending-commands.md) - send-keys, new panes, starting servers
* [Landscape](./reference/landscape.md) - plugins, ecosystem, setup recommendations

**Plugins:**
* [Resurrect](./reference/plugin-resurrect.md) - manual save/restore sessions
* [Continuum](./reference/plugin-continuum.md) - auto save/restore (extends resurrect)
* [Sessionx](./reference/plugin-sessionx.md) - fuzzy session picker, worktree workflows

**Integrations:**
* [Zed](./reference/integration-zed.md) - auto-attach to project sessions
* [Ghostty](./reference/integration-ghostty.md) - manual attach workflows
