# KG-Microbe Regeneration Guide

> Generated: 2025-12-18

## Overview

To regenerate KG-Microbe transformations from scratch:

```bash
cd ~/gitrepos/kg-microbe
poetry run kg download    # Download raw data
poetry run kg transform   # Transform to KGX format
poetry run kg merge       # Merge transformed graphs
```

## Quick Start: Using Pre-processed Databases

**To avoid slow ontology processing (saves hours + 500GB RAM), download pre-built databases:**

```bash
cd ~/gitrepos/kg-microbe

# Option A: Download just ChEBI (3.7 GB) - for testing or madin_etal transform
wget 'https://drive.google.com/uc?export=download&id=1UlQW9oXu7f7Y3FTVCVvGc1lH-_we9ds6' -O data/raw/chebi.db

# Option B: Download full raw data tarball (includes both chebi.db and ncbitaxon.db)
wget https://portal.nersc.gov/project/m4689/KGMicrobe-raw-20250222.tar.gz
tar -xzf KGMicrobe-raw-20250222.tar.gz -C data/raw/

# Then run transform (skips ROBOT processing for ontologies with .db files)
poetry run kg transform -s madin_etal  # Or other sources
```

## Download Step

Downloads data from `download.yaml` into `data/raw/`:

**Key ontology files downloaded:**
- NCBITaxon: `ncbitaxon.owl.gz` (63 MB) → processes to `ncbitaxon.db` (11 GB SQLite)
- ChEBI: `chebi.owl.gz` (60 MB) → processes to `chebi.db` (3.5 GB SQLite)
- ENVO: `envo.json` (6.5 MB)
- GO: `go.json` (74 MB)
- METPO: `metpo.owl` (370 KB)
- EC: `ec.json` (54 MB)

**Data sources:**
- BacDive: `bacdive_strains.json` (748 MB) - from Google Drive
- MediaDive: Auto-downloads bulk data (~60-120k API calls, 30-60 min)
- BactoTraits: `BactoTraits_databaseV2_Jun2022.csv`
- Madin et al: `madin_etal.csv`

### MediaDive Special Handling

MediaDive download has two phases:
1. Basic media list: `mediadive.json`
2. Bulk details download (automatic): recipes, strains, solutions, compounds
   - Saved to `data/raw/mediadive/`
   - Cached to avoid repeated API calls during transform

## Transform Step

Transforms raw data into KGX format (nodes.tsv + edges.tsv) in `data/transformed/`:

**Current transformed sources:**
- `bacdive/` - 127M edges, 13M nodes
- `bactotraits/`
- `madin_etal/`

### Ontology Processing

**NCBITaxon** (slow - requires ROBOT):
1. Decompresses `ncbitaxon.owl.gz` → `ncbitaxon.owl`
2. Uses ROBOT to remove excluded branches (from `exclusion_branches.tsv`):
   - NCBITaxon:28384 (Vertebrata)
   - NCBITaxon:33090 (Plants)
   - NCBITaxon:33208 (Metazoa)
   - NCBITaxon:1407750
   - NCBITaxon:1145094
   - NCBITaxon:119167
   - NCBITaxon:590738
   - NCBITaxon:10239 (Viruses)
3. Converts to JSON: `ncbitaxon_removed_subset.json`
4. Transforms to KGX format

**Environment variables for ROBOT:**
```bash
export ROBOT_JAVA_ARGS="-Xmx12g -XX:+UseG1GC"  # Adjust memory as needed
```

## Pre-processed Files

**SQLite databases in `data/raw/`:**
- `ncbitaxon.db` (11 GB) - Pre-processed NCBITaxon
- `chebi.db` (3.5 GB) - Pre-processed ChEBI

**Status:** These appear to be created during transform/processing, NOT downloaded.

### Potential Workarounds for Slow Downloads

**Option 1: Download pre-processed SQLite databases from Google Drive (RECOMMENDED)**

Skip the slow ROBOT processing by downloading pre-built SQLite databases:

