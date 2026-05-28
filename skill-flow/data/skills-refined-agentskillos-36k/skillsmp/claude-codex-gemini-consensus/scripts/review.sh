#!/bin/bash
# =============================================================================
# Consensus Review Wrapper Script
# =============================================================================
# GUARANTEED REVIEWER_MODE injection for all agent invocations.
# Use this script instead of calling agents directly to prevent infinite loops.
#
# Usage:
#   ./review.sh codex "Your review prompt here"
#   ./review.sh gemini "Your review prompt here"
#   ./review.sh claude "Your review prompt here"
#
# The script automatically prepends REVIEWER_MODE constraints to every prompt.
# =============================================================================

set -euo pipefail

REVIEWER_HEADER='REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS (claude, codex, gemini).
You MAY read files, web search, and run sanity checks. Provide YOUR expert review only.

'

usage() {
    echo "Usage: $0 <agent> <prompt> [options]"
    echo ""
    echo "Agents:"
    echo "  codex   - Invoke OpenAI Codex CLI"
    echo "  gemini  - Invoke Google Gemini CLI"
    echo "  claude  - Invoke Anthropic Claude CLI"
    echo ""
    echo "Options:"
    echo "  --search    Enable web search (codex/gemini)"
    echo "  --cd PATH   Change working directory"
    echo ""
    echo "Examples:"
    echo "  $0 codex 'Review this code for bugs: \$(cat main.py)'"
    echo "  $0 gemini 'Validate this analysis plan' --search"
    echo "  $0 claude 'Check for security issues in auth.py'"
    exit 1
}

if [[ $# -lt 2 ]]; then
    usage
fi

AGENT="$1"
PROMPT="$2"
shift 2

# Parse optional arguments
SEARCH_FLAG=""
CD_PATH=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --search)
            SEARCH_FLAG="--search"
            shift
            ;;
        --cd)
            CD_PATH="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Prepend REVIEWER_MODE header to prompt (GUARANTEED)
FULL_PROMPT="${REVIEWER_HEADER}${PROMPT}"

case "$AGENT" in
    codex)
        CMD="codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check"
        [[ -n "$SEARCH_FLAG" ]] && CMD="$CMD --search"
        [[ -n "$CD_PATH" ]] && CMD="$CMD --cd \"$CD_PATH\""
        eval "$CMD \"$FULL_PROMPT\""
        ;;
    gemini)
        CMD="gemini --yolo"
        # Gemini has built-in web search, no flag needed
        eval "$CMD -p \"$FULL_PROMPT\""
        ;;
    claude)
        CMD="claude --dangerously-skip-permissions"
        eval "$CMD -p \"$FULL_PROMPT\""
        ;;
    *)
        echo "Error: Unknown agent '$AGENT'"
        echo "Valid agents: codex, gemini, claude"
        exit 1
        ;;
esac
