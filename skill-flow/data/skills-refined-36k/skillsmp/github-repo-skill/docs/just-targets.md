# Just Targets Reference

This document lists all available `just` targets. Run `just --list` to see this list in your terminal.

## Quick Reference

| Category | Common Targets |
|----------|----------------|
| **Getting Started** | `just install`, `just test`, `just qa` |
| **MediaDive Pipeline** | `just load-mediadive`, `just mediadive-kgx-clean-export`, `just neo4j-upload-kgx` |
| **Google Sheets** | `just download-normalized-kgx-sheets`, `just download-source-sink-sheets` |
| **Neo4j** | `just neo4j-start`, `just neo4j-clear`, `just neo4j-status` |
| **Edge Patterns** | `just edge-patterns-merged`, `just edge-patterns-by-source` |
| **Cleanup** | `just clean-output-kgx`, `just clean-edge-patterns`, `just clean-all` |

---

## QA & Development

| Target | Description | Time |
|--------|-------------|------|
| `qa` | Run all QA checks (linting, tests, schema, docs, smoke tests) | ~30s |
| `ci` | Alias for `qa` | ~30s |
| `lint-fast` | Run only linting checks (skips tests/docs/schema) | ~5s |
| `test` | Run all tests | ~2s |
| `test-verbose` | Run tests with verbose output and HTML coverage report | ~10s |
| `lint` | Run linting | ~5s |

## Project Management

| Target | Description |
|--------|-------------|
| `setup` | Initialize a new project (for projects not yet under version control) |
| `install` | Install project dependencies |
| `update` | Updates project template and LinkML package |
| `clean` | Clean all generated files |

## Model Development

| Target | Description |
|--------|-------------|
| `gen-python` | Generate the Python data models (dataclasses & pydantic) |
| `gen-project` | Generate project files including Python data model |
| `gen-doc` | Generate markdown documentation for the schema |
| `site` | (Re-)Generate project and documentation locally |
| `testdoc` | Build docs and run test server |
| `deploy` | Deploy documentation site to GitHub Pages |

---

## Data Loading

### Google Sheets

| Target | Description | Requirements |
|--------|-------------|--------------|
| `download-sheets` | Download all tabs from BER CMM Google Sheet as TSV | Google Sheets API credentials |
| `download-sheet {tab}` | Download specific tab(s) from Google Sheet | Google Sheets API credentials |

### MediaDive

| Target | Description | Time |
|--------|-------------|------|
| `load-mediadive` | Load MediaDive base data (media, solutions, ingredients) into MongoDB | ~10 sec |
| `load-mediadive-details` | Fetch detailed MediaDive data (media, solutions, ingredients, strains) | 3-4+ hours |
| `load-bacdive` | Load BacDive strain data into MongoDB | Varies |

### MongoDB Maintenance

| Target | Description |
|--------|-------------|
| `mediadive-backup` | Backup MediaDive MongoDB to `data/mongodb_backups/{date}/` |
| `mediadive-restore {date}` | Restore MediaDive MongoDB from backup (e.g., `just mediadive-restore 20251219`) |
| `mediadive-merge-references` | Merge reference field from media into media_details |
| `mediadive-merge-bacdive-ids` | Merge bacdive_id from medium_strains into strains |
| `mediadive-drop-redundant` | Drop redundant collections (runs merge first) |

---

## KGX Export

### MediaDive KGX

| Target | Description | Output |
|--------|-------------|--------|
| `mediadive-kgx-export` | Export MediaDive data to KGX format | `output/kgx/mediadive_*.tsv` |
| `mediadive-kgx-clean-export` | Clean and re-export MediaDive KGX files | `output/kgx/mediadive_*.tsv` |

### Google Sheets KGX

| Target | Description | Output |
|--------|-------------|--------|
| `strains-kgx-from-curies {input} {id_field} [output_dir]` | Generate KGX for strains from CURIEs | `output/kgx/strains_from_curies/` |
| `strains-kgx-sample {input} {id_field} {n}` | Generate KGX for sampled strains | `output/kgx/strains_sample/` |
| `chemicals-kgx-from-curies {input} {id_field} [output_dir]` | Generate KGX for chemicals from CURIEs | `output/kgx/chemicals_from_curies/` |
| `kgx-export-growth` | Export growth preferences to KGX format | `output/kgx/growth_*.tsv` |
| `kgx-export-media-ingredients` | Export media-ingredient edges to KGX format | `output/kgx/media_ingredients_*.tsv` |
| `kgx-export-all` | Export all (strains, growth, media ingredients) | `output/kgx/*.tsv` |