**ChEBI database (3.7 GB):**
```bash
# Download from Google Drive
https://drive.google.com/file/d/1UlQW9oXu7f7Y3FTVCVvGc1lH-_we9ds6/view?usp=drive_link

# Save to kg-microbe/data/raw/chebi.db
# Then skip the chebi transform step
```

**NCBITaxon database (11.8 GB):**
- Download from NERSC portal: https://portal.nersc.gov/project/m4689/KGMicrobe-raw-20250222.tar.gz
- This tarball (KGMicrobe-raw-20250222.tar.gz) contains ALL raw data including both .db files
- Extract to `data/raw/` to skip ontology processing

**Note:** These databases are maintained by the BBOP team and updated with KG-Microbe releases.

Sources:
- ChEBI link: Marcin Joachimiak (BerkeleyBOP Slack #kg-microbe-ml, 2025-10-30)
- Raw data tarball: Google Drive doc "KG-Microbe Data Products (NERSC, S3, GitHub)"

**Option 2: Use KG-Hub cached releases**

Latest KG-Microbe release: https://github.com/Knowledge-Graph-Hub/kg-microbe/releases/tag/2025-03-07

Download pre-transformed tarballs:
- Individual source tarballs (bacdive.tar.gz, etc.)
- kg-microbe-core.tar.gz
- kg-microbe-biomedical.tar.gz

Extract to `data/transformed/` to skip download+transform steps.

**Option 3: Copy existing files**

If you've already run the pipeline once:
- Copy `data/raw/*.db` files to avoid re-processing ontologies
- Copy `data/raw/mediadive/` to avoid MediaDive API calls
- Copy `data/transformed/` to skip entire transform step

## Memory Requirements

From README:
> The KG construction process, particularly the transform step involving trimming of NCBI Taxonomy for any KG and the steps involving the microbial UniProt dataset for KG-Microbe-Function and KG-Microbe-Biomedical-Function, is computationally intensive. Successful execution on a local machine may require significant memory resources (e.g., >500 GB of RAM).

**Notes:**
- NCBITaxon processing is memory-intensive
- ROBOT operations on large ontologies require substantial RAM
- Consider using NERSC or other HPC resources for full pipeline

## Output Locations

**Transformed data:**
```
data/transformed/
├── bacdive/
│   ├── edges.tsv (127M)
│   ├── nodes.tsv (13M)
│   └── bacdive_media_links.txt
├── bactotraits/
│   ├── edges.tsv
│   └── nodes.tsv
└── madin_etal/
    ├── edges.tsv
    └── nodes.tsv
```

**Merged data:**
```
data/merged/kg-microbe-core/
data/merged/kg-microbe-biomedical/
```

## Testing/Snippet Mode

For testing without full downloads:
```bash
poetry run kg download --snippet-only  # Downloads only first 5 KB of each source
```

## Makefile Targets

Additional useful targets:
```bash
make run-summary          # Show statistics on merged KG
make neo4j-upload         # Upload to Neo4j
```

## Edge Pattern Analysis

After transform, analyze edge patterns:
```bash
python ~/gitrepos/cmm-ai-automation/src/cmm_ai_automation/scripts/edge_patterns_by_source.py \
  ~/gitrepos/kg-microbe/data/transformed > edge_patterns.tsv
```

## Resolved Questions

- ✅ **Where do `ncbitaxon.db` and `chebi.db` come from?**
  - Created by semsql/OAK during transform step using ROBOT
  - Pre-built versions available on Google Drive (see Option 1 above)

- ✅ **Can we skip ROBOT processing?**
  - Yes! Download pre-built .db files from Google Drive
  - Saves hours of processing time and memory

## TODO: Investigate

- [x] Locate ncbitaxon.db - **Found:** Available in NERSC raw data tarball
- [x] Locate chebi.db - **Found:** Available on Google Drive and in NERSC tarball
- [ ] Document exact memory requirements per transform source
- [ ] Test if OBO Foundry provides public .db files at http://purl.obolibrary.org/obo/
- [ ] Verify Google Drive download link works (may require Google auth)
