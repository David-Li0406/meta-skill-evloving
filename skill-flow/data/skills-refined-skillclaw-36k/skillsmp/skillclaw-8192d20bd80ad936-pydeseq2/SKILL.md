---
name: pydeseq2
description: Use this skill when performing differential gene expression analysis on bulk RNA-seq data, allowing for comparisons between experimental conditions and integration into Python-based workflows.
---

# PyDESeq2

## Overview

PyDESeq2 is a Python implementation of DESeq2 for differential expression analysis with bulk RNA-seq data. It enables users to design and execute complete workflows from data loading through result interpretation, including single-factor and multi-factor designs, Wald tests with multiple testing correction, and integration with pandas and AnnData.

## When to Use This Skill

This skill should be used when:
- Analyzing bulk RNA-seq count data for differential expression
- Comparing gene expression between experimental conditions (e.g., treated vs control)
- Performing multi-factor designs accounting for batch effects or covariates
- Converting R-based DESeq2 workflows to Python
- Integrating differential expression analysis into Python-based pipelines
- Users mention "DESeq2", "differential expression", "RNA-seq analysis", or "PyDESeq2"

## Quick Start Workflow

For users who want to perform a standard differential expression analysis:

```python
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

# 1. Load data
counts_df = pd.read_csv("counts.csv", index_col=0).T  # Transpose to samples × genes
metadata = pd.read_csv("metadata.csv", index_col=0)

# 2. Filter low-count genes
genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= 10]
counts_df = counts_df[genes_to_keep]

# 3. Initialize and fit DESeq2
dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~condition",
    refit_cooks=True
)
dds.deseq2()

# 4. Perform statistical testing
ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()

# 5. Access results
results = ds.results_df
significant = results[results.padj < 0.05]
print(f"Found {len(significant)} significant genes")
```

## Core Workflow Steps

### Step 1: Data Preparation

**Input requirements:**
- **Count matrix:** Samples × genes DataFrame with non-negative integer read counts
- **Metadata:** Samples × variables DataFrame with experimental factors

**Common data loading patterns:**

```python
# From CSV (typical format: genes × samples, needs transpose)
counts_df = pd.read_csv("counts.csv", index_col=0).T
metadata = pd.read_csv("metadata.csv", index_col=0)
```