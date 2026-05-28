---
name: dotfiles
description: Manage dotfiles configuration with bidirectional sync between local environment and ~/.dotfiles repository. Understand the automation script, configuration structure, and common commands.
---

# Dotfiles Management Skill

## Overview

The dotfiles automation provides bidirectional sync between local configuration files and a centralized `~/.dotfiles` repository. Configuration is managed via `dotfiles.json` and the `dotfiles` command.

## Structure

**Repository**: `~/.dotfiles/` (git-tracked)

**Key Files**:
- `dotfiles.json` - Configuration mapping (tool → file paths)
- `config/` - Organized dotfile storage by tool name
- `bin/dotfiles` - Ruby automation script (also in `~/bin/dotfiles`)

**Storage Pattern**:
```
~/.dotfiles/config/{tool_name}/
```

Examples:
- `~/.dotfiles/config/git/.gitconfig`
- `~/.dotfiles/config/zsh/.zshrc`
- `~/.dotfiles/config/sublimetext/Preferences.sublime-settings`

## Configuration Format

**File**: `~/.dotfiles/dotfiles.json`

**Structure**:
```json
{
  "tool_name": [
    "~/path/to/config_file",
    "~/path/to/directory/*",
    "~/path/to/directory/"
  ]
}
```

**Path Types**:
- Single file: `~/.gitconfig`
- Directory (recursive): `~/.config/nvim/*` or `~/.config/nvim/`
- Preserves relative directory structure

## Commands

**Save (local → dotfiles)**:
```bash
dotfiles save          # Copy local configs to dotfiles repo
dotfiles save -n       # Dry run (show what would be done)
dotfiles save -v       # Verbose output
dotfiles save -p       # Prune removed files from dotfiles
```

**Load (dotfiles → local)**:
```bash
dotfiles load          # Restore configs from dotfiles repo
dotfiles load -n       # Dry run
dotfiles load -v       # Verbose output
dotfiles load -p       # Prune removed files from local
```

**Status**:
```bash
dotfiles status        # Show sync status of managed files
# Output: in sync, local changes, dotfile changes, missing, etc.
```

**Config**:
```bash
dotfiles config        # Show configuration mapping as JSON
```

## Status Indicators

| Status | Meaning | Color |
|--------|---------|-------|
| `in sync` | Files match | Green |
| `local changes` | Local file newer | Red |
| `dotfile changes` | Dotfile newer | Red |
| `local copy missing` | Only dotfile exists | Gray |
| `dotfile missing` | Only local exists | Gray |
| `neither exists` | Both missing | Red |

## Options

- `-n, --dry-run` - Preview changes without applying
- `-v, --verbose` - Show detailed file operations
- `-p, --prune` - Remove destination files missing from source
- `-h, --help` - Show help message

## Expected Workflows

When the user says specific commands, follow these workflows:

**"Save dotfiles"**:
1. Optionally run `dotfiles status` to check current state
2. Optionally run `dotfiles save -n -v` (dry-run) if you see it necessary
3. Run `dotfiles save -v`

**"Load dotfiles"**:
1. Optionally run `dotfiles status` to check current state
2. Optionally run `dotfiles load -n -v` (dry-run) for safety if you see it necessary
3. Run `dotfiles load -v`

**"Push dotfiles"**:
1. Change to `~/.dotfiles` directory
2. Run `git add .`
3. Run `git commit -m "Update dotfiles"`
4. Run `git push origin main` (or appropriate branch)
5. Resolve merge conflicts if necessary

**"Pull dotfiles"**:
1. Change to `~/.dotfiles` directory
2. Run `git pull origin main` (or appropriate branch)
3. Resolve merge conflicts if necessary

## Usage Guidelines

- Check `dotfiles status` when it makes sense before saving/loading
- Use dry-run (`-n`) for safety when you consider it necessary
- Edit `dotfiles.json` to add new config files
- Config stored in `~/.dotfiles/config/{tool_name}/`
- The `~/.dotfiles` repo is git-tracked
- Single source of truth for configuration across machines
