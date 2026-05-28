-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at INTEGER NOT NULL
);

-- Events: All communication + document events across channels
CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,
    timestamp INTEGER NOT NULL,
    channel TEXT NOT NULL,
    content_types TEXT NOT NULL,  -- JSON array: ["text"], ["text", "image"]
    content TEXT,
    direction TEXT NOT NULL,      -- sent, received, observed, created, updated, deleted
    thread_id TEXT,
    reply_to TEXT,
    source_adapter TEXT NOT NULL,
    source_id TEXT NOT NULL,
    metadata_json TEXT,           -- Optional structured metadata (AIX tool calls, files, etc.)
    UNIQUE(source_adapter, source_id)
);

CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_channel ON events(channel);
CREATE INDEX IF NOT EXISTS idx_events_thread ON events(thread_id);

-- Document heads: Stable pointers for document-style events (skills, docs, memory, tools)
CREATE TABLE IF NOT EXISTS document_heads (
    doc_key TEXT PRIMARY KEY,           -- stable id (ex: "skill:gog")
    channel TEXT NOT NULL,              -- "skill", "doc", "memory", "tool"
    current_event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    content_hash TEXT NOT NULL,
    title TEXT,
    description TEXT,
    metadata_json TEXT,
    updated_at INTEGER NOT NULL,
    retrieval_count INTEGER NOT NULL DEFAULT 0,
    last_retrieved_at INTEGER
);

CREATE INDEX IF NOT EXISTS idx_document_heads_channel ON document_heads(channel);
CREATE INDEX IF NOT EXISTS idx_document_heads_event ON document_heads(current_event_id);

