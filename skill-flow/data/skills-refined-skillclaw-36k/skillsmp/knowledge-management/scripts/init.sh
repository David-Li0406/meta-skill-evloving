#!/bin/bash
# Knowledge Management System - Init Script
# Usage: ./init.sh [project-root]

set -e

# Validate path to prevent path traversal attacks
validate_path() {
    local path="$1"

    # Reject paths containing .. (path traversal)
    if [[ "$path" == *".."* ]]; then
        echo "❌ Error: Path cannot contain '..'" >&2
        exit 1
    fi

    # Resolve to absolute path
    local resolved_path
    resolved_path=$(cd "$path" 2>/dev/null && pwd) || {
        # If directory doesn't exist, check parent
        local parent_dir=$(dirname "$path")
        if [ "$parent_dir" != "." ] && [ "$parent_dir" != "/" ]; then
            resolved_path=$(cd "$parent_dir" 2>/dev/null && pwd)/$(basename "$path") || {
                echo "❌ Error: Invalid path '$path'" >&2
                exit 1
            }
        else
            resolved_path="$path"
        fi
    }

    echo "$resolved_path"
}

RAW_PROJECT_ROOT="${1:-.}"
PROJECT_ROOT=$(validate_path "$RAW_PROJECT_ROOT")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Initializing Knowledge Management System..."
echo "   Project: $PROJECT_ROOT"
echo ""

# Create directories
echo "📁 Creating directories..."
mkdir -p "$PROJECT_ROOT/docs/learnings"
mkdir -p "$PROJECT_ROOT/docs/knowledge-base"
mkdir -p "$PROJECT_ROOT/docs/retrospective"
mkdir -p "$PROJECT_ROOT/docs/auto-captured"
mkdir -p "$PROJECT_ROOT/.claude/commands"
mkdir -p "$PROJECT_ROOT/.claude/scripts"
mkdir -p "$PROJECT_ROOT/.claude/agents"

# Copy command files from assets (all .md files except README.md)
echo "📄 Copying command files..."
if [ -d "$SKILL_ROOT/assets/commands" ]; then
    for file in "$SKILL_ROOT/assets/commands"/*.md; do
        filename=$(basename "$file")
        if [ "$filename" != "README.md" ]; then
            cp "$file" "$PROJECT_ROOT/.claude/commands/"
            echo "   - $filename"
        fi
    done
fi

# Copy scripts
echo "📜 Copying scripts..."
if [ -f "$SKILL_ROOT/scripts/notify.sh" ]; then
    cp "$SKILL_ROOT/scripts/notify.sh" "$PROJECT_ROOT/.claude/scripts/"
    chmod +x "$PROJECT_ROOT/.claude/scripts/notify.sh"
    echo "   - notify.sh"
fi

# Copy hooks.json example
echo "🔗 Copying hooks example..."
if [ -f "$SKILL_ROOT/hooks.json" ]; then
    cp "$SKILL_ROOT/hooks.json" "$PROJECT_ROOT/.claude/hooks.example.json"
    echo "   - hooks.example.json"
fi

# Copy agent files
echo "🤖 Copying agents..."
if [ -d "$SKILL_ROOT/assets/agents" ]; then
    for file in "$SKILL_ROOT/assets/agents"/*.md; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            cp "$file" "$PROJECT_ROOT/.claude/agents/"
            echo "   - $filename"
        fi
    done
fi

# Create .gitkeep files
touch "$PROJECT_ROOT/docs/learnings/.gitkeep"
touch "$PROJECT_ROOT/docs/knowledge-base/.gitkeep"
touch "$PROJECT_ROOT/docs/retrospective/.gitkeep"
touch "$PROJECT_ROOT/docs/auto-captured/.gitkeep"

echo ""
echo "✅ Knowledge Management System initialized!"
echo ""
echo "📂 Structure created:"
echo "   $PROJECT_ROOT/"
echo "   ├── .claude/"
echo "   │   ├── commands/        (slash commands)"
echo "   │   ├── agents/          (subagents)"
echo "   │   ├── scripts/         (notify.sh)"
echo "   │   └── hooks.example.json"
echo "   └── docs/"
echo "       ├── learnings/"
echo "       ├── knowledge-base/"
echo "       ├── retrospective/"
echo "       └── auto-captured/"
echo ""
echo "📝 Next steps:"
echo "   1. Add to git: git add .claude/ docs/"
echo "   2. Commit: git commit -m 'feat: add Knowledge Management System'"
echo "   3. (Optional) Enable notifications:"
echo "      - Copy hooks.example.json to settings.json"
echo "      - Update script paths to match your project"
echo ""
echo "🎯 Commands:"
echo "   /mem [topic]     - Quick knowledge capture"
echo "   /distill [topic] - Extract patterns"
echo "   /td              - Post-task retrospective"
echo "   /improve         - Work on pending items"
echo ""
echo "🔔 Notifications:"
echo "   notify.sh sends macOS notifications when Claude needs attention"
echo ""
echo "🤖 Subagents:"
echo "   code-reviewer     - Review code for bugs, security, performance"
echo "   code-simplifier   - Simplify code after writing"
echo "   security-auditor  - Security vulnerability audit"
echo "   knowledge-curator - Suggest topics to distill"
echo "   session-analyzer  - Create retrospective drafts"
echo "   build-validator   - Validate build, tests, lint"
