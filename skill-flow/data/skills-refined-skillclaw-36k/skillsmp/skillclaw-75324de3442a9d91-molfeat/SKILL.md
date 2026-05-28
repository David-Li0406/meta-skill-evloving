---
name: molfeat
description: Use this skill for molecular featurization in machine learning, converting chemical structures into numerical representations for tasks like QSAR modeling and virtual screening.
---

# Molfeat - Molecular Featurization Hub

## Overview

Molfeat is a comprehensive Python library for molecular featurization that unifies 100+ pre-trained embeddings and hand-crafted featurizers. It converts chemical structures (SMILES strings or RDKit molecules) into numerical representations for machine learning tasks, including QSAR modeling, virtual screening, similarity searching, and deep learning applications. The library features fast parallel processing, scikit-learn compatible transformers, and built-in caching.

## When to Use This Skill

This skill should be used when working with:
- **Molecular machine learning**: Building QSAR/QSPR models, property prediction
- **Virtual screening**: Ranking compound libraries for biological activity
- **Similarity searching**: Finding structurally similar molecules
- **Chemical space analysis**: Clustering, visualization, dimensionality reduction
- **Deep learning**: Training neural networks on molecular data
- **Featurization pipelines**: Converting SMILES to ML-ready representations
- **Cheminformatics**: Any task requiring molecular feature extraction

## Installation

```bash
pip install molfeat

# With all optional dependencies
pip install "molfeat[all]"
```

**Optional dependencies for specific featurizers:**
- `molfeat[dgl]` - GNN models (GIN variants)
- `molfeat[graphormer]` - Graphormer models
- `molfeat[transformer]` - ChemBERTa, ChemGPT, MolT5
- `molfeat[fcd]` - FCD descriptors
- `molfeat[map4]` - MAP4 fingerprints

## Core Concepts

Molfeat organizes featurization into three hierarchical classes:

### 1. Calculators (`molfeat.calc`)

Callable objects that convert individual molecules into feature vectors. They accept RDKit `Chem.Mol` objects or SMILES strings.

**Use calculators for:**
- Single molecule featurization
- Custom processing loops
- Direct feature computation

**Example:**
```python
from molfeat.calc import FPCalculator

calc = FPCalculator("ecfp", radius=3, fpSize=2048)
features = calc("CCO")  # Returns numpy array (2048,)
```

### 2. Transformers (`molfeat.trans`)

Scikit-learn compatible transformers that wrap calculators for batch processing with parallelization.

**Use transformers for:**
- Batch featurization of molecular datasets
- Integration with scikit-learn pipelines
- Parallel processing