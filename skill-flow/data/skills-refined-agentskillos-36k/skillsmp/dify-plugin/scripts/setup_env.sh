#!/bin/bash
#
# Setup Dify plugin development environment
#
# Usage:
#   ./setup_env.sh              # Install dify CLI and uv
#   ./setup_env.sh --init NAME  # Also create a new plugin project
#
# If this script fails, see references/preparation.md for manual steps.

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

info() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Detect OS and architecture
detect_platform() {
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    ARCH=$(uname -m)

    case "$OS" in
        darwin) OS="darwin" ;;
        linux) OS="linux" ;;
        *) error "Unsupported OS: $OS" ;;
    esac

    case "$ARCH" in
        x86_64|amd64) ARCH="amd64" ;;
        arm64|aarch64) ARCH="arm64" ;;
        *) error "Unsupported architecture: $ARCH" ;;
    esac

    echo "$OS-$ARCH"
}

# Check if command exists
has_command() {
    command -v "$1" &> /dev/null
}

# Install Dify CLI
install_dify_cli() {
    if has_command dify; then
        info "dify CLI already installed: $(dify version 2>/dev/null || echo 'unknown version')"
        return 0
    fi

    PLATFORM=$(detect_platform)
    info "Detected platform: $PLATFORM"

    # Try brew on macOS first
    if [[ "$PLATFORM" == darwin-* ]] && has_command brew; then
        info "Installing dify CLI via Homebrew..."
        brew tap langgenius/dify 2>/dev/null || true
        brew install dify
        return 0
    fi

    # Manual download
    info "Downloading dify CLI..."
    RELEASE_URL="https://github.com/langgenius/dify-plugin-daemon/releases/latest/download/dify-plugin-${PLATFORM}"
    INSTALL_PATH="/usr/local/bin/dify"

    if [[ -w /usr/local/bin ]]; then
        curl -fsSL "$RELEASE_URL" -o "$INSTALL_PATH"
        chmod +x "$INSTALL_PATH"
    else
        warn "Need sudo to install to /usr/local/bin"
        sudo curl -fsSL "$RELEASE_URL" -o "$INSTALL_PATH"
        sudo chmod +x "$INSTALL_PATH"
    fi

    info "dify CLI installed: $(dify version)"
}

# Install uv (Python package manager)
install_uv() {
    if has_command uv; then
        info "uv already installed: $(uv --version)"
        return 0
    fi

    info "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Add to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"

    if has_command uv; then
        info "uv installed: $(uv --version)"
    else
        warn "uv installed but not in PATH. Add ~/.local/bin to your PATH"
    fi
}

# Check Python version
check_python() {
    if ! has_command python3; then
        error "Python 3 not found. Please install Python 3.12+"
    fi

    PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    info "Python version: $PY_VERSION"

    # Check if >= 3.12
    PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
    PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)

    if [[ "$PY_MAJOR" -lt 3 ]] || [[ "$PY_MAJOR" -eq 3 && "$PY_MINOR" -lt 12 ]]; then
        warn "Python 3.12+ recommended, you have $PY_VERSION"
    fi
}

# Initialize a new plugin project
init_plugin() {
    local name="$1"

    if [[ -z "$name" ]]; then
        info "Running interactive plugin init..."
        dify plugin init
    else
        info "Creating plugin: $name"
        mkdir -p "$name"
        cd "$name"
        dify plugin init
    fi
}

# Setup Python environment for plugin
setup_plugin_env() {
    if [[ ! -f "manifest.yaml" ]]; then
        warn "No manifest.yaml found. Run from plugin directory or use --init"
        return 1
    fi

    info "Setting up Python environment..."
    uv init --no-readme 2>/dev/null || true
    uv add dify_plugin
    info "Plugin environment ready"
}

# Main
main() {
    echo "========================================"
    echo "Dify Plugin Development Environment Setup"
    echo "========================================"
    echo

    check_python
    install_dify_cli
    install_uv

    echo
    info "Environment setup complete!"
    echo
    echo "Next steps:"
    echo "  1. Create a plugin:  dify plugin init"
    echo "  2. Setup deps:       cd <plugin> && uv init --no-readme && uv add dify_plugin"
    echo "  3. Get debug key:    python scripts/get_debug_key.py --host <url> ..."
    echo "  4. Run plugin:       uv run python -m main"

    # Handle --init flag
    if [[ "$1" == "--init" ]]; then
        echo
        init_plugin "$2"
        setup_plugin_env
    fi
}

main "$@"
