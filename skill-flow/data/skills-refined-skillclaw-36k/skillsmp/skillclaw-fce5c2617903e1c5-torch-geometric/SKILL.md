---
name: torch-geometric
description: Use this skill when developing and training Graph Neural Networks (GNNs) for tasks such as node classification, link prediction, and molecular property prediction.
---

# PyTorch Geometric (PyG)

## Overview

PyTorch Geometric is a library built on PyTorch for developing and training Graph Neural Networks (GNNs). This skill is applicable for deep learning on graphs and irregular structures, including mini-batch processing, multi-GPU training, and geometric deep learning applications.

## When to Use This Skill

Use this skill when working with:
- **Graph-based machine learning**: Node classification, graph classification, link prediction
- **Molecular property prediction**: Drug discovery, chemical property prediction
- **Social network analysis**: Community detection, influence prediction
- **Citation networks**: Paper classification, recommendation systems
- **3D geometric data**: Point clouds, meshes, molecular structures
- **Heterogeneous graphs**: Multi-type nodes and edges (e.g., knowledge graphs)
- **Large-scale graph learning**: Neighbor sampling, distributed training

## Quick Start

### Installation

```bash
pip install torch_geometric
```

For additional dependencies (sparse operations, clustering):
```bash
pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-${TORCH}+${CUDA}.html
```

### Basic Graph Creation

```python
import torch
from torch_geometric.data import Data

# Create a simple graph with 3 nodes
edge_index = torch.tensor([[0, 1, 1, 2],  # source nodes
                           [1, 0, 2, 1]], dtype=torch.long)  # target nodes
x = torch.tensor([[-1], [0], [1]], dtype=torch.float)  # node features

data = Data(x=x, edge_index=edge_index)
print(f"Nodes: {data.num_nodes}, Edges: {data.num_edges}")
```

### Loading a Benchmark Dataset

```python
from torch_geometric.datasets import Planetoid

# Load Cora citation network
dataset = Planetoid(root='/tmp/Cora', name='Cora')
data = dataset[0]  # Get the first (and only) graph

print(f"Dataset: {dataset}")
print(f"Nodes: {data.num_nodes}, Edges: {data.num_edges}")
print(f"Features: {data.num_node_features}, Classes: {dataset.num_classes}")
```

## Core Concepts

### Data Structure

PyG represents graphs using the `torch_geometric.data.Data` class with these key attributes:

- **`data.x`**: Node feature matrix `[num_nodes, num_node_features]`
- **`data.edge_index`**: Graph connectivity in COO format