# tmux-resurrect

Manual save/restore of tmux sessions. Foundation for continuum.

## What It Does

- Save entire tmux environment to disk
- Restore after reboot/crash
- Preserves: sessions, windows, panes, working directories
- Optionally restores: running processes, vim/neovim sessions

## Installation (with tpm-redux)

```bash
# In .tmux.conf
set -g @plugin 'tmux-plugins/tmux-resurrect'
```

Then: `prefix + I` to install.

## Usage

| Keybinding | Action |
|------------|--------|
| `prefix + Ctrl-s` | Save state |
| `prefix + Ctrl-r` | Restore state |

## What Gets Restored

| Restored | Not Restored (by default) |
|----------|---------------------------|
| Sessions (names) | Running processes |
| Windows (names, layout) | Scrollback/history |
| Panes (positions) | Environment variables |
| Working directories | |

## Process Restoration

To restore specific processes:

```bash
set -g @resurrect-processes 'vim nvim "npm run dev" "pnpm dev" postgres'
```

Commands must match exactly. Quoted strings for commands with spaces.

## Vim/Neovim Session Restoration

```bash
# Restore vim sessions (requires vim-obsession or similar)
set -g @resurrect-strategy-vim 'session'
set -g @resurrect-strategy-nvim 'session'
```

## State Location

Default: `~/.tmux/resurrect/`
With XDG: `~/.config/tmux/resurrect/`

Custom:
```bash
set -g @resurrect-dir '~/.config/tmux/resurrect'
```

Files:
- `last` → symlink to most recent
- `tmux_resurrect_YYYYMMDDTHHMMSS.txt` → timestamped saves

## Standalone vs With Continuum

| Mode | Save | Restore |
|------|------|---------|
| Resurrect only | Manual (`prefix + Ctrl-s`) | Manual (`prefix + Ctrl-r`) |
| With Continuum | Auto every 15 min | Auto on tmux start |

## Sources

- [tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect)
