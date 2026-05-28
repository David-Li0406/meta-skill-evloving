# Chapter 2: Data Model Analysis

[<- Back to Index](00_index.md) | [Previous: Project Context](01_project_context.md) | [Next: Data Quality Issues ->](03_data_quality_issues.md)

---

## The Two Data Systems

### System A: Google Sheets -> XLSX -> TSV

```
Collaborators type/paste into Google Sheets
    | (manual process, undocumented)
    v
Marcin downloads as XLSX
    |
    v
data/sheet/BER CMM Data for AI.xlsx (254 KB, Dec 4 2025)
    |
    v
make convert-excel (runs src/convert_sheets.py)
    |
    v
data/txt/sheet/BER_CMM_Data_for_AI_*.tsv (16 files)
```

**Characteristics:**
- Contains manual entries, possibly LLM-generated content
- Has UTF-8 encoding issues (mojibake: see [Chapter 3](03_data_quality_issues.md))
- Overwrites previous TSV files on each conversion
- No version control on Google Sheet edits
- No record of who entered what or when

### System B: Python Extend Scripts

```
Seed data (hardcoded in Python or from TSV)
    |
    v
API queries (NCBI, KEGG, UniProt, PDB, KG-Microbe)
    |
    v
src/extend_*.py scripts
    |
    v
data/txt/sheet/extended/BER_CMM_Data_for_AI_*_extended.tsv (16 files)
```

**Characteristics:**
- Reproducible (run `make update-*` commands)
- Clean UTF-8 encoding
- Outputs to separate `extended/` subdirectory
- Source provenance tracked (mostly)
- Some data hardcoded in Python (e.g., `CURATED_MEDIA` dict in media_search.py)

---

## Case Study: media_ingredients.tsv

### The Two Versions

| Aspect | Google Sheet Version | Extended Version |
|--------|---------------------|------------------|
| **Location** | `data/txt/sheet/BER_CMM_Data_for_AI_media_ingredients.tsv` | `data/txt/sheet/extended/BER_CMM_Data_for_AI_media_ingredients_extended.tsv` |
| **Date** | Dec 4, 2025 | Nov 13, 2025 |
| **Size** | 12 KB (64 rows) | 9 KB |
| **Media count** | 8 media | 7 media |
| **Has MP medium?** | Yes (with detailed description) | No |
| **UTF-8 clean?** | No (mojibake present) | Yes |
| **kg_microbe_nodes** | Populated | Populated (different values) |

### Where Did MP Medium Come From?

The Google Sheet version contains "MP medium (PIPES-buffered methylotroph minimal medium)" with an elaborate description:

> "Defined minimal medium composed of a PIPES buffering system, phosphorus salts, major inorganic salts, and a trace metals mix..."

But **MP medium does not exist in the Python code** (`src/media_search.py` -> `CURATED_MEDIA` dict only has 7 media: ATCC:1306, NMS, AMS, DSMZ:88, LB, R2A, MPYG).

**Possible origins (unknown which is true):**
1. Someone manually typed it into Google Sheets
2. An LLM generated it and someone pasted it
3. A different script generated it (not found in codebase)
4. Copied from literature

**This cannot be determined from available evidence.**

### Column Analysis: media_ingredients.tsv

| Column | Purpose | Populated | Issues |
|--------|---------|-----------|--------|
| `ingredient_id` | Primary key | 100% | Pattern: `{media_id}_ING_{NNN}` |
| `ingredient_name` | Chemical name | 100% | |
| `media_id` | FK -> growth_media | 100% | |
| `media_name` | Denormalized | 100% | Violates 3NF (redundant) |
| `ontology_id` | CHEBI ID | ~75% | Missing for complex mixtures |
| `ontology_label` | CHEBI label | ~75% | |
| `chemical_formula` | Molecular formula | ~70% | UTF-8 corruption |
| `concentration` | Numeric value | 100% | |
| `unit` | g/L, mL/L, mM, etc. | 100% | Inconsistent units |
| `role` | Functional category | 100% | Undocumented vocabulary |
| `kg_microbe_nodes` | KG linkage | ~80% | Mixed ID types |
| `notes` | Comments | 0% | Unused |
| `source` | Provenance | 100% | All rows say "extend" |

---

## Foreign Key Analysis: media_ingredients.tsv

### OUTBOUND (media_ingredients references other tables)

| Column | References | Target Table | Target Column | Status |
|--------|------------|--------------|---------------|--------|
| **media_id** | -> | **growth_media** | `media_id` | Valid FK - All 8 media_ids exist |
| **ontology_id** (CHEBI:*) | -> | **chemicals** | `chebi_id` | Partial overlap |

### INBOUND (other tables reference media_ingredients)

