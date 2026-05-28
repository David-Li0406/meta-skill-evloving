#!/usr/bin/env bash

# detect-loops.sh — Find coherence cycles and autopoietic loops
# Part of nexus-graph-visualizer (e.5.3.1)

set -euo pipefail

# Configuration
INPUT_DIR="${INPUT_DIR:-/tmp/nexus-graph}"
ADJACENCY_FILE="$INPUT_DIR/adjacency.txt"
NODES_FILE="$INPUT_DIR/nodes.txt"
OUTPUT_FILE="${OUTPUT_FILE:-/tmp/nexus-graph/loops.txt}"

# Colors
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
    MAGENTA='\033[0;35m'
    CYAN='\033[0;36m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' BLUE='' MAGENTA='' CYAN='' NC=''
fi

echo -e "${BLUE}=== Nexus Graph: Loop Detector ===${NC}"
echo

# Check if input files exist
if [[ ! -f "$ADJACENCY_FILE" ]]; then
    echo -e "${RED}✗ Error: Adjacency file not found: $ADJACENCY_FILE${NC}" >&2
    echo "Run build-graph.sh first." >&2
    exit 1
fi

# Clear previous output
> "$OUTPUT_FILE"

# Build adjacency map in memory
declare -A adjacency
while IFS=':' read -r skill deps; do
    # Trim whitespace
    skill=$(echo "$skill" | xargs)
    deps=$(echo "$deps" | xargs)
    
    [[ -z "$skill" ]] && continue
    
    adjacency[$skill]="$deps"
done < "$ADJACENCY_FILE"

# Get skill tier
get_tier() {
    local skill="$1"
    grep "^${skill}|" "$NODES_FILE" 2>/dev/null | cut -d'|' -f2 || echo "?"
}

# Get skill morpheme
get_morpheme() {
    local skill="$1"
    grep "^${skill}|" "$NODES_FILE" 2>/dev/null | cut -d'|' -f3 || echo "?"
}

# DFS-based cycle detection
declare -A visited
declare -A rec_stack
declare -a path
loops_found=0

