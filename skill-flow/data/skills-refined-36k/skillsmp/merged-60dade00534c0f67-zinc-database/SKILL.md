---
name: zinc-database
description: Access ZINC (230M+ purchasable compounds). Search by ZINC ID/SMILES, perform similarity searches, and retrieve 3D-ready structures for docking, analog discovery, virtual screening, and drug discovery.
---

# ZINC Database

## Overview

ZINC is a freely accessible repository of 230M+ purchasable compounds maintained by UCSF. This skill allows you to search by ZINC ID or SMILES, perform similarity searches, download 3D-ready structures for docking, and discover analogs for virtual screening and drug discovery.

## When to Use This Skill

This skill should be used when:

- **Virtual screening**: Finding compounds for molecular docking studies
- **Lead discovery**: Identifying commercially-available compounds for drug development
- **Structure searches**: Performing similarity or analog searches by SMILES
- **Compound retrieval**: Looking up molecules by ZINC IDs or supplier codes
- **Chemical space exploration**: Exploring purchasable chemical diversity
- **Docking studies**: Accessing 3D-ready molecular structures
- **Analog searches**: Finding similar compounds based on structural similarity
- **Supplier queries**: Identifying compounds from specific chemical vendors
- **Random sampling**: Obtaining random compound sets for screening

## Database Versions

ZINC has evolved through multiple versions:

- **ZINC22** (Current): Largest version with 230+ million purchasable compounds and multi-billion scale make-on-demand compounds
- **ZINC20**: Still maintained, focused on lead-like and drug-like compounds
- **ZINC15**: Predecessor version, legacy but still documented

This skill primarily focuses on ZINC22, the most current and comprehensive version.

## Access Methods

### Web Interface

Primary access point: [ZINC Web Interface](https://zinc.docking.org/)  
Interactive searching: [CartBlanche22](https://cartblanche22.docking.org/)

### API Access

All ZINC22 searches can be performed programmatically via the CartBlanche22 API:

**Base URL**: `https://cartblanche22.docking.org/`

All API endpoints return data in text or JSON format with customizable fields.

## Core Capabilities

### 1. Search by ZINC ID

Retrieve specific compounds using their ZINC identifiers.

**Web interface**: [Search by ZINC ID](https://cartblanche22.docking.org/search/zincid)

**API endpoint**:
```bash
curl "https://cartblanche22.docking.org/[email protected]_fields=smiles,zinc_id"
```

**Multiple IDs**:
```bash
curl "https://cartblanche22.docking.org/substances.txt:zinc_id=ZINC000000000001,ZINC000000000002&output_fields=smiles,zinc_id,tranche"
```

### 2. Search by SMILES

Find compounds by chemical structure using SMILES notation, with optional distance parameters for analog searching.

**Web interface**: [Search by SMILES](https://cartblanche22.docking.org/search/smiles)

**API endpoint**:
```bash
curl "https://cartblanche22.docking.org/[email protected]=4-Fadist=4"
```

### 3. Search by Supplier Codes

Query compounds from specific chemical suppliers or retrieve all molecules from particular catalogs.

**Web interface**: [Search by Supplier Codes](https://cartblanche22.docking.org/search/catitems)

**API endpoint**:
```bash
curl "https://cartblanche22.docking.org/catitems.txt:catitem_id=SUPPLIER-CODE-123"
```

### 4. Random Compound Sampling

Generate random compound sets for screening or benchmarking purposes.

**Web interface**: [Random Compound Sampling](https://cartblanche22.docking.org/search/random)

**API endpoint**:
```bash
curl "https://cartblanche22.docking.org/substance/random.txt:count=100"
```

## Common Workflows

### Workflow 1: Preparing a Docking Library

1. **Define search criteria** based on target properties or desired chemical space.
2. **Query ZINC22** using the appropriate search method:
   ```bash
   curl "https://cartblanche22.docking.org/substance/random.txt:count=10000&subset=drug-like&output_fields=zinc_id,smiles,tranche" > docking_library.txt
   ```
3. **Parse results** to extract ZINC IDs and SMILES.
4. **Download 3D structures** for docking using ZINC ID or download from file repositories.

### Workflow 2: Finding Analogs of a Hit Compound

1. **Obtain SMILES** of the hit compound.
2. **Perform similarity search** with distance threshold:
   ```bash
   curl "https://cartblanche22.docking.org/smiles.txt:smiles=CC(C)Cc1ccc(cc1)C(C)C(=O)O&dist=5&output_fields=zinc_id,smiles,catalogs" > analogs.txt
   ```
3. **Analyze results** to identify purchasable analogs.
4. **Retrieve 3D structures** for the most promising analogs.

### Workflow 3: Batch Compound Retrieval

1. **Compile list of ZINC IDs** from literature, databases, or previous screens.
2. **Query ZINC22 API**:
   ```bash
   curl "https://cartblanche22.docking.org/substances.txt:zinc_id=ZINC000000000001,ZINC000000000002&output_fields=zinc_id,smiles,supplier_code,catalogs"
   ```
3. **Process results** for downstream analysis or purchasing.

### Workflow 4: Chemical Space Sampling

1. **Select subset parameters** based on screening goals.
2. **Generate random sample**:
   ```bash
   curl "https://cartblanche22.docking.org/substance/random.txt:count=5000&subset=lead-like&output_fields=zinc_id,smiles,tranche" > chemical_space_sample.txt
   ```
3. **Analyze chemical diversity** and prepare for virtual screening.

## Output Fields

Customize API responses with the `output_fields` parameter:

**Available fields**:
- `zinc_id`: ZINC identifier
- `smiles`: SMILES string representation
- `sub_id`: Internal substance ID
- `supplier_code`: Vendor catalog number
- `catalogs`: List of suppliers offering the compound
- `tranche`: Encoded molecular properties (H-count, LogP, MW, reactivity phase)

## Tranche System

ZINC organizes compounds into "tranches" based on molecular properties:

**Format**: `H##P###M###-phase`

Use tranche data to filter compounds by drug-likeness criteria.

## Downloading 3D Structures

For molecular docking, 3D structures are available via file repositories:

**File repository**: [ZINC File Repository](https://files.docking.org/zinc22/)

Structures are organized by tranches and available in multiple formats.

## Python Integration

### Using curl with Python

```python
import subprocess

def query_zinc_by_id(zinc_id, output_fields="zinc_id,smiles,catalogs"):
    """Query ZINC22 by ZINC ID."""
    url = f"https://cartblanche22.docking.org/[email protected]_id={zinc_id}&output_fields={output_fields}"
    result = subprocess.run(['curl', url], capture_output=True, text=True)
    return result.stdout
```

## Best Practices

### Query Optimization

- **Start specific**: Begin with exact searches before expanding to similarity searches.
- **Limit output fields**: Request only necessary fields to reduce data transfer.

### Data Quality

- **Verify availability**: Supplier catalogs change; confirm compound availability before large orders.

## Important Disclaimers

### Data Reliability

ZINC explicitly states: **"We do not guarantee the quality of any molecule for any purpose and take no responsibility for errors arising from the use of this database."**

### Appropriate Use

- ZINC is intended for academic and research purposes in drug discovery.

## Additional Resources

- **ZINC Website**: [ZINC Website](https://zinc.docking.org/)
- **ZINC Wiki**: [ZINC Wiki](https://wiki.docking.org/)