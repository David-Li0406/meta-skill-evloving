# Popular Dotfiles Repositories

Reference implementations from well-maintained dotfiles repositories.

## Table of Contents

1. [Overview](#overview)
2. [Featured Repositories](#featured-repositories)
3. [Pattern Comparison](#pattern-comparison)
4. [Key Takeaways](#key-takeaways)

---

## Overview

| Repository | Focus | Management | Notable Features |
|------------|-------|------------|------------------|
| mathiasbynens/dotfiles | macOS | Bootstrap script | Comprehensive macOS defaults |
| holman/dotfiles | Topic-based | Topical organization | Modular design |
| thoughtbot/dotfiles | Simplicity | rcm | Minimal, well-documented |
| dmmulroy/.dotfiles | Modern CLI | GNU Stow | dot CLI tool, Fish shell |
| coderabbitai/dotfiles | AI-powered | chezmoi | Copilot integration |

---

## Featured Repositories

### mathiasbynens/dotfiles

**URL**: github.com/mathiasbynens/dotfiles

**Key Features**:
- Extensive macOS defaults configuration
- Bootstrap script for full setup
- Sensible shell defaults

**Structure**:
```
.
├── .aliases
├── .bash_profile
├── .bashrc
├── .exports
├── .functions
├── .macos          # macOS defaults script
├── .path
├── bootstrap.sh
└── brew.sh
```

**Notable Pattern**: Single flat structure with dot-prefixed files.

---

### holman/dotfiles

**URL**: github.com/holman/dotfiles

**Key Features**:
- Topic-centric organization
- Automatic sourcing by file extension
- Homebrew-first approach

**Structure**:
```
.
├── bin/
├── git/
│   ├── aliases.zsh
│   ├── gitconfig.symlink
│   └── gitignore.symlink
├── ruby/
├── zsh/
├── script/
│   ├── bootstrap
│   └── install
└── Brewfile
```

**Notable Pattern**: `*.symlink` files get linked to `$HOME`.

**Loading Convention**:
- `path.zsh` - Loaded first, PATH modifications
- `*.zsh` - Loaded automatically
- `completion.zsh` - Loaded last

---

### thoughtbot/dotfiles

**URL**: github.com/thoughtbot/dotfiles

**Key Features**:
- Minimal and focused
- Uses rcm for management
- Easy to fork and customize

**Structure**:
```
.
├── aliases
├── gitconfig
├── gitmessage
├── gitignore
├── tmux.conf
├── vimrc
└── zshrc
```

**Notable Pattern**: Extremely simple, uses rcm's conventions.

---

### dmmulroy/.dotfiles

**URL**: github.com/dmmulroy/.dotfiles

**Key Features**:
- Custom `dot` CLI tool
- GNU Stow for symlinks
- Fish shell focus
- Claude Code integration

**Structure**:
```
.
├── dot                 # CLI tool
├── home/
│   └── .config/
│       ├── fish/
│       ├── nvim/
│       └── tmux/
├── packages/
│   ├── bundle
│   └── bundle.work
└── scripts/
```

**Notable Pattern**: Home directory mirrors target structure for Stow.

**CLI Commands**:
```bash
dot init              # Full installation
dot update            # Update packages
dot doctor            # Check system health
dot link              # Create symlinks
```

---

### coderabbitai/dotfiles

**URL**: github.com/coderabbitai/dotfiles

**Key Features**:
- chezmoi management
- AI integration (Copilot)
- Auto-update system
- Gruvbox theming

**Structure**:
```
.
├── .chezmoi.toml.tmpl
├── .chezmoiexternal.toml
├── dot_config/
│   ├── nvim/
│   ├── tmux/
│   └── zsh/
└── run_once_install.sh
```

**Notable Pattern**: chezmoi templating for machine-specific config.

**Auto-Update System**:
```bash
# Configurable update interval
export SYSTEM_UPDATE_DAYS=7

# Force update
autoupdate.zsh --force
```

---

## Pattern Comparison

### Symlink Management

| Method | Pros | Cons |
|--------|------|------|
| **GNU Stow** | Simple, reversible | Requires specific structure |
| **chezmoi** | Templating, encryption | Learning curve |
| **rcm** | Thoughtbot standard | Ruby dependency |
| **Custom script** | Full control | Maintenance burden |

### File Organization

| Pattern | Example | Best For |
|---------|---------|----------|
| **Flat** | mathiasbynens | Small configs |
| **Topic-based** | holman | Many tools |
| **XDG Mirror** | dmmulroy | XDG compliance |
| **chezmoi** | coderabbitai | Multi-machine |

### Shell Choice

| Shell | Repository | Benefits |
|-------|------------|----------|
| Bash | mathiasbynens | Universal |
| Zsh | holman, thoughtbot | Plugins, completion |
| Fish | dmmulroy | Modern syntax, fast |

---

## Key Takeaways

### From mathiasbynens
- Comprehensive `.macos` defaults script
- Document every setting change

### From holman
- Topic-based organization scales well
- Convention over configuration (`*.symlink`)

### From thoughtbot
- Simplicity wins
- Well-documented is better than clever

### From dmmulroy
- CLI tools improve UX
- Stow provides clean symlink management
- Conditional work/personal configs

### From coderabbitai
- chezmoi enables templating
- Auto-updates keep system fresh
- AI integration enhances productivity

---

## Useful Resources

- **awesome-dotfiles**: github.com/webpro/awesome-dotfiles
- **dotfiles.github.io**: Community guide
- **XDG Base Directory**: specifications.freedesktop.org/basedir-spec
