#!/usr/bin/env python3
"""
Small-World Network Metrics Calculator

Calculates Watts-Strogatz metrics for network analysis.
Part of the thermodynamic-economics skill for Univrs.io.

Usage:
    python small_world_metrics.py --nodes 1000 --degree 10 --rewire 0.1
    python small_world_metrics.py --edgelist network.csv
"""

import argparse
import json
import math
from collections import deque
from typing import Dict, List, Tuple, Optional
import random

class Graph:
    """Simple graph implementation for metric calculation."""
    
    def __init__(self):
        self.adj: Dict[int, set] = {}
        
    def add_node(self, n: int):
        if n not in self.adj:
            self.adj[n] = set()
            
    def add_edge(self, u: int, v: int):
        self.add_node(u)
        self.add_node(v)
        self.adj[u].add(v)
        self.adj[v].add(u)
        
    def nodes(self) -> List[int]:
        return list(self.adj.keys())
        
    def edges(self) -> List[Tuple[int, int]]:
        seen = set()
        result = []
        for u in self.adj:
            for v in self.adj[u]:
                if (v, u) not in seen:
                    result.append((u, v))
                    seen.add((u, v))
        return result
        
    def degree(self, n: int) -> int:
        return len(self.adj.get(n, []))
        
    def neighbors(self, n: int) -> set:
        return self.adj.get(n, set())


