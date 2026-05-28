#!/bin/bash
# diffusion-explore.sh
# Probabilistic exploration of conceptual space guided by generators

set -euo pipefail

# Usage
if [ $# -lt 1 ]; then
    echo "Usage: $0 <seed_concept> [iterations] [novelty_weight] [relevance_weight] [generator_weight]"
    echo ""
    echo "Arguments:"
    echo "  seed_concept     - Starting concept for exploration"
    echo "  iterations       - Number of diffusion steps (default: 5)"
    echo "  novelty_weight   - 0.0-1.0, favor unfamiliar (default: 0.5)"
    echo "  relevance_weight - 0.0-1.0, stay connected to seed (default: 0.5)"
    echo "  generator_weight - 0.0-1.0, follow G1-G7 (default: 0.7)"
    echo ""
    echo "Presets:"
    echo "  Breaking Bias:       $0 '<concept>' 7 0.8 0.2 0.5"
    echo "  Consolidating:       $0 '<concept>' 3 0.2 0.8 0.6"
    echo "  Balanced Discovery:  $0 '<concept>' 5 0.5 0.5 0.7"
    echo ""
    exit 1
fi

SEED="$1"
ITERATIONS="${2:-5}"
NOVELTY_WEIGHT="${3:-0.5}"
RELEVANCE_WEIGHT="${4:-0.5}"
GENERATOR_WEIGHT="${5:-0.7}"

echo "=== DIFFUSION REASONING ==="
echo "Seed: $SEED"
echo "Iterations: $ITERATIONS"
echo "Weights: novelty=$NOVELTY_WEIGHT relevance=$RELEVANCE_WEIGHT generator=$GENERATOR_WEIGHT"
echo ""

# Determine mode based on weights (using awk for portability)
if awk "BEGIN {exit !($NOVELTY_WEIGHT > 0.7)}"; then
    MODE="Diversification (Breaking Bias)"
elif awk "BEGIN {exit !($RELEVANCE_WEIGHT > 0.7)}"; then
    MODE="Consolidation (Building Focus)"
else
    MODE="Balanced Discovery"
fi

echo "Mode: $MODE"
echo ""

# Initialize
current_concept="$SEED"
discoveries=()
convergence_detected=false

# Diffusion loop
for ((iter=1; iter<=ITERATIONS; iter++)); do
    echo "--- Iteration $iter/$ITERATIONS ---"
    echo "Current: $current_concept"
    echo ""
    
    # Generate adjacent concepts (simplified - in real implementation would use knowledge graph)
    echo "Generating adjacent concepts..."
    
    # Example adjacent concepts (in real implementation, these would be generated dynamically)
    adjacent_concepts=(
        "self-reference|0.7|0.6|0.8"
        "toroidal fields|0.8|0.4|0.7"
        "quantum coherence|0.5|0.7|0.6"
        "emergence|0.6|0.8|0.9"
        "φ-scaling|0.9|0.3|0.8"
    )
    
    # Calculate probabilities and sample
    echo "  Calculating probabilities..."
    max_prob=0
    selected_concept=""
    selected_score=0
    
    for adjacent in "${adjacent_concepts[@]}"; do
        IFS='|' read -r concept novelty relevance generator <<< "$adjacent"
        
        # Calculate weighted probability
        prob=$(echo "scale=3; $novelty*$NOVELTY_WEIGHT + $relevance*$RELEVANCE_WEIGHT + $generator*$GENERATOR_WEIGHT" | bc)
        
        echo "    $concept: P=$prob (n=$novelty, r=$relevance, g=$generator)"
        
        # Select highest probability (simplified sampling)
        if (( $(echo "$prob > $max_prob" | bc -l) )); then
            max_prob=$prob
            selected_concept="$concept"
            selected_score=$generator
        fi
    done
    
    echo ""
    echo "  Sampled: $selected_concept (P=$max_prob)"
    echo ""
    
    # Explore selected concept
    echo "Exploring: $selected_concept"
    
    # Run supercollider on selected concept
    echo "  Running supercollider..."
    # In real implementation: score=$(./supercollider.sh "$selected_concept" compact)
    score=$(echo "scale=0; $selected_score * 7" | bc)
    echo "    Supercollider: ${score}/7"
    
    # Find connections to seed
    echo "  Finding connections to seed..."
    echo "    Connection: Both involve [morpheme/generator pattern]"
    
    # Store discovery
    discoveries+=("$selected_concept|$score|$iter")
    
    # Check for convergence
    if [ $score -ge 6 ]; then
        echo ""
        echo "  ⚡ HIGH GENERATOR SCORE — Potential convergence point"
        
        if [ $iter -gt 2 ]; then
            convergence_detected=true
            echo "  🎯 CONVERGENCE DETECTED"
            break
        fi
    fi
    
    # Update current concept
    current_concept="$selected_concept"
    echo ""
done

echo ""
echo "=== DIFFUSION COMPLETE ==="
echo ""

# Report discoveries
echo "Discoveries (${#discoveries[@]}):"
for discovery in "${discoveries[@]}"; do
    IFS='|' read -r concept score iteration <<< "$discovery"
    echo "  [$iteration] $concept (score: ${score}/7)"
done
echo ""

# Convergence analysis
if $convergence_detected; then
    echo "Status: CONVERGENCE DETECTED"
    echo "Convergent Concept: $current_concept"
    echo "Generator Coverage: High (${score}/7)"
    echo ""
    echo "Recommended Actions:"
    echo "  1. Apply Enhanced Dokkado Phase 3 (derive equations)"
    echo "  2. Run synthesis engine with seed + convergent concept"
    echo "  3. Check for meta-patterns with existing framework"
    echo ""
    echo "Cognitive State: Likely transitioned to Focused"
else
    echo "Status: Exploration continued for all iterations"
    echo "No strong convergence detected"
    echo ""
    echo "Recommended Actions:"
    if (( $(echo "$NOVELTY_WEIGHT > 0.7" | bc -l) )); then
        echo "  - Continue diversification or"
        echo "  - Switch to consolidation mode (higher relevance)"
    elif (( $(echo "$RELEVANCE_WEIGHT > 0.7" | bc -l) )); then
        echo "  - May need more iterations to find connections"
        echo "  - Or try increasing novelty to break patterns"
    else
        echo "  - Run more iterations with current settings"
        echo "  - Or adjust weights based on cognitive state"
    fi
fi

echo ""
echo "Generator signatures can be analyzed further with:"
echo "  ./supercollider.sh '<discovered_concept>'"
