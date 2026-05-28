# CMM Knowledge Graph & Machine Learning Pipeline

> Comprehensive overview of the CultureBotAI/CMM project's data pipeline, knowledge graph construction, and machine learning components.

**Last updated:** 2025-12-18

---

## Table of Contents

1. [Pipeline Overview](#pipeline-overview)
2. [Data Sources](#data-sources)
3. [Component Details](#component-details)
   - [MicroMediaParam](#1-micromediaparam-public)
   - [kg-ai-prep](#2-kg-ai-prep-private)
   - [MicroGrowLink](#3-microgrowlink-private)
   - [microbe-rules](#4-microbe-rules-public)
   - [MicroGrowLinkService](#5-microgrowlinkservice-public)
   - [CMM-AI](#6-cmm-ai-private)
   - [MATE-LLM](#7-mate-llm-private)
4. [KGX Data Format](#kgx-data-format)
5. [Machine Learning Models](#machine-learning-models)
6. [Your Role: Knowledge Graph Construction](#your-role-knowledge-graph-construction)
7. [Anticipated Payoffs](#anticipated-payoffs)
8. [Repository Access](#repository-access)

---

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. DATA SOURCES                                                            │
│  ├── BacDive/MediaDive (strain-media relationships)                         │
│  ├── DSMZ (media compositions, chemical ingredients)                        │
│  └── ChEBI/PubChem (chemical ontologies)                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  2. MicroMediaParam                                                         │
│  Chemical compound → Knowledge Graph entity mapping                         │
│  Output: composition_kg_mapping_final.tsv                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  3. Knowledge Graph Construction (YOUR WORK)                                │
│  Create strain→medium edges in KGX format                                   │
│  Output: nodes.tsv, edges.tsv                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  4. kg-ai-prep                                                              │
│  Graph preprocessing & filtering for ML                                     │
│  Output: Model-ready train/val/test splits                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  5. MicroGrowLink                                                           │
│  Train graph transformer models (RGT, HGT, NBFNet)                          │
│  Task: Link prediction for "microbe_grows_in_medium"                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  6. microbe-rules                                                           │
│  CatBoost models for feature importance & interpretability                  │
│  Output: Which chemicals/features predict growth                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  7. MicroGrowLinkService                                                    │
│  Gradio web application serving predictions                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Sources

### BacDive / MediaDive
- **URL:** https://bacdive.dsmz.de / https://mediadive.dsmz.de
- **Content:** Strain metadata, growth conditions, media compositions
- **Format:** JSON API

### DSMZ Media Database
- **Content:** 1,807+ microbial growth media formulations
- **Details:** Chemical compositions, concentrations, preparation instructions
- **Solutions:** Expandable solution references (e.g., "solution:241")

### Chemical Ontologies
- **ChEBI:** Chemical Entities of Biological Interest
- **PubChem:** Chemical compound database
- **CAS-RN:** Chemical Abstracts Service Registry Numbers

---

## Component Details

### 1. MicroMediaParam (PUBLIC)

**Repository:** https://github.com/CultureBotAI/MicroMediaParam

**Purpose:** Map chemical compounds from growth media to knowledge graph entities.

**Key Statistics:**
- 23,181 chemical entries processed
- 1,807 microbial growth media
- 78% ChEBI coverage (18,088 compounds mapped)
- 99.99% mapping accuracy

**Features:**
- Hydrate parsing (e.g., "MgCl2 6-hydrate" → base + water molecules)
- Multi-database mapping (ChEBI, PubChem, CAS-RN)
- Molecular weight calculation (anhydrous and hydrated forms)
- DSMZ solution expansion into individual chemicals
- Fuzzy matching for chemical name variations

**Output:** `composition_kg_mapping_final.tsv`

Key columns:
- `medium_id`: Unique medium identifier
- `original`: Original compound name
- `mapped`: Database identifier (ChEBI/PubChem/CAS-RN)
- `base_compound`: Chemical without hydration
- `water_molecules`: Hydration number
- `base_chebi_id`: ChEBI identifier
- `base_chebi_label`: Human-readable name
- `base_chebi_formula`: Standardized formula
- `base_molecular_weight`: Anhydrous MW
- `hydrated_molecular_weight`: Total MW with water

---

### 2. kg-ai-prep (PRIVATE)

**Repository:** https://github.com/CultureBotAI/kg-ai-prep

**Purpose:** Prepare knowledge graphs for AI model training with research-backed filtering strategies.

**Problems Addressed:**
- Embedding collapse (trivial values)
- Low-confidence predictions
- Training instability
- Structural noise in raw KGs

**Filtering Strategies:**

| Filter Type | Options |
|------------|---------|
| **Structural** | Singleton removal, leaf pruning, degree thresholds, k-core extraction, hub removal |
| **Component** | Giant component extraction, small component removal, bridge detection |
| **Relational** | Task-specific filtering, redundant relation removal, confidence thresholds |
| **Metapath** | Domain-guided subgraph extraction, multi-hop preservation |

**Model-Specific Optimizations:**

| Model | Strategy |
|-------|----------|
| **RotatE/TransE** | Remove singletons/leaves, dense connectivity |
| **RGT/GNNs** | Preserve attribute nodes, k-core filtering |
| **A*Net** | Ensure path connectivity, minimum degree |

**CLI Usage:**
```bash
# Analyze graph
kg-ai-prep analyze nodes.tsv edges.tsv --target-relation "microbe_grows_in_medium"

# Full preprocessing
kg-ai-prep preprocess nodes.tsv edges.tsv \
    --output-dir processed_kg/ \
    --remove-singletons \
    --min-degree 2 \
    --giant-component-only \
    --target-relation "microbe_grows_in_medium" \
    --export-rotate
```

**Python API:**
```python
from kg_ai_prep import KGPreprocessor, FilterConfig, SplitConfig

prep = KGPreprocessor()
graph = prep.load_kgx("nodes.tsv", "edges.tsv")

config = FilterConfig(
    target_relation="microbe_grows_in_medium",
    remove_singletons=True,
    min_degree=2,
    keep_giant_component_only=True,
    model_type="rotate"
)

filtered_graph = prep.filter(graph, config)

split_config = SplitConfig(
    strategy="transductive_edge",
    ratios=(0.8, 0.1, 0.1),
    negative_sampling_ratio=1.0,
    hard_negatives=True
)

splits = prep.split(filtered_graph, split_config)
prep.export_rotate(splits, "rotate_output/")
```

**Performance Benefits** (from Ratajczak et al., 2022):
- 20-40% improvement on target prediction tasks
- 26-60% reduction in irrelevant nodes
- Increased prediction confidence
- More stable hyperparameter tuning

---

### 3. MicroGrowLink (PRIVATE)

**Repository:** https://github.com/CultureBotAI/MicroGrowLink

**Purpose:** Train link prediction models on the microbial growth knowledge graph.

**Supported Models:**

| Model | Type | Description |
|-------|------|-------------|
| **RGT** | Relational Graph Transformer | Transformer architecture for heterogeneous graphs |
| **HGT** | Heterogeneous Graph Transformer | Attention-based heterogeneous graph learning |
| **NBFNet** | Neural Bellman-Ford Network | Path-based reasoning for link prediction |

*Note: Relational GCNs (RGCNs) have been deprecated.*

**Input Requirements:**
- `merged-kg_nodes.tsv` (KGX format)
- `merged-kg_edges.tsv` (KGX format)

**Directory Structure:**
```
MicroGrowLink/
├── data/           # KGX data and taxa lists
├── hpc/            # SLURM scripts for multi-GPU
├── scripts/        # Utility scripts
├── src/
│   ├── learn/      # Model implementations
│   └── eval/       # Evaluation scripts
├── docs/           # Model documentation (RGT.md, HGT.md, NBFNet.md)
└── predictions/    # Output predictions
```

**Task:** Predict `microbe_grows_in_medium` edges (which microbes can grow in which media).

---

### 4. microbe-rules (PUBLIC)

**Repository:** https://github.com/CultureBotAI/microbe-rules

**Purpose:** Interpretable ML using CatBoost for feature importance analysis.

**Models:**
- Binary classification models (CatBoost)
- Two configurations: 514 features and 65 features
- Multiple model variants per configuration

**Pipeline:**
```bash
# Prepare data
python 01_prepare_data_binary.py

# Train models
python 02_compute_compare_models.py 514 --model_id 1
python 02_compute_compare_models.py 65 --model_id 0

# Feature importance
python 03_compute_feature_importance_agreement.py 65
python 03_compute_feature_importance_agreement.py 514

# ARA analysis
python 04_compute_ara.py 65 --trte_set train
python 04_compute_ara.py 514 --trte_set test
```

**Output:** Feature importance rankings showing which chemicals/properties predict microbial growth.

**Requirements:** Python 3.12 (CatBoost incompatible with 3.13)

---

### 5. MicroGrowLinkService (PUBLIC)

**Repository:** https://github.com/CultureBotAI/MicroGrowLinkService

**Purpose:** Gradio web application serving growth media predictions.

**Features:**
- User-friendly interface for querying predictions
- Takes taxon as input, returns predicted growth media
- Serves trained MicroGrowLink models

---

### 6. CMM-AI (PRIVATE)

**Repository:** https://github.com/CultureBotAI/CMM-AI

**Purpose:** Lanthanide bioprocessing data pipeline for rare earth element research.

**Scientific Focus:**
- XoxF methanol dehydrogenase (lanthanide-dependent enzymes)
- Methylotrophic bacteria
- Environmental metal cycling
- Siderophore/lanthanophore transport

**Data Tables (16 total):**

| Table | Rows | Description |
|-------|------|-------------|
| Taxa & Genomes | 211 | Bacteria/archaea with NCBI Assembly URLs |
| Genes & Proteins | 226 | UniProt/KEGG with annotations |
| Biosamples | 132 | Environmental samples |
| Publications | 99 | PubMed/bioRxiv literature |
| Pathways | 77 | KEGG/MetaCyc pathways |
| Chemicals | 66 | PubChem/ChEBI compounds |
| Media Ingredients | 63 | Growth media components |
| Transcriptomics | 29 | RNA-seq from SRA/GEO |
| Strains | 24 | Culture collection strains |
| Structures | 18 | PDB + AlphaFold predictions |
| Protocols | 17 | Experimental SOPs |
| Datasets | 15 | Research datasets |
| Assays | 10 | Analytical methods |
| Growth Media | 8 | Complete formulations |
| Bioprocesses | 5 | Experimental conditions |
| Screening Results | 4 | HTS data |

**Total:** ~1,004 data rows across 16 tables

**Makefile Commands:**
```bash
make install          # Install dependencies
make convert-excel    # Excel → TSV conversion
make update-all       # Run full pipeline
make update-genomes   # Extend with NCBI data
make status          # View pipeline status
```

---

### 7. MATE-LLM (PRIVATE)

**Repository:** https://github.com/CultureBotAI/MATE-LLM

**Purpose:** Metadata And Table Extraction with LLMs

**Description:** Uses large language models to extract structured metadata and tabular data from scientific literature.

---

## KGX Data Format

The pipeline uses **KGX (Knowledge Graph Exchange)** TSV format throughout.

### Nodes File (`nodes.tsv`)

```tsv
id	category	name	description
CHEBI:16828	biolink:ChemicalEntity	L-tryptophan	Amino acid
EC:4.1.99.1	biolink:Enzyme	tryptophan deaminase	Enzyme
NCBITaxon:123456	biolink:OrganismTaxon	Methylobacterium sp.	Bacterium
DSMZ:1234	biolink:EnvironmentalFeature	Medium 1234	Growth medium
```

### Edges File (`edges.tsv`)

```tsv
subject	predicate	object	confidence
NCBITaxon:123456	microbe_grows_in_medium	DSMZ:1234	0.95
CHEBI:16828	biolink:part_of	DSMZ:1234	1.0
```

### Key Predicates

| Predicate | Meaning |
|-----------|---------|
| `microbe_grows_in_medium` | **Target relation** - taxon can grow in medium |
| `biolink:part_of` | Chemical is component of medium |
| `biolink:participates_in` | Chemical participates in reaction |
| `biolink:capable_of` | Organism has capability |

---

## Machine Learning Models

### Graph Embedding Models (MicroGrowLink)

| Model | Architecture | Strengths |
|-------|--------------|-----------|
| **RGT** | Relational Graph Transformer | Handles relation types explicitly |
| **HGT** | Heterogeneous Graph Transformer | Attention across node/edge types |
| **NBFNet** | Neural Bellman-Ford | Path-based reasoning |

### Interpretable Models (microbe-rules)

| Model | Type | Use Case |
|-------|------|----------|
| **CatBoost** | Gradient Boosting | Feature importance, explainability |

### Export Formats

**RotateE Format:**
- `train.txt`, `val.txt`, `test.txt` (tab-separated triples)
- `entity2id.txt`, `relation2id.txt` (vocabularies)

**RGT Format:**
- `train_graph.json`, `val_graph.json`, `test_graph.json`
- `node_features.json`, `vocabularies.json`

**A*Net Format:**
- `graph.json` (with path costs)
- `val_queries.json`, `test_queries.json`

---

## Your Role: Knowledge Graph Construction

### What You Need to Build

**Primary task:** Create KGX-format edges representing `microbe_grows_in_medium` relationships.

### Input Sources

1. **BacDive/MediaDive API** - strain-media associations
2. **MicroMediaParam output** - chemical compositions already mapped to ChEBI
3. **DSMZ strain collections** - culture metadata

### Output Requirements

1. **nodes.tsv** with:
   - Taxon nodes (`biolink:OrganismTaxon`)
   - Medium nodes (`biolink:EnvironmentalFeature`)
   - Chemical nodes (`biolink:ChemicalEntity`) - from MicroMediaParam

2. **edges.tsv** with:
   - `microbe_grows_in_medium` edges (strain → medium)
   - `biolink:part_of` edges (chemical → medium)
   - Confidence scores where available

### Tools Available

- **linkml-store** - mentioned in Slack discussions for KG construction
- **kg-ai-prep** - for preprocessing your KG before ML training
- **METPO** (Microbial Phenotype Ontology) - for phenotype annotations

### Workflow

```
1. Extract strain-media pairs from BacDive/MediaDive
          ↓
2. Map strains to NCBITaxon IDs
          ↓
3. Map media to DSMZ IDs (already in MicroMediaParam)
          ↓
4. Create KGX nodes.tsv and edges.tsv
          ↓
5. Run kg-ai-prep for filtering/splitting
          ↓
6. Hand off to Marcin for MicroGrowLink training
```

---

## Anticipated Payoffs

### Scientific Goals

1. **Predict growth media for unstudied microbes**
   - Given a new taxon, suggest media it might grow in
   - Reduce trial-and-error in cultivation

2. **Explain predictions**
   - Identify which chemicals drive growth predictions
   - Understand nutritional requirements

3. **Design novel media**
   - Potentially design new media for difficult-to-culture organisms
   - Optimize existing media formulations

### Technical Benefits

- **20-40% improvement** in link prediction accuracy (with proper KG filtering)
- **Reduced training time** by removing irrelevant graph structure
- **Interpretable results** via CatBoost feature importance

### Broader Impact

- Advance cultivation of rare earth element-processing microbes
- Support lanthanide bioprocessing research
- Enable culture-independent predictions for environmental samples

---

## Repository Access

### Public Repositories (Direct Access)

| Repository | URL |
|------------|-----|
| MicroMediaParam | https://github.com/CultureBotAI/MicroMediaParam |
| microbe-rules | https://github.com/CultureBotAI/microbe-rules |
| MicroGrowLinkService | https://github.com/CultureBotAI/MicroGrowLinkService |
| PFAS-AI | https://github.com/CultureBotAI/PFAS-AI |
| auto-term-catalog | https://github.com/CultureBotAI/auto-term-catalog |
| assay-metadata | https://github.com/CultureBotAI/assay-metadata |
| eggnog_runner | https://github.com/CultureBotAI/eggnog_runner |

### Private Repositories (gh CLI Access)

| Repository | Description |
|------------|-------------|
| kg-ai-prep | KG preprocessing for ML |
| MicroGrowLink | Core ML training code |
| CMM-AI | Lanthanide data pipeline |
| MATE-LLM | LLM-based extraction |
| KG-Microbe-search | KG search functionality |
| kg-microbe-projects | Project configurations |
| eggnogtable | EggNOG data tables |

**Access via gh CLI:**
```bash
# View README
gh api repos/CultureBotAI/kg-ai-prep/readme --jq '.content' | base64 -d

# List files
gh api repos/CultureBotAI/kg-ai-prep/contents --jq '.[].name'

# Clone (if needed)
gh repo clone CultureBotAI/kg-ai-prep
```

---

## Quick Reference

### Key Target Relation
```
microbe_grows_in_medium
```

### KGX Node Categories
```
biolink:OrganismTaxon      # Microbial taxa
biolink:EnvironmentalFeature  # Growth media
biolink:ChemicalEntity     # Chemical compounds
biolink:Enzyme             # Enzymes
biolink:MolecularActivity  # Activities
```

### Filtering Commands (kg-ai-prep)
```bash
# Basic preprocessing
kg-ai-prep preprocess nodes.tsv edges.tsv \
    --remove-singletons \
    --min-degree 2 \
    --giant-component-only \
    --target-relation "microbe_grows_in_medium"

# Model-specific export
--export-rotate   # For RotatE/TransE
--export-rgt      # For RGT
--export-astar    # For A*Net/NBFNet
```

### Related Slack Workspaces
- **NMDC** (`slack-nmdc`)
- **BerkeleyBOP** (`slack-berkeleybop`)
- **BER-CMM** (`slack-ber-cmm`) - #cmm-ai, #all-ber-cmm-pilot-project

### Related GitHub Repos
- `turbomam/issues` - Issue #3 (cmm-ai project) and #16 (Slack MCP guide)
- `CultureBotAI/*` - All ML and KG repos

---

*Document generated from CultureBotAI repository analysis via gh CLI.*
