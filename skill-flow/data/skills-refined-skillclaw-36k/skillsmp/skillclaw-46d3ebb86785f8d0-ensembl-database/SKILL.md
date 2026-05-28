---
name: ensembl-database
description: Use this skill when you need to query the Ensembl genome database for gene information, sequence retrieval, variant analysis, and comparative genomics across over 250 species.
---

# Ensembl Database

## Overview

Access and query the Ensembl genome database, a comprehensive resource for vertebrate genomic data maintained by EMBL-EBI. The database provides gene annotations, sequences, variants, regulatory information, and comparative genomics data for over 250 species. Current release is 115 (September 2025).

## When to Use This Skill

This skill should be used when:

- Querying gene information by symbol or Ensembl ID
- Retrieving DNA, transcript, or protein sequences
- Analyzing genetic variants using the Variant Effect Predictor (VEP)
- Finding orthologs and paralogs across species
- Accessing regulatory features and genomic annotations
- Converting coordinates between genome assemblies (e.g., GRCh37 to GRCh38)
- Performing comparative genomics analyses
- Integrating Ensembl data into genomic research pipelines

## Core Capabilities

### 1. Gene Information Retrieval

Query gene data by symbol, Ensembl ID, or external database identifiers.

**Common operations:**
- Look up gene information by symbol (e.g., "BRCA2", "TP53")
- Retrieve transcript and protein information
- Get gene coordinates and chromosomal locations
- Access cross-references to external databases (UniProt, RefSeq, etc.)

**Using the ensembl_rest package:**
```python
from ensembl_rest import EnsemblClient

client = EnsemblClient()

# Look up gene by symbol
gene_data = client.symbol_lookup(
    species='human',
    symbol='BRCA2'
)

# Get detailed gene information
gene_info = client.lookup_id(
    id='ENSG00000139618',  # BRCA2 Ensembl ID
    expand=True
)
```

**Direct REST API (no package):**
```python
import requests

server = "https://rest.ensembl.org"

# Symbol lookup
response = requests.get(
    f"{server}/lookup/symbol/homo_sapiens/BRCA2",
    headers={"Content-Type": "application/json"}
)
gene_data = response.json()
```

### 2. Sequence Retrieval

Fetch genomic, transcript, or protein sequences in various formats (JSON, FASTA, plain text).

**Operations:**
- Get DNA sequences for genes or genomic regions
- Retrieve transcript sequences (cDNA)
- Access protein sequences
- Extract sequences with flanking regions or modifications

**Example:**
```python
# Using ensembl_rest package
sequence = client.sequence_id(
    id='ENSG00000139618'  # BRCA2 Ensembl ID
)
```