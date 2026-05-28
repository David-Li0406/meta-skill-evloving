---
name: geo-database
description: Use this skill when you need to access NCBI GEO for gene expression and genomics data, including searching and downloading microarray and RNA-seq datasets.
---

# GEO Database

## Overview

The Gene Expression Omnibus (GEO) is NCBI's public repository for high-throughput gene expression and functional genomics data. GEO contains over 264,000 studies with more than 8 million samples from both array-based and sequence-based experiments.

## When to Use This Skill

This skill should be used when searching for gene expression datasets, retrieving experimental data, downloading raw and processed files, querying expression profiles, or integrating GEO data into computational analysis workflows.

## Core Capabilities

### 1. Understanding GEO Data Organization

GEO organizes data hierarchically using different accession types:

- **Series (GSE):** A complete experiment with a set of related samples (e.g., GSE123456).
- **Sample (GSM):** A single experimental sample or biological replicate (e.g., GSM987654).
- **Platform (GPL):** The microarray or sequencing platform used (e.g., GPL570).
- **DataSet (GDS):** Curated collections with consistent formatting (e.g., GDS5678).
- **Profiles:** Gene-specific expression data linked to sequence features.

### 2. Searching GEO Data

**GEO DataSets Search:**

Search for studies by keywords, organism, or experimental conditions:

```python
from Bio import Entrez

# Configure Entrez (required)
Entrez.email = "your.email@example.com"

# Search for datasets
def search_geo_datasets(query, retmax=20):
    """Search GEO DataSets database"""
    handle = Entrez.esearch(
        db="gds",
        term=query,
        retmax=retmax
    )
    record = Entrez.read(handle)
    handle.close()
    return record['IdList']
```

### 3. Downloading Data

To download datasets, you can use the following function:

```python
def download_geo_data(accession_id):
    """Download GEO data for a given accession ID"""
    url = f"https://ftp.ncbi.nlm.nih.gov/geo/series/{accession_id[0:6]}/{accession_id}/soft/{accession_id}.soft.gz"
    response = requests.get(url)
    with open(f"{accession_id}.soft.gz", 'wb') as f:
        f.write(response.content)
```