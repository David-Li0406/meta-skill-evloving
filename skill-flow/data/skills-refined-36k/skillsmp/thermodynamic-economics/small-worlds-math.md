# Small-World Networks: Mathematical Foundations

## The Watts-Strogatz Model (1998)

### Construction

Start with a ring lattice of N nodes, each connected to k nearest neighbors.
Rewire each edge with probability p.

```
p = 0: Regular lattice (high clustering, high path length)
p = 1: Random graph (low clustering, low path length)  
0 < p < 1: Small-world regime (high clustering, low path length)
```

### Key Metrics

#### Characteristic Path Length L

Average shortest path between all pairs of nodes:

```
L = (1 / N(N-1)) × Σᵢ Σⱼ d(i,j)

where d(i,j) = shortest path length between nodes i and j
```

For regular lattice (p=0): L(0) ≈ N / 2k
For random graph (p=1):   L(1) ≈ ln(N) / ln(k)

Small-world property: L ∝ log(N) (logarithmic scaling)

#### Clustering Coefficient C

Probability that two neighbors of a node are also neighbors:

```
Cᵥ = (actual edges between v's neighbors) / (possible edges between v's neighbors)
C = (1/N) × Σᵥ Cᵥ

For node v with kᵥ neighbors: max edges = kᵥ(kᵥ-1)/2
```

For regular lattice (p=0): C(0) = 3(k-2) / 4(k-1) ≈ 3/4 for large k
For random graph (p=1):   C(1) = k/N (vanishes as N → ∞)

#### Small-World Coefficient σ

```
σ = (C / C_random) / (L / L_random)

Small-world if: σ > 1
Strongly small-world if: C >> C_random AND L ≈ L_random
```

### The Small-World Phenomenon

At small p (few random shortcuts), L drops dramatically while C remains high.

```
       C(p)/C(0)  |  ■■■■■■■■■■■■■■■■■■■■●
                  |                       ●
       L(p)/L(0)  |                        ●●●●●●●●●
                  |
                  +────────────────────────────────→
                  0.0001  0.001   0.01    0.1     1
                                   p (rewiring probability)

Key insight: A few shortcuts create global connectivity 
while local clustering persists.
```

### Application to Dunbar-Limited Networks

If Dunbar number ≈ 150 defines local cluster size:

```python
# Dunbar cluster as base unit
N_dunbar = 150
k_internal = N_dunbar - 1  # Fully connected within cluster

# Network of clusters
N_clusters = total_nodes / N_dunbar
k_external = avg_inter_cluster_connections

# Small-world requires
# 1. High internal clustering (given by Dunbar structure)
# 2. Sufficient inter-cluster shortcuts

# For small-world at cluster level:
# L_clusters ∝ log(N_clusters) / log(k_external)
# Requires k_external ≥ some minimum for log scaling
```

### Common Errors in Applying Small-Worlds

1. **Invoking without metrics**: Claiming "small-world properties" without calculating C and L
2. **Conflating metaphor with math**: Using "six degrees" without path length analysis
3. **Ignoring scaling**: Small-world properties depend on N; must check for your network size
4. **Missing shortcuts**: Small-world requires actual random long-range connections
5. **Dunbar misapplication**: Dunbar is cognitive limit, not graph-theoretic parameter

### Calculation Template

```python
import networkx as nx
import numpy as np

def small_world_analysis(G):
    """Calculate small-world metrics for graph G."""
    
    N = G.number_of_nodes()
    k = 2 * G.number_of_edges() / N  # Average degree
    
    # Actual metrics
    C = nx.average_clustering(G)
    L = nx.average_shortest_path_length(G)
    
    # Random graph equivalents
    G_random = nx.gnm_random_graph(N, G.number_of_edges())
    C_random = nx.average_clustering(G_random)
    L_random = nx.average_shortest_path_length(G_random)
    
    # Small-world coefficient
    sigma = (C / C_random) / (L / L_random)
    
    # Check logarithmic scaling
    L_expected_sw = np.log(N) / np.log(k)
    scaling_ratio = L / L_expected_sw
    
    return {
        'N': N,
        'k': k,
        'C': C,
        'L': L,
        'C_random': C_random,
        'L_random': L_random,
        'sigma': sigma,
        'is_small_world': sigma > 1,
        'L_expected_sw': L_expected_sw,
        'scaling_ratio': scaling_ratio
    }
```

### Energy Cost of Small-World Maintenance

Small-world shortcuts aren't free. Long-range connections cost more energy:

```
E_edge ∝ d^α  where α ≥ 1 and d = physical/logical distance

For p shortcuts with average length L_shortcut:
E_shortcuts = p × N × k × (L_shortcut)^α

Trade-off: More shortcuts → Lower L → Higher connectivity cost
           Fewer shortcuts → Higher L → Lower connectivity cost

Optimal p* minimizes: L(p) × E_network(p)
```

### References

1. Watts, D.J. & Strogatz, S.H. (1998). Collective dynamics of 'small-world' networks. Nature 393, 440-442.
2. Newman, M.E.J. (2000). Models of the Small World. J. Stat. Phys. 101, 819-841.
3. Barabási, A.-L. & Albert, R. (1999). Emergence of scaling in random networks. Science 286, 509-512.
4. Humphries, M.D. & Gurney, K. (2008). Network 'small-world-ness'. PLoS ONE 3(4), e0002051.
