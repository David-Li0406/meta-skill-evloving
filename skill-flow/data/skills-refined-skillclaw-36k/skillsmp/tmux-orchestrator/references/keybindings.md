# Tmux Keybindings Reference

Custom tmux configuration from `~/nix-system/home/programs/tmux.nix`

## Prefix Key

- **Ctrl+a** - Main prefix (replaces default Ctrl+b)

## Pane Management

- `prefix + |` - Split horizontally (creates vertical divider, side-by-side panes)
- `prefix + -` - Split vertically (creates horizontal divider, stacked panes)
- `Alt + Arrow Keys` - Navigate between panes (no prefix needed)
- `prefix + Ctrl + Arrow Keys` - Resize panes (repeatable)
- `prefix + x` - Kill current pane (with confirmation)

Note: All panes open in the current path by default.

## Window Management

- `Shift + Left/Right Arrow` - Switch between windows (no prefix needed)
- `prefix + c` - Create new window (opens in current path)
- `prefix + w` - List windows
- `prefix + W` - Choose window interactively
- `prefix + X` - Kill current window (with confirmation)

## Session Management

- `prefix + S` - Choose session interactively
- `prefix + s` - Switch to last session

## Copy Mode (Vi-style)

- `prefix + [` - Enter copy mode
- `v` - Begin selection (in copy mode)
- `y` - Copy selection to clipboard via wl-copy (in copy mode)
- `r` - Toggle rectangle mode (in copy mode)

## Config & Misc

- `prefix + r` - Reload tmux config

## Shell Aliases

Available from shell configuration:

- `tm` - tmux
- `tma` - tmux attach-session -t
- `tmn` - tmux new-session -s
- `tml` - tmux list-sessions
- `tmk` - tmux kill-session -t
- `tms` - Interactive session manager (tmux-session script)
- `tmd` - Create dev session with 3-pane layout

## Plugins

The configuration includes these tmux plugins:

- **sensible** - Sensible defaults
- **yank** - Copy to system clipboard
- **resurrect** - Save/restore sessions (`prefix + Ctrl+s` to save, `prefix + Ctrl+r` to restore)
- **continuum** - Auto-save sessions every 15 minutes
- **fzf-tmux-url** - Open URLs with fzf
- **dracula** - Theme

## Configuration Details

- **Terminal**: screen-256color (xterm-256color for ghostty)
- **History**: 100,000 lines
- **Key mode**: Vi
- **Mouse**: Enabled
- **Base index**: 1 (windows and panes start at 1, not 0)
- **Escape time**: 0ms
- **Repeat time**: 1000ms
- **Auto-rename**: Disabled
- **Renumber windows**: Enabled (windows renumber when one is closed)
- **Focus events**: Enabled (for vim compatibility)
