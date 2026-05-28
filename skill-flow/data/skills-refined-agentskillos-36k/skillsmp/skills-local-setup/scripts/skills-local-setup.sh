#!/bin/bash

# Skills Local Setup - Create symlinks for AI tools in the current repository
# Usage: ./skills-local-setup.sh [gemini|claude|agent|opencode|all]
#
# Source of truth: .claude/ directory
# Symlinks: .agent/, .opencode/ -> .claude/ (compatibility)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in a git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 1
fi

REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

# Function to add entry to .gitignore if not present
add_to_gitignore() {
    local entry="$1"
    if [ ! -f .gitignore ]; then
        echo "# AI tool symlinks" > .gitignore
    fi
    if ! grep -q "^${entry}$" .gitignore 2>/dev/null; then
        # Ensure file ends with newline before appending
        if [ -s .gitignore ] && [ "$(tail -c1 .gitignore | wc -l)" -eq 0 ]; then
            echo "" >> .gitignore
        fi
        echo "$entry" >> .gitignore
        echo -e "${GREEN}✓${NC} Added '$entry' to .gitignore"
    else
        echo -e "${YELLOW}ℹ${NC} '$entry' already in .gitignore"
    fi
}

# Function to create symlink safely
create_symlink() {
    local source="$1"
    local target="$2"
    local gitignore_entry="$3"

    if [ -L "$target" ]; then
        echo -e "${YELLOW}ℹ${NC} Symlink already exists: $target -> $(readlink "$target")"
    elif [ -e "$target" ]; then
        echo -e "${RED}⚠${NC} $target exists but is not a symlink."
        echo ""
        echo "📁 Current contents:"
        if [ -d "$target" ]; then
            ls -la "$target" 2>/dev/null | head -20
            ITEM_COUNT=$(find "$target" -mindepth 1 2>/dev/null | wc -l | tr -d ' ')
            echo ""
            if [ "$ITEM_COUNT" -gt 0 ]; then
                echo -e "${RED}⚠  This folder contains $ITEM_COUNT item(s) that will be DELETED.${NC}"
            else
                echo -e "${YELLOW}ℹ${NC} This folder is empty."
            fi
        else
            ls -la "$target" 2>/dev/null
            echo ""
            echo -e "${RED}⚠  This file will be DELETED.${NC}"
        fi
        echo ""

        read -p "Do you want to remove $target and create the symlink? [y/N] " -n 1 -r
        echo ""

        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "🗑️  Removing $target..."
            rm -rf "$target"
            ln -s "$source" "$target"
            echo -e "${GREEN}✓${NC} Created: $target -> $source"
        else
            echo -e "${YELLOW}ℹ${NC} Skipped $target (kept existing content)"
            add_to_gitignore "$gitignore_entry"
            return 0
        fi
    else
        ln -s "$source" "$target"
        echo -e "${GREEN}✓${NC} Created: $target -> $source"
    fi

    add_to_gitignore "$gitignore_entry"
}

# Setup Gemini
setup_gemini() {
    echo ""
    echo "🔷 Setting up Gemini..."

    if [ ! -f AGENTS.md ]; then
        echo -e "${YELLOW}ℹ${NC} AGENTS.md not found in repo root."
        echo ""
        echo "📋 AGENT INSTRUCTION: Please use the 'skills-index-updater' skill to create AGENTS.md first."
        echo "   Run: /skills-index-updater"
        echo "   Then re-run this setup script."
        echo ""
        return 1
    fi

    # Create GEMINI.md with directive to load AGENTS.md
    if [ -f GEMINI.md ]; then
        echo -e "${YELLOW}ℹ${NC} GEMINI.md already exists"
        cat GEMINI.md
    else
        echo "Load always AGENTS.md to read your system instructions." > GEMINI.md
        echo -e "${GREEN}✓${NC} Created GEMINI.md with AGENTS.md directive"
    fi

    add_to_gitignore "GEMINI.md"
}

