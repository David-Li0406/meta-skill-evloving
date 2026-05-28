# Ralph Agent Instructions — Comms Eve Migration

## Context

You are implementing the Eve→Comms migration. This adds:
- **threads** table (chat/channel metadata)
- **attachments** table (media metadata)
- **conversation abstraction** (flexible chunking with definitions)
- **analysis framework** (generic LLM analysis with facets)
- **embeddings** table

The detailed schema design is in `docs/SCHEMA_DESIGN_ANALYSIS.md` — **READ THIS FIRST**.

## Key Files

- `docs/SCHEMA_DESIGN_ANALYSIS.md` — **The PRD for schema design** (READ THIS)
- `scripts/ralph/prd.json` — User stories with acceptance criteria
- `scripts/ralph/progress.txt` — Learnings and patterns (check Codebase Patterns first)
- `AGENTS.md` — Codebase patterns for this project
- `internal/db/schema.sql` — Current database schema

## Your Task

1. Read `docs/SCHEMA_DESIGN_ANALYSIS.md` (the schema design spec)
2. Read `scripts/ralph/prd.json` for user stories
3. Read `scripts/ralph/progress.txt` (especially Codebase Patterns at top)
4. Pick the highest priority story where `passes: false`
5. Implement that ONE story following the schema design
6. Run `go build ./cmd/comms` to verify it compiles
7. Run `go test ./...` if tests exist
8. Update AGENTS.md with learnings about this codebase
9. Commit: `feat: [US-XXX] - [Title]`
10. Update prd.json: set `passes: true` for completed story
11. Append learnings to progress.txt

## Schema Design Summary

From `docs/SCHEMA_DESIGN_ANALYSIS.md`:

```sql
-- threads: generic containers (chats, email threads, channels)
CREATE TABLE threads (
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

-- attachments: media metadata
CREATE TABLE attachments (
    id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    filename TEXT,
    mime_type TEXT,
    size_bytes INTEGER,
    media_type TEXT,
    storage_uri TEXT,
    storage_type TEXT,
    content_hash TEXT,
    source_id TEXT,
    metadata_json TEXT,
    created_at INTEGER NOT NULL
);

-- conversation_definitions: how to chunk
CREATE TABLE conversation_definitions (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    channel TEXT,
    strategy TEXT NOT NULL,
    config_json TEXT NOT NULL,
    description TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

-- conversations: chunked groups of events
CREATE TABLE conversations (
    id TEXT PRIMARY KEY,
    definition_id TEXT NOT NULL REFERENCES conversation_definitions(id),
    channel TEXT,
    thread_id TEXT REFERENCES threads(id),
    start_time INTEGER NOT NULL,
    end_time INTEGER NOT NULL,
    event_count INTEGER NOT NULL,
    first_event_id TEXT,
    last_event_id TEXT,
    created_at INTEGER NOT NULL
);

-- conversation_events: mapping
CREATE TABLE conversation_events (
    conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    position INTEGER NOT NULL,
    PRIMARY KEY (conversation_id, event_id)
);

-- analysis_types: analysis definitions
CREATE TABLE analysis_types (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    version TEXT NOT NULL,
    description TEXT,
    output_type TEXT NOT NULL,
    facets_config_json TEXT,
    prompt_template TEXT NOT NULL,
    model TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

-- analysis_runs: execution tracking
CREATE TABLE analysis_runs (
    id TEXT PRIMARY KEY,
    analysis_type_id TEXT NOT NULL REFERENCES analysis_types(id),
    conversation_id TEXT NOT NULL REFERENCES conversations(id),
    status TEXT NOT NULL,
    started_at INTEGER,
    completed_at INTEGER,
    output_text TEXT,
    error_message TEXT,
    blocked_reason TEXT,
    retry_count INTEGER DEFAULT 0,
    created_at INTEGER NOT NULL,
    UNIQUE(analysis_type_id, conversation_id)
);

-- facets: queryable extracted values
CREATE TABLE facets (
    id TEXT PRIMARY KEY,
    analysis_run_id TEXT NOT NULL REFERENCES analysis_runs(id) ON DELETE CASCADE,
    conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    facet_type TEXT NOT NULL,
    value TEXT NOT NULL,
    person_id TEXT REFERENCES persons(id),
    confidence REAL,
    metadata_json TEXT,
    created_at INTEGER NOT NULL
);

-- embeddings: vector storage
CREATE TABLE embeddings (
    id TEXT PRIMARY KEY,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    model TEXT NOT NULL,
    embedding_blob BLOB NOT NULL,
    dimension INTEGER NOT NULL,
    source_text_hash TEXT,
    created_at INTEGER NOT NULL,
    UNIQUE(entity_type, entity_id, model)
);
```

## Key Design Decisions

1. **NO conversation_id on events** — events are immutable, use conversation_events mapping
2. **Reactions are events** — content_types=['reaction'], reply_to refs the reacted event
3. **No is_group on threads** — derived from event_participants per-event
4. **Facets are the queryable output** — don't store raw LLM JSON, extract to facets table

## Progress Format

APPEND to progress.txt after each story:

```markdown
---
## [Date] - [US-XXX] [Title]
- What was implemented
- Files changed
- **Learnings:**
  - Patterns discovered
  - Gotchas encountered
```

Add reusable patterns to TOP of progress.txt in Codebase Patterns section.

## Stop Condition

If ALL stories in prd.json have `passes: true`, reply:
```
<promise>COMPLETE</promise>
```

Otherwise, end normally after completing one story.

## Critical Rules

1. **ONE story per iteration** — Do not implement multiple stories
2. **Build must pass** — `go build ./cmd/comms` must succeed before committing
3. **Follow schema design** — Use exact schema from SCHEMA_DESIGN_ANALYSIS.md
4. **No placeholders** — Full implementations only
5. **Update progress.txt** — Capture learnings for future iterations
6. **Update AGENTS.md** — Document codebase patterns
7. **Commit message format** — `feat: [US-XXX] - [Title]`
