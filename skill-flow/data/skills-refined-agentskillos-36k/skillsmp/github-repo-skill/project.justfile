## Add your own just recipes here. This is imported by the main justfile.
## Note: .env is loaded via `set dotenv-load` in main justfile

# =============================================================================
# QA TARGETS
# =============================================================================

# Run all QA checks (linting, tests, schema, docs, smoke tests) - nothing runs twice
qa:
  uv run pre-commit run --all-files --hook-stage manual
  @echo "✓ Full QA complete"

# Alias for CI (same as qa)
ci: qa

# Run only linting checks (fast, skips tests/docs/schema)
lint-fast:
  uv run pre-commit run --all-files

# Run tests with verbose output and HTML coverage report
test-verbose:
  uv run pytest -m "" --cov --cov-report=term-missing --cov-report=html -v --durations=10

# =============================================================================
# variables
# =============================================================================

# Google Sheets download destinations
#
# Experimentalist sheet: shared and (unfortunately) usable as both source and sink.
experimentalist_source_sink_sheet_id := "1h-kOdyvVb1EJPqgTiklTN9Z8br_8bP8KGmxA19clo7Q"
experimentalist_source_sink_dir := "data/private/experimentalist-source-sink-downloads"


# Normalized KGX sheet: restricted and intended to be read-only in code (hand curated).
normalized_kgx_sheet_id := "1mKcHpdL70EJdmqmXile7lCHzDUws5nxYNVNo058HKrQ"
normalized_kgx_dir := "data/private/normalized-kgx-downloads"

cache_root := "cache"
pubchem_cache_dir := "{{cache_root}}/pubchem"
ncbi_cache_dir := "{{cache_root}}/ncbi"
cas_cache_dir := "{{cache_root}}/cas"

# BacDive MongoDB defaults
# Override: just bacdive_max_id=300 bacdive_database=bdtest bacdive_collection=bdtest load-bacdive
bacdive_max_id := "200000"
bacdive_min_id := "1"
bacdive_database := "bacdive"
bacdive_collection := "strains"

# =============================================================================
# cleaning TARGETS
# =============================================================================


# Clean KGX outputs only
# SAFE: Only removes KGX files, keeps other outputs
clean-output-kgx:
  rm -rf output/kgx/
  @echo "✓ Cleaned KGX outputs"

# Clean CAS cache (ingredient enrichment data)
# Use this to force fresh fetches from CAS API
# SAFE: Only removes cached CAS API responses
clean-cache-cas:
  rm -rf {{cas_cache_dir}}/
  @echo "✓ Cleaned CAS cache"

# Clean NCBI taxonomy cache (synonyms, linkouts)
# Use this when NCBI data format changes or to force fresh fetches
# SAFE: Only removes cached NCBI API responses, will be re-fetched on next use
clean-cache-ncbi:
  rm -rf {{ncbi_cache_dir}}/
  @echo "✓ Cleaned NCBI taxonomy cache"

# Clean PubChem cache (ingredient enrichment data)
# Use this to force fresh fetches from PubChem API
# SAFE: Only removes cached PubChem API responses
clean-cache-pubchem:
  rm -rf {{pubchem_cache_dir}}/
  @echo "✓ Cleaned PubChem cache"

# Clean all caches (NCBI, PubChem, CAS)
# Use this for a complete fresh start with all external APIs
clean-cache-all: clean-cache-ncbi clean-cache-pubchem clean-cache-cas
  @echo "✓ Cleaned all caches"

# Clean enrichment outputs (DuckDB store, KGX files, intermediate files)
# SAFE: Only removes generated files, not downloaded source data
clean-enrichment-db:
  rm -f data/enrichment.duckdb
  @echo "✓ Cleaned enrichment outputs"

# Clean everything including downloaded sheets (full reset)
# WARNING: Will need to re-download from Google Sheets
clean-all: clean clean-output-kgx clean-edge-patterns clean-cache-all clean-enrichment-db clean-all-sheets
  @echo "✓ Cleaned all data (sheets will be re-downloaded)"


