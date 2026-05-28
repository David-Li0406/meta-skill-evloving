# aix 🧠

AI session intelligence - search and analyze your AI conversation history from multiple sources.

`aix` reads directly from AI harness databases (Cursor, Claude Code CLI, Codex CLI, Claude Desktop, OpenCode), exports raw sessions for durability, and provides queryable storage with semantic search capabilities.

## Features

- **Multi-source sync** - Cursor, Claude Code CLI, Codex CLI, Claude Desktop, OpenCode
- **Direct database access** - Reads directly from each tool's internal storage
- **Durable export** - Exports raw sessions to `~/nexus/home/sessions/` for git-tracking
- **Model tracking** - Captures which AI model was used for each session
- **Rich metadata extraction** - Capabilities, lints, file references, code blocks
- **Semantic search** - Find conversations by meaning using embeddings
- **Raw SQL queries** - Full access to your conversation data

## Installation

```bash
# Via Homebrew
brew install Napageneral/tap/aix

# Via Go
go install github.com/Napageneral/aix/cmd/aix@latest

# From source
git clone https://github.com/Napageneral/aix
cd aix
make install
```

## Quick Start

```bash
# Initialize and sync from all sources
aix init
aix sync --all                        # Sync from all available sources
aix sync --source cursor              # Or sync from specific source

# Browse your sessions
aix sessions --today
aix sessions --source claude-code     # Filter by source
aix show <session-id>
aix stats

# Query directly
aix db query "SELECT source, COUNT(*) as sessions FROM sessions GROUP BY source"
aix db query "SELECT model, COUNT(*) as sessions FROM sessions GROUP BY model ORDER BY sessions DESC"

# Semantic search (requires GEMINI_API_KEY)
export GEMINI_API_KEY=your-key
aix embed --limit 10000
aix search "how to fix TypeScript errors"
```

## Supported Sources

| Source | Tool | Data Location | Status |
|--------|------|---------------|--------|
| `cursor` | Cursor IDE | `~/Library/Application Support/Cursor/.../state.vscdb` | Full messages |
| `claude-code` | Claude Code CLI | `~/.claude/projects/` (JSONL files) | Full messages |
| `codex` | Anthropic Codex CLI | `~/.codex/sessions/` (JSONL files) | Full messages |
| `opencode` | OpenCode | `~/.local/share/opencode/storage/` | Full messages |
| `claude` | Claude Desktop | `~/Library/Application Support/Claude/claude-code-sessions/` | Metadata only* |

*Claude Desktop stores messages in LevelDB. Currently only session metadata (title, model, timestamps) is extracted.

### Coming Soon (PRs Welcome)

- **ChatGPT Desktop** - Files exist but use encrypted/proprietary format
- **Aider** - If you use it, let us know where sessions are stored
- **Continue** - VS Code extension

## Commands

| Command | Description |
|---------|-------------|
| `aix init` | Initialize config and database |
| `aix sync --source <src>` | Sync from source (cursor, claude-code, codex, claude, opencode) |
| `aix sync --all` | Sync from all available sources |
| `aix sessions` | List sessions (filters: --project, --source, --today, --week) |
| `aix show <id>` | View session details (partial ID ok) |
| `aix db query <sql>` | Run SQL queries (SELECT only) |
| `aix stats` | Show database statistics |
| `aix embed` | Generate embeddings for search |
| `aix search <query>` | Semantic search across messages |

All commands support `--json` for machine-readable output.

## Data Flow

```
Source DBs                   Export Path                    Analysis DB
───────────                  ───────────                    ───────────
Cursor DB (SQLite)  ──┐
Claude Code CLI     ──┼──►  ~/nexus/home/sessions/  ──►    aix.db
Codex CLI           ──┤        cursor/                     (queryable)
Claude Desktop      ──┤        claude-code/
OpenCode (JSON)     ──┘        codex/
                               claude/
                               opencode/
```

### Storage Locations

| Path | Purpose |
|------|---------|
| `~/nexus/home/sessions/` | Exported raw sessions (durable, git-tracked) |
| `~/Library/Application Support/aix/aix.db` | Analysis database (macOS) |
| `~/.local/share/aix/aix.db` | Analysis database (Linux) |

The `aix.db` can always be rebuilt from the exported sessions.

### Sample Stats

```
Sessions:        2,065
Messages:        223,615
File references: 15,351
Projects:        42
By source:
  cursor:      1,958
  claude-code: 100
  codex:       4
  opencode:    2
  claude:      1
```

## Requirements

- macOS or Linux
- Go 1.22+ (for building from source)
- At least one AI tool (Cursor, Claude Code CLI, Codex, Claude Desktop, or OpenCode)
- `GEMINI_API_KEY` (optional, for semantic search)

## Related

- [taskengine](https://github.com/Napageneral/taskengine) - Durable job queue for high-throughput embeddings

## License

MIT
