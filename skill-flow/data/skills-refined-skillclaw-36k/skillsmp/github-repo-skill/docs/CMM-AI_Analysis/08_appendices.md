# Chapter 8: Appendices

[<- Back to Index](00_index.md) | [Previous: Recommendations](07_recommendations.md)

---

## Appendix A: File Inventory

### Original Excel File

```
data/sheet/BER CMM Data for AI.xlsx (254 KB, Dec 4 2025)
```

### Converted TSV Files (from Google Sheet)

```
data/txt/sheet/
+-- BER_CMM_Data_for_AI_assays.tsv              (5 KB)
+-- BER_CMM_Data_for_AI_bioprocesses.tsv        (2 KB)
+-- BER_CMM_Data_for_AI_biosamples.tsv          (12 KB)
+-- BER_CMM_Data_for_AI_chemicals.tsv           (15 KB)
+-- BER_CMM_Data_for_AI_datasets.tsv            (4 KB)
+-- BER_CMM_Data_for_AI_genes_and_proteins.tsv  (73 KB)
+-- BER_CMM_Data_for_AI_growth_media.tsv        (3 KB)
+-- BER_CMM_Data_for_AI_macromolecular_structures.tsv (3 KB)
+-- BER_CMM_Data_for_AI_media_ingredients.tsv   (12 KB)
+-- BER_CMM_Data_for_AI_pathways.tsv            (15 KB)
+-- BER_CMM_Data_for_AI_protocols.tsv           (7 KB)
+-- BER_CMM_Data_for_AI_publications.tsv        (26 KB)
+-- BER_CMM_Data_for_AI_screening_results.tsv   (1 KB)
+-- BER_CMM_Data_for_AI_strains.tsv             (13 KB)
+-- BER_CMM_Data_for_AI_taxa_and_genomes.tsv    (60 KB)
+-- BER_CMM_Data_for_AI_transcriptomics.tsv     (10 KB)
```

### Extended TSV Files (from Python scripts)

```
data/txt/sheet/extended/
+-- BER_CMM_Data_for_AI_assays_extended.tsv              (7 KB)
+-- BER_CMM_Data_for_AI_bioprocesses_extended.tsv        (4 KB)
+-- BER_CMM_Data_for_AI_biosamples_extended.tsv          (8 KB)
+-- BER_CMM_Data_for_AI_chemicals_extended.tsv           (15 KB)
+-- BER_CMM_Data_for_AI_datasets_extended.tsv            (3 KB)
+-- BER_CMM_Data_for_AI_genes_and_proteins_extended.tsv  (72 KB)
+-- BER_CMM_Data_for_AI_growth_media_extended.tsv        (2 KB)
+-- BER_CMM_Data_for_AI_macromolecular_structures_extended.tsv (2 KB)
+-- BER_CMM_Data_for_AI_media_ingredients_extended.tsv   (9 KB)
+-- BER_CMM_Data_for_AI_pathways_extended.tsv            (13 KB)
+-- BER_CMM_Data_for_AI_protocols_extended.tsv           (2 KB)
+-- BER_CMM_Data_for_AI_publications_extended.tsv        (21 KB)
+-- BER_CMM_Data_for_AI_screening_results_extended.tsv   (1 KB)
+-- BER_CMM_Data_for_AI_strains_extended.tsv             (13 KB)
+-- BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv    (61 KB)
+-- BER_CMM_Data_for_AI_transcriptomics_extended.tsv     (10 KB)
```

---

## Appendix B: Key File Locations

### Python Scripts for Media

- `src/media_search.py` - Contains `CURATED_MEDIA` dict and KG queries
- `src/extend_media.py` - Wrapper script that calls media_search

### Conversion Scripts

- `src/convert_sheets.py` - XLSX -> TSV conversion
- `src/parsers.py` - General file parsing utilities

### Configuration

- `Makefile` - Pipeline automation (974 lines)
- `CLAUDE.md` - AI assistant guidance (29 KB)
- `.mcp.json` - Google Drive MCP server config

### Schema

- `schema/lanthanide_bioprocessing.yaml` - LinkML schema
- `src/linkml_models.py` - Generated Python models (auto-generated)

---

## Appendix C: Data Creation Methods

### Method 1: Manual Entry in Google Sheets

**Who:** Experimental collaborators
**What:** Typing or pasting data directly
**When:** Unknown (no changelog)
**Tracking:** None

### Method 2: XLSX Download and Conversion

**Who:** Marcin
**What:** Download Google Sheet as XLSX, commit to repo
**Command:** `make convert-excel`
**Script:** `src/convert_sheets.py`
**Output:** `data/txt/sheet/*.tsv` (overwrites previous)

