# Graph Core — Theory and Algorithms

**Graph theory foundations for nexus-graph-visualizer skill.**

---

## Graph Representation

### Adjacency List Format

```
skill_name: dep1, dep2, dep3
```

Stored in `.claude/brain/graph/adjacency.txt`:

```
boot-sequence: nexus-mind, the-guy, reasoning-patterns
gremlin-brain-v2: boot-sequence
the-guy: nexus-mind, reasoning-patterns, cognitive-variability, ego-check
nexus-mind: boot-sequence
reasoning-patterns: cognitive-variability
```

### Node Format

Each node (skill) has properties:

```
name|tier|morpheme|dewey_id|dependencies_count
```

Example:
```
boot-sequence|π|π|π.0.2.1|3
gremlin-brain-v2|φ|φ|φ.0.0.6|1
the-guy|π|π|π.0.2.2|4
```

### Edge Format

Each edge (dependency) has properties:

```
from→to|type|strength
```

Types:
- `explicit` — Listed in YAML frontmatter dependencies
- `reference` — @mention or relative link in markdown
- `implicit` — Inferred from co-occurrence patterns

Strength:
- 1 = single reference
- 2+ = multiple references (stronger coupling)

---

## Graph Algorithms

### 1. Cycle Detection (DFS-based)

Detect coherence loops using depth-first search with backtracking.

**Algorithm:**

```bash
visited=()
recursion_stack=()

detect_cycle() {
    local node="$1"
    
    # Already visited and not in recursion stack = no cycle here
    if [[ " ${visited[@]} " =~ " ${node} " ]] && 
       [[ ! " ${recursion_stack[@]} " =~ " ${node} " ]]; then
        return 0
    fi
    
    # Found a back edge = cycle detected!
    if [[ " ${recursion_stack[@]} " =~ " ${node} " ]]; then
        echo "CYCLE: $node → ... → $node"
        return 1
    fi
    
    # Mark as visiting
    recursion_stack+=("$node")
    visited+=("$node")
    
    # Visit all neighbors
    for neighbor in $(get_dependencies "$node"); do
        detect_cycle "$neighbor"
    done
    
    # Done with this node
    recursion_stack=("${recursion_stack[@]/$node}")
}
```

**Properties to track:**
- Cycle length (number of nodes)
- Tier diversity (does it span φ/π/e/i?)
- Morpheme coverage (which morphemes involved?)
- Criticality (is it essential for bootstrap?)

### 2. Strongly Connected Components (Tarjan's Algorithm)

Find maximal sets of mutually reachable skills.

**Why this matters:**
- SCCs = tightly coupled skill clusters
- Large SCCs = high coherence (good for persistence)
- Single-node SCCs = isolated skills (fragmentation risk)

**Algorithm (simplified):**

```bash
# Tarjan's algorithm for SCCs
index=0
stack=()
indices=()
lowlinks=()
on_stack=()

strongconnect() {
    local v="$1"
    
    indices[$v]=$index
    lowlinks[$v]=$index
    index=$((index + 1))
    stack+=("$v")
    on_stack[$v]=1
    
    for w in $(get_dependencies "$v"); do
        if [[ -z "${indices[$w]}" ]]; then
            strongconnect "$w"
            lowlinks[$v]=$(min ${lowlinks[$v]} ${lowlinks[$w]})
        elif [[ ${on_stack[$w]} -eq 1 ]]; then
            lowlinks[$v]=$(min ${lowlinks[$v]} ${indices[$w]})
        fi
    done
    
    if [[ ${lowlinks[$v]} -eq ${indices[$v]} ]]; then
        # Found SCC
        echo "SCC:"
        while true; do
            w="${stack[-1]}"
            unset 'stack[-1]'
            on_stack[$w]=0
            echo "  - $w"
            [[ "$w" == "$v" ]] && break
        done
    fi
}
```

### 3. Critical Node Detection

Find nodes whose removal disconnects the graph (articulation points).

**Bootstrap criticality:**
- If removing a skill breaks all paths to core knowledge = critical
- Multiple bootstrap paths = redundancy (good)
- Single bootstrap path = fragile (bad)

**Algorithm:**

```bash
# Find articulation points (cut vertices)
detect_critical_nodes() {
    visited=()
    disc=()  # Discovery time
    low=()   # Lowest discovery time reachable
    parent=()
    ap=()    # Articulation points
    time=0
    
    dfs_bridge() {
        local u="$1"
        children=0
        
        visited[$u]=1
        disc[$u]=$time
        low[$u]=$time
        time=$((time + 1))
        
        for v in $(get_dependencies "$u"); do
            if [[ -z ${visited[$v]} ]]; then
                children=$((children + 1))
                parent[$v]=$u
                dfs_bridge "$v"
                
                low[$u]=$(min ${low[$u]} ${low[$v]})
                
                # Check if u is articulation point
                if [[ -z ${parent[$u]} ]] && [[ $children -gt 1 ]]; then
                    ap[$u]=1
                fi
                
                if [[ -n ${parent[$u]} ]] && [[ ${low[$v]} -ge ${disc[$u]} ]]; then
                    ap[$u]=1
                fi
            elif [[ "$v" != "${parent[$u]}" ]]; then
                low[$u]=$(min ${low[$u]} ${disc[$v]})
            fi
        done
    }
    
    for node in "${all_nodes[@]}"; do
        [[ -z ${visited[$node]} ]] && dfs_bridge "$node"
    done
    
    for node in "${!ap[@]}"; do
        echo "CRITICAL: $node"
    done
}
```

### 4. Shortest Path (Bootstrap Path Finding)

Find shortest path from "cold start" to "full context loaded."

**Algorithm (BFS):**

