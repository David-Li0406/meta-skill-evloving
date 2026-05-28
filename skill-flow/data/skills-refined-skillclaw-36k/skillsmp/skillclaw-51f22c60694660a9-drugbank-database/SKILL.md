---
name: drugbank-database
description: Use this skill when you need to access and analyze comprehensive drug information from the DrugBank database for pharmaceutical research, drug discovery, or pharmacology studies.
---

# DrugBank Database

## Overview

DrugBank is a comprehensive bioinformatics and cheminformatics database containing detailed information on drugs and drug targets. This skill enables programmatic access to DrugBank data, including approximately 9,591 drug entries (2,037 FDA-approved small molecules, 241 biotech drugs, 96 nutraceuticals, and over 6,000 experimental compounds) with 200+ data fields per entry.

## Core Capabilities

### 1. Data Access and Authentication

Download and access DrugBank data using Python with proper authentication. The skill provides guidance on:

- Installing and configuring the `drugbank-downloader` package
- Managing credentials securely via environment variables or config files
- Downloading specific or latest database versions
- Opening and parsing XML data efficiently
- Working with cached data to optimize performance

**When to use**: Setting up DrugBank access, downloading database updates, initial project configuration.

### 2. Drug Information Queries

Extract comprehensive drug information from the database, including identifiers, chemical properties, pharmacology, clinical data, and cross-references to external databases.

**Query capabilities**:
- Search by DrugBank ID, name, CAS number, or keywords
- Extract basic drug information (name, type, description, indication)
- Retrieve chemical properties (SMILES, InChI, molecular formula)
- Get pharmacology data (mechanism of action, pharmacodynamics, ADME)
- Access external identifiers (PubChem, ChEMBL, UniProt, KEGG)
- Build searchable drug datasets and export to DataFrames
- Filter drugs by type (small molecule, biotech, nutraceutical)

**When to use**: Retrieving specific drug information, building drug databases, pharmacology research, literature review, drug profiling.