#!/bin/bash
# post-comments.sh - Post generated comments to Linear issue
#
# Usage:
#   post-comments.sh <issue-id> <analysis-file> <agent-prompt-file> [--workspace WORKSPACE]
#
# Posts two comments:
#   1. Analysis + Diagrams (human-readable)
#   2. Agent Prompt (structured XML)

set -e

ISSUE_ID="$1"
ANALYSIS_FILE="$2"
AGENT_PROMPT_FILE="$3"
WORKSPACE=""

# Parse remaining arguments
shift 3 || true
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

if [[ -z "$ISSUE_ID" || -z "$ANALYSIS_FILE" || -z "$AGENT_PROMPT_FILE" ]]; then
    echo "Usage: post-comments.sh <issue-id> <analysis-file> <agent-prompt-file> [--workspace WORKSPACE]"
    echo ""
    echo "Examples:"
    echo "  post-comments.sh ARB-123 analysis.md agent-prompt.md"
    echo "  post-comments.sh SIP-364 /tmp/analysis.md /tmp/prompt.md --workspace spottedinprod"
    exit 1
fi

# Validate files exist
if [[ ! -f "$ANALYSIS_FILE" ]]; then
    echo "ERROR: Analysis file not found: $ANALYSIS_FILE"
    exit 1
fi

if [[ ! -f "$AGENT_PROMPT_FILE" ]]; then
    echo "ERROR: Agent prompt file not found: $AGENT_PROMPT_FILE"
    exit 1
fi

echo "=== Posting Comments to $ISSUE_ID ==="
echo ""

# Post analysis comment
echo "Posting Analysis + Diagrams..."
ANALYSIS_BODY=$(cat "$ANALYSIS_FILE")
if linear comment create -i "$ISSUE_ID" -b "$ANALYSIS_BODY" $WORKSPACE; then
    echo "  Success: Analysis comment posted"
else
    echo "  ERROR: Failed to post analysis comment"
    exit 1
fi

echo ""

# Post agent prompt comment
echo "Posting Agent Prompt..."
AGENT_BODY=$(cat "$AGENT_PROMPT_FILE")
if linear comment create -i "$ISSUE_ID" -b "$AGENT_BODY" $WORKSPACE; then
    echo "  Success: Agent prompt posted"
else
    echo "  ERROR: Failed to post agent prompt"
    exit 1
fi

echo ""
echo "=== Done ==="
echo "Posted 2 comments to $ISSUE_ID"
echo ""
echo "Verify: linear comment list $ISSUE_ID $WORKSPACE"
