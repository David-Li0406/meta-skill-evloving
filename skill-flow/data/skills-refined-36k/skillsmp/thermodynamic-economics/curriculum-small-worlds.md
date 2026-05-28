# Curriculum: Small-World Network Mathematics

**Phase 1 - Acknowledge & Learn**

---

## Course Overview

This curriculum provides the mathematical foundations for analyzing network topology, specifically addressing the critique that we invoked Dunbar numbers without demonstrating actual small-world properties.

**Prerequisites**: Basic probability, familiarity with graphs

**Duration**: Self-paced, approximately 15-20 hours of study

**Outcome**: Ability to calculate small-world metrics and validate network designs

---

## Module 1: The Watts-Strogatz Model

### 1.1 Historical Context

In 1998, Duncan Watts and Steven Strogatz published "Collective dynamics of 'small-world' networks" in Nature, providing a mathematical framework for understanding networks that are neither completely regular nor completely random.

**The question they answered**: Why do real networks have both high clustering (like regular lattices) and short path lengths (like random graphs)?

### 1.2 Model Construction

The Watts-Strogatz algorithm:

```
STEP 1: Create a ring lattice
- N nodes arranged in a circle
- Each node connected to k nearest neighbors (k/2 on each side)

STEP 2: Rewire edges
- For each edge, with probability p:
  - Remove the edge
  - Reconnect to a random node (avoiding self-loops and duplicates)
```

Visualization of the spectrum:

```
p = 0 (Regular Lattice)          p = 0.1 (Small-World)           p = 1 (Random)
      ●───●                            ●───●                          ●   ●
     /│   │\                          /│╲ ╱│\                        / \ / \
    ● │   │ ●                        ● │ ╳ │ ●                      ●───●───●
    │ │   │ │                        │ │╱ ╲│ │                       \ / \ /
    ● │   │ ●                        ● │   │ ●                        ●   ●
     \│   │/                          \│   │/
      ●───●                            ●───●

High clustering                  High clustering                 Low clustering
High path length                 SHORT path length              Short path length
```

### 1.3 The Key Insight

A few random shortcuts dramatically reduce path length while preserving local clustering.

```
Metric behavior as p increases:

L(p)/L(0)  1.0 |●●●●●●
               |      ●●
               |        ●●●●●●●●●●
           0.5 |
               |
           0.0 +────────────────────
               0.0001  0.01    1.0
                         p

C(p)/C(0)  1.0 |●●●●●●●●●●●●●●
               |              ●●
               |                ●●●●
           0.5 |
               |
           0.0 +────────────────────
               0.0001  0.01    1.0
                         p

Key: L drops fast, C drops slow → Small-world regime exists
```

### 1.4 Implementation

Reference implementation: `small_world_metrics.py`

```python
from small_world_metrics import watts_strogatz, small_world_metrics

# Create a Watts-Strogatz network
# N=1000 nodes, k=10 neighbors each, p=0.1 rewiring probability
g = watts_strogatz(n=1000, k=10, p=0.1, seed=42)

# Calculate metrics
metrics = small_world_metrics(g)
print(f"Clustering C: {metrics['C']:.4f}")
print(f"Path length L: {metrics['L']:.4f}")
print(f"Small-world sigma: {metrics['sigma']:.2f}")
print(f"Is small-world: {metrics['is_small_world']}")
```

### Exercises - Module 1

1. Generate Watts-Strogatz networks with p = 0, 0.01, 0.1, 1.0 and compare metrics
2. Plot C(p)/C(0) and L(p)/L(0) for p in [0.0001, 1.0]
3. Find the smallest p that achieves small-world properties (sigma > 1)

### Readings - Module 1

**Primary**:
- Watts, D.J. & Strogatz, S.H. (1998). "Collective dynamics of 'small-world' networks." *Nature* 393, 440-442.

---

## Module 2: Clustering Coefficient Calculation

### 2.1 Definition

The clustering coefficient measures how densely connected a node's neighborhood is.

**Local clustering coefficient** for node v:

