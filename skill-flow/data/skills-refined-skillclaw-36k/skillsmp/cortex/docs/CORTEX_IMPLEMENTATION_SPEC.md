---
summary: "Implementation spec for Cortex - remaining work items"
read_when:
  - Implementing Cortex features
  - Planning next work items
  - Understanding what's done vs remaining
---
# Cortex Implementation Spec

This document tracks implementation status and remaining work items. For architectural vision, see `ARCHITECTURE_EVOLUTION.md`.

**Last updated:** January 2026

---

## Decisions (Locked In)

| Decision | Rationale |
|----------|-----------|
| **Keep `analyses` terminology** | Indicative of LLM doing real intelligence work. No rename to "extractions." |
| **Hybrid search across ALL events** | Skills stored as generic events, search should work across all event types |
| **Single-event segments for metadata** | AIX metadata → single-event segment → facets on ingestion |
| **Defer routing decision logic** | Build the search layer first, tune routing thresholds later |
| **Defer freshness scoring** | Nice to have, not blocking |
| **Defer memory synthesis** | Needs more design |

---

## Phase 1: Foundation — ✅ COMPLETE

### 1.1 Rename comms → cortex ✅
- CLI binary renamed to `cortex`
- `cmd/cortex/main.go` exists
- Module updated

### 1.2 Rename conversations → segments ✅
- Schema uses `segments`, `segment_definitions`, `segment_events`
- Code updated throughout

### 1.3 Checkpoint tables ✅
- Not using separate checkpoint tables
- Using segments + analyses instead

---

## Phase 2: Live Sync — ✅ COMPLETE

### 2.1 iMessage watcher ✅
- `cortex watch imessage` implemented
- Uses fsnotify on chat.db
- Debounce + auto-sync working

### 2.2 AIX file watcher ✅
- `cortex watch aix` implemented
- Watches aix.db for changes (respects `AIX_DB_PATH`)
- Optional metadata extraction after sync

### 2.3 Auto-sync pipeline ✅
- AIX adapter syncs messages + metadata
- `metadata_json` column populated
- `cortex extract aix-metadata` extracts facets

---

## Phase 3: Skills + Hybrid Search — ✅ COMPLETE

### 3.1 Document indexing ✅
- `cortex documents index` scans `~/nexus/skills/`
- Indexes SKILL.md files into `document_heads`
- Creates events with `channel='skill'`

### 3.2 FTS5 index ✅
- `events_fts` virtual table exists
- Triggers keep FTS in sync on INSERT/UPDATE/DELETE
- Porter stemming + unicode tokenization

### 3.3 Hybrid search API ✅
- `cortex search` — semantic search over segments
- `cortex route` — routing candidates over segments
- `cortex documents search` — document search
- Vector + lexical scoring
- Channel filtering supported

---

## Phase 4: AIX Metadata + Turn Handling — ✅ COMPLETE

### 4.1 Single-event segments ✅
- `single_event` definition seeded (channel-agnostic)
- `single_event` strategy implemented in `internal/chunk/chunk.go`

### 4.2 AIX metadata → facets ✅
- `cortex extract aix-metadata` command
- Extracts: `file_reference`, `tool_invocation`, `mode`, `capability`
- Implementation in `internal/adapters/aix_facets.go`

### 4.3 Turn-pair segments ✅
- `turn_pair` chunking strategy implemented
- `ai_turn_pair` definition seeded via `cortex chunk seed`

### 4.4 Turn quality analysis ✅
- `turn_quality_v1` analysis type seeded
- `cortex extract turn-quality` command enqueues jobs
- Prompt: `prompts/checkpoint-feedback-v1.prompt.md`
- Output facets: `turn_sentiment`, `turn_correction`, `turn_frustration`, `turn_praise`, `turn_acceptance`, `turn_quality_band`, `turn_quality_score`

---

## Phase 5: Temporal Query — ❌ NOT BUILT

### 5.1 Daily cross-channel segments
- `daily` or `time_window` strategy needed
- Create one segment per day across all channels

### 5.2 Temporal query API
- `cortex timeline` command (basic version may exist)
- Group by day/hour/segment

---

## Deferred / Future Work

### Routing Infrastructure (Partial)
- Search API + `cortex route` implemented
- Candidate scoring + thresholds still needed
- Freshness scoring (file state hashes) still needed

### Memory Synthesis
- Sequential processing of facets → MEMORY.md
- Conflict/contradiction handling
- Storage format decisions

---

## Remaining Work (Prioritized)

### High Priority
1. **Routing decision logic** — Scoring, thresholds, ambiguity handling
2. **Freshness scoring** — File state hashes for staleness
3. **Daily segments** — Cross-channel daily grouping

### Medium Priority
4. **Timeline CLI** — Better temporal queries

### Low Priority / Deferred
5. **Memory synthesis** — Sequential compaction and MEMORY.md rendering

---

*See ARCHITECTURE_EVOLUTION.md for architectural vision and full backlog.*
