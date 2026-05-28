# Graph Analysis Algorithms

Algorithms for analyzing design documentation relationship graphs.

## Graph Structure

### Nodes

Each design doc is a node with properties:

- `id`: Unique identifier (module/filename)
- `path`: Full path to file
- `module`: Module name
- `category`: Design doc category
- `status`: Document status
- `completeness`: Completion percentage
- `updated`: Last update date

**Example node:**

```json
{
  "id": "effect-type-registry/observability",
  "path": ".claude/design/effect-type-registry/observability.md",
  "module": "effect-type-registry",
  "category": "observability",
  "status": "current",
  "completeness": 85,
  "updated": "2026-01-15"
}
```

### Edges

Each reference creates an edge with properties:

- `from`: Source document ID
- `to`: Target document ID
- `type`: Relationship type (related, dependency, content-link)
- `bidirectional`: Whether both docs reference each other

**Edge types:**

- **related**: Listed in frontmatter `related` array
- **dependency**: Listed in frontmatter `dependencies` array
- **content-link**: Markdown link in document content

**Example edge:**

```json
{
  "from": "effect-type-registry/observability",
  "to": "effect-type-registry/architecture",
  "type": "related",
  "bidirectional": true
}
```

### Graph Representation

Complete graph structure:

```json
{
  "nodes": [
    { "id": "module/doc", "...": "..." }
  ],
  "edges": [
    { "from": "module/doc-a", "to": "module/doc-b", "...": "..." }
  ]
}
```

## Orphan Detection

### Orphan Detection Algorithm

Find documents with no incoming or outgoing edges:

```text
Orphan Detection Algorithm:

for each node in graph:
  incoming = count of edges where node is 'to'
  outgoing = count of edges where node is 'from'

  if incoming == 0 and outgoing == 0:
    mark node as orphaned
    add to orphans list
```

### Orphan Detection Implementation

```bash
# For each design doc
for doc in ${design_docs[@]}; do
  # Count references in frontmatter
  related_count=$(grep -c "^  - " frontmatter_related)
  deps_count=$(grep -c "^  - " frontmatter_dependencies)

  # Count content links
  links_count=$(grep -c '\[.*\](\..*\.md)' content)

  # Count incoming references (grep this doc in all others)
  incoming_count=$(grep -rl "$(basename $doc)" other_docs | wc -l)

  outgoing=$((related_count + deps_count + links_count))
  incoming=$incoming_count

  if [ $outgoing -eq 0 ] && [ $incoming -eq 0 ]; then
    echo "ORPHANED: $doc"
  fi
done
```

### Orphan Categories

#### Type 1: New Stub Documents

- Recently created
- Low completeness (<20%)
- Expected to gain references as they're developed

#### Type 2: Abandoned Stubs

- Old creation date (>90 days)
- Still stub status
- No progress or references
- **Action:** Archive or delete

#### Type 3: Intentionally Standalone

- Complete documentation
- Self-contained topic
- No natural relationships
- **Action:** May be acceptable, review

#### Type 4: Broken References

- Had references that were removed
- References to deleted docs
- **Action:** Add new references or archive

## Circular Dependency Detection

### Circular Dependency Detection Algorithm

Detect cycles in dependency graph using depth-first search:

```text
Circular Dependency Detection:

function find_cycles(node, visited, path, cycles):
  if node in path:
    # Found cycle
    cycle = path[path.index(node):]
    cycle.append(node)  # Complete the cycle
    cycles.add(cycle)
    return

  if node in visited:
    return

  visited.add(node)
  path.append(node)

  # Follow only dependency edges
  for edge in node.dependency_edges:
    find_cycles(edge.to, visited, path, cycles)

  path.pop()

# Main
visited = set()
cycles = set()

for each node:
  if node not in visited:
    find_cycles(node, visited, [], cycles)

return cycles
```

### Circular Dependency Detection Implementation

```bash
# Build dependency graph (dependencies only, not related or content-links)
build_dependency_graph() {
  for doc in ${design_docs[@]}; do
    # Extract dependencies from frontmatter
    deps=$(awk '/^dependencies:/,/^[a-z]/' $doc | grep "^  - ")

    for dep in $deps; do
      echo "$doc -> $dep"
    done
  done
}

# Detect cycles using DFS
detect_cycles() {
  dependency_graph=$(build_dependency_graph)

  # Use tsort to detect cycles
  echo "$dependency_graph" | tsort 2>&1 | grep "cycle"
}
```

