---
name: scanpy
description: Use this skill when analyzing single-cell RNA-seq data for quality control, normalization, dimensionality reduction, clustering, and visualization.
---

# Scanpy: Single-Cell Analysis

## Overview

Scanpy is a scalable Python toolkit for analyzing single-cell RNA-seq data, built on AnnData. Apply this skill for complete single-cell workflows including quality control, normalization, dimensionality reduction, clustering, marker gene identification, visualization, and trajectory analysis.

## When to Use This Skill

This skill should be used when:
- Analyzing single-cell RNA-seq data (.h5ad, 10X, CSV formats)
- Performing quality control on scRNA-seq datasets
- Creating UMAP, t-SNE, or PCA visualizations
- Identifying cell clusters and finding marker genes
- Annotating cell types based on gene expression
- Conducting trajectory inference or pseudotime analysis
- Generating publication-quality single-cell plots

## Quick Start

### Basic Import and Setup

```python
import scanpy as sc
import pandas as pd
import numpy as np

# Configure settings
sc.settings.verbosity = 3
sc.settings.set_figure_params(dpi=80, facecolor='white')
sc.settings.figdir = './figures/'
```

### Loading Data

```python
# From 10X Genomics
adata = sc.read_10x_mtx('path/to/data/')
adata = sc.read_10x_h5('path/to/data.h5')

# From h5ad (AnnData format)
adata = sc.read_h5ad('path/to/data.h5ad')

# From CSV
adata = sc.read_csv('path/to/data.csv')
```

### Understanding AnnData Structure

The AnnData object is the core data structure in scanpy:

```python
adata.X          # Expression matrix (cells × genes)
adata.obs        # Cell metadata (DataFrame)
adata.var        # Gene metadata (DataFrame)
adata.uns        # Unstructured annotations (dict)
adata.obsm       # Multi-dimensional cell data (PCA, UMAP)
adata.raw        # Raw data backup

# Access cell and gene names
adata.obs_names  # Cell barcodes
adata.var_names  # Gene names
```

## Standard Analysis Workflow

### 1. Quality Control

Identify and filter low-quality cells and genes:

```python
# Identify mitochondrial genes
adata.var['mt'] = adata.var_names.str.startswith('MT-')

# Calculate QC metrics
sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], inplace=True)

# Visualize QC metrics
sc.pl.violin(adata, ['n_genes', 'n_counts', 'percent_mito'], jitter=0.4)
```

### 2. Normalization

Normalize the data to account for differences in sequencing depth:

```python
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)  # Log-transform the data
```

### 3. Dimensionality Reduction

Perform PCA, UMAP, or t-SNE for visualization:

```python
sc.pp.pca(adata, n_comps=50)
sc.pp.neighbors(adata)
sc.tl.umap(adata)
```

### 4. Clustering

Cluster the cells based on their expression profiles:

```python
sc.tl.leiden(adata)
```

### 5. Visualization

Visualize the results:

```python
sc.pl.umap(adata, color=['leiden', 'gene_name'])
```