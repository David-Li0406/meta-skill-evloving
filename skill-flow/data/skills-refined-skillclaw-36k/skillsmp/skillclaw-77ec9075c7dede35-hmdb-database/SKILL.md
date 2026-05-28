---
name: hmdb-database
description: Use this skill when performing metabolomics research, clinical chemistry, biomarker discovery, or metabolite identification tasks.
---

# HMDB Database

## Overview

The Human Metabolome Database (HMDB) is a comprehensive, freely available resource containing detailed information about small molecule metabolites found in the human body.

## Database Contents

HMDB version 5.0 (current as of 2025) contains:

- **220,945 metabolite entries** covering both water-soluble and lipid-soluble compounds
- **8,610 protein sequences** for enzymes and transporters involved in metabolism
- **130+ data fields per metabolite** including:
  - Chemical properties (structure, formula, molecular weight, InChI, SMILES)
  - Clinical data (biomarker associations, diseases, normal/abnormal concentrations)
  - Biological information (pathways, reactions, locations)
  - Spectroscopic data (NMR, MS, MS-MS spectra)
  - External database links (KEGG, PubChem, MetaCyc, ChEBI, PDB, UniProt, GenBank)

## Core Capabilities

### 1. Web-Based Metabolite Searches

Access HMDB through the web interface at [https://www.hmdb.ca/](https://www.hmdb.ca/) for:

**Text Searches:**
- Search by metabolite name, synonym, or identifier (HMDB ID)
- Example HMDB IDs: HMDB0000001, HMDB0001234
- Search by disease associations or pathway involvement
- Query by biological specimen type (urine, serum, CSF, saliva, feces, sweat)

**Structure-Based Searches:**
- Use ChemQuery for structure and substructure searches
- Search by molecular weight or molecular weight range
- Use SMILES or InChI strings to find compounds

**Spectral Searches:**
- LC-MS spectral matching
- GC-MS spectral matching
- NMR spectral searches for metabolite identification

**Advanced Searches:**
- Combine multiple criteria (name, properties, concentration ranges)
- Filter by biological locations or specimen types
- Search by protein/enzyme associations