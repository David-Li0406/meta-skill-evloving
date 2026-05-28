# Amnesia

A dead-simple memory system for AI coding assistants. **One Python script, zero config.**

## Quick Install

```bash
# Install uv (required)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone directly to your skills folder
git clone https://github.com/youruser/amnesia.git ~/.config/opencode/skills/amnesia

# Make scripts executable
chmod +x ~/.config/opencode/skills/amnesia/*.py ~/.config/opencode/skills/amnesia/*.sh
```

The database is created automatically on first use (pass `--init`).

## What It Does

- **Semantic search** - Find memories by meaning ("container issues" finds "Docker networking")
- **Save conversations** - Run `/sum` to save the current chat
- **Works offline** - Everything runs locally, no API keys needed

## Usage

### In Your AI Assistant

Just ask naturally:
> "Do you remember how we fixed the CORS issue?"

Or save the conversation:
> `/sum`

### Command Line

```bash
# Initialize database
~/.config/opencode/skills/amnesia/save.py init

# Search memories
~/.config/opencode/skills/amnesia/save.py query "authentication bug"
~/.config/opencode/skills/amnesia/save.py query "docker networking" --limit 10

# Save a memory (full conversation is extracted automatically from session)
echo "Summary of what we did..." | ~/.config/opencode/skills/amnesia/save.py save \
    --id "ses_abc123" \
    --title "Auth Fix" \
    --tags "auth,bug"
```

## How It Works

```
Save: /sum → save.py → opencode export → SQLite + embeddings
Query: "remember..." → save.py query → semantic search → results
```

The full conversation is automatically extracted from the opencode session - you only provide the summary.

## Database

**Location**: `~/amnesia/memories.db`

Override with environment variable:
```bash
export AMNESIA_DB="/path/to/custom/memories.db"
```

### Schema

```sql
-- Text content
memories (
    id TEXT PRIMARY KEY,          -- session ID
    title TEXT NOT NULL,
    content TEXT NOT NULL,        -- summary (used for search)
    full_content TEXT,            -- full conversation transcript
    tags TEXT,                    -- comma-separated
    created_at TEXT,
    updated_at TEXT
)

-- Vector embeddings for semantic search
memories_vec (
    id TEXT PRIMARY KEY,
    embedding FLOAT[768]          -- all-mpnet-base-v2
)
```

- `content`: The summary (indexed for semantic search)
- `full_content`: Full conversation (stored for reference, not indexed)

## Files

```
amnesia/
├── SKILL.md      # Skill definition (read by AI)
├── save.py       # Main script: save, query, init
└── README.md     # This file
```

## Dependencies

- **Required**: [uv](https://github.com/astral-sh/uv) (manages Python dependencies automatically)
- **Required**: opencode CLI (for session export)
