#!/bin/bash
# Claude Code Wrapper with Auto-Capture
# Wraps the claude command and offers auto-capture after session ends
#
# Usage:
#   ./claude-wrap.sh [claude-args...]
#
# Installation:
#   # Add alias to ~/.bashrc or ~/.zshrc
#   alias claude='~/.claude/skills/knowledge-management/scripts/claude-wrap.sh'
#
# Options (via environment variables):
#   CLAUDE_AUTO_CAPTURE=always    - Always auto-capture (skip prompt)
#   CLAUDE_AUTO_CAPTURE=never     - Never auto-capture
#   CLAUDE_AUTO_CAPTURE=ai        - Use AI-powered capture
#   CLAUDE_MIN_FILES=3            - Minimum files for auto-capture

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TZ='Asia/Bangkok'
export TZ

# Configuration
MIN_FILES="${CLAUDE_MIN_FILES:-3}"
AUTO_MODE="${CLAUDE_AUTO_CAPTURE:-ask}"

# Find the real claude command
CLAUDE_BIN=$(which claude 2>/dev/null || echo "")

# Check if we're calling ourselves recursively
if [ -z "$CLAUDE_BIN" ] || [ "$CLAUDE_BIN" = "$0" ]; then
    # Try common locations
    if [ -x "/usr/local/bin/claude" ]; then
        CLAUDE_BIN="/usr/local/bin/claude"
    elif [ -x "$HOME/.local/bin/claude" ]; then
        CLAUDE_BIN="$HOME/.local/bin/claude"
    elif [ -x "$HOME/.npm/bin/claude" ]; then
        CLAUDE_BIN="$HOME/.npm/bin/claude"
    else
        echo "❌ Error: claude command not found"
        echo "Please ensure Claude Code CLI is installed"
        exit 1
    fi
fi

# Store start time
START_TIME=$(date '+%Y-%m-%d %H:%M:%S')
START_EPOCH=$(date '+%s')

# Run claude with all arguments
"$CLAUDE_BIN" "$@"
EXIT_CODE=$?

# Calculate session duration
END_EPOCH=$(date '+%s')
DURATION=$((END_EPOCH - START_EPOCH))
DURATION_MIN=$((DURATION / 60))
DURATION_SEC=$((DURATION % 60))

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Session Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   Started: $START_TIME"
echo "   Duration: ${DURATION_MIN}m ${DURATION_SEC}s"

# Check git status
if git rev-parse --git-dir > /dev/null 2>&1; then
    CHANGED=$(git diff --name-only HEAD 2>/dev/null | wc -l | tr -d ' ')
    STAGED=$(git diff --cached --name-only 2>/dev/null | wc -l | tr -d ' ')
    UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null | wc -l | tr -d ' ')
    TOTAL=$((CHANGED + STAGED + UNTRACKED))

    echo "   Files changed: $TOTAL"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Check if we should auto-capture
    if [ "$TOTAL" -ge "$MIN_FILES" ]; then
        case "$AUTO_MODE" in
            always)
                echo ""
                echo "🔄 Auto-capturing session..."
                "$SCRIPT_DIR/auto-capture.sh" . --force
                ;;
            ai)
                echo ""
                echo "🤖 AI-capturing session..."
                "$SCRIPT_DIR/ai-capture.sh" . --force
                ;;
            never)
                echo ""
                echo "💡 Tip: $TOTAL files changed. Run ./scripts/auto-capture.sh to capture."
                ;;
            *)
                # Ask user
                echo ""
                echo "❓ Auto-capture this session? ($TOTAL files changed)"
                echo ""
                echo "   [1] Basic capture (quick)"
                echo "   [2] AI-powered capture (detailed, requires API key)"
                echo "   [n] Skip"
                echo ""
                read -r -p "Choice [1/2/n]: " choice

                case "$choice" in
                    1|y|Y|yes|YES)
                        "$SCRIPT_DIR/auto-capture.sh" . --force
                        ;;
                    2|ai|AI)
                        "$SCRIPT_DIR/ai-capture.sh" . --force
                        ;;
                    *)
                        echo "⏭️  Skipped auto-capture"
                        ;;
                esac
                ;;
        esac
    else
        echo ""
        echo "💡 Only $TOTAL files changed (min: $MIN_FILES for auto-capture)"
    fi
else
    echo "   (Not a git repository)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fi

exit $EXIT_CODE
