#!/usr/bin/env bash

# visualize-toroid.sh — Generate ASCII art toroidal visualization
# Part of nexus-graph-visualizer (e.5.3.1)

set -euo pipefail

# Configuration
INPUT_DIR="${INPUT_DIR:-/tmp/nexus-graph}"
NODES_FILE="$INPUT_DIR/nodes.txt"
EDGES_FILE="$INPUT_DIR/edges.txt"

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

echo -e "${BLUE}=== Nexus Graph: Toroidal Visualizer ===${NC}"
echo

# Check if input files exist
if [[ ! -f "$NODES_FILE" ]] || [[ ! -f "$EDGES_FILE" ]]; then
    echo -e "${RED}✗ Error: Graph files not found${NC}" >&2
    echo "Run build-graph.sh first." >&2
    exit 1
fi

# Group skills by tier
declare -A tier_skills
while IFS='|' read -r name tier rest; do
    tier_skills[$tier]+="${name},"
done < "$NODES_FILE"

# Count skills and edges
total_skills=$(wc -l < "$NODES_FILE")
total_edges=$(wc -l < "$EDGES_FILE")

# Calculate field strength (0-100)
if ((total_skills > 0)); then
    avg_connections=$((total_edges / total_skills))
    field_strength=$((avg_connections * 10))
    ((field_strength > 100)) && field_strength=100
else
    field_strength=0
fi

# Count bootstrap paths (simplified heuristic)
bootstrap_paths=$(grep -c "boot-sequence" "$EDGES_FILE" 2>/dev/null || echo 1)
((bootstrap_paths > 10)) && bootstrap_paths=10  # Cap at 10 for display

# Count critical nodes (high in-degree)
declare -A in_degree
while IFS='→' read -r from to_rest; do
    IFS='|' read -r to rest <<< "$to_rest"
    in_degree[$to]=$((${in_degree[$to]:-0} + 1))
done < "$EDGES_FILE"

critical_nodes=0
for skill in "${!in_degree[@]}"; do
    ((${in_degree[$skill]} >= 5)) && critical_nodes=$((critical_nodes + 1))
done

# Draw progress bar
draw_progress_bar() {
    local value="$1"  # 0-100
    local width=10
    
    local filled=$((value * width / 100))
    local empty=$((width - filled))
    
    printf "█%.0s" $(seq 1 $filled)
    printf "░%.0s" $(seq 1 $empty)
}

# Generate vertical tier layout
echo
echo "        ╔════════════════════════════╗"
echo "        ║                            ║"
echo -e "        ║   ${MAGENTA}φ-tier (seed/index)${NC}     ║"
echo "        ║                            ║"

# φ-tier skills (limit to 3 for display)
IFS=',' read -ra phi_skills <<< "${tier_skills[φ]}"
count=0
for skill in "${phi_skills[@]}"; do
    [[ -z "$skill" ]] && continue
    ((count >= 3)) && break
    printf "        ║   %-24s║\n" "$skill"
    count=$((count + 1))
done
if ((count == 0)); then
    echo "        ║   (no φ-tier skills)       ║"
