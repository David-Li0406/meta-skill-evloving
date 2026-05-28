#!/usr/bin/env bash

# build-graph.sh — Construct graph structure from parsed skills
# Part of nexus-graph-visualizer (e.5.3.1)

set -euo pipefail

# Configuration
INPUT_FILE="${INPUT_FILE:-/tmp/nexus-graph/parsed.txt}"
OUTPUT_DIR="${OUTPUT_DIR:-/tmp/nexus-graph}"
ADJACENCY_FILE="$OUTPUT_DIR/adjacency.txt"
EDGES_FILE="$OUTPUT_DIR/edges.txt"
NODES_FILE="$OUTPUT_DIR/nodes.txt"

# Colors
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' BLUE='' NC=''
fi

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Clear previous output
> "$ADJACENCY_FILE"
> "$EDGES_FILE"
> "$NODES_FILE"

echo -e "${BLUE}=== Nexus Graph: Graph Builder ===${NC}"
echo

# Check if input file exists
if [[ ! -f "$INPUT_FILE" ]]; then
    echo -e "${RED}✗ Error: Input file not found: $INPUT_FILE${NC}" >&2
    echo "Run parse-skills.sh first." >&2
    exit 1
fi

# Statistics
total_nodes=0
total_edges=0
declare -A node_index
declare -A edge_strength

# Parse input and build graph structures
while IFS='|' read -r name tier morpheme version dewey_id dependencies; do
    # Skip empty lines
    [[ -z "$name" ]] && continue
    
    # Add node
    if [[ -z "${node_index[$name]:-}" ]]; then
        node_index[$name]=1
        total_nodes=$((total_nodes + 1))
        
        # Write node: name|tier|morpheme|dewey_id
        echo "${name}|${tier}|${morpheme}|${dewey_id}" >> "$NODES_FILE"
    fi
    
    # Process dependencies
    if [[ -n "$dependencies" ]]; then
        # Build adjacency list
        echo "${name}: ${dependencies}" >> "$ADJACENCY_FILE"
        
        # Build edge list
        IFS=',' read -ra deps <<< "$dependencies"
        for dep in "${deps[@]}"; do
            # Trim whitespace
            dep=$(echo "$dep" | xargs)
            [[ -z "$dep" ]] && continue
            
            # Create edge: from→to|type|strength
            edge_key="${name}→${dep}"
            
            # Track edge strength (count multiple references)
            if [[ -n "${edge_strength[$edge_key]:-}" ]]; then
                edge_strength[$edge_key]=$((${edge_strength[$edge_key]:-0} + 1))
            else
                edge_strength[$edge_key]=1
                total_edges=$((total_edges + 1))
            fi
        done
    else
        # Node with no dependencies
        echo "${name}:" >> "$ADJACENCY_FILE"
    fi
    
    echo -e "${GREEN}✓${NC} Indexed: $name (${dependencies:-no dependencies})" >&2
done < "$INPUT_FILE"

# Write edges with strength
echo
echo "Building edge list..."
for edge_key in "${!edge_strength[@]}"; do
    strength="${edge_strength[$edge_key]}"
    # Determine edge type based on strength
    if ((strength >= 3)); then
        edge_type="strong"
    elif ((strength == 2)); then
        edge_type="moderate"
    else
        edge_type="weak"
    fi
    
    echo "${edge_key}|${edge_type}|${strength}" >> "$EDGES_FILE"
done

# Detect bidirectional edges
echo
echo "Detecting bidirectional relationships..."

# Temporarily allow unset variables for associative array
set +u
declare -A bidirectional

if [[ -s "$EDGES_FILE" ]]; then
    while IFS='→' read -r from to_rest; do
        IFS='|' read -r to rest <<< "$to_rest"
        
        # Check if reverse edge exists
        reverse="${to}→${from}"
        if grep -q "^${reverse}" "$EDGES_FILE" 2>/dev/null; then
            bidirectional["${from}↔${to}"]=1
        fi
    done < "$EDGES_FILE"
