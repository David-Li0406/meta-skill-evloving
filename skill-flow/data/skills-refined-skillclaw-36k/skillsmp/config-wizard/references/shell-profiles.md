# Shell Profile Configuration

Complete guide for shell integration, prompts, and productivity enhancements.

## Shell Integration

### Ghostty Shell Integration

Ghostty provides native shell integration for enhanced features.

#### Automatic Detection
```
shell-integration = detect
```

#### Explicit Shell
```
shell-integration = zsh    # or bash, fish, elvish
```

#### Features
```
shell-integration-features = cursor,sudo,title
```

**Available features:**
- `cursor` - Change cursor shape based on vi mode
- `sudo` - Preserve integration through sudo
- `title` - Set window title to current command
- `no-cursor` / `no-sudo` / `no-title` - Disable specific features

### Shell Configuration Files

#### Zsh
Add to `~/.zshrc`:
```bash
# Ghostty shell integration (usually auto-loaded)
if [[ -n "$GHOSTTY_RESOURCES_DIR" ]]; then
  source "$GHOSTTY_RESOURCES_DIR/shell-integration/zsh/ghostty-integration"
fi
```

#### Bash
Add to `~/.bashrc`:
```bash
# Ghostty shell integration
if [[ -n "$GHOSTTY_RESOURCES_DIR" ]]; then
  source "$GHOSTTY_RESOURCES_DIR/shell-integration/bash/ghostty-integration"
fi
```

#### Fish
Add to `~/.config/fish/config.fish`:
```fish
# Ghostty shell integration
if set -q GHOSTTY_RESOURCES_DIR
  source "$GHOSTTY_RESOURCES_DIR/shell-integration/fish/ghostty-integration"
end
```

## Prompt Themes

### Starship (Recommended)

Cross-shell, fast, customizable prompt.

#### Installation
```bash
# macOS
brew install starship

# Linux
curl -sS https://starship.rs/install.sh | sh
```

#### Shell Setup
```bash
# Zsh (~/.zshrc)
eval "$(starship init zsh)"

# Bash (~/.bashrc)
eval "$(starship init bash)"

# Fish (~/.config/fish/config.fish)
starship init fish | source
```

#### Configuration (~/.config/starship.toml)

**Minimal preset:**
```toml
format = "$directory$git_branch$git_status$character"

[character]
success_symbol = "[➜](green)"
error_symbol = "[➜](red)"

[directory]
truncation_length = 3
truncate_to_repo = true

[git_branch]
format = "[$branch]($style) "
style = "purple"

[git_status]
format = '[$all_status$ahead_behind]($style) '
style = "yellow"
```

**Powerline preset:**
```toml
format = """
[](bg:#3c3836 fg:#8ec07c)\
$directory\
[](fg:#3c3836 bg:#504945)\
$git_branch\
$git_status\
[](fg:#504945 bg:#665c54)\
$cmd_duration\
[](fg:#665c54)\
$line_break\
$character"""

[directory]
format = "[ $path ]($style)"
style = "fg:#282828 bg:#8ec07c"
truncation_length = 3

[git_branch]
format = "[ $branch ]($style)"
style = "fg:#ebdbb2 bg:#504945"

[git_status]
format = "[$all_status$ahead_behind]($style)"
style = "fg:#fabd2f bg:#504945"

[cmd_duration]
format = "[ $duration ]($style)"
style = "fg:#ebdbb2 bg:#665c54"
min_time = 2_000

[character]
success_symbol = "[❯](green)"
error_symbol = "[❯](red)"
```

### Powerlevel10k (Zsh Only)

Feature-rich zsh prompt with configuration wizard.

#### Installation
```bash
# Oh My Zsh
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k

# Homebrew
brew install powerlevel10k
echo "source $(brew --prefix)/share/powerlevel10k/powerlevel10k.zsh-theme" >> ~/.zshrc
```

#### Configuration
```bash
# Run configuration wizard
p10k configure
```

#### Recommended settings for Ghostty:
- **Prompt style**: Rainbow or Lean
- **Character set**: Unicode
- **Prompt flow**: Two lines
- **Enable transient prompt**: Yes (cleaner history)

### Pure (Minimal)

Simple, fast prompt.

#### Installation
```bash
# npm
npm install --global pure-prompt

# Homebrew
brew install pure
```

#### Zsh Setup
```bash
# ~/.zshrc
autoload -U promptinit; promptinit
prompt pure
```

### Custom Minimal Prompt

For those who want minimal dependencies.

#### Zsh
```bash
# ~/.zshrc
autoload -Uz vcs_info
precmd() { vcs_info }
zstyle ':vcs_info:git:*' formats '%b'

setopt PROMPT_SUBST
PROMPT='%F{cyan}%~%f %F{magenta}${vcs_info_msg_0_}%f %F{green}❯%f '
```

