# Citation Network Paper Collector

A tool that explores citation networks starting from seed papers, collects key papers, and stores them in the kg2 knowledge graph.

## Installation

```bash
uv sync
```

Create `.env` file:
```
S2_API_KEY=your_semantic_scholar_api_key  # optional, for higher rate limits
OPENAI_API_KEY=your_openai_api_key        # required for enrichment
POLITE_EMAIL=your@email.com               # optional, for CrossRef/OpenAlex polite pool
```

## Usage

```bash
./kg2 init -s "ARXIV:1706.03762" -s "DOI:10.1234/example"
./kg2 run
./kg2 status
./kg2 fetch-contexts
./kg2 enrich
./kg2 link
./kg2 backfill-abstracts
./kg2 organize-concepts
```

The `kg2` wrapper script handles directory switching, so it works from anywhere.

### Options

```bash
# Global options
--db TEXT          # SQLite DB path (default: ./papers.db)
--repo TEXT        # GraphDB repository name (default: kg2)
--api-key TEXT     # Semantic Scholar API key
-q, --quiet        # Suppress progress output

# init
-s, --seeds TEXT   # Seed paper IDs (repeatable, required)
--max-papers INT   # Maximum papers to collect (default: 500)

# run
--max INT          # Maximum iterations

# enrich / link
--max INT          # Maximum papers to process
-w, --watch        # Poll for new papers instead of exiting
--poll INT         # Poll interval in seconds (default: 10)
--workers INT      # Number of parallel workers (default: 1)

# backfill-abstracts
--max INT          # Maximum papers to check

# organize-concepts
--skip-llm         # Only auto-merge (>= 0.95), skip LLM analysis
--workers INT      # Number of parallel workers (default: 1)
--cache-stats      # Show embedding cache statistics
```

### Seed ID Formats

Formats supported by Semantic Scholar API:
- `ARXIV:1706.03762`
- `DOI:10.1234/example`
- `CorpusId:12345678`
- Semantic Scholar Paper ID (40-char hex)

## How It Works

1. **init**: Fetch seed papers, save to SQLite and kg2, build initial queue
2. **run**: Process queue by score - fetch metadata, filter, insert to kg2
3. **fetch-contexts**: Get citation intents/snippets from Semantic Scholar
4. **enrich**: Extract concepts and claims with LLM
5. **link**: Find claim relations between papers
6. **organize-concepts**: Merge duplicate concepts and add missing relations (broader/partOf/dependsOn)

### Scoring

Papers are prioritized by:
- Age-normalized citation count (20%)
- Seed connection strength (30%)
- Connection density with collected papers (15%)
- Bidirectional citation bonus (10%)
- Semantic similarity to seeds (25%)
- Citation impact factor (multiplier)

## Concurrent Execution

Four processes can run in parallel:

```bash
./kg2 run                          # collect papers
./kg2 fetch-contexts --watch       # fetch citation contexts
./kg2 enrich --watch --workers 3   # enrich with concepts/claims
./kg2 link --watch --workers 2     # find claim relations
```

The `--workers N` flag spawns N worker processes that safely process papers in parallel using atomic database claims.

## Data

SQLite tables:
- `papers`: Paper metadata and processing state
- `queue`: Candidates for collection
- `config`: Configuration (seeds, max_papers)
- `pending_cites`: Citation edges to create in kg2
- `citation_contexts`: Citation intents and text snippets
- `paper_embeddings`, `claim_embeddings`, `concept_embeddings`: Embedding vectors
- `seed_centroid`: Centroid of seed paper embeddings

## Reprocessing

```bash
# Reset enrichment and linking
sqlite3 papers.db "UPDATE papers SET llm_enriched_at = NULL, link_checked_at = NULL"

# Reset linking only
sqlite3 papers.db "UPDATE papers SET link_checked_at = NULL"

# Reset skipped papers after backfilling abstracts
sqlite3 papers.db "UPDATE papers SET llm_enriched_at = NULL, link_checked_at = NULL, enrichment_skip_reason = NULL WHERE enrichment_skip_reason = 'no_abstract' AND abstract IS NOT NULL"
```

Note: Resetting enrichment requires resetting linking too. Existing kg2 data is not deleted.

## Development

```bash
uv run pytest              # run from script/ directory
uv run ruff check .        # lint
```

Mock clients in `mocks.py` enable testing without external APIs.
