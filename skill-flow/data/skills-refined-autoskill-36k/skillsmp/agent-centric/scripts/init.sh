#!/usr/bin/env bash
#
# Initialize .agents/ directory structure for Agent Centric framework.
#
# Usage:
#     CLAUDE_PROJECT_DIR="..." CLAUDE_SKILL_DIR="..." bash init.sh
#
# This script:
#   1. Creates .agents/ directory structure
#   2. Copies scripts from skill directory
#   3. Creates config.json
#   4. Creates .agents/CLAUDE.md
#   5. Adds reference to project's root CLAUDE.md
#   6. Creates empty index files
#

set -e

# Require environment variables
if [ -z "$CLAUDE_PROJECT_DIR" ]; then
    echo "Error: CLAUDE_PROJECT_DIR not set" >&2
    exit 1
fi
if [ -z "$CLAUDE_SKILL_DIR" ]; then
    echo "Error: CLAUDE_SKILL_DIR not set" >&2
    exit 1
fi

PROJECT_DIR="$CLAUDE_PROJECT_DIR"
SKILL_DIR="$CLAUDE_SKILL_DIR"
AGENTS_DIR="$PROJECT_DIR/.agents"

echo "Initializing .agents/ directory in $PROJECT_DIR..."

# Create directory structure
mkdir -p "$AGENTS_DIR/decisions"
mkdir -p "$AGENTS_DIR/scripts"

# Create .gitkeep for empty decisions directory
touch "$AGENTS_DIR/decisions/.gitkeep"

# Create config.json if not exists (before sync, so sync can check disableAutoUpdateScripts)
if [ ! -f "$AGENTS_DIR/config.json" ]; then
    cat > "$AGENTS_DIR/config.json" << 'EOF'
{
  "tags": [],
  "disableAutoUpdateScripts": []
}
EOF
    echo "Created config.json"
fi

# Sync scripts, templates, CLAUDE.md, and .gitignore
bash "$SKILL_DIR/scripts/sync-scripts.sh"

# Create empty index files
for INDEX_FILE in INDEX-TAGS.md INDEX-AGD-RELATIONS.md; do
    if [ ! -f "$AGENTS_DIR/$INDEX_FILE" ]; then
        touch "$AGENTS_DIR/$INDEX_FILE"
    fi
done

# Run generate-index to create proper index headers
CLAUDE_PROJECT_DIR="$PROJECT_DIR" "$AGENTS_DIR/scripts/generate-index.py"
echo "Generated index files"

# Add reference to project's root CLAUDE.md
ROOT_CLAUDE_MD="$PROJECT_DIR/CLAUDE.md"
AGENTS_REF="See [.agents/CLAUDE.md](.agents/CLAUDE.md) for the Agent Centric framework."

if [ -f "$ROOT_CLAUDE_MD" ]; then
    if ! grep -q ".agents/CLAUDE.md" "$ROOT_CLAUDE_MD"; then
        echo "" >> "$ROOT_CLAUDE_MD"
        echo "$AGENTS_REF" >> "$ROOT_CLAUDE_MD"
        echo "Added reference to root CLAUDE.md"
    else
        echo "Reference already exists in root CLAUDE.md"
    fi
else
    echo "$AGENTS_REF" > "$ROOT_CLAUDE_MD"
    echo "Created root CLAUDE.md with reference"
fi

echo ""
echo "Initialization complete!"
echo ""
echo "Next steps:"
echo "  1. Add tags to .agents/config.json tags array"
echo "  2. Start creating AGD files in .agents/decisions/"