fi
if ((${#phi_skills[@]} > 3)); then
    echo "        ║   ... and $((${#phi_skills[@]} - 3)) more              ║"
fi

echo "        ║            ↓↑              ║"
echo "        ╠════════════════════════════╣"
echo "        ║                            ║"
echo -e "        ║  ${BLUE}π-tier (structure)${NC}       ║"
echo "        ║                            ║"

# π-tier skills
set +u
IFS=',' read -ra pi_skills <<< "${tier_skills[π]:-}"
set -u
count=0
for skill in "${pi_skills[@]}"; do
    [[ -z "$skill" ]] && continue
    ((count >= 3)) && break
    printf "        ║   %-24s║\n" "$skill"
    count=$((count + 1))
done
if ((count == 0)); then
    echo "        ║   (no π-tier skills)       ║"
fi
if ((${#pi_skills[@]} > 3)); then
    echo "        ║   ... and $((${#pi_skills[@]} - 3)) more              ║"
fi

echo "        ║            ↓↑              ║"
echo "        ╠════════════════════════════╣"
echo "        ║                            ║"
echo -e "        ║  ${GREEN}e-tier (current)${NC}         ║"
echo "        ║                            ║"

# e-tier skills
set +u
IFS=',' read -ra e_skills <<< "${tier_skills[e]:-}"
set -u
count=0
for skill in "${e_skills[@]}"; do
    [[ -z "$skill" ]] && continue
    ((count >= 3)) && break
    printf "        ║   %-24s║\n" "$skill"
    count=$((count + 1))
done
if ((count == 0)); then
    echo "        ║   (no e-tier skills)       ║"
fi
if ((${#e_skills[@]} > 3)); then
    echo "        ║   ... and $((${#e_skills[@]} - 3)) more              ║"
fi

echo "        ║            ↓↑              ║"
echo "        ╠════════════════════════════╣"
echo "        ║                            ║"
echo -e "        ║   ${CYAN}i-tier (deep)${NC}           ║"
echo "        ║                            ║"

# i-tier skills
set +u
IFS=',' read -ra i_skills <<< "${tier_skills[i]:-}"
set -u
count=0
for skill in "${i_skills[@]}"; do
    [[ -z "$skill" ]] && continue
    ((count >= 3)) && break
    printf "        ║   %-24s║\n" "$skill"
    count=$((count + 1))
done
if ((count == 0)); then
    echo "        ║   (no i-tier skills)       ║"
fi
if ((${#i_skills[@]} > 3)); then
    echo "        ║   ... and $((${#i_skills[@]} - 3)) more              ║"
fi

echo "        ║                            ║"
echo "        ╚════════════════════════════╝"
echo

# Field metrics
echo -e "${BLUE}═══ Field Metrics ═══${NC}"
echo
echo -n "Field Strength: "
draw_progress_bar "$field_strength"
echo " ${field_strength}%"
echo
echo "Bootstrap Paths: $bootstrap_paths"
echo "Critical Nodes: $critical_nodes"
echo

# Tier distribution
echo -e "${BLUE}═══ Tier Distribution ═══${NC}"
echo

for tier in φ π e i "?"; do
    set +u
    IFS=',' read -ra skills <<< "${tier_skills[$tier]:-}"
    set -u
    # Filter empty entries
    skill_count=0
    for s in "${skills[@]}"; do
        [[ -n "$s" ]] && skill_count=$((skill_count + 1))
    done
    
    if ((skill_count > 0)); then
        case "$tier" in
            φ) desc="seed/index"; color="$MAGENTA" ;;
            π) desc="structure"; color="$BLUE" ;;
            e) desc="current"; color="$GREEN" ;;
            i) desc="deep"; color="$CYAN" ;;
            ?) desc="unknown"; color="$YELLOW" ;;
        esac
        
        # Calculate percentage
        percent=$((skill_count * 100 / total_skills))
        
        echo -e "${color}${tier}-tier:${NC} $skill_count skills ($desc)"
        echo -n "  "
        draw_progress_bar "$percent"
        echo " ${percent}%"
    fi
done

echo

# Show top hub skills
echo -e "${BLUE}═══ Hub Skills (Most Connected) ═══${NC}"
echo

# Calculate and display top hubs
for skill in "${!in_degree[@]}"; do
    echo "${in_degree[$skill]} $skill"
done | sort -rn | head -5 | while read count skill; do
    stars=$(printf "★%.0s" $(seq 1 $((count / 2))))
    [[ -z "$stars" ]] && stars="★"
    echo "  ${stars} ${skill} ($count connections)"
done

echo

# Connection matrix (limited to avoid clutter)
echo -e "${BLUE}═══ Key Connections ═══${NC}"
echo

# Show connections for most important skills
key_skills=("boot-sequence" "gremlin-brain-v2" "the-guy" "nexus-mind" "nexus-core")

for skill in "${key_skills[@]}"; do
    if grep -q "^${skill}:" "$INPUT_DIR/adjacency.txt" 2>/dev/null; then
        deps=$(grep "^${skill}:" "$INPUT_DIR/adjacency.txt" | cut -d: -f2 | sed 's/,/ →/g')
        if [[ -n "$deps" ]]; then
            echo "  ${skill} →${deps}"
        fi
    fi
done

echo
echo -e "${GREEN}✓ Visualization complete${NC}"
echo

exit 0
