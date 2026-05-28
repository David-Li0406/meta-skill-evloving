#!/bin/bash

# HTML Presentation Beautifier Plugin Installation Script
# This script installs the plugin globally or creates a symlink in the current directory

set -e

PLUGIN_NAME="html-presentation-beautifier"
PLUGIN_SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GLOBAL_PLUGIN_DIR="$HOME/.claude-code-plugins"
INSTALL_TYPE="${1:-local}"

echo "🎨 HTML Presentation Beautifier Plugin Installer"
echo "================================================"
echo ""

# Detect installation type
if [ "$INSTALL_TYPE" = "global" ] || [ "$INSTALL_TYPE" = "-g" ] || [ "$INSTALL_TYPE" = "--global" ]; then
    INSTALL_TYPE="global"
elif [ "$INSTALL_TYPE" = "link" ] || [ "$INSTALL_TYPE" = "-l" ] || [ "$INSTALL_TYPE" = "--link" ]; then
    INSTALL_TYPE="link"
else
    INSTALL_TYPE="local"
fi

case $INSTALL_TYPE in
    global)
        echo "📦 Installing plugin globally..."
        echo "   Source: $PLUGIN_SOURCE"
        echo "   Target: $GLOBAL_PLUGIN_DIR/$PLUGIN_NAME"

        # Create global plugin directory if it doesn't exist
        mkdir -p "$GLOBAL_PLUGIN_DIR"

        # Copy plugin to global directory
        if [ -d "$GLOBAL_PLUGIN_DIR/$PLUGIN_NAME" ]; then
            echo "⚠️  Plugin already exists in global directory. Removing old version..."
            rm -rf "$GLOBAL_PLUGIN_DIR/$PLUGIN_NAME"
        fi

        cp -R "$PLUGIN_SOURCE" "$GLOBAL_PLUGIN_DIR/$PLUGIN_NAME"
        echo "✅ Plugin installed globally to: $GLOBAL_PLUGIN_DIR/$PLUGIN_NAME"
        echo ""
        echo "📝 To use this plugin in a project, create a symlink:"
        echo "   ln -s $GLOBAL_PLUGIN_DIR/$PLUGIN_NAME/.claude-plugin .claude-plugin"
        echo "   ln -s $GLOBAL_PLUGIN_DIR/$PLUGIN_NAME/commands commands"
        echo "   ln -s $GLOBAL_PLUGIN_DIR/$PLUGIN_NAME/skills skills"
        ;;

    link)
        echo "🔗 Creating symlinks in current directory..."
        echo "   Source: $PLUGIN_SOURCE"
        echo "   Target: $(pwd)"

        # Check if we're in a git repository
        if [ ! -d .git ] && [ ! -f .git ]; then
            echo "⚠️  Warning: Current directory doesn't appear to be a git repository"
            read -p "Continue anyway? (y/N) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                echo "❌ Installation cancelled"
                exit 1
            fi
        fi

        # Create symlinks
        if [ -e .claude-plugin ]; then
            echo "⚠️  .claude-plugin already exists. Skipping..."
        else
            ln -s "$PLUGIN_SOURCE/.claude-plugin" .claude-plugin
            echo "✅ Created symlink: .claude-plugin"
        fi

        if [ -e commands ]; then
            echo "⚠️  commands already exists. Skipping..."
        else
            ln -s "$PLUGIN_SOURCE/commands" commands
            echo "✅ Created symlink: commands"
        fi

        if [ -e skills ]; then
            echo "⚠️  skills already exists. Skipping..."
        else
            ln -s "$PLUGIN_SOURCE/skills" skills
            echo "✅ Created symlink: skills"
        fi

        echo ""
        echo "✅ Plugin linked in current directory"
        ;;

    local)
        echo "📋 Plugin is already installed in: $PLUGIN_SOURCE"
        echo ""
        echo "The plugin structure is ready. No additional installation needed."
        echo ""
        echo "To use the /beauty command, make sure you're in the plugin directory"
        echo "or create symlinks in your project directory:"
        echo ""
        echo "  ./install.sh link    # Create symlinks in current directory"
        echo "  ./install.sh global  # Install globally"
        echo ""
        ;;

esac

echo ""
echo "🎉 Installation complete!"
echo ""
echo "📚 Plugin Information:"
echo "   Name: $PLUGIN_NAME"
echo "   Version: 1.0.0"
echo "   Command: /beauty"
echo ""
echo "Usage: /beauty <file1> <file2> ..."
echo ""
