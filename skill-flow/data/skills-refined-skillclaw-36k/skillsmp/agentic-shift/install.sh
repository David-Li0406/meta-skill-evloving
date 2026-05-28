#!/bin/bash
# The Agentic Shift - One-line installer
# curl -sL https://raw.githubusercontent.com/vishwastam/the-agentic-shift/main/install.sh | bash

set -e

SKILL_NAME="agentic-shift"
SKILL_DIR="$HOME/.claude/skills/$SKILL_NAME"
REPO_URL="https://github.com/vishwastam/the-agentic-shift"

echo "Installing The Agentic Shift..."

# Check if Claude Code is installed
if ! command -v claude &> /dev/null; then
    echo "Error: Claude Code CLI not found."
    echo "Install it first: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

# Create skills directory if needed
mkdir -p "$HOME/.claude/skills"

# Remove existing installation
if [ -d "$SKILL_DIR" ]; then
    rm -rf "$SKILL_DIR"
fi

# Clone just the skill folder
echo "Downloading skill..."
TMP_DIR=$(mktemp -d)
git clone --depth 1 --filter=blob:none --sparse "$REPO_URL" "$TMP_DIR" 2>/dev/null
cd "$TMP_DIR"
git sparse-checkout set agentic-shift-skill 2>/dev/null
mv agentic-shift-skill "$SKILL_DIR"
cd - > /dev/null
rm -rf "$TMP_DIR"

echo ""
echo "Installed! Start with:"
echo ""
echo "  claude /agentic-shift"
echo ""
