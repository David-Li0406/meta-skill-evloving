# tmux-continuum

Automatic session persistence. Extends [tmux-resurrect](./plugin-resurrect.md) with auto-save and auto-restore.

## What It Does

```
tmux server starts → auto-restore from disk
        ↓
Every 15 min → auto-save state
        ↓
Reboot → tmux starts → auto-restore → back where you were
```

## Installation (with tpm-redux)

```bash
# In .tmux.conf (resurrect is required)
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'

# Enable auto-restore
set -g @continuum-restore 'on'
```

Then: `prefix + I` to install.

## Configuration

```bash
# Auto-restore when tmux starts (recommended)
set -g @continuum-restore 'on'

# Save interval in minutes (default: 15)
set -g @continuum-save-interval '15'
```

## What Gets Restored

See [resurrect reference](./plugin-resurrect.md) for details on:
- What's restored by default
- Process restoration config
- Vim/neovim session restoration

## Manual Controls

Still available from resurrect:

| Keybinding | Action |
|------------|--------|
| `prefix + Ctrl-s` | Save now |
| `prefix + Ctrl-r` | Restore now |

## Troubleshooting

**Sessions not restoring on start?**
1. Check `@continuum-restore` is `'on'`
2. Check state files exist: `ls ~/.config/tmux/resurrect/`
3. Try manual restore: `prefix + Ctrl-r`

**Save interval not working?**
- Continuum saves in background; check `~/.config/tmux/resurrect/last` timestamp

## Sources

- [tmux-continuum](https://github.com/tmux-plugins/tmux-continuum)
