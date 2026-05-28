---
name: string-database
description: Use this skill when you need to query the STRING API for protein-protein interactions, perform functional enrichment analysis, or discover interaction partners across various species.
---

# STRING Database

## Overview

STRING is a comprehensive database of known and predicted protein-protein interactions covering 59M proteins and over 20B interactions across 5000+ organisms. It allows users to query interaction networks, perform functional enrichment, and discover partners via a REST API for systems biology and pathway analysis.

## When to Use This Skill

This skill should be used when:
- Retrieving protein-protein interaction networks for single or multiple proteins.
- Performing functional enrichment analysis (GO, KEGG, Pfam) on protein lists.
- Discovering interaction partners and expanding protein networks.
- Testing if proteins form significantly enriched functional modules.
- Generating network visualizations with evidence-based coloring.
- Analyzing homology and protein family relationships.
- Conducting cross-species protein interaction comparisons.
- Identifying hub proteins and network connectivity patterns.

## Quick Start

The skill provides:
1. Python helper functions for all STRING REST API operations.
2. Comprehensive reference documentation with detailed API specifications.

When users request STRING data, determine which operation is needed and use the appropriate function.

## Core Operations

### 1. Identifier Mapping (`string_map_ids`)

Convert gene names, protein names, and external IDs to STRING identifiers.

**When to use**: Starting any STRING analysis, validating protein names, finding canonical identifiers.

**Usage**:
```python
from string_api import string_map_ids

# Map single protein
result = string_map_ids('TP53', species=9606)

# Map multiple proteins
result = string_map_ids(['TP53', 'BRCA1', 'EGFR', 'MDM2'], species=9606)

# Map with multiple matches per query
result = string_map_ids('p53', species=9606, limit=5)
```

**Parameters**:
- `species`: NCBI taxon ID (9606 = human, 10090 = mouse, 7227 = fly).
- `limit`: Number of matches per identifier (default: 1).
- `echo_query`: Include query term in output (default: 1).

**Best practice**: Always map identifiers first for faster subsequent queries.

### 2. Network Retrieval (`string_network`)

Get protein-protein interaction network data in tabular format.

**When to use**: Building interaction networks for analysis.

**Usage**:
```python
from string_api import string_network

# Retrieve network for a single protein
network = string_network('TP53', species=9606)

# Retrieve network for multiple proteins
network = string_network(['TP53', 'BRCA1'], species=9606)
```

**Parameters**:
- `species`: NCBI taxon ID.
- `format`: Desired output format (e.g., 'tsv', 'json').

This skill provides a powerful tool for bioinformatics research and systems biology applications.