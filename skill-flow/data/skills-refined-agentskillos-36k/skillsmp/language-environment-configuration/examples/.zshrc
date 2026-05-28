# Zsh configuration for Claude Code sandbox
# This is a complete working example

# Path to oh-my-zsh installation
export ZSH="$HOME/.oh-my-zsh"

# Theme (using starship instead)
ZSH_THEME=""

# Plugins
plugins=(
  git
  docker
  rust
  python
  node
  npm
  command-not-found
  colored-man-pages
  zsh-autosuggestions
  zsh-syntax-highlighting
)

source $ZSH/oh-my-zsh.sh

# Language environments
export PATH="/root/.cargo/bin:$PATH"

export NVM_DIR="/root/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && . "$NVM_DIR/bash_completion"

# Python
export PYTHONUNBUFFERED=1

# Starship prompt
eval "$(starship init zsh)"

# Custom aliases
alias l='eza -ao --sort=old -F=always --icons=auto --color=always --color-scale=size --color-scale-mode=gradient --group-directories-first --git --git-ignore --no-quotes --time-style=relative --no-permissions --no-user'
alias ll='l -l'
alias lk='eza -a -F=never --icons=never --group-directories-first'

# eza tree function
lt() {
  eza -alT --icons=always --color=always --color-scale=all --color-scale-mode=gradient --group-directories-first --git --git-ignore --no-quotes --level=${1:-2}
}

# Git aliases
alias gs='git status'
alias gd='git diff'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline --graph --all'

# Development aliases
alias c='cargo'
alias cr='cargo run'
alias ct='cargo test'
alias cb='cargo build'

# Container indicator
if [ -f /.dockerenv ]; then
    export IN_CONTAINER=true
fi
