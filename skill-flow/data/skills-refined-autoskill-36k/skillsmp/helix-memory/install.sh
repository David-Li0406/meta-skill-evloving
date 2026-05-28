#!/bin/bash
# Helix Memory - One-liner installer
# Usage: curl -fsSL https://raw.githubusercontent.com/MarcinDudekDev/helix-memory/main/install.sh | bash

set -e

REPO_URL="https://github.com/MarcinDudekDev/helix-memory.git"
INSTALL_DIR="$HOME/.claude/skills/helix-memory"

echo ""
echo "  ╦ ╦┌─┐┬  ┬─┐ ┬  ╔╦╗┌─┐┌┬┐┌─┐┬─┐┬ ┬"
echo "  ╠═╣├┤ │  │┌┴┬┘  ║║║├┤ ││││ │├┬┘└┬┘"
echo "  ╩ ╩└─┘┴─┘┴┴ └─  ╩ ╩└─┘┴ ┴└─┘┴└─ ┴ "
echo ""
echo "  Long-term memory for Claude Code"
echo ""

# Check dependencies
echo "Checking dependencies..."

if ! command -v docker &>/dev/null; then
    echo "ERROR: Docker required. Install from https://docker.com/products/docker-desktop"
    exit 1
fi
echo "  ✓ Docker"

if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python 3 required."
    exit 1
fi
echo "  ✓ Python 3"

# Install requests if missing
python3 -c "import requests" 2>/dev/null || pip3 install -q requests
echo "  ✓ Python requests"

# Install Helix CLI if missing
if ! command -v helix &>/dev/null; then
    echo ""
    echo "Installing Helix CLI..."
    curl -fsSL https://www.helix-db.com/install.sh | bash
    export PATH="$HOME/.local/bin:$PATH"
fi
echo "  ✓ Helix CLI"

# Clone or update repo
echo ""
if [ -d "$INSTALL_DIR/.git" ]; then
    echo "Updating existing installation..."
    cd "$INSTALL_DIR"
    git pull --quiet
else
    echo "Installing to $INSTALL_DIR..."
    rm -rf "$INSTALL_DIR"
    mkdir -p "$(dirname "$INSTALL_DIR")"
    git clone --quiet "$REPO_URL" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# Make scripts executable
chmod +x memory hooks/*.py 2>/dev/null || true

# Copy SKILL.md to root for Claude discovery
cp -f skills/helix-memory/SKILL.md . 2>/dev/null || true

# Start Docker if needed
if ! docker info &>/dev/null 2>&1; then
    echo ""
    echo "Starting Docker..."
    open -a "Docker Desktop" 2>/dev/null || true
    sleep 5
fi

# Initialize HelixDB
echo ""
echo "Starting HelixDB..."
helix push dev 2>/dev/null || true

# Verify
echo ""
if curl -s http://localhost:6969/health >/dev/null 2>&1; then
    echo "  ✓ HelixDB running on localhost:6969"
else
    echo "  ! HelixDB may need a moment to start"
fi

# Success
echo ""
echo "════════════════════════════════════════════"
echo "  Installation complete!"
echo "════════════════════════════════════════════"
echo ""
echo "  Quick start:"
echo "    $INSTALL_DIR/memory status"
echo "    $INSTALL_DIR/memory search \"topic\""
echo ""
echo "  Add alias to ~/.zshrc:"
echo "    alias memory='$INSTALL_DIR/memory'"
echo ""
echo "  Optional - better semantic search:"
echo "    brew install ollama && ollama pull nomic-embed-text"
echo ""
echo "  Hooks are auto-configured via the plugin."
echo "  Restart Claude Code to activate."
echo ""
