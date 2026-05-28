# Chezmoi Scripts (run_once, run_onchange, run_before, etc.)

## Overview

Chezmoi supports executable scripts that run automatically at specific times during the `chezmoi apply` process. Scripts use Go templates and can be conditional.

## Script Types

### run_once

Run exactly once per machine.

**Filename pattern:** `run_once_<name>.sh.tmpl` (or `.tmpl` extension)

**Use cases:**
- Initial setup tasks
- One-time installations
- Bootstrapping

**Example:**
```bash
# run_once_install_homebrew.sh.tmpl
{{ if eq .chezmoi.os "darwin" -}}
#!/bin/bash
if ! command -v brew &> /dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
{{ end -}}
```

### run_onchange

Run whenever the script file changes (detected by chezmoi).

**Filename pattern:** `run_onchange_<name>.sh.tmpl`

**Use cases:**
- Install/update packages
- Rebuild configs
- Apply changes

**Example - Conditional package installation:**
```bash
# run_onchange_install-packages.sh.tmpl
{{ if eq .chezmoi.os "linux" -}}
#!/bin/bash
sudo apt update
sudo apt install -y ripgrep fd-find bat exa
{{ else if eq .chezmoi.os "darwin" -}}
#!/bin/bash
brew install ripgrep fd bat eza
{{ end -}}
```

**Example - Brew bundle:**
```bash
# run_onchange_brew-bundle.sh.tmpl
{{ if eq .chezmoi.os "darwin" -}}
#!/bin/bash
brew bundle --file=/dev/stdin <<EOF
{{ range .packages.darwin.brews -}}
brew "{{ . }}"
{{ end -}}
{{ range .packages.darwin.casks -}}
cask "{{ . }}"
{{ end -}}
EOF
{{ end -}}
```

### run_before

Run before the target file is applied.

**Filename pattern:** `run_before_<target-file>.<ext>.tmpl`

**Example:**
```bash
# run_before_dot_vimrc.sh.tmpl
{{ if eq .chezmoi.os "darwin" -}}
#!/bin/bash
# Ensure vim plugin directory exists before applying .vimrc
mkdir -p ~/.vim/autoload ~/.vim/bundle
{{ end -}}
```

### run_after

Run after the target file is applied.

**Filename pattern:** `run_after_<target-file>.<ext>.tmpl`

**Example:**
```bash
# run_after_dot_tmux.conf.sh.tmpl
#!/bin/bash
# Reload tmux configuration
if command -v tmux &> /dev/null; then
    tmux source-file ~/.tmux.conf 2>/dev/null || true
fi
```

## Script Configuration

### Script Execution Order

Scripts execute in this order during `chezmoi apply`:

1. **run_before** scripts (before target files)
2. **run_once** scripts (if not already executed)
3. **run_onchange** scripts (if changed)
4. Target files are applied
5. **run_after** scripts (after target files)

### Script Attributes

Control script behavior with special file attributes:

```bash
# Make script executable
chezmoi chattr +executable run_once_install.sh.tmpl

# Make script quiet (suppress output)
chezmoi chattr +quiet run_onchange_update.sh.tmpl

# Prevent script from running
chezmoi chattr +prevent run_once_setup.sh.tmpl
```

**Common attributes:**
- `+executable`: Script must be executable (default for scripts)
- `-executable`: Don't make executable
- `+quiet`: Suppress script output
- `+prevent`: Don't run the script
- `+template`: Process as Go template (default for `.tmpl` files)

### Persistent State

**run_once tracking:**
- chezmoi tracks which `run_once` scripts have executed
- State stored in `~/.config/chezmoi/chezmoi.state`
- To re-run: `chezmoi state delete --run <script-name>`

**Re-run a run_once script:**
```bash
# View all script state
chezmoi state dump

# Clear all run_once script state (they will re-run on next apply)
chezmoi state delete-bucket --bucket=scriptState

# Or delete specific state entry by key
chezmoi state delete --bucket=scriptState --key=<script-sha256>
```

## Complete Examples

### System Setup

**run_once_000-setup-system.sh.tmpl:**
```bash
#!/bin/bash
set -euo pipefail

{{ if eq .chezmoi.os "darwin" -}}
# macOS setup
echo "Setting up macOS..."

# Install Xcode command line tools
if ! command -v xcode-select &> /dev/null; then
    xcode-select --install
fi

# Set default screenshot location
defaults write com.apple.screencapture location ~/Downloads
killall SystemUIServer

{{ else if eq .chezmoi.os "linux" -}}
# Linux setup
echo "Setting up Linux..."

# Ensure basic packages
sudo apt update
sudo apt install -y curl git wget build-essential

{{ end -}}
```

### Package Management

