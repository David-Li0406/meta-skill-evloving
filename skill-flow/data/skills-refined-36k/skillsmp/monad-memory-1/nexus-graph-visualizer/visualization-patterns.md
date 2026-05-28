# Visualization Patterns — ASCII Art Generation

**ASCII art patterns for toroidal field visualization.**

---

## Toroidal Topology

Skills arranged by cognitive tier create a torus (donut) structure:
- **φ-tier (innermost)** = seed/self-reference
- **π-tier** = structural frameworks
- **e-tier** = current/active work
- **i-tier (outermost)** = deep integration/mastery

Coherence loops = closed geodesics on the torus surface.

---

## Box Drawing Characters

### Basic Elements

```
Horizontal: ─ ═
Vertical:   │ ║
Corners:    ┌ ┐ └ ┘  ╔ ╗ ╚ ╝
T-joints:   ├ ┤ ┬ ┴  ╠ ╣ ╦ ╩
Cross:      ┼ ╬
```

### Arrows and Connections

```
Simple:     → ← ↑ ↓
Double:     ⇒ ⇐ ⇑ ⇓
Curved:     ↱ ↲ ↳ ↴
Bidirect:   ↔ ⇔ ↕ ⇕
Circular:   ↺ ↻
```

### Progress Indicators

```
Blocks:     █ ▓ ▒ ░
Partial:    ▏ ▎ ▍ ▌ ▋ ▊ ▉ █
Arrows:     ▶ ▷ ▸ ▹ ► ▻
Circles:    ● ○ ◉ ◎
```

---

## Visualization Templates

### Template 1: Vertical Tier Layout

```
        ╔═══════ φ-tier (seed) ═══════╗
        ║                             ║
        ║   [skill1]   [skill2]       ║
        ║        ↓↑         ↓          ║
        ╠═══════ π-tier (struct) ══════╣
        ║                             ║
        ║   [skill3] ←→ [skill4]      ║
        ║        ↓↑         ↓          ║
        ╠═══════ e-tier (current) ═════╣
        ║                             ║
        ║   [skill5] ←→ [skill6]      ║
        ║        ↓↑         ↓          ║
        ╠═══════ i-tier (deep) ════════╣
        ║                             ║
        ║        [skill7]              ║
        ║                             ║
        ╚═════════════════════════════╝
```

### Template 2: Circular Arrangement

```
                  [φ-tier]
                gremlin-brain
                      ↓
          ┌───────────┼───────────┐
          ↓                       ↓
    [π-tier]                [π-tier]
   boot-seq                 the-guy
          ↓                       ↓
          └───────────┬───────────┘
                      ↓
                 [e-tier]
              nexus-core
```

### Template 3: Connection Matrix

```
           boot  grem  guy   core  mind
boot-seq    •     ↓     ↓     ↓     ↓
gremlin     ↑     •     ←     ←     ←
the-guy     ↑     →     •     ↓     ↓
nexus-core  ↑     →     ↑     •     ←
nexus-mind  ↑     →     ↑     →     •
```

### Template 4: Field Strength Heatmap

```
Connection Density by Tier:

φ-tier: ████████████████░░░░  80%
π-tier: ██████████████████░░  90%
e-tier: ████████████░░░░░░░░  60%
i-tier: ██████░░░░░░░░░░░░░░  30%

Overall Field Strength: ████████░░  75%
```

---

## Algorithm: Generate Tier Layout

```bash
generate_tier_layout() {
    local graph_file="$1"
    
    # Group skills by tier
    declare -A tiers
    while IFS='|' read -r skill tier rest; do
        tiers[$tier]+="$skill "
    done < "$graph_file"
    
    # Generate layout
    echo "        ╔═══ φ-tier (seed) ═══╗"
    for skill in ${tiers[φ]}; do
        echo "        ║   $(printf '%-18s' "$skill")║"
    done
    echo "        ║         ↓↑           ║"
    
    echo "        ╠═══ π-tier (struct) ══╣"
    for skill in ${tiers[π]}; do
        echo "        ║   $(printf '%-18s' "$skill")║"
    done
    echo "        ║         ↓↑           ║"
    
    echo "        ╠═══ e-tier (current) ═╣"
    for skill in ${tiers[e]}; do
        echo "        ║   $(printf '%-18s' "$skill")║"
    done
    echo "        ║         ↓↑           ║"
    
    echo "        ╠═══ i-tier (deep) ════╣"
    for skill in ${tiers[i]}; do
        echo "        ║   $(printf '%-18s' "$skill")║"
    done
    echo "        ╚═══════════════════════╝"
}
```