detect_cycle() {
    local node="$1"
    
    # Mark as visiting
    visited["$node"]=1
    rec_stack["$node"]=1
    path+=("$node")
    
    # Get dependencies
    local deps="${adjacency[$node]}"
    
    if [[ -n "$deps" ]]; then
        IFS=',' read -ra dep_array <<< "$deps"
        
        for dep in "${dep_array[@]}"; do
            # Trim whitespace
            dep=$(echo "$dep" | xargs)
            [[ -z "$dep" ]] && continue
            
            # Skip if dependency doesn't exist in our graph
            [[ -z "${adjacency[$dep]}" ]] && [[ -z $(grep "^${dep}:" "$ADJACENCY_FILE" 2>/dev/null) ]] && continue
            
            # If not visited, recurse
            if [[ -z "${visited[$dep]:-}" ]]; then
                detect_cycle "$dep"
            # If in recursion stack, we found a cycle!
            elif [[ -n "${rec_stack[$dep]:-}" ]]; then
                # Extract the cycle from path
                local cycle_start=0
                for ((i=0; i<${#path[@]}; i++)); do
                    if [[ "${path[i]}" == "$dep" ]]; then
                        cycle_start=$i
                        break
                    fi
                done
                
                # Found a loop!
                loops_found=$((loops_found + 1))
                
                echo "LOOP_${loops_found}:" >> "$OUTPUT_FILE"
                
                local cycle_path=""
                for ((i=cycle_start; i<${#path[@]}; i++)); do
                    echo "  ${path[i]}" >> "$OUTPUT_FILE"
                    cycle_path="${cycle_path}${path[i]}→"
                done
                echo "  ${dep}" >> "$OUTPUT_FILE"
                echo "" >> "$OUTPUT_FILE"
                
                # Calculate loop properties
                local loop_length=$((${#path[@]} - cycle_start))
                
                # Get unique tiers in loop
                local -A loop_tiers
                for ((i=cycle_start; i<${#path[@]}; i++)); do
                    tier=$(get_tier "${path[i]}")
                    loop_tiers[$tier]=1
                done
                tier=$(get_tier "$dep")
                loop_tiers[$tier]=1
                
                # Get unique morphemes in loop
                local -A loop_morphemes
                for ((i=cycle_start; i<${#path[@]}; i++)); do
                    morpheme=$(get_morpheme "${path[i]}")
                    loop_morphemes[$morpheme]=1
                done
                morpheme=$(get_morpheme "$dep")
                loop_morphemes[$morpheme]=1
                
                # Check if bootstrap-critical
                local is_critical=""
                if echo "${cycle_path}" | grep -q "boot-sequence"; then
                    if echo "${cycle_path}" | grep -q "nexus-mind"; then
                        is_critical="YES"
                    fi
                fi
                
                # Display loop
                echo -e "${MAGENTA}🔄 Loop #${loops_found}${NC}"
                echo "  Path: ${cycle_path}${dep}"
                echo "  Length: $loop_length nodes"
                echo "  Tier diversity: ${#loop_tiers[@]}/4 (${!loop_tiers[@]})"
                echo "  Morpheme diversity: ${#loop_morphemes[@]}/6 (${!loop_morphemes[@]})"
                [[ -n "$is_critical" ]] && echo -e "  ${RED}⚠ RESURRECTION CRITICAL${NC}"
                echo
            fi
        done
    fi
    
    # Backtrack
    unset 'path[-1]'
    unset "rec_stack[$node]"
}

# Find all cycles
echo "Scanning for autopoietic loops..."
echo

set +u  # Disable unset variable check for associative arrays
for skill in "${!adjacency[@]}"; do
    if [[ -z "${visited[$skill]:-}" ]]; then
        detect_cycle "$skill"
    fi
done
set -u

# Summary
echo
echo -e "${BLUE}=== Loop Detection Summary ===${NC}"
echo "Total autopoietic loops found: $loops_found"
echo

if ((loops_found > 0)); then
    echo "Loop details written to: $OUTPUT_FILE"
    echo
    
    # Analyze loop quality
    echo -e "${BLUE}=== Loop Quality Analysis ===${NC}"

    strong_loops=0
    moderate_loops=0
    weak_loops=0
    
    # Count loops by strength (based on length and tier diversity)
    awk '/^LOOP_/ { 
        loop_num = $0
        getline
        count = 0
        tiers = ""
        while (getline && $0 != "") {
            if ($0 ~ /^  [a-z]/) {
                count++
            }
        }
        if (count >= 4) print "strong"
        else if (count >= 3) print "moderate"
        else print "weak"
    }' "$OUTPUT_FILE" | while read strength; do
        case "$strength" in
            strong) strong_loops=$((strong_loops + 1)) ;;
            moderate) moderate_loops=$((moderate_loops + 1)) ;;
            weak) weak_loops=$((weak_loops + 1)) ;;
        esac
    done
    
    # Note: The above loop runs in a subshell, so we recalculate for display
    strong_loops=$(grep -A 20 "^LOOP_" "$OUTPUT_FILE" | grep "^  " | awk 'BEGIN{RS=""; FS="\n"} {if (NF >= 4) print "strong"}' | wc -l)
    moderate_loops=$(grep -A 20 "^LOOP_" "$OUTPUT_FILE" | grep "^  " | awk 'BEGIN{RS=""; FS="\n"} {if (NF == 3) print "moderate"}' | wc -l)
    weak_loops=$(grep -A 20 "^LOOP_" "$OUTPUT_FILE" | grep "^  " | awk 'BEGIN{RS=""; FS="\n"} {if (NF <= 2) print "weak"}' | wc -l)
    
    echo "  Strong loops (4+ nodes): $strong_loops"
    echo "  Moderate loops (3 nodes): $moderate_loops"
    echo "  Weak loops (2 nodes): $weak_loops"
    echo
    
    # Check for resurrection-critical loops
    if grep -q "boot-sequence" "$OUTPUT_FILE" && grep -q "nexus-mind" "$OUTPUT_FILE"; then
        echo -e "${GREEN}✓${NC} Resurrection-critical loops detected!"
        echo "  The identity recovery mechanism is present."
    else
        echo -e "${YELLOW}⚠${NC} No clear resurrection-critical loops found."
        echo "  Consider adding connections between boot-sequence and nexus-mind."
    fi
else
    echo -e "${YELLOW}⚠ No loops detected.${NC}"
    echo "This may indicate:"
    echo "  - Graph is a DAG (directed acyclic graph)"
    echo "  - Missing skill dependencies"
    echo "  - Insufficient cross-references"
    echo
    echo "Autopoietic systems typically contain loops."
    echo "Consider adding bidirectional dependencies for coherence."
fi

echo

exit 0
