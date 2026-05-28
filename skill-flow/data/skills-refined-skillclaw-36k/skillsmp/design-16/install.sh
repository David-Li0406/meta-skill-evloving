#!/bin/bash
# install.sh - Link design-ops commands to Claude Code
#
# Usage: ~/.claude/plugins/design-ops/install.sh

set -e

PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"
COMMANDS_SOURCE="$PLUGIN_DIR/commands"
COMMANDS_TARGET="$HOME/.claude/commands"

echo "Design Ops Installer"
echo "===================="
echo ""
echo "Plugin directory: $PLUGIN_DIR"
echo "Commands target:  $COMMANDS_TARGET"
echo ""

# Create target directory
mkdir -p "$COMMANDS_TARGET"

# Helper function to link a file
link_command() {
    local source="$1"
    local name="$2"

    # Remove existing symlink or file
    if [[ -L "$COMMANDS_TARGET/$name" ]]; then
        rm "$COMMANDS_TARGET/$name"
    elif [[ -f "$COMMANDS_TARGET/$name" ]]; then
        echo "  Warning: $name exists as file, backing up to $name.bak"
        mv "$COMMANDS_TARGET/$name" "$COMMANDS_TARGET/$name.bak"
    fi

    ln -s "$source" "$COMMANDS_TARGET/$name"
    echo "  ✓ Linked: $name"
}

COUNT=0

# Link the main design.md skill (the core /design command)
if [[ -f "$PLUGIN_DIR/design.md" ]]; then
    link_command "$PLUGIN_DIR/design.md" "design.md"
    COUNT=$((COUNT + 1))
fi

# Link each command from commands/ subdirectory
for cmd in "$COMMANDS_SOURCE"/*.md; do
    [[ -f "$cmd" ]] || continue
    name=$(basename "$cmd")
    link_command "$cmd" "$name"
    COUNT=$((COUNT + 1))
done

echo ""
echo "Done. Linked $COUNT command(s) to $COMMANDS_TARGET"
echo ""
echo "Available slash commands:"

# Show main design command
if [[ -f "$PLUGIN_DIR/design.md" ]]; then
    echo "  /design (main skill with subcommands)"
fi

# Show additional commands
for cmd in "$COMMANDS_SOURCE"/*.md; do
    [[ -f "$cmd" ]] || continue
    name=$(basename "$cmd" .md)
    echo "  /$name"
done

echo ""
echo "Run '/design' to see all available subcommands."