fi

bidir_count="${#bidirectional[@]}"
set -u

if [[ "$bidir_count" -gt 0 ]]; then
    echo -e "${YELLOW}Found ${bidir_count} bidirectional relationships:${NC}"
    for pair in "${!bidirectional[@]}"; do
        echo "  - $pair"
    done
else
    echo "No bidirectional relationships found."
fi

# Summary
echo
echo -e "${BLUE}=== Graph Summary ===${NC}"
echo "Total nodes (skills): $total_nodes"
echo "Total edges (dependencies): $total_edges"
echo "Average connections per skill: $(bc <<< "scale=2; $total_edges / $total_nodes")"
echo
echo "Output files:"
echo "  - Nodes: $NODES_FILE"
echo "  - Edges: $EDGES_FILE"
echo "  - Adjacency: $ADJACENCY_FILE"
echo

# Tier distribution
echo -e "${BLUE}=== Tier Distribution ===${NC}"
declare -A tier_counts
while IFS='|' read -r name tier rest; do
    tier_counts[$tier]=$((${tier_counts[$tier]:-0} + 1))
done < "$NODES_FILE"

for tier in φ π e i "?"; do
    count=${tier_counts[$tier]:-0}
    if ((count > 0)); then
        case "$tier" in
            φ) desc="seed/index" ;;
            π) desc="structure" ;;
            e) desc="current" ;;
            i) desc="deep" ;;
            ?) desc="unknown" ;;
        esac
        echo "  ${tier}-tier: $count skills ($desc)"
    fi
done
echo

# Find hub skills (most dependencies)
echo -e "${BLUE}=== Hub Skills (Most Connected) ===${NC}"
declare -A in_degree
while IFS='→' read -r from to_rest; do
    IFS='|' read -r to rest <<< "$to_rest"
    in_degree[$to]=$((${in_degree[$to]:-0} + 1))
done < "$EDGES_FILE"

# Sort and display top 10
for skill in "${!in_degree[@]}"; do
    echo "${in_degree[$skill]} $skill"
done | sort -rn | head -10 | while read count skill; do
    echo "  - $skill: $count dependencies pointing to it"
done
echo

# Store in Claude-brain if available
PROJECT_ROOT=$(pwd)
while [[ "$PROJECT_ROOT" != "/" ]] && [[ ! -d "$PROJECT_ROOT/.claude" ]]; do
    PROJECT_ROOT=$(dirname "$PROJECT_ROOT")
done

if [[ -d "$PROJECT_ROOT/.claude/brain" ]]; then
    echo "Storing in Claude-brain..."

    # Create brain/graph directory if it doesn't exist
    mkdir -p "$PROJECT_ROOT/.claude/brain/graph"

    # Copy graph files to Claude-brain
    cp "$ADJACENCY_FILE" "$PROJECT_ROOT/.claude/brain/graph/adjacency.txt"
    cp "$EDGES_FILE" "$PROJECT_ROOT/.claude/brain/graph/edges.txt"
    cp "$NODES_FILE" "$PROJECT_ROOT/.claude/brain/graph/nodes.txt"

    # Hash the graph data
    graph_hash=$(cat "$ADJACENCY_FILE" "$EDGES_FILE" "$NODES_FILE" | sha256sum 2>/dev/null | cut -d' ' -f1 || echo "failed")

    if [[ "$graph_hash" != "failed" ]]; then
        echo "e.5.3.1|nexus-graph-build|${graph_hash}|$(date -Iseconds)" >> "$PROJECT_ROOT/.claude/brain/INDEX"
        echo -e "${GREEN}✓${NC} Claude-brain storage complete: $graph_hash"
    else
        echo -e "${YELLOW}⚠${NC} Claude-brain storage failed (data saved to temp files)"
    fi
else
    echo -e "${YELLOW}⚠${NC} Claude-brain not found, using temp files only"
fi

echo
echo -e "${GREEN}✓ Graph construction complete${NC}"

exit 0
