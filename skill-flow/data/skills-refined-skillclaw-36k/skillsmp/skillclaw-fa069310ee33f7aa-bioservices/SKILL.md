---
name: bioservices
description: Use this skill when you need to access and analyze biological data from multiple bioinformatics databases in a unified workflow.
---

# BioServices

## Overview

BioServices is a Python package providing programmatic access to approximately 40 bioinformatics web services and databases. It allows you to retrieve biological data, perform cross-database queries, map identifiers, analyze sequences, and integrate multiple biological resources in Python workflows. The package handles both REST and SOAP/WSDL protocols transparently.

## When to Use This Skill

This skill should be used when:
- Retrieving protein sequences, annotations, or structures from databases like UniProt, PDB, and Pfam.
- Analyzing metabolic pathways and gene functions via KEGG or Reactome.
- Searching compound databases (ChEBI, ChEMBL, PubChem) for chemical information.
- Converting identifiers between different biological databases (e.g., KEGG↔UniProt).
- Running sequence similarity searches (e.g., BLAST, MUSCLE alignment).
- Querying gene ontology terms (QuickGO, GO annotations).
- Accessing protein-protein interaction data (PSICQUIC, IntactComplex).
- Mining genomic data (BioMart, ArrayExpress, ENA).
- Integrating data from multiple bioinformatics resources in a single workflow.

## Core Capabilities

### 1. Protein Analysis

Retrieve protein information, sequences, and functional annotations:

```python
from bioservices import UniProt

u = UniProt(verbose=False)

# Search for protein by name
results = u.search("ZAP70_HUMAN", frmt="tab", columns="id,genes,organism")

# Retrieve FASTA sequence
sequence = u.retrieve("P43403", "fasta")

# Map identifiers between databases
kegg_ids = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query="P43403")
```

**Key methods:**
- `search()`: Query UniProt with flexible search terms.
- `retrieve()`: Get protein entries in various formats (FASTA, XML, tab).
- `mapping()`: Convert identifiers between databases.

### 2. Pathway Discovery and Analysis

Access KEGG pathway information for genes and organisms:

```python
from bioservices import KEGG

k = KEGG()
k.organism = "hsa"  # Set to human

# Search for organisms
k.lookfor_organism("droso")  # Find Drosophila species

# Find pathways by name
k.lookfor_pathway("B cell")  # Retrieve pathways related to B cells
```

**Key methods:**
- `lookfor_organism()`: Search for organisms in KEGG.
- `lookfor_pathway()`: Retrieve pathways by name.

## Additional Information

For more details on the API and its capabilities, refer to the official documentation.