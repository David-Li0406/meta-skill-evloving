#!/bin/bash
# Quick Session Status Check
#
# Shows current session info and requirement status.
# Usage: ./check-session.sh

set -e

echo "🔍 Requirements Framework Session Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if req command is available
if ! command -v req &> /dev/null; then
    # Try alias
    if [ -f "$HOME/.claude/hooks/requirements-cli.py" ]; then
        REQ="python3 $HOME/.claude/hooks/requirements-cli.py"
    else
        echo "❌ req command not found"
        echo "Install: ./install.sh in requirements-framework repo"
        exit 1
    fi
else
    REQ="req"
fi

# Show active sessions
echo "📋 Active Sessions:"
echo ""
$REQ sessions 2>/dev/null || echo "   (No sessions found or error occurred)"
echo ""

# Show requirement status
echo "📊 Requirement Status:"
echo ""
$REQ status 2>/dev/null || echo "   (Unable to get status)"
echo ""

# Quick health check
echo "🏥 Quick Health Check:"
echo ""

# Check config exists
if [ -f ".claude/requirements.yaml" ]; then
    echo "   ✓ Project config: .claude/requirements.yaml"
else
    echo "   ℹ️  No project config (using global/defaults)"
fi

if [ -f "$HOME/.claude/requirements.yaml" ]; then
    echo "   ✓ Global config: ~/.claude/requirements.yaml"
fi

# Check hooks directory
if [ -d "$HOME/.claude/hooks" ]; then
    echo "   ✓ Hooks directory exists"
else
    echo "   ✗ Hooks directory missing"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 Commands:"
echo "   req satisfy <name>  - Satisfy requirement"
echo "   req clear <name>    - Clear requirement"
echo "   req doctor          - Full diagnostics"
