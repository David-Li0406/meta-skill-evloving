# aix - AI Session Intelligence

## Status: ✅ Working

`aix` is a CLI tool for analyzing AI conversation history from Cursor. It reads directly from Cursor's internal SQLite database and provides queryable storage with semantic search capabilities.

## What's Implemented

### Phase 1: Cursor Session Parser ✅
- [x] `aix init` - Initialize config and database
- [x] `aix sync --source cursor` - Parse exported JSON files
- [x] `aix sync --source cursor --direct` - **Read directly from Cursor's DB** (handles new sharded format)
- [x] `aix sessions` - List sessions with filters (--project, --today, --week)
- [x] `aix show <id>` - Show session with messages (partial ID matching)
- [x] `aix db query` - Run raw SQL queries
- [x] `aix stats` - Database statistics
- [x] `aix version` - Version info with --json support

**Rich metadata extraction:**
- Per-message capabilities (Cursor capability IDs)
- Linter errors from context
- File references (relevant files, recent locations)
- Code blocks (suggested/generated)
- UUIDv7 timestamp extraction for accurate message timing

### Phase 2: Semantic Search ✅
- [x] `aix embed` - Generate embeddings using Gemini API
- [x] `aix compute embed` - High-throughput embedding via taskengine
- [x] `aix compute status` - Queue status
- [x] `aix search <query>` - Cosine similarity search across embedded messages

### Data Stats (as of 2026-01-11)
- 1,958 sessions parsed
- 220,039 messages extracted
- 15,342 file references
- 41 projects identified
- Date range: Aug 2024 - Jan 2026

## Architecture

```
cmd/aix/main.go          # CLI entry point (cobra)
internal/
├── db/
│   ├── db.go            # Database operations (raw SQL, no ORM)
│   └── schema.sql       # SQLite schema
├── sync/
│   ├── cursor.go        # JSON file parser (old format)
│   └── cursor_db.go     # Direct DB parser (new format)
├── models/
│   └── session.go       # Data structures
├── gemini/
│   └── client.go        # Gemini API client for embeddings
└── embeddings/
    └── batcher.go       # Batched embedding requests
```

## Key Technical Details

### Cursor's Storage Format Evolution

**Old format (pre-March 2025):**
- All data in `composerData:uuid` key
- Messages inline in `conversation[]` array

**New format (post-March 2025):**
- Metadata in `composerData:uuid` with `fullConversationHeadersOnly[]`
- Message content in separate `bubbleId:composerId:bubbleId` keys
- ~230K bubble entries in Cursor's 10GB database

The `--direct` flag handles both formats automatically.

### Database Location
- macOS: `~/Library/Application Support/aix/aix.db`
- Linux: `~/.local/share/aix/aix.db`

### Environment Variables
- `GEMINI_API_KEY` - Required for embeddings/search
- `AIX_EMBED_MODEL` - Override embedding model (default: text-embedding-005)

## Future Ideas

- [ ] Export command for data portability
- [ ] Claude/ChatGPT session import
- [ ] Intent extraction / conversation summarization
- [ ] Integration with cartographer for session → skill mapping
- [ ] Time-series analysis of coding patterns
