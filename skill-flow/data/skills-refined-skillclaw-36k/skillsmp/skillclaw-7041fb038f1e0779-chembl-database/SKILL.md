---
name: chembl-database
description: Use this skill when you need to query ChEMBL's bioactive molecules and drug discovery data, including searching for compounds, retrieving bioactivity data, and exploring target-ligand relationships.
---

# ChEMBL Database

## Overview

ChEMBL is a manually curated database of bioactive molecules maintained by the European Bioinformatics Institute (EBI), containing over 2 million compounds, 19 million bioactivity measurements, 13,000+ drug targets, and data on approved drugs and clinical candidates. Access and query this data programmatically using the ChEMBL Python client for drug discovery and medicinal chemistry research.

## When to Use This Skill

This skill should be used when:

- **Compound searches**: Finding molecules by name, structure, or properties.
- **Target information**: Retrieving data about proteins, enzymes, or biological targets.
- **Bioactivity data**: Querying IC50, Ki, EC50, or other activity measurements.
- **Drug information**: Looking up approved drugs, mechanisms, or indications.
- **Structure searches**: Performing similarity or substructure searches.
- **Cheminformatics**: Analyzing molecular properties and drug-likeness.
- **Target-ligand relationships**: Exploring compound-target interactions.
- **Drug discovery**: Identifying inhibitors, agonists, or bioactive molecules.

## Installation and Setup

### Python Client

The ChEMBL Python client is required for programmatic access:

```bash
pip install chembl_webresource_client
```

### Basic Usage Pattern

```python
from chembl_webresource_client.new_client import new_client

# Access different endpoints
molecule = new_client.molecule
target = new_client.target
activity = new_client.activity
drug = new_client.drug
```

## Core Capabilities

### 1. Molecule Queries

**Retrieve by ChEMBL ID:**
```python
molecule = new_client.molecule
aspirin = molecule.get('CHEMBL25')
```

**Search by name:**
```python
results = molecule.filter(pref_name__icontains='aspirin')
```

**Filter by properties:**
```python
# Find small molecules (MW <= 500) with favorable LogP
results = molecule.filter(
    molecule_properties__mw_freebase__lte=500,
    molecule_properties__alogp__lte=5
)
```

### 2. Target Queries

**Retrieve target information:**
```python
target = new_client.target
egfr = target.get('CHEMBL203')
```

**Search for specific target types:**
```python
# Find all kinase targets
kinases = target.filter(target_type='SINGLE PROTEIN')
```