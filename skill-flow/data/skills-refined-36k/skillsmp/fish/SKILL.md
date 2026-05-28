---
name: fish
description: Help with fish shell configuration, aliases, functions, and keybindings. Use when the user asks about shell config, aliases, or when modifying shell behavior. IMPORTANT - Trent uses fish as his primary shell, not zsh.
---

# Fish Shell Skill

## Overview

**Fish is Trent's primary shell.** Always add aliases and functions to fish config, not zsh.

## Configuration Locations

- **Main config**: `~/.config/fish/config.fish`
- **Functions**: `~/.config/fish/functions/*.fish` (one function per file)
- **Local overrides**: `~/.config/fish/conf.d/local.fish`
- **Secrets (not tracked)**: `~/.config/fish/secrets.fish`
- **Completions**: `~/.config/fish/completions/*.fish`

## Config Structure

The main `config.fish` is organized into sections:

1. **Core Shell Setup** - Homebrew, environment variables, PATH
2. **Essential Tools** - starship, zoxide, fzf, nvm
3. **Aliases** - All aliases in one place
4. **Vi Mode** - Fish vi mode with cursor shape changes
5. **Auto-start** - Creates "home" tmux session on startup

## Key Aliases

```fish
# Shell
alias ef='nvim ~/.config/fish/config.fish'
alias elf='nvim ~/.config/fish/conf.d/local.fish'

# Claude
alias cc='claude'
alias ccr='claude --resume'
alias ccd='claude --dangerously-skip-permissions'

# Modern CLI tools
alias cat='bat'
alias ls='eza'
alias ll='eza -l'
alias la='eza -la'
alias tree='eza --tree'
alias v='nvim'

# Chezmoi
alias cadd='chezmoi re-add'
alias capply='chezmoi apply'

# Tmux
alias ta='tmux attach -t'
alias tn='tmux new -s'
alias tls='tmux ls'
alias tk='tmux kill-session -t'

# Git
alias gc='git commit -m'
alias gca='git add . && git commit -a -m'
alias gp='git push origin HEAD'
alias gpu='git pull origin'
alias gst='git status'
alias ghpr='gh pr create -f --draft && gh pr view --web'

# Python
alias python='python3'
alias pip='pip3'
alias cvenv='python3 -m venv .venv'
alias svenv='source .venv/bin/activate'
alias ur='uv run'

# SSH
alias mm='ssh -L 3000:localhost:3000 -L 8000:localhost:8000 trenthaines@100.77.152.106'
```

## Key Functions (in ~/.config/fish/functions/)

- `t.fish` - Smart tmux attach/create
- `ts.fish` - Tmux session selector with fzf
- `tns.fish` - Create new tmux session with git project
- `tnw.fish` - Create new tmux window with 3-pane layout
- `cf.fish` - Change directory with fzf
- `vf.fish` - Open file in nvim with fzf
- `rgf.fish` - Ripgrep with fzf
- `glog.fish` - Git log with fzf
- `gs.fish` - Git status
- `otp.fish` - OTP code generator

## Vi Mode

Fish is configured with vi mode:

```fish
fish_vi_key_bindings

# Cursor shapes
set -g fish_cursor_default block      # Normal mode
set -g fish_cursor_insert line        # Insert mode
set -g fish_cursor_replace_one underscore
set -g fish_cursor_visual block

# Key bindings
bind -M default v edit_command_buffer  # Edit in nvim
bind -M insert \ce edit_command_buffer
```

## Adding New Aliases

Add to the Aliases section in `~/.config/fish/config.fish`:

```fish
alias name='command'
```

## Adding New Functions

Create a new file `~/.config/fish/functions/funcname.fish`:

```fish
function funcname --description "Description here"
    # function body
end
```

## Plugin Manager

Uses **fisher** for plugins:

```fish
fisher install jorgebucaran/nvm.fish  # Example
fisher list                            # List installed
fisher update                          # Update all
```

Current plugins:
- `nvm.fish` - Node version manager
- `bass` - Run bash scripts in fish

## Integration with Other Tools

- **Starship** - Prompt (init in config.fish)
- **Zoxide** - Smart cd (init in config.fish)
- **fzf** - Fuzzy finder (init in config.fish)
- **Tmux** - Auto-creates "home" session on startup
- **Pyenv** - Python version manager (shims in PATH)

## Common Tasks

### Reload config
```fish
source ~/.config/fish/config.fish
# or just open new terminal
```

### Edit config
```fish
ef   # Opens config.fish in nvim
elf  # Opens local.fish in nvim
```

### Add to PATH
```fish
set -gx PATH "/new/path" $PATH
# or
fish_add_path /new/path
```

### Set environment variable
```fish
set -gx VAR_NAME "value"
```

## Notes

- Fish syntax differs from bash/zsh - no `export`, use `set -gx`
- Command substitution: `(command)` not `$(command)`
- No need to quote variables in most cases
- Functions auto-load from functions/ directory
