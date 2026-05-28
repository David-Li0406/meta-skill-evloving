---
name: metabolomics-workbench-database
description: Use this skill when you need to access the NIH Metabolomics Workbench via REST API to query metabolites, study metadata, and perform biomarker discovery.
---

# Skill body

## Overview

The Metabolomics Workbench is a comprehensive NIH Common Fund-sponsored platform hosted at UCSD that serves as the primary repository for metabolomics research data. It provides programmatic access to over 4,200 processed studies (3,790+ publicly available), standardized metabolite nomenclature through RefMet, and powerful search capabilities across multiple analytical platforms (GC-MS, LC-MS, NMR).

## Core Capabilities

### 1. Querying Metabolite Structures and Data

Access comprehensive metabolite information including structures, identifiers, and cross-references to external databases.

**Key operations:**
- Retrieve compound data by various identifiers (PubChem CID, InChI Key, KEGG ID, HMDB ID, etc.)
- Download molecular structures as MOL files or PNG images
- Access standardized compound classifications
- Cross-reference between different metabolite databases

**Example queries:**
```python
import requests

# Get compound information by PubChem CID
response = requests.get('https://www.metabolomicsworkbench.org/rest/compound/pubchem_cid/5281365/all/json')

# Download molecular structure as PNG
response = requests.get('https://www.metabolomicsworkbench.org/rest/compound/regno/11/png')

# Get compound name by registry number
response = requests.get('https://www.metabolomicsworkbench.org/rest/compound/regno/11/name/json')
```

### 2. Accessing Study Metadata and Experimental Results

Query metabolomics studies by various criteria and retrieve complete experimental datasets.

**Key operations:**
- Search studies by metabolite, institute, investigator, or title
- Access study summaries, experimental factors, and analysis details
- Retrieve complete experimental data in various formats
- Download mwTab format files for complete study information
- Query untargeted metabolomics data

**Example queries:**
```python
# List all available public studies
response = requests.get('https://www.metabolomicsworkbench.org/rest/study/all/json')
```