---
name: anndata
description: Use this skill when working with annotated data matrices in single-cell analysis, particularly with .h5ad files and the scverse ecosystem.
---

# AnnData

## Overview

AnnData is a Python package for handling annotated data matrices, storing experimental measurements (X) alongside observation metadata (obs), variable metadata (var), and multi-dimensional annotations (obsm, varm, obsp, varp, uns). Originally designed for single-cell genomics through Scanpy, it now serves as a general-purpose framework for any annotated data requiring efficient storage, manipulation, and analysis.

## When to Use This Skill

Use this skill when:
- Creating, reading, or writing AnnData objects
- Working with h5ad, zarr, or other genomics data formats
- Performing single-cell RNA-seq analysis
- Managing large datasets with sparse matrices or backed mode
- Concatenating multiple datasets or experimental batches
- Subsetting, filtering, or transforming annotated data
- Integrating with scanpy, scvi-tools, or other scverse ecosystem tools

## Installation

```bash
uv pip install anndata

# With optional dependencies
uv pip install anndata[dev,test,doc]
```

## Quick Start

### Creating an AnnData object
```python
import anndata as ad
import numpy as np
import pandas as pd

# Minimal creation
X = np.random.rand(100, 2000)  # 100 cells × 2000 genes
adata = ad.AnnData(X)

# With metadata
obs = pd.DataFrame({
    'cell_type': ['T cell', 'B cell'] * 50,
    'sample': ['A', 'B'] * 50
}, index=[f'cell_{i}' for i in range(100)])

var = pd.DataFrame({
    'gene_name': [f'Gene_{i}' for i in range(2000)]
}, index=[f'ENSG{i:05d}' for i in range(2000)])

adata = ad.AnnData(X=X, obs=obs, var=var)
```

### Reading data
```python
# Read h5ad file
adata = ad.read_h5ad('data.h5ad')

# Read with backed mode (for large files)
adata = ad.read_h5ad('large_data.h5ad', backed='r')

# Read other formats
adata = ad.read_csv('data.csv')
adata = ad.read_loom('data.loom')
adata = ad.read_10x_h5('filtered_feature_bc_matrix.h5')
```

### Writing data
```python
# Write h5ad file
adata.write_h5ad('output.h5ad')

# Write with compression
adata.write_h5ad('output.h5ad', compression='gzip')

# Write other formats
adata.write_zarr('output.zarr')
```