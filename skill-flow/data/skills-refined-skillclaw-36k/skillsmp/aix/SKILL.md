---
name: aix
description: AI session intelligence - search and analyze your AI conversation history from Cursor, Claude Code CLI, Codex, Claude Desktop, and OpenCode with semantic search via embeddings
homepage: https://github.com/Napageneral/aix
metadata: {"nexus":{"emoji":"🧠","os":["darwin","linux"],"requires":{"bins":["aix"]},"install":[{"id":"brew","kind":"brew","formula":"Napageneral/tap/aix","bins":["aix"],"label":"Install via Homebrew"},{"id":"go","kind":"shell","script":"go install github.com/Napageneral/aix/cmd/aix@latest","bins":["aix"],"label":"Install via Go"}]}}
---

# aix 🧠

AI session intelligence - search and analyze your AI conversation history from multiple sources. Reads directly from AI tool databases, exports raw sessions to `~/nexus/home/sessions/` for durability, and stores conversations in a queryable SQLite database with support for semantic search via embeddings.

## Supported Sources

| Source | Tool | Data Location | Status |
|--------|------|---------------|--------|
| `cursor` | Cursor IDE | Cursor's SQLite database | Full messages |
| `claude-code` | Claude Code CLI | `~/.claude/projects/` | Full messages |
| `codex` | Anthropic Codex CLI | `~/.codex/sessions/` | Full messages |
| `opencode` | OpenCode | `~/.local/share/opencode/storage/` | Full messages |
| `claude` | Claude Desktop | `~/Library/Application Support/Claude/` | Metadata only* |

*Claude Desktop stores messages in LevelDB - currently only session metadata is extracted.

## Quick Start

```bash
aix init                              # Initialize config and database
aix sync --all                        # Sync from ALL sources
aix sync --source cursor              # Or sync from specific source
aix sessions                          # List all sessions
aix show <session-id>                 # View session details
aix stats                             # Show statistics with source breakdown
```

## Commands

### Sync & Import

| Command | Description |
|---------|-------------|
| `aix sync --all` | Sync from all available sources |
| `aix sync --source cursor` | Sync from Cursor |
| `aix sync --source claude-code` | Sync from Claude Code CLI |
| `aix sync --source codex` | Sync from Codex CLI |
| `aix sync --source claude` | Sync from Claude Desktop |
| `aix sync --source opencode` | Sync from OpenCode |
| `aix sync --no-export` | Skip export (not recommended) |
| `aix sync --export-path <path>` | Custom export location |

### Browse & Query

| Command | Description |
|---------|-------------|
| `aix sessions [--source <s>] [--project <p>] [--today]` | List sessions with filters |
| `aix show <session-id>` | Show full session with messages (partial ID ok) |
| `aix db query <sql>` | Run raw SQL queries (SELECT/WITH only) |
| `aix stats` | Show database statistics with source breakdown |

### Semantic Search (requires GEMINI_API_KEY)

| Command | Description |
|---------|-------------|
| `aix embed [--model <m>] [--limit <n>]` | Generate embeddings for messages |
| `aix compute embed` | High-throughput embedding via taskengine |
| `aix compute status` | Show compute queue status |
| `aix search <query> [--project <p>]` | Semantic search across messages |

Default embedding model: `text-embedding-004`

## Examples

```bash
# Initialize and sync from all sources
aix init
aix sync --all

# Browse sessions
aix sessions                          # All sessions (default limit 50)
aix sessions --source claude-code     # Filter by source
aix sessions --source cursor --today  # Cursor sessions from today
aix sessions --project nexus -n 100   # Filter by project, limit 100

# View a session (supports partial ID)
aix show a46d032c                     # Partial ID works

# Query database directly
aix db query "SELECT source, COUNT(*) as sessions FROM sessions GROUP BY source"
aix db query "SELECT model, COUNT(*) FROM sessions WHERE model != '' GROUP BY model ORDER BY COUNT(*) DESC"
aix db query "SELECT * FROM messages WHERE content LIKE '%error%' LIMIT 5"

# Semantic search (after generating embeddings)
export GEMINI_API_KEY=your-key
aix embed --limit 10000               # Embed first 10k messages
aix search "how to fix TypeScript errors"
```

## Useful Queries

```sql
-- Sessions by source
SELECT source, COUNT(*) as sessions, SUM(message_count) as msgs 
FROM sessions GROUP BY source ORDER BY sessions DESC;

-- Model usage by source
SELECT source, model, COUNT(*) as sessions FROM sessions 
WHERE model IS NOT NULL GROUP BY source, model ORDER BY sessions DESC;

-- Recent activity by day
SELECT date(created_at/1000, 'unixepoch') as day, source, COUNT(*) as sessions 
FROM sessions WHERE created_at > 0 GROUP BY day, source ORDER BY day DESC LIMIT 30;

-- Longest sessions
SELECT id, source, project, model, message_count, datetime(created_at/1000, 'unixepoch') as created 
FROM sessions ORDER BY message_count DESC LIMIT 10;
```

## Data Storage

| Path | Purpose |
|------|---------|
| `~/.config/aix/config.json` | Configuration |
| `~/Library/Application Support/aix/aix.db` | Analysis database (macOS) |
| `~/.local/share/aix/aix.db` | Analysis database (Linux) |
| `~/nexus/home/sessions/cursor/` | Exported Cursor sessions |
| `~/nexus/home/sessions/claude-code/` | Exported Claude Code CLI sessions |
| `~/nexus/home/sessions/codex/` | Exported Codex sessions |
| `~/nexus/home/sessions/claude/` | Exported Claude Desktop sessions |
| `~/nexus/home/sessions/opencode/` | Exported OpenCode sessions |

## Source-Specific Notes

### Cursor
- Handles both old format (pre-March 2025) and new sharded format
- Full message content and rich metadata extraction
- Model tracked from `modelConfig.modelName`

### Claude Code CLI (`~/.claude/projects/`)
- JSONL format with user/assistant message events
- Full message content extracted
- Model tracked from assistant message metadata
- Includes 100+ sessions for active users

### Codex CLI (`~/.codex/sessions/`)
- JSONL format with `session_meta` and `response_item` events
- Model tracked from `model_provider` field
- Full message content extracted

### Claude Desktop
- Session metadata from JSON files (title, model, timestamps)
- Full messages stored in LevelDB (not currently extracted)

### OpenCode
- JSON files for sessions, messages, and parts
- Full message content assembled from parts

## Bootstrap (for AI agents)

```bash
# Check if installed
which aix && aix version --json

# Build from source
cd ~/nexus/home/projects/aix
go build -o aix ./cmd/aix/
./aix init
./aix sync --all

# Verify
./aix stats
./aix db query "SELECT source, COUNT(*) as sessions FROM sessions GROUP BY source"
```

## Dependencies

- Go 1.22+
- SQLite3 (via go-sqlite3)
- For embeddings: `GEMINI_API_KEY` environment variable

## Related

- [taskengine](https://github.com/Napageneral/taskengine) - Durable job queue used for high-throughput embeddings
- [.intent/ROADMAP.md](.intent/ROADMAP.md) - Future plans including conversation chunking
