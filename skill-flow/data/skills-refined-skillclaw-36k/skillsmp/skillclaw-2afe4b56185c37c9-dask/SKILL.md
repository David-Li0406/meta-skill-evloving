---
name: dask
description: Use this skill when you need to scale existing pandas/NumPy code beyond memory limits or across clusters for distributed computing.
---

# Dask

## Overview

Dask is a Python library for parallel and distributed computing that enables three critical capabilities:
- **Larger-than-memory execution** on single machines for data exceeding available RAM.
- **Parallel processing** for improved computational speed across multiple cores.
- **Distributed computation** supporting terabyte-scale datasets across multiple machines.

Dask scales from laptops (processing ~100 GiB) to clusters (processing ~100 TiB) while maintaining familiar Python APIs.

## When to Use This Skill

This skill should be used when:
- Processing datasets that exceed available RAM.
- Scaling pandas or NumPy operations to larger datasets.
- Parallelizing computations for performance improvements.
- Processing multiple files efficiently (CSVs, Parquet, JSON, text logs).
- Building custom parallel workflows with task dependencies.
- Distributing workloads across multiple cores or machines.

## Core Capabilities

Dask provides five main components, each suited to different use cases:

### 1. DataFrames - Parallel Pandas Operations

**Purpose**: Scale pandas operations to larger datasets through parallel processing.

**When to Use**:
- Tabular data exceeds available RAM.
- Need to process multiple CSV/Parquet files together.
- Pandas operations are slow and need parallelization.
- Scaling from pandas prototype to production.

**Quick Example**:
```python
import dask.dataframe as dd

# Read multiple files as single DataFrame
ddf = dd.read_csv('data/2024-*.csv')

# Operations are lazy until compute()
filtered = ddf[ddf['value'] > 100]
result = filtered.groupby('category').mean().compute()
```

**Key Points**:
- Operations are lazy (build task graph) until explicitly computed.
- Dask integrates seamlessly with existing pandas workflows.