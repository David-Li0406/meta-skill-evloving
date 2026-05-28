-- Schema for aix - AI session intelligence
-- Updated: 2026-01-11

-- Sessions table - one row per conversation
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,              -- composerId UUID
    source TEXT NOT NULL DEFAULT 'cursor',
    project TEXT,                     -- inferred from file paths
    model TEXT,                       -- AI model used (e.g. 'claude-4.5-opus-high-thinking')
    created_at INTEGER,               -- unix timestamp in milliseconds
    message_count INTEGER DEFAULT 0,
    summary TEXT,                     -- generated later
    raw_json TEXT                     -- original JSON for re-parsing
);

-- Messages table - individual conversation turns
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,              -- bubbleId
    session_id TEXT NOT NULL REFERENCES sessions(id),
    role TEXT NOT NULL,               -- 'user', 'assistant', 'tool'
    content TEXT,
    sequence INTEGER,                 -- order in conversation
    timestamp INTEGER,
    UNIQUE(session_id, sequence)
);

-- Files referenced in sessions
CREATE TABLE IF NOT EXISTS files_referenced (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    file_path TEXT NOT NULL,
    UNIQUE(session_id, file_path)
);

-- Per-message metadata (rich Cursor fields, tool usage, etc)
CREATE TABLE IF NOT EXISTS message_metadata (
    message_id TEXT PRIMARY KEY REFERENCES messages(id),
    session_id TEXT NOT NULL REFERENCES sessions(id),
    metadata_json TEXT NOT NULL
);

-- Flattened capability usage (Cursor capability IDs per bubble)
CREATE TABLE IF NOT EXISTS message_capabilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id TEXT NOT NULL REFERENCES messages(id),
    session_id TEXT NOT NULL REFERENCES sessions(id),
    phase TEXT NOT NULL,         -- e.g. 'mutate-request', 'process-stream'
    capability INTEGER NOT NULL, -- numeric capability id
    UNIQUE(message_id, phase, capability)
);

-- Flattened linter errors captured in Cursor context
CREATE TABLE IF NOT EXISTS message_lints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id TEXT NOT NULL REFERENCES messages(id),
    session_id TEXT NOT NULL REFERENCES sessions(id),
    file_path TEXT,
    message TEXT,
    source TEXT,
    start_line INTEGER,
    start_col INTEGER,
    end_line INTEGER,
    end_col INTEGER
);

-- Per-message file references (richer than session-level aggregation)
CREATE TABLE IF NOT EXISTS message_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id TEXT NOT NULL REFERENCES messages(id),
    session_id TEXT NOT NULL REFERENCES sessions(id),
    kind TEXT NOT NULL, -- 'relevant', 'recent_location'
    file_path TEXT NOT NULL,
    line_number INTEGER,
    UNIQUE(message_id, kind, file_path, line_number)
);

-- Suggested code blocks (Cursor-provided code blocks attached to a bubble)
CREATE TABLE IF NOT EXISTS message_codeblocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id TEXT NOT NULL REFERENCES messages(id),
    session_id TEXT NOT NULL REFERENCES sessions(id),
    idx INTEGER NOT NULL,
    raw_json TEXT NOT NULL,
    UNIQUE(message_id, idx)
);

-- Embeddings table for storing vector representations (Phase 2)
CREATE TABLE IF NOT EXISTS embeddings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type TEXT NOT NULL, -- 'message', 'session', etc.
    entity_id TEXT NOT NULL,
    model TEXT NOT NULL,
    embedding_blob BLOB NOT NULL,
    dimension INTEGER NOT NULL,
    created_at INTEGER, -- unix timestamp in milliseconds
    UNIQUE(entity_type, entity_id, model)
);

-- Sync state tracking
CREATE TABLE IF NOT EXISTS sync_state (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at INTEGER
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_sessions_created ON sessions(created_at);
CREATE INDEX IF NOT EXISTS idx_sessions_project ON sessions(project);
CREATE INDEX IF NOT EXISTS idx_sessions_source ON sessions(source);
CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id);
CREATE INDEX IF NOT EXISTS idx_files_session ON files_referenced(session_id);
CREATE INDEX IF NOT EXISTS idx_message_metadata_session ON message_metadata(session_id);
CREATE INDEX IF NOT EXISTS idx_message_capabilities_session ON message_capabilities(session_id);
CREATE INDEX IF NOT EXISTS idx_message_lints_session ON message_lints(session_id);
CREATE INDEX IF NOT EXISTS idx_message_files_session ON message_files(session_id);
CREATE INDEX IF NOT EXISTS idx_message_files_path ON message_files(file_path);
CREATE INDEX IF NOT EXISTS idx_message_codeblocks_session ON message_codeblocks(session_id);

CREATE INDEX IF NOT EXISTS idx_embeddings_entity ON embeddings(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_embeddings_model ON embeddings(model);
CREATE INDEX IF NOT EXISTS idx_sessions_model ON sessions(model);

-- Migration: add model column if missing (for existing databases)
-- SQLite doesn't support ADD COLUMN IF NOT EXISTS, so we handle this in Go
