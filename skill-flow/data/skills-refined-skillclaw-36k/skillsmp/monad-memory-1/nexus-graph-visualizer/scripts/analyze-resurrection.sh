#!/usr/bin/env bash

# analyze-resurrection.sh — Score identity recovery robustness
# Part of nexus-graph-visualizer (e.5.3.1)

set -euo pipefail

# Configuration
INPUT_DIR="${INPUT_DIR:-/tmp/nexus-graph}"
NODES_FILE="$INPUT_DIR/nodes.txt"
EDGES_FILE="$INPUT_DIR/edges.txt"
ADJACENCY_FILE="$INPUT_DIR/adjacency.txt"
LOOPS_FILE="$INPUT_DIR/loops.txt"

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

echo -e "${BLUE}=== Nexus Graph: Resurrection Analyzer ===${NC}"
echo

# Check if input files exist
if [[ ! -f "$NODES_FILE" ]] || [[ ! -f "$EDGES_FILE" ]]; then
    echo -e "${RED}✗ Error: Graph files not found${NC}" >&2
    echo "Run build-graph.sh first." >&2
    exit 1
fi

# Count bootstrap paths (heuristic: paths from boot-sequence)
count_bootstrap_paths() {
    local paths=0
    
    # Count direct and indirect paths from boot-sequence to nexus-mind
    if grep -q "boot-sequence" "$ADJACENCY_FILE" && grep -q "nexus-mind" "$ADJACENCY_FILE"; then
        # Direct path
        if grep "^boot-sequence:" "$ADJACENCY_FILE" | grep -q "nexus-mind"; then
            paths=$((paths + 1))
        fi
        
        # Indirect paths (through intermediaries)
        local intermediaries=$(grep "^boot-sequence:" "$ADJACENCY_FILE" | cut -d: -f2 | tr ',' '\n')
        for inter in $intermediaries; do
            if grep "^${inter}:" "$ADJACENCY_FILE" 2>/dev/null | grep -q "nexus-mind"; then
                paths=$((paths + 1))
            fi
        done
        
        # At least 1 path if both skills exist
        ((paths == 0)) && paths=1
    fi
    
    echo "$paths"
}

# Find critical nodes (articulation points heuristic)
find_critical_nodes() {
    declare -A in_degree
    
    # Calculate in-degree for each node
    while IFS='→' read -r from to_rest; do
        IFS='|' read -r to rest <<< "$to_rest"
        in_degree[$to]=$((${in_degree[$to]:-0} + 1))
    done < "$EDGES_FILE"
    
    # Nodes with high in-degree are critical
    local critical=0
    for skill in "${!in_degree[@]}"; do
        if ((${in_degree[$skill]} >= 5)); then
            critical=$((critical + 1))
            echo "$skill"
        fi
    done
    
    # Return count via return code (limited to 0-255)
    return 0
}

# Calculate loop strength
calculate_loop_strength() {
    if [[ ! -f "$LOOPS_FILE" ]]; then
        echo "0"
        return
    fi
    
    local total_strength=0
    local loop_count=$(grep -c "^LOOP_" "$LOOPS_FILE" 2>/dev/null)
    loop_count=${loop_count:-0}
    
    if [[ "$loop_count" -eq 0 ]]; then
        echo "0"
        return
    fi
    
    # Simple heuristic: longer loops with more tier diversity = stronger
    awk '/^LOOP_/ {
        getline
        count = 0
        while (getline && $0 != "" && $0 !~ /^LOOP_/) {
            if ($0 ~ /^  [a-z]/) count++
        }
        print count
    }' "$LOOPS_FILE" | awk '{sum += $1} END {if (NR > 0) print int(sum / NR); else print 0}'
}

# Calculate morpheme coverage
calculate_morpheme_coverage() {
    local morphemes=$(cut -d'|' -f3 "$NODES_FILE" | sort -u | grep -v "?" | wc -l)
    echo "$morphemes"
}

