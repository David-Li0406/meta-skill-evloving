#!/bin/bash
# Sync Status Check
#
# Wrapper for sync.sh status with additional context.
# Usage: ./sync-status.sh

set -e

REPO_DIR="$HOME/Tools/claude-requirements-framework"

if [ ! -d "$REPO_DIR" ]; then
    echo "❌ Repository not found: $REPO_DIR"
    exit 1
fi

cd "$REPO_DIR"

echo "📊 Requirements Framework Sync Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Repository: $REPO_DIR"
echo "Deployed:   $HOME/.claude/hooks/"
echo ""

# Run sync status
./sync.sh status

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 Commands:"
echo "   ./sync.sh deploy  - Deploy repo → hooks"
echo "   ./sync.sh diff    - Show differences"
