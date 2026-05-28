---
name: hyprland
description: "Hyprland automation with hyprctl: create/close named workspaces, open a standard 3-window dev layout (Codex + shell + Neovim) for a project, and manage windows via hyprctl dispatch. Use when asked to manipulate Hyprland workspaces or windows, or to script Hyprland layouts."
---

# Hyprland

## Quick start

- Create workspace: `scripts/hypr-ws-create.sh <name>`
- Close workspace(s): `scripts/hypr-ws-close.sh <name> [name...]`
- Open project layout: `scripts/hypr-ws-open-project.sh [project|path]`
- Open custom terminals: `scripts/hypr-ws-open-terms.sh <workspace> <dir> [Title::Command]...`
- Get instance signature: `scripts/hypr-instance.sh [--all]`
- Focus window by rule: `scripts/hypr-win-focus.sh --class REGEX --title REGEX`
- Move active window: `scripts/hypr-win-move.sh <workspace> [--follow]`
- Float & center: `scripts/hypr-win-float.sh --size 1300x800 --center`
- Resize active window: `scripts/hypr-win-resize.sh --exact 1300 800`
- Pick window (wofi): `scripts/hypr-win-pick.sh`
- List windows: `scripts/hypr-list-clients.sh`

## Workspace tasks

### Create a named workspace

Run `scripts/hypr-ws-create.sh <name>`.

### Close/delete a workspace

Run `scripts/hypr-ws-close.sh <name> [name...]`.

Behavior:
- Closes windows by address, then `killactive`, then SIGTERM/SIGKILL if needed.
- Switches to `HYPR_WS_FALLBACK` (default `1`) unless set to `none`.
- Removes workspace names from `~/.cache/hypr-launcher/workspaces.txt` if present.

### Open a 3-window dev layout

Run `scripts/hypr-ws-open-project.sh [project|path]`.

Defaults:
- Project roots: `~/Code/self` and `~/Code/rcrai`.
- Workspace name: repo basename.
- Term: `ghostty`.
- Codex args: `--dangerously-bypass-approvals-and-sandbox`.

Project resolution:
- `self/foo` -> `~/Code/self/foo`
- `rcrai/foo` -> `~/Code/rcrai/foo`
- `foo` -> search under both roots
- `/abs/path` -> use as-is

Env overrides:
- `HYPR_PROJECT_ROOTS` (colon-separated roots)
- `HYPR_WORKSPACE_NAME`
- `HYPR_WORKSPACE_TERM`
- `HYPR_WORKSPACE_NVIM_CMD`
- `HYPR_WORKSPACE_CODEX_BIN`
- `HYPR_WORKSPACE_CODEX_CMD`
- `HYPR_WORKSPACE_CODEX_ARGS`
- `HYPR_WORKSPACE_SHELL`
- `HYPR_WORKSPACE_SHELL_ARGS`
- `HYPR_WORKSPACE_PATH_PREFIX`

### Open custom terminal layout

Run `scripts/hypr-ws-open-terms.sh <workspace> <dir> [Title::Command]...`.

Examples:
- `scripts/hypr-ws-open-terms.sh notes ~/notes "Nvim::nvim" "Shell::zsh"`
- `HYPR_WS_TERMS="Codex::codex --dangerously-bypass-approvals-and-sandbox|Shell::zsh|Nvim::nvim" scripts/hypr-ws-open-terms.sh dev ~/Code/self/mobius`

Env overrides:
- `HYPR_WS_TERM`
- `HYPR_WS_SHELL`
- `HYPR_WS_SHELL_ARGS`
- `HYPR_WS_PATH_PREFIX`
- `HYPR_WS_TERMS`

## Window management

Use `hyprctl dispatch` for ad-hoc window actions. Add new scripts under `scripts/` when the action is repeatable.

Examples:
- Focus: `hyprctl dispatch focuswindow address:<addr>`
- Move: `hyprctl dispatch movetoworkspace name:<ws>`
- Resize: `hyprctl dispatch resizeactive exact 1300 800`

### Focus a window by rule

Run `scripts/hypr-win-focus.sh --class REGEX --title REGEX [--workspace NAME] [--icase] [--exec CMD]`.

### Move active window to workspace

Run `scripts/hypr-win-move.sh <workspace> [--follow]`.

### Toggle floating with size/center

Run `scripts/hypr-win-float.sh [--size WxH] [--center]`.

### Resize active window

Run `scripts/hypr-win-resize.sh --exact <width> <height>` or `--delta <dx> <dy>`.

### Center active window

Run `scripts/hypr-win-center.sh`.

### Pick a window (wofi)

Run `scripts/hypr-win-pick.sh` to select and focus.

### List clients

Run `scripts/hypr-list-clients.sh` to list `address`, `workspace`, `class`, `title`.
