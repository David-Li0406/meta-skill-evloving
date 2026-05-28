# BacDive MongoDB

This document describes how BacDive strain data is loaded, stored, and used in this project.

## Overview

BacDive (Bacterial Diversity Metadatabase) provides comprehensive strain-level data for bacteria and archaea. We maintain a local MongoDB copy to enable fast lookups during strain enrichment without repeated API calls.

## MongoDB Structure

- **Database**: `bacdive` (default, configurable)
- **Collection**: `strains` (default, configurable)
- **Document count**: ~100k strains
- **ID range**: 1 to ~180,000 (sparse, ~56% density)

## Justfile Variables

All BacDive targets use these configurable variables (defined in `project.justfile`):

| Variable | Default | Description |
|----------|---------|-------------|
| `bacdive_max_id` | `200000` | Maximum BacDive ID to fetch |
| `bacdive_min_id` | `1` | Minimum BacDive ID to fetch |
| `bacdive_database` | `bacdive` | MongoDB database name |
| `bacdive_collection` | `strains` | MongoDB collection name |

Override variables by placing them before the target:
```bash
just bacdive_database=test bacdive_collection=test load-bacdive
```

## Justfile Targets

All BacDive-related targets are in `project.justfile`:

| Target | Description |
|--------|-------------|
| `load-bacdive` | Populate MongoDB from BacDive API (iterates ID range 1-200000) |
| `kgx-export-bacdive` | Export MongoDB strains to KGX JSON Lines format |
| `strains-kgx-from-curies` | Enrich strain CURIEs using MongoDB lookups |
| `mediadive-merge-bacdive-ids` | Merge bacdive_id from MediaDive into strains |

All targets that read from BacDive MongoDB respect the `bacdive_database` and `bacdive_collection` variables.

### Loading BacDive Data

```bash
# Full load (IDs 1-200000, takes several hours)
just load-bacdive

# Test with subset
just bacdive_max_id=300 load-bacdive

# Custom database/collection
just bacdive_max_id=300 bacdive_database=bdtemp bacdive_collection=bdtemp load-bacdive

# Incremental update (new IDs only)
just bacdive_min_id=176393 load-bacdive
```

### Exporting/Using BacDive Data

```bash
# Export from default database
just kgx-export-bacdive

# Export from custom database
just bacdive_database=bdtemp bacdive_collection=bdtemp kgx-export-bacdive

# Enrich strains from custom database
just bacdive_database=bdtemp strains-kgx-from-curies
```

**Requirements:**
- MongoDB running locally
- `BACDIVE_EMAIL` and `BACDIVE_PASSWORD` in `.env` (register at https://bacdive.dsmz.de/)

## Python Scripts

### Scripts with Justfile Targets

| Script | Target | Purpose |
|--------|--------|---------|
| `load_bacdive_mongodb.py` | `load-bacdive` | Fetch from BacDive API and store in MongoDB |
| `export_bacdive_kgx.py` | `kgx-export-bacdive` | Export strains to KGX JSON Lines |
| `strains_kgx_from_curies.py` | `strains-kgx-from-curies` | Enrich strain CURIEs with BacDive/NCBI data |

### Orphaned Scripts (No Justfile Target)

These scripts exist but have no corresponding justfile target:

| Script | Purpose | Status |
|--------|---------|--------|
| `export_growth_kgx.py` | Export growth data to KGX | May be superseded by other exports |
| `index_bacdive_chromadb.py` | Build ChromaDB embeddings from BacDive | Experimental |
| `index_bacdive_media_compositions.py` | Index media compositions | Experimental |
| `test_culture_collection_search.py` | Ad-hoc test for culture collection lookups | Should move to tests/ |
| `test_species_search_with_synonyms.py` | Ad-hoc test for species synonym search | Should move to tests/ |

## Library Module

The `src/cmm_ai_automation/strains/bacdive.py` module provides functions for:

- `get_bacdive_collection(database=None, collection=None)` - Get MongoDB collection handle (parameterized)
- `lookup_bacdive_by_dsm()` - Find strain by DSM number
- `lookup_bacdive_by_ncbi_taxon()` - Find strain by NCBITaxon ID
- `lookup_bacdive_by_species()` - Find strain by species name
- `search_species_with_synonyms()` - Search including taxonomic synonyms
- `lookup_bacdive_by_culture_collection()` - Find by any culture collection ID
- `enrich_strain_from_bacdive()` - Enrich a StrainRecord with BacDive data

All scripts can be run with `--database` and `--collection` options to override the defaults.

## MongoDB Indexes

The loader creates these indexes for efficient lookups:

- `bacdive_id`
- `General.species`
- `Name and taxonomic classification.species`
- `General.DSM-Number`

## Data Flow

```
BacDive API
    │
    ▼ (just load-bacdive)
MongoDB bacdive.strains
    │
    ├──▶ strains_kgx_from_curies.py ──▶ output/kgx/strains_from_curies/
    │
    └──▶ export_bacdive_kgx.py ──▶ output/kgx/cmm_strains_bacdive_*.jsonl
```