### Cycle Types

#### Type 1: Direct Cycle (A → B → A)

```text
cache-optimization → observability
observability → cache-optimization
```

**Fix:** Change one to 'related' instead of 'dependency'

#### Type 2: Indirect Cycle (A → B → C → A)

```text
cache-optimization → observability
observability → architecture
architecture → cache-optimization
```

**Fix:** Review which dependency is weakest and change to 'related'

#### Type 3: Self-Dependency (A → A)

```text
observability → observability
```

**Fix:** Remove self-reference (likely error)

## Connected Components

### Connected Components Algorithm

Find isolated clusters of documents:

```text
Connected Components Algorithm:

function depth_first_search(node, visited, component):
  visited.add(node)
  component.add(node)

  # Follow all edge types (not just dependencies)
  for edge in node.all_edges:
    neighbor = edge.to if edge.from == node else edge.from
    if neighbor not in visited:
      depth_first_search(neighbor, visited, component)

# Main
components = []
visited = set()

for each node:
  if node not in visited:
    component = set()
    depth_first_search(node, visited, component)
    components.append(component)

# Isolated clusters are components with size > 1 that have
# no edges to other components
isolated = [c for c in components if size(c) > 1 and is_isolated(c)]
```

### Connected Components Implementation

```bash
# Find connected components
find_components() {
  declare -A visited
  components=()

  for doc in ${design_docs[@]}; do
    if [ -z "${visited[$doc]}" ]; then
      component=$(dfs_component "$doc")
      components+=("$component")
    fi
  done

  echo "${components[@]}"
}

# DFS to find component
dfs_component() {
  local start=$1
  local component=()
  local stack=("$start")

  while [ ${#stack[@]} -gt 0 ]; do
    node="${stack[-1]}"
    unset 'stack[-1]'

    if [ -z "${visited[$node]}" ]; then
      visited[$node]=1
      component+=("$node")

      # Get neighbors (all edge types)
      neighbors=$(get_all_neighbors "$node")
      stack+=($neighbors)
    fi
  done

  echo "${component[@]}"
}
```

### Cluster Analysis

**Indicators of Isolation:**

- Component size > 1
- No edges to other components
- All docs in same module (possible)
- Different category from main cluster

**Causes:**

- Module-specific documentation
- Forgotten legacy docs
- Intentional separation

**Actions:**

- Review if intentional
- Add cross-module references if related
- Archive if legacy/obsolete

## Bidirectional Relationship Detection

### Bidirectional Relationship Detection Algorithm

Find docs that reference each other:

```text
Bidirectional Detection:

bidirectional_pairs = set()

for each edge (A → B):
  # Check if reverse edge exists
  if exists edge (B → A) with same type:
    pair = (min(A, B), max(A, B))  # Normalize order
    bidirectional_pairs.add(pair)

return bidirectional_pairs
```

### Bidirectional Relationship Detection Implementation

```bash
# Find bidirectional relationships
find_bidirectional() {
  declare -A edges
  bidirectional=()

  # Build edge map
  for doc in ${design_docs[@]}; do
    refs=$(get_references "$doc")  # All types
    for ref in $refs; do
      edges["$doc -> $ref"]=$type
    done
  done

  # Check for reverse edges
  for edge in "${!edges[@]}"; do
    from="${edge% -> *}"
    to="${edge#* -> }"
    reverse="$to -> $from"

    if [ -n "${edges[$reverse]}" ]; then
      # Both directions exist
      if [ "${edges[$edge]}" == "${edges[$reverse]}" ]; then
        # Same type (related, dependency, etc.)
        echo "$from ↔ $to (${edges[$edge]})"
      fi
    fi
  done
}
```

### Bidirectional Categories

#### Type 1: Mutual Related (Good)

```text
observability ↔ architecture (both in related)
```

**Status:** Healthy cross-referencing

#### Type 2: Mutual Dependencies (Warning)

```text
cache-optimization ↔ observability (both in dependencies)
```

**Status:** Circular dependency, needs fixing

#### Type 3: Mixed Types

```text
A → B (dependency)
B → A (related)
```

**Status:** Asymmetric relationship, review

