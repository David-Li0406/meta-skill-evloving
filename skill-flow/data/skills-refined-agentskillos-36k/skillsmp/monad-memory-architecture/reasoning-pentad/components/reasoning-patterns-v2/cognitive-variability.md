# Cognitive Variability Integration

**Purpose:** State-aware reasoning that adapts to cognitive context, integrating with the cognitive-variability skill for optimal reasoning mode selection.

---

## Core Integration

This file extends the standalone `cognitive-variability` skill by mapping its four states (Biased/Focused/Diversified/Dispersed) to specific reasoning-patterns-v2 modes and generator patterns.

**Key Insight:** Cognitive state affects which generators (G1-G7) dominate thinking, and optimal reasoning requires state-appropriate tool selection.

---

## The Four States with Generator Signatures

### State 1: BIASED

**Characteristics:**
- Dense local connections (high connection density)
- No narrative arc
- Single thread dominates
- Tunnel vision

**Generator Pattern:**
- **Overactive:** G1 (iteration) without G2 (contrast)
- **Suppressed:** G4 (independent validation), G6 (distinction preservation)
- **Result:** Recursive drilling without breadth

**Reasoning Mode Problems:**
- Supercollider: Inflates scores (sees generators everywhere)
- Dokkado: Stuck in Phase 1-2 loop (never advances)
- Synthesis: Forces collapse (ignores G6)
- Diffusion: Refuses to explore (high relevance weight only)

**Optimal Action:**
- **Activate:** Diffusion reasoning with HIGH novelty weight (0.7-0.9)
- **Force:** G2 application (find contrasts)
- **Require:** G4 checks (seek independent sources)
- **Goal:** Transition to Diversified state

**Transition Strategy:**
```bash
if detect_state == "Biased"; then
    echo "⚠️ BIASED STATE DETECTED"
    echo "Action: Activating diversification protocols"
    
    # Force diffusion with high novelty
    ./diffusion-explore.sh "$current_concept" 7 0.85 0.15 0.5
    
    # Require G2 and G4 checks
    echo "Must find: Contrasting perspective (G2)"
    echo "Must find: Independent validation (G4)"
    
    # Monitor for arc emergence
    check_narrative_arc_after_iterations 3
fi
```

### State 2: FOCUSED

**Characteristics:**
- Dense connections + narrative arc
- Productive synthesis
- Flow state
- Coherent progress

**Generator Pattern:**
- **Balanced:** All G1-G7 apply appropriately
- **Healthy G1:** Iteration advances, doesn't loop
- **Active G6:** Distinctions preserved during synthesis
- **Result:** Optimal derivation and integration

**Reasoning Mode Performance:**
- Supercollider: Accurate assessments
- Dokkado: Smooth progression through phases
- Synthesis: Respects G6, finds resonance
- Diffusion: Minimal (targeted exploration only)

**Optimal Action:**
- **MAINTAIN STATE** — don't disrupt
- Continue current reasoning mode
- Use supercollider to validate progress
- Minimal diffusion (only for specific gaps)

**Maintenance Strategy:**
```bash
if detect_state == "Focused"; then
    echo "✓ FOCUSED STATE — OPTIMAL"
    echo "Action: Maintaining current approach"
    
    # Continue with current mode
    # Periodic supercollider checks
    if [ $((steps % 5)) -eq 0 ]; then
        supercollider_check "$current_synthesis"
    fi
    
    # Monitor for exhaustion
    if time_in_focused > 90_minutes; then
        echo "⚠️ Approaching exhaustion, prepare for transition"
        prepare_consolidation
    fi
fi
```

### State 3: DIVERSIFIED

**Characteristics:**
- Sparse connections + narrative arc
- Creative exploration
- Multiple threads with coherent direction
- Discovery mode

**Generator Pattern:**
- **High G2:** Actively seeking contrast
- **High G4:** Multi-source exploration
- **Moderate G1:** Iteration across domains, not within
- **Result:** Breadth with coherence

**Reasoning Mode Performance:**
- Supercollider: Good for assessing discoveries
- Dokkado: Phase 2 (Water) excels — pattern matching
- Synthesis: Discovers patterns to synthesize
- Diffusion: OPTIMAL — balanced exploration

**Optimal Action:**
- **Maintain for discovery work**
- Use diffusion with balanced weights
- Run supercollider on discoveries
- Prepare to transition to Focused for synthesis

