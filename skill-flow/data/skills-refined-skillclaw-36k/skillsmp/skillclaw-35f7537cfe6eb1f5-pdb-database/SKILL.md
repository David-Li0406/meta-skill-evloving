---
name: pdb-database
description: Use this skill when you need to access the RCSB PDB for 3D protein or nucleic acid structures, allowing you to search, download, and retrieve metadata for structural biology and drug discovery.
---

# PDB Database

## Overview

RCSB PDB is the worldwide repository for 3D structural data of biological macromolecules. You can search for structures, retrieve coordinates and metadata, and perform sequence and structure similarity searches across over 200,000 experimentally determined structures and computed models.

## When to Use This Skill

This skill should be used when:
- Searching for protein or nucleic acid 3D structures by text, sequence, or structural similarity.
- Downloading coordinate files in PDB, mmCIF, or BinaryCIF formats.
- Retrieving structural metadata, experimental methods, or quality metrics.
- Performing batch operations across multiple structures.
- Integrating PDB data into computational workflows for drug discovery, protein engineering, or structural biology research.

## Core Capabilities

### 1. Searching for Structures

Find PDB entries using various search criteria:

**Text Search:** Search by protein name, keywords, or descriptions.
```python
from rcsbapi.search import TextQuery
query = TextQuery("hemoglobin")
results = list(query())
print(f"Found {len(results)} structures")
```

**Attribute Search:** Query specific properties (organism, resolution, method, etc.).
```python
from rcsbapi.search import AttributeQuery
from rcsbapi.search.attrs import rcsb_entity_source_organism

# Find human protein structures
query = AttributeQuery(
    attribute=rcsb_entity_source_organism.scientific_name,
    operator="exact_match",
    value="Homo sapiens"
)
results = list(query())
```

**Sequence Similarity:** Find structures similar to a given sequence.
```python
from rcsbapi.search import SequenceQuery

query = SequenceQuery(
    value="MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAGQEEYSAMRDQYMRTGEGFLCVFAINNTKSFEDIHHYREQIKRVKDSEDVPMVLVGNKCDLPSRTVDTKQAQDLARSYGIPFIETSAKTRQGVDDAFYTLVREIRKHKEKMSKDGKKKKKKSKTKCVIM",
    evalue_cutoff=0.1,
    identity_cutoff=0.9
)
results = list(query())
```

**Structure Similarity:** Find structures with similar 3D geometry.
```python
from rcsbapi.search import StructSimilarityQuery

query = StructSimilarityQuery(
    structure_search_type="entry",
    entry_id="4HHB"  # Hemoglobin
)
results = list(query())
```

**Combining Queries:** Use logical operators to build complex searches.
```python
# Example of combining queries (not fully detailed in the evidence)
```