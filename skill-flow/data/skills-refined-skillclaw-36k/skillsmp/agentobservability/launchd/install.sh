#!/bin/bash
# Install observability server as launchd service

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE="$SCRIPT_DIR/com.pai.observability-server.plist.template"
TARGET="$HOME/Library/LaunchAgents/com.pai.observability-server.plist"
USER=$(whoami)

# Detect bun path
BUN_PATH=$(which bun 2>/dev/null || echo "/opt/homebrew/bin/bun")

echo "Installing observability server launchd service..."
echo "  User: $USER"
echo "  Bun: $BUN_PATH"

# Create LaunchAgents directory if needed
mkdir -p "$HOME/Library/LaunchAgents"

# Create logs directory
mkdir -p "$HOME/.claude/Skills/AgentObservability/logs"

# Generate plist from template
sed -e "s|{{USER}}|$USER|g" \
    -e "s|/opt/homebrew/bin/bun|$BUN_PATH|g" \
    "$TEMPLATE" > "$TARGET"

echo "Created: $TARGET"

# Unload if already loaded
launchctl bootout gui/$(id -u)/com.pai.observability-server 2>/dev/null || true

# Load the service
launchctl bootstrap gui/$(id -u) "$TARGET"

echo "Service installed and started!"
echo ""
echo "Management commands:"
echo "  Status:  launchctl list | grep observability"
echo "  Stop:    launchctl stop com.pai.observability-server"
echo "  Start:   launchctl start com.pai.observability-server"
echo "  Logs:    tail -f ~/.claude/Skills/AgentObservability/logs/server-stdout.log"
