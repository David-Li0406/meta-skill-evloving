---
name: arboreto
description: Use this skill when inferring gene regulatory networks (GRNs) from gene expression data to identify transcription factor-target gene relationships and regulatory interactions.
---

# Arboreto

## Overview

Arboreto is a computational library for inferring gene regulatory networks (GRNs) from gene expression data using scalable algorithms (GRNBoost2, GENIE3). It supports distributed computation for large-scale datasets.

**Core capability**: Identify which transcription factors (TFs) regulate which target genes based on expression patterns across observations (cells, samples, conditions).

## Quick Start

Install arboreto:
```bash
uv pip install arboreto
```

Basic GRN inference:
```python
import pandas as pd
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Load expression data (genes as columns)
    expression_matrix = pd.read_csv('expression_data.tsv', sep='\t')

    # Infer regulatory network
    network = grnboost2(expression_data=expression_matrix)

    # Save results (TF, target, importance)
    network.to_csv('network.tsv', sep='\t', index=False, header=False)
```

**Critical**: Always use `if __name__ == '__main__':` guard because Dask spawns new processes.

## Core Capabilities

### 1. Basic GRN Inference

For standard GRN inference workflows including:
- Input data preparation (Pandas DataFrame or NumPy array)
- Running inference with GRNBoost2 or GENIE3
- Filtering by transcription factors
- Output format and interpretation

**Use the ready-to-run script** for standard inference tasks:
```bash
python scripts/basic_grn_inference.py expression_data.tsv output_network.tsv --tf-file tfs.txt --seed 777
```

### 2. Algorithm Selection

Arboreto provides two algorithms:

**GRNBoost2 (Recommended)**:
- Fast gradient boosting-based inference
- Optimized for large datasets (10k+ observations)
- Default choice for most analyses

**GENIE3**:
- Random Forest-based inference
- Original multiple regression approach
- Use for comparison or validation

Quick comparison:
```python
from arboreto.algo import grnboost2, genie3

# Fast, recommended
network_grnboost = grnboost2(expression_data=matrix)

# Classic algorithm
network_genie3 = genie3(expression_data=matrix)
```