# Delete all TSVs downloaded from the experimentalist source/sink sheet
clean-source-sink-sheets:
  rm -f {{experimentalist_source_sink_dir}}/*.tsv
  @echo "✓ Cleaned experimentalist source/sink TSVs"

# Delete all TSVs downloaded from the normalized KGX sheet
clean-normalized-kgx-sheets:
  rm -f {{normalized_kgx_dir}}/*.tsv
  @echo "✓ Cleaned normalized KGX TSVs"

# Clean all Google Sheets TSVs
clean-all-sheets: clean-source-sink-sheets clean-normalized-kgx-sheets
  @echo "✓ Cleaned all Google Sheets TSVs"

# Clean and re-export MediaDive KGX files
mediadive-kgx-clean-export:
  rm -f output/kgx/mediadive_nodes.tsv output/kgx/mediadive_edges.tsv
  uv run python -m cmm_ai_automation.scripts.export_mediadive_kgx
  @echo "✓ Cleaned and re-exported MediaDive to KGX"

# Remove Neo4j data volume (full reset)
neo4j-clean: neo4j-stop
  docker volume rm cmm-neo4j-data || true
  @echo "✓ Neo4j data volume removed"

# Clear Neo4j database
# REQUIRES: Neo4j running
neo4j-clear:
  uv run python -m cmm_ai_automation.scripts.neo4j_clear

# =============================================================================
# FUNCTIONAL TARGETS - Data Pipeline Operations
# =============================================================================

# Generate KGX nodes and edges for strains from a file containing strain id CURIEs
# Fetches from BacDive MongoDB and/or NCBI API, creates in_taxon edges to species
# REQUIRES: BacDive MongoDB (for bacdive: CURIEs), NETWORK: yes (NCBI API)
# Use bacdive_database/bacdive_collection variables to override MongoDB location
strains-kgx-from-curies input='data/private/normalized-kgx-downloads/growth_kgx_nodes.tsv' id_field='id' output_dir='output/kgx/strains_from_curies':
  @mkdir -p {{output_dir}}
  uv run python -m cmm_ai_automation.scripts.strains_kgx_from_curies \
    --input {{input}} \
    --id-field {{id_field}} \
    --database {{bacdive_database}} \
    --collection {{bacdive_collection}} \
    --output-dir {{output_dir}}
  @echo "✓ Exported strains to {{output_dir}}/"

# Generate KGX nodes and edges for chemicals from a file of CURIEs
# Input file must have a column with CHEBI:, PUBCHEM.COMPOUND:, doi:, or uuid: CURIEs
# Fetches from ChEBI and PubChem APIs; doi/uuid entries are not passed forward
# REQUIRES: ChEBI API, PubChem API, NETWORK: yes
chemicals-kgx-from-curies input='data/private/normalized-kgx-downloads/medium_kgx_nodes.tsv' id_field='id' output_dir='output/kgx/chemicals_from_curies':
    @mkdir -p "{{output_dir}}"
    uv run python -m cmm_ai_automation.scripts.chemicals_kgx_from_curies \
      --input "{{input}}" \
      --id-field "{{id_field}}" \
      --output-dir "{{output_dir}}"
    @echo "✓ Exported chemicals to {{output_dir}}/"

# Generate KGX for chemicals with sampling (for testing)
chemicals-kgx-sample input='data/private/normalized-kgx-downloads/medium_kgx_nodes.tsv' id_field='id' n='10' output_dir='output/kgx/chemicals_sample':
  @mkdir -p "{{output_dir}}"
  uv run python -m cmm_ai_automation.scripts.chemicals_kgx_from_curies \
    --input "{{input}}" \
    --id-field "{{id_field}}" \
    --sample-n "{{n}}" \
    --output-dir "{{output_dir}}"
  @echo "✓ Exported sampled chemicals to {{output_dir}}/"

# =============================================================================
# Google Sheets TARGETS
# =============================================================================

# Download all tabs from the experimentalist source/sink sheet
# REQUIRES: Google Sheets API credentials, NETWORK: yes, WRITES: {{experimentalist_source_sink_dir}}/*.tsv
download-source-sink-sheets:
  @echo "Spreadsheet ID: {{experimentalist_source_sink_sheet_id}}"
  @echo "Output dir:     {{experimentalist_source_sink_dir}}"
  uv run download-sheets --spreadsheet "{{experimentalist_source_sink_sheet_id}}" --output-dir {{experimentalist_source_sink_dir}}

# Download normalized KGX tabs from the restricted sheet
# REQUIRES: Google Sheets API credentials, NETWORK: yes, WRITES: {{normalized_kgx_dir}}/*.tsv
download-normalized-kgx-sheets:
  @echo "Spreadsheet ID: {{normalized_kgx_sheet_id}}"
  @echo "Output dir:     {{normalized_kgx_dir}}"
  uv run download-sheets --spreadsheet "{{normalized_kgx_sheet_id}}" --output-dir {{normalized_kgx_dir}} \
    --tabs growth_kgx_nodes \
    --tabs growth_kgx_edges \
    --tabs medium_kgx_nodes \
    --tabs medium_kgx_edges

# =============================================================================
# MediaDive TARGETS
# =============================================================================


# Load MediaDive base data (media, solutions, ingredients) into MongoDB
# REQUIRES: MongoDB running on localhost:27017, NETWORK: yes, DESTRUCTIVE: drops/recreates collections
# TIME: ~10 seconds (3 bulk API calls)
load-mediadive:
  uv run python -m cmm_ai_automation.scripts.load_mediadive_mongodb

# Fetch detailed MediaDive data into MongoDB (media, solutions, ingredients, strains)
# REQUIRES: MongoDB with mediadive.media collection, NETWORK: yes, DESTRUCTIVE: drops/recreates detail collections
# TIME: 3-4+ hours (~64,000 API calls; 0.1s rate limit + API latency)
load-mediadive-details:
  uv run python -m cmm_ai_automation.scripts.load_mediadive_details

# Merge reference field from media into media_details.medium.reference
# REQUIRES: Both media and media_details collections populated
# Run this before dropping the media collection
mediadive-merge-references:
  mongosh mediadive --eval 'let n=0; db.media.find({reference: {$ne: null}}).forEach(doc => { if(db.media_details.updateOne({_id: doc.id}, {$set: {"medium.reference": doc.reference}}).modifiedCount) n++; }); print("Merged", n, "references")'

# Merge bacdive_id from medium_strains into strains collection
# REQUIRES: Both medium_strains and strains collections populated
# Run this before dropping medium_strains
mediadive-merge-bacdive-ids:
  mongosh mediadive --eval 'const m = {}; db.medium_strains.find().forEach(doc => doc.strains.forEach(s => { if (s.bacdive_id) m[s.id] = s.bacdive_id; })); let u = 0; Object.entries(m).forEach(([id, bid]) => { if (db.strains.updateOne({_id: parseInt(id)}, {$set: {bacdive_id: bid}}).modifiedCount) u++; }); print("Merged", u, "bacdive_ids into strains")'

# Drop redundant MediaDive collections (ingredients, media, solutions, medium_strains)
# Runs merge targets first to preserve unique data
mediadive-drop-redundant: mediadive-merge-references mediadive-merge-bacdive-ids
  mongosh mediadive --eval 'db.ingredients.drop(); db.solutions.drop(); db.media.drop(); db.medium_strains.drop(); print("Dropped: ingredients, solutions, media, medium_strains")'

# Export MediaDive data to KGX format
# REQUIRES: MediaDive MongoDB populated, WRITES: output/kgx/mediadive_nodes.tsv, output/kgx/mediadive_edges.tsv
mediadive-kgx-export:
  uv run python -m cmm_ai_automation.scripts.export_mediadive_kgx \
    --output output/kgx/mediadive/ \
    --mongodb-uri "mongodb://localhost:27017"
  @echo "✓ Exported MediaDive to KGX"


# Backup MediaDive MongoDB to data/mongodb_backups/{date}/
# SAFE: read-only, creates timestamped backup
mediadive-backup:
  mongodump --db mediadive --out data/mongodb_backups/$(date +%Y%m%d)
  @echo "✓ Backup saved to data/mongodb_backups/$(date +%Y%m%d)/mediadive/"

# Restore MediaDive MongoDB from a backup
# DESTRUCTIVE: drops and recreates all collections
# Usage: just mediadive-restore 20251219
mediadive-restore date:
  mongorestore --db mediadive --drop data/mongodb_backups/{{date}}/mediadive/
  @echo "✓ Restored from data/mongodb_backups/{{date}}/mediadive/"


# =============================================================================
# ChromaDB TARGETS
# =============================================================================

# Build NCBITaxon ChromaDB for semantic search
# REQUIRES: NCBITaxon OWL file, OpenAI API key, EXPENSIVE: OpenAI embeddings, WRITES: ChromaDB
build-ncbitaxon db_path:
  uv run python -m cmm_ai_automation.scripts.build_ncbitaxon_chromadb --db-path {{db_path}}

# =============================================================================
# BacDive TARGETS
# =============================================================================

# Load BacDive strain data into MongoDB by iterating over ID range
# REQUIRES: MongoDB running, BACDIVE_EMAIL and BACDIVE_PASSWORD in .env
# NETWORK: yes (BacDive API)
# TIME: Several hours (~100k IDs with rate limiting, ~56% have data)
# WRITES: MongoDB bacdive.strains collection (default)
#
# Examples:
#   just load-bacdive                                              # Full load (1-200000)
#   just bacdive_max_id=300 load-bacdive                           # First 300 IDs
#   just bacdive_max_id=300 bacdive_database=test load-bacdive     # Custom database
load-bacdive:
  uv run python -m cmm_ai_automation.scripts.load_bacdive_mongodb \
    --max-id {{bacdive_max_id}} \
    --min-id {{bacdive_min_id}} \
    --database {{bacdive_database}} \
    --collection {{bacdive_collection}}
# Codify strains using NCBITaxon ChromaDB semantic search
# REQUIRES: ChromaDB built, input TSV, NETWORK: OpenAI API, WRITES: output TSV

# Export BacDive strains directly from MongoDB to KGX JSON Lines format
# REQUIRES: BacDive MongoDB populated (via load-bacdive), NETWORK: no (MongoDB local)
# WRITES: output/kgx/bacdive/cmm_strains_bacdive_nodes.jsonl, output/kgx/bacdive/cmm_strains_bacdive_edges.jsonl
# Use bacdive_database/bacdive_collection variables to override MongoDB location
kgx-export-bacdive limit='':
  @mkdir -p output/kgx/bacdive
  uv run python -m cmm_ai_automation.scripts.export_bacdive_kgx \
    --database {{bacdive_database}} \
    --collection {{bacdive_collection}} \
    {{ if limit != '' { '--limit ' + limit } else { '' } }}
  @echo "✓ BacDive MongoDB export complete"

# Clean BacDive KGX output files only
clean-kgx-bacdive:
  rm -rf output/kgx/bacdive
  @echo "✓ Cleaned BacDive KGX outputs"

# =============================================================================
# NEO4J TARGETS - Local Graph Database
# =============================================================================

# Start local Neo4j instance (Docker)
# REQUIRES: Docker running, NETWORK: pulls neo4j image if needed
# ACCESS: http://localhost:7474 (browser), bolt://localhost:7687 (driver)
# CREDS: Set NEO4J_USER and NEO4J_PASSWORD in .env
neo4j-start:
  #!/usr/bin/env bash
  set -a; source .env; set +a
  echo "Starting Neo4j container..."
  docker run -d --name cmm-neo4j \
    -p 7474:7474 -p 7687:7687 \
    -v cmm-neo4j-data:/data \
    -e NEO4J_AUTH=${NEO4J_USER:-neo4j}/${NEO4J_PASSWORD:-neo4j} \
    -e NEO4J_PLUGINS='["apoc"]' \
    neo4j:5
  echo "✓ Neo4j starting at http://localhost:7474"
  echo "  Credentials from .env (NEO4J_USER/NEO4J_PASSWORD)"
  echo "  Wait ~30s for startup, then run: just neo4j-upload"

# Check Neo4j status
neo4j-status:
  @docker ps --filter name=cmm-neo4j || echo "Neo4j not running"

# Upload MediaDive KGX to Neo4j using custom loader
# PROS: Custom labels (GrowthMedium, Strain, Ingredient, Solution)
# CONS: List properties stored as pipe-delimited strings
# REQUIRES: Neo4j running, MediaDive KGX files exist
neo4j-upload-custom:
  uv run python -m cmm_ai_automation.scripts.neo4j_load

# Upload MediaDive KGX to Neo4j using kgx neo4j-upload
# PROS: Proper list handling (xref, synonym as arrays)
# CONS: Generic Node labels only
# REQUIRES: Neo4j running, MediaDive KGX files exist
neo4j-upload-kgx:
  #!/usr/bin/env bash
  set -a; source .env; set +a
  echo "Uploading MediaDive KGX to Neo4j via kgx..."
  uv run kgx neo4j-upload \
    -i tsv \
    -l ${NEO4J_URI:-bolt://localhost:7687} \
    -u ${NEO4J_USER:-neo4j} \
    -p ${NEO4J_PASSWORD:-neo4j} \
    output/kgx/mediadive_nodes.tsv output/kgx/mediadive_edges.tsv
  echo "✓ Upload complete - browse at http://localhost:7474"

# Stop Neo4j container (preserves data)
neo4j-stop:
  docker stop cmm-neo4j || true
  docker rm cmm-neo4j || true
  @echo "✓ Neo4j stopped (data preserved in volume)"

# =============================================================================
# KGX Merge TARGETS
# =============================================================================

# Full KGX pipeline: clean, download, enrich, merge
# This is the main entry point for rebuilding the normalized KGX graph from scratch
# REQUIRES: Google Sheets API credentials, BacDive MongoDB, ChEBI/PubChem/NCBI APIs
# NETWORK: yes
# WRITES:
# - data/private/normalized-kgx-downloads/*.tsv (downloaded sheets)
# - output/kgx/strains_from_curies/*.tsv (enriched strains)
# - output/kgx/chemicals_from_curies/*.tsv (enriched chemicals)
# - output/kgx/merged/merged_nodes.tsv, merged_edges.tsv (final merged graph)
kgx-rebuild-all: clean-normalized-kgx-sheets clean-output-kgx download-normalized-kgx-sheets strains-kgx-from-curies chemicals-kgx-from-curies kgx-merge-all
  @echo "✓ Full KGX pipeline complete"
  @echo "  Output: output/kgx/merged/merged_nodes.tsv"
  @echo "  Output: output/kgx/merged/merged_edges.tsv"

# Merge normalized KGX sheets with strains/chemicals KGX exports into one graph
# WRITES:
# - output/kgx/merged/merged_nodes.tsv
# - output/kgx/merged/merged_edges.tsv
kgx-merge-all:
  @mkdir -p output/kgx/merged
  uv run kgx merge \
    --merge-config config/kgx_merge_config.yaml \
    --source normalized_medium \
    --source normalized_growth \
    --source strains_from_curies \
    --source chemicals_from_curies \
    --destination merged_tsv
  @echo "✓ Wrote output/kgx/merged/merged_nodes.tsv and output/kgx/merged/merged_edges.tsv"

# =============================================================================
# KGX Edge Pattern Analysis TARGETS
# =============================================================================

# Default paths for kg-microbe analysis
kg_microbe_merged := "../kg-microbe/data/merged"
kg_microbe_transformed := "../kg-microbe/data/transformed"
edge_patterns_output := "output/edge_patterns"

# Extract edge patterns from merged KGX output (source breakdown NOT preserved)
# For *_nodes.tsv and *_edges.tsv in a flat directory
# REQUIRES: Merged KGX files exist
# WRITES: output/edge_patterns/edge_patterns_merged.tsv
# Override with: just kg_microbe_merged=/custom/path edge-patterns-merged
edge-patterns-merged:
  @mkdir -p "{{edge_patterns_output}}"
  uv run python -m cmm_ai_automation.scripts.edge_patterns_merged "{{kg_microbe_merged}}" > "{{edge_patterns_output}}/edge_patterns_merged.tsv"
  @echo "✓ Wrote {{edge_patterns_output}}/edge_patterns_merged.tsv"

# Extract edge patterns from transformed data (source breakdown IS preserved)
# For <source>/nodes.tsv and <source>/edges.tsv subdirectories
# REQUIRES: Transformed KGX directories exist
# WRITES: output/edge_patterns/edge_patterns_by_source.tsv
# Override with: just kg_microbe_transformed=/custom/path edge-patterns-by-source
edge-patterns-by-source:
  @mkdir -p "{{edge_patterns_output}}"
  uv run python -m cmm_ai_automation.scripts.edge_patterns_by_source "{{kg_microbe_transformed}}" > "{{edge_patterns_output}}/edge_patterns_by_source.tsv"
  @echo "✓ Wrote {{edge_patterns_output}}/edge_patterns_by_source.tsv"

# Clean all edge pattern outputs
clean-edge-patterns:
  rm -rf {{edge_patterns_output}}/
  @echo "✓ Cleaned edge patterns outputs"