def create_ring_lattice(n: int, k: int) -> Graph:
    """Create a ring lattice with n nodes, each connected to k nearest neighbors."""
    g = Graph()
    for i in range(n):
        g.add_node(i)
    
    # Connect each node to k/2 neighbors on each side
    for i in range(n):
        for j in range(1, k // 2 + 1):
            g.add_edge(i, (i + j) % n)
            g.add_edge(i, (i - j) % n)
    
    return g


def watts_strogatz(n: int, k: int, p: float, seed: Optional[int] = None) -> Graph:
    """
    Create a Watts-Strogatz small-world graph.
    
    Args:
        n: Number of nodes
        k: Each node is connected to k nearest neighbors in ring topology
        p: Probability of rewiring each edge
        seed: Random seed for reproducibility
    
    Returns:
        Small-world graph
    """
    if seed is not None:
        random.seed(seed)
    
    g = create_ring_lattice(n, k)
    nodes = list(range(n))
    
    # Rewire edges
    for i in range(n):
        for j in range(1, k // 2 + 1):
            if random.random() < p:
                # Remove old edge
                old_target = (i + j) % n
                g.adj[i].discard(old_target)
                g.adj[old_target].discard(i)
                
                # Add new random edge (avoid self-loops and duplicates)
                candidates = [x for x in nodes if x != i and x not in g.adj[i]]
                if candidates:
                    new_target = random.choice(candidates)
                    g.add_edge(i, new_target)
    
    return g


def erdos_renyi(n: int, m: int, seed: Optional[int] = None) -> Graph:
    """Create an Erdős-Rényi random graph with n nodes and m edges."""
    if seed is not None:
        random.seed(seed)
    
    g = Graph()
    for i in range(n):
        g.add_node(i)
    
    # All possible edges
    possible = [(i, j) for i in range(n) for j in range(i + 1, n)]
    random.shuffle(possible)
    
    for u, v in possible[:m]:
        g.add_edge(u, v)
    
    return g


def shortest_path_lengths(g: Graph, source: int) -> Dict[int, int]:
    """BFS to find shortest paths from source to all nodes."""
    dist = {source: 0}
    queue = deque([source])
    
    while queue:
        u = queue.popleft()
        for v in g.neighbors(u):
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    
    return dist


def average_path_length(g: Graph) -> float:
    """Calculate average shortest path length."""
    nodes = g.nodes()
    n = len(nodes)
    if n < 2:
        return 0
    
    total = 0
    count = 0
    
    for source in nodes:
        dists = shortest_path_lengths(g, source)
        for target, d in dists.items():
            if target != source:
                total += d
                count += 1
    
    return total / count if count > 0 else float('inf')


def clustering_coefficient(g: Graph) -> float:
    """Calculate average clustering coefficient."""
    nodes = g.nodes()
    if not nodes:
        return 0
    
    total = 0
    for v in nodes:
        neighbors = list(g.neighbors(v))
        k = len(neighbors)
        if k < 2:
            continue
        
        # Count edges between neighbors
        edges_between = 0
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                if neighbors[j] in g.neighbors(neighbors[i]):
                    edges_between += 1
        
        # Maximum possible edges
        max_edges = k * (k - 1) / 2
        total += edges_between / max_edges
    
    return total / len(nodes)


def small_world_metrics(g: Graph) -> Dict:
    """Calculate comprehensive small-world metrics."""
    n = len(g.nodes())
    m = len(g.edges())
    k = 2 * m / n if n > 0 else 0
    
    C = clustering_coefficient(g)
    L = average_path_length(g)
    
    # Create equivalent random graph for comparison
    g_random = erdos_renyi(n, m, seed=42)
    C_random = clustering_coefficient(g_random)
    L_random = average_path_length(g_random)
    
    # Small-world coefficient
    if C_random > 0 and L_random > 0:
        gamma = C / C_random
        lambda_ = L / L_random
        sigma = gamma / lambda_ if lambda_ > 0 else 0
    else:
        gamma = lambda_ = sigma = 0
    
    # Expected small-world path length
    if k > 1:
        L_expected_sw = math.log(n) / math.log(k)
    else:
        L_expected_sw = n
    
    return {
        'N': n,
        'M': m,
        'k': k,
        'C': C,
        'L': L,
        'C_random': C_random,
        'L_random': L_random,
        'gamma': gamma,
        'lambda': lambda_,
        'sigma': sigma,
        'is_small_world': sigma > 1,
        'L_expected_sw': L_expected_sw,
        'L_ratio': L / L_expected_sw if L_expected_sw > 0 else 0,
        'interpretation': interpret_metrics(C, L, sigma, L_expected_sw)
    }


def interpret_metrics(C: float, L: float, sigma: float, L_expected: float) -> str:
    """Provide interpretation of small-world metrics."""
    parts = []
    
    if sigma > 1:
        parts.append(f"✓ Small-world (σ = {sigma:.2f} > 1)")
    else:
        parts.append(f"✗ Not small-world (σ = {sigma:.2f} ≤ 1)")
    
    if C > 0.5:
        parts.append(f"✓ High clustering (C = {C:.3f})")
    elif C > 0.1:
        parts.append(f"○ Moderate clustering (C = {C:.3f})")
    else:
        parts.append(f"✗ Low clustering (C = {C:.3f})")
    
    L_ratio = L / L_expected if L_expected > 0 else float('inf')
    if L_ratio < 2:
        parts.append(f"✓ Logarithmic scaling (L ≈ {L_ratio:.1f} × log(N)/log(k))")
    else:
        parts.append(f"✗ Non-logarithmic scaling (L = {L_ratio:.1f} × log(N)/log(k))")
    
    return "; ".join(parts)


def main():
    parser = argparse.ArgumentParser(description='Small-World Network Metrics Calculator')
    parser.add_argument('--nodes', '-n', type=int, default=100, help='Number of nodes')
    parser.add_argument('--degree', '-k', type=int, default=6, help='Average degree')
    parser.add_argument('--rewire', '-p', type=float, default=0.1, help='Rewiring probability')
    parser.add_argument('--seed', type=int, help='Random seed')
    parser.add_argument('--edgelist', type=str, help='Load graph from edge list CSV')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    if args.edgelist:
        # Load graph from file
        g = Graph()
        with open(args.edgelist, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split(',')
                    if len(parts) >= 2:
                        g.add_edge(int(parts[0]), int(parts[1]))
        print(f"Loaded graph with {len(g.nodes())} nodes and {len(g.edges())} edges")
    else:
        # Generate Watts-Strogatz graph
        g = watts_strogatz(args.nodes, args.degree, args.rewire, args.seed)
        print(f"Generated Watts-Strogatz graph: N={args.nodes}, k={args.degree}, p={args.rewire}")
    
    print("\nCalculating metrics...")
    metrics = small_world_metrics(g)
    
    if args.json:
        print(json.dumps(metrics, indent=2))
    else:
        print("\n" + "=" * 60)
        print("SMALL-WORLD NETWORK ANALYSIS")
        print("=" * 60)
        print(f"Nodes (N):                    {metrics['N']}")
        print(f"Edges (M):                    {metrics['M']}")
        print(f"Average degree (k):           {metrics['k']:.2f}")
        print("-" * 60)
        print(f"Clustering coefficient (C):   {metrics['C']:.4f}")
        print(f"Random graph C:               {metrics['C_random']:.4f}")
        print(f"γ = C/C_random:               {metrics['gamma']:.2f}")
        print("-" * 60)
        print(f"Path length (L):              {metrics['L']:.4f}")
        print(f"Random graph L:               {metrics['L_random']:.4f}")
        print(f"λ = L/L_random:               {metrics['lambda']:.2f}")
        print(f"Expected SW L [log(N)/log(k)]: {metrics['L_expected_sw']:.4f}")
        print("-" * 60)
        print(f"Small-world coefficient (σ):  {metrics['sigma']:.2f}")
        print(f"Is small-world:               {'YES' if metrics['is_small_world'] else 'NO'}")
        print("=" * 60)
        print(f"\nInterpretation: {metrics['interpretation']}")


if __name__ == '__main__':
    main()