### Method 3: Python Extend Scripts (Deterministic)

**Commands:**
```bash
make update-media      # -> extend_media.py -> media_search.py
make update-genomes    # -> extend_lanthanide_data.py -> ncbi_search.py
make update-pathways   # -> extend_pathways.py -> pathway_search.py
make update-genes      # -> extend_genes.py -> gene_search.py
make update-structures # -> extend_structures.py -> structure_search.py
make update-publications # -> extend_publications.py -> publication_search.py
make update-datasets   # -> extend_datasets.py -> dataset_search.py
```

**Output:** `data/txt/sheet/extended/*_extended.tsv`

### Method 4: Hardcoded Data in Python

**Example:** `src/media_search.py` lines 135-274

```python
CURATED_MEDIA = {
    "ATCC:1306": {
        "media_name": "ATCC Medium 1306 (Methanol mineral salts)",
        "ingredients": [
            {"name": "Methanol", "formula": "CH3OH", "chebi": "CHEBI:17790"},
            ...
        ]
    },
    # 7 media hardcoded here
}
```

This is **not data entry** - it's code. Changes require editing Python files.

### Method 5: KG-Microbe Queries

**Script:** `src/media_search.py` functions:
- `query_kg_microbe_for_ingredient()` - lines 24-85
- `query_kg_microbe_for_medium()` - lines 88-131

**Database:** `data/kgm/kg-microbe.duckdb`
**Note:** Contains SQL injection vulnerability (f-string interpolation)

### Method 6: LLM-Generated Content (Suspected)

**Evidence:** Some descriptions appear LLM-generated (verbose, structured)
**Example:** MP medium description in Google Sheet
**Tracking:** None - no way to distinguish from manual entry

---

## Appendix D: Proposed Prefix Registry

### Recommendation: Create a Prefix Registry Sheet

A new TSV file (`BER_CMM_Data_for_AI_prefixes.tsv`) should define all prefixes used in the data:

### Proposed Schema

| Column | Description |
|--------|-------------|
| `prefix_id` | Short prefix string (e.g., `CHEBI`, `ingredient`) |
| `prefix_name` | Human-readable name |
| `uri_pattern` | URI expansion pattern (if resolvable) |
| `example_id` | Example local ID |
| `example_uri` | Resolved example URI |
| `resolver` | Where to resolve (bioregistry.io, direct URL, internal DB) |
| `source` | Authority (OBO, DSMZ, LBL internal, etc.) |
| `notes` | Usage notes |

### Proposed Content

| prefix_id | prefix_name | uri_pattern | example_id | resolver | source |
|-----------|-------------|-------------|------------|----------|--------|
| CHEBI | ChEBI | http://purl.obolibrary.org/obo/CHEBI_ | 17790 | bioregistry.io | OBO |
| GO | Gene Ontology | http://purl.obolibrary.org/obo/GO_ | 0008150 | bioregistry.io | OBO |
| EC | Enzyme Commission | https://www.enzyme-database.org/query.php?ec= | 1.1.2.7 | bioregistry.io | ExPASy |
| NCBITaxon | NCBI Taxonomy | http://purl.obolibrary.org/obo/NCBITaxon_ | 270351 | bioregistry.io | NCBI |
| UniProtKB | UniProt | http://purl.uniprot.org/uniprot/ | P12345 | bioregistry.io | UniProt |
| PDB | Protein Data Bank | https://www.rcsb.org/structure/ | 1ABC | bioregistry.io | RCSB |
| KEGG | KEGG | https://www.kegg.jp/entry/ | K00001 | bioregistry.io | KEGG |
| PMID | PubMed | http://www.ncbi.nlm.nih.gov/pubmed/ | 36719530 | bioregistry.io | NCBI |
| DOI | Digital Object Identifier | https://doi.org/ | 10.1038/s41586-024-07070-8 | doi.org | DOI Foundation |
| CAS-RN | CAS Registry Number | (not directly resolvable) | 5625-37-6 | commonchemistry.cas.org | CAS |
| PubChem | PubChem Compound | https://pubchem.ncbi.nlm.nih.gov/compound/ | 12345 | bioregistry.io | NCBI |
| mediadive.medium | MediaDive Medium | https://mediadive.dsmz.de/medium/ | 77 | bioregistry.io | DSMZ |
| mediadive.solution | MediaDive Solution | https://mediadive.dsmz.de/solution/ | S6 | bioregistry.io | DSMZ |
| ingredient | KG-Microbe Ingredient | (internal) | 1633 | kg-microbe.duckdb | LBL |
| solution | KG-Microbe Solution | (internal) | 4592 | kg-microbe.duckdb | LBL |
| medium | KG-Microbe Medium | (internal) | J562 | kg-microbe.duckdb | LBL |
| ATCC | ATCC Culture Collection | https://www.atcc.org/products/ | BAA-1231 | direct | ATCC |
| DSMZ | DSMZ Culture Collection | https://www.dsmz.de/collection/catalogue/ | 88 | direct | DSMZ |

