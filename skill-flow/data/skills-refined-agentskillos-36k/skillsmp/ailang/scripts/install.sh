#!/usr/bin/env bash
# Install AILANG binary from GitHub releases

set -euo pipefail

REPO="sunholo-data/ailang"
INSTALL_DIR="${AILANG_INSTALL_DIR:-/usr/local/bin}"

echo "Installing AILANG..."

# Detect platform
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

case "$OS" in
    darwin) PLATFORM="darwin" ;;
    linux) PLATFORM="linux" ;;
    mingw*|msys*|cygwin*) PLATFORM="windows" ;;
    *) echo "Unsupported OS: $OS" >&2; exit 1 ;;
esac

case "$ARCH" in
    x86_64|amd64) ARCH="amd64" ;;
    arm64|aarch64) ARCH="arm64" ;;
    *) echo "Unsupported architecture: $ARCH" >&2; exit 1 ;;
esac

echo "Detected: $PLATFORM-$ARCH"

# Get latest release
echo "Fetching latest release..."
LATEST=$(curl -sL "https://api.github.com/repos/$REPO/releases/latest" | grep '"tag_name"' | sed -E 's/.*"([^"]+)".*/\1/')

if [[ -z "$LATEST" ]]; then
    echo "Failed to fetch latest release" >&2
    exit 1
fi

echo "Latest version: $LATEST"

# Construct download URL
if [[ "$PLATFORM" == "windows" ]]; then
    ASSET="ailang-${PLATFORM}-${ARCH}.zip"
else
    ASSET="ailang-${PLATFORM}-${ARCH}.tar.gz"
fi

URL="https://github.com/$REPO/releases/download/$LATEST/$ASSET"
echo "Downloading: $URL"

# Download and extract
TMP_DIR=$(mktemp -d)
trap "rm -rf $TMP_DIR" EXIT

cd "$TMP_DIR"
curl -sL "$URL" -o "$ASSET"

if [[ "$PLATFORM" == "windows" ]]; then
    unzip -q "$ASSET"
else
    tar xzf "$ASSET"
fi

# Install binary
if [[ -w "$INSTALL_DIR" ]]; then
    mv ailang "$INSTALL_DIR/"
else
    echo "Installing to $INSTALL_DIR (requires sudo)..."
    sudo mv ailang "$INSTALL_DIR/"
fi

echo ""
echo "AILANG installed successfully!"
echo "Version: $(ailang --version 2>/dev/null || echo 'unknown')"
echo "Location: $(which ailang)"