# Ensure .claude/skills exists (source of truth - NOT added to gitignore)
ensure_claude_skills() {
    if [ ! -d .claude/skills ]; then
        echo -e "${YELLOW}ℹ${NC} Creating .claude/skills/ directory..."
        mkdir -p .claude/skills
        echo -e "${GREEN}✓${NC} Created .claude/skills/"
    fi

    # Migrate settings if needed
    if [ ! -f .claude/settings.json ] && [ -f .agent/settings.json ]; then
        echo -e "${YELLOW}ℹ${NC} Found .agent/settings.json, migrating to .claude/settings.json..."
        cp .agent/settings.json .claude/settings.json
        echo -e "${GREEN}✓${NC} Copied settings to .claude/settings.json"
    fi
}

# Setup Agent backward compatibility (.agent/ symlinks to .claude/)
setup_agent() {
    echo ""
    echo "🔗 Setting up .agent/ backward compatibility..."

    # Ensure .claude/skills exists first
    ensure_claude_skills

    # Create .agent directory if needed
    mkdir -p .agent

    # Skills symlink: .agent/skills -> .claude/skills
    create_symlink "../.claude/skills" ".agent/skills" ".agent/"

    # Settings symlink: .agent/settings.json -> .claude/settings.json
    if [ -f .claude/settings.json ]; then
        create_symlink "../.claude/settings.json" ".agent/settings.json" ".agent/"
    else
        echo -e "${YELLOW}ℹ${NC} No .claude/settings.json found, skipping settings symlink"
    fi

    # Ensure .agent/ is in gitignore
    add_to_gitignore ".agent/"
}

# Setup OpenCode compatibility (.opencode/skill/ singular -> .claude/skills/)
setup_opencode() {
    echo ""
    echo "🟢 Setting up OpenCode compatibility..."

    # Ensure .claude/skills exists first
    ensure_claude_skills

    # Create .opencode directory if needed
    mkdir -p .opencode

    # Skills symlink: .opencode/skill (singular!) -> .claude/skills
    create_symlink "../.claude/skills" ".opencode/skill" ".opencode/"

    # Ensure .opencode/ is in gitignore
    add_to_gitignore ".opencode/"
}

# Show usage
show_usage() {
    echo "Usage: $0 [agent|opencode|gemini|all]"
    echo ""
    echo "Options:"
    echo "  agent    - Create .agent/ symlinks to .claude/ (backward compat)"
    echo "  opencode - Create .opencode/skill/ symlink to .claude/skills/"
    echo "  gemini   - Create GEMINI.md with directive to load AGENTS.md"
    echo "  all      - Setup all compatibility layers (agent + opencode + gemini)"
    echo ""
    echo "Directory structure:"
    echo "  .claude/skills/   <- SOURCE (tracked in git)"
    echo "  .agent/skills/    -> symlink to .claude/skills/ (gitignored)"
    echo "  .opencode/skill/  -> symlink to .claude/skills/ (gitignored, singular!)"
    echo "  GEMINI.md         <- directive file (gitignored)"
    echo ""
    echo "Examples:"
    echo "  $0 agent         # Add .agent/ backward compat symlinks"
    echo "  $0 opencode      # Add OpenCode compatibility"
    echo "  $0 all           # Setup everything"
}

# Main
case "${1:-}" in
    agent)
        setup_agent
        ;;
    opencode)
        setup_opencode
        ;;
    gemini)
        setup_gemini
        ;;
    all)
        setup_agent
        setup_opencode
        setup_gemini
        ;;
    -h|--help|"")
        show_usage
        exit 0
        ;;
    *)
        echo -e "${RED}Unknown option: $1${NC}"
        show_usage
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Verify with:"
echo "  ls -la .claude/ .agent/ .opencode/ GEMINI.md 2>/dev/null"
echo "  git status"
