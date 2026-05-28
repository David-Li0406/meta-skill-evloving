#!/usr/bin/env bash
# vm-bootstrap/install.sh - Interactive tool installation
# Follows LINUX_VM_BOOTSTRAP_SPEC.md phases
#
# IMPORTANT: This script is operator-confirmed (prompts before each install)
# NEVER prints secrets (tokens, API keys, bearer tokens, etc.)

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info() { echo -e "${BLUE}ℹ${NC} $*"; }
success() { echo -e "${GREEN}✓${NC} $*"; }
warn() { echo -e "${YELLOW}⚠${NC} $*"; }
error() { echo -e "${RED}✗${NC} $*"; }

confirm() {
    local prompt="$1"
    read -r -p "$prompt [y/N] " response
    case "$response" in
        [yY][eE][sS]|[yY])
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

echo "======================================"
echo " Linux VM Bootstrap Installer"
echo "======================================"
echo ""

# OS check
if [[ "$(uname -s)" != "Linux" ]]; then
    error "This installer is Linux-only. Detected: $(uname -s)"
    exit 1
fi

success "OS: Linux ($(uname -r))"
echo ""

warn "This is an INTERACTIVE installer that will prompt before each tool installation."
warn "It will NEVER print or store secrets (tokens, API keys, etc.)."
echo ""

if ! confirm "Continue with installation?"; then
    info "Installation cancelled."
    exit 0
fi

echo ""
info "Phase 0: Base OS packages (apt)"
echo ""

if confirm "Install base packages? (git, curl, jq, ripgrep, tmux, build tools)"; then
    info "Running: sudo apt-get update && sudo apt-get install -y ..."
    sudo apt-get update
    sudo apt-get install -y \
        git curl ca-certificates gnupg lsb-release unzip \
        build-essential pkg-config \
        jq ripgrep tmux
    success "Base packages installed"
else
    warn "Skipping base packages"
fi

echo ""
info "Phase 1: Homebrew (Linuxbrew)"
echo ""

if command -v brew >/dev/null 2>&1; then
    success "Homebrew already installed: $(brew --version | head -1)"
else
    if confirm "Install Homebrew (Linuxbrew)?"; then
        info "Running Homebrew installer..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

        # Add to shell profile
        if [[ -f /home/linuxbrew/.linuxbrew/bin/brew ]]; then
            eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
            if [[ -f ~/.bashrc ]] && ! grep -q "linuxbrew" ~/.bashrc; then
                echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.bashrc
            fi
            success "Homebrew installed"
        else
            error "Homebrew installation may have failed"
        fi
    else
        warn "Skipping Homebrew"
    fi
fi

echo ""
info "Phase 2: mise (toolchain manager)"
echo ""

if command -v mise >/dev/null 2>&1; then
    success "mise already installed: $(mise --version)"
else
    if confirm "Install mise?"; then
        info "Running mise installer..."
        curl https://mise.run | sh

        # Add to shell profile
        if [[ -f ~/.bashrc ]] && ! grep -q "mise activate" ~/.bashrc; then
            echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc
        fi
        success "mise installed (restart shell or run: source ~/.bashrc)"
    else
        warn "Skipping mise"
    fi
fi

echo ""
info "Phase 3: GitHub CLI (gh)"
echo ""

if command -v gh >/dev/null 2>&1; then
    success "gh already installed: $(gh --version | head -1)"
else
    if command -v brew >/dev/null 2>&1; then
        if confirm "Install GitHub CLI (gh) via Homebrew?"; then
            brew install gh
            success "gh installed"
        else
            warn "Skipping gh"
        fi
    else
        warn "Homebrew not available, skipping gh installation"
        warn "Install Homebrew first or use: https://cli.github.com/manual/installation"
    fi
fi

echo ""
info "Phase 4: Poetry (Python dependency manager)"
echo ""

if command -v poetry >/dev/null 2>&1; then
    success "poetry already installed: $(poetry --version)"
else
    if confirm "Install Poetry via pipx?"; then
        if ! command -v pipx >/dev/null 2>&1; then
            info "Installing pipx first..."
            python3 -m pip install --user pipx
            python3 -m pipx ensurepath
        fi
        pipx install poetry
        success "poetry installed"
    else
        warn "Skipping poetry"
    fi
fi

echo ""
info "Phase 5: Beads CLI (bd)"
echo ""

if command -v bd >/dev/null 2>&1; then
    success "bd already installed: $(bd --version)"
else
    warn "Beads CLI (bd) not found"
    info "Install Beads per: https://github.com/beadshq/beads"
    info "Typically: npm install -g @beadshq/beads-cli"
fi

echo ""
info "Phase 6: Skills mount"
echo ""

if [[ -L "$HOME/.agent/skills" ]]; then
    TARGET="$(readlink "$HOME/.agent/skills")"
    success "~/.agent/skills -> $TARGET"
elif [[ -d "$HOME/.agent/skills" ]]; then
    success "~/.agent/skills exists (directory)"
else
    if confirm "Create ~/.agent/skills symlink -> ~/agent-skills?"; then
        mkdir -p ~/.agent
        if [[ -d ~/agent-skills ]]; then
            ln -sfn ~/agent-skills ~/.agent/skills
            success "~/.agent/skills -> ~/agent-skills"
        else
            warn "~/agent-skills directory not found"
            info "Clone first: git clone https://github.com/stars-end/agent-skills.git ~/agent-skills"
        fi
    else
        warn "Skipping skills mount"
    fi
fi

echo ""
echo "======================================"
echo " Installation Complete"
echo "======================================"
echo ""

info "Next steps:"
info "1. Restart your shell or run: source ~/.bashrc"
info "2. Clone repos: ~/prime-radiant-ai, ~/affordabot, ~/agent-skills"
info "3. Run 'mise install' in each repo"
info "4. Run 'gh auth login' to authenticate"
info "5. Run 'railway login' (in mise-enabled repo) to authenticate"
info "6. Run '~/agent-skills/vm-bootstrap/verify.sh check' to verify"

echo ""
