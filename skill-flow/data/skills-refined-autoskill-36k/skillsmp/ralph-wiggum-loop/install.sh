#!/bin/bash
# gumloop installer
# 
# Install: curl -fsSL https://raw.githubusercontent.com/adriancodes/gumloop/main/install.sh | bash

set -euo pipefail

REPO="adriancodes/gumloop"
INSTALL_DIR="$HOME/.local/bin"
BINARY_NAME="gumloop"

echo "Installing gumloop..."

# Create install directory
mkdir -p "$INSTALL_DIR"

# Download binary
curl -fsSL "https://raw.githubusercontent.com/$REPO/main/gumloop" -o "$INSTALL_DIR/$BINARY_NAME"

# Make executable
chmod +x "$INSTALL_DIR/$BINARY_NAME"

# Check if PATH includes install dir
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "⚠️  $INSTALL_DIR is not in your PATH"
    echo ""
    echo "Add this to your shell config (~/.bashrc, ~/.zshrc, etc.):"
    echo ""
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "Then restart your shell or run: source ~/.bashrc"
    echo ""
fi

# Verify installation
if command -v gumloop &> /dev/null; then
    echo "✅ gumloop installed successfully!"
    echo ""
    gumloop --version
else
    echo "✅ gumloop installed to $INSTALL_DIR/$BINARY_NAME"
    echo ""
    echo "After updating your PATH, run: gumloop --help"
fi

echo ""
echo "Quick start:"
echo "  cd your-project"
echo "  git init"
echo "  gumloop -p 'Study codebase. Implement one thing. Commit.' --choo-choo"
echo ""
