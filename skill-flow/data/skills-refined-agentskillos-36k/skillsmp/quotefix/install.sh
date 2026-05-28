#!/usr/bin/env bash

##############################################################################
# Quotefix Skill - Global Installer
#
# Installs the skill globally to ~/.claude/skills/ so it's available
# in ALL Claude Code sessions across all projects.
#
# Usage:
#   bash install.sh              # Install globally
#   bash install.sh --uninstall  # Remove global installation
##############################################################################

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Skill name
SKILL_NAME="quotefix"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Target directory (global personal skills)
TARGET_DIR="$HOME/.claude/skills/$SKILL_NAME"

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to install the skill
install_skill() {
    print_info "Installing Quotefix skill globally..."
    echo ""

    # Create the global skills directory if it doesn't exist
    if [ ! -d "$HOME/.claude/skills" ]; then
        mkdir -p "$HOME/.claude/skills"
        print_success "Created ~/.claude/skills directory"
    fi

    # Check if skill already exists
    if [ -d "$TARGET_DIR" ]; then
        print_warning "Skill already exists at $TARGET_DIR"
        read -p "Do you want to overwrite it? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Installation cancelled."
            exit 0
        fi
        rm -rf "$TARGET_DIR"
        print_success "Removed existing installation"
    fi

    # Copy the skill files
    cp -r "$SCRIPT_DIR" "$TARGET_DIR"
    print_success "Copied skill files to $TARGET_DIR"

    # Remove the install scripts from the target (we don't need them there)
    rm -f "$TARGET_DIR/install.sh"
    rm -f "$TARGET_DIR/install.ps1"
    rm -f "$TARGET_DIR/INSTALL.md"

    echo ""
    print_success "Installation complete!"
    echo ""
    print_info "The skill is now globally available in all Claude Code sessions."
    print_info "Location: $TARGET_DIR"
    echo ""
    print_info "Files installed:"
    echo "  - SKILL.md     (Main skill definition)"
    echo "  - examples.md  (Practical examples)"
    echo "  - README.md    (Documentation)"
    echo ""
    print_success "You can now use Claude Code in any project, and it will automatically"
    print_success "apply shell environment detection and nested quoting best practices!"
}

# Function to uninstall the skill
uninstall_skill() {
    print_info "Uninstalling Quotefix skill..."
    echo ""

    if [ ! -d "$TARGET_DIR" ]; then
        print_warning "Skill is not installed at $TARGET_DIR"
        exit 0
    fi

    rm -rf "$TARGET_DIR"
    print_success "Removed skill from $TARGET_DIR"
    echo ""
    print_success "Uninstallation complete!"
}

# Main execution
if [ "$1" = "--uninstall" ]; then
    uninstall_skill
else
    install_skill
fi
