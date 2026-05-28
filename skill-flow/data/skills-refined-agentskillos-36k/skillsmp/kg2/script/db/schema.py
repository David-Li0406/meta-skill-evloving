"""Database schema definition."""

SCHEMA = """
CREATE TABLE IF NOT EXISTS papers (
    id TEXT PRIMARY KEY,
    doi TEXT,
    arxiv_id TEXT,
    kg2_uri TEXT,
    title TEXT NOT NULL,
    authors JSON,
    year INTEGER,
    abstract TEXT,
    citation_count INTEGER,
    venue_id TEXT,
    venue_name TEXT,
    venue_type TEXT,
    refs JSON,
    cites JSON,
    status TEXT NOT NULL,
    collected_at TEXT NOT NULL,
    llm_enriched_at TEXT,
    llm_processing_at TEXT,
    link_checked_at TEXT,
    link_processing_at TEXT,
    raw_response JSON
);

CREATE INDEX IF NOT EXISTS idx_papers_status ON papers(status);
CREATE INDEX IF NOT EXISTS idx_papers_year ON papers(year);
CREATE INDEX IF NOT EXISTS idx_papers_doi ON papers(doi);
CREATE INDEX IF NOT EXISTS idx_papers_arxiv ON papers(arxiv_id);
CREATE INDEX IF NOT EXISTS idx_papers_llm ON papers(llm_enriched_at);
CREATE INDEX IF NOT EXISTS idx_papers_link ON papers(link_checked_at);
CREATE UNIQUE INDEX IF NOT EXISTS idx_papers_kg2_uri ON papers(kg2_uri) WHERE kg2_uri IS NOT NULL;

CREATE TABLE IF NOT EXISTS queue (
    id TEXT PRIMARY KEY,
    score REAL NOT NULL,
    source_id TEXT,
    relation TEXT,
    status TEXT NOT NULL,
    discovered_at TEXT NOT NULL,
    processed_at TEXT,
    skip_reason TEXT
);

CREATE INDEX IF NOT EXISTS idx_queue_status_score ON queue(status, score DESC);

CREATE TABLE IF NOT EXISTS config (
    key TEXT PRIMARY KEY,
    value JSON
);

CREATE TABLE IF NOT EXISTS pending_cites (
    citing_id TEXT NOT NULL,
    cited_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY (citing_id, cited_id)
);

CREATE INDEX IF NOT EXISTS idx_pending_cites_cited ON pending_cites(cited_id);

CREATE TABLE IF NOT EXISTS citation_contexts (
    citing_id TEXT NOT NULL,
    cited_id TEXT NOT NULL,
    intents JSON,
    contexts JSON,
    created_at TEXT NOT NULL,
    PRIMARY KEY (citing_id, cited_id)
);

CREATE INDEX IF NOT EXISTS idx_citation_contexts_citing ON citation_contexts(citing_id);
CREATE INDEX IF NOT EXISTS idx_citation_contexts_cited ON citation_contexts(cited_id);

CREATE TABLE IF NOT EXISTS paper_embeddings (
    paper_id TEXT PRIMARY KEY,
    embedding BLOB NOT NULL,
    model TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS claim_embeddings (
    claim_uri TEXT PRIMARY KEY,
    embedding BLOB NOT NULL,
    model TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS concept_embeddings (
    concept_uri TEXT PRIMARY KEY,
    embedding BLOB NOT NULL,
    model TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS seed_centroid (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    embedding BLOB NOT NULL,
    model TEXT NOT NULL,
    paper_ids JSON NOT NULL,
    created_at TEXT NOT NULL
);
"""

# Migrations for existing databases (safe to run multiple times)
MIGRATIONS = [
    "ALTER TABLE papers ADD COLUMN llm_processing_at TEXT",
    "ALTER TABLE papers ADD COLUMN link_processing_at TEXT",
    "CREATE INDEX IF NOT EXISTS idx_papers_llm_processing ON papers(llm_processing_at)",
    "CREATE INDEX IF NOT EXISTS idx_papers_link_processing ON papers(link_processing_at)",
    "ALTER TABLE papers ADD COLUMN enrichment_skip_reason TEXT",
    # Citation contexts table
    """CREATE TABLE IF NOT EXISTS citation_contexts (
        citing_id TEXT NOT NULL,
        cited_id TEXT NOT NULL,
        intents JSON,
        contexts JSON,
        created_at TEXT NOT NULL,
        PRIMARY KEY (citing_id, cited_id)
    )""",
    "CREATE INDEX IF NOT EXISTS idx_citation_contexts_citing ON citation_contexts(citing_id)",
    "CREATE INDEX IF NOT EXISTS idx_citation_contexts_cited ON citation_contexts(cited_id)",
    # Track whether citation contexts have been fetched for a paper
    "ALTER TABLE papers ADD COLUMN contexts_fetched_at TEXT",
    # Embedding tables
    """CREATE TABLE IF NOT EXISTS paper_embeddings (
        paper_id TEXT PRIMARY KEY,
        embedding BLOB NOT NULL,
        model TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS claim_embeddings (
        claim_uri TEXT PRIMARY KEY,
        embedding BLOB NOT NULL,
        model TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS concept_embeddings (
        concept_uri TEXT PRIMARY KEY,
        embedding BLOB NOT NULL,
        model TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS seed_centroid (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        embedding BLOB NOT NULL,
        model TEXT NOT NULL,
        paper_ids JSON NOT NULL,
        created_at TEXT NOT NULL
    )""",
]
