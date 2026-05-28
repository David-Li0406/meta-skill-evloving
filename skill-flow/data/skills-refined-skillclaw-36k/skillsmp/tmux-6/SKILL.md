---
name: tmux
description: Use tmux to run interactive or long-running commands (e.g., SSH) when Codex must read stdout/stderr without a live TTY. Use when users mention tmux or need persistent terminal output. Forbid tmux windows; use a single window with panes only.
---

# Tmux (No Windows)

**No TTY:** Never attach or type directly in tmux. Always interact via `send-keys` and read output with `capture-pane`.

## Policy

- Use tmux only when a command is interactive or long-running and Codex must read stdout/stderr (e.g., SSH, REPLs, tailing logs).
- Always create a new session for a task; prefer a unique name like `codex-<task>` or `codex-<timestamp>`.
- Never create or switch windows (`new-window`, `select-window`, `kill-window`, `rename-window`).
- Use panes only within the single default window.
- Interact via tmux CLI commands (`send-keys`, `capture-pane`, `select-pane`).
- Use tmux key sequences via `send-keys` (e.g., `C-c`, `C-m`) instead of typing them in a TTY.

## Core workflow

1. Create a session:
   - `tmux new-session -d -s <name>`
   - If unsure whether it exists, use `tmux has-session -t <name>`.

2. Run a command in the first pane:
   - `tmux send-keys -t <name>:0.0 "<command>" C-m`

3. Read output (stdout/stderr):
   - `tmux capture-pane -pt <name>:0.0 -S -200` (adjust `-S` for more scrollback)

4. Interact further:
   - `tmux send-keys -t <name>:0.0 "<input>" C-m`

## Working with panes

- Split vertically:
  - `tmux split-window -v -t <name>:0.0`
- Split horizontally:
  - `tmux split-window -h -t <name>:0.0`
- Select a pane:
  - `tmux select-pane -t <name>:0.<pane>`
- Run a command in a pane:
  - `tmux send-keys -t <name>:0.<pane> "<command>" C-m`
- Capture output from a pane:
  - `tmux capture-pane -pt <name>:0.<pane> -S -200`

## SSH example

- `tmux new-session -d -s codex-ssh`
- `tmux send-keys -t codex-ssh:0.0 "ssh user@host" C-m`
- `tmux capture-pane -pt codex-ssh:0.0 -S -200`

## Cleanup

- Kill the session when done:
  - `tmux kill-session -t <name>`

## CLI tips (no TTY)

- Check if a session exists:
  - `tmux has-session -t <name>`
- List sessions/panes:
  - `tmux list-sessions`
  - `tmux list-panes -t <name>`
- Stop a running command:
  - `tmux send-keys -t <name>:0.<pane> C-c`
- Send literal text (avoid shell expansion surprises):
  - `tmux send-keys -t <name>:0.<pane> -l \"literal text\"`
- Capture full scrollback when debugging:
  - `tmux capture-pane -pt <name>:0.<pane> -S -`
- Do not use `tmux attach`; rely on CLI commands only.