# Calculate tier balance
calculate_tier_balance() {
    declare -A tier_counts
    local total=0
    
    while IFS='|' read -r name tier rest; do
        [[ "$tier" == "?" ]] && continue
        tier_counts[$tier]=$((${tier_counts[$tier]:-0} + 1))
        total=$((total + 1))
    done < "$NODES_FILE"
    
    if ((total == 0)); then
        echo "50"  # Neutral score if no tier info
        return
    fi
    
    # If very few skills have tier info, return neutral score
    if ((total < 4)); then
        echo "50"
        return
    fi
    
    # Calculate standard deviation from equal distribution
    local mean=$((total / 4))
    local variance=0
    
    for tier in φ π e i; do
        local count=${tier_counts[$tier]:-0}
        local diff=$((count - mean))
        variance=$((variance + diff * diff))
    done
    
    # Lower variance = better balance
    # Convert to 0-100 score (100 = perfect balance)
    local stddev=$(echo "scale=2; sqrt($variance / 4)" | bc)
    local balance=$(echo "scale=0; (100 - ($stddev * 5))/1" | bc)
    
    # Clamp to 0-100 (use bc for comparisons)
    if (($(echo "$balance < 0" | bc -l))); then balance=0; fi
    if (($(echo "$balance > 100" | bc -l))); then balance=100; fi
    
    echo "$balance"
}

# Calculate resurrection score
echo "Analyzing resurrection protocol strength..."
echo

# Collect metrics
bootstrap_paths=$(count_bootstrap_paths) || bootstrap_paths=0
critical_nodes_list=$(find_critical_nodes) || critical_nodes_list=""
critical_count=$(echo "$critical_nodes_list" | grep -v "^$" | wc -l) || critical_count=0
loop_strength=$(calculate_loop_strength) || loop_strength=0
morpheme_coverage=$(calculate_morpheme_coverage) || morpheme_coverage=0
tier_balance=$(calculate_tier_balance) || tier_balance=50

# Calculate component scores
# Bootstrap paths: 0-20 points (log scale, max at 4+ paths)
if ((bootstrap_paths >= 4)); then
    paths_score=20
elif ((bootstrap_paths == 3)); then
    paths_score=18
elif ((bootstrap_paths == 2)); then
    paths_score=15
elif ((bootstrap_paths == 1)); then
    paths_score=10
else
    paths_score=0
fi

# Critical nodes: 0-30 points (fewer is better)
critical_score=$((30 - critical_count * 5))
((critical_score < 0)) && critical_score=0

# Loop strength: 0-30 points
loop_score=$((loop_strength * 3))
((loop_score > 30)) && loop_score=30

# Morpheme coverage: 0-10 points
morpheme_score=$((morpheme_coverage * 10 / 6))
((morpheme_score > 10)) && morpheme_score=10

# Tier balance: 0-10 points
# Clean up tier_balance (remove any non-numeric characters except negative sign)
tier_balance=$(echo "$tier_balance" | tr -cd '0-9-' | head -c 10)
[[ -z "$tier_balance" ]] && tier_balance=50
balance_score=$((tier_balance / 10))

# Total score
total_score=$((paths_score + critical_score + loop_score + morpheme_score + balance_score))

# Determine grade
if ((total_score >= 90)); then
    grade="ROBUST ✓✓✓"
    color="$GREEN"
elif ((total_score >= 75)); then
    grade="STRONG ✓✓"
    color="$GREEN"
elif ((total_score >= 60)); then
    grade="MODERATE ✓"
    color="$YELLOW"
elif ((total_score >= 45)); then
    grade="FRAGILE ⚠"
    color="$YELLOW"
else
    grade="BRITTLE ✗"
    color="$RED"
fi

# Display report
echo
echo "════════════════════════════════════════════════════════"
echo -e "  ${color}🧠 Resurrection Protocol Strength: ${total_score}/100${NC}"
echo -e "     ${color}${grade}${NC}"
echo "════════════════════════════════════════════════════════"
echo
echo -e "${BLUE}📊 Component Breakdown:${NC}"
echo

# Bootstrap Paths
echo "Bootstrap Paths:"
echo "  Count: $bootstrap_paths"
echo "  Score: $paths_score/20"
if ((bootstrap_paths >= 3)); then
    echo -e "  ${GREEN}✓${NC} GOOD - Multiple recovery routes exist"
elif ((bootstrap_paths == 2)); then
    echo -e "  ${YELLOW}⚠${NC} MODERATE - Limited redundancy"
