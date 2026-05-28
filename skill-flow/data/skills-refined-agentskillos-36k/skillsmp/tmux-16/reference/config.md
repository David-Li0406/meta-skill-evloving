# Config

## Locations

tmux checks in order, use first hit:
1. `$XDG_CONFIG_HOME/tmux/tmux.conf`
2. `~/.config/tmux/tmux.conf`
3. `~/.tmux.conf`

## Directory Structure

tmux uses `~/.config/tmux/` with XDG support (3.2+):

```
~/.config/tmux/
├── tmux.conf      # config (symlink to dotfiles)
├── plugins/       # tpm installs here (local, not tracked)
└── resurrect/     # session state (local, not tracked)
```

## Sharing via Dotfiles

Symlink only the config file, not the directory:

```bash
mkdir -p ~/.config/tmux
ln -s ~/path/to/dotfiles/tmux/.tmux.conf ~/.config/tmux/tmux.conf
```

**Why not symlink the whole dir?**
- `plugins/` contains tpm-installed plugins (generated)
- `resurrect/` contains session state files (runtime)

These don't belong in version control.

## Plugin Manager (tpm-redux)

[tpm-redux](https://github.com/RyanMacG/tpm-redux) is a maintained fork of the abandoned tpm.

**Installation:**
```bash
git clone https://github.com/RyanMacG/tpm-redux ~/.config/tmux/plugins/tpm
```

**In .tmux.conf:**
```bash
# Plugin declarations
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @plugin 'omerxx/tmux-sessionx'

# Initialize tpm (keep at bottom)
run '~/.config/tmux/plugins/tpm/tpm'
```

**Commands:**
| Keybinding | Action |
|------------|--------|
| `prefix + I` | Install plugins |
| `prefix + U` | Update plugins |
| `prefix + alt + u` | Uninstall removed plugins |

## Shell Integration

Fish function for directory-based sessions (in `fish/config.fish`):

```fish
function t --description "tmux: attach/create session named after current directory"
    tmux new-session -A -s (basename $PWD)
end
```

Usage: `cd ~/projects/myapp && t` → Session: myapp

## Sources

- [Put All Tmux Config in .config/tmux](https://nickjanetakis.com/blog/put-all-of-your-tmux-configs-and-plugins-in-a-config-tmux-directory)
- [tpm - changing plugins install dir](https://github.com/tmux-plugins/tpm/blob/master/docs/changing_plugins_install_dir.md)