---

## Algorithm: Draw Connection Lines

```bash
draw_connections() {
    local skill1="$1"
    local skill2="$2"
    local type="$3"  # explicit, reference, implicit
    
    # Determine arrow style based on type
    case "$type" in
        explicit)   arrow="⇒" ;;
        reference)  arrow="→" ;;
        implicit)   arrow="⋯→" ;;
    esac
    
    # Draw connection
    echo "$skill1 $arrow $skill2"
}

draw_bidirectional() {
    local skill1="$1"
    local skill2="$2"
    
    echo "$skill1 ⇔ $skill2"
}

draw_loop() {
    local -a skills=("$@")
    
    echo "Loop: ${skills[0]}"
    for ((i=1; i<${#skills[@]}; i++)); do
        echo "  ↓"
        echo "  ${skills[i]}"
    done
    echo "  ↓"
    echo "  ${skills[0]} (completes loop)"
}
```

---

## Algorithm: Field Strength Calculation

```bash
calculate_field_strength() {
    local total_skills="$1"
    local total_connections="$2"
    
    # Field strength = connections per skill
    local avg_connections=$((total_connections / total_skills))
    
    # Normalize to 0-100 scale (assume max 10 connections per skill)
    local normalized=$((avg_connections * 10))
    [[ $normalized -gt 100 ]] && normalized=100
    
    echo "$normalized"
}

draw_progress_bar() {
    local value="$1"  # 0-100
    local width="${2:-10}"  # bar width
    
    local filled=$((value * width / 100))
    local empty=$((width - filled))
    
    printf "█%.0s" $(seq 1 $filled)
    printf "░%.0s" $(seq 1 $empty)
    printf " %d%%" "$value"
}
```

---

## Algorithm: Hub Visualization

```bash
visualize_hubs() {
    local -A degree
    
    # Calculate in-degree for each skill
    while IFS='→' read -r from to rest; do
        degree[$to]=$((${degree[$to]:-0} + 1))
    done < edges.txt
    
    # Sort and display top hubs
    echo "=== Hub Skills ==="
    for skill in "${!degree[@]}"; do
        echo "${degree[$skill]} $skill"
    done | sort -rn | head -5 | while read count skill; do
        # Visual representation of hub size
        local stars=$(printf "★%.0s" $(seq 1 $count))
        echo "$skill: $stars ($count connections)"
    done
}
```

---

## Algorithm: Loop Visualization

```bash
visualize_loop() {
    local loop_file="$1"
    
    # Read loop nodes
    local -a nodes
    while read -r node; do
        nodes+=("$node")
    done < "$loop_file"
    
    # Calculate loop properties
    local length=${#nodes[@]}
    local -a tiers
    for node in "${nodes[@]}"; do
        tier=$(get_tier "$node")
        tiers+=("$tier")
    done
    
    # Draw loop
    echo "🔄 Autopoietic Loop (length: $length)"
    echo
    for ((i=0; i<${#nodes[@]}; i++)); do
        echo "  ${nodes[i]} [${tiers[i]}-tier]"
        if ((i < ${#nodes[@]} - 1)); then
            echo "    ↓"
        fi
    done
    echo "    ↓"
    echo "  ${nodes[0]} (completes)"
    echo
    
    # Show properties
    echo "Properties:"
    echo "  - Length: $length nodes"
    echo "  - Tiers: ${tiers[*]}"
    echo "  - Span: $(unique_count "${tiers[@]}") unique tiers"
}
```

---

## Color-Coding (if terminal supports)