-- Retrieval log: Optional per-query document retrieval tracking
CREATE TABLE IF NOT EXISTS retrieval_log (
    id TEXT PRIMARY KEY,
    doc_key TEXT NOT NULL REFERENCES document_heads(doc_key) ON DELETE CASCADE,
    event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    query_text TEXT,
    score REAL,
    retrieved_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_retrieval_log_doc ON retrieval_log(doc_key);
CREATE INDEX IF NOT EXISTS idx_retrieval_log_ts ON retrieval_log(retrieved_at);

-- Persons: People with unified identity
CREATE TABLE IF NOT EXISTS persons (
    id TEXT PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    display_name TEXT,
    is_me INTEGER DEFAULT 0,
    relationship_type TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_persons_is_me ON persons(is_me);
CREATE INDEX IF NOT EXISTS idx_persons_canonical_name ON persons(canonical_name);

-- Identities: Identifiers (phone, email, handle) linked to persons
CREATE TABLE IF NOT EXISTS identities (
    id TEXT PRIMARY KEY,
    person_id TEXT NOT NULL REFERENCES persons(id) ON DELETE CASCADE,
    channel TEXT NOT NULL,
    identifier TEXT NOT NULL,
    created_at INTEGER NOT NULL,
    UNIQUE(channel, identifier)
);

CREATE INDEX IF NOT EXISTS idx_identities_person ON identities(person_id);
CREATE INDEX IF NOT EXISTS idx_identities_identifier ON identities(channel, identifier);

-- Event Participants: Who was involved in each event
CREATE TABLE IF NOT EXISTS event_participants (
    event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    person_id TEXT NOT NULL REFERENCES persons(id) ON DELETE CASCADE,
    role TEXT NOT NULL,  -- sender, recipient, cc, observer
    PRIMARY KEY (event_id, person_id, role)
);

CREATE INDEX IF NOT EXISTS idx_event_participants_event ON event_participants(event_id);
CREATE INDEX IF NOT EXISTS idx_event_participants_person ON event_participants(person_id);

-- Event state: Channel-agnostic mutable state for messages
CREATE TABLE IF NOT EXISTS event_state (
    event_id TEXT PRIMARY KEY REFERENCES events(id) ON DELETE CASCADE,
    read_state TEXT NOT NULL DEFAULT 'unknown', -- unknown|read|unread
    flagged INTEGER NOT NULL DEFAULT 0,
    archived INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'sent', -- draft|sent|received|failed|deleted|unknown
    updated_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_event_state_read_state ON event_state(read_state);
CREATE INDEX IF NOT EXISTS idx_event_state_flagged ON event_state(flagged);
CREATE INDEX IF NOT EXISTS idx_event_state_archived ON event_state(archived);

-- Event tags: Channel-agnostic tags (distinct from analysis tags table above)
CREATE TABLE IF NOT EXISTS event_tags (
    event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    tag TEXT NOT NULL,
    source TEXT NOT NULL DEFAULT 'system', -- system|user|analysis|gmail|imessage|...
    created_at INTEGER NOT NULL,
    PRIMARY KEY (event_id, tag, source)
);

CREATE INDEX IF NOT EXISTS idx_event_tags_event ON event_tags(event_id);
CREATE INDEX IF NOT EXISTS idx_event_tags_tag ON event_tags(tag);

-- Tags: Soft tags on events for categorization
CREATE TABLE IF NOT EXISTS tags (
    id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    tag_type TEXT NOT NULL,    -- topic, entity, emotion, project, context
    value TEXT NOT NULL,
    confidence REAL,
    source TEXT NOT NULL,      -- user, analysis
    created_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_tags_event ON tags(event_id);
CREATE INDEX IF NOT EXISTS idx_tags_type_value ON tags(tag_type, value);

-- Threads: Grouping containers for events (chats, email threads, channels, sessions)
CREATE TABLE IF NOT EXISTS threads (
    id TEXT PRIMARY KEY,
    channel TEXT NOT NULL,
    name TEXT,
    source_adapter TEXT NOT NULL,
    source_id TEXT NOT NULL,
    parent_thread_id TEXT REFERENCES threads(id),
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    UNIQUE(source_adapter, source_id)
);

CREATE INDEX IF NOT EXISTS idx_threads_channel ON threads(channel);
CREATE INDEX IF NOT EXISTS idx_threads_parent ON threads(parent_thread_id);
CREATE INDEX IF NOT EXISTS idx_threads_name ON threads(name);

-- Attachments: Media/file metadata for events
CREATE TABLE IF NOT EXISTS attachments (
    id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,

    -- File metadata
    filename TEXT,
    mime_type TEXT,
    size_bytes INTEGER,

    -- Type hints
    media_type TEXT,                       -- "image", "video", "audio", "document", "sticker", "link"

    -- Storage location
    storage_uri TEXT,                      -- file:///path, s3://bucket/key, https://url
    storage_type TEXT,                     -- "local", "s3", "url", "inline"

    -- Content hash for dedup
    content_hash TEXT,

    -- Source tracking
    source_id TEXT,                        -- Original attachment ID from source

    -- Additional metadata
    metadata_json TEXT,                    -- Width/height for images, duration for video, etc.

    created_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_attachments_event ON attachments(event_id);
CREATE INDEX IF NOT EXISTS idx_attachments_mime ON attachments(mime_type);
CREATE INDEX IF NOT EXISTS idx_attachments_media_type ON attachments(media_type);
CREATE INDEX IF NOT EXISTS idx_attachments_hash ON attachments(content_hash);

-- Sync watermarks: Track last sync per adapter
CREATE TABLE IF NOT EXISTS sync_watermarks (
    adapter TEXT PRIMARY KEY,
    last_sync_at INTEGER NOT NULL,
    last_event_id TEXT
);

-- Adapter state: generic key/value store for adapter-specific durable state
CREATE TABLE IF NOT EXISTS adapter_state (
    adapter TEXT NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    updated_at INTEGER NOT NULL,
    PRIMARY KEY (adapter, key)
);

-- Bus events: append-only event stream for downstream automation
CREATE TABLE IF NOT EXISTS bus_events (
    seq INTEGER PRIMARY KEY AUTOINCREMENT,
    id TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    adapter TEXT,
    cortex_event_id TEXT,
    created_at INTEGER NOT NULL,
    payload_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_bus_events_created_at ON bus_events(created_at);
CREATE INDEX IF NOT EXISTS idx_bus_events_type ON bus_events(type);
CREATE INDEX IF NOT EXISTS idx_bus_events_event ON bus_events(cortex_event_id);

-- Sync jobs: Track background/resumable sync progress per adapter
CREATE TABLE IF NOT EXISTS sync_jobs (
    adapter TEXT PRIMARY KEY,
    status TEXT NOT NULL,      -- running, success, error
    phase TEXT NOT NULL,       -- sync, recent, backfill, incremental, history
    cursor TEXT,               -- opaque cursor (e.g., backfill:YYYY-MM-DD)
    started_at INTEGER,
    updated_at INTEGER NOT NULL,
    last_error TEXT,
    progress_json TEXT         -- JSON blob with counters, ETA, etc.
);

-- Merge suggestions: Proposed identity merges for user review
-- Generated from fuzzy evidence (name similarity, shared domains) rather than
-- deterministic matches (exact email/phone overlap which auto-merge).
CREATE TABLE IF NOT EXISTS merge_suggestions (
    id TEXT PRIMARY KEY,
    person1_id TEXT NOT NULL REFERENCES persons(id) ON DELETE CASCADE,
    person2_id TEXT NOT NULL REFERENCES persons(id) ON DELETE CASCADE,
    evidence_type TEXT NOT NULL,   -- name_similarity, shared_domain, co_occurrence
    evidence_json TEXT,            -- details about why this match was suggested
    confidence REAL NOT NULL,      -- 0.0-1.0 score
    person1_event_count INTEGER,   -- cached for prioritization
    person2_event_count INTEGER,
    status TEXT NOT NULL DEFAULT 'pending', -- pending, accepted, rejected, expired
    created_at INTEGER NOT NULL,
    reviewed_at INTEGER,
    UNIQUE(person1_id, person2_id)
);

CREATE INDEX IF NOT EXISTS idx_merge_suggestions_status ON merge_suggestions(status);
CREATE INDEX IF NOT EXISTS idx_merge_suggestions_confidence ON merge_suggestions(confidence DESC);
CREATE INDEX IF NOT EXISTS idx_merge_suggestions_person1 ON merge_suggestions(person1_id);
CREATE INDEX IF NOT EXISTS idx_merge_suggestions_person2 ON merge_suggestions(person2_id);

-- Person facts: Rich identity graph data extracted from episodes
-- Stores all PII and enrichment data with attribution and confidence
CREATE TABLE IF NOT EXISTS person_facts (
    id TEXT PRIMARY KEY,
    person_id TEXT NOT NULL REFERENCES persons(id) ON DELETE CASCADE,

    -- What fact
    category TEXT NOT NULL,         -- 'core_identity', 'contact', 'professional', etc.
    fact_type TEXT NOT NULL,        -- 'email_work', 'full_name', 'business_owned', etc.
    fact_value TEXT NOT NULL,       -- the actual value

    -- Confidence & Source
    confidence REAL DEFAULT 0.5,    -- 0.0-1.0
    source_type TEXT NOT NULL,      -- 'self_disclosed', 'mentioned', 'inferred', 'signature'
    source_channel TEXT,            -- 'imessage', 'gmail', etc.
    source_episode_id TEXT,    -- episode where extracted
    source_facet_id TEXT,           -- link to facets table
    evidence TEXT,                  -- quote from message

    -- Classification
    is_sensitive INTEGER DEFAULT 0,       -- SSN, medical, financial
    is_identifier INTEGER DEFAULT 0,      -- used for identity matching
    is_hard_identifier INTEGER DEFAULT 0, -- triggers instant merge consideration

    -- Timestamps
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,

    UNIQUE(person_id, category, fact_type, fact_value)
);

CREATE INDEX IF NOT EXISTS idx_person_facts_person ON person_facts(person_id);
CREATE INDEX IF NOT EXISTS idx_person_facts_type ON person_facts(category, fact_type);
CREATE INDEX IF NOT EXISTS idx_person_facts_value ON person_facts(fact_value);
CREATE INDEX IF NOT EXISTS idx_person_facts_hard_id ON person_facts(fact_type, fact_value)
    WHERE is_hard_identifier = 1;

-- Unattributed facts: Facts extracted from episodes that couldn't be attributed to a specific person
-- For example: phone numbers shared without context about whose number it is
CREATE TABLE IF NOT EXISTS unattributed_facts (
    id TEXT PRIMARY KEY,
    fact_type TEXT NOT NULL,
    fact_value TEXT NOT NULL,

    shared_by_person_id TEXT REFERENCES persons(id),
    source_event_id TEXT REFERENCES events(id),
    source_episode_id TEXT REFERENCES episodes(id),
    context TEXT,
    possible_attributions TEXT,     -- JSON array of guesses

    resolved_to_person_id TEXT REFERENCES persons(id),
    resolution_evidence TEXT,

    created_at INTEGER NOT NULL,
    resolved_at INTEGER
);

CREATE INDEX IF NOT EXISTS idx_unattributed_value ON unattributed_facts(fact_type, fact_value);
CREATE INDEX IF NOT EXISTS idx_unattributed_unresolved ON unattributed_facts(resolved_to_person_id)
    WHERE resolved_to_person_id IS NULL;

-- Candidate mentions: Third-party references without strong identifiers
CREATE TABLE IF NOT EXISTS candidate_mentions (
    id TEXT PRIMARY KEY,
    reference TEXT NOT NULL,
    known_facts_json TEXT,                -- JSON map of extracted facts
    source_episode_id TEXT REFERENCES episodes(id),
    created_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_candidate_mentions_reference ON candidate_mentions(reference);
CREATE INDEX IF NOT EXISTS idx_candidate_mentions_episode ON candidate_mentions(source_episode_id);

-- Merge events: Proposed and executed identity merges
-- Tracks both pending suggestions and completed merges with full audit trail
CREATE TABLE IF NOT EXISTS merge_events (
    id TEXT PRIMARY KEY,
    source_person_id TEXT NOT NULL REFERENCES persons(id),
    target_person_id TEXT NOT NULL REFERENCES persons(id),
    merge_type TEXT NOT NULL,        -- 'hard_identifier', 'compound', 'soft_accumulation', 'manual'

    triggering_facts TEXT,           -- JSON array of facts that caused merge
    similarity_score REAL,

    status TEXT DEFAULT 'pending',   -- 'pending', 'accepted', 'rejected', 'executed'
    auto_eligible INTEGER DEFAULT 0, -- whether this can auto-execute

    created_at INTEGER NOT NULL,
    resolved_at INTEGER,
    resolved_by TEXT                 -- 'auto' or user identifier
);

CREATE INDEX IF NOT EXISTS idx_merge_events_status ON merge_events(status);
CREATE INDEX IF NOT EXISTS idx_merge_events_persons ON merge_events(source_person_id, target_person_id);

-- Episode definitions: HOW to chunk events into episodes
CREATE TABLE IF NOT EXISTS episode_definitions (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,             -- "imessage_90min", "gmail_thread", "cross_channel_persona"

    -- Scope (what events to consider)
    channel TEXT,                          -- NULL = all channels, or specific channel

    -- Strategy
    strategy TEXT NOT NULL,                -- "time_gap", "thread", "single_event", "turn_pair", "session", "daily", "persona_pair", "custom"
    config_json TEXT NOT NULL,             -- Strategy-specific config

    description TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

-- Episodes: instances produced by applying a definition
CREATE TABLE IF NOT EXISTS episodes (
    id TEXT PRIMARY KEY,
    definition_id TEXT NOT NULL REFERENCES episode_definitions(id),

    -- Scope info (denormalized for queries)
    -- These can be NULL for cross-channel/cross-thread episodes
    channel TEXT,                          -- NULL if spans multiple channels
    thread_id TEXT REFERENCES threads(id), -- NULL if spans multiple threads

    -- Time bounds
    start_time INTEGER NOT NULL,
    end_time INTEGER NOT NULL,

    -- Stats
    event_count INTEGER NOT NULL,

    -- Convenience refs
    first_event_id TEXT,
    last_event_id TEXT,

    created_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_episodes_definition ON episodes(definition_id);
CREATE INDEX IF NOT EXISTS idx_episodes_channel ON episodes(channel);
CREATE INDEX IF NOT EXISTS idx_episodes_thread ON episodes(thread_id);
CREATE INDEX IF NOT EXISTS idx_episodes_time ON episodes(start_time, end_time);

-- Episode events: which events belong to which episode
CREATE TABLE IF NOT EXISTS episode_events (
    episode_id TEXT NOT NULL REFERENCES episodes(id) ON DELETE CASCADE,
    event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    position INTEGER NOT NULL,             -- order within episode (1-indexed)
    PRIMARY KEY (episode_id, event_id)
);

CREATE INDEX IF NOT EXISTS idx_episode_events_event ON episode_events(event_id);

-- Analysis types: defines what kind of analysis this is
CREATE TABLE IF NOT EXISTS analysis_types (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,           -- "convo_all_v1", "pii_extraction_v1", "summary_v1"
    version TEXT NOT NULL,               -- "1.0.0"
    description TEXT,

    -- Output type
    output_type TEXT NOT NULL,           -- "structured", "freeform"

    -- For structured outputs: what facets to extract
    -- NULL for freeform analyses
    facets_config_json TEXT,             -- Extraction rules

    -- Prompt (assuming all analyses are LLM-based)
    prompt_template TEXT NOT NULL,       -- The prompt template with {segment_text} placeholder
    model TEXT,                          -- "gemini-2.0-flash-thinking", etc.

    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

-- Analysis runs: one per (analysis_type, episode) pair
CREATE TABLE IF NOT EXISTS analysis_runs (
    id TEXT PRIMARY KEY,
    analysis_type_id TEXT NOT NULL REFERENCES analysis_types(id),
    episode_id TEXT NOT NULL REFERENCES episodes(id),

    status TEXT NOT NULL,                -- "pending", "running", "completed", "failed", "blocked"

    -- Timing
    started_at INTEGER,
    completed_at INTEGER,

    -- For freeform analyses: store the text output
    output_text TEXT,                    -- Markdown, plain text, whatever the LLM produced

    -- Error handling
    error_message TEXT,
    blocked_reason TEXT,
    retry_count INTEGER DEFAULT 0,

    created_at INTEGER NOT NULL,

    UNIQUE(analysis_type_id, episode_id)
);

CREATE INDEX IF NOT EXISTS idx_analysis_runs_type ON analysis_runs(analysis_type_id);
CREATE INDEX IF NOT EXISTS idx_analysis_runs_episode ON analysis_runs(episode_id);
CREATE INDEX IF NOT EXISTS idx_analysis_runs_status ON analysis_runs(status);

-- Facets: extracted queryable values from structured analyses
CREATE TABLE IF NOT EXISTS facets (
    id TEXT PRIMARY KEY,
    analysis_run_id TEXT NOT NULL REFERENCES analysis_runs(id) ON DELETE CASCADE,
    episode_id TEXT NOT NULL REFERENCES episodes(id) ON DELETE CASCADE,

    -- What kind of facet
    facet_type TEXT NOT NULL,            -- "entity", "topic", "emotion", "pii_email", "summary", etc.

    -- The extracted value
    value TEXT NOT NULL,                 -- "Grace", "travel", "joy", "grace@example.com"

    -- Attribution (optional - who mentioned this)
    person_id TEXT REFERENCES persons(id),

    -- Confidence/metadata
    confidence REAL,
    metadata_json TEXT,                  -- Additional context

    created_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_facets_type_value ON facets(facet_type, value);
CREATE INDEX IF NOT EXISTS idx_facets_episode ON facets(episode_id);
CREATE INDEX IF NOT EXISTS idx_facets_analysis_run ON facets(analysis_run_id);
CREATE INDEX IF NOT EXISTS idx_facets_person ON facets(person_id);
CREATE INDEX IF NOT EXISTS idx_facets_value ON facets(value);

-- ============================================
-- EMBEDDINGS (unified for all embeddable types)
-- ============================================
-- Unified embedding storage for events, episodes, entities, and relationships.
-- target_type + target_id identify what was embedded.
CREATE TABLE IF NOT EXISTS embeddings (
    id TEXT PRIMARY KEY,

    -- What is embedded
    target_type TEXT NOT NULL,           -- "event", "episode", "entity", "relationship"
    target_id TEXT NOT NULL,             -- ID of the embedded target

    -- The embedding
    model TEXT NOT NULL,                 -- "gemini-embedding-004", etc.
    embedding_blob BLOB NOT NULL,        -- Binary vector (little-endian float64 array)
    dimension INTEGER NOT NULL,          -- 768, 1024, etc.

    -- Source text hash (for change detection / re-embedding)
    source_text_hash TEXT,

    created_at INTEGER NOT NULL,

    UNIQUE(target_type, target_id, model)
);

CREATE INDEX IF NOT EXISTS idx_embeddings_target ON embeddings(target_type, target_id);
CREATE INDEX IF NOT EXISTS idx_embeddings_model ON embeddings(model);

-- FTS5 full-text search index for events
-- Provides fast BM25-based lexical search over event content
CREATE VIRTUAL TABLE IF NOT EXISTS events_fts USING fts5(
    event_id UNINDEXED,     -- Link to events table (not indexed)
    channel UNINDEXED,      -- For filtering (not indexed)
    content,                -- Main searchable content
    tokenize='porter unicode61'
);

-- FTS5 triggers to keep index in sync with events table
CREATE TRIGGER IF NOT EXISTS events_fts_insert AFTER INSERT ON events BEGIN
    INSERT INTO events_fts(event_id, channel, content)
    VALUES (new.id, new.channel, COALESCE(new.content, ''));
END;

CREATE TRIGGER IF NOT EXISTS events_fts_update AFTER UPDATE ON events BEGIN
    DELETE FROM events_fts WHERE event_id = old.id;
    INSERT INTO events_fts(event_id, channel, content)
    VALUES (new.id, new.channel, COALESCE(new.content, ''));
END;

CREATE TRIGGER IF NOT EXISTS events_fts_delete AFTER DELETE ON events BEGIN
    DELETE FROM events_fts WHERE event_id = old.id;
END;

-- ============================================
-- ENTITIES (canonical, deduplicated)
-- ============================================
-- This generalizes People/Contacts to all entity types.
-- A "Person" entity is just an entity with entity_type_id=1.
-- Entity types: 0=Entity, 1=Person, 2=Company, 3=Project, 4=Location, 5=Event, 6=Document, 7=Pet
CREATE TABLE IF NOT EXISTS entities (
    id TEXT PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    entity_type_id INTEGER NOT NULL,  -- ID from configured entity types (see §3.2)

    summary TEXT,               -- Auto-generated from relationships + episodes
    summary_updated_at TEXT,    -- When summary was last regenerated

    -- How this entity was created
    origin TEXT NOT NULL,       -- 'contact_import', 'extracted', 'manual'
    confidence REAL DEFAULT 1.0,
    merged_into TEXT REFERENCES entities(id),  -- Non-null if this entity was merged

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(entity_type_id);
CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(canonical_name);

-- ============================================
-- ENTITY ALIASES (identity resolution)
-- ============================================
-- Stores identity markers: email, phone, handles, name variants.
-- ALIASES CAN BE SHARED: family phone, team email can map to multiple entities.
-- When resolving, shared aliases require disambiguation.
-- When merging entities, reassign loser's aliases to winner.
--
-- Identity relationships (HAS_EMAIL, HAS_PHONE, HAS_HANDLE) are promoted here
-- rather than stored in the relationships table. See §4.4.
CREATE TABLE IF NOT EXISTS entity_aliases (
    id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL REFERENCES entities(id),
    alias TEXT NOT NULL,
    alias_type TEXT NOT NULL,  -- 'name', 'email', 'phone', 'handle', 'username', 'nickname'
    normalized TEXT,           -- Lowercase/cleaned for matching
    is_shared BOOLEAN DEFAULT FALSE,  -- TRUE if multiple entities share this alias
    created_at TEXT NOT NULL
    -- NOTE: No UNIQUE constraint - same alias can map to multiple entities
);

CREATE INDEX IF NOT EXISTS idx_entity_aliases_lookup ON entity_aliases(alias, alias_type);
CREATE INDEX IF NOT EXISTS idx_entity_aliases_normalized ON entity_aliases(normalized, alias_type);
CREATE INDEX IF NOT EXISTS idx_entity_aliases_entity ON entity_aliases(entity_id);

-- ============================================
-- RELATIONSHIPS (deduplicated triples with temporal bounds)
-- ============================================
-- Identity relationships (HAS_EMAIL, HAS_PHONE, HAS_HANDLE) go to entity_aliases.
-- Temporal relationships (BORN_ON, OCCURRED_ON, etc.) use target_literal.
-- All other relationships use target_entity_id.
CREATE TABLE IF NOT EXISTS relationships (
    id TEXT PRIMARY KEY,
    source_entity_id TEXT NOT NULL REFERENCES entities(id),
    target_entity_id TEXT REFERENCES entities(id),
    target_literal TEXT,  -- For temporal relationships (ISO 8601)
    relation_type TEXT NOT NULL,  -- WORKS_AT, KNOWS, CREATED, BORN_ON, etc.
    fact TEXT NOT NULL,           -- Natural language: "Tyler works at Anthropic"

    -- Bi-temporal tracking (Graphiti-style)
    valid_at TEXT,      -- When relationship became true in reality
    invalid_at TEXT,    -- When relationship stopped being true in reality
    created_at TEXT NOT NULL,  -- When system first learned about it

    -- Metadata
    confidence REAL DEFAULT 1.0,

    -- Exactly one of target_entity_id or target_literal must be set
    CHECK (
        (target_entity_id IS NOT NULL AND target_literal IS NULL) OR
        (target_entity_id IS NULL AND target_literal IS NOT NULL)
    )
);

CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships(source_entity_id);
CREATE INDEX IF NOT EXISTS idx_relationships_target ON relationships(target_entity_id);
CREATE INDEX IF NOT EXISTS idx_relationships_type ON relationships(relation_type);
CREATE INDEX IF NOT EXISTS idx_relationships_temporal ON relationships(valid_at, invalid_at);

-- Uniqueness for entity-target relationships
CREATE UNIQUE INDEX IF NOT EXISTS idx_relationships_unique_entity
ON relationships(source_entity_id, target_entity_id, relation_type, valid_at)
WHERE target_entity_id IS NOT NULL;

-- Uniqueness for literal-target relationships
CREATE UNIQUE INDEX IF NOT EXISTS idx_relationships_unique_literal
ON relationships(source_entity_id, target_literal, relation_type, valid_at)
WHERE target_literal IS NOT NULL;

-- ============================================
-- EPISODE-ENTITY MENTIONS (which episodes mention which entities)
-- ============================================
-- Junction table: many-to-many between episodes and entities.
-- Used for: entity summary generation, recency queries, channel derivation.
-- "Which channels does Tyler appear in?" = query episodes via this table.
CREATE TABLE IF NOT EXISTS episode_entity_mentions (
    episode_id TEXT NOT NULL REFERENCES episodes(id) ON DELETE CASCADE,
    entity_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    mention_count INTEGER DEFAULT 1,
    created_at TEXT NOT NULL,
    PRIMARY KEY (episode_id, entity_id)
);

CREATE INDEX IF NOT EXISTS idx_episode_entity_mentions_entity ON episode_entity_mentions(entity_id);

-- ============================================
-- EPISODE-RELATIONSHIP MENTIONS (provenance for relationships)
-- ============================================
-- Junction table: many-to-many between episodes and relationships.
-- Same relationship mentioned in 10 episodes = 10 records here.
-- Used for: frequency signals, provenance, confidence boosting.
--
-- relationship_id is NULL for identity relationships (HAS_EMAIL, HAS_PHONE, etc.)
-- that go to entity_aliases instead of the relationships table.
CREATE TABLE IF NOT EXISTS episode_relationship_mentions (
    id TEXT PRIMARY KEY,
    episode_id TEXT NOT NULL REFERENCES episodes(id) ON DELETE CASCADE,
    relationship_id TEXT REFERENCES relationships(id) ON DELETE CASCADE,  -- NULL for identity relationships
    extracted_fact TEXT NOT NULL,  -- Original extracted text (raw, pre-dedup)
    asserted_by_entity_id TEXT REFERENCES entities(id),  -- Speaker who made the statement
    source_type TEXT,  -- 'self_disclosed', 'mentioned', 'inferred'

    -- For identity relationships (HAS_EMAIL, etc.) that go to aliases instead
    target_literal TEXT,  -- The literal value (email, phone, etc.)
    alias_id TEXT REFERENCES entity_aliases(id) ON DELETE SET NULL,  -- Link to created alias

    confidence REAL,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_episode_rel_mentions_episode ON episode_relationship_mentions(episode_id);
CREATE INDEX IF NOT EXISTS idx_episode_rel_mentions_relationship ON episode_relationship_mentions(relationship_id);

-- ============================================
-- MERGE CANDIDATES (suspected duplicates for review)
-- ============================================
-- When resolution is uncertain, create a merge candidate for human review.
-- Better to have duplicates than false-merge corruption.
CREATE TABLE IF NOT EXISTS merge_candidates (
    id TEXT PRIMARY KEY,
    entity_a_id TEXT NOT NULL REFERENCES entities(id),
    entity_b_id TEXT NOT NULL REFERENCES entities(id),

    -- Scoring
    confidence REAL NOT NULL,         -- 0.0-1.0
    auto_eligible BOOLEAN DEFAULT FALSE,

    -- Evidence (why we think they match)
    reason TEXT NOT NULL,             -- 'hard_identifier', 'name_similarity', 'compound', 'soft_accumulation', 'ambiguous_resolution'
    matching_facts TEXT,              -- JSON: [{fact_type, fact_value}, ...]
    context TEXT,                     -- JSON: additional evidence
    candidates_considered TEXT,       -- JSON: top N candidates we scored (for debugging)

    -- Conflicts (reasons NOT to merge)
    conflicts TEXT,                   -- JSON: [{type, values_a, values_b}, ...]

    -- Status
    status TEXT DEFAULT 'pending',    -- 'pending', 'merged', 'rejected', 'deferred'

    -- Resolution
    created_at TEXT NOT NULL,
    resolved_at TEXT,
    resolved_by TEXT,                 -- 'auto', 'user:<id>', etc.
    resolution_reason TEXT,

    UNIQUE(entity_a_id, entity_b_id)
);

CREATE INDEX IF NOT EXISTS idx_merge_candidates_status ON merge_candidates(status);
CREATE INDEX IF NOT EXISTS idx_merge_candidates_auto ON merge_candidates(auto_eligible) WHERE status = 'pending';

-- ============================================
-- ENTITY MERGE EVENTS (audit log for entity merges)
-- ============================================
-- Tracks all entity merge operations with full audit trail.
-- This is the entity-based version (replaces person-based merge_events).
CREATE TABLE IF NOT EXISTS entity_merge_events (
    id TEXT PRIMARY KEY,
    source_entity_id TEXT NOT NULL REFERENCES entities(id),
    target_entity_id TEXT NOT NULL REFERENCES entities(id),
    merge_type TEXT NOT NULL,      -- 'hard_identifier', 'name_similarity', 'compound', 'manual', etc.
    triggering_facts TEXT,         -- JSON: facts that triggered the merge
    similarity_score REAL,
    created_at TEXT NOT NULL,
    resolved_by TEXT               -- 'auto', 'user:<id>', etc.
);

CREATE INDEX IF NOT EXISTS idx_entity_merge_events_target ON entity_merge_events(target_entity_id);

-- Insert initial schema version
INSERT OR IGNORE INTO schema_version (version, applied_at)
VALUES (20, strftime('%s', 'now'));

-- NOTE: pii_extraction_v1 analysis type is now registered via `cortex compute seed` command
-- This matches the pattern used for convo-all-v1 and is more maintainable
-- Run `cortex compute seed` after initialization to register analysis types