## One-Way Reference Detection

### One-Way Reference Detection Algorithm

Find unreciprocated references:

```text
One-Way Detection:

one_way_refs = []

for each edge (A → B):
  if not exists edge (B → A):
    one_way_refs.append({
      from: A,
      to: B,
      type: edge.type
    })

return one_way_refs
```

### One-Way Reference Detection Implementation

```bash
# Find one-way references
find_one_way() {
  all_edges=$(build_all_edges)

  echo "$all_edges" | while read edge; do
    from="${edge% -> *}"
    to="${edge#* -> }"
    type="${edge#*: }"

    # Check if reverse exists
    reverse=$(echo "$all_edges" | grep "^$to -> $from")

    if [ -z "$reverse" ]; then
      echo "ONE-WAY: $from → $to ($type)"
      echo "  Suggestion: Add $from to $to's related docs"
    fi
  done
}
```

### One-Way Categories

#### Category 1: Should Be Bidirectional

```text
cache-optimization → architecture (related)
```

**Fix:** Add cache-optimization to architecture's related array

#### Category 2: Intentional Asymmetry

```text
implementation-details → architecture (dependency)
```

**Status:** Acceptable, implementation depends on architecture but not reverse

#### Category 3: Content Links

```text
doc-a → doc-b (content-link only)
```

**Status:** May be fine, review if related should be added

## Cross-Module Analysis

### Cross-Module Analysis Algorithm

Identify relationships crossing module boundaries:

```text
Cross-Module Detection:

cross_module_edges = []

for each edge (A → B):
  if A.module != B.module:
    cross_module_edges.append(edge)

# Analyze patterns
modules_connected = count unique module pairs in cross_module_edges
integration_points = count cross-module edges per module
```

### Cross-Module Analysis Implementation

```bash
# Find cross-module references
find_cross_module() {
  for doc in ${design_docs[@]}; do
    doc_module=$(get_module "$doc")
    refs=$(get_references "$doc")

    for ref in $refs; do
      ref_module=$(get_module "$ref")

      if [ "$doc_module" != "$ref_module" ]; then
        echo "CROSS-MODULE: $doc_module/$doc → $ref_module/$ref"
      fi
    done
  done
}
```

### Cross-Module Patterns

#### Pattern 1: Integration Documentation

```text
rspress-plugin/type-loading → effect-type-registry/architecture
```

**Meaning:** Plugin integrates with registry, documented dependency

#### Pattern 2: Shared Concepts

```text
module-a/observability ↔ module-b/observability
```

**Meaning:** Shared observability patterns

#### Pattern 3: Reused Decisions

```text
module-b/design → module-a/design (reference to decision rationale)
```

**Meaning:** Reusing design decisions

## Metrics Calculation

### Node Metrics

**Degree:** Total edges connected to node

```text
degree(node) = incoming_edges + outgoing_edges
```

**In-Degree:** Incoming edges only

```text
in_degree(node) = count of edges where node is 'to'
```

**Out-Degree:** Outgoing edges only

```text
out_degree(node) = count of edges where node is 'from'
```

**Centrality:** Importance in graph

```text
Simple centrality = degree(node) / max_degree_in_graph
```

### Graph Metrics

**Density:** How connected the graph is

```text
density = actual_edges / possible_edges
possible_edges = n * (n - 1) / 2  # For undirected
```

**Average Degree:**

```text
avg_degree = sum(all node degrees) / node_count
```

**Clustering Coefficient:** How clustered nodes are

```text
For each node:
  neighbors = nodes directly connected
  possible_connections = neighbors * (neighbors - 1) / 2
  actual_connections = edges between neighbors
  local_clustering = actual / possible

global_clustering = average of all local_clustering values
```

## Special Cases

### Archived Documents

Include in analysis but flag distinctly:

```text
if node.status == 'archived':
  # Include in graph
  # Mark with special styling
  # Report active docs referencing archived ones
  # Recommend updating references
```

### Stub Documents

Track stubs referenced by current docs:

```text
if node.status == 'stub' and in_degree > 0:
  # Stub is blocking progress
  # Flag for completion
  # List docs waiting on this stub
```

### Broken References

Detect references to non-existent docs:

```text
for each edge:
  if not exists(edge.to):
    report_broken_reference(edge.from, edge.to)
```
