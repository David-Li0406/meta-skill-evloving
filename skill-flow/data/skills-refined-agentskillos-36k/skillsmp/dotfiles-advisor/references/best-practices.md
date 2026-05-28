# Dotfiles Best Practices

## Table of Contents

1. [Directory Structure](#directory-structure)
2. [XDG Base Directory](#xdg-base-directory)
3. [Symlink Management](#symlink-management)
4. [Shell Configuration](#shell-configuration)
5. [Git Configuration](#git-configuration)
6. [Automation](#automation)
7. [Cross-Platform Support](#cross-platform-support)

---

## Directory Structure

### Recommended Layout

```
dotfiles/
├── config/                  # XDG_CONFIG_HOME contents
│   ├── git/
│   │   ├── config
│   │   └── ignore
│   ├── zsh/
│   │   ├── .zshrc
│   │   ├── aliases.zsh
│   │   └── functions.zsh
│   ├── nvim/
│   │   ├── init.lua
│   │   └── lua/plugins/
│   └── tmux/
│       └── tmux.conf
├── local/
│   └── share/dotfiles/      # XDG_DATA_HOME/dotfiles
│       └── brewfiles/
├── scripts/                 # Setup/utility scripts
├── makefile                 # Automation entry point
└── .gitignore
```

### Key Patterns

- **Flat config/**: Mirror `~/.config` structure for easy symlinking
- **Tool isolation**: Each tool in its own directory
- **Scripts separate**: Keep setup scripts outside config

---

## XDG Base Directory

### Standard Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `XDG_CONFIG_HOME` | `~/.config` | User configuration |
| `XDG_DATA_HOME` | `~/.local/share` | User data |
| `XDG_STATE_HOME` | `~/.local/state` | User state (logs, history) |
| `XDG_CACHE_HOME` | `~/.cache` | Non-essential cache |

### Setting in Shell

```bash
# .zshenv or .zprofile
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
```

### Migrating Non-Compliant Tools

```bash
# Zsh
export ZDOTDIR="$XDG_CONFIG_HOME/zsh"

# Less
export LESSHISTFILE="$XDG_STATE_HOME/less/history"

# Node.js
export NODE_REPL_HISTORY="$XDG_STATE_HOME/node/repl_history"
export NPM_CONFIG_USERCONFIG="$XDG_CONFIG_HOME/npm/npmrc"

# Go
export GOPATH="$XDG_DATA_HOME/go"

# Rust
export CARGO_HOME="$XDG_DATA_HOME/cargo"
export RUSTUP_HOME="$XDG_DATA_HOME/rustup"
```

---

## Symlink Management

### GNU Stow (Recommended)

```bash
# Structure: home/.config/git/config -> ~/.config/git/config
cd dotfiles
stow -t ~ home
```

### Manual Symlinks

```bash
# Create parent directories first
mkdir -p ~/.config/git
ln -sf "$DOTFILES/config/git/config" ~/.config/git/config
```

### Makefile Pattern

```makefile
DOTFILES := $(shell pwd)

.PHONY: link
link:
	@mkdir -p ~/.config
	@for dir in $(wildcard config/*); do \
		ln -sfn "$(DOTFILES)/$$dir" ~/.config/$$(basename $$dir); \
	done
```

---

## Shell Configuration

### File Organization

```
config/zsh/
├── .zshrc           # Main entry point
├── .zshenv          # Environment variables (always loaded)
├── aliases.zsh      # Command aliases
├── functions.zsh    # Shell functions
├── path.zsh         # PATH modifications
├── completion.zsh   # Completion settings
└── plugins.zsh      # Plugin manager config
```

### Modular Loading

```bash
# .zshrc
ZDOTDIR="${XDG_CONFIG_HOME}/zsh"

for config in "$ZDOTDIR"/*.zsh; do
    [[ -f "$config" ]] && source "$config"
done

# Load local overrides
[[ -f "$ZDOTDIR/.zshrc.local" ]] && source "$ZDOTDIR/.zshrc.local"
```

### Performance Tips

```bash
# Lazy load nvm (saves ~500ms)
nvm() {
    unset -f nvm
    export NVM_DIR="$XDG_DATA_HOME/nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"
    nvm "$@"
}

# Cache completions
autoload -Uz compinit
if [[ -n ${ZDOTDIR}/.zcompdump(#qN.mh+24) ]]; then
    compinit
else
    compinit -C
fi
```

---

## Git Configuration

### Conditional Includes

```gitconfig
# ~/.config/git/config
[user]
    name = Your Name
    email = personal@example.com

[includeIf "gitdir:~/Code/work/"]
    path = ~/.config/git/config.work

[include]
    path = ~/.config/git/config.local
```

### Recommended Defaults

```gitconfig
[init]
    defaultBranch = main

[pull]
    rebase = true

[rebase]
    autoStash = true

[rerere]
    enabled = true

[diff]
    algorithm = histogram

[merge]
    conflictStyle = zdiff3
```

### Global Gitignore

```gitignore
# ~/.config/git/ignore
.DS_Store
*.swp
*.swo
.idea/
.vscode/
*.local
.env.local
```

---

## Automation

### Makefile Structure

```makefile
.PHONY: all install link packages test clean

all: install

install: link packages

link:
	@echo "Creating symlinks..."
	@./scripts/link.sh

packages:
	@echo "Installing packages..."
	@brew bundle --file=local/share/dotfiles/brewfiles/.Brewfile

test:
	@echo "Running tests..."
	@shellcheck scripts/*.sh
	@zsh -n config/zsh/.zshrc

clean:
	@echo "Removing symlinks..."
	@./scripts/unlink.sh
```

### CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  shellcheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run ShellCheck
        uses: ludeeus/action-shellcheck@master
        with:
          scandir: './scripts'
```

---

## Cross-Platform Support

### OS Detection

```bash
case "$(uname -s)" in
    Darwin)
        # macOS specific
        export HOMEBREW_PREFIX="/opt/homebrew"
        ;;
    Linux)
        # Linux specific
        export HOMEBREW_PREFIX="/home/linuxbrew/.linuxbrew"
        ;;
esac
```

### Conditional Configuration

```bash
# Load OS-specific config
OS_CONFIG="$ZDOTDIR/os-$(uname -s | tr '[:upper:]' '[:lower:]').zsh"
[[ -f "$OS_CONFIG" ]] && source "$OS_CONFIG"
```

### Platform-Specific Brewfiles

```
local/share/dotfiles/brewfiles/
├── .Brewfile           # Common packages
├── .Brewfile.darwin    # macOS only
└── .Brewfile.linux     # Linux only
```
