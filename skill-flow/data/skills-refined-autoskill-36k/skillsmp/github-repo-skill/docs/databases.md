# Database Interactions

This document describes the databases used by cmm-ai-automation and the scripts that interact with them.

## MongoDB Databases

| Database | Collection(s) | Loader Script | Client/Usage |
|----------|---------------|---------------|--------------|
| **bacdive** | `strains` | `load_bacdive_mongodb.py` | `strains/bacdive.py`, `strains_kgx_from_curies.py`, `export_bacdive_kgx.py` |
| **mediadive** | `media`, `solutions`, `ingredients` | `load_mediadive_mongodb.py` | `clients/mediadive_mongodb.py`, `export_mediadive_kgx.py` |

### BacDive MongoDB

- **Database**: `bacdive`
- **Collection**: `strains`
- **Loader**: `src/cmm_ai_automation/scripts/load_bacdive_mongodb.py`
- **Description**: Downloads ~97k strains from BacDive API using SPARQL to discover IDs and the official bacdive Python package to fetch complete JSON documents.
- **Used by**:
  - `src/cmm_ai_automation/strains/bacdive.py` - Core BacDive data extraction
  - `src/cmm_ai_automation/scripts/strains_kgx_from_curies.py` - CURIE-based strain KGX generation
  - `src/cmm_ai_automation/scripts/export_bacdive_kgx.py` - Full BacDive KGX export

### MediaDive MongoDB

- **Database**: `mediadive`
- **Collections**: `media`, `solutions`, `ingredients`
- **Loader**: `src/cmm_ai_automation/scripts/load_mediadive_mongodb.py`
- **Description**: Downloads media, solutions, and ingredients from MediaDive REST API.
- **Used by**:
  - `src/cmm_ai_automation/clients/mediadive_mongodb.py` - MediaDive MongoDB client
  - `src/cmm_ai_automation/scripts/export_mediadive_kgx.py` - MediaDive KGX export

---

## ChromaDB Collections (Vector Search)

| ChromaDB Path | Collection | Indexer Script | Query Script | Size |
|---------------|------------|----------------|--------------|------|
| `data/chroma_bacdive` | bacdive strains | `index_bacdive_chromadb.py` | (fuzzy strain search) | ~455 MB |
| `data/chroma_bacdive_media` | bacdive media compositions | `index_bacdive_media_compositions.py` | (media grounding) | ~18 MB |
| `data/chroma_mediadive` | media, ingredients, strains | `index_mediadive_chromadb.py` | `export_grounded_media_kgx.py` | ~53 MB |
| `data/chroma_ncbitaxon` | ncbitaxon_embeddings | `build_ncbitaxon_chromadb.py` | `codify_strains.py` | ~18 GB |

### BacDive ChromaDB

- **Path**: `data/chroma_bacdive`
- **Indexer**: `src/cmm_ai_automation/scripts/index_bacdive_chromadb.py`
- **Description**: Creates a searchable index of BacDive strain data for fuzzy matching of strain names, culture collection IDs, and growth conditions.
- **Source**: BacDive MongoDB

### BacDive Media ChromaDB

- **Path**: `data/chroma_bacdive_media`
- **Indexer**: `src/cmm_ai_automation/scripts/index_bacdive_media_compositions.py`
- **Description**: Creates embeddings of media name + composition text for semantic matching against ungrounded media names from the growth_media sheet.
- **Source**: `data/bacdive_strain_medium_edges.tsv`
- **Used by**: Media grounding workflows

### MediaDive ChromaDB

- **Path**: `data/chroma_mediadive`
- **Collections**: `mediadive_media`, `mediadive_ingredients`, `mediadive_strains`
- **Indexer**: `src/cmm_ai_automation/scripts/index_mediadive_chromadb.py`
- **Description**: Lightweight searchable indexes of MediaDive data including media/solution names, ingredient names/synonyms, and strain species.
- **Source**: MediaDive MongoDB
- **Used by**: `export_grounded_media_kgx.py` for media name grounding

### NCBITaxon ChromaDB

- **Path**: `data/chroma_ncbitaxon`
- **Size**: ~18 GB
- **Collection**: `ncbitaxon_embeddings`
- **Indexer**: `src/cmm_ai_automation/scripts/build_ncbitaxon_chromadb.py`
- **Description**: Pre-computed embeddings for the entire NCBITaxon ontology (~2M+ terms) for semantic search of taxonomic terms. Uses `text-embedding-3-small` embeddings.
- **Source**: OLS (Ontology Lookup Service) embeddings SQLite database
- **Used by**: `codify_strains.py` for finding NCBITaxon IDs from strain names

---

## DuckDB

| Database | Module | Usage |
|----------|--------|-------|
| `data/enrichment.duckdb` | `store/enrichment_store.py` | `enrich_to_store.py` - stores enriched chemical data |

### Enrichment Store

- **Path**: `data/enrichment.duckdb`
- **Module**: `src/cmm_ai_automation/store/enrichment_store.py`
- **Description**: LinkML-store backed DuckDB database for multi-source chemical enrichment. Stores data from PubChem, ChEBI, CAS, and Node Normalization APIs with entity resolution based on (InChIKey, CAS RN) composite keys.
- **Used by**: `enrich_to_store.py` for the ingredient enrichment pipeline

---

## Summary by Purpose

### Data Loading (MongoDB)

| Script | Description |
|--------|-------------|
| `load_bacdive_mongodb.py` | Downloads ~97k strains from BacDive API |
| `load_mediadive_mongodb.py` | Downloads media/solutions/ingredients from MediaDive REST API |

### Semantic Search Indexing (ChromaDB)

| Script | Description |
|--------|-------------|
| `index_bacdive_chromadb.py` | Index BacDive strains for fuzzy search |
| `index_bacdive_media_compositions.py` | Index BacDive media compositions for media grounding |
| `index_mediadive_chromadb.py` | Index MediaDive data for fuzzy search |
| `build_ncbitaxon_chromadb.py` | Index full NCBITaxon from OLS embeddings (~18 GB) |

### Entity Resolution (uses ChromaDB)

| Script | Description |
|--------|-------------|
| `codify_strains.py` | Find NCBITaxon IDs for strain names using semantic search |
| `export_grounded_media_kgx.py` | Ground media names to MediaDive IDs |

### Chemical Enrichment (DuckDB)

| Script | Description |
|--------|-------------|
| `enrich_to_store.py` | Multi-source enrichment with entity resolution, stores in DuckDB |
