#!/bin/bash
# Interactive setup script for Claude Code rules
# Helps users symlink rules from rbw-claude-code to their project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Determine the path to rbw-claude-code templates
if [ -n "$CLAUDE_PLUGIN_ROOT" ]; then
    # Running from within Claude Code
    SCRIPT_DIR="$(dirname "$0")"
    RBW_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
else
    # Try common locations
    if [ -d "${HOME}/.claude/plugins/marketplaces/rbw-claude-code" ]; then
        RBW_ROOT="${HOME}/.claude/plugins/marketplaces/rbw-claude-code"
    elif [ -d "${HOME}/repo/rbw-claude-code" ]; then
        RBW_ROOT="${HOME}/repo/rbw-claude-code"
    else
        echo -e "${RED}Error: Could not find rbw-claude-code directory${NC}"
        echo "Please set RBW_CLAUDE_CODE environment variable to the path"
        exit 1
    fi
fi

TEMPLATES_DIR="${RBW_ROOT}/templates/rules"
PYTHON_RULES_DIR="${TEMPLATES_DIR}/python"

# Target directory (current project)
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
RULES_DIR="${PROJECT_DIR}/.claude/rules"

echo -e "${BLUE}=== Claude Code Rules Setup ===${NC}"
echo ""
echo "Source: ${TEMPLATES_DIR}"
echo "Target: ${RULES_DIR}"
echo ""

# Check if templates exist
if [ ! -d "$PYTHON_RULES_DIR" ]; then
    echo -e "${RED}Error: Python rules not found at ${PYTHON_RULES_DIR}${NC}"
    exit 1
fi

# Create rules directory
mkdir -p "$RULES_DIR"

# Function to create symlink
create_link() {
    local source="$1"
    local name=$(basename "$source")
    local target="${RULES_DIR}/${name}"

    # Verify source exists
    if [ ! -f "$source" ]; then
        echo -e "${RED}  Error: Source not found: ${source}${NC}"
        return 1
    fi

    if [ -L "$target" ]; then
        echo -e "${YELLOW}  Replacing existing symlink: ${name}${NC}"
        rm "$target"
    elif [ -f "$target" ]; then
        echo -e "${YELLOW}  Skipping (file exists): ${name}${NC}"
        return
    fi

    ln -s "$source" "$target"
    echo -e "${GREEN}  Linked: ${name}${NC}"
}

# Menu
echo "Which rules would you like to install?"
echo ""
echo "  1) All Python rules (asyncio, typing, architecture, testing, prohibited)"
echo "  2) Python rules + anti-slop"
echo "  3) Just anti-slop"
echo "  4) Select individual rules"
echo "  5) Cancel"
echo ""
read -p "Choose [1-5]: " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}Installing Python rules...${NC}"
        for rule in asyncio typing architecture testing prohibited; do
            create_link "${PYTHON_RULES_DIR}/${rule}.md"
        done
        ;;
    2)
        echo ""
        echo -e "${BLUE}Installing Python rules + anti-slop...${NC}"
        for rule in asyncio typing architecture testing prohibited; do
            create_link "${PYTHON_RULES_DIR}/${rule}.md"
        done
        create_link "${TEMPLATES_DIR}/anti-slop.md"
        ;;
    3)
        echo ""
        echo -e "${BLUE}Installing anti-slop...${NC}"
        create_link "${TEMPLATES_DIR}/anti-slop.md"
        ;;
    4)
        echo ""
        echo "Select rules to install (y/n for each):"
        echo ""

        for rule in asyncio typing architecture testing prohibited; do
            read -p "  Python/${rule}.md? [y/N]: " yn
            if [[ $yn =~ ^[Yy]$ ]]; then
                create_link "${PYTHON_RULES_DIR}/${rule}.md"
            fi
        done

        read -p "  anti-slop.md? [y/N]: " yn
        if [[ $yn =~ ^[Yy]$ ]]; then
            create_link "${TEMPLATES_DIR}/anti-slop.md"
        fi
        ;;
    5)
        echo "Cancelled."
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Done!${NC} Rules installed at: ${RULES_DIR}"
echo ""
echo "Verify with: ls -la ${RULES_DIR}"
