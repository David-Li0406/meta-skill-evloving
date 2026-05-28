---
name: tmux-interactive-sessions
description: Manage interactive terminal sessions using tmux. Use for REPLs, long-running processes, interactive CLIs, or commands needing persistent state.
---

# tmux Interactive Sessions

Use the loaded `mcp__tmux__*` tools for interactive terminal work.

## When to Use This

- **REPLs**: python, node, irb, psql, sqlite3
- **Long-running processes**: dev servers, watch commands, builds
- **Interactive CLIs**: htop, vim, less
- **Persistent state**: when `cd`, `source`, or `export` must persist

## Workflow

1. **find-session** first to reuse existing, else **create-session**
2. **list-panes** to get paneId
3. **execute-command** with `rawMode: true` for REPLs
4. **capture-pane** after rawMode commands to see output
5. **kill-session** when done

## Key Insight

The standard `execute-command` wraps commands with markers to detect completion. This breaks REPLs and interactive apps. Use:

- `rawMode: true` — for REPLs, interactive prompts
- `noEnter: true` — for TUI navigation (sends keystrokes only)

After either, use **capture-pane** to see results.
