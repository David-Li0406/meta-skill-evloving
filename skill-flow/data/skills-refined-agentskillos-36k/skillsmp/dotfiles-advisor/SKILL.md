---
name: dotfiles-advisor
description: Dotfiles management best practices for XDG-compliant, cross-platform, and maintainable configurations. Use when adding new config files to dotfiles, refactoring existing configurations, improving setup scripts, or ensuring security with sensitive data separation. Covers automation (Makefile, CI/CD), maintainability (modularity, documentation), and security (.local pattern).
---

# Dotfiles Advisor

Provide best practices and advice for dotfiles management based on popular repositories and established patterns.

## Core Principles

### 1. XDG Base Directory Compliance

Follow XDG specification for clean home directory:

```bash
XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"
XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
```

### 2. Security: Separate Sensitive Data

Use `.local` pattern for machine-specific secrets:

```bash
# In .zshrc
[[ -f ~/.zshrc.local ]] && source ~/.zshrc.local

# In .gitconfig
[include]
    path = ~/.gitconfig.local
```

Never commit: API keys, tokens, credentials, work-specific paths.

### 3. Modular Structure

Organize by tool/purpose:

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

| Topic | Reference |
|-------|-----------|
| Best practices | [references/best-practices.md](references/best-practices.md) |
| Popular repos | [references/popular-repos.md](references/popular-repos.md) |
| Security | [references/security.md](references/security.md) |

## Advice Workflow

1. Identify the configuration type (shell, editor, git, etc.)
2. Check XDG compliance options
3. Apply security patterns (.local separation)
4. Reference popular repos for proven patterns
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

- Use plugin manager (lazy.nvim recommended)
- Organize plugins by category in `lua/plugins/`
- Keep keymaps in dedicated file