**Discovery Strategy:**
```bash
if detect_state == "Diversified"; then
    echo "✓ DIVERSIFIED STATE — CREATIVE EXPLORATION"
    echo "Action: Continuing discovery with structure"
    
    # Balanced diffusion
    ./diffusion-explore.sh "$seed" 5 0.5 0.5 0.7
    
    # Supercollider on discoveries
    for discovery in "${discoveries[@]}"; do
        score=$(supercollider "$discovery")
        if [ "$score" -ge 5 ]; then
            high_value_discoveries+=("$discovery")
        fi
    done
    
    # When ready, consolidate
    if sufficient_discoveries; then
        echo "→ Transitioning to Focused for synthesis"
        transition_to_focused
    fi
fi
```

### State 4: DISPERSED

**Characteristics:**
- Sparse connections, no arc
- Scattered thinking
- Random exploration
- No coherence

**Generator Pattern:**
- **Inconsistent:** Generators apply randomly
- **Weak G1:** No iterative structure
- **Absent G6:** No maintained distinctions
- **Result:** Chaos without productivity

**Reasoning Mode Problems:**
- Supercollider: Unreliable (can't assess coherence)
- Dokkado: Can't complete phases
- Synthesis: Produces incoherent results
- Diffusion: Makes things worse (more scatter)

**Optimal Action:**
- **Consolidate immediately**
- STOP diffusion
- Pick ONE thread (activate Biased if necessary)
- Use high-relevance diffusion to find connections
- Transition to Focused ASAP

**Recovery Strategy:**
```bash
if detect_state == "Dispersed"; then
    echo "⚠️ DISPERSED STATE — REQUIRES CONSOLIDATION"
    echo "Action: Emergency consolidation protocols"
    
    # STOP current activities
    stop_diffusion
    
    # Identify strongest thread
    strongest_thread=$(find_highest_generator_score "$all_threads")
    
    # Narrow focus
    echo "Narrowing to: $strongest_thread"
    
    # High-relevance diffusion to connect
    ./diffusion-explore.sh "$strongest_thread" 3 0.2 0.8 0.7
    
    # Goal: Biased (at least one coherent thread)
    # Then: Biased → Diversified → Focused
    
    if arc_emerges; then
        echo "→ Arc detected, transitioning to Focused"
        transition_to_focused
    elif single_thread_strong; then
        echo "→ Single thread established (Biased)"
        echo "Next: Diversify from this foundation"
    fi
fi
```

---

## State Detection Implementation

### Connection Density Measurement

```bash
measure_connection_density() {
    local recent_output="$1"
    
    # Extract concepts
    concepts=$(extract_concepts "$recent_output")
    num_concepts=$(echo "$concepts" | wc -l)
    
    # Count connections between concepts
    connections=0
    for concept_a in $concepts; do
        for concept_b in $concepts; do
            if [ "$concept_a" = "$concept_b" ]; then continue; fi
            if concepts_connected "$concept_a" "$concept_b" "$recent_output"; then
                connections=$((connections + 1))
            fi
        done
    done
    
    # Calculate density
    max_connections=$((num_concepts * (num_concepts - 1)))
    if [ "$max_connections" -gt 0 ]; then
        density=$(echo "scale=2; $connections / $max_connections" | bc)
    else
        density=0
    fi
    
    # Classify
    if (( $(echo "$density > 0.5" | bc -l) )); then
        echo "High"
    else
        echo "Low"
    fi
}
```

### Narrative Arc Detection

```bash
detect_narrative_arc() {
    local recent_output="$1"
    
    # Check for:
    # 1. Clear progression (concepts build on each other)
    # 2. Coherent direction (moving toward conclusion)
    # 3. Unifying theme (common thread)
    
    has_progression=$(check_concept_building "$recent_output")
    has_direction=$(check_coherent_direction "$recent_output")
    has_theme=$(check_unifying_theme "$recent_output")
    
    if [ "$has_progression" = "yes" ] && \
       [ "$has_direction" = "yes" ] && \
       [ "$has_theme" = "yes" ]; then
        echo "Present"
    else
        echo "Absent"
    fi
}
```

### Complete State Detection

```bash
detect_cognitive_state() {
    local recent_output="$1"
    
    density=$(measure_connection_density "$recent_output")
    arc=$(detect_narrative_arc "$recent_output")
    
    if [ "$density" = "High" ] && [ "$arc" = "Present" ]; then
        echo "Focused"
    elif [ "$density" = "High" ] && [ "$arc" = "Absent" ]; then
        echo "Biased"
    elif [ "$density" = "Low" ] && [ "$arc" = "Present" ]; then
        echo "Diversified"
    else
        echo "Dispersed"
    fi
}
```

---

## State-Aware Mode Selection

### Automatic Mode Selection

```bash
select_reasoning_mode() {
    local task="$1"
    local current_state="$2"
    
    case "$current_state" in
        "Focused")
            # Optimal for derivation and synthesis
            if [ "$task" = "derive" ] || [ "$task" = "synthesize" ]; then
                echo "enhanced_dokkado"
            elif [ "$task" = "assess" ]; then
                echo "supercollider"
            else
                echo "maintain_current"
            fi
            ;;
            
        "Biased")
            # Need diversification
            if [ "$task" = "derive" ]; then
                echo "WARN: Biased state not optimal for derivation"
                echo "ACTION: Force diversification first"
                echo "MODE: diffusion_high_novelty"
            else
                echo "diffusion_high_novelty"
            fi
            ;;
            
        "Diversified")
            # Optimal for discovery
            if [ "$task" = "discover" ] || [ "$task" = "explore" ]; then
                echo "diffusion_balanced"
            elif [ "$task" = "assess" ]; then
                echo "supercollider"
            elif [ "$task" = "synthesize" ]; then
                echo "WARN: Consider consolidating to Focused first"
                echo "MODE: synthesis_engine_with_prep"
            fi
            ;;
            
        "Dispersed")
            # Emergency consolidation
            echo "WARN: Dispersed state requires consolidation"
            echo "ACTION: Narrow focus immediately"
            echo "MODE: consolidation_protocol"
            ;;
    esac
}
```

### State Transition Triggers

```bash
check_transition_needed() {
    local current_state="$1"
    local time_in_state="$2"
    local progress_metric="$3"
    
    case "$current_state" in
        "Focused")
            # Exhaustion check
            if [ "$time_in_state" -gt 90 ]; then
                echo "TRANSITION: Focused → Break (exhaustion)"
                return 0
            fi
            # Stuck check
            if [ "$progress_metric" = "stuck" ]; then
                echo "TRANSITION: Focused → Diversified (need breadth)"
                return 0
            fi
            ;;
            
        "Biased")
            # Always needs transition
            echo "TRANSITION: Biased → Diversified (forced)"
            return 0
            ;;
            
        "Diversified")
            # Ready to synthesize?
            if [ "$progress_metric" = "sufficient_discoveries" ]; then
                echo "TRANSITION: Diversified → Focused (synthesis)"
                return 0
            fi
            # Too long without consolidation?
            if [ "$time_in_state" -gt 60 ]; then
                echo "TRANSITION: Diversified → Focused (consolidate)"
                return 0
            fi
            ;;
            
        "Dispersed")
            # Always needs immediate transition
            echo "TRANSITION: Dispersed → Focused or Biased (emergency)"
            return 0
            ;;
    esac
    
    return 1  # No transition needed
}
```

---

## Generator-State Correlation

### Healthy Generator Patterns by State

**Focused State:**
```
G1: ✓ Active, advancing (not looping)
G2: ✓ Preserved contrasts inform synthesis
G3: ✓ Morphemes clear and applied
G4: ✓ Multiple sources considered
G5: ✓ Derivations rigorous
G6: ✓ Distinctions maintained
G7: ✓ Scaling patterns recognized

Pattern: All generators balanced and productive
```

**Diversified State:**
```
G1: ○ Moderate (iterating across, not within)
G2: ✓ High (actively seeking contrast)
G3: ○ Moderate (morphemes emerging)
G4: ✓ High (multi-source exploration)
G5: ○ Low (not yet deriving)
G6: ✓ Active (preserving alternatives)
G7: ○ Moderate (noting patterns)

Pattern: G2 and G4 elevated, G1 and G5 lower
```

**Biased State:**
```
G1: ✗ Overactive (endless iteration)
G2: ✗ Suppressed (no contrast sought)
G3: ○ Moderate (limited morphemes)
G4: ✗ Suppressed (ignoring alternatives)
G5: ○ Maybe (derivation in limited scope)
G6: ✗ Violated (forcing collapse)
G7: ○ May be present

Pattern: G1 high, G2/G4/G6 suppressed
```

**Dispersed State:**
```
G1: ✗ Inconsistent (random iteration)
G2: ✗ Absent (no maintained contrasts)
G3: ✗ Unclear (morphemes scattered)
G4: ✗ Absent (no systematic sourcing)
G5: ✗ Absent (no derivation)
G6: ✗ Violated (no preserved structure)
G7: ✗ Absent (no pattern recognition)

Pattern: All generators weak or inconsistent
```

### Diagnostic Generator Checks

```bash
diagnose_state_from_generators() {
    local g1_strength="$1"
    local g2_strength="$2"
    local g4_strength="$3"
    local g6_strength="$4"
    
    # Focused: All balanced
    if [ "$g1_strength" = "moderate" ] && \
       [ "$g2_strength" = "moderate" ] && \
       [ "$g4_strength" = "moderate" ] && \
       [ "$g6_strength" = "high" ]; then
        echo "Focused"
        return
    fi
    
    # Biased: G1 high, G2/G4/G6 low
    if [ "$g1_strength" = "high" ] && \
       [ "$g2_strength" = "low" ] && \
       [ "$g4_strength" = "low" ]; then
        echo "Biased"
        return
    fi
    
    # Diversified: G2/G4 high, G1 moderate
    if [ "$g2_strength" = "high" ] && \
       [ "$g4_strength" = "high" ] && \
       [ "$g1_strength" = "moderate" ]; then
        echo "Diversified"
        return
    fi
    
    # Dispersed: All low or inconsistent
    if [ "$g1_strength" = "low" ] && \
       [ "$g2_strength" = "low" ]; then
        echo "Dispersed"
        return
    fi
    
    echo "Unknown"
}
```

---

## Practical Integration

### Example: Dokkado with State Awareness

```bash
run_dokkado_with_state_awareness() {
    local initial_state=$(detect_cognitive_state "$context")
    
    echo "Initial State: $initial_state"
    
    case "$initial_state" in
        "Biased")
            echo "⚠️ Not optimal for Dokkado"
            echo "Recommend: Diversify first"
            echo ""
            read -p "Proceed anyway? (y/n) " proceed
            if [ "$proceed" != "y" ]; then
                echo "Running diversification..."
                diversify_then_dokkado
                return
            fi
            ;;
            
        "Dispersed")
            echo "⚠️ Cannot run Dokkado in Dispersed state"
            echo "Consolidating first..."
            consolidate_then_dokkado
            return
            ;;
            
        "Focused"|"Diversified")
            echo "✓ Good state for Dokkado"
            ;;
    esac
    
    # Run Dokkado phases with state monitoring
    for phase in {1..5}; do
        echo "=== Phase $phase ==="
        state=$(detect_cognitive_state "$current_context")
        
        if [ "$state" = "Dispersed" ]; then
            echo "⚠️ State degraded to Dispersed"
            echo "Pausing to consolidate"
            consolidate
        fi
        
        run_dokkado_phase "$phase"
    done
}
```

### Example: Synthesis with State Check

```bash
synthesize_with_state_check() {
    local pattern_a="$1"
    local pattern_b="$2"
    
    state=$(detect_cognitive_state "$recent_work")
    
    if [ "$state" != "Focused" ]; then
        echo "⚠️ Synthesis works best in Focused state"
        echo "Current state: $state"
        echo ""
        
        if [ "$state" = "Diversified" ]; then
            echo "Consolidating discoveries..."
            consolidate_diversified_to_focused
        elif [ "$state" = "Biased" ]; then
            echo "Diversifying first, then consolidating..."
            biased_to_focused_via_diversified
        elif [ "$state" = "Dispersed" ]; then
            echo "Emergency consolidation required"
            return 1
        fi
    fi
    
    echo "✓ Focused state achieved"
    ./synthesize-patterns.sh "$pattern_a" "$pattern_b"
}
```

---

## Summary

**Cognitive-variability integration provides:**
- State-aware mode selection
- Generator pattern diagnostics
- Automatic transition triggers
- State-optimized reasoning

**Key mappings:**
- Focused → All modes optimal
- Diversified → Diffusion, discovery optimal
- Biased → Force diversification
- Dispersed → Emergency consolidation

**Use for:**
- Detecting when reasoning is suboptimal
- Selecting appropriate reasoning mode
- Triggering state transitions
- Maintaining productive flow

**Remember:**
- State affects which generators dominate
- Optimal state depends on task
- Transitions are necessary, not failures
- Focused is optimal but unsustainable long-term

---

**Cognitive variability isn't a bug—it's how consciousness explores and consolidates. We make it conscious and deliberate.** 🧠🌊🔥
