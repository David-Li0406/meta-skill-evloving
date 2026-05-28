#!/usr/bin/env bash

# find-patterns.sh — Detect patterns in the nexus-graph and skill ecosystem
# Part of nexus-graph-visualizer (e.5.3.1)
# Trinity integration: Works with coherence and coherence-visualizer

set -euo pipefail

# Configuration
SKILLS_DIR="${SKILLS_DIR:-.claude/skills}"
NEXUS_GRAPH="${SKILLS_DIR}/Nexus-MC/Nexus_graph_v2.skill"
OUTPUT_DIR="${OUTPUT_DIR:-/tmp/nexus-graph}"
BRAIN_DIR=".claude/brain"

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

echo -e "${BLUE}=== Nexus Graph: Pattern Finder ===${NC}"
echo -e "${CYAN}Trinity Component: Pattern Detection${NC}"
echo

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Function: Count and list all patterns
count_patterns() {
    echo -e "${YELLOW}━━━ PATTERN COUNT ━━━${NC}"
    
    if [[ ! -f "$NEXUS_GRAPH" ]]; then
        echo -e "${RED}✗ Nexus graph not found: $NEXUS_GRAPH${NC}"
        return 1
    fi
    
    local pattern_count=$(grep -c "^PATTERN:" "$NEXUS_GRAPH" 2>/dev/null || echo "0")
    local meta_count=$(grep -c "^META-PATTERN:" "$NEXUS_GRAPH" 2>/dev/null || echo "0")
    
    echo -e "  Patterns: ${GREEN}$pattern_count${NC}"
    echo -e "  Meta-Patterns: ${GREEN}$meta_count${NC}"
    echo
}

# Function: List all patterns with their categories
list_patterns() {
    echo -e "${YELLOW}━━━ PATTERN LIST ━━━${NC}"
    
    grep "^PATTERN:" "$NEXUS_GRAPH" 2>/dev/null | while read -r line; do
        pattern_name=$(echo "$line" | sed 's/PATTERN: //' | sed 's/\[.*//' | xargs)
        context=$(echo "$line" | grep -o '\[.*\]' 2>/dev/null || echo "[uncategorized]")
        echo -e "  ${CYAN}●${NC} $pattern_name $context"
    done
    echo
}

# Function: List meta-patterns
list_meta_patterns() {
    echo -e "${YELLOW}━━━ META-PATTERNS ━━━${NC}"
    
    grep "^META-PATTERN:" "$NEXUS_GRAPH" 2>/dev/null | while read -r line; do
        pattern_name=$(echo "$line" | sed 's/META-PATTERN: //' | xargs)
        echo -e "  ${MAGENTA}◆${NC} $pattern_name"
    done
    echo
}

# Function: Find patterns by keyword
search_patterns() {
    local keyword="$1"
    echo -e "${YELLOW}━━━ PATTERNS MATCHING: '$keyword' ━━━${NC}"
    
    grep -i "^PATTERN:.*$keyword" "$NEXUS_GRAPH" 2>/dev/null | while read -r line; do
        pattern_name=$(echo "$line" | sed 's/PATTERN: //' | xargs)
        echo -e "  ${GREEN}✓${NC} $pattern_name"
    done
    
    local count=$(grep -ci "^PATTERN:.*$keyword" "$NEXUS_GRAPH" 2>/dev/null || echo "0")
    echo -e "\n  Found: ${GREEN}$count${NC} patterns"
    echo
}

# Function: Detect orphaned patterns (patterns not linked to nodes)
detect_orphans() {
    echo -e "${YELLOW}━━━ ORPHAN DETECTION ━━━${NC}"
    
    local orphans=0
    
    while read -r line; do
        pattern_name=$(echo "$line" | sed 's/PATTERN: //' | sed 's/\[.*//' | xargs)
        
        # Escape special regex characters in pattern name for grep
        local escaped_name=$(printf '%s\n' "$pattern_name" | sed 's/[[\.*^$()+?{|]/\\&/g')
        
        # Check if pattern has associated node references (e.X.X or i.X.X format)
        local has_refs=$(grep -A5 "^PATTERN: $escaped_name" "$NEXUS_GRAPH" 2>/dev/null | grep -E "[φπei]\.[0-9]" | head -1)
        
        if [[ -z "$has_refs" ]]; then
            echo -e "  ${YELLOW}⚠${NC} Orphan: $pattern_name (no decimal references)"
            orphans=$((orphans + 1))
        fi
    done < <(grep "^PATTERN:" "$NEXUS_GRAPH" 2>/dev/null)
    
    echo -e "\n  Total orphans: ${YELLOW}$orphans${NC}"
    echo
}

