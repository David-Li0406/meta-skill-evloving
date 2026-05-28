#!/bin/bash
# Dotfiles Installation Script
# Supports macOS and Linux

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIGS_DIR="$(dirname "$SCRIPT_DIR")/configs"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

info() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Detect OS
detect_os() {
    case "$(uname -s)" in
        Darwin) OS="macos" ;;
        Linux)  OS="linux" ;;
        *)      error "Unsupported OS: $(uname -s)" ;;
    esac
    info "Detected OS: $OS"
}

# Backup existing config
backup_if_exists() {
    local file="$1"
    if [[ -f "$file" && ! -L "$file" ]]; then
        local backup="${file}.backup.$(date +%Y%m%d%H%M%S)"
        warn "Backing up $file to $backup"
        mv "$file" "$backup"
    fi
}

# Install dependencies
install_deps() {
    info "Installing dependencies..."

    if [[ "$OS" == "macos" ]]; then
        if ! command -v brew &>/dev/null; then
            error "Homebrew not found. Install from https://brew.sh"
        fi
        brew install neovim fzf eza tmux || true
        brew install --cask ghostty font-sf-mono-nerd-font || true

    elif [[ "$OS" == "linux" ]]; then
        if command -v apt &>/dev/null; then
            sudo apt update
            sudo apt install -y neovim fzf tmux zsh curl git
            # eza needs manual install on Ubuntu
            if ! command -v eza &>/dev/null; then
                warn "eza not in apt, install from: https://github.com/eza-community/eza/releases"
            fi
        elif command -v pacman &>/dev/null; then
            sudo pacman -S --noconfirm neovim fzf eza tmux zsh ghostty
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y neovim fzf tmux zsh
        else
            warn "Unknown package manager. Please install: neovim, fzf, eza, tmux, zsh manually"
        fi
    fi
}

# Create directories
create_dirs() {
    info "Creating config directories..."
    mkdir -p ~/.config/nvim
    mkdir -p ~/.config/ghostty
    mkdir -p ~/.config/tmux
}

# Install configs
install_configs() {
    info "Installing configuration files..."

    # Zsh
    backup_if_exists ~/.zshrc
    cp "$CONFIGS_DIR/zshrc" ~/.zshrc
    info "Installed ~/.zshrc"

    # Tmux (XDG location)
    backup_if_exists ~/.config/tmux/tmux.conf
    cp "$CONFIGS_DIR/tmux.conf" ~/.config/tmux/tmux.conf
    info "Installed ~/.config/tmux/tmux.conf"

    # Neovim
    backup_if_exists ~/.config/nvim/init.lua
    cp "$CONFIGS_DIR/init.lua" ~/.config/nvim/init.lua
    info "Installed ~/.config/nvim/init.lua"

    # Ghostty
    backup_if_exists ~/.config/ghostty/config
    cp "$CONFIGS_DIR/ghostty" ~/.config/ghostty/config
    info "Installed ~/.config/ghostty/config"
}

# Install Neovim plugins
install_nvim_plugins() {
    info "Installing Neovim plugins (this may take a moment)..."
    nvim --headless "+Lazy! sync" +qa 2>/dev/null || true
    info "Neovim plugins installed"
}

# Main
main() {
    echo "======================================"
    echo "  Dotfiles Installation Script"
    echo "======================================"
    echo ""

    detect_os

    read -p "Install dependencies? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_deps
    fi

    create_dirs
    install_configs

    read -p "Install Neovim plugins now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_nvim_plugins
    fi

    echo ""
    info "Installation complete!"
    echo ""
    echo "Next steps:"
    echo "  1. Restart your terminal or run: source ~/.zshrc"
    echo "  2. Open Neovim to finish plugin installation"
    echo "  3. (Optional) Set zsh as default: chsh -s \$(which zsh)"
}

main "$@"
