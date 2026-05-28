---
name: geniml
description: Use this skill when working with genomic interval data (BED files) for machine learning tasks, such as training region embeddings, single-cell ATAC-seq analysis, and building consensus peaks.
---

# Geniml: Genomic Interval Machine Learning

## Overview

Geniml is a Python package for building machine learning models on genomic interval data from BED files. It provides unsupervised methods for learning embeddings of genomic regions, single cells, and metadata labels, enabling similarity searches, clustering, and downstream ML tasks.

## Installation

Install geniml using uv:

```bash
uv uv pip install geniml
```

For ML dependencies (PyTorch, etc.):

```bash
uv uv pip install 'geniml[ml]'
```

Development version from GitHub:

```bash
uv uv pip install git+https://github.com/databio/geniml.git
```

## Core Capabilities

Geniml provides several primary capabilities:

### 1. Region2Vec: Genomic Region Embeddings

Train unsupervised embeddings of genomic regions using word2vec-style learning.

**Use for:** Dimensionality reduction of BED files, region similarity analysis, feature vectors for downstream ML.

**Workflow:**
1. Tokenize BED files using a universe reference.
2. Train Region2Vec model on tokens.
3. Generate embeddings for regions.

### 2. BEDspace: Joint Region and Metadata Embeddings

Train shared embeddings for region sets and metadata labels using StarSpace.

**Use for:** Metadata-aware searches, cross-modal queries (region→label or label→region), joint analysis of genomic content and experimental conditions.

**Workflow:**
1. Preprocess regions and metadata.
2. Train BEDspace model.
3. Compute distances.
4. Query across regions and labels.

### 3. scEmbed: Single-Cell Chromatin Accessibility Embeddings

Train Region2Vec models on single-cell ATAC-seq data for cell-level embeddings.

**Use for:** scATAC-seq clustering, cell-type annotation, dimensionality reduction of single cells, integration with scanpy workflows.

**Workflow:**
1. Prepare AnnData with peak coordinates.
2. Train scEmbed model on the data.
3. Generate embeddings for single cells.

## Conclusion

Geniml is a versatile tool for genomic interval data analysis, providing essential methods for embedding learning and machine learning applications in bioinformatics.