### LinkML Schema Addition

The schema should also be updated to include these prefixes:

```yaml
prefixes:
  # === External Ontologies (OBO Foundry) ===
  CHEBI: http://purl.obolibrary.org/obo/CHEBI_
  GO: http://purl.obolibrary.org/obo/GO_
  NCBITaxon: http://purl.obolibrary.org/obo/NCBITaxon_
  OBI: http://purl.obolibrary.org/obo/OBI_
  ENVO: http://purl.obolibrary.org/obo/ENVO_

  # === External Databases ===
  UniProtKB: http://purl.uniprot.org/uniprot/
  PDB: https://www.rcsb.org/structure/
  KEGG: https://www.kegg.jp/entry/
  EC: https://www.enzyme-database.org/query.php?ec=
  RHEA: https://www.rhea-db.org/rhea/
  PubChem: https://pubchem.ncbi.nlm.nih.gov/compound/
  ChEMBL: https://www.ebi.ac.uk/chembl/compound_report_card/

  # === Literature ===
  DOI: https://doi.org/
  PMID: http://www.ncbi.nlm.nih.gov/pubmed/

  # === MediaDive (DSMZ) ===
  mediadive.medium: https://mediadive.dsmz.de/medium/
  mediadive.solution: https://mediadive.dsmz.de/solution/

  # === KG-Microbe Internal (LBL) ===
  # Note: These are internal IDs, not resolvable URIs
  # Query kg-microbe.duckdb for actual data
  kgm.ingredient: tag:kg-microbe.lbl.gov,2024:ingredient/
  kgm.solution: tag:kg-microbe.lbl.gov,2024:solution/
  kgm.medium: tag:kg-microbe.lbl.gov,2024:medium/

  # === Culture Collections ===
  ATCC: https://www.atcc.org/products/
  DSMZ: https://www.dsmz.de/collection/catalogue/details/culture/DSM-
```

### Benefits of a Prefix Registry

1. **Self-documenting**: Users can understand what `ingredient:1633` means
2. **Validation**: Can check that IDs use registered prefixes
3. **Resolution**: Know where to look up each ID type
4. **Interoperability**: Standard prefix -> URI mappings for RDF export
5. **KG Integration**: Clear mapping between CMM-AI IDs and KG-Microbe/MediaDive

---

## Appendix E: CHEBI ID Overlap Analysis

```
media_ingredients.ontology_id values with CHEBI: ~48 unique IDs
chemicals.chebi_id values: ~30 unique IDs

Overlap examples:
- CHEBI:17790 (Methanol) - in both tables
- CHEBI:17234 (Glucose) - in both tables
- CHEBI:32599 (MgSO4*7H2O) - only in media_ingredients
```

The **chemicals** table focuses on **REE-related compounds** (lanthanides, lanthanophores), while **media_ingredients** has **common lab chemicals** (salts, buffers). They serve different purposes but share the CHEBI namespace.

---

## Appendix F: Schema Validation Features

The LinkML schema enforces:

1. **Required fields**: `scientific_name`, `sample_id`, `ingredient_id`, etc.
2. **Identifier patterns**: `ingredient_id` must match `^[A-Z0-9_:]+_ING_\\d+$`
3. **Enumerated values**: `role` must be from `ingredient_role_enum`
4. **Data types**: `concentration` is `float`, `ncbi_taxon_id` is `integer`
5. **Foreign keys**: `media_id` described as "Foreign key to GrowthMediaRecord" (not enforced programmatically)

### What's Missing from the Schema

The schema's `prefixes:` block (lines 16-41) only covers common ontology prefixes.

**NOT included** (but appear in data):
- `ingredient:` - KG-Microbe internal
- `solution:` - KG-Microbe internal
- `medium:` - KG-Microbe internal
- `mediadive.medium:` - DSMZ MediaDive
- `mediadive.solution:` - DSMZ MediaDive
- `CAS-RN:` - Chemical Abstracts Service

---

*Report generated: 2025-12-05*
*Split into chapters from original 2,323-line file to improve navigation and reduce redundancy.*

---

[<- Back to Index](00_index.md) | [Previous: Recommendations](07_recommendations.md)
