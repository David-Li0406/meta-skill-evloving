#!/bin/bash
# Show GitLab project context for ticket creation sessions
# Usage: ./context.sh

echo "=== GitLab Project Context ==="
echo ""

echo "## Repository"
glab repo view 2>/dev/null | head -5
echo ""

echo "## Labels"
glab label list 2>/dev/null || echo "No labels found"
echo ""

echo "## Recent Issues (last 10)"
glab issue list --per-page 10 2>/dev/null || echo "No open issues"
echo ""

echo "## Auth Status"
glab auth status 2>&1 | head -3