**run_onchange_install-packages.sh.tmpl:**
```bash
#!/bin/bash
set -euo pipefail

{{ if eq .chezmoi.os "darwin" -}}
# macOS with Homebrew
if ! brew bundle --file=/dev/stdin <<EOF
{{ range .packages.darwin.brews -}}
brew "{{ . }}"
{{ end -}}
{{ range .packages.darwin.casks -}}
cask "{{ . }}"
{{ end -}}
{{ range .packages.darwin.mas -}}
mas "{{ . }}"
{{ end -}}
EOF
then
    echo "Some Homebrew packages failed to install"
fi

{{ else if eq .chezmoi.os "linux" -}}
# Linux with apt
{{ if .packages.linux }}
sudo apt install -y {{ range .packages.linux }}{{ . }} {{ end }}
{{ end }}
{{ end -}}
```

### Development Tools

**run_onchange_install-dev-tools.sh.tmpl:**
```bash
#!/bin/bash
set -euo pipefail

# Install language-specific tools

{{ if .tools.golang -}}
# Go tools
if command -v go &> /dev/null; then
    go install golang.org/x/tools/gopls@latest
    go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
fi
{{ end -}}

{{ if .tools.node -}}
# Node.js tools
if command -v npm &> /dev/null; then
    npm install -g typescript-language-server
    npm install -g @tailwindcss/language-server
fi
{{ end -}}

{{ if .tools.python -}}
# Python tools
if command -v pip3 &> /dev/null; then
    pip3 install --user black ruff mypy
fi
{{ end -}}
```

### Shell Plugins

**run_once_oh-my-zsh.sh.tmpl:**
```bash
#!/bin/bash
{{ if eq .chezmoi.os "darwin" -}}
if [ ! -d ~/.oh-my-zsh ]; then
    sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
fi
{{ end -}}
```

### Git Configuration

**run_after_dot_gitconfig.sh.tmpl:**
```bash
#!/bin/bash
# Set gitconfig includes for machine-specific settings
GITCONFIG_LOCAL="$HOME/.gitconfig.local"

if [ ! -f "$GITCONFIG_LOCAL" ]; then
    cat > "$GITCONFIG_LOCAL" <<EOF
# Machine-specific git configuration
EOF
fi
```

### Vim Plugins

**run_after_dot_vimrc.sh.tmpl:**
```bash
#!/bin/bash
# Install vim-plug if not present
if [ ! -f ~/.vim/autoload/plug.vim ]; then
    curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
        https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
fi

# Install plugins
vim +PlugInstall +qa
```

### Custom Tools Installation

**run_onchange_install-custom-tools.sh.tmpl:**
```bash
#!/bin/bash
set -euo pipefail

{{- if .chezmoi.githubToken -}}
# Install tools that require GitHub authentication

# gh (GitHub CLI)
if ! command -v gh &> /dev/null; then
    {{ if eq .chezmoi.os "darwin" -}}
    brew install gh
    {{ else if eq .chezmoi.os "linux" -}}
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
    sudo apt update
    sudo apt install gh
    {{ end -}}

    # Authenticate with GitHub
    echo "{{ .chezmoi.githubToken }}" | gh auth login --with-token
fi
{{ end -}}
```

## Data File Integration

**.chezmoidata/packages.yaml:**
```yaml
darwin:
  brews:
    - git
    - vim
    - ripgrep
    - fd
    - bat
    - eza
  casks:
    - firefox
    - visual-studio-code
  mas:
    - 497799835  # Xcode

linux:
  - git
  - vim
  - ripgrep
  - fd-find
  - bat
  - exa
```

**Usage in script:**
```bash
{{ range .packages.darwin.brews -}}
brew install {{ . }}
{{ end -}}
```

## Best Practices

1. **Always use `set -euo pipefail`** - Catch errors early
2. **Check command existence** - Before using tools
3. **Make scripts idempotent** - Safe to run multiple times
4. **Use descriptive names** - `run_once_000-bootstrap.sh.tmpl`
5. **Order run_once scripts** - Use prefixes (000_, 001_, etc.)
6. **Test scripts** - Run them manually before committing
7. **Keep scripts focused** - One responsibility per script
8. **Handle errors gracefully** - Use conditional checks
9. **Document dependencies** - Comment what's required
10. **Use templates** - Leverage `.chezmoi.os` and custom data

## Debugging Scripts

**Run scripts verbosely:**
```bash
chezmoi apply --verbose
```

**Dry run (show what would be executed):**
```bash
chezmoi apply --dry-run
```

**Scripts execute automatically** during `chezmoi apply`. There is no separate `chezmoi execute` command.

**Check script state:**
```bash
chezmoi state dump
```
