#!/bin/bash
# audit-issue.sh - Fetch Linear issue and detect context
#
# Usage:
#   audit-issue.sh <issue-id> [--workspace WORKSPACE]
#
# Output:
#   - Issue details (title, description, state)
#   - Existing comments count
#   - Repo context detection

set -e

ISSUE_ID="$1"
WORKSPACE=""

# Parse arguments
shift || true
while [[ $# -gt 0 ]]; do
    case $1 in
        --workspace)
            WORKSPACE="--workspace $2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

if [[ -z "$ISSUE_ID" ]]; then
    echo "Usage: audit-issue.sh <issue-id> [--workspace WORKSPACE]"
    echo ""
    echo "Examples:"
    echo "  audit-issue.sh ARB-123"
    echo "  audit-issue.sh SIP-364 --workspace spottedinprod"
    exit 1
fi

echo "=== Issue Audit: $ISSUE_ID ==="
echo ""

# Fetch issue details
echo "## Issue Details"
linear issue view "$ISSUE_ID" $WORKSPACE
echo ""

# Check existing comments
echo "## Existing Comments"
COMMENT_COUNT=$(linear comment list "$ISSUE_ID" $WORKSPACE --json 2>/dev/null | jq 'length' || echo "0")
echo "Comments: $COMMENT_COUNT"
if [[ "$COMMENT_COUNT" -gt 0 ]]; then
    echo ""
    echo "Latest comments:"
    linear comment list "$ISSUE_ID" $WORKSPACE --json | jq -r '.[-3:] | .[] | "- \(.body | split("\n")[0])"' 2>/dev/null || true
fi
echo ""

# Detect repo context
echo "## Repo Context"
if [[ -d "apps" ]] || [[ -d "packages" ]]; then
    echo "Type: Monorepo"
    echo "Apps: $(ls -d apps/* 2>/dev/null | wc -l | tr -d ' ')"
    echo "Packages: $(ls -d packages/* 2>/dev/null | wc -l | tr -d ' ')"
else
    echo "Type: Single package"
fi

if [[ -f "convex.json" ]] || [[ -d "convex" ]]; then
    echo "Backend: Convex"
fi

if [[ -f "next.config.js" ]] || [[ -f "next.config.mjs" ]]; then
    echo "Frontend: Next.js"
fi

echo ""
echo "## Git Status"
git log --oneline -5 2>/dev/null || echo "Not in git repo"
