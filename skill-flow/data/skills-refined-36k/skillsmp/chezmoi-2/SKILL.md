---
name: chezmoi
description: Manage dotfiles using chezmoi. Use when working with dotfile management, cross-platform configuration, templating config files, editing dotfiles, or when the user mentions chezmoi, dotfiles, apply, diff, source state, or configuration sync.
allowed-tools:
  - Bash(chezmoi:*)
---

# Chezmoi Dotfile Manager

Chezmoi manages dotfiles across multiple machines using a source directory, version control, and Go templates.

## Core Concepts

### Three-Tier Architecture

1. **Home directory** (`~`) - Your actual dotfiles (destination state)
2. **Source directory** (`~/.local/share/chezmoi/`) - Chezmoi's managed files (source state)
3. **Remote repository** - Git repo for syncing across machines

### Source State Encoding

Chezmoi encodes file attributes in filenames:
- `dot_bashrc` → `~/.bashrc`
- `private_dot_netrc` → `~/.netrc` (restricted permissions)
- `executable_dot_local/bin/script` → `~/.local/bin/script` (executable)

## Essential Commands

```bash
# Preview and Apply
chezmoi diff                           # Show detailed diff
chezmoi diff --reverse                 # Show what destination has that source doesn't
chezmoi apply                          # Apply all changes
chezmoi apply ~/.bashrc                # Apply specific file
chezmoi apply -v                       # Verbose apply
chezmoi apply -n                       # Dry-run (preview only)

# Adding and Editing
chezmoi add ~/.bashrc                  # Add file to source state
chezmoi add --template ~/.config/file  # Add as template
chezmoi edit ~/.bashrc                 # Edit in $EDITOR
chezmoi edit --apply ~/.bashrc         # Edit and apply immediately

# Inspection
chezmoi cat ~/.bashrc                  # Show what would be written
chezmoi data                           # Show all template variables
chezmoi source-path ~/.bashrc          # Show source file path
chezmoi execute-template '{{ .chezmoi.os }}'  # Test template expression

# Syncing
chezmoi update                         # Pull and apply (git pull + apply)
chezmoi re-add                         # Re-add modified managed files

# File Management
chezmoi forget ~/.old-config           # Stop managing (keep file)
chezmoi chattr +template ~/.bashrc     # Convert to template
chezmoi chattr +executable ~/.local/bin/script  # Make executable
```

## Application Order

When running `chezmoi apply`:
1. `run_before_` scripts execute first
2. Files, directories, and symlinks are created/updated
3. `run_after_` scripts execute last

## Detailed Documentation

- **[File Naming Conventions](file-naming.md)** - Prefixes, suffixes, and filename encoding
- **[Templating](templating.md)** - Go template syntax, variables, and functions
- **[Scripts](scripts.md)** - Script types, execution order, and patterns
- **[External Files](external-files.md)** - Fetching files from URLs, archives, and git repos
- **[Secrets Management](secrets.md)** - Password managers and encryption
