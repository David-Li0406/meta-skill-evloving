---
name: torchdrug
description: Use this skill when building custom graph neural network architectures for drug discovery, protein modeling, or knowledge graph reasoning.
---

# Skill body

## Overview

TorchDrug is a comprehensive PyTorch-based machine learning toolbox for drug discovery and molecular science. It allows the application of graph neural networks, pre-trained models, and task definitions to molecules, proteins, and biological knowledge graphs. Key functionalities include molecular property prediction, protein modeling, knowledge graph reasoning, molecular generation, and retrosynthesis planning, supported by 40+ curated datasets and 20+ model architectures.

## When to Use This Skill

This skill should be used when working with:

**Data Types:**
- SMILES strings or molecular structures
- Protein sequences or 3D structures (PDB files)
- Chemical reactions and retrosynthesis
- Biomedical knowledge graphs
- Drug discovery datasets

**Tasks:**
- Predicting molecular properties (solubility, toxicity, activity)
- Protein function or structure prediction
- Drug-target binding prediction
- Generating new molecular structures
- Planning chemical synthesis routes
- Link prediction in biomedical knowledge bases
- Training graph neural networks on scientific data

**Libraries and Integration:**
- TorchDrug is the primary library
- Often used with RDKit for cheminformatics
- Compatible with PyTorch and PyTorch Lightning
- Integrates with AlphaFold and ESM for proteins

## Getting Started

### Installation

```bash
pip install torchdrug
# Or with optional dependencies
pip install torchdrug[full]
```

### Quick Example

```python
from torchdrug import datasets, models, tasks
from torch.utils.data import DataLoader

# Load molecular dataset
dataset = datasets.BBBP("~/molecule-datasets/")
train_set, valid_set, test_set = dataset.split()

# Define GNN model
model = models.GIN(
    input_dim=dataset.node_feature_dim,
    hidden_dims=[256, 256, 256],
    edge_input_dim=dataset.edge_feature_dim,
    batch_norm=True,
    readout="mean"
)

# Create property prediction task
task = tasks.PropertyPrediction(
    model,
    task=dataset.tasks,
    criterion="bce",
    metric=["auroc", "auprc"]
)

# Train with PyTorch
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
```