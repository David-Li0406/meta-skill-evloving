---
name: pubchem-database
description: Use this skill when you need to query the PubChem database for chemical compounds, retrieve their properties, or perform similarity and substructure searches.
---

# Skill body

## Overview

PubChem is the world's largest freely available chemical database with over 110 million compounds and 270 million bioactivities. This skill allows you to query chemical structures by name, CID, or SMILES, retrieve molecular properties, perform similarity and substructure searches, and access bioactivity data using the PUG-REST API and PubChemPy.

## When to Use This Skill

Use this skill when:
- Searching for chemical compounds by name, structure (SMILES/InChI), or molecular formula.
- Retrieving molecular properties (e.g., molecular weight, LogP, TPSA).
- Performing similarity searches to find structurally related compounds.
- Conducting substructure searches for specific chemical motifs.
- Accessing bioactivity data from screening assays.
- Converting between chemical identifier formats (CID, SMILES, InChI).
- Batch processing multiple compounds for drug-likeness screening or property analysis.

## Core Capabilities

### 1. Chemical Structure Search

Search for compounds using multiple identifier types:

**By Chemical Name**:
```python
import pubchempy as pcp
compounds = pcp.get_compounds('aspirin', 'name')
compound = compounds[0]
```

**By CID (Compound ID)**:
```python
compound = pcp.Compound.from_cid(2244)  # Aspirin
```

**By SMILES**:
```python
compound = pcp.get_compounds('CC(=O)OC1=CC=CC=C1C(=O)O', 'smiles')[0]
```

**By InChI**:
```python
compound = pcp.get_compounds('InChI=1S/C9H8O4/...', 'inchi')[0]
```

**By Molecular Formula**:
```python
compounds = pcp.get_compounds('C9H8O4', 'formula')
# Returns all compounds matching this formula
```

### 2. Property Retrieval

Retrieve molecular properties for compounds using either high-level or low-level approaches:

**Using PubChemPy (Recommended)**:
```python
import pubchempy as pcp

# Get compound object with all properties
compound = pcp.get_compounds('caffeine', 'name')[0]

# Access individual properties
molecular_formula = compound.molecular_formula
molecular_weight = compound.molecular_weight
iupac_name = compound.iupac_name
smiles = compound.canonical_smiles
inchi = compound.inchi
xlogp = compound.xlogp  # Partition coefficient
tpsa = compound.tpsa    # Topological polar surface area
```

**Get Specific Properties**:
```python
# Request only specific properties
properties = pcp.get_properties(['MolecularWeight', 'XLogP'], [compound.cid])
```