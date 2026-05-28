---
name: networkx
description: Use this skill when creating, analyzing, and visualizing complex networks and graphs in Python, applicable to various domains involving relationships between entities.
---

# NetworkX

## Overview

NetworkX is a Python package for creating, manipulating, and analyzing complex networks and graphs. Use this skill when working with network or graph data structures, including social networks, biological networks, transportation systems, citation networks, knowledge graphs, or any system involving relationships between entities.

## When to Use This Skill

Invoke this skill when tasks involve:

- **Creating graphs**: Building network structures from data, adding nodes and edges with attributes.
- **Graph analysis**: Computing centrality measures, finding shortest paths, detecting communities, measuring clustering.
- **Graph algorithms**: Running standard algorithms like Dijkstra's, PageRank, minimum spanning trees, maximum flow.
- **Network generation**: Creating synthetic networks (random, scale-free, small-world models) for testing or simulation.
- **Graph I/O**: Reading from or writing to various formats (edge lists, GraphML, JSON, CSV, adjacency matrices).
- **Visualization**: Drawing and customizing network visualizations with matplotlib or interactive libraries.
- **Network comparison**: Checking isomorphism, computing graph metrics, analyzing structural properties.

## Core Capabilities

### 1. Graph Creation and Manipulation

NetworkX supports four main graph types:
- **Graph**: Undirected graphs with single edges.
- **DiGraph**: Directed graphs with one-way connections.
- **MultiGraph**: Undirected graphs allowing multiple edges between nodes.
- **MultiDiGraph**: Directed graphs with multiple edges.

Create graphs by:
```python
import networkx as nx

# Create empty graph
G = nx.Graph()

# Add nodes (can be any hashable type)
G.add_node(1)
G.add_nodes_from([2, 3, 4])
G.add_node("protein_A", type='enzyme', weight=1.5)

# Add edges
G.add_edge(1, 2)
G.add_edges_from([(1, 3), (2, 4)])
G.add_edge(1, 4, weight=0.8, relation='interacts')
```