```
C_v = (number of edges between v's neighbors) / (maximum possible edges between v's neighbors)

If v has k neighbors, maximum possible edges = k(k-1)/2

        a───b
       /     \
      v       c
       \     /
        d───e

C_v = (edges among {a,b,c,d,e}) / (5×4/2) = (edges) / 10
```

**Global clustering coefficient** (average):

```
C = (1/N) × Σ C_v  for all nodes v
```

### 2.2 Calculation Algorithm

```python
def clustering_coefficient(graph):
    """Calculate average clustering coefficient."""
    total = 0

    for v in graph.nodes():
        neighbors = list(graph.neighbors(v))
        k = len(neighbors)

        if k < 2:
            # Node cannot have clustering with < 2 neighbors
            continue

        # Count edges between neighbors
        edges_between = 0
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                if graph.has_edge(neighbors[i], neighbors[j]):
                    edges_between += 1

        # Calculate local clustering
        max_edges = k * (k - 1) / 2
        total += edges_between / max_edges

    return total / len(graph.nodes())
```

### 2.3 Expected Values

For different network types:

| Network Type | Clustering C | Formula |
|--------------|--------------|---------|
| Complete graph | 1.0 | Everyone connected to everyone |
| Ring lattice | ~0.75 | 3(k-2)/4(k-1) for large k |
| Random (Erdos-Renyi) | k/N | Vanishes as N grows |
| Small-world (WS) | ~C(0) × f(p) | High, slowly decreasing with p |

### 2.4 Interpretation

High clustering (C > 0.1) indicates:
- Local communities exist
- Neighbors of neighbors are likely connected
- Information can spread locally

Low clustering (C < 0.01) indicates:
- Sparse, tree-like structure
- No local communities
- Each connection is independent

### Exercises - Module 2

1. Calculate C by hand for a 6-node example graph
2. Compare C for lattice vs. random graph of same size
3. Verify that `small_world_metrics.py` produces correct C values

---

## Module 3: Path Length Analysis

### 3.1 Definition

**Shortest path length** d(i,j): Minimum number of edges to traverse from node i to node j.

**Characteristic path length** L: Average shortest path over all node pairs.

```
L = (1 / N(N-1)) × Σ_i Σ_j d(i,j)

where i ≠ j and the graph is connected
```

### 3.2 Calculation Algorithm (BFS)

```python
from collections import deque

def shortest_paths_from(graph, source):
    """BFS to find shortest paths from source to all nodes."""
    distances = {source: 0}
    queue = deque([source])

    while queue:
        current = queue.popleft()
        for neighbor in graph.neighbors(current):
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    return distances

def average_path_length(graph):
    """Calculate average shortest path length."""
    total = 0
    count = 0

    for source in graph.nodes():
        distances = shortest_paths_from(graph, source)
        for target, dist in distances.items():
            if target != source:
                total += dist
                count += 1

    return total / count if count > 0 else float('inf')
```

### 3.3 Expected Values

| Network Type | Path Length L | Formula |
|--------------|---------------|---------|
| Complete graph | 1.0 | Direct connection everywhere |
| Ring lattice | N/2k | Linear in N |
| Random graph | log(N)/log(k) | Logarithmic in N |
| Small-world | ~log(N)/log(k) | Logarithmic (like random) |

### 3.4 The "Six Degrees" Phenomenon

For a small-world network with N nodes and average degree k:

```
L ≈ log(N) / log(k)

Example (Watts-Strogatz parameters):
N = 7 billion (world population)
k = 44 (estimated average social connections)
L ≈ log(7×10^9) / log(44) ≈ 22.7 / 3.78 ≈ 6

Hence "six degrees of separation"
```

**Critical point**: This only works if:
1. Network actually has small-world structure
2. Shortcuts exist between distant regions
3. k is large enough

### Exercises - Module 3

1. Calculate L by hand for a 6-node ring lattice
2. Verify L ~ log(N)/log(k) for Watts-Strogatz networks
3. At what N does L exceed 10 for k=6, p=0.1?

---

## Module 4: Small-World Coefficient (sigma > 1.0)

### 4.1 Definition