| Source Table | Source Column | References | Status |
|--------------|---------------|------------|--------|
| **bioprocesses** | `growth_conditions` | mentions media names | Soft reference - Text, not FK |
| **strains** | `growth_requirements` | None | Missing - Should link |

### Missing Relationships (Should Exist Based on Proposal)

| Relationship | Why It's Needed |
|--------------|-----------------|
| **strains** -> **growth_media** | Task 2.1: "Strains...will be grown comparing use of REE in soluble vs insoluble form" |
| **screening_results** -> **growth_media** | Task 1.3: HTP screening needs to record which media was used |
| **bioprocesses** -> **growth_media** | Should be a proper FK, not text like "LB medium" |

### Denormalization Issue

The `media_name` column in media_ingredients is **redundant** - it duplicates data from growth_media. This violates 3NF:

```
media_ingredients.media_id -> growth_media.media_id -> growth_media.media_name
```

If `media_name` changes in growth_media, it must be updated in 64 rows of media_ingredients.

---

## Media/Ingredients Data Model Design Analysis

### Current State Assessment

#### 1. Normalization Violations

**Current structure** (denormalized):
```
media_ingredients.tsv contains:
- ingredient_id (PK)
- ingredient_name
- media_id (FK)
- media_name  <- REDUNDANT (violates 3NF)
- ontology_id
- ontology_label
- chemical_formula
- concentration
- unit
- role
- kg_microbe_nodes
```

**Recommended 3-table structure**:

| Table | Purpose | Columns |
|-------|---------|---------|
| **growth_media** | Media characteristics | media_id (PK), media_name, ph, sterilization, target_organisms, references |
| **ingredients** | Canonical ingredient definitions | ingredient_id (PK, use CHEBI where available), name, formula, cas_number, default_roles[] |
| **media_compositions** | Junction with concentrations | media_id (FK), ingredient_id (FK), concentration, unit, role_in_context, preparation_notes |

#### 2. Ad-hoc ingredient_id Namespace

**Current**: `ATCC1306_001`, `NMS_001` - embeds media context into ingredient IDs

**Problem**: Same chemical (MgSO4*7H2O) gets multiple IDs:
- `AMS_ING_001` = MgSO4*7H2O in AMS medium
- `ATCC:1306_ING_003` = MgSO4*7H2O in ATCC:1306 medium
- `NMS_ING_001` = MgSO4*7H2O in NMS medium

**Recommendation**: Use CHEBI as canonical identifier where available. For compounds without CHEBI:
- Create a project namespace: `CMM:ING-0001`, `CMM:ING-0002`, etc.
- Document what each local ID represents
- Store the mapping to CHEBI/CAS when added later

#### 3. Context-Dependent Roles

**Yes, ingredients can have different roles depending on context:**

| Ingredient | Context 1 | Context 2 |
|------------|-----------|-----------|
| K2HPO4 (dipotassium phosphate) | **buffer** (pH stabilization) | **mineral** (phosphorus source) |
| (NH4)2SO4 (ammonium sulfate) | **nitrogen source** | **sulfur source** |
| FeSO4*7H2O (ferrous sulfate) | **trace element** (minimal media) | **iron source** (iron-limited experiments) |
| NaCl (sodium chloride) | **salt** (osmotic balance) | **mineral** (Na+ source) |

**Current model assigns ONE role per ingredient per media** - this loses information.

**Recommendation**:
- Allow multivalued roles: `roles: ["buffer", "phosphorus source"]`
- Or create separate columns: `primary_role`, `secondary_roles`

---

## Microbe-Media Relationship Analysis

### Question: Do any data tables assert relationships between microbes and media?

**Short answer: The relationships are WEAK and mostly implicit. No explicit FK relationships exist.**

### What Currently EXISTS

| Table | Column | Relationship to Media | Type |
|-------|--------|----------------------|------|
| **growth_media** | `target_organisms` | Lists genera like "Methylobacterium; Methylorubrum; methylotrophs" | Soft/implicit - free text |
| **bioprocesses** | `growth_conditions` | Text like "LB medium, aerobic, 200 rpm shaking" | Soft/implicit - text, not FK |
| **strains** | `growth_requirements` | Lists phenotypes like "urease; catalase; mesophilic" | NOT media - enzymatic traits |
| **screening_results** | (none) | No media column at all | Missing |

### Recommended Fix: New Junction Table

A proper design would add a `strain_media_growth` junction table:

| Column | Type | Description |
|--------|------|-------------|
| `strain_id` | FK -> strains | Which strain |
| `media_id` | FK -> growth_media | Which medium |
| `growth_quality` | enum | none, poor, moderate, good, optimal |
| `doubling_time_hours` | float | Growth rate metric |
| `max_od600` | float | Maximum optical density achieved |
| `optimal_temperature` | float | Optimal growth temperature |
| `optimal_ph` | float | Optimal pH |
| `ree_supplementation` | string | REE type and concentration if applicable |
| `notes` | string | Additional observations |
| `source` | string | Literature, experiment, DSMZ catalog, etc. |

