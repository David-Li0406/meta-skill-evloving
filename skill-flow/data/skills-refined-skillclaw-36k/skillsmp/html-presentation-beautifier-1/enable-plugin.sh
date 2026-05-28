#!/bin/bash

# Quick enable script for html-presentation-beautifier plugin
# This script enables the plugin in the current directory

set -e

PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_DIR="$(pwd)"

echo "🔗 Enabling HTML Presentation Beautifier Plugin..."
echo "   Plugin: $PLUGIN_DIR"
echo "   Target: $CURRENT_DIR"
echo ""

# Check if already enabled
if [ -L ".claude-plugin" ] && [ "$(readlink .claude-plugin)" = "$PLUGIN_DIR/.claude-plugin" ]; then
    echo "✅ Plugin already enabled in this directory"
    exit 0
fi

# Create symlinks
echo "Creating symlinks..."

if [ -e ".claude-plugin" ]; then
    if [ -L ".claude-plugin" ]; then
        rm .claude-plugin
    else
        echo "❌ Error: .claude-plugin already exists and is not a symlink"
        echo "   Please remove it first:"
        echo "   rm -rf .claude-plugin"
        exit 1
    fi
fi

if [ -e "commands" ]; then
    if [ -L "commands" ]; then
        rm commands
    else
        echo "❌ Error: commands already exists and is not a symlink"
        echo "   Please remove it first:"
        echo "   rm -rf commands"
        exit 1
    fi
fi

if [ -e "skills" ]; then
    if [ -L "skills" ]; then
        rm skills
    else
        echo "❌ Error: skills already exists and is not a symlink"
        echo "   Please remove it first:"
        echo "   rm -rf skills"
        exit 1
    fi
fi

# Create the symlinks
ln -s "$PLUGIN_DIR/.claude-plugin" .claude-plugin
ln -s "$PLUGIN_DIR/commands" commands
ln -s "$PLUGIN_DIR/skills" skills

echo ""
echo "✅ Plugin enabled successfully!"
echo ""
echo "You can now use the /beauty command in this directory."
echo ""
echo "Usage: /beauty <file1> <file2> ..."
echo ""