### Enrichment Pipeline

| Target | Description |
|--------|-------------|
| `ingredients-to-kgx` | Full pipeline: download sheets -> dedupe -> enrich -> export KGX |
| `enrich-to-store` | Multi-source enrichment storing in DuckDB |
| `enrich-and-export-kgx` | Multi-source enrichment with KGX export |
| `enrich-to-store-test {n}` | Test enrichment with first N ingredients (default: 5) |
| `export-kgx` | Export existing EnrichmentStore to KGX format |
| `enrich-ingredients {input} {output}` | Enrich ingredients with PubChem data |

---

## KGX Operations

| Target | Description | Output |
|--------|-------------|--------|
| `kgx-validate` | Validate KGX files against Biolink Model | `output/kgx/validation_report.json` |
| `kgx-validate-all` | Validate all KGX files | `output/kgx/validation_report.json` |
| `kgx-to-rdf` | Transform KGX to N-Triples RDF format | `output/kgx/*.nt` |
| `kgx-to-jsonl` | Transform KGX to JSONL format | `output/kgx/*.jsonl` |
| `kgx-merge` | Merge multiple KGX graphs into one | `output/kgx/merged_*` |
| `kgx-graph-summary` | Generate graph summary statistics | `output/kgx/summary.yaml`, `meta-kg.json` |

### Edge Pattern Analysis

| Target | Description | Output |
|--------|-------------|--------|
| `edge-patterns-merged` | Edge patterns from merged KGX (no source breakdown) | `output/edge_patterns/edge_patterns_merged.tsv` |
| `edge-patterns-by-source` | Edge patterns with source breakdown | `output/edge_patterns/edge_patterns_by_source.tsv` |

---

## Neo4j

### Lifecycle

| Target | Description |
|--------|-------------|
| `neo4j-start` | Start local Neo4j instance in Docker |
| `neo4j-stop` | Stop Neo4j container (preserves data) |
| `neo4j-clean` | Remove Neo4j data volume (full reset) |
| `neo4j-clear` | Clear Neo4j database (keeps container running) |
| `neo4j-status` | Check Neo4j container status |

### Data Loading

| Target | Description | Labels | List Handling |
|--------|-------------|--------|---------------|
| `neo4j-upload-kgx` | Upload using `kgx neo4j-upload` tool | Generic "Node" | Proper arrays |
| `neo4j-upload-custom` | Upload using custom Python loader | GrowthMedium, Strain, etc. | Pipe-delimited strings |

**Recommendation:** Use `neo4j-upload-kgx` for proper list handling (xref, synonym as arrays).

---

## Cleanup

| Target | Description | Safety |
|--------|-------------|--------|
| `clean-output-kgx` | Clean all KGX outputs | Safe - only removes `output/kgx/` |
| `clean-kgx-bacdive` | Clean BacDive KGX outputs only | Safe - only removes BacDive JSONL files |
| `clean-edge-patterns` | Clean edge pattern outputs | Safe - only removes `output/edge_patterns/` |
| `clean-enrichment-db` | Clean enrichment database | Safe - keeps source data |
| `clean-cache-all` | Clean all API caches (NCBI, PubChem, CAS) | Safe - will re-fetch on next use |
| `clean-all-sheets` | Clean all Google Sheets TSVs | Need to re-download |
| `clean-all` | Clean everything including downloaded sheets | **Warning** - need to re-download |
| `clean` | Clean all generated files | Removes generated Python/docs |

---

## Semantic Search

| Target | Description |
|--------|-------------|
| `build-ncbitaxon {db_path}` | Build NCBITaxon ChromaDB for semantic search |
| `codify-strains {input} {output} {chroma_path}` | Codify strains using NCBITaxon ChromaDB |

---

## Environment Variables

Many targets require environment variables. Set these in `.env`:

```bash
# Google Sheets
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service_account.json

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# BacDive (optional)
BACDIVE_EMAIL=your@email.com
BACDIVE_PASSWORD=your-password

# CAS API (optional)
CAS_API_KEY=your-cas-key
```