---

## LinkML Schema and Data Table Relationships

### Data Flow Architecture

```
+-----------------------------------------------------------------------------+
|                           DATA SOURCES                                       |
+-----------------------------------------------------------------------------+
|  Google Sheets -> XLSX -> TSV (data/txt/sheet/*.tsv)                        |
|  Python extend scripts -> Extended TSV (data/txt/sheet/extended/*_extended.tsv)|
+-----------------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------------+
|                        src/tsv_to_linkml.py                                  |
|  Converts TSV files -> LinkML YAML format                                    |
+-----------------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------------+
|                     data/linkml_database.yaml                                |
|  5,098 lines of YAML data                                                    |
+-----------------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------------+
|                       linkml-validate                                        |
|  Validates YAML against schema/lanthanide_bioprocessing.yaml                |
+-----------------------------------------------------------------------------+
```

### Schema Class to TSV File Mapping

| Schema Class | TSV File | Key Fields |
|--------------|----------|------------|
| `GenomeRecord` | `taxa_and_genomes.tsv` | scientific_name, ncbi_taxon_id, genome_identifier |
| `BiosampleRecord` | `biosamples.tsv` | sample_id, organism, download_url |
| `PathwayRecord` | `pathways.tsv` | pathway_id, pathway_name, genes |
| `GeneProteinRecord` | `genes_and_proteins.tsv` | gene_protein_id, annotation, ec_number |
| `MacromolecularStructureRecord` | `macromolecular_structures.tsv` | pdb_id, method, resolution |
| `PublicationRecord` | `publications.tsv` | url, title, journal, year, pmid |
| `DatasetRecord` | `datasets.tsv` | dataset_name, data_type, url |
| `ChemicalCompoundRecord` | `chemicals.tsv` | chemical_id, chebi_id, compound_type |
| `AssayMeasurementRecord` | `assays.tsv` | assay_id, assay_type, detection_method |
| `BioprocessConditionsRecord` | `bioprocesses.tsv` | process_id, strain_used, pH, temperature |
| `ScreeningResultRecord` | `screening_results.tsv` | experiment_id, strain_barcode, hit_classification |
| `ProtocolRecord` | `protocols.tsv` | protocol_id, protocol_type, protocol_doi |
| `TranscriptomicsRecord` | `transcriptomics.tsv` | accession, experiment_type |
| `StrainRecord` | `strains.tsv` | strain_id, source_collection |
| `GrowthMediaRecord` | `growth_media.tsv` | media_id, media_name, ph |
| `MediaIngredientRecord` | `media_ingredients.tsv` | ingredient_id, media_id, concentration, role |

---

## Bioregistry vs Data Repository Clarification

### Common Confusion

Marcin mentioned "mediadive data are in bioregistry" - this is confusing because:

| Tool | What It Is | What It Contains |
|------|------------|------------------|
| **[Bioregistry](https://bioregistry.io/)** | Prefix registry/resolver | Metadata about databases (prefix patterns, URLs, contacts) |
| **[PyOBO](https://github.com/biopragmatics/pyobo)** | Data converter | Code to download and convert databases to OBO/OWL |
| **[obo-db-ingest](https://github.com/biopragmatics/obo-db-ingest)** | Data repository | Actual converted OBO/OWL files from PyOBO |

### MediaDive Specifically

- **Bioregistry HAS**: Prefix registration for `mediadive.medium` and `mediadive.solution`
  - `mediadive.medium:77` resolves to `https://mediadive.dsmz.de/medium/77`
- **Bioregistry DOES NOT HAVE**: The actual MediaDive data
- **obo-db-ingest**: Does NOT currently contain MediaDive
- **Raw data lives at**: https://mediadive.dsmz.de/ with RDF export available

### Best Practices: MediaDive Reference

**MediaDive** (https://mediadive.dsmz.de/) is the gold standard for microbial growth media databases.

**Their data model**:

| Entity | Count | Description |
|--------|-------|-------------|
| Media | 3,327 | Complete formulations with metadata |
| Solutions | 5,844 | Stock solutions, trace element mixes, vitamin mixes |
| Ingredients | 1,235 | Canonical chemical compounds |

**Key design principles from MediaDive**:

1. **Hierarchical ingredients**: Solutions can contain other solutions
2. **Canonical ingredient registry**: Each unique chemical has ONE record
3. **Concentration in junction table**: Amount, unit, preparation notes
4. **SPARQL endpoint**: Machine-readable access for integration
5. **Provenance**: Each medium has source references

---

[<- Back to Index](00_index.md) | [Previous: Project Context](01_project_context.md) | [Next: Data Quality Issues ->](03_data_quality_issues.md)
