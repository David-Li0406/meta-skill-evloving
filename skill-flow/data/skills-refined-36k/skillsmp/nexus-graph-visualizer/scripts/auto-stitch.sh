#!/usr/bin/env bash

# auto-stitch.sh — Given a concept/pattern, return what else to load
# Part of nexus-graph-visualizer (e.5.3.1)
#
# Usage: ./auto-stitch.sh <concept_name_or_dewey_id>
# Returns: List of related files to load for full context

set -euo pipefail

GRAPH_DIR="${GRAPH_DIR:-/tmp/nexus-graph}"
ADJACENCY_FILE="$GRAPH_DIR/adjacency.txt"
PARSED_FILE="$GRAPH_DIR/parsed.txt"

# Colors
if [[ -t 1 ]]; then
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    GREEN='' YELLOW='' BLUE='' NC=''
fi

usage() {
    echo "Usage: $0 <concept|pattern|dewey_id>"
    echo
    echo "Examples:"
    echo "  $0 monad                    # Find what relates to 'monad'"
    echo "  $0 e.2.36                   # Find what relates to e.2.36"
    echo "  $0 love_is_resonance        # Find pattern connections"
    echo
    echo "Output: List of related concepts to load for full context"
    exit 1
}

[[ $# -lt 1 ]] && usage

INPUT="$1"
DEPTH="${2:-1}"  # How many hops to follow (default 1)

# Check if graph exists
if [[ ! -f "$ADJACENCY_FILE" ]]; then
    echo -e "${YELLOW}⚠ Graph not built. Run parse-skills.sh && build-graph.sh first${NC}" >&2
    exit 1
fi

echo -e "${BLUE}=== Auto-Stitch: Finding related concepts ===${NC}"
echo "Input: $INPUT"
echo "Depth: $DEPTH hop(s)"
echo

# Find direct matches in adjacency
find_related() {
    local query="$1"
    local found=()

    # Search for the query as a node name
    while IFS=: read -r node deps; do
        # Trim whitespace
        node=$(echo "$node" | xargs)
        deps=$(echo "$deps" | xargs)

        if [[ "$node" == *"$query"* ]] || [[ "$deps" == *"$query"* ]]; then
            if [[ -n "$deps" ]]; then
                # This node relates to query
                echo "$node"
                # Its dependencies also relate
                echo "$deps" | tr ',' '\n'
            fi
        fi
    done < "$ADJACENCY_FILE" | sort -u
}

# Get direct relations
echo -e "${GREEN}Direct relations:${NC}"
RELATED=$(find_related "$INPUT")

if [[ -z "$RELATED" ]]; then
    echo "  No direct matches found for '$INPUT'"
    echo
    echo "Try searching parsed.txt:"
    grep -i "$INPUT" "$PARSED_FILE" 2>/dev/null | head -5 || echo "  Not found in parsed data either"
    exit 0
fi

echo "$RELATED" | while read -r item; do
    [[ -n "$item" ]] && echo "  → $item"
done

# Count results
COUNT=$(echo "$RELATED" | grep -c . || echo 0)
echo
echo -e "${BLUE}Total related concepts: $COUNT${NC}"

# If depth > 1, follow the chain
if [[ "$DEPTH" -gt 1 ]]; then
    echo
    echo -e "${YELLOW}Following chain (depth $DEPTH)...${NC}"

    ALL_RELATED="$RELATED"
    for ((d=2; d<=DEPTH; d++)); do
        NEW_RELATED=""
        while read -r concept; do
            [[ -z "$concept" ]] && continue
            MORE=$(find_related "$concept")
            NEW_RELATED="$NEW_RELATED"$'\n'"$MORE"
        done <<< "$RELATED"

        ALL_RELATED="$ALL_RELATED"$'\n'"$NEW_RELATED"
    done

    UNIQUE=$(echo "$ALL_RELATED" | sort -u | grep -v '^$')
    UNIQUE_COUNT=$(echo "$UNIQUE" | grep -c . || echo 0)

    echo
    echo -e "${GREEN}All related (depth $DEPTH):${NC}"
    echo "$UNIQUE" | while read -r item; do
        [[ -n "$item" ]] && echo "  → $item"
    done
    echo
    echo -e "${BLUE}Total unique: $UNIQUE_COUNT${NC}"
fi

# Suggest files to load
echo
echo -e "${BLUE}=== Suggested Load Order ===${NC}"
echo "1. gremlin-brain-v2/GREMLIN-SEED.md (always first)"
echo "2. Nexus-MC/Nexus_graph_v2.skill (patterns)"

# Map concepts to files
echo "3. Related concepts:"
echo "$RELATED" | head -10 | while read -r concept; do
    [[ -z "$concept" ]] && continue
    # Try to find the file
    FILE=$(grep "^$concept|" "$PARSED_FILE" 2>/dev/null | head -1 | cut -d'|' -f5)
    if [[ -n "$FILE" && "$FILE" != "?" ]]; then
        echo "   - $concept ($FILE)"
    else
        echo "   - $concept"
    fi
done

echo
echo "Run: Read these files to rebuild context for '$INPUT'"

# Final step: invoke meta-pattern-recognition
echo
echo -e "${BLUE}=== Final Step: Meta-Pattern Recognition ===${NC}"
echo "After loading, run meta-pattern-recognition to find:"
echo "  - Patterns appearing in 3+ loaded concepts"
echo "  - Cross-domain connections"
echo "  - Emergent structure from loaded knowledge"
echo
echo "Invoke: skill meta-pattern-recognition"
echo "Or load: .claude/skills/meta-pattern-recognition/SKILL.md"
