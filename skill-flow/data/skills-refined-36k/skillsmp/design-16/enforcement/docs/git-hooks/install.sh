#!/bin/bash
# install.sh - Set up git hooks for invariant validation
#
# Usage:
#   ./enforcement/docs/git-hooks/install.sh
#
# This script:
# - Copies pre-commit and pre-push hooks to .git/hooks/
# - Makes them executable
# - Backs up existing hooks (if any)
# - Works from any directory in the repo

set -e

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}=========================================="
echo -e "  Git Hooks Installer"
echo -e "==========================================${NC}"
echo ""

# Find repo root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 1
fi

# Determine script location (may be called from anywhere)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_SOURCE="$SCRIPT_DIR"

# Fallback: try standard location relative to repo root
if [ ! -f "$HOOKS_SOURCE/pre-commit" ]; then
    HOOKS_SOURCE="$REPO_ROOT/enforcement/docs/git-hooks"
fi

if [ ! -f "$HOOKS_SOURCE/pre-commit" ]; then
    echo -e "${RED}Error: Cannot find hook source files${NC}"
    echo "Expected at: $HOOKS_SOURCE/pre-commit"
    exit 1
fi

HOOKS_DIR="$REPO_ROOT/.git/hooks"

# Ensure hooks directory exists
mkdir -p "$HOOKS_DIR"

# Install function
install_hook() {
    local hook_name="$1"
    local source="$HOOKS_SOURCE/$hook_name"
    local dest="$HOOKS_DIR/$hook_name"

    if [ ! -f "$source" ]; then
        echo -e "${YELLOW}Skipping $hook_name (source not found)${NC}"
        return
    fi

    # Backup existing hook if it exists and isn't ours
    if [ -f "$dest" ]; then
        if grep -q "invariant" "$dest" 2>/dev/null; then
            echo -e "  ${BLUE}$hook_name${NC}: Updating existing invariant hook"
        else
            local backup="$dest.backup.$(date +%Y%m%d%H%M%S)"
            cp "$dest" "$backup"
            echo -e "  ${YELLOW}$hook_name${NC}: Backed up existing hook to $(basename $backup)"
        fi
    fi

    # Copy and make executable
    cp "$source" "$dest"
    chmod +x "$dest"
    echo -e "  ${GREEN}$hook_name${NC}: Installed"
}

echo "Installing hooks to: $HOOKS_DIR"
echo ""

install_hook "pre-commit"
install_hook "pre-push"

echo ""
echo -e "${GREEN}Installation complete!${NC}"
echo ""
echo "Hooks installed:"
echo "  - pre-commit: Validates staged spec files before commit"
echo "  - pre-push: Validates all changed specs before push"
echo ""
echo "To test:"
echo "  1. Modify a spec file in specs/ or prp/"
echo "  2. Run: git add <file> && git commit -m 'test'"
echo ""
echo "To bypass hooks (emergency):"
echo "  git commit --no-verify"
echo "  git push --no-verify"
echo ""
echo "To uninstall:"
echo "  rm $HOOKS_DIR/pre-commit $HOOKS_DIR/pre-push"
echo ""