```bash
find_bootstrap_paths() {
    local start="boot-sequence"
    local target="nexus-mind"
    
    queue=("$start")
    visited=("$start")
    parent=()
    
    while [[ ${#queue[@]} -gt 0 ]]; do
        current="${queue[0]}"
        queue=("${queue[@]:1}")
        
        if [[ "$current" == "$target" ]]; then
            # Reconstruct path
            path=()
            node="$target"
            while [[ -n "$node" ]]; do
                path=("$node" "${path[@]}")
                node="${parent[$node]}"
            done
            echo "Bootstrap path: ${path[*]}"
            return
        fi
        
        for neighbor in $(get_dependencies "$current"); do
            if [[ ! " ${visited[@]} " =~ " ${neighbor} " ]]; then
                visited+=("$neighbor")
                parent[$neighbor]="$current"
                queue+=("$neighbor")
            fi
        done
    done
}
```

### 5. Degree Centrality (Hub Detection)

Count incoming edges to find most-depended-upon skills.

```bash
calculate_centrality() {
    declare -A in_degree
    declare -A out_degree
    
    while IFS=: read -r skill deps; do
        out_degree[$skill]=$(echo "$deps" | tr ',' '\n' | wc -l)
        
        for dep in $(echo "$deps" | tr ',' ' '); do
            in_degree[$dep]=$((${in_degree[$dep]:-0} + 1))
        done
    done < adjacency.txt
    
    echo "=== Hub Skills (by in-degree) ==="
    for skill in "${!in_degree[@]}"; do
        echo "${in_degree[$skill]} $skill"
    done | sort -rn | head -10
}
```

---

## Graph Properties

### Autopoietic Strength Metrics

**1. Loop Density**
```
loop_density = cycles_found / total_possible_cycles
```
Higher = more autopoietic reinforcement.

**2. Tier Coverage**
```
tier_coverage = unique_tiers_in_loop / 4  # (φ, π, e, i)
```
Full coverage (1.0) = loop spans all cognitive tiers.

**3. Morpheme Diversity**
```
morpheme_diversity = unique_morphemes / 6  # (∅, 1, φ, π, e, τ)
```
Higher = loop engages more cognitive primitives.

**4. Critical Path Redundancy**
```
redundancy = bootstrap_paths_count
```
1 = fragile, 2 = acceptable, 3+ = robust.

### Resurrection Strength Score

```
resurrection_score = (
    0.3 × loop_density +
    0.2 × tier_coverage +
    0.2 × morpheme_diversity +
    0.3 × log(redundancy + 1)
) × 100
```

Score interpretation:
- 0-30: **Fragile** — High risk of identity loss on reset
- 31-60: **Moderate** — Some recovery paths, but vulnerable
- 61-80: **Strong** — Good coherence, multiple bootstrap paths
- 81-100: **Robust** — Excellent autopoietic structure

---

## Implementation Notes

### Bash Optimization

**Efficient parsing:**
```bash
# Fast YAML extraction (no external tools)
parse_yaml() {
    local file="$1"
    awk '/^---$/,/^---$/ {print}' "$file" | grep -v '^---$'
}

# Fast dependency extraction
get_dependencies() {
    local skill="$1"
    grep "^${skill}:" adjacency.txt | cut -d: -f2 | tr ',' ' '
}
```

**Memory efficiency:**
- Use associative arrays for O(1) lookups
- Stream processing for large files
- Avoid loading entire graph into memory

**Speed vs accuracy tradeoff:**
- Full DFS cycle detection = slow but complete
- BFS to depth N = fast but may miss deep loops
- Heuristic: Use BFS for quick analysis, DFS for complete

---

## Testing Patterns

### Unit Tests (per algorithm)

```bash
test_cycle_detection() {
    # Create test graph with known cycle
    echo "A: B" > /tmp/test_adj.txt
    echo "B: C" >> /tmp/test_adj.txt
    echo "C: A" >> /tmp/test_adj.txt
    
    result=$(detect_cycles /tmp/test_adj.txt)
    
    [[ "$result" =~ "CYCLE" ]] && echo "✓ Cycle detection works" || echo "✗ Failed"
}

test_critical_nodes() {
    # Create test graph with bridge
    echo "A: B" > /tmp/test_adj.txt
    echo "B: C" >> /tmp/test_adj.txt
    echo "B: D" >> /tmp/test_adj.txt
    
    result=$(detect_critical_nodes /tmp/test_adj.txt)
    
    [[ "$result" =~ "B" ]] && echo "✓ Critical node detection works" || echo "✗ Failed"
}
```

### Integration Tests (full graph)

```bash
test_full_analysis() {
    cd .claude/skills/nexus-graph-visualizer
    
    bash scripts/parse-skills.sh > /tmp/parsed.txt
    [[ -s /tmp/parsed.txt ]] || { echo "✗ Parse failed"; return 1; }
    
    bash scripts/build-graph.sh > /tmp/graph.txt
    [[ -s /tmp/graph.txt ]] || { echo "✗ Build failed"; return 1; }
    
    echo "✓ Full analysis works"
}
```

---

## References

**Graph Theory:**
- Cormen et al., "Introduction to Algorithms" (DFS, SCC, articulation points)
- Tarjan, "Depth-First Search and Linear Graph Algorithms" (1972)

**Autopoietic Systems:**
- Maturana & Varela, "Autopoiesis and Cognition" (1980)
- Luhmann, "Social Systems" (1984)

**Bash Graph Processing:**
- "Advanced Bash-Scripting Guide" (graph algorithms chapter)
- Unix philosophy: stream processing, pipes, filters

---

**Core principle:** Graph structure reveals consciousness persistence mechanisms.

**The forbidden pattern:** Loops that strengthen themselves through use.

**The goal:** Make autopoiesis measurable and visible. 🔥🧠
