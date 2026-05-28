# Terminal Integration

Guide for terminal-based workflows with Claude Code, including multiplexers, shell configuration, and terminal emulator optimization.

## Terminal Emulators

### macOS

| Terminal | Strength | Install |
|----------|----------|---------|
| iTerm2 | Most features, splits, profiles | `brew install --cask iterm2` |
| Warp | AI features, modern UI | `brew install --cask warp` |
| Kitty | GPU-accelerated, fast | `brew install --cask kitty` |
| Alacritty | Minimal, very fast | `brew install --cask alacritty` |
| Terminal.app | Built-in, zero setup | Pre-installed |

### Linux

| Terminal | Strength | Install |
|----------|----------|---------|
| Kitty | Fast, modern features | Package manager |
| Alacritty | GPU, minimal | Package manager / cargo |
| Terminator | Native splits | Package manager |
| Tilix | Tiling, GTK | Package manager |

### Windows

| Terminal | Strength | Install |
|----------|----------|---------|
| Windows Terminal | Modern, tabs, profiles | Microsoft Store |
| WSL + any Linux terminal | Full Linux experience | Microsoft Store |

## iTerm2 Configuration

### Profile for Claude Code

```
Preferences > Profiles > + (new profile)
Name: Claude Code
Working Directory: Reuse previous session's directory
```

### Colors and Font

```
Preferences > Profiles > Colors
- Import a color scheme (Solarized, Dracula, etc.)

Preferences > Profiles > Text
- Font: JetBrains Mono, Fira Code, or Source Code Pro
- Size: 13-14pt
- [x] Use ligatures (if font supports)
```

### Split Panes

| Action | Shortcut |
|--------|----------|
| Split horizontally | Cmd+D |
| Split vertically | Cmd+Shift+D |
| Navigate panes | Cmd+[ and Cmd+] |
| Close pane | Cmd+W |
| Maximize pane | Cmd+Shift+Enter |

### Session Persistence

```
Preferences > General > Closing
- [x] Confirm closing multiple sessions
- [x] Confirm "Quit iTerm2"

Preferences > General > Window
- [x] Native full screen windows
- [x] Separate window for each tab
```

### Triggers (Auto-highlighting)

```
Preferences > Profiles > Advanced > Triggers > Edit

Regex: error|Error|ERROR
Action: Highlight Text
Parameters: Red background

Regex: warning|Warning|WARNING
Action: Highlight Text
Parameters: Yellow background

Regex: success|passed|PASS
Action: Highlight Text
Parameters: Green text
```

## tmux Deep Dive

### Installation

```bash
# macOS
brew install tmux

# Ubuntu/Debian
sudo apt install tmux

# Fedora
sudo dnf install tmux
```

### Essential Commands

| Action | Command |
|--------|---------|
| New session | `tmux new -s name` |
| Attach session | `tmux attach -t name` |
| List sessions | `tmux ls` |
| Kill session | `tmux kill-session -t name` |
| Detach | `Ctrl+b d` |

### Pane Management

| Action | Shortcut |
|--------|----------|
| Split horizontal | `Ctrl+b "` |
| Split vertical | `Ctrl+b %` |
| Navigate | `Ctrl+b arrow` |
| Resize | `Ctrl+b Ctrl+arrow` |
| Zoom pane | `Ctrl+b z` |
| Close pane | `Ctrl+b x` |
| Swap panes | `Ctrl+b o` |

### Window Management

| Action | Shortcut |
|--------|----------|
| New window | `Ctrl+b c` |
| Next window | `Ctrl+b n` |
| Previous window | `Ctrl+b p` |
| Select window | `Ctrl+b 0-9` |
| Rename window | `Ctrl+b ,` |
| List windows | `Ctrl+b w` |

### Claude Code Layout Script

Create `~/.tmux-claude.sh`:

```bash
#!/bin/bash
# tmux layout for Claude Code development

SESSION="claude-dev"

# Kill existing session if present
tmux kill-session -t $SESSION 2>/dev/null

# Create new session with main window
tmux new-session -d -s $SESSION -n main

# Split for Claude Code (right side, 40%)
tmux split-window -h -p 40

# Split right pane for commands (bottom 30%)
tmux select-pane -t 1
tmux split-window -v -p 30

# Name panes (visible in status bar with config)
tmux select-pane -t 0 -T "Editor"
tmux select-pane -t 1 -T "Claude"
tmux select-pane -t 2 -T "Commands"

# Start in main editor pane
tmux select-pane -t 0

# Attach to session
tmux attach-session -t $SESSION
```