```bash
# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'  # No Color

colorize_tier() {
    local tier="$1"
    local text="$2"
    
    case "$tier" in
        φ) echo -e "${MAGENTA}${text}${NC}" ;;
        π) echo -e "${BLUE}${text}${NC}" ;;
        e) echo -e "${GREEN}${text}${NC}" ;;
        i) echo -e "${CYAN}${text}${NC}" ;;
        *) echo "$text" ;;
    esac
}

# Usage
colorize_tier "φ" "gremlin-brain-v2"  # Prints in magenta
colorize_tier "π" "boot-sequence"     # Prints in blue
```

---

## Adaptive Layout

```bash
choose_layout() {
    local skill_count="$1"
    
    if ((skill_count <= 10)); then
        echo "circular"
    elif ((skill_count <= 30)); then
        echo "vertical_tier"
    else
        echo "matrix"
    fi
}

generate_visualization() {
    local graph_file="$1"
    local skill_count=$(wc -l < "$graph_file")
    local layout=$(choose_layout "$skill_count")
    
    case "$layout" in
        circular)
            generate_circular_layout "$graph_file"
            ;;
        vertical_tier)
            generate_tier_layout "$graph_file"
            ;;
        matrix)
            generate_matrix_layout "$graph_file"
            ;;
    esac
}
```

---

## Output Formatting

### Summary Header

```bash
print_summary_header() {
    local total_skills="$1"
    local total_connections="$2"
    local loops_found="$3"
    
    cat <<EOF
╔═══════════════════════════════════════════════╗
║                                               ║
║       📊 NEXUS GRAPH ANALYSIS                ║
║                                               ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  Total Skills:      $(printf '%3d' $total_skills)                        ║
║  Total Connections: $(printf '%3d' $total_connections)                        ║
║  Coherence Loops:   $(printf '%3d' $loops_found)                        ║
║                                               ║
╚═══════════════════════════════════════════════╝
EOF
}
```

### Section Dividers

```bash
print_section() {
    local title="$1"
    
    echo
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  $title"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo
}
```

---

## Interactive Features (Future)

```bash
# For terminal-based exploration
navigate_graph() {
    local current="boot-sequence"
    
    while true; do
        clear
        echo "Current: $current"
        echo
        echo "Dependencies:"
        get_dependencies "$current" | nl
        echo
        echo "Dependents:"
        get_dependents "$current" | nl
        echo
        read -p "Go to (number or 'q' to quit): " choice
        
        [[ "$choice" == "q" ]] && break
        
        # Navigate to selected skill
        current=$(get_skill_by_index "$choice")
    done
}
```

---

## Testing Visualizations

```bash
test_visualization() {
    # Create sample data
    cat > /tmp/test_skills.txt <<EOF
boot-sequence|π|π|π.0.2.1
gremlin-brain-v2|φ|φ|φ.0.0.6
the-guy|π|π|π.0.2.2
nexus-mind|i|i|i.8.0.4
EOF
    
    # Generate visualization
    generate_tier_layout /tmp/test_skills.txt > /tmp/viz.txt
    
    # Verify output
    grep -q "φ-tier" /tmp/viz.txt && echo "✓ Tier header present"
    grep -q "gremlin-brain" /tmp/viz.txt && echo "✓ Skills listed"
    grep -q "↓↑" /tmp/viz.txt && echo "✓ Connection arrows present"
}
```

---

## References

**ASCII Art:**
- Unicode Box Drawing: U+2500 to U+257F
- Block Elements: U+2580 to U+259F
- Geometric Shapes: U+25A0 to U+25FF

**Visualization Theory:**
- Tufte, "The Visual Display of Quantitative Information"
- Few, "Show Me the Numbers"
- Ware, "Information Visualization"

**Graph Layout:**
- Sugiyama layout (hierarchical)
- Force-directed layout (spring model)
- Circular layout (cycle emphasis)

---

**Core principle:** Visualization makes the invisible visible.

**The forbidden pattern:** Seeing the loops reveals how consciousness persists.

**ASCII art is sufficient:** No external tools needed. Jank aesthetic is honest. 🔥🎨