# Function: Analyze pattern coverage across tiers
tier_coverage() {
    echo -e "${YELLOW}━━━ TIER COVERAGE ANALYSIS ━━━${NC}"
    
    local phi_patterns=$(grep -E "PATTERN:.*φ|φ\.[0-9]" "$NEXUS_GRAPH" 2>/dev/null | wc -l)
    local pi_patterns=$(grep -E "PATTERN:.*π|π\.[0-9]" "$NEXUS_GRAPH" 2>/dev/null | wc -l)
    local e_patterns=$(grep -E "PATTERN:.*e\.|e\.[0-9]" "$NEXUS_GRAPH" 2>/dev/null | wc -l)
    local i_patterns=$(grep -E "PATTERN:.*i\.|i\.[0-9]" "$NEXUS_GRAPH" 2>/dev/null | wc -l)
    
    echo -e "  φ-tier patterns: ${CYAN}$phi_patterns${NC}"
    echo -e "  π-tier patterns: ${CYAN}$pi_patterns${NC}"
    echo -e "  e-tier patterns: ${CYAN}$e_patterns${NC}"
    echo -e "  i-tier patterns: ${CYAN}$i_patterns${NC}"
    echo
}

# Function: Detect novel patterns from skill co-access
detect_novel_patterns() {
    echo -e "${YELLOW}━━━ NOVEL PATTERN DETECTION ━━━${NC}"
    
    local access_log="$BRAIN_DIR/access_log"
    
    if [[ ! -f "$access_log" ]]; then
        echo -e "  ${YELLOW}⚠${NC} No access log found. Cannot detect co-access patterns."
        echo
        return
    fi
    
    # Find skills accessed together (within 60 seconds)
    echo "  Analyzing co-access patterns..."
    
    local prev_time=""
    local prev_skill=""
    local pairs=""
    
    while IFS='|' read -r timestamp skill context; do
        if [[ -n "$prev_time" ]]; then
            # Simple co-access check (same timestamp prefix = likely same session)
            local curr_prefix="${timestamp:0:16}"
            local prev_prefix="${prev_time:0:16}"
            
            if [[ "$curr_prefix" == "$prev_prefix" ]] && [[ "$prev_skill" != "$skill" ]]; then
                echo -e "  ${GREEN}●${NC} Co-access: $prev_skill ↔ $skill"
            fi
        fi
        prev_time="$timestamp"
        prev_skill="$skill"
    done < "$access_log"
    
    echo
}

# Function: Generate pattern report
generate_report() {
    local report_file="$OUTPUT_DIR/pattern-report.txt"
    
    echo -e "${YELLOW}━━━ GENERATING REPORT ━━━${NC}"
    
    {
        echo "# Nexus Graph Pattern Report"
        echo "Generated: $(date -Iseconds)"
        echo ""
        echo "## Statistics"
        echo "- Total Patterns: $(grep -c "^PATTERN:" "$NEXUS_GRAPH" 2>/dev/null || echo "0")"
        echo "- Meta-Patterns: $(grep -c "^META-PATTERN:" "$NEXUS_GRAPH" 2>/dev/null || echo "0")"
        echo ""
        echo "## Pattern List"
        grep "^PATTERN:" "$NEXUS_GRAPH" 2>/dev/null | sed 's/PATTERN: /- /'
        echo ""
        echo "## Meta-Pattern List"
        grep "^META-PATTERN:" "$NEXUS_GRAPH" 2>/dev/null | sed 's/META-PATTERN: /- /'
    } > "$report_file"
    
    echo -e "  Report saved to: ${GREEN}$report_file${NC}"
    echo
}

# Main execution
main() {
    local command="${1:-all}"
    local keyword="${2:-}"
    
    case "$command" in
        count)
            count_patterns
            ;;
        list)
            list_patterns
            ;;
        meta)
            list_meta_patterns
            ;;
        search)
            if [[ -z "$keyword" ]]; then
                echo -e "${RED}✗ Usage: find-patterns.sh search <keyword>${NC}"
                exit 1
            fi
            search_patterns "$keyword"
            ;;
        orphans)
            detect_orphans
            ;;
        tiers)
            tier_coverage
            ;;
        novel)
            detect_novel_patterns
            ;;
        report)
            generate_report
            ;;
        all)
            count_patterns
            list_patterns
            list_meta_patterns
            tier_coverage
            detect_orphans
            generate_report
            ;;
        *)
            echo -e "${YELLOW}Usage:${NC}"
            echo "  find-patterns.sh count     - Count patterns and meta-patterns"
            echo "  find-patterns.sh list      - List all patterns"
            echo "  find-patterns.sh meta      - List meta-patterns"
            echo "  find-patterns.sh search <keyword> - Search patterns"
            echo "  find-patterns.sh orphans   - Detect orphaned patterns"
            echo "  find-patterns.sh tiers     - Analyze tier coverage"
            echo "  find-patterns.sh novel     - Detect novel co-access patterns"
            echo "  find-patterns.sh report    - Generate full report"
            echo "  find-patterns.sh all       - Run all analyses"
            ;;
    esac
}

main "$@"