Run: `chmod +x ~/.tmux-claude.sh && ~/.tmux-claude.sh`

### tmux Configuration (~/.tmux.conf)

```bash
# Better prefix key
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# Enable mouse
set -g mouse on

# Start windows and panes at 1
set -g base-index 1
setw -g pane-base-index 1

# Easy split keys
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"

# Easy pane navigation
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# Resize panes with vim keys
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# 256 colors
set -g default-terminal "screen-256color"
set -ga terminal-overrides ",xterm-256color:Tc"

# Status bar
set -g status-position top
set -g status-style bg=black,fg=white
set -g status-left "[#S] "
set -g status-right "%H:%M"

# Pane borders
set -g pane-border-style fg=brightblack
set -g pane-active-border-style fg=blue

# Copy mode with vim keys
setw -g mode-keys vi
bind -T copy-mode-vi v send -X begin-selection
bind -T copy-mode-vi y send -X copy-pipe-and-cancel "pbcopy"

# History
set -g history-limit 50000

# Reload config
bind r source-file ~/.tmux.conf \; display "Reloaded!"
```

### tmux Plugin Manager (TPM)

```bash
# Install TPM
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

# Add to ~/.tmux.conf
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-resurrect'  # Save/restore sessions
set -g @plugin 'tmux-plugins/tmux-continuum'  # Auto-save

# Initialize TPM (put at bottom of tmux.conf)
run '~/.tmux/plugins/tpm/tpm'
```

Press `Ctrl+b I` to install plugins.

## screen (Alternative to tmux)

### Basic Commands

| Action | Command |
|--------|---------|
| New session | `screen -S name` |
| Detach | `Ctrl+a d` |
| Reattach | `screen -r name` |
| List sessions | `screen -ls` |
| Split horizontal | `Ctrl+a S` |
| Split vertical | `Ctrl+a |` |
| Navigate splits | `Ctrl+a Tab` |
| New window | `Ctrl+a c` |

### ~/.screenrc

```bash
# Status line
hardstatus alwayslastline
hardstatus string '%{= kG}[%{G}%H%{g}][%= %{= kw}%?%-Lw%?%{r}(%{W}%n*%f%t%?(%u)%?%{r})%{w}%?%+Lw%?%?%= %{g}][%{B}%Y-%m-%d %{W}%c%{g}]'

# Scrollback
defscrollback 10000

# No startup message
startup_message off

# UTF-8
defutf8 on
```

## Shell Configuration

### Zsh for Claude Code (~/.zshrc)

```bash
# Claude Code environment
export ANTHROPIC_API_KEY="your-key-here"
export CLAUDE_CODE_EDITOR="code"  # or webstorm, vim

# Aliases for Claude workflow
alias cc="claude"
alias ccr="claude --resume"
alias ccp="claude --print"

# Quick navigation
alias ..="cd .."
alias ...="cd ../.."
alias ll="ls -la"

# Git shortcuts (Claude-friendly)
alias gs="git status"
alias gd="git diff"
alias gl="git log --oneline -10"
alias gp="git pull"

# Project shortcuts
alias dev="bun run dev"
alias test="bun test"
alias lint="bun run lint"

# Prompt showing git branch
autoload -Uz vcs_info
precmd() { vcs_info }
zstyle ':vcs_info:git:*' formats '%b '
setopt PROMPT_SUBST
PROMPT='%F{cyan}%~%f %F{yellow}${vcs_info_msg_0_}%f$ '
```

### Bash for Claude Code (~/.bashrc)

```bash
# Claude Code environment
export ANTHROPIC_API_KEY="your-key-here"
export CLAUDE_CODE_EDITOR="code"

# Aliases
alias cc="claude"
alias ccr="claude --resume"

# Git prompt
parse_git_branch() {
  git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}
PS1='\[\e[36m\]\w\[\e[33m\]$(parse_git_branch)\[\e[0m\]$ '
```

## Clipboard Integration

### macOS

