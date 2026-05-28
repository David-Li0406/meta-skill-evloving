#!/bin/bash
# cognitive-state-check.sh
# Assess cognitive state and suggest transitions

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <recent_output_file> [mode]"
    echo ""
    echo "Arguments:"
    echo "  recent_output_file - File containing recent reasoning output"
    echo "  mode               - 'assess' (default) or 'recommend'"
    echo ""
    echo "Analyzes cognitive state: Biased/Focused/Diversified/Dispersed"
    exit 1
fi

INPUT_FILE="$1"
MODE="${2:-assess}"

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File not found: $INPUT_FILE"
    exit 1
fi

echo "=== COGNITIVE STATE CHECK ==="
echo "Analyzing: $INPUT_FILE"
echo ""

# Read content
content=$(cat "$INPUT_FILE")

# Measure connection density
echo "Step 1: Measuring Connection Density"
echo ""

# Count concepts (simplified - count unique important words)
concept_count=$(echo "$content" | grep -oE '\b[A-Z][a-z]{4,}\b' | sort -u | wc -l)
echo "  Concepts identified: $concept_count"

# Count connections (simplified - count connecting words)
connection_words="therefore|thus|because|leads to|results in|implies|suggests|connected|related"
connection_count=$(echo "$content" | grep -oiE "$connection_words" | wc -l)
echo "  Connections identified: $connection_count"

# Calculate density
if [ $concept_count -gt 0 ]; then
    density=$(echo "scale=2; $connection_count / $concept_count" | bc)
else
    density=0
fi

echo "  Connection density: $density"

# Classify density
if (( $(echo "$density > 0.5" | bc -l) )); then
    density_class="High"
    echo "  Classification: High (dense local connections)"
else
    density_class="Low"
    echo "  Classification: Low (sparse connections)"
fi

echo ""

# Detect narrative arc
echo "Step 2: Detecting Narrative Arc"
echo ""

# Check for progression indicators
progression_words="first|second|then|next|finally|leads to|therefore"
progression_count=$(echo "$content" | grep -oiE "$progression_words" | wc -l)
echo "  Progression indicators: $progression_count"

# Check for coherent direction
direction_words="toward|goal|conclusion|synthesis|result"
direction_count=$(echo "$content" | grep -oiE "$direction_words" | wc -l)
echo "  Direction indicators: $direction_count"

# Check for unifying theme (repeated key concepts)
key_concept=$(echo "$content" | grep -oE '\b[A-Z][a-z]{4,}\b' | sort | uniq -c | sort -rn | head -1 | awk '{print $2}')
key_concept_count=$(echo "$content" | grep -oE '\b[A-Z][a-z]{4,}\b' | sort | uniq -c | sort -rn | head -1 | awk '{print $1}')
echo "  Dominant concept: $key_concept (appears $key_concept_count times)"

# Classify arc
arc_score=$((progression_count + direction_count))
if [ $arc_score -ge 5 ] && [ "$key_concept_count" -ge 3 ]; then
    arc_class="Present"
    echo "  Classification: Present (coherent narrative arc)"
else
    arc_class="Absent"
    echo "  Classification: Absent (no clear narrative arc)"
fi

echo ""

# Determine cognitive state
echo "Step 3: Cognitive State Determination"
echo ""

if [ "$density_class" = "High" ] && [ "$arc_class" = "Present" ]; then
    STATE="Focused"
    COLOR="\033[0;32m" # Green
    STATUS="✓ OPTIMAL"
elif [ "$density_class" = "High" ] && [ "$arc_class" = "Absent" ]; then
    STATE="Biased"
    COLOR="\033[0;33m" # Yellow
    STATUS="⚠ NEEDS DIVERSIFICATION"
elif [ "$density_class" = "Low" ] && [ "$arc_class" = "Present" ]; then
    STATE="Diversified"
    COLOR="\033[0;34m" # Blue
    STATUS="✓ CREATIVE EXPLORATION"
else
    STATE="Dispersed"
    COLOR="\033[0;31m" # Red
    STATUS="⚠ REQUIRES CONSOLIDATION"
fi

echo -e "Cognitive State: ${COLOR}${STATE}${NC}"
echo -e "Status: ${STATUS}"
echo ""

# Generator pattern analysis
echo "Step 4: Generator Pattern Analysis"
echo ""

