---
name: kegg-database
description: Use this skill when querying pathways, genes, compounds, enzymes, diseases, and drugs across multiple organisms using KEGG's REST API.
---

# KEGG Database

## Overview

KEGG (Kyoto Encyclopedia of Genes and Genomes) is a comprehensive bioinformatics resource for biological pathway analysis and molecular interaction networks. The KEGG API is available only for academic use.

## Quick Start

The skill provides Python helper functions for all KEGG REST API operations. When users request KEGG data, determine which operation is needed and use the appropriate function.

## Core Operations

### 1. Database Information (`kegg_info`)

Retrieve metadata and statistics about KEGG databases.

**When to use**: Understanding database structure, checking available data, getting release information.

**Usage**:
```python
from kegg_api import kegg_info

# Get pathway database info
info = kegg_info('pathway')

# Get organism-specific info
hsa_info = kegg_info('hsa')  # Human genome
```

**Common databases**: `kegg`, `pathway`, `module`, `brite`, `genes`, `genome`, `compound`, `glycan`, `reaction`, `enzyme`, `disease`, `drug`

### 2. Listing Entries (`kegg_list`)

List entry identifiers and names from KEGG databases.

**When to use**: Getting all pathways for an organism, listing genes, retrieving compound catalogs.

**Usage**:
```python
from kegg_api import kegg_list

# List all reference pathways
pathways = kegg_list('pathway')

# List human-specific pathways
hsa_pathways = kegg_list('pathway', 'hsa')

# List specific genes (max 10)
genes = kegg_list('hsa:10458+hsa:10459')
```

**Common organism codes**: `hsa` (human), `mmu` (mouse), `dme` (fruit fly), `sce` (yeast), `eco` (E. coli)

### 3. Searching (`kegg_find`)

Search KEGG databases by keywords or molecular properties.

**When to use**: Finding genes by name/description, searching compounds by formula or mass, discovering entries by keywords.

**Usage**:
```python
from kegg_api import kegg_find

# Example search
results = kegg_find('gene_name')
```