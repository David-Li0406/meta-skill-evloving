---
name: dotfiles-management
description: Use this skill for best practices in managing dotfiles, ensuring XDG compliance, maintainability, and security when configuring your development environment.
---

# Dotfiles Management

This skill provides comprehensive guidance on managing dotfiles effectively, focusing on maintainability, security, and automation.

## Core Principles

### 1. XDG Base Directory Compliance

Follow the XDG specification for a clean home directory setup:

```bash
XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"
XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
```

### 2. Security: Separate Sensitive Data

Utilize the `.local` pattern for machine-specific secrets to avoid committing sensitive information:

```bash
# In .zshrc
[[ -f ~/.zshrc.local ]] && source ~/.zshrc.local

# In .gitconfig
[include]
    path = ~/.gitconfig.local
```

### 3. Modular Structure

Organize your dotfiles by tool or purpose for better maintainability:

```
dotfiles/
├── config/
│   ├── git/
│   ├── zsh/
│   ├── nvim/
│   └── tmux/
├── local/share/dotfiles/
└── makefile
```

## Quick Reference

### Adding New Config

1. Place config in `config/<tool-name>/`
2. Update `link.sh` to create symlink
3. Add `.local.template` for sensitive values
4. Test with `make link && make verify`

### Script Standards

```bash
#!/bin/bash
set -eu
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

info "Starting task"
# Use helper functions: isRunningOnMac, safeDownload, etc.
success "Task complete"
```

## Advice Workflow

1. Identify the configuration type (shell, editor, git, etc.)
2. Check XDG compliance options
3. Apply security patterns (.local separation)
4. Reference popular repositories for proven patterns
5. Suggest automation (Makefile targets, CI)

## Common Recommendations

### Shell Configuration

- Split into logical files: `aliases.zsh`, `functions.zsh`, `path.zsh`
- Use lazy loading for heavy plugins
- Keep PATH modifications in one place

### Git Configuration

- Use conditional includes for work/personal
- Set up sensible defaults (autostash, rerere)
- Configure commit signing

### Editor (Neovim/Vim)

- Use a plugin manager (lazy.nvim recommended)
- Organize plugins by category in `lua/plugins/`
- Keep keymaps in a dedicated file