The small-world coefficient sigma (σ) compares a network to an equivalent random graph:

```
σ = γ / λ

where:
γ = C / C_random      (clustering ratio)
λ = L / L_random      (path length ratio)

Small-world if: σ > 1
```

### 4.2 Intuition

A network is small-world when it has:
- Much higher clustering than random (γ >> 1)
- Similar path length to random (λ ≈ 1)

```
                     γ (clustering ratio)
                       │
                       │         Small-world
                       │         region (σ > 1)
                   2.0 │    ●●●●●●●
                       │   ●      ●●
                       │  ●         ●
                   1.0 │─●──────────●──────
                       │              ●  Random
                       │               ●
                   0.0 +───────────────────→
                       0.5  1.0  1.5  2.0
                              λ (path length ratio)
```

### 4.3 Calculation

```python
def small_world_coefficient(graph):
    """Calculate sigma for small-world assessment."""

    N = graph.number_of_nodes()
    M = graph.number_of_edges()

    # Actual network metrics
    C = clustering_coefficient(graph)
    L = average_path_length(graph)

    # Generate equivalent random graph
    random_graph = erdos_renyi_graph(N, M)
    C_random = clustering_coefficient(random_graph)
    L_random = average_path_length(random_graph)

    # Calculate sigma
    gamma = C / C_random if C_random > 0 else 0
    lambda_ = L / L_random if L_random > 0 else float('inf')
    sigma = gamma / lambda_ if lambda_ > 0 else 0

    return {
        'C': C,
        'L': L,
        'C_random': C_random,
        'L_random': L_random,
        'gamma': gamma,
        'lambda': lambda_,
        'sigma': sigma,
        'is_small_world': sigma > 1
    }
```

### 4.4 The Omega Alternative

Some researchers prefer omega (ω) which ranges from -1 to 1:

```
ω = L_random/L - C/C_lattice

ω ≈ 0: Small-world
ω ≈ -1: Lattice-like
ω ≈ +1: Random-like
```

### Exercises - Module 4

1. Calculate σ for Watts-Strogatz networks at different p values
2. Find the p value that maximizes σ
3. Compare σ and ω metrics for the same network

### Readings - Module 4

**Primary**:
- Humphries, M.D. & Gurney, K. (2008). "Network 'small-world-ness': a quantitative method for determining canonical network equivalence." *PLoS ONE* 3(4), e0002051.

---

## Module 5: Application to Dunbar-Limited Networks

### 5.1 Dunbar's Number

Robin Dunbar proposed cognitive limits on social group sizes based on neocortex ratio:

| Level | Size | Description |
|-------|------|-------------|
| Support clique | ~5 | Intimate relationships |
| Sympathy group | ~15 | Close friends |
| Affinity group | ~50 | Good friends |
| Active network | ~150 | Casual friends (Dunbar number) |
| Mega-band | ~500 | Acquaintances |
| Tribe | ~1500 | Can recognize faces |

### 5.2 The Error We Made

**Claim**: "Our network uses Dunbar numbers, so it has small-world properties."

**Problem**: Dunbar numbers define cluster SIZE, not network TOPOLOGY.

```
Just because groups are size 150 does NOT mean:
- Groups are internally well-connected
- Groups have appropriate inter-group links
- The resulting network has small-world metrics

You must CALCULATE C, L, σ to verify.
```

### 5.3 Designing Dunbar-Constrained Small-Worlds

To create a small-world network with Dunbar constraints:

```python
def dunbar_small_world(n_clusters, dunbar_size=150, internal_k=10,
                       external_p=0.1):
    """
    Create a small-world network respecting Dunbar limits.

    Args:
        n_clusters: Number of Dunbar-sized clusters
        dunbar_size: Size of each cluster (default 150)
        internal_k: Internal connections per node
        external_p: Probability of external (cross-cluster) links
    """
    total_nodes = n_clusters * dunbar_size
    graph = Graph()

    # Create internal cluster structure
    for cluster_id in range(n_clusters):
        base = cluster_id * dunbar_size

        # Internal ring lattice
        for i in range(dunbar_size):
            node = base + i
            graph.add_node(node)
            for j in range(1, internal_k // 2 + 1):
                neighbor = base + ((i + j) % dunbar_size)
                graph.add_edge(node, neighbor)

    # Add cross-cluster shortcuts
    for node in graph.nodes():
        if random.random() < external_p:
            # Link to random node in different cluster
            my_cluster = node // dunbar_size
            other_clusters = [c for c in range(n_clusters) if c != my_cluster]
            target_cluster = random.choice(other_clusters)
            target_node = target_cluster * dunbar_size + random.randint(0, dunbar_size - 1)
            graph.add_edge(node, target_node)

    return graph
```

### 5.4 Verification Requirements

For any Dunbar-based network claim, you MUST verify:

```
CHECK 1: Internal clustering
- Calculate C within each Dunbar cluster
- Should be high (> 0.3) if "communities" are real

CHECK 2: Cross-cluster connectivity
- Calculate number of inter-cluster edges
- Need sufficient shortcuts for small-world property

CHECK 3: Global small-world metrics
- σ > 1.0 for the full network
- L ~ log(N)/log(k) for scalability

CHECK 4: Path length scaling
- Test with increasing N
- Verify L grows logarithmically, not linearly
```

### 5.5 Energy Cost of Shortcuts

Small-world shortcuts are not free. Long-range connections cost more:

```
E_local ∝ d_local^α    (short, cheap)
E_shortcut ∝ d_shortcut^α    (long, expensive)

Total network energy:
E_network = Σ E_local + Σ E_shortcut
          = N × k_local × d_local^α + N × p × d_avg_shortcut^α

Trade-off: More shortcuts → Lower L → Higher energy cost
           Fewer shortcuts → Higher L → Lower energy cost

Optimal design minimizes: L × E_network
```

### Exercises - Module 5

1. Create a 10-cluster Dunbar network and calculate σ
2. Find minimum external_p needed for σ > 1
3. Estimate energy cost of maintaining the small-world property

### Readings - Module 5

**Primary**:
- Dunbar, R.I.M. (1992). "Neocortex size as a constraint on group size in primates." *Journal of Human Evolution* 22(6), 469-493.
- Dunbar, R.I.M. (2010). *How Many Friends Does One Person Need?* Faber & Faber.

---

## Assessment

### Verification Checklist

Before claiming "small-world properties," verify:

| Metric | Requirement | Calculated Value |
|--------|-------------|------------------|
| N (nodes) | Specified | ___ |
| k (avg degree) | Sufficient (> 4) | ___ |
| C (clustering) | High (> 0.1) | ___ |
| L (path length) | Logarithmic | ___ |
| C_random | Calculated | ___ |
| L_random | Calculated | ___ |
| γ (gamma) | >> 1 | ___ |
| λ (lambda) | ≈ 1 | ___ |
| σ (sigma) | > 1.0 | ___ |

### Capstone Project

**Project**: Small-World Analysis of Proposed Hyphal Network

Requirements:
1. Define network parameters (N, k, p, cluster structure)
2. Generate network using `small_world_metrics.py`
3. Calculate all metrics in the checklist above
4. Verify σ > 1.0
5. Test scaling: does L remain logarithmic as N increases?
6. Estimate energy cost of maintaining small-world property

Deliverable: Report with calculations and visualizations

---

## Additional Resources

### Tools

- `small_world_metrics.py` - Metrics calculation
- `small-worlds-math.md` - Mathematical reference

### Libraries

- NetworkX (Python) - Comprehensive network analysis
- igraph (R/Python) - High-performance graph analysis
- graph-tool (Python) - Advanced network analysis

### Extended Reading List

1. Newman, M.E.J. (2010). *Networks: An Introduction*. Oxford University Press.
2. Barabasi, A.-L. (2016). *Network Science*. Cambridge University Press. [Available free online]
3. Easley, D. & Kleinberg, J. (2010). *Networks, Crowds, and Markets*. Cambridge University Press.

---

*Phase 1 - Acknowledge & Learn*
*Thermodynamic Economics Learning Initiative*
*Generated: 2026-01-02*
