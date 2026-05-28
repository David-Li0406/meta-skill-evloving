# Scripts

Chezmoi supports executable scripts that run at specific points during `chezmoi apply`.

## Script Types

| Prefix | Behavior |
|--------|----------|
| `run_` | Run every `chezmoi apply` |
| `run_once_` | Run once per content hash |
| `run_onchange_` | Run when script content changes |
| `run_before_` | Run before file changes |
| `run_after_` | Run after file changes |

Combine prefixes: `run_once_before_`, `run_onchange_after_`, etc.

## Script Location

Place in `.chezmoiscripts/` or alongside managed files:

```
home/
├── .chezmoiscripts/
│   ├── run_once_before_install-packages.sh.tmpl
│   └── run_after_configure-macos.sh.tmpl
└── dot_config/
    └── run_onchange_reload-config.sh
```

## Environment Variables

Scripts receive these environment variables:

| Variable | Value |
|----------|-------|
| `CHEZMOI` | `1` |
| `CHEZMOI_OS` | Operating system |
| `CHEZMOI_ARCH` | Architecture |
| `CHEZMOI_HOSTNAME` | Hostname |
| `CHEZMOI_SOURCE_DIR` | Source directory path |
| `CHEZMOI_HOME_DIR` | Home directory path |

## Example: Package Installation

```bash
#!/bin/bash
# run_once_before_install-packages.sh.tmpl

set -e

{{ if eq .chezmoi.os "darwin" -}}
brew bundle --file={{ joinPath .chezmoi.sourceDir "Brewfile" | quote }}
{{ else if eq .chezmoi.os "linux" -}}
{{   if eq .chezmoi.osRelease.id "ubuntu" -}}
sudo apt update && sudo apt install -y ripgrep fd-find bat
{{   else if eq .chezmoi.osRelease.id "fedora" -}}
sudo dnf install -y ripgrep fd-find bat
{{   else if eq .chezmoi.osRelease.id "arch" -}}
sudo pacman -S --noconfirm ripgrep fd bat
{{   end -}}
{{ end -}}
```

## Example: Trigger on File Change

Use hash comments to trigger `run_onchange_` when a file changes:

```bash
#!/bin/bash
# run_onchange_reload-shell.sh.tmpl
# Hash: {{ include "dot_zshrc.tmpl" | sha256sum }}

# This script runs when .zshrc changes
echo "Shell config updated. Restart your shell to apply changes."
```

## Example: Numbered Execution Order

Use numbers in script names to control order:

```
.chezmoiscripts/
├── run_onchange_after_1-setup-directories.sh
├── run_onchange_after_2-install-oh-my-zsh.sh
└── run_onchange_after_3-install-homebrew.sh
```

Scripts run in alphabetical order, so `1-` runs before `2-`.

## Script Best Practices

1. **Use `set -e`** to exit on error
2. **Use `set -u`** to error on undefined variables
3. **Make scripts idempotent** - safe to run multiple times
4. **Use `run_once_`** for one-time setup (package installation)
5. **Use `run_onchange_`** for config reloads triggered by file changes
6. **Include hash comments** to trigger `run_onchange_` scripts
7. **Use `.tmpl` suffix** for OS-specific logic

## Resetting Script State

```bash
chezmoi state delete-bucket --bucket=scriptState   # Reset run_once_
chezmoi state delete-bucket --bucket=entryState    # Reset run_onchange_
```

## Debugging Scripts

```bash
chezmoi apply -v                       # Verbose output
chezmoi apply -n                       # Dry run (shows what would run)
chezmoi diff                           # Preview changes
```

## Modify Scripts

Use `modify_` prefix for scripts that modify existing files:

```bash
#!/bin/bash
# modify_dot_bashrc

# Read current file from stdin
cat

# Append new content
echo "# Added by chezmoi"
echo "export NEW_VAR=value"
```

The script receives the current file contents on stdin and outputs the modified contents on stdout.