#### Bash
```bash
# ~/.bashrc
parse_git_branch() {
  git branch 2>/dev/null | grep '^*' | colrm 1 2
}

PS1='\[\033[36m\]\w\[\033[0m\] \[\033[35m\]$(parse_git_branch)\[\033[0m\] \[\033[32m\]❯\[\033[0m\] '
```

## Useful Aliases

### Navigation
```bash
# Quick directory access
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias ~='cd ~'

# List files
alias ll='ls -lah'
alias la='ls -A'
alias l='ls -CF'

# Modern replacements (if installed)
alias ls='eza --icons'        # or 'exa' for older version
alias ll='eza -lah --icons'
alias tree='eza --tree --icons'
alias cat='bat'
```

### Git Shortcuts
```bash
# Status and info
alias gs='git status'
alias gd='git diff'
alias gl='git log --oneline -20'
alias glog='git log --graph --oneline --all'

# Branching
alias gb='git branch'
alias gco='git checkout'
alias gcb='git checkout -b'
alias gm='git merge'

# Committing
alias ga='git add'
alias gc='git commit'
alias gcm='git commit -m'
alias gca='git commit --amend'

# Remote
alias gp='git push'
alias gpf='git push --force-with-lease'
alias gpl='git pull'
alias gf='git fetch'

# Utilities
alias grh='git reset --hard'
alias grs='git reset --soft HEAD~1'
alias gst='git stash'
alias gstp='git stash pop'
```

### Development
```bash
# Node/npm
alias ni='npm install'
alias nr='npm run'
alias nrd='npm run dev'
alias nrb='npm run build'
alias nrt='npm run test'

# Python
alias py='python3'
alias pip='pip3'
alias venv='python3 -m venv'
alias activate='source venv/bin/activate'

# Docker
alias d='docker'
alias dc='docker compose'
alias dps='docker ps'
alias dex='docker exec -it'
```

### Claude Code
```bash
alias cc='claude'
alias ccc='claude --continue'
alias ccr='claude --resume'
```

## Useful Functions

### Quick Project Navigation
```bash
# Jump to project directories
function proj() {
  cd ~/projects/"$1" 2>/dev/null || cd ~/Projects/"$1" 2>/dev/null || echo "Project not found: $1"
}

# With tab completion (zsh)
_proj() {
  _files -W ~/projects -/
}
compdef _proj proj
```

### Git Helpers
```bash
# Quick commit with message
function gcam() {
  git add -A && git commit -m "$*"
}

# Create and push new branch
function gnew() {
  git checkout -b "$1" && git push -u origin "$1"
}

# Delete merged branches
function gclean() {
  git branch --merged | grep -v '\*\|main\|master' | xargs -n 1 git branch -d
}
```

### Directory Utilities
```bash
# Create directory and cd into it
function mkcd() {
  mkdir -p "$1" && cd "$1"
}

# Find and cd to directory
function fcd() {
  cd "$(find . -type d -name "*$1*" | head -1)"
}
```

## Oh My Zsh (Optional)

Popular zsh framework with plugins.

### Installation
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

### Recommended Plugins
```bash
# ~/.zshrc
plugins=(
  git
  docker
  npm
  python
  colored-man-pages
  command-not-found
  zsh-autosuggestions
  zsh-syntax-highlighting
)
```

### Plugin Installation
```bash
# zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

## Environment Setup

### PATH Configuration
```bash
# ~/.zshrc or ~/.bashrc
export PATH="$HOME/bin:$HOME/.local/bin:$PATH"
export PATH="$HOME/.cargo/bin:$PATH"  # Rust
export PATH="$HOME/go/bin:$PATH"       # Go
```

### Common Environment Variables
```bash
export EDITOR='code'  # or vim, nvim, etc.
export VISUAL='code'
export PAGER='less'
export LANG='en_US.UTF-8'
```

### History Configuration (Zsh)
```bash
HISTSIZE=50000
SAVEHIST=50000
HISTFILE=~/.zsh_history
setopt EXTENDED_HISTORY
setopt HIST_EXPIRE_DUPS_FIRST
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
setopt HIST_VERIFY
setopt SHARE_HISTORY
```

## Ghostty-Specific Shell Tips

### Detect Ghostty
```bash
if [[ -n "$GHOSTTY_RESOURCES_DIR" ]]; then
  # Running in Ghostty
  echo "Welcome to Ghostty!"
fi
```

### Set Window Title
```bash
# Zsh
function set_title() {
  echo -ne "\033]0;$1\007"
}
precmd() { set_title "${PWD/#$HOME/~}" }
preexec() { set_title "$1" }
```

### Quick Terminal Settings
```bash
# Toggle transparency (requires Ghostty to be configured for it)
alias ghost-solid='ghostty +set-config background-opacity=1.0'
alias ghost-trans='ghostty +set-config background-opacity=0.95'
```
