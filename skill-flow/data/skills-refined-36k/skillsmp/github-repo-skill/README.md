<a href="https://github.com/dalito/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# cmm-ai-automation

AI-assisted automation for Critical Mineral Metabolism (CMM) data curation using LinkML, OBO Foundry tools, and Google Sheets integration.

## Collaboration

This repository is developed in collaboration with [CultureBotAI/CMM-AI](https://github.com/CultureBotAI/CMM-AI), which focuses on AI-driven discovery of microorganisms relevant to critical mineral metabolism. While CMM-AI handles the biological discovery and analysis workflows, this repository provides:

- Schema-driven data modeling with LinkML
- Integration with private Google Sheets data sources
- OBO Foundry ontology tooling for semantic annotation

### Integration with Knowledge Graph Ecosystem

This project integrates with several knowledge graph and ontology resources:

| Project | Integration |
|---------|-------------|
| [kg-microbe](https://github.com/Knowledge-Graph-Hub/kg-microbe) | Source of microbial knowledge graph data; CMM strains are linked via `kg_node_ids` |
| [kgx](https://github.com/biolink/kgx) | Knowledge graph exchange format for importing/exporting Biolink Model-compliant data |
| [biolink-model](https://github.com/biolink/biolink-model) | Schema and upper ontology for biological knowledge representation |
| [biolink-model-toolkit](https://github.com/biolink/biolink-model-toolkit) | Python utilities for working with Biolink Model |
| [metpo](https://github.com/berkeleybop/metpo) | Microbial Phenotype Ontology for annotating phenotypic traits of CMM-relevant organisms |

See also:
- [biolink organization](https://github.com/orgs/biolink/repositories) - Biolink Model ecosystem
- [biopragmatics organization](https://github.com/biopragmatics) - Identifier and ontology tools including:
  - [bioregistry](https://github.com/biopragmatics/bioregistry) - Integrative registry of biological databases and ontologies
  - [curies](https://github.com/biopragmatics/curies) - CURIE/URI conversion
  - [pyobo](https://github.com/biopragmatics/pyobo) - Python package for ontologies and nomenclatures

### OLS Embeddings for Semantic Search

This project can leverage pre-computed embeddings from the [Ontology Lookup Service (OLS)](https://www.ebi.ac.uk/ols4/) for semantic search and term mapping. See [cthoyt.com/2025/08/04/ontology-text-embeddings.html](https://cthoyt.com/2025/08/04/ontology-text-embeddings.html) for background.

**Local embeddings database:**
- ~9.5 million term embeddings from OLS-registered ontologies
- Model: OpenAI `text-embedding-3-small` (1536 dimensions)
- Schema: `(ontologyId, entityType, iri, document, model, hash, embeddings)`
- Embeddings stored as JSON strings

**Planned use cases:**
- Search Google Sheets content (strain names, media ingredients) against ontology terms
- Generate candidate mappings for unmapped terms
- Create CMM-specific embedding subsets for faster search

Reference implementation: [berkeleybop/metpo](https://github.com/berkeleybop/metpo) embeddings search code.

### CMM-AI Data Sources and APIs

The collaborating [CultureBotAI/CMM-AI](https://github.com/CultureBotAI/CMM-AI) project uses the following APIs and data sources:

**NCBI APIs (via Biopython Entrez):**
| API | Used For |
|-----|----------|
| Entrez esearch/efetch/esummary | Assembly, BioSample, Taxonomy, PubMed/PMC |
| PMC ID Converter | PMID to PMC ID resolution |
| GEO/SRA | Transcriptomics datasets |

**Other APIs:**
| API | Used For |
|-----|----------|
| [KEGG REST](https://rest.kegg.jp) | Metabolic pathways |
| [PubChem REST](https://pubchem.ncbi.nlm.nih.gov/rest/pug) | Chemical compounds |
| [RCSB PDB](https://www.rcsb.org) | Protein structures |
| [UniProt](https://www.uniprot.org) | Protein sequences and annotations |

**Database links generated:**
- Culture collections: ATCC, DSMZ, NCIMB
- MetaCyc pathways
- DOI resolution
- AlphaFold predictions
- JGI IMG/GOLD

**Ontologies used:**
CHEBI, GO, ENVO, OBI, NCBITaxon, MIxS, RHEA, BAO

**Related issues:**
- [CMM-AI #38](https://github.com/CultureBotAI/CMM-AI/issues/38) - Document how to obtain KG-Microbe database files
- [CMM-AI #37](https://github.com/CultureBotAI/CMM-AI/issues/37) - Document sources for curated media data
- [CMM-AI #16](https://github.com/CultureBotAI/CMM-AI/issues/16) - Document the 5 Data Sources in Schema

## Features

- **LinkML Schema**: Data models for CMM microbial strain data
- **Google Sheets Integration**: Read/write access to private Google Sheets (e.g., BER CMM Data)
- **AI Automation**: GitHub Actions with Claude Code for issue triage, summarization, and code assistance
- **OBO Foundry Tools**: Integration with OLS (Ontology Lookup Service) for ontology term lookup

## Implementation Notes

### Custom KGX Validation

This project employs a custom KGX validation process to accommodate project-specific requirements. These customizations are implemented in `src/cmm_ai_automation/scripts/validate_kgx_custom.py` and can be executed via the following `just` target:

```bash
just validate-kgx-custom [nodes_tsv] [edges_tsv]
```

**Note:** The script has default file paths (`data/private/static/delaney-media-*.tsv`) for local development convenience, but these files are private and not tracked in git. Users should provide their own KGX node and edge files as arguments.

The primary customizations include:

1.  **Monkey Patching**: The script monkey patches `kgx.prefix_manager.PrefixManager.is_curie` to allow slashes in the local part of CURIEs (e.g., `doi:10.1007/s00203-018-1567-5`). This is necessary because the default regex in the `kgx` library is too strict for certain valid identifiers used in this project.
2.  **Custom Prefix Injection**: The script injects additional prefixes into the `kgx.validator.Validator` instance at runtime. These prefixes are defined in `config/kgx_validation_config.yaml` and allow the validator to recognize project-specific namespaces (like `doi`, `uuid`, etc.) that are not yet registered in the standard Biolink context.

These patches and injections are applied only within the scope of the `validate-kgx-custom` target to minimize global side effects.

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [just](https://github.com/casey/just/) (command runner)
- [Docker](https://www.docker.com/) (for Neo4j)
- [MongoDB](https://www.mongodb.com/) (local or remote)

### Installation

```bash
# Clone the repository
git clone https://github.com/turbomam/cmm-ai-automation.git
cd cmm-ai-automation

# Install dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install

# Verify installation
just --list
```

### Environment Setup

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

The `.env` file contains credentials for various services. Key variables:

```bash
# Google Sheets (see "Google Sheets Authentication" section below)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service_account.json

# Neo4j (local Docker instance)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# BacDive API (register at https://api.bacdive.dsmz.de/)
BACDIVE_EMAIL=your@email.com
BACDIVE_PASSWORD=your-password

# NCBI Entrez API (get key at https://www.ncbi.nlm.nih.gov/account/settings/)
# Optional but recommended to avoid rate limits
NCBI_API_KEY=your-ncbi-api-key

# CAS Common Chemistry API (get key at https://commonchemistry.cas.org/api)
CAS_API_KEY=your-cas-key

# OpenAI API (for ChromaDB embeddings, get key at https://platform.openai.com/api-keys)
OPENAI_API_KEY=your-openai-key
```

See `.env.example` for the complete list with documentation.

### Google Sheets Authentication

Google Sheets access uses **service account authentication** (not OAuth user flow). This requires a one-time setup:

**1. Create a Google Cloud Project:**
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project (or use an existing one)

**2. Enable APIs:**
- Navigate to "APIs & Services" > "Library"
- Enable **Google Sheets API**
- Enable **Google Drive API**

**3. Create a Service Account:**
- Go to "APIs & Services" > "Credentials"
- Click "Create Credentials" > "Service account"
- Give it a name (e.g., "cmm-sheets-reader")
- No additional permissions needed for basic access
- Click "Done"

**4. Download the JSON Key:**
- Click on the service account you just created
- Go to "Keys" tab > "Add Key" > "Create new key"
- Choose JSON format and download
- Save to a secure location (e.g., `~/.config/gspread/service_account.json`)

**5. Share Spreadsheets with the Service Account:**
- Copy the service account email (looks like `name@project.iam.gserviceaccount.com`)
- Open each Google Sheet you want to access
- Click "Share" and add the service account email as a Viewer (or Editor if write access needed)

**6. Configure the Credential Path:**

Either set the environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service_account.json
```

Or place the file at the default gspread location:
```bash
mkdir -p ~/.config/gspread
cp /path/to/downloaded-key.json ~/.config/gspread/service_account.json
```

**Verify setup:**

Use a spreadsheet ID for a Google Sheet that has been shared with your service account (replace `<YOUR_SPREADSHEET_ID>` below):
```bash
uv run download-sheets --spreadsheet "<YOUR_SPREADSHEET_ID>" --output-dir /tmp/test
```

### Run the Data Pipeline

```bash
# 1. Start infrastructure
just neo4j-start              # Start Neo4j in Docker
# Ensure MongoDB is running (mongod or via Docker)

# 2. Load source data
just load-mediadive           # Load MediaDive base data (~10 sec)
just load-mediadive-details   # Fetch detailed data (~3-4 hours)

# 3. Export to KGX format
just mediadive-kgx-clean-export

# 4. Load into Neo4j
just neo4j-upload-kgx         # Uses kgx tool (proper list handling)
# OR
just neo4j-upload-custom      # Custom loader (custom labels)

# 5. Browse results
open http://localhost:7474    # Neo4j Browser
```

See [docs/pipeline.md](docs/pipeline.md) for detailed pipeline documentation.

### KGX Rebuild Pipeline

The `kgx-rebuild-all` target builds the **merged CMM Growth Knowledge Graph** - an integrated KGX dataset combining microbial strain data, growth media compositions, and chemical information enriched from multiple databases.

```bash
just kgx-rebuild-all
```

**Pipeline steps:**

| Step | Target | Description |
|------|--------|-------------|
| 1 | `clean-normalized-kgx-sheets` | Remove downloaded TSVs from `data/private/normalized-kgx-downloads/` |
| 2 | `clean-output-kgx` | Remove generated KGX outputs from `output/kgx/` |
| 3 | `download-normalized-kgx-sheets` | Download growth and medium TSVs from Google Sheets |
| 4 | `strains-kgx-from-curies` | Enrich strain CURIEs with BacDive/NCBI data |
| 5 | `chemicals-kgx-from-curies` | Enrich chemical CURIEs with PubChem/ChEBI data |
| 6 | `kgx-merge-all` | Merge all sources into final KGX files |

**Output: Merged CMM Growth Knowledge Graph**
- `output/kgx/merged/merged_nodes.tsv` - All nodes (strains, species, chemicals, media, roles)
- `output/kgx/merged/merged_edges.tsv` - All edges (in_taxon, has_role, has_part relationships)

**Data sources enriched:**
- **Strains**: BacDive (culture collection IDs, synonyms, genome accessions), NCBI Taxonomy (rank, parent taxon)
- **Chemicals**: ChEBI and PubChem (formula, mass, InChIKey, synonyms, xrefs, CAS numbers); ChEBI also provides functional role annotations

**Requirements:**
- MongoDB running locally with BacDive data loaded (see below)
- Google Sheets credentials configured
- Network access for PubChem/ChEBI/NCBI APIs

**One-time BacDive setup:**
```bash
# 1. Register for free BacDive API credentials at https://bacdive.dsmz.de/
# 2. Add credentials to .env:
#    BACDIVE_EMAIL=your@email.com
#    BACDIVE_PASSWORD=your-password

# 3. Ensure MongoDB is running (mongod or via Docker)

# 4. Load BacDive data (iterates IDs 1-200000, ~100k strains exist)
just load-bacdive                         # Full load (several hours)
just bacdive_max_id=1000 load-bacdive     # Test with first 1000 IDs

# 5. Incremental update (fetch only new IDs)
just bacdive_min_id=176393 load-bacdive   # From current max+1
```

### KGX Edge Pattern Analysis

Two scripts analyze edge patterns (subject-predicate-object triples) in KGX data. These are useful for understanding the structure of kg-microbe or any KGX dataset.

```bash
# Analyze merged KGX output (source breakdown NOT preserved)
# Default: ../kg-microbe/data/merged → output/edge_patterns/edge_patterns_merged.tsv
just edge-patterns-merged

# Analyze transformed data (source breakdown IS preserved)
# Default: ../kg-microbe/data/transformed → output/edge_patterns/edge_patterns_by_source.tsv
just edge-patterns-by-source

# Clean edge pattern outputs
just clean-edge-patterns
```

**Output format** (TSV to `output/edge_patterns/`):
```
source | subject_category | subject_prefix | predicate | object_category | object_prefix | count
```

| Target | Input Structure | Use Case |
|--------|-----------------|----------|
| `edge-patterns-merged` | Single dir with `*_nodes.tsv`, `*_edges.tsv` | Quick aggregate stats from merged output |
| `edge-patterns-by-source` | Subdirs with `<source>/nodes.tsv`, `edges.tsv` | See which source contributes each pattern |

**Requirements:**
- Clone [kg-microbe](https://github.com/Knowledge-Graph-Hub/kg-microbe) as a sibling directory (`../kg-microbe`)
- Or provide custom paths: `just kg_microbe_merged=/path/to/merged edge-patterns-merged`

## Google Sheets Usage

```python
from cmm_ai_automation.gsheets import get_sheet_data, list_worksheets

# List available tabs in the BER CMM spreadsheet
tabs = list_worksheets("BER CMM Data for AI - for editing")
print(tabs)

# Read data from a specific tab
df = get_sheet_data("BER CMM Data for AI - for editing", "media_ingredients")
print(df.head())
```

## AI Integration

This repo includes GitHub Actions that respond to `@claude` mentions in issues and PRs:
- Issue triage and labeling
- Issue summarization
- Code assistance and PR reviews

Requires `CLAUDE_CODE_OAUTH_TOKEN` secret to be configured.

## Documentation Website

[https://turbomam.github.io/cmm-ai-automation](https://turbomam.github.io/cmm-ai-automation)

## Repository Structure

* [docs/](docs/) - mkdocs-managed documentation
  * [elements/](docs/elements/) - generated schema documentation
* [examples/](examples/) - Examples of using the schema
* [project/](project/) - project files (these files are auto-generated, do not edit)
* [src/](src/) - source files (edit these)
  * [cmm_ai_automation](src/cmm_ai_automation)
    * [schema/](src/cmm_ai_automation/schema) -- LinkML schema
      (edit this)
    * [datamodel/](src/cmm_ai_automation/datamodel) -- generated
      Python datamodel
* [tests/](tests/) - Python tests
  * [data/](tests/data) - Example data

## Developer Tools

There are several pre-defined command-recipes available.
They are written for the command runner [just](https://github.com/casey/just/). To list all pre-defined commands, run `just` or `just --list`.

## Testing and Quality Assurance

### Quick Start

```bash
# Install all dependencies including QA tools
uv sync --group qa

# Run unit tests (fast, no network)
uv run pytest

# Run with coverage report
uv run pytest --cov=cmm_ai_automation
```

### Test Categories

| Command | What it runs | Speed |
|---------|--------------|-------|
| `uv run pytest` | Unit tests only (default) | ~1.5s |
| `uv run pytest -m integration` | Integration tests (real API calls) | Slower |
| `uv run pytest --cov=cmm_ai_automation` | Unit tests with coverage | ~9s |
| `uv run pytest --durations=20` | Show slowest 20 tests | ~1.5s |

### Pre-commit Hooks

Pre-commit hooks run automatically before each commit, catching issues early:

```bash
# Install pre-commit hooks (one-time setup)
uv sync --group qa
uv run pre-commit install

# Run all hooks manually on all files
uv run pre-commit run --all-files

# Run specific hook
uv run pre-commit run ruff --all-files
uv run pre-commit run mypy --all-files
```

**Hooks included:**
- `ruff` - Fast Python linter and formatter
- `ruff-format` - Code formatting
- `mypy` - Static type checking
- `yamllint` - YAML linting
- `codespell` - Spell checking
- `typos` - Fast typo detection
- `deptry` - Dependency checking
- `check-yaml`, `end-of-file-fixer`, `trailing-whitespace` - General file hygiene

### Running Individual QA Tools

```bash
# Linting with ruff
uv run ruff check src/
uv run ruff check --fix src/  # Auto-fix issues

# Type checking with mypy
uv run mypy src/cmm_ai_automation/

# Format code
uv run ruff format src/

# Check dependencies
uv run deptry src/
```

### Thorough QA Check (CI-equivalent)

Run everything that CI runs:

```bash
# 1. Install all dependencies
uv sync --group qa --group dev

# 2. Run pre-commit on all files
uv run pre-commit run --all-files

# 3. Run tests with coverage
uv run pytest --cov=cmm_ai_automation

# 4. Build documentation (catches doc errors)
uv run mkdocs build
```

### Integration Tests

Integration tests make real API calls and are skipped by default (some APIs block CI IPs):

```bash
# Run integration tests (requires network, API keys)
uv run pytest -m integration

# Run specific integration test file
uv run pytest tests/test_chebi.py -m integration

# Run both unit and integration tests
uv run pytest -m ""
```

**API keys for integration tests:**
- `CAS_API_KEY` - CAS Common Chemistry API
- Most other APIs (ChEBI, PubChem, MediaDive, NodeNormalization) work without keys

### Coverage Targets

Current coverage configuration (see `pyproject.toml`):
- Scripts are excluded from coverage (CLI entry points)
- Target: 30% minimum (see issue #29 for roadmap to 60%)
- Run `uv run pytest --cov-report=term-missing` to see uncovered lines

## Credits

This project uses the template [linkml-project-copier](https://github.com/dalito/linkml-project-copier) published as [doi:10.5281/zenodo.15163584](https://doi.org/10.5281/zenodo.15163584).

AI automation workflows adapted from [ai4curation/github-ai-integrations](https://github.com/ai4curation/github-ai-integrations) (Monarch Initiative).

## Related Projects

- [CultureBotAI/CMM-AI](https://github.com/CultureBotAI/CMM-AI) - AI-driven discovery for critical mineral metabolism research
- [Knowledge-Graph-Hub/kg-microbe](https://github.com/Knowledge-Graph-Hub/kg-microbe) - Knowledge graph for microbial data integration
- [biolink organization](https://github.com/orgs/biolink/repositories) - Biolink Model ecosystem including:
  - [biolink/kgx](https://github.com/biolink/kgx) - Knowledge Graph Exchange tools
  - [biolink/biolink-model](https://github.com/biolink/biolink-model) - Schema and upper ontology
  - [biolink/biolink-model-toolkit](https://github.com/biolink/biolink-model-toolkit) - Python utilities
- [berkeleybop/metpo](https://github.com/berkeleybop/metpo) - Microbial Phenotype Ontology for phenotypic trait annotation
- [biopragmatics organization](https://github.com/biopragmatics) - Identifier and ontology tools including:
  - [bioregistry](https://github.com/biopragmatics/bioregistry) - Integrative registry of biological databases and ontologies
  - [curies](https://github.com/biopragmatics/curies) - CURIE/URI conversion
  - [pyobo](https://github.com/biopragmatics/pyobo) - Python package for ontologies and nomenclatures