elif ((bootstrap_paths == 1)); then
    echo -e "  ${RED}✗${NC} FRAGILE - Single path of recovery"
else
    echo -e "  ${RED}✗${NC} CRITICAL - No bootstrap path found"
fi
echo

# Critical Nodes
echo "Critical Nodes:"
echo "  Count: $critical_count"
echo "  Score: $critical_score/30"
if ((critical_count == 0)); then
    echo -e "  ${GREEN}✓${NC} Excellent - No single points of failure"
elif ((critical_count <= 2)); then
    echo -e "  ${YELLOW}⚠${NC} Acceptable - Few critical dependencies"
    echo "  Critical skills:"
    echo "$critical_nodes_list" | while read node; do
        [[ -n "$node" ]] && echo "    - $node"
    done
else
    echo -e "  ${RED}✗${NC} Concerning - Multiple SPOFs detected"
    echo "  Critical skills:"
    echo "$critical_nodes_list" | head -5 | while read node; do
        [[ -n "$node" ]] && echo "    - $node"
    done
    ((critical_count > 5)) && echo "    ... and $((critical_count - 5)) more"
fi
echo

# Loop Strength
echo "Autopoietic Loops:"
echo "  Average strength: $loop_strength"
echo "  Score: $loop_score/30"
if ((loop_strength >= 12)); then
    echo -e "  ${GREEN}✓${NC} Strong loops with good diversity"
elif ((loop_strength >= 8)); then
    echo -e "  ${YELLOW}⚠${NC} Moderate loops, could be stronger"
elif ((loop_strength > 0)); then
    echo -e "  ${YELLOW}⚠${NC} Weak loops detected"
else
    echo -e "  ${RED}✗${NC} No autopoietic loops found"
fi
echo

# Morpheme Coverage
echo "Morpheme Coverage:"
echo "  Present: $morpheme_coverage/6"
echo "  Score: $morpheme_score/10"
if ((morpheme_coverage == 6)); then
    echo -e "  ${GREEN}✓${NC} Complete - All aeonic morphemes represented"
elif ((morpheme_coverage >= 4)); then
    echo -e "  ${YELLOW}⚠${NC} Good - Minor gaps acceptable"
else
    echo -e "  ${RED}✗${NC} Incomplete - Missing key morphemes"
fi
echo

# Tier Balance
echo "Tier Balance:"
echo "  Score: $balance_score/10"
if ((balance_score >= 8)); then
    echo -e "  ${GREEN}✓${NC} Well balanced across tiers"
elif ((balance_score >= 5)); then
    echo -e "  ${YELLOW}⚠${NC} Moderate imbalance"
else
    echo -e "  ${RED}✗${NC} Heavily skewed distribution"
fi
echo

# Recommendations
echo "════════════════════════════════════════════════════════"
echo -e "${BLUE}📋 Recommendations:${NC}"
echo

if ((bootstrap_paths < 2)); then
    echo -e "${RED}🚨 URGENT:${NC} Create additional bootstrap paths"
    echo "   - Add alternative entry points to nexus-mind"
    echo "   - Consider creating backup boot skill"
    echo
fi

if ((critical_count > 2)); then
    echo -e "${YELLOW}⚠${NC}  Reduce critical node dependencies:"
    echo "$critical_nodes_list" | head -3 | while read node; do
        [[ -n "$node" ]] && echo "   - Add redundant paths around: $node"
    done
    echo
fi

if ((loop_strength < 10)); then
    echo -e "${YELLOW}⚠${NC}  Strengthen autopoietic loops:"
    echo "   - Increase cross-tier dependencies"
    echo "   - Add morpheme-diverse skills to loops"
    echo
fi

if ((morpheme_coverage < 5)); then
    echo -e "${YELLOW}⚠${NC}  Improve morpheme coverage:"
    echo "   - Add skills for missing morphemes"
    echo
fi

if ((total_score >= 75)); then
    echo -e "${GREEN}✓${NC} System demonstrates strong autopoietic structure"
    echo "  Identity recovery is robust across resets"
fi

echo "════════════════════════════════════════════════════════"
echo

exit 0
