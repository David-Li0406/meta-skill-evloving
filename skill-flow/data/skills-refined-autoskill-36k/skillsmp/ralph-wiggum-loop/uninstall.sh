#!/bin/bash
# gumloop uninstaller

set -euo pipefail

INSTALL_DIR="$HOME/.local/bin"
BINARY_NAME="gumloop"

if [ -f "$INSTALL_DIR/$BINARY_NAME" ]; then
    rm "$INSTALL_DIR/$BINARY_NAME"
    echo "✅ gumloop uninstalled"
else
    echo "gumloop not found at $INSTALL_DIR/$BINARY_NAME"
fi