case "$STATE" in
    Focused)
        echo "  Generator Pattern: Balanced (all G1-G7 healthy)"
        echo "  G1: ✓ Iteration advancing (not looping)"
        echo "  G2: ✓ Contrasts informing synthesis"
        echo "  G6: ✓ Distinctions maintained"
        ;;
    Biased)
        echo "  Generator Pattern: G1 overactive, G2/G4/G6 suppressed"
        echo "  G1: ✗ Endless iteration without progress"
        echo "  G2: ✗ No contrast sought (tunnel vision)"
        echo "  G4: ✗ Ignoring alternative sources"
        echo "  G6: ✗ Risk of forcing collapse"
        ;;
    Diversified)
        echo "  Generator Pattern: G2/G4 elevated, G1/G5 moderate"
        echo "  G2: ✓ Actively seeking contrast"
        echo "  G4: ✓ Multi-source exploration"
        echo "  G1: ○ Iterating across domains (not within)"
        ;;
    Dispersed)
        echo "  Generator Pattern: All generators weak/inconsistent"
        echo "  G1: ✗ Random iteration"
        echo "  G2: ✗ No maintained contrasts"
        echo "  G6: ✗ No preserved structure"
        ;;
esac

echo ""

# Recommendations
if [ "$MODE" = "recommend" ] || [ "$STATE" != "Focused" ]; then
    echo "=== RECOMMENDATIONS ==="
    echo ""
    
    case "$STATE" in
        Focused)
            echo "Action: MAINTAIN current state"
            echo ""
            echo "This is optimal for:"
            echo "  • Derivation work (Enhanced Dokkado Phase 3)"
            echo "  • Synthesis (combining patterns)"
            echo "  • Theory building"
            echo ""
            echo "Warnings:"
            echo "  • Monitor for exhaustion (~90 min limit)"
            echo "  • Run periodic supercollider checks"
            echo "  • Prepare transition after extended session"
            ;;
            
        Biased)
            echo "Action: FORCE DIVERSIFICATION"
            echo ""
            echo "Immediate steps:"
            echo "  1. Run diffusion reasoning with high novelty (0.8)"
            echo "     ./diffusion-explore.sh '<current_concept>' 7 0.8 0.2 0.5"
            echo ""
            echo "  2. Require G2 application"
            echo "     • Find contrasting perspective"
            echo "     • Seek disconfirming evidence"
            echo ""
            echo "  3. Require G4 checks"
            echo "     • Consult independent sources"
            echo "     • Different methodologies"
            echo ""
            echo "Goal: Transition to Diversified state"
            ;;
            
        Diversified)
            echo "Action: CONTINUE EXPLORATION"
            echo ""
            echo "This state is good for:"
            echo "  • Discovery and exploration"
            echo "  • Pattern matching across domains"
            echo "  • Creative breakthroughs"
            echo ""
            echo "When ready to consolidate:"
            echo "  • Run synthesis engine on discoveries"
            echo "  • Apply Enhanced Dokkado Phase 2 (pattern matching)"
            echo "  • Transition to Focused for derivation"
            echo ""
            echo "Maintain with balanced diffusion (0.5/0.5)"
            ;;
            
        Dispersed)
            echo "Action: EMERGENCY CONSOLIDATION"
            echo ""
            echo "Immediate steps:"
            echo "  1. STOP current diffusion/exploration"
            echo ""
            echo "  2. Identify strongest thread"
            echo "     • Run supercollider on all threads"
            echo "     • Pick highest scoring concept"
            echo ""
            echo "  3. Narrow focus with high-relevance diffusion"
            echo "     ./diffusion-explore.sh '<strongest_thread>' 3 0.2 0.8 0.7"
            echo ""
            echo "  4. Build connections"
            echo "     • Use synthesis engine to connect discoveries"
            echo "     • Look for unifying morphemes/generators"
            echo ""
            echo "Goal: Biased (one coherent thread) → Focused (add arc)"
            ;;
    esac
    
    echo ""
fi

echo "=== COMPLETE ==="
echo ""
echo "Current State: $STATE"
echo "Recommended Mode: $(case "$STATE" in
    Focused) echo "Enhanced Dokkado / Synthesis Engine" ;;
    Biased) echo "Diffusion Reasoning (high novelty)" ;;
    Diversified) echo "Pattern Matching / Balanced Diffusion" ;;
    Dispersed) echo "Consolidation / High-relevance Diffusion" ;;
esac)"
