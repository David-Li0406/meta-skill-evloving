# Cortex Memory System Specification

**Status:** Draft v2 - Reviewed  
**Last Updated:** January 22, 2026  
**Related:** `ARCHITECTURE_EVOLUTION.md`, `prompts/graphiti/README.md`

---

## Overview

This document specifies a **memory system** built onto Cortex that enables:

1. **Entity extraction and resolution** — Identify and deduplicate people, places, things
2. **Relationship extraction** — Capture facts as triples (subject → predicate → object)
3. **Temporal tracking** — Bi-temporal model for when facts are true vs. when we learned them
4. **Contradiction detection** — Invalidate stale facts when new information contradicts them
5. **Graph-based querying** — Traverse relationships, not just search by similarity

This system draws inspiration from [Graphiti](https://github.com/getzep/graphiti) while maintaining Cortex's more flexible architecture.

### Known Gaps / Future Work

| Gap | Description | Related Doc |
|-----|-------------|-------------|
| **Taxonomy Evolution** | Relationship types are free-form strings. Entity types need refinement over time. Need a generic solution for clustering/canonicalizing ontologies. | `docs/ideas/TAXONOMY_EVOLUTION.md` |
| **Entity Summary Generation** | Auto-generate summaries from episodes + relationships. Lazy generation on query. | Deferred |
| **Community Detection** | Cluster related entities for faster retrieval and organization. | Deferred |

---

## Part 1: Naming Changes

### Segments → Episodes

**Decision:** Rename `segments` to `episodes` throughout Cortex.

**Rationale:**
- "Episode" captures temporal boundedness and narrative coherence
- Maps to neuroscience concept of episodic memory (experiences) vs. semantic memory (facts)
- Aligns with Graphiti terminology for interoperability

**Schema changes:**
```sql
-- Rename tables
ALTER TABLE segments RENAME TO episodes;
ALTER TABLE segment_definitions RENAME TO episode_definitions;
ALTER TABLE segment_events RENAME TO episode_events;

-- Update foreign key columns
ALTER TABLE analysis_runs RENAME COLUMN segment_id TO episode_id;
```

---

## Part 2: Architecture Comparison

### Cortex vs. Graphiti Schema

| Concept | Cortex (Current) | Graphiti | Notes |
|---------|------------------|----------|-------|
| Raw content | `events` table | `EpisodicNode` | Similar purpose |
| Temporal grouping | `segments` (→ `episodes`) | Episodes are single messages | **Cortex is more flexible** |
| Context window | Configurable via definitions | Hardcoded 8 previous | **Cortex is more flexible** |
| Extracted facts | `facets` (key-value) | `EntityEdge` (triples) | Add triples to Cortex |
| Entities | Not explicit | `EntityNode` | **Add to Cortex** |
| Entity resolution | Not implemented | Inline during extraction | **Add to Cortex** |
| Embeddings | `embeddings` table | On nodes/edges | Similar |
| Temporal bounds | Not implemented | `valid_at`, `invalid_at` | **Add to Cortex** |

### Key Insight: Event → Episode Abstraction

Graphiti ingests single messages and looks back 8 episodes for context. This is limiting.

**Cortex's approach is superior:**
```
Events (raw) → Episode Definitions (chunking rules) → Episodes (grouped)
                                                          ↓
                                                   Entity Extraction
                                                   (over full episode)
```

Benefits:
- **Tunable context**: Episode size determined by chunking strategy, not hardcoded
- **Channel-appropriate**: Different strategies for different sources
- **LLM-efficient**: Extract entities from coherent episode, not sliding window

---

## Part 3: Data Model

### 3.1 Storage Strategy

**SQLite-only** — no graph database needed for current use case.

**SQLite** stores everything:
- Events (raw messages, documents)
- Episodes (temporal groupings, equivalent to Graphiti's EpisodicNode)
- Episode definitions (chunking strategies)
- Facets (key-value extractions, including raw triple extractions)
- Entities (People, Companies, Projects, etc. — generalizes Contacts/People)
- Entity aliases (union-find for identity resolution)
- Relationships (deduplicated triples with temporal bounds)
- Embeddings (unified table for events, episodes, entities, relationships)
- Mentions (episode↔entity, episode↔relationship links)
- Merge candidates (suspected duplicates for review)

**Why no graph database:**
1. Multi-hop traversal queries are rare for personal memory (~1-10k entities)
2. SQLite recursive CTEs handle the queries we need
3. Single source of truth, no sync complexity
4. Proven, embedded, battle-tested

**If needed later:** Schema is designed to support Kuzu. Add only if we hit queries like shortest-path or community detection algorithms that SQLite can't handle efficiently.

### 3.2 Entity Types

**Philosophy: Entities are things you want to traverse to/from.** Abstract concepts (hobbies, professions, technologies) are discoverable via embedding search on episodes. Literal values (emails, phones, dates) use `target_literal` on relationships.

This keeps the entity model focused on:
- **People** you interact with
- **Organizations** you work with/for
- **Projects** you build or reference
- **Places** with geographic significance
- **Events** with participants
- **Documents** you create or reference
- **Pets** (animal companions)

**Default types:**

| ID | Name | Description | Examples |
|----|------|-------------|----------|
| 0 | Entity | Default/unknown type | Fallback |
| 1 | Person | A human being | Tyler, Dad, Casey |
| 2 | Company | Business or organization | Anthropic, Google, Intent Systems |
| 3 | Project | A project, product, or codebase | Cortex, Nexus, HTAA |
| 4 | Location | A place | Austin, Texas, 1812 Dwyer Ave |
| 5 | Event | A meeting or occurrence | "Jan 21 standup", "HTAA meeting" |
| 6 | Document | A file or written work | README.md, "the spec" |
| 7 | Pet | An animal companion | Luna, Max |

**Stored in config or code:**

```go
var DefaultEntityTypes = []EntityType{
    {ID: 0, Name: "Entity", Description: "Default/unknown type"},
    {ID: 1, Name: "Person", Description: "A human being"},
    {ID: 2, Name: "Company", Description: "Business or organization"},
    {ID: 3, Name: "Project", Description: "A project, product, or codebase"},
    {ID: 4, Name: "Location", Description: "A place (city, address, venue)"},
    {ID: 5, Name: "Event", Description: "A meeting, occurrence, or happening"},
    {ID: 6, Name: "Document", Description: "A file, article, or written work"},
    {ID: 7, Name: "Pet", Description: "An animal companion"},
}
```

**Resolution strategies by type:**

| Entity Type | Resolution Strategy |
|-------------|---------------------|
| Person | Aliases + context scoring + LLM |
| Company, Project | Name similarity + aliases |
| Location | Name + normalization (geocoding optional) |
| Event | Name + date + participants |
| Document | Path/name + content hash |
| Pet | Name + owner relationship |

**Extensible:** Add custom types for specific domains (e.g., `Repository`, `Meeting`).

**What's NOT an entity:**
- **Dates** — stored as `target_literal` on temporal relationships (ISO 8601)
- **AI agents** — no durable identity; AI chat content is in episodes
- **Concepts, activities, professions** — searchable via episode embeddings

### 3.3 Relationship Types

Relationships are **free-form strings** (taxonomy evolution will cluster them later).

**Target types:** Relationships point to either an entity (`target_entity_id`) or a literal value (`target_literal`).

| Target Type | Relationship Types | Format |
|-------------|-------------------|--------|
| **Literal → Alias** | HAS_EMAIL, HAS_PHONE, HAS_HANDLE, HAS_USERNAME, ALSO_KNOWN_AS | Promoted to `entity_aliases` |
| **Literal → Date** | BORN_ON, ANNIVERSARY_ON, OCCURRED_ON, SCHEDULED_FOR, STARTED_ON, ENDED_ON | ISO 8601: `YYYY-MM-DD` or `YYYY-MM` |
| **Entity** | Everything else | UUID reference |

**Common entity-to-entity relationship types:**

| Category | Relationship Types | Target Entity Type |
|----------|-------------------|-------------------|
| **Personal** | BORN_IN, LIVES_IN | Location |
| **Personal** | HAS_PET | Pet |
| **Professional** | WORKS_AT, OWNS, FOUNDED | Company |
| **Professional** | ATTENDED | Company (school) or Event |
| **Social** | KNOWS, FRIEND_OF, SPOUSE_OF, PARENT_OF, DATING | Person |
| **Projects** | CREATED, BUILDING, WORKING_ON, CONTRIBUTED_TO | Project |
| **Events** | ATTENDED, HOSTED | Event |
| **Location** | LOCATED_IN, VISITED | Location |
| **Content** | AUTHORED, REFERENCES | Document |

**Literal value formats:**

| Type | Format | Examples |
|------|--------|----------|
| Email | Lowercase | `tyler@example.com` |
| Phone | E.164 preferred | `+1-707-287-6731` |
| Handle | With @ prefix | `@tnapathy` |
| Username | As-is | `tnapathy` |
| Date | ISO 8601 | `1990-05-15`, `2024-01`, `2020` |

**All relationships have:**
- `relation_type`: The type (free-form string, SCREAMING_SNAKE_CASE)
- `fact`: Natural language description ("Tyler works at Anthropic")
- `target_entity_id` OR `target_literal` (exactly one must be set)
- `valid_at` / `invalid_at`: Bi-temporal bounds (when relationship was true in reality)
- `created_at`: When system learned about it
- Provenance lives in `episode_relationship_mentions` (episode, speaker attribution, source_type)

### 3.4 SQLite Schema Additions

```sql
-- ============================================
-- ENTITIES (canonical, deduplicated)
-- ============================================
-- This generalizes People/Contacts to all entity types.
-- A "Person" entity is just an entity with entity_type_id=1.
CREATE TABLE entities (
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

CREATE INDEX idx_entities_type ON entities(entity_type_id);
CREATE INDEX idx_entities_name ON entities(canonical_name);

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
CREATE TABLE entity_aliases (
    id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL REFERENCES entities(id),
    alias TEXT NOT NULL,
    alias_type TEXT NOT NULL,  -- 'name', 'email', 'phone', 'handle', 'username', 'nickname'
    normalized TEXT,           -- Lowercase/cleaned for matching
    is_shared BOOLEAN DEFAULT FALSE,  -- TRUE if multiple entities share this alias
    created_at TEXT NOT NULL
    -- NOTE: No UNIQUE constraint - same alias can map to multiple entities
);

CREATE INDEX idx_entity_aliases_lookup ON entity_aliases(alias, alias_type);
CREATE INDEX idx_entity_aliases_normalized ON entity_aliases(normalized, alias_type);
CREATE INDEX idx_entity_aliases_entity ON entity_aliases(entity_id);

-- ============================================
-- RELATIONSHIPS (deduplicated triples with temporal bounds)
-- ============================================
-- Identity relationships (HAS_EMAIL, HAS_PHONE, HAS_HANDLE) go to entity_aliases.
-- Temporal relationships (BORN_ON, OCCURRED_ON, etc.) use target_literal.
-- All other relationships use target_entity_id.
CREATE TABLE relationships (
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

CREATE INDEX idx_relationships_source ON relationships(source_entity_id);
CREATE INDEX idx_relationships_target ON relationships(target_entity_id);
CREATE INDEX idx_relationships_type ON relationships(relation_type);
CREATE INDEX idx_relationships_temporal ON relationships(valid_at, invalid_at);

-- Uniqueness for entity-target relationships
CREATE UNIQUE INDEX idx_relationships_unique_entity
ON relationships(source_entity_id, target_entity_id, relation_type, valid_at)
WHERE target_entity_id IS NOT NULL;

-- Uniqueness for literal-target relationships
CREATE UNIQUE INDEX idx_relationships_unique_literal
ON relationships(source_entity_id, target_literal, relation_type, valid_at)
WHERE target_literal IS NOT NULL;

-- ============================================
-- EPISODE-ENTITY MENTIONS (which episodes mention which entities)
-- ============================================
-- Junction table: many-to-many between episodes and entities.
-- Used for: entity summary generation, recency queries, channel derivation.
-- "Which channels does Tyler appear in?" = query episodes via this table.
CREATE TABLE episode_entity_mentions (
    episode_id TEXT NOT NULL REFERENCES episodes(id),
    entity_id TEXT NOT NULL REFERENCES entities(id),
    mention_count INTEGER DEFAULT 1,
    created_at TEXT NOT NULL,
    PRIMARY KEY (episode_id, entity_id)
);

CREATE INDEX idx_episode_entity_mentions_entity ON episode_entity_mentions(entity_id);

-- ============================================
-- EPISODE-RELATIONSHIP MENTIONS (provenance for relationships)
-- ============================================
-- Junction table: many-to-many between episodes and relationships.
-- Same relationship mentioned in 10 episodes = 10 records here.
-- Used for: frequency signals, provenance, confidence boosting.
CREATE TABLE episode_relationship_mentions (
    id TEXT PRIMARY KEY,
    episode_id TEXT NOT NULL REFERENCES episodes(id),
    relationship_id TEXT REFERENCES relationships(id),  -- NULL for identity relationships
    extracted_fact TEXT NOT NULL,  -- Original extracted text (raw, pre-dedup)
    asserted_by_entity_id TEXT REFERENCES entities(id),  -- Speaker who made the statement
    source_type TEXT,  -- 'self_disclosed', 'mentioned', 'inferred'
    
    -- For identity relationships (HAS_EMAIL, etc.) that go to aliases instead
    target_literal TEXT,  -- The literal value (email, phone, etc.)
    alias_id TEXT REFERENCES entity_aliases(id),  -- Link to created alias
    
    confidence REAL,
    created_at TEXT NOT NULL
);

CREATE INDEX idx_episode_rel_mentions_episode ON episode_relationship_mentions(episode_id);
CREATE INDEX idx_episode_rel_mentions_relationship ON episode_relationship_mentions(relationship_id);

-- ============================================
-- MERGE CANDIDATES (suspected duplicates for review)
-- ============================================
-- When resolution is uncertain, create a merge candidate for human review.
-- Better to have duplicates than false-merge corruption.
CREATE TABLE merge_candidates (
    id TEXT PRIMARY KEY,
    entity_a_id TEXT NOT NULL REFERENCES entities(id),
    entity_b_id TEXT NOT NULL REFERENCES entities(id),
    confidence REAL,
    reason TEXT,  -- 'name_similarity', 'relationship_overlap', 'co_mention', etc.
    context TEXT, -- JSON with supporting evidence
    status TEXT DEFAULT 'pending',  -- 'pending', 'merged', 'rejected'
    created_at TEXT NOT NULL,
    resolved_at TEXT
);

CREATE INDEX idx_merge_candidates_status ON merge_candidates(status);

-- ============================================
-- MERGE EVENTS (audit log)
-- ============================================
CREATE TABLE merge_events (
    id TEXT PRIMARY KEY,
    source_entity_id TEXT NOT NULL REFERENCES entities(id),
    target_entity_id TEXT NOT NULL REFERENCES entities(id),
    merge_type TEXT NOT NULL,      -- 'hard_identifier', 'name_similarity', etc.
    triggering_facts TEXT,         -- JSON: facts that triggered the merge
    similarity_score REAL,
    created_at TEXT NOT NULL,
    resolved_by TEXT               -- 'auto', 'user:<id>', etc.
);

CREATE INDEX idx_merge_events_target ON merge_events(target_entity_id);

-- ============================================
-- EMBEDDINGS (unified for all embeddable types)
-- ============================================
-- Extend existing embeddings table rather than separate tables per type.
-- target_type + target_id identify what was embedded.
ALTER TABLE embeddings ADD COLUMN target_type TEXT;  -- 'event', 'episode', 'entity', 'relationship'
ALTER TABLE embeddings ADD COLUMN target_id TEXT;

-- For new installs, the full schema would be:
-- CREATE TABLE embeddings (
--     id TEXT PRIMARY KEY,
--     target_type TEXT NOT NULL,  -- 'event', 'episode', 'entity', 'relationship'
--     target_id TEXT NOT NULL,
--     embedding BLOB NOT NULL,
--     model TEXT NOT NULL,
--     created_at TEXT NOT NULL,
--     UNIQUE(target_type, target_id, model)
-- );

CREATE INDEX idx_embeddings_target ON embeddings(target_type, target_id);
```

### 3.5 Graph Schema (Kuzu) — Deferred

If SQLite graph queries prove insufficient, add Kuzu with this schema:

```
Node Types:
- Episode (uuid, name, valid_at, created_at)  -- content stays in SQLite
- Entity (uuid, name, type, summary, created_at)
- Community (uuid, name, summary, created_at)

Edge Types:
- MENTIONS (Episode → Entity)
- RELATES_TO (Entity → Entity) with properties:
  - relation_type, fact, valid_at, invalid_at, created_at
- HAS_MEMBER (Community → Entity)
```

**When to add Kuzu:**
- Multi-hop traversal queries are too slow (e.g., "friends of friends")
- Recursive CTEs become unwieldy
- Graph algorithms needed (PageRank, community detection)

### 3.6 Keeping Both Facets AND Relationships

**Decision:** Maintain both extraction types in parallel.

| Extraction Type | Use Case | Example |
|-----------------|----------|---------|
| **Facets** (key-value) | Simple attributes, metadata, raw extractions | `{key: "sentiment", value: "positive"}` |
| **Relationships** (triples) | Entity connections (deduplicated) | `Tyler --WORKS_AT--> Intent Systems` |

**How they work together:**

```
1. Extract raw triple from episode
   "Tyler works at Intent Systems"
   
2. Store as facet (raw, preserves provenance)
   Facet: {
     analysis_type: "relationship_extraction",
     key: "triple",
     value: "Tyler WORKS_AT Intent Systems",
     episode_id: "ep_123"
   }
   
3. Resolve entities (Tyler → entity_abc, Intent Systems → entity_xyz)

4. Dedupe against existing relationships

5. Store in relationships table (canonical, deduplicated)
   Relationship: {
     source_entity_id: "entity_abc",
     target_entity_id: "entity_xyz", 
     relation_type: "WORKS_AT",
     fact: "Tyler Brandt works at Intent Systems"
   }

6. Link back: episode_relationship_mentions
   Links ep_123 → this relationship
```

**Why both?**
- Facets preserve raw extractions (useful for taxonomy evolution, debugging)
- Relationships are deduplicated for querying
- Facets are cheap/fast, relationships require resolution
- Can analyze extraction quality by comparing facets vs relationships

---

## Part 4: Extraction Pipeline

### 4.0 Key Insight: Graph-Independent Extraction

**Problem:** Existing knowledge should influence how entities are interpreted.

**Example:** When processing "Tyler mentioned the project is delayed":
- Multiple Tylers exist in the graph
- "the project" could refer to several projects
- We need context to disambiguate

**Rejected approach: Retrieval-augmented extraction**
```
Episode → Retrieve context → Inject into prompt → Extract
```
Problems:
- Makes extraction sequential (can't parallelize)
- Bad graph data corrupts extraction
- Non-deterministic (same input → different output depending on graph state)

**Chosen approach: Graph-independent extraction with resolution-time context**
```
Episode → Extract (graph-independent) → Resolve with graph context
```

Extraction doesn't query the existing graph. Resolution uses the graph to disambiguate:

```
1. EXTRACT (graph-independent)
   Input: "Tyler mentioned the project is delayed"
   Output: entities=["Tyler", "the project"], relationships=[("Tyler", "MENTIONED", "the project")]

2. RESOLVE "Tyler" (with graph context)
   - Search entity_aliases for "Tyler" → multiple candidates
   - Context signals:
     - Episode channel: work Slack → weight work-Tyler higher
     - Recent mentions: Tyler Brandt mentioned 3 episodes ago → weight higher
     - Co-mentions: "the project" + Tyler Brandt has PROJECT relationships
   - Score candidates, pick highest (or create new if uncertain)
   - Track top N candidates considered (for debugging/review)

3. RESOLVE "the project" (with graph context)
   - What projects does resolved-Tyler connect to?
   - Recent context suggests Cortex project
   - If confident → resolve to "Cortex"
   - If ambiguous → create generic entity, flag for review
```

**Benefits:**
- Extraction is graph-independent, parallelizable, reproducible
- Resolution uses graph context where it matters
- Bad graph data doesn't corrupt extraction
- Can re-run resolution if graph improves

**Episode lookback — configurable per episode_definition:**
- `lookback_episodes: 0` — Default (our episodes are already rich context)
- `lookback_episodes: 1-2` — For coreference-heavy contexts
- Configurable in extraction prompt template

### 4.1 Pipeline Overview

This pipeline follows Graphiti's proven approach: split extraction into focused prompts, then resolve against the graph.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      MEMORY EXTRACTION PIPELINE                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  INPUT: Episode (grouped events from any chunking strategy)             │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 1. EXTRACT ENTITIES (graph-independent)                          │   │
│  │    Prompt: extract-entities.prompt.md                            │   │
│  │    Input: episode content + optional previous episodes           │   │
│  │    Output: [{name, entity_type_id}, ...]                         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 2. RESOLVE ENTITIES (with graph context)                         │   │
│  │    - Exact alias match (high confidence)                         │   │
│  │    - Embed + search existing entities                            │   │
│  │    - Context scoring (channel, co-mentions, relationships)       │   │
│  │    - Track top N candidates considered (for debugging)           │   │
│  │    - LLM disambiguation only if scores are close                 │   │
│  │    - CRITICAL: Create new if uncertain (duplicates > false merge)│   │
│  │    Output: resolved_entities[], uuid_map{}, candidates_considered│   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 3. EXTRACT RELATIONSHIPS (graph-independent)                     │   │
│  │    Prompt: extract-relationships.prompt.md                       │   │
│  │    Input: episode content + resolved entities with UUIDs         │   │
│  │    Output: [{source_uuid, target, relation_type, fact,           │   │
│  │              valid_at, invalid_at}, ...]                         │   │
│  │    Note: HAS_* identity relationships use target_literal         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 4. RESOLVE EDGES                                                 │   │
│  │    - Search existing edges between same entity pairs             │   │
│  │    - Prompt: resolve-edges.prompt.md                             │   │
│  │    - Decision: merge with existing OR create new                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 5. IDENTITY PROMOTION (code)                                     │   │
│  │    HAS_* relationships → aliases (self_disclosed only)           │   │
│  │    Store provenance in episode_relationship_mentions             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 6. DETECT CONTRADICTIONS                                         │   │
│  │    Prompt: detect-contradictions.prompt.md                       │   │
│  │    Find: existing facts contradicted by new facts                │   │
│  │    Action: set invalid_at on old edge (use episode timestamp     │   │
│  │            or inferred date)                                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 7. GENERATE EMBEDDINGS                                           │   │
│  │     - Embed new entity names                                     │   │
│  │     - Embed new relationship facts                               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 8. SAVE                                                          │   │
│  │    SQLite: entities, entity_aliases, relationships,              │   │
│  │            episode_*_mentions, embeddings                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 9. UPDATE ENTITY SUMMARIES (optional, deferred)                  │   │
│  │    Prompt: summarize-entity.prompt.md                            │   │
│  │    Update summaries for entities mentioned in this episode       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  PARALLEL: Extract facets using existing Cortex pipeline               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Entity Resolution Details

**The Problem:** Same entity appears with different names:
- "Tyler" / "Tyler Brandt" / "tnapathy@gmail.com"
- "Intent Systems" / "Intent" / "the company"

**The Harder Problem:** Multiple people with same name:
- Tyler Brandt (you), Tyler from college, Tyler at the coffee shop
- Must avoid false-positive merges — duplicates can be fixed, false merges corrupt data

**Resolution Strategy:**

```
1. EXACT ALIAS MATCH
   Search entity_aliases table for exact match (normalized)
   Email/phone matches are high confidence → use existing entity
   Name-only matches require further validation

2. SEMANTIC SIMILARITY
   Embed extracted name
   Search entity embeddings by cosine similarity
   Candidates = top K above threshold (0.85+)

3. CONTEXT SCORING (for each candidate)
   Score based on disambiguation signals:
   
   +high:  Identifier match (email, phone, handle)
   +high:  Co-mentioned with related entities we know
           "Tyler and Casey" + we know Casey→Tyler Brandt
   +med:   Same channel as recent mentions of candidate
   +med:   Relationship context fits (works at same company)
   +low:   Name similarity only
   
   -score: Different channel, no overlap signals
  -score: Conflicting identifiers (different phone number)

4. DECISION LOGIC
   If single candidate with high score (>0.9) → match
   If multiple candidates, clear winner (gap >0.3) → match winner
   If ambiguous (scores close) → LLM disambiguation
   If LLM uncertain → create NEW entity, add to merge_candidates
   If no candidates → create new entity

5. CRITICAL RULE
   When in doubt, create new entity.
   Duplicates are recoverable. False merges corrupt data.
   Surface uncertain cases in merge_candidates for human review.
```

**Cross-platform contact deduplication:**

Gmail contact "Casey Adams <casey@example.com>" and iMessage "Casey 💕" may be same person.

```
Detection strategies:
1. Identifier overlap: If any identifier matches → high-confidence merge
2. Relationship inference: Both contacts message same third parties → likely same
3. Name + relationship: Same name + similar relationship graph → candidate
4. Surface for review: Add to merge_candidates with evidence
```

### 4.3 Contacts Integration

**Contacts are pre-seeded entities** with high confidence. This generalizes People/Contacts into the entity system.

```
Import flow:
1. Load contacts from address book / CRM / iMessage / Gmail
2. For each contact:
   - Check if entity with matching identifier exists
   - If yes: add new aliases to existing entity
   - If no: create new entity (origin='contact_import')
3. Add aliases: email, phone, handle, nickname
4. Set confidence=1.0 (user-verified data)

Resolution flow:
1. When extracting "Tyler" from message
2. First check entity_aliases for exact match
3. Contact-imported entities get priority (confidence=1.0)
4. Unknown people become new entities (origin='extracted')
```

**Cross-platform merging:**

```
Scenario: Import Gmail contacts, then iMessage contacts

Gmail import creates:  Entity "Casey Adams" with alias "casey@example.com"
iMessage import finds: Contact "Casey" with phone "+1-555-1234"

If no identifier overlap:
  - Create merge_candidate with reason='name_similarity'
  - Surface for human review
  
If identifier overlap (same phone in both):
  - Auto-merge, combine aliases
```

### 4.4 Identity Promotion: target_literal → Aliases

**Key insight:** Identity relationships (HAS_EMAIL, HAS_PHONE, HAS_HANDLE) use `target_literal` instead of `target_entity_id`. They go directly to aliases, not the relationships table.

**Why this approach:**
- Identifiers (emails, phones) aren't entities you traverse to
- Avoids entity count bloat from literal values
- Aliases are the right abstraction for identity resolution
- Provenance preserved in `episode_relationship_mentions.target_literal`

**The flow:**

```
1. EXTRACTION (graph-independent)
   Message: "my recovery email is jim@napageneralstore.com"
   From: Dad (+1-650-823-8440)
   
   Extracted relationships:
   [
     {
       source_entity_id: 0,  // Dad
       relation_type: "HAS_EMAIL",
       target_literal: "jim@napageneralstore.com",  // NOT target_entity_id
       fact: "Dad's email is jim@napageneralstore.com",
       source_type: "self_disclosed"
     }
   ]

2. ENTITY RESOLUTION
   "Dad" → resolves to existing Dad entity UUID

3. IDENTITY PROMOTION (code step)
   For relationships with type in IDENTITY_TYPES:
     If source_type = 'self_disclosed':
       - Create alias: (Dad_uuid, "jim@napageneralstore.com", type='email')
       - Store provenance: episode_relationship_mentions with target_literal
       - Do NOT create a relationships table entry

4. COLLISION DETECTION (runs on aliases)
   Check: Does any other entity have alias "jim@napageneralstore.com"?
   If yes → create merge_candidate
```

**Identity relationship types (use target_literal):**

| Relationship Type | Alias Type | Notes |
|-------------------|-----------|-------|
| HAS_EMAIL | email | Unique identifier |
| HAS_PHONE | phone | Unique identifier |
| HAS_HANDLE | handle | Twitter, Instagram, etc. |
| HAS_USERNAME | username | Platform-specific |
| ALSO_KNOWN_AS | nickname | Name variants |

**All other relationships use target_entity_id** and go to the relationships table normally.

**Shared identifier handling:**

```
Scenario: Family phone number shared by multiple people

Message from Dad: "our home number is 555-1234"
Message from Mom: "you can reach us at 555-1234"

Both extractions produce:
  {source: Dad, type: HAS_PHONE, target_literal: "555-1234", source_type: "self_disclosed"}
  {source: Mom, type: HAS_PHONE, target_literal: "555-1234", source_type: "self_disclosed"}

Identity promotion:
  Both entities get the alias added
  Detect shared: same alias across multiple entities → set is_shared=TRUE
  
Result:
  entity_aliases: 
    - (Dad, "555-1234", type='phone', is_shared=TRUE)
    - (Mom, "555-1234", type='phone', is_shared=TRUE)

Resolution behavior:
  When searching for "555-1234": returns BOTH Dad and Mom
  Collision detection: Shared aliases don't trigger merge candidates
  Disambiguation: Requires additional context (channel, co-mentions)
```

### 4.5 person_facts Migration

**Current system:** `person_facts` table with category/fact_type/fact_value structure.

**Goal:** Unify into entity memory system. **Everything becomes relationships** (some to entities, some to literals).

**Philosophy:** No attributes. If it's worth storing, it's worth making queryable via the graph.

**New system mapping:**

| Current (person_facts) | New System | Example |
|------------------------|------------|---------|
| **Identity (→ Aliases)** | | |
| email_* | `entity_aliases` | type='email' |
| phone_* | `entity_aliases` | type='phone' |
| social_* | `entity_aliases` | type='handle' |
| full_legal_name | `entity_aliases` + `canonical_name` | type='name' |
| nickname | `entity_aliases` | type='nickname' |
| **Dates (→ target_literal)** | | |
| birthdate | `relationship` | (Person) --BORN_ON--> "1990-05-15" |
| anniversary | `relationship` | (Person) --ANNIVERSARY_ON--> "2023-02-18" |
| **Organizations (→ Company Entities)** | | |
| employer_current | `relationship` | (Person) --WORKS_AT--> (Company:Anthropic) |
| business_owned | `relationship` | (Person) --OWNS--> (Company) |
| school_attended | `relationship` | (Person) --ATTENDED--> (Company:Stanford) |
| **People (→ Person Entities)** | | |
| spouse | `relationship` | (Person) --SPOUSE_OF--> (Person) |
| children | `relationship` | (Person) --PARENT_OF--> (Person) |
| **Places (→ Location Entities)** | | |
| location_current | `relationship` | (Person) --LIVES_IN--> (Location:Austin) |
| place_of_birth | `relationship` | (Person) --BORN_IN--> (Location) |
| **Abstract facts (→ Episode search)** | | |
| profession | Episode text | Searchable via embedding ("who is a software engineer?") |
| hobbies | Episode text | Searchable via embedding ("who likes hiking?") |
| dietary_preferences | Episode text | Searchable via embedding ("who is vegetarian?") |
| **Evidence / Context** | | |
| evidence | `relationship.fact` | Natural language: "Dad said his email is..." |
| source_type | `episode_relationship_mentions.source_type` | self_disclosed / mentioned / inferred |
| asserted_by | `episode_relationship_mentions.asserted_by_entity_id` | Who said it (speaker attribution) |
| confidence | `relationship.confidence` | 0.0-1.0 |

**Queryable examples:**

```sql
-- Who was born in 1990?
SELECT e.canonical_name 
FROM entities e
JOIN relationships r ON e.id = r.source_entity_id
WHERE r.relation_type = 'BORN_ON' AND r.target_literal LIKE '1990%';

-- Who works at Anthropic?
SELECT e.canonical_name
FROM entities e
JOIN relationships r ON e.id = r.source_entity_id
JOIN entities c ON r.target_entity_id = c.id
WHERE r.relation_type = 'WORKS_AT' AND c.canonical_name = 'Anthropic';
```

**Migration strategy:**
1. Import existing person_facts:
   - Identity fields → entity_aliases
   - Temporal fields → relationships with `target_literal` (ISO 8601)
   - Entity-backed fields → create target entities + relationships
2. Entity resolution deduplicates target entities
3. Keep person_facts table during transition
4. Deprecate after validation

### 4.6 Entity Summary Generation

**What:** Auto-generated summary of an entity from its episodes and relationships.

**When to generate/update:**
- Lazy: On query, if `summary_updated_at` < latest episode mention
- Eager: After processing episode that mentions entity (batched)
- Recommended: Lazy with cache invalidation

**How:**

```
1. Get recent episodes mentioning entity (via episode_entity_mentions)
   - Limit to most recent N or past M days
   
2. Get relationships involving entity
   - Both directions (source and target)
   - Include temporal validity
   
3. Generate summary via LLM
   Prompt: summarize-entity.prompt.md
   Input: entity name, type, episode snippets, relationships
   Output: 2-3 sentence summary
   
4. Update entity.summary, entity.summary_updated_at
```

**Example:**

```
Entity: Casey Adams (Person)
Episodes: [500 mentions across iMessage, email]
Relationships:
  - LIVES_WITH Tyler (valid_at: 2024-02-01)
  - WORKS_AT Acme Corp (valid_at: 2023-06-15, invalid_at: 2025-01-01)
  - WORKS_AT NewJob Inc (valid_at: 2025-01-15)

Summary: "Casey Adams is Tyler's partner. They've lived together since 
February 2024. Casey recently started working at NewJob Inc after 
leaving Acme Corp."
```

### 4.5 Utterance Classification (Sarcasm, Hedging, Hypotheticals)

**Before extraction, classify the utterance:**

| Classification | Extraction Behavior |
|----------------|---------------------|
| **Sincere** | Extract normally |
| **Sarcastic** | Extract opposite meaning, or skip |
| **Hypothetical** | Don't extract as fact |
| **Uncertain** | Extract with low confidence |
| **Question** | Don't extract as fact (it's a query) |

**Prompt pattern:**
```
Given this text, classify the utterance:
- sincere: Stated as fact
- sarcastic: Opposite of literal meaning
- hypothetical: "If...", "Would be...", speculation
- uncertain: "Maybe...", "I think...", hedging
- question: Asking for information

Text: "Oh great, another meeting about meetings"
Classification: sarcastic
```

---

## Part 5: Chunking Strategies

### 5.1 Generic Strategy Interface

**Decision:** Chunking strategies should be generic, not channel-specific.

```go
type ChunkingStrategy interface {
    Name() string
    Chunk(events []Event) []Episode
}

// Implementations (generic names)
type TimeGapStrategy struct {
    GapThreshold time.Duration  // e.g., 5 minutes
}

type TurnPairStrategy struct {
    // Groups user message + assistant response
}

type FixedWindowStrategy struct {
    WindowSize time.Duration  // e.g., 1 hour, 1 day
}

type TokenLimitStrategy struct {
    MaxTokens int  // e.g., 4000 tokens
}

type SemanticStrategy struct {
    SimilarityThreshold float64  // Split when topic changes
}

type SingleEventStrategy struct {
    // Each event is its own episode (for rich metadata)
}
```

### 5.2 Channel-Strategy Recommendations

| Channel | Recommended Strategy | Rationale |
|---------|---------------------|-----------|
| iMessage | TimeGap (5min) | Conversation breaks |
| Email | Per-thread or SingleEvent | Threads are natural units |
| AI Sessions | TurnPair | User intent + response |
| AI Sessions (metadata) | SingleEvent | Preserve rich metadata |
| Documents | Semantic or TokenLimit | Topic coherence |
| Calendar | SingleEvent | Each event is atomic |

### 5.3 Semantic Chunking

**How it works:**

```
1. Split text into sentences
2. Embed each sentence
3. Compute similarity between adjacent sentences
4. Split where similarity drops below threshold

Example:
Sentences: [S1, S2, S3, S4, S5]
Similarities: [0.9, 0.85, 0.3, 0.88]
                          ↑
                    Split here (topic change)

Result: [Episode(S1,S2,S3), Episode(S4,S5)]
```

**Implementation options:**
- Embedding-based (fast, works well)
- LLM-based (more accurate, slower)

---

## Part 6: Query Capabilities

### 6.1 Query Types

| Query Type | Description | Implementation |
|------------|-------------|----------------|
| **Semantic** | "What do I know about X?" | Vector search on entity/fact embeddings |
| **Temporal** | "What happened last week?" | Filter by episode.valid_at |
| **Relational** | "Who does Tyler work with?" | Graph traversal (Kuzu) |
| **Hybrid** | Combine above | Multi-stage retrieval |

### 6.2 Example Queries

**Semantic (SQLite + embeddings):**
```sql
SELECT e.*, 
       cosine_similarity(ee.name_embedding, ?) as score
FROM entities e
JOIN entity_embeddings ee ON e.id = ee.entity_id
WHERE score > 0.8
ORDER BY score DESC
LIMIT 10;
```

**Relational (Kuzu/Cypher):**
```cypher
-- "Who does Tyler know through work?"
MATCH (tyler:Entity {name: 'Tyler Brandt'})-[:RELATES_TO {relation_type: 'WORKS_AT'}]->(company)
MATCH (company)<-[:RELATES_TO {relation_type: 'WORKS_AT'}]-(colleague)
WHERE colleague <> tyler
RETURN colleague.name, company.name
```

**Temporal with validity:**
```sql
-- "What was Tyler's job in 2024?"
SELECT r.*, se.name as source, te.name as target
FROM relationships r
JOIN entities se ON r.source_entity_id = se.id
JOIN entities te ON r.target_entity_id = te.id
WHERE se.canonical_name = 'Tyler Brandt'
  AND r.relation_type = 'WORKS_AT'
  AND r.valid_at <= '2024-12-31'
  AND (r.invalid_at IS NULL OR r.invalid_at > '2024-01-01');
```

---

## Part 7: Batch Processing

### 7.1 Community Detection

**Purpose:** Cluster related entities into communities for:
- Faster retrieval (search communities first)
- Automatic organization (project groupings, social circles)
- Summary generation

**Algorithm:**
1. Build entity graph from relationships
2. Run clustering (Louvain, Label Propagation)
3. For each cluster, generate community name and summary
4. Store as CommunityNode with HAS_MEMBER edges

**This is NOT taxonomy evolution** — communities are emergent groupings, not type hierarchies.

### 7.2 Taxonomy Evolution (Future Work)

**Problem:** Entity types need to evolve as data grows.

**Example:**
- Start: `{type: "Company"}`
- Later: `{type: "Company", subtype: "Startup", industry: "FinTech"}`

**Approach (to be designed separately):**
1. Periodically analyze all entities of a type
2. Cluster by embedding similarity
3. Propose subtype names for clusters
4. Human reviews or auto-accepts
5. Update entity types, re-classify existing

**Note:** This builds on top of the memory system. Design separately after core system works.

**Also applies to:** Relationship types (WORKS_AT vs EMPLOYED_BY), entity types, capability ontologies.

See: `docs/ideas/TAXONOMY_EVOLUTION.md`

---

## Part 8: Merge System (Identity Resolution)

### 8.1 Overview

The merge system resolves when two entities should be combined into one. 

**Critical principle:** False positives are worse than duplicates. Duplicates can be merged later; false merges corrupt data.

### 8.2 When Merge Candidates Are Created

| Trigger | Confidence | Auto-Eligible? |
|---------|------------|----------------|
| Hard identifier collision (email, phone, handle) | 0.95+ | Yes (if no conflicts) |
| Multiple hard identifiers match | 0.99 | Yes |
| Contact import with identifier overlap | 0.95 | Yes |
| Fuzzy name match (Jaccard ≥ 0.9) | 0.70-0.85 | No |
| Compound match (name + birthdate) | 0.90 | Maybe |
| Compound match (name + employer + city) | 0.85 | No |
| Soft accumulation (multiple weak signals) | 0.60-0.80 | No |
| Cross-platform name similarity | 0.50-0.70 | No |

### 8.3 Merge Candidate Schema

```sql
CREATE TABLE merge_candidates (
    id TEXT PRIMARY KEY,
    entity_a_id TEXT NOT NULL REFERENCES entities(id),
    entity_b_id TEXT NOT NULL REFERENCES entities(id),
    
    -- Scoring
    confidence REAL NOT NULL,         -- 0.0-1.0
    auto_eligible BOOLEAN DEFAULT FALSE,
    
    -- Evidence (why we think they match)
    reason TEXT NOT NULL,             -- 'hard_identifier', 'name_similarity', 'compound', 'soft_accumulation'
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

CREATE INDEX idx_merge_candidates_status ON merge_candidates(status);
CREATE INDEX idx_merge_candidates_auto ON merge_candidates(auto_eligible) WHERE status = 'pending';
```

### 8.4 Collision Detection Algorithm

Uses O(F) approach from IDENTITY_RESOLUTION_PLAN.md — iterate through facts, not person pairs.

```python
def detect_collisions():
    # Phase 1: Hard identifier collisions
    for alias_type in ['email', 'phone', 'handle']:
        collisions = sql("""
            SELECT alias, GROUP_CONCAT(entity_id) as entities
            FROM entity_aliases
            WHERE alias_type = ?
            GROUP BY alias
            HAVING COUNT(DISTINCT entity_id) > 1
        """, alias_type)
        
        for collision in collisions:
            entities = collision.entities.split(',')
            create_merge_candidate(
                entities=entities,
                reason='hard_identifier',
                confidence=0.95,
                auto_eligible=True,
                matching_facts=[{type: alias_type, value: collision.alias}]
            )
    
    # Phase 2: Compound identifier matching
    # name + birthdate, name + employer + city, etc.
    compound_matches = find_compound_matches()
    for match in compound_matches:
        create_merge_candidate(
            entities=[match.entity_a, match.entity_b],
            reason='compound',
            confidence=match.confidence,
            auto_eligible=(match.confidence >= 0.90),
            matching_facts=match.facts
        )
    
    # Phase 3: Soft identifier accumulation
    scores = {}  # (entity_a, entity_b) -> score
    for fact_type, weight in SOFT_IDENTIFIER_WEIGHTS.items():
        collisions = find_fact_collisions(fact_type)
        for collision in collisions:
            for pair in pairs(collision.entities):
                scores[pair] += weight
    
    for pair, score in scores.items():
        if score >= 0.6:
            create_merge_candidate(
                entities=list(pair),
                reason='soft_accumulation',
                confidence=score,
                auto_eligible=False,
                matching_facts=get_shared_facts(pair)
            )
```

### 8.5 Conflict Detection

Before auto-merging, check for conflicts:

```python
def detect_conflicts(entity_a, entity_b) -> list[Conflict]:
    conflicts = []
    
    # Different hard identifiers of same type
    for alias_type in ['phone', 'email']:
        aliases_a = get_aliases(entity_a, alias_type)
        aliases_b = get_aliases(entity_b, alias_type)
        if aliases_a and aliases_b and not aliases_a.intersection(aliases_b):
            # Both have phones, but different phones = conflict
            conflicts.append(Conflict(
                type=f'different_{alias_type}s',
                values_a=list(aliases_a),
                values_b=list(aliases_b)
            ))
    
    # Different birthdates (via relationships)
    bday_a = get_single_relationship_target(entity_a, 'BORN_ON')
    bday_b = get_single_relationship_target(entity_b, 'BORN_ON')
    if bday_a and bday_b and bday_a != bday_b:
        conflicts.append(Conflict(
            type='different_birthdates',
            values_a=bday_a,
            values_b=bday_b
        ))
    
    # Temporal impossibilities (e.g., can't work at two places at once)
    # ... additional conflict checks ...
    
    return conflicts
```

### 8.6 Auto-Merge Rules

```python
def should_auto_merge(candidate: MergeCandidate) -> bool:
    # Rule 1: Hard identifier with high confidence, no conflicts
    if candidate.reason == 'hard_identifier':
        if candidate.confidence >= 0.95 and not candidate.conflicts:
            return True
    
    # Rule 2: Multiple hard identifiers match
    hard_matches = count_hard_identifier_matches(candidate)
    if hard_matches >= 2:
        return True
    
    # Rule 3: Contact import with identifier overlap
    if both_from_contact_import(candidate) and has_identifier_overlap(candidate):
        return True
    
    # Default: Don't auto-merge (require human review)
    return False

def process_merge_candidates():
    pending = get_pending_candidates()
    
    for candidate in pending:
        # Check for conflicts
        conflicts = detect_conflicts(candidate.entity_a, candidate.entity_b)
        candidate.conflicts = conflicts
        
        if conflicts:
            candidate.auto_eligible = False
        elif should_auto_merge(candidate):
            execute_merge(candidate, resolved_by='auto')
        else:
            # Leave for human review
            pass
```

### 8.7 Merge Execution

```python
def execute_merge(candidate: MergeCandidate, resolved_by: str):
    source = candidate.entity_a  # Will be merged into target
    target = candidate.entity_b  # Will remain
    
    # 1. Move all aliases from source to target
    sql("UPDATE entity_aliases SET entity_id = ? WHERE entity_id = ?", 
        target.id, source.id)
    
    # 2. Update all relationships to point to target
    sql("UPDATE relationships SET source_entity_id = ? WHERE source_entity_id = ?",
        target.id, source.id)
    sql("UPDATE relationships SET target_entity_id = ? WHERE target_entity_id = ?",
        target.id, source.id)
    
    # 3. Move episode mentions
    sql("""
        INSERT OR REPLACE INTO episode_entity_mentions (episode_id, entity_id, mention_count, created_at)
        SELECT episode_id, ?, mention_count, created_at
        FROM episode_entity_mentions WHERE entity_id = ?
    """, target.id, source.id)
    sql("DELETE FROM episode_entity_mentions WHERE entity_id = ?", source.id)
    
    # 4. Update canonical name if source has better name
    if is_better_name(source.canonical_name, target.canonical_name):
        sql("UPDATE entities SET canonical_name = ? WHERE id = ?",
            source.canonical_name, target.id)
    
    # 5. Mark source as merged (don't delete for audit trail)
    sql("""
        UPDATE entities 
        SET merged_into = ?, 
            canonical_name = canonical_name || ' [MERGED→' || ? || ']'
        WHERE id = ?
    """, target.id, target.canonical_name, source.id)
    
    # 6. Log the merge
    sql("""
        INSERT INTO merge_events 
        (id, source_entity_id, target_entity_id, merge_type, triggering_facts, 
         similarity_score, created_at, resolved_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, uuid(), source.id, target.id, candidate.reason, 
        json.dumps(candidate.matching_facts), candidate.confidence, 
        now(), resolved_by)
    
    # 7. Update candidate status
    sql("""
        UPDATE merge_candidates 
        SET status = 'merged', resolved_at = ?, resolved_by = ?
        WHERE id = ?
    """, now(), resolved_by, candidate.id)
```

### 8.8 CLI Interface

```bash
# List pending merge candidates
cortex identify merge-candidates [--status pending|merged|rejected]
cortex identify merge-candidates --auto-eligible

# Show candidate details
cortex identify merge-candidate <id>
# Output:
# ┌─────────────────────────────────────────────────────────────┐
# │ Merge Candidate: mc_abc123                                   │
# ├─────────────────────────────────────────────────────────────┤
# │ Entity A: Tyler Brandt (Person)                              │
# │   Origin: contact_import (iMessage)                          │
# │   Aliases: +1-707-287-6731, tnapathy@gmail.com               │
# │   Relationships: WORKS_AT Intent Systems                     │
# │                                                              │
# │ Entity B: Tyler B (Person)                                   │
# │   Origin: contact_import (Gmail)                             │
# │   Aliases: tyler@anthropic.com                               │
# │   Relationships: WORKS_AT Anthropic                          │
# │                                                              │
# │ Match Reason: name_similarity (Jaccard: 0.91)                │
# │ Confidence: 0.75                                             │
# │ Auto-eligible: No                                            │
# │                                                              │
# │ Conflicts:                                                   │
# │   ⚠ Different employers: Intent Systems vs Anthropic        │
# │                                                              │
# │ Candidates Considered:                                       │
# │   1. Tyler Brandt (score: 0.91) ← selected                   │
# │   2. Tyler (coffee shop) (score: 0.45)                       │
# │   3. Tyler (college) (score: 0.38)                           │
# │                                                              │
# │ Recommendation: REVIEW (possible job change)                 │
# └─────────────────────────────────────────────────────────────┘

# Accept/reject
cortex identify accept <id> [--reason "same person, job change"]
cortex identify reject <id> [--reason "different people"]

# Bulk operations
cortex identify accept --all-auto  # Accept all auto-eligible
cortex identify run-detection      # Run collision detection

# Manual merge
cortex identify merge <entity_a> <entity_b> [--force]

# Stats
cortex identify status
# Output:
# Identity Resolution Status:
#   Active entities:     1,234
#   Merged entities:       56
#   Pending candidates:    12 (3 auto-eligible)
#   Aliases:            2,456
#   Relationships:      3,789
```

---

## Part 9: Implementation Plan

### Phase 1: Schema & Naming
- [ ] Rename segments → episodes (tables, columns, code)
- [ ] Add entities table
- [ ] Add entity_aliases table
- [ ] Add relationships table
- [ ] Add relationship_mentions table
- [ ] Add entity/relationship embeddings tables
- [ ] Add episode_entity_mentions table

### Phase 2: Entity Extraction
- [ ] Implement entity extraction using prompts
- [ ] Implement entity embedding
- [ ] Implement entity resolution (search + LLM)
- [ ] Integrate with contacts (pre-seeded entities)

### Phase 3: Relationship Extraction
- [ ] Implement relationship extraction using prompts
- [ ] Implement temporal bounds extraction
- [ ] Implement relationship resolution (dedup)
- [ ] Implement contradiction detection

### Phase 4: Identity System
- [ ] Implement identity promotion (target_literal → aliases)
- [ ] Implement collision detection (O(F) algorithm)
- [ ] Implement merge candidate creation
- [ ] Implement auto-merge rules
- [ ] Implement merge execution
- [ ] Add CLI for merge review

### Phase 5: Chunking Improvements
- [ ] Refactor chunking to generic interface
- [ ] Implement semantic chunking
- [ ] Implement token-limit chunking
- [ ] Per-channel strategy configuration

### Phase 6: Query Layer
- [ ] Unified search across entities + episodes
- [ ] Relational queries (graph traversal)
- [ ] Temporal queries with validity filtering

### Phase 7: Batch Processing
- [ ] Community detection job
- [ ] Entity summary refresh job
- [ ] (Deferred) Taxonomy evolution

---

## Part 10: Verification & Test Suite

This section defines end-to-end tests that prove each feature in this spec works as intended.

### 10.1 Test Methodology

- Use **fixture episodes** with expected outputs (golden files)
- Run the **full pipeline**: extract → resolve → promote → dedupe → persist
- Verify both **structure** (counts, FK integrity) and **semantics** (facts and values)
- Re-run the same episodes to confirm **idempotency**
- Fix model/config versions so results are deterministic

### 10.2 Core Fixtures (Minimum Set)

| Fixture | Focus | Expected Outcome |
|---------|-------|------------------|
| F1: Simple Person + Company | Base extraction | Person + Company entities, 1 WORKS_AT relationship |
| F2: Identity Literals | HAS_EMAIL/HAS_PHONE | Alias created, no relationship row, mention w/ target_literal |
| F3: Temporal Literals | BORN_ON / STARTED_ON | ISO 8601 target_literal dates |
| F4: Ambiguous Name | Two candidates | New entity + merge_candidate |
| F5: Shared Identifier | Family phone | alias.is_shared=TRUE, no merge_candidate |
| F6: Contradiction | Works-at then left | old edge invalid_at set, new edge added |
| F7: Contact Import | Gmail + iMessage | Auto-merge with identifier overlap |
| F8: Document + Project | README ref | Document + Project + REFERENCES edge |
| F9: Event Attendance | Meeting | Event entity + ATTENDED edges |
| F10: person_facts migration | Legacy facts | Aliases + relationships mapped correctly |

### 10.3 Schema & Integrity Tests

- All FKs are valid for entities/relationships/mentions
- `episode_relationship_mentions.relationship_id` nullable for literal-only rows
- Unique constraint prevents duplicate relationships per `(source, target, type, valid_at)`
- `entity_aliases` allows shared aliases across entities

### 10.4 Entity Extraction Tests

- Only entity types from §3.2 are extracted
- Speakers extracted in conversational episodes
- No dates, AI agents, or concepts extracted as entities
- Entities only in `previous_episodes` are excluded

**Pass:** Expected entities (name + type) match fixture outputs.

### 10.5 Entity Resolution Tests

- Exact alias match resolves to existing entity
- Ambiguous matches create new entity + merge_candidate
- `merge_candidates.candidates_considered` populated
- Deterministic results with fixed graph + config

### 10.6 Relationship Extraction Tests

- Identity + temporal relationships use `target_literal`
- All other relationships use `target_entity_id`
- `valid_at`/`invalid_at` only when explicitly stated
- Dates normalized to ISO 8601 (YYYY-MM-DD, YYYY-MM, YYYY)

### 10.7 Identity Promotion Tests

- HAS_EMAIL / HAS_PHONE / HAS_HANDLE → alias created
- Promotion only when `source_type = self_disclosed`
- `episode_relationship_mentions` stores `target_literal` + `alias_id`
- No rows inserted in `relationships` for identity-only facts

### 10.8 Edge Deduplication Tests

- Repeated extraction yields 1 relationship row
- Multiple mentions produce multiple `episode_relationship_mentions`
- Different `valid_at` values create distinct relationship rows

### 10.9 Contradiction Detection Tests

- Contradicting statements set `invalid_at` on old relationship
- Uses episode timestamp if explicit date not provided
- Old relationships are retained (audit preserved)

### 10.10 Mentions & Provenance Tests

- `episode_entity_mentions` created for each entity
- `episode_relationship_mentions` created for each relationship
- `asserted_by_entity_id` set when speaker is known
- `source_type` reflects self_disclosed / mentioned / inferred

### 10.11 Contact Import + Merge Tests

- Identifier overlap triggers auto-merge
- Name-only overlap creates merge_candidate (no auto-merge)
- Shared aliases do not generate merge_candidates

### 10.12 Query Layer Tests

- "Who works at Anthropic?" returns expected people
- "Where does Casey live?" returns expected location
- Temporal queries respect valid_at/invalid_at

### 10.13 Idempotency Tests

- Reprocessing the same episode yields **no new entities or relationships**
- Only mentions may increase (if deduped per episode)

### 10.14 Performance Guards

- Process N=1,000 episodes under target runtime
- Collision detection runs in O(F) time

---

## Part 11: Verification Harness (Real Data Fixtures)

This section defines the **verification harness** that runs the test suite using real data fixtures
from your sources (aix, gog, imessage). The goal is to validate system behavior on realistic data
and make it easy to "vibe check" results with your own messages.

### 11.1 Harness Structure

**Directory layout (proposed):**

```
fixtures/
  manifest.yaml
  aix/
    <fixture_id>/
      episode.json
      expectations.yaml
  gog/
    <fixture_id>/
      episode.json
      expectations.yaml
  imessage/
    <fixture_id>/
      episode.json
      expectations.yaml
reports/
  latest/
    summary.md
    failures.md
    graph_diff.json
```

**episode.json (input):**
```json
{
  "fixture_id": "imessage-01-job-change",
  "source": "imessage",
  "channel": "messages",
  "participants": ["Tyler", "Casey"],
  "reference_time": "2026-01-21T10:05:00-06:00",
  "episode_content": "Tyler: I left Intent Systems in December and joined Anthropic."
}
```

**expectations.yaml (assertions):**
```yaml
entities:
  must_have:
    - {name: "Tyler", type: "Person"}
    - {name: "Anthropic", type: "Company"}
  must_not_have:
    - {name: "Claude", type: "Person"}
relationships:
  must_have:
    - {source: "Tyler", type: "WORKS_AT", target: "Anthropic", valid_at: "2026-01"}
    - {source: "Tyler", type: "WORKS_AT", target: "Intent Systems", invalid_at: "2025-12"}
aliases:
  must_have: []
mentions:
  require_asserted_by: true
```

**Matching rules:**
- `must_have` = required outputs
- `must_not_have` = forbidden outputs
- `optional` = allowed but not required (tolerate LLM variance)
- Relationship matching uses (source name, relation_type, target literal/entity)

### 11.2 Harness Execution Flow

1. Load fixture episodes from `fixtures/*/*/episode.json`
2. Run full pipeline: extract → resolve → promote → dedupe → persist
3. Compare outputs against `expectations.yaml`
4. Generate reports: pass/fail + diffable summaries
5. Re-run all fixtures to verify idempotency

### 11.3 Real Data Fixture Selection (What to Capture)

The fixtures should cover **variation** in:
- Source (aix, gog, imessage)
- Channel type (DM, group, email)
- Identity markers (email/phone/handle)
- Temporal information (absolute + relative dates)
- Contradictions (job changes, moving locations)
- Merge ambiguity (same name, shared identifiers)

#### AIX Fixtures (structured/internal notes)

Focus on **personal facts** and **project updates**:
- Job change + start date (temporal literals)
- Location mention (city or address)
- Project updates with ownership (WORKING_ON / BUILDING)
- Event planning (SCHEDULED_FOR)

**Example cases:**
- "I started Nexus in January"
- "Meeting with Casey next Tuesday"
- "Moved to Austin last year"

#### GOG Fixtures (email/contact data)

Focus on **identity extraction** and **signature parsing**:
- Email signature with phone + handle
- Role/company change mentioned in email
- Attending/hosting an event (calendar invite)
- Thread where multiple people share same first name

**Example cases:**
- Signature: "— Casey Adams | c.adams@example.com | +1‑555‑123‑4567"
- "I left Intent Systems and joined Anthropic"

#### iMessage Fixtures (chat data)

Focus on **relationship and social context**:
- Group chat with multiple participants
- Nicknames and aliases ("Mom", "Dad")
- Shared identifier (family phone)
- Scheduling + rescheduling with relative dates
- Contradiction detection (job/location change)

**Example cases:**
- "Our home number is 555‑1234"
- "I'm in Austin now, moved last month"
- "Dinner next Friday" (relative date)

### 11.4 Fixture Coverage Matrix

| Feature | AIX | GOG | iMessage |
|---------|-----|-----|----------|
| Identity literals | ✓ | ✓ | ✓ |
| Temporal literals | ✓ | ✓ | ✓ |
| Contradictions | ✓ | ✓ | ✓ |
| Shared identifiers | – | ✓ | ✓ |
| Ambiguous names | – | ✓ | ✓ |
| Event attendance | ✓ | ✓ | ✓ |
| Document references | ✓ | ✓ | – |

### 11.5 Evaluation Outputs (Vibe Check)

Produce a human-readable report per fixture:
- Entities created / reused
- Relationships created / invalidated
- Aliases added (with is_shared flag)
- Merge candidates generated
- Diffs vs expected output

This makes it easy to skim and validate that **the system feels right**.

---

## Part 12: Open Questions

### Resolved in This Spec

| Question | Decision |
|----------|----------|
| Segments vs Episodes? | **Episodes** (rename) |
| Facets vs Relationships? | **Both** (raw facet + deduplicated relationship) |
| SQLite vs Graph DB? | **SQLite-only** (recursive CTEs handle our queries) |
| Contacts integration? | **Pre-seeded entities** (generalizes People/Contacts) |
| Chunking naming? | **Generic strategies** (not channel-specific) |
| Episode lookback? | **Configurable** per episode_definition |
| Previous memory influence? | **Graph-independent extraction** with resolution-time context |
| Entity source field? | **origin** = how created, channels derived from episodes |
| Separate embedding tables? | **Unified** embeddings table with target_type |
| Multiple Tylers problem? | **Context scoring + conservative merging** |
| Cross-platform contacts? | **merge_candidates table** for review |
| PII extraction? | **Unified** with entity extraction |
| Entity summaries? | **Lazy generation** (deferred) |
| Relationship type taxonomy? | **Free-form strings** (taxonomy evolution later) |
| Emails/phones as entities or aliases? | **Aliases via target_literal** (not entities) |
| person_facts migration? | **Mapped to relationships + identity promotion** |
| Auto-merge rules? | **Defined in Part 8** |
| Track candidates considered? | **Yes**, stored in merge_candidates.candidates_considered |
| Entity types? | **8 types**: Person, Company, Project, Location, Event, Document, Pet, Entity (fallback) |
| Dates? | **Not entities** — stored as `target_literal` on temporal relationships (ISO 8601) |
| AI agents? | **Not entities** — no durable identity; AI chat content lives in episodes |
| Concepts/activities/professions? | **Not entities** — discoverable via episode embedding search |
| Shared identifiers? | **Aliases can be shared** (is_shared=TRUE) |
| AI chat logs? | AI agents are NOT entities (no durable identity); extract human ideas/facts from chats |
| Unified vs split extraction? | **Split** (Graphiti-style: entities first, then relationships) |
| Bi-temporal model? | **Yes**: valid_at/invalid_at for real-world time, created_at for system time |
| Date format? | **ISO 8601** (YYYY-MM-DD, YYYY-MM for month precision) |
| Negation handling? | **None explicit** — LLM infers appropriate relationship type |

### Still Open

1. **Embedding model**: Same model for entities, relationships, and episodes? Or specialized?

2. **Exact thresholds**: Fine-tune confidence thresholds for auto-merge (currently 0.95).

3. **Batch job frequency**: How often to run collision detection? Community detection?

4. **Conflict resolution UX**: When conflicts detected, what's the interface for resolution?

---

## Appendix A: Prompts Reference

All prompts live in `prompts/graphiti/`. See `prompts/graphiti/README.md` for detailed documentation.

**Core pipeline prompts (in order):**

| Prompt | Purpose |
|--------|---------|
| `extract-entities.prompt.md` | Extract entities from episode content |
| `extract-relationships.prompt.md` | Extract relationships (uses resolved entity UUIDs) |
| `resolve-edges.prompt.md` | Deduplicate relationships against existing edges |
| `detect-contradictions.prompt.md` | Find and invalidate contradicted facts |

**Optional/deferred prompts:**

| Prompt | Purpose |
|--------|---------|
| `summarize-entity.prompt.md` | Entity summary generation (deferred) |

---

## Appendix B: References

- [Graphiti](https://github.com/getzep/graphiti) — Temporal knowledge graph framework
- [Cognee](https://github.com/topoteretes/cognee) — AI memory with graph + vector
- [Kuzu](https://kuzudb.com/) — Embedded graph database
- [Zep Paper](https://arxiv.org/abs/2501.13956) — Temporal Knowledge Graph Architecture for Agent Memory

---

*This document is the specification for the Cortex memory system. Implementation should follow the phases outlined in Part 9.*
