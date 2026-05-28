---
name: using-tmux-for-interactive-commands
description: Use this skill when you need to run interactive CLI tools (like vim, git rebase -i, or REPLs) that require real-time input/output, leveraging tmux for detached session control.
---

# Using tmux for Interactive Commands

## Overview

Interactive CLI tools (vim, interactive git rebase, REPLs, etc.) cannot be controlled through standard bash because they require a real terminal. tmux provides detached sessions that can be controlled programmatically via `send-keys` and `capture-pane`.

## When to Use

**Use tmux when:**
- Running vim, nano, or other text editors programmatically
- Controlling interactive REPLs (Python, Node, etc.)
- Handling interactive git commands (`git rebase -i`, `git add -p`)
- Working with full-screen terminal apps (htop, etc.)
- Commands that require terminal control codes or readline

**Don't use for:**
- Simple non-interactive commands (use regular Bash tool)
- Commands that accept input via stdin redirection
- One-shot commands that don't need interaction

## Quick Reference

| Task | Command |
|------|---------|
| Start session | `tmux new-session -d -s <name> <command>` |
| Send input | `tmux send-keys -t <name> 'text' Enter` |
| Capture output | `tmux capture-pane -t <name> -p` |
| Stop session | `tmux kill-session -t <name>` |
| List sessions | `tmux list-sessions` |

## Core Pattern

### Before (Won't Work)
```bash
# This hangs because vim expects interactive terminal
bash -c "vim file.txt"
```

### After (Works)
```bash
# Create detached tmux session
tmux new-session -d -s edit_session vim file.txt

# Send commands (Enter, Escape are tmux key names)
tmux send-keys -t edit_session 'i' 'Hello World' Escape ':wq' Enter

# Capture what's on screen
tmux capture-pane -t edit_session -p

# Clean up
tmux kill-session -t edit_session
```

## Implementation

### Basic Workflow

1. **Create detached session** with the interactive command.
2. **Wait briefly** for initialization (100-500ms depending on command).
3. **Send input** using `send-keys` (can send special keys like Enter, Escape).
4. **Capture output** using `capture-pane -p` to see current screen state.
5. **Repeat** steps 3-4 as needed.
6. **Terminate** session when done.

### Special Keys

Common tmux key names:
- `Enter` - Return/newline
- `Escape` - ESC key
- `C-c` - Ctrl+C
- `C-x` - Ctrl+X
- `Up`, `Down`, `Left`, `Right` - Arrow keys
- `Space` - Space bar
- `BSpace` - Backspace