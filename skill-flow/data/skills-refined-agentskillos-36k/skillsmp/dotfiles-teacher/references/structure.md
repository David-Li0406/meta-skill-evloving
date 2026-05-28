# Directory Structure

## Table of Contents

1. [Repository Layout](#repository-layout)
2. [XDG Base Directory](#xdg-base-directory)
3. [Naming Conventions](#naming-conventions)
4. [Adding New Tools](#adding-new-tools)

## Repository Layout

```
dotfiles/
├── config/              # Tool configurations (XDG_CONFIG_HOME targets)
│   ├── zsh/
│   ├── git/
│   ├── tmux/
│   └── <tool>/
├── local/
│   ├── bin/             # Setup scripts
│   ├── share/dotfiles/  # Data files (Brewfiles, package lists)
│   └── state/dotfiles/  # State/backup files
├── makefile             # Entry point for all operations
└── .zshenv              # Bootstrap (sets ZDOTDIR)
```

## XDG Base Directory

Follow [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/latest/):

| Variable | Default | Purpose |
|----------|---------|---------|
| `XDG_CONFIG_HOME` | `~/.config` | User config files |
| `XDG_DATA_HOME` | `~/.local/share` | User data files |
| `XDG_STATE_HOME` | `~/.local/state` | State/history files |
| `XDG_CACHE_HOME` | `~/.cache` | Cache files |

### Config Placement Pattern

```bash
# In link.sh
mkdir -p "$XDG_CONFIG_HOME/tool"
ln -fnsv "$DOTFILES_DIR/config/tool/config" "$XDG_CONFIG_HOME/tool/config"
```

### Non-XDG Tools

Some tools don't support XDG. Handle exceptions:

```bash
# Claude Code (XDG unsupported)
mkdir -p "$HOME/.claude"
ln -fnsv "$DOTFILES_DIR/config/claude/*" "$HOME/.claude/"

# VSCode (platform-specific)
if isRunningOnMac; then
    VSCODE_DIR="$HOME/Library/Application Support/Code/User"
else
    VSCODE_DIR="$HOME/.vscode"
fi
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Config dir | Lowercase, hyphen-separated | `config/my-tool/` |
| Main config | Match tool's expected name | `config`, `settings.json` |
| Local template | `.local.template` suffix | `config.local.template` |
| Scripts | Lowercase, descriptive | `init.sh`, `link.sh` |

## Adding New Tools

1. Create directory: `config/<tool-name>/`
2. Add main config file
3. Create `.local.template` if sensitive values exist
4. Update `link.sh`:

```bash
# <tool-name> configuration
if [[ -f "$DOTFILES_DIR/config/<tool-name>/config" ]]; then
    mkdir -p "$XDG_CONFIG_HOME/<tool-name>"
    ln -fnsv "$DOTFILES_DIR/config/<tool-name>/config" "$XDG_CONFIG_HOME/<tool-name>/config"
fi
```

5. Test: `make link && make verify`
