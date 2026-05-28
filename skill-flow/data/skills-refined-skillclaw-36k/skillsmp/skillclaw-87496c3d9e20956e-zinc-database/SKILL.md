---
name: zinc-database
description: Use this skill when you need to access ZINC, a repository of over 230 million purchasable compounds, for tasks such as virtual screening, lead discovery, and compound retrieval.
---

# ZINC Database

## Overview

ZINC is a freely accessible repository of over 230 million purchasable compounds maintained by UCSF. It allows users to search by ZINC ID or SMILES, perform similarity searches, download 3D-ready structures for docking, and discover analogs for virtual screening and drug discovery.

## When to Use This Skill

This skill should be used when:

- **Virtual screening**: Finding compounds for molecular docking studies.
- **Lead discovery**: Identifying commercially-available compounds for drug development.
- **Structure searches**: Performing similarity or analog searches by SMILES.
- **Compound retrieval**: Looking up molecules by ZINC IDs or supplier codes.
- **Chemical space exploration**: Exploring purchasable chemical diversity.
- **Docking studies**: Accessing 3D-ready molecular structures.
- **Analog searches**: Finding similar compounds based on structural similarity.
- **Supplier queries**: Identifying compounds from specific chemical vendors.
- **Random sampling**: Obtaining random compound sets for screening.

## Database Versions

ZINC has evolved through multiple versions:

- **ZINC22** (Current): The largest version with over 230 million purchasable compounds and multi-billion scale make-on-demand compounds.
- **ZINC20**: Still maintained, focused on lead-like and drug-like compounds.
- **ZINC15**: Predecessor version, legacy but still documented.

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