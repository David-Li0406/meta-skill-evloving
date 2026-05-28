---
name: geo-database
description: Access NCBI GEO for gene expression/genomics data. Search/download microarray and RNA-seq datasets (GSE, GSM, GPL), retrieve SOFT/Matrix files, for transcriptomics and expression analysis.
---

# GEO Database

## Overview

The Gene Expression Omnibus (GEO) is NCBI's public repository for high-throughput gene expression and functional genomics data. GEO contains over 264,000 studies with more than 8 million samples from both array-based and sequence-based experiments.

## When to Use This Skill

This skill should be used when searching for gene expression datasets, retrieving experimental data, downloading raw and processed files, querying expression profiles, or integrating GEO data into computational analysis workflows.

## Core Capabilities

### 1. Understanding GEO Data Organization

GEO organizes data hierarchically using different accession types:

**Series (GSE):** A complete experiment with a set of related samples
- Example: GSE123456
- Contains experimental design, samples, and overall study information
- Largest organizational unit in GEO
- Current count: 264,928+ series

**Sample (GSM):** A single experimental sample or biological replicate
- Example: GSM987654
- Contains individual sample data, protocols, and metadata
- Linked to platforms and series
- Current count: 8,068,632+ samples

**Platform (GPL):** The microarray or sequencing platform used
- Example: GPL570 (Affymetrix Human Genome U133 Plus 2.0 Array)
- Describes the technology and probe/feature annotations
- Shared across multiple experiments
- Current count: 27,739+ platforms

**DataSet (GDS):** Curated collections with consistent formatting
- Example: GDS5678
- Experimentally-comparable samples organized by study design
- Processed for differential analysis
- Subset of GEO data (4,348 curated datasets)
- Ideal for quick comparative analyses

**Profiles:** Gene-specific expression data linked to sequence features
- Queryable by gene name or annotation
- Cross-references to Entrez Gene
- Enables gene-centric searches across all studies

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
        retmax=retmax,
        usehistory="y"
    )
    results = Entrez.read(handle)
    handle.close()
    return results

# Example searches
results = search_geo_datasets("breast cancer[MeSH] AND Homo sapiens[Organism]")
print(f"Found {results['Count']} datasets")

# Search by specific platform
results = search_geo_datasets("GPL570[Accession]")

# Search by study type
results = search_geo_datasets("expression profiling by array[DataSet Type]")
```

**GEO Profiles Search:**

Find gene-specific expression patterns:

```python
# Search for gene expression profiles
def search_geo_profiles(gene_name, organism="Homo sapiens", retmax=100):
    """Search GEO Profiles for a specific gene"""
    query = f"{gene_name}[Gene Name] AND {organism}[Organism]"
    handle = Entrez.esearch(
        db="geoprofiles",
        term=query,
        retmax=retmax
    )
    results = Entrez.read(handle)
    handle.close()
    return results

# Find TP53 expression across studies
tp53_results = search_geo_profiles("TP53", organism="Homo sapiens")
print(f"Found {tp53_results['Count']} expression profiles for TP53")
```

**Advanced Search Patterns:**

```python
# Combine multiple search terms
def advanced_geo_search(terms, operator="AND"):
    """Build complex search queries"""
    query = f" {operator} ".join(terms)
    return search_geo_datasets(query)

# Find recent high-throughput studies
search_terms = [
    "RNA-seq[DataSet Type]",
    "Homo sapiens[Organism]",
    "2024[Publication Date]"
]
results = advanced_geo_search(search_terms)

# Search by author and condition
search_terms = [
    "Smith[Author]",
    "diabetes[Disease]"
]
results = advanced_geo_search(search_terms)
```

### 3. Retrieving GEO Data with GEOparse (Recommended)

**GEOparse** is the primary Python library for accessing GEO data:

**Installation:**
```bash
uv pip install GEOparse
```

**Basic Usage:**

```python
import GEOparse

# Download and parse a GEO Series
gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")

# Access series metadata
print(gse.metadata['title'])
print(gse.metadata['summary'])
print(gse.metadata['overall_design'])

# Access sample information
for gsm_name, gsm in gse.gsms.items():
    print(f"Sample: {gsm_name}")
    print(f"  Title: {gsm.metadata['title'][0]}")
    print(f"  Source: {gsm.metadata['source_name_ch1'][0]}")
    print(f"  Characteristics: {gsm.metadata.get('characteristics_ch1', [])}")

# Access platform information
for gpl_name, gpl in gse.gpls.items():
    print(f"Platform: {gpl_name}")
    print(f"  Title: {gpl.metadata['title'][0]}")
    print(f"  Organism: {gpl.metadata['organism'][0]}")
```

**Working with Expression Data:**

```python
import GEOparse
import pandas as pd

# Get expression data from series
gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")

# Extract expression matrix
# Method 1: From series matrix file (fastest)
if hasattr(gse, 'pivot_samples'):
    expression_df = gse.pivot_samples('VALUE')
    print(expression_df.shape)  # genes x samples

# Method 2: From individual samples
expression_data = {}
for gsm_name, gsm in gse.gsms.items():
    if hasattr(gsm, 'table'):
        expression_data[gsm_name] = gsm.table['VALUE']

expression_df = pd.DataFrame(expression_data)
print(f"Expression matrix: {expression_df.shape}")
```

**Accessing Supplementary Files:**

```python
import GEOparse

gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")

# Download supplementary files
gse.download_supplementary_files(
    directory="./data/GSE123456_suppl",
    download_sra=False  # Set to True to download SRA files
)

# List available supplementary files
for gsm_name, gsm in gse.gsms.items():
    if hasattr(gsm, 'supplementary_files'):
        print(f"Sample {gsm_name}:")
        for file_url in gsm.metadata.get('supplementary_file', []):
            print(f"  {file_url}")
```

**Filtering and Subsetting Data:**

```python
import GEOparse

gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")

# Filter samples by metadata
control_samples = [
    gsm_name for gsm_name, gsm in gse.gsms.items()
    if 'control' in gsm.metadata.get('title', [''])[0].lower()
]

treatment_samples = [
    gsm_name for gsm_name, gsm in gse.gsms.items()
    if 'treatment' in gsm.metadata.get('title', [''])[0].lower()
]

print(f"Control samples: {len(control_samples)}")
print(f"Treatment samples: {len(treatment_samples)}")

# Extract subset expression matrix
expression_df = gse.pivot_samples('VALUE')
control_expr = expression_df[control_samples]
treatment_expr = expression_df[treatment_samples]
```

### 4. Using NCBI E-utilities for GEO Access

**E-utilities** provide lower-level programmatic access to GEO metadata:

**Basic E-utilities Workflow:**

```python
from Bio import Entrez
import time

Entrez.email = "your.email@example.com"

# Step 1: Search for GEO entries
def search_geo(query, db="gds", retmax=100):
    """Search GEO using E-utilities"""
    handle = Entrez.esearch(
        db=db,
        term=query,
        retmax=retmax,
        usehistory="y"
    )
    results = Entrez.read(handle)
    handle.close()
    return results

# Step 2: Fetch summaries
def fetch_geo_summaries(id_list, db="gds"):
    """Fetch document summaries for GEO entries"""
    ids = ",".join(id_list)
    handle = Entrez.esummary(db=db, id=ids)
    summaries = Entrez.read(handle)
    handle.close()
    return summaries

# Step 3: Fetch full records
def fetch_geo_records(id_list, db="gds"):
    """Fetch full GEO records"""
    ids = ",".join(id_list)
    handle = Entrez.efetch(db=db, id=ids, retmode="xml")
    records = Entrez.read(handle)
    handle.close()
    return records

# Example workflow
search_results = search_geo("breast cancer AND Homo sapiens")
id_list = search_results['IdList'][:5]

summaries = fetch_geo_summaries(id_list)
for summary in summaries:
    print(f"GDS: {summary.get('Accession', 'N/A')}")
    print(f"Title: {summary.get('title', 'N/A')}")
    print(f"Samples: {summary.get('n_samples', 'N/A')}")
    print()
```

**Batch Processing with E-utilities:**

```python
from Bio import Entrez
import time

Entrez.email = "your.email@example.com"

def batch_fetch_geo_metadata(accessions, batch_size=100):
    """Fetch metadata for multiple GEO accessions"""
    results = {}

    for i in range(0, len(accessions), batch_size):
        batch = accessions[i:i + batch_size]

        # Search for each accession
        for accession in batch:
            try:
                query = f"{accession}[Accession]"
                search_handle = Entrez.esearch(db="gds", term=query)
                search_results = Entrez.read(search_handle)
                search_handle.close()

                if search_results['IdList']:
                    # Fetch summary
                    summary_handle = Entrez.esummary(
                        db="gds",
                        id=search_results['IdList'][0]
                    )
                    summary = Entrez.read(summary_handle)
                    summary_handle.close()
                    results[accession] = summary[0]

                # Be polite to NCBI servers
                time.sleep(0.34)  # Max 3 requests per second

            except Exception as e:
                print(f"Error fetching {accession}: {e}")

    return results

# Fetch metadata for multiple datasets
gse_list = ["GSE100001", "GSE100002", "GSE100003"]
metadata = batch_fetch_geo_metadata(gse_list)
```

### 5. Direct FTP Access for Data Files

**FTP URLs for GEO Data:**

GEO data can be downloaded directly via FTP:

```python
import ftplib
import os

def download_geo_ftp(accession, file_type="matrix", dest_dir="./data"):
    """Download GEO files via FTP"""
    # Construct FTP path based on accession type
    if accession.startswith("GSE"):
        # Series files
        gse_num = accession[3:]
        base_num = gse_num[:-3] + "nnn"
        ftp_path = f"/geo/series/GSE{base_num}/{accession}/"

        if file_type == "matrix":
            filename = f"{accession}_series_matrix.txt.gz"
        elif file_type == "soft":
            filename = f"{accession}_family.soft.gz"
        elif file_type == "miniml":
            filename = f"{accession}_family.xml.tgz"

    # Connect to FTP server
    ftp = ftplib.FTP("ftp.ncbi.nlm.nih.gov")
    ftp.login()
    ftp.cwd(ftp_path)

    # Download file
    os.makedirs(dest_dir, exist_ok=True)
    local_file = os.path.join(dest_dir, filename)

    with open(local_file, 'wb') as f:
        ftp.retrbinary(f'RETR {filename}', f.write)

    ftp.quit()
    print(f"Downloaded: {local_file}")
    return local_file

# Download series matrix file
download_geo_ftp("GSE123456", file_type="matrix")

# Download SOFT format file
download_geo_ftp("GSE123456", file_type="soft")
```

**Using wget or curl for Downloads:**

```bash
# Download series matrix file
wget ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE123nnn/GSE123456/matrix/GSE123456_series_matrix.txt.gz

# Download all supplementary files for a series
wget -r -np -nd ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE123nnn/GSE123456/suppl/

# Download SOFT format family file
wget ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE123nnn/GSE123456/soft/GSE123456_family.soft.gz
```

### 6. Analyzing GEO Data

**Quality Control and Preprocessing:**

```python
import GEOparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")
expression_df = gse.pivot_samples('VALUE')

# Check for missing values
print(f"Missing values: {expression_df.isnull().sum().sum()}")

# Log transformation (if needed)
if expression_df.min().min() > 0:  # Check if already log-transformed
    if expression_df.max().max() > 100:
        expression_df = np.log2(expression_df + 1)
        print("Applied log2 transformation")

# Distribution plots
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
expression_df.plot.box(ax=plt.gca())
plt.title("Expression Distribution per Sample")
plt.xticks(rotation=90)

plt.subplot(1, 2, 2)
expression_df.mean(axis=1).hist(bins=50)
plt.title("Gene Expression Distribution")
plt.xlabel("Average Expression")

plt.tight_layout()
plt.savefig("geo_qc.png", dpi=300, bbox_inches='tight')
```

**Differential Expression Analysis:**

```python
import GEOparse
import pandas as pd
import numpy as np
from scipy import stats

gse = GEOparse.get_GEO(geo="GSE123456", destdir="./data")
expression_df = gse.pivot_samples('VALUE')

# Define sample groups
control_samples = ["GSM1", "GSM2", "GSM3"]
treatment_samples = ["GSM4", "GSM5", "GSM6"]

# Calculate fold changes and p-values
results = []
for gene in expression_df.index:
    control_expr = expression_df.loc[gene, control_samples]
    treatment_expr = expression_df.loc[gene, treatment_samples]

    # Calculate statistics
    fold_change = treatment_expr.mean() - control_expr.mean()
    t_stat, p_value = stats.ttest_ind(treatment_expr, control_expr)

    results.append({
        'gene': gene,
        'log2_fold_change': fold_change,
        'p_value': p_value,
        'control_mean': control_expr.mean(),
        'treatment_mean': treatment_expr.mean()
    })

# Create results DataFrame
de_results = pd.DataFrame(results)

# Multiple testing correction (Benjamini-Hochberg)
from statsmodels.stats.multitest import multipletests
_, de_results['q_value'], _, _ = multipletests(
    de_results['p_value'],
    method='fdr_bh'
)

# Filter significant genes
significant_genes = de_results[
    (de_results['q_value'] < 0.05) &
    (abs(de_results['log2_fold_change']) > 1)