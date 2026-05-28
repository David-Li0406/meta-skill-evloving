#!/bin/bash
#
# Quick Lore Generator
# Creates a lore entry with LLM-generated content and links it
#
# Usage: ./quick-lore.sh "What happened" [persona_id]
#
# Example:
#   ./quick-lore.sh "Fixed the authentication bug that was blocking login"
#   ./quick-lore.sh "Implemented dark mode" persona_1744992765

set -e

LORE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}"/../../..)" && pwd)"
DESCRIPTION="${1:-}"
PERSONA_ID="${2:-persona_1763820091}"  # Default: Village Elder

if [ -z "$DESCRIPTION" ]; then
    echo "Usage: $0 \"What happened\" [persona_id]"
    echo ""
    echo "Examples:"
    echo "  $0 \"Fixed critical bug in auth system\""
    echo "  $0 \"Added new feature\" persona_1744992765"
    exit 1
fi

echo "=== Quick Lore Generator ==="
echo "Input: $DESCRIPTION"
echo "Persona: $PERSONA_ID"
echo ""

# Use the lore-flow pipeline
export LLM_PROVIDER="${LLM_PROVIDER:-claude}"
"$LORE_DIR/integration/lore-flow.sh" manual "$DESCRIPTION"

echo ""
echo "Done! Check the output above for entry ID."