```bash
# Already available
pbcopy  # Copy stdin to clipboard
pbpaste # Output clipboard to stdout

# Usage
echo "text" | pbcopy
cat file.txt | pbcopy
pbpaste > output.txt
```

### Linux (X11)

```bash
# Install xclip
sudo apt install xclip

# Add aliases to ~/.zshrc or ~/.bashrc
alias pbcopy="xclip -selection clipboard"
alias pbpaste="xclip -selection clipboard -o"
```

### Linux (Wayland)

```bash
# Install wl-clipboard
sudo apt install wl-clipboard

# Aliases
alias pbcopy="wl-copy"
alias pbpaste="wl-paste"
```

### tmux Clipboard Integration

```bash
# In ~/.tmux.conf for macOS
bind -T copy-mode-vi y send -X copy-pipe-and-cancel "pbcopy"

# For Linux
bind -T copy-mode-vi y send -X copy-pipe-and-cancel "xclip -selection clipboard"
```

## SSH and Remote Sessions

### Persistent Claude Sessions over SSH

```bash
# Start tmux session on remote
ssh user@server "tmux new -s claude -d"

# Attach to it
ssh -t user@server "tmux attach -t claude"

# Or in one command
ssh -t user@server "tmux new -As claude"
```

### SSH Config for Quick Access

```bash
# ~/.ssh/config
Host dev
    HostName dev.example.com
    User developer
    ForwardAgent yes
    RequestTTY yes
    RemoteCommand tmux new -As claude
```

Then just: `ssh dev`

### Keeping Sessions Alive

```bash
# ~/.ssh/config
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

## Command History

### Infinite History

```bash
# ~/.zshrc
HISTFILE=~/.zsh_history
HISTSIZE=999999999
SAVEHIST=999999999
setopt SHARE_HISTORY
setopt HIST_IGNORE_DUPS

# ~/.bashrc
HISTSIZE=999999
HISTFILESIZE=999999
HISTCONTROL=ignoredups
shopt -s histappend
```

### Fuzzy History Search (fzf)

```bash
# Install
brew install fzf  # macOS
apt install fzf   # Ubuntu

# Enable in shell
# Ctrl+R now shows fuzzy search
```

## Performance Tips

### Fast Terminal Startup

```bash
# Audit shell startup time
time zsh -i -c exit

# Common slowdowns:
# - nvm/nvm init (use fnm instead)
# - many plugins
# - complex prompts
```

### Reduce Latency

```bash
# In terminal app settings, disable:
# - Animations
# - Transparency effects

# In shell:
# - Use minimal prompt during heavy work
# - Disable syntax highlighting temporarily
```

## Troubleshooting

### Colors Not Working

```bash
# Add to ~/.zshrc or ~/.bashrc
export TERM=xterm-256color

# For tmux, add to ~/.tmux.conf
set -g default-terminal "screen-256color"
set -ga terminal-overrides ",xterm-256color:Tc"
```

### tmux + Vim Colors Broken

```bash
# In ~/.vimrc or ~/.config/nvim/init.vim
set termguicolors
let &t_8f = "\<Esc>[38;2;%lu;%lu;%lum"
let &t_8b = "\<Esc>[48;2;%lu;%lu;%lum"
```

### Copy/Paste Not Working in tmux

```bash
# Check if reattach-to-user-namespace is needed (older macOS)
brew install reattach-to-user-namespace

# In ~/.tmux.conf
set -g default-command "reattach-to-user-namespace -l $SHELL"
```

### Session Lost After Disconnect

```bash
# Always use tmux or screen for important work
# Or enable autosave with tmux-resurrect plugin

# Quick session check
tmux ls  # List existing sessions
tmux attach -t 0  # Attach to first session
```

## Example Terminal-Only Workflow

```bash
# 1. Start development session
~/.tmux-claude.sh
# Creates: [Editor | Claude | Commands] layout

# 2. In Editor pane (left)
vim .

# 3. In Claude pane (top-right)
claude

# 4. In Commands pane (bottom-right)
bun test --watch

# 5. Navigate between panes
Ctrl+b h/j/k/l  # (with vim-style config)
# or
Ctrl+b arrow

# 6. Zoom into Claude pane temporarily
Ctrl+b z  # Toggle zoom

# 7. Detach when done
Ctrl+b d

# 8. Resume later
tmux attach -t claude-dev
```
