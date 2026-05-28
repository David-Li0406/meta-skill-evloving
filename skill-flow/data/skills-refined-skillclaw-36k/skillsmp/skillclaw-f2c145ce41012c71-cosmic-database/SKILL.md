---
name: cosmic-database
description: Use this skill when you need to access the COSMIC cancer mutation database for querying somatic mutations, Cancer Gene Census, mutational signatures, and gene fusions in cancer research and precision oncology.
---

# COSMIC Database

## Overview

COSMIC (Catalogue of Somatic Mutations in Cancer) is the world's largest and most comprehensive database for exploring somatic mutations in human cancer. Access COSMIC's extensive collection of cancer genomics data, including millions of mutations across thousands of cancer types, curated gene lists, mutational signatures, and clinical annotations programmatically.

## When to Use This Skill

This skill should be used when:
- Downloading cancer mutation data from COSMIC
- Accessing the Cancer Gene Census for curated cancer gene lists
- Retrieving mutational signature profiles
- Querying structural variants, copy number alterations, or gene fusions
- Analyzing drug resistance mutations
- Working with cancer cell line genomics data
- Integrating cancer mutation data into bioinformatics pipelines
- Researching specific genes or mutations in cancer contexts

## Prerequisites

### Account Registration
COSMIC requires authentication for data downloads:
- **Academic users**: Free access with registration at [COSMIC Registration](https://cancer.sanger.ac.uk/cosmic/register)
- **Commercial users**: License required (contact QIAGEN)

### Python Requirements
```bash
pip install requests pandas
```

## Quick Start

### 1. Basic File Download

Use the following code to download COSMIC data files:

```python
from scripts.download_cosmic import download_cosmic_file

# Download mutation data
download_cosmic_file(
    email="your_email@institution.edu",
    password="your_password",
    filepath="GRCh38/cosmic/latest/CosmicMutantExport.tsv.gz",
    output_filename="cosmic_mutations.tsv.gz"
)
```

### 2. Command-Line Usage

```bash
# Download using shorthand data type
python scripts/download_cosmic.py user@email.com --data-type mutations

# Download specific file
python scripts/download_cosmic.py user@email.com \
    --filepath GRCh38/cosmic/latest/cancer_gene_census.csv

# Download for specific genome assembly
python scripts/download_cosmic.py user@email.com \
    --data-type gene_census --assembly GRCh37 -o cancer_genes.csv
```

### 3. Working with Downloaded Data

```python
import pandas as pd

# Read mutation data
mutations = pd.read_csv('cosmic_mutations.tsv.gz', sep='\t', compression='gzip')
```