# HelixDB Memory Hooks

Automatic memory reflection and storage system using Claude Code hooks.

## Overview

Three hooks work together to automatically manage long-term memory:

1. **Stop Hook** (`reflect_and_store.py`) - After I respond, analyzes conversation and stores important info
2. **UserPromptSubmit Hook** (`load_memories.py`) - Before processing, loads relevant memories as context
3. **SessionEnd Hook** (`session_summary.py`) - When session ends, creates summary

## Configuration

Hooks are configured in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [{"hooks": [{"type": "command", "command": "/path/to/helix-memory/hooks/reflect_and_store.py"}]}],
    "UserPromptSubmit": [{"hooks": [{"type": "command", "command": "/path/to/helix-memory/hooks/load_memories.py"}]}],
    "SessionEnd": [{"hooks": [{"type": "command", "command": "/path/to/helix-memory/hooks/session_summary.py"}]}]
  }
}
```

## Hook Scripts

### reflect_and_store.py (Stop Hook)

**When:** After Claude finishes responding

**What it does:**
- Reads conversation transcript (last 20 messages)
- Detects important information using pattern matching:
  - User preferences ("I prefer...", "always use...")
  - Decisions ("decided to...", "let's use...")
  - Facts ("I'm using...", "working on...")
  - Tasks ("need to...", "TODO...")
  - Context ("project uses...", "building a...")
- Stores to HelixDB with appropriate category and importance
- Generates embeddings for semantic search

**Pattern Detection:**
- **Preferences** (importance 8-10): "i prefer", "i like to", "always", "never use"
- **Decisions** (importance 7-9): "decided to", "let's use", "we'll go with", "chose to"
- **Context** (importance 6-8): "project uses", "working on", "building a"
- **Tasks** (importance 5-8): "need to", "todo", "next step", "blocker"
- **Facts** (importance 6-8): "i'm using", "my setup", "installed", "configured"

**Output:** "Stored N memories to long-term storage" (shown to user)

### load_memories.py (UserPromptSubmit Hook)

**When:** Before Claude processes user's message

**What it does:**
- Extracts keywords from user prompt
- Searches HelixDB for relevant memories
- Injects as additional context

### session_summary.py (SessionEnd Hook)

**When:** Session terminates

**What it does:**
- Analyzes full session transcript
- Extracts:
  - Topics discussed
  - Decisions made
  - Tasks completed
  - Outstanding items
- Creates session summary memory
- Stores with session context

## Data Flow

### Stop Hook Flow
```
User/Claude messages
    |
Transcript written to JSONL
    |
Stop hook triggered
    |
Parse last 20 messages
    |
Pattern matching analysis
    |
Store to HelixDB:
  - StoreMemory(content, category, importance, tags)
  - StoreMemoryEmbedding(memory_id, vector, content)
    |
Display summary to user
```

### UserPromptSubmit Hook Flow
```
User submits prompt
    |
Hook triggered BEFORE Claude sees it
    |
Extract keywords
    |
Search HelixDB
    |
Format as additional context
    |
Inject into prompt
    |
Claude processes with context loaded
```

## Dependencies

### Python Packages
```bash
pip install requests
```

### HelixDB
- Must be running at `http://localhost:6969`
- Start with: `memory start`

### Common Module
All hooks use `common.py` for shared functionality:
- `read_hook_input()` - Parse JSON from stdin
- `parse_transcript()` - Read conversation JSONL
- `extract_message_content()` - Get text from messages
- `store_memory()` - Store to HelixDB
- `store_memory_embedding()` - Store embeddings
- `generate_embedding()` - Create vectors via Ollama/Gemini

## Memory Categories

### preference (importance: 8-10)
User's personal preferences affecting all interactions

**Examples:**
- "I prefer concise responses"
- "Always use pytest for Python testing"
- "Never commit without running tests"

### decision (importance: 7-9)
Important technical or architectural decisions

**Examples:**
- "Decided to use HelixDB for memory storage"
- "Chose React over Vue for this project"
- "Going with PostgreSQL instead of MySQL"

### context (importance: 6-8)
Project or domain background information

**Examples:**
- "Working on WordPress plugin for event management"
- "Project uses Python 3.11+ with FastAPI"
- "Building a SaaS app for small businesses"

### task (importance: 5-8)
Ongoing work, TODOs, blockers

**Examples:**
- "Need to fix Docker build issue"
- "TODO: Add tests for authentication"
- "Blocked on API key from client"

### fact (importance: 6-8)
Factual information about environment, setup, tools

**Examples:**
- "Using Docker Desktop v28.5.1"
- "Development on macOS"
- "Editor: VS Code with Vim extension"

## Testing Hooks

### Test Stop Hook Manually
```bash
echo '{"transcript_path": "/path/to/transcript.jsonl", "session_id": "test-123", "cwd": "/home/user"}' | \
  python3 ./hooks/reflect_and_store.py
```

### Test UserPromptSubmit Hook
```bash
echo '{"prompt": "How do I test Python code?", "session_id": "test-123"}' | \
  python3 ./hooks/load_memories.py
```

### Test SessionEnd Hook
```bash
echo '{"transcript_path": "/path/to/transcript.jsonl", "session_id": "test-123", "cwd": "/home/user"}' | \
  python3 ./hooks/session_summary.py
```

## Debugging

### Enable Verbose Output
Hooks print to stderr. Check Claude Code logs or terminal output.

### Check If Hooks Are Running
Look for messages:
- "Stored N memories to long-term storage"
- "Session summary stored"

### Common Issues

**Hook not executing:**
- Check `~/.claude/settings.json` for correct paths
- Ensure scripts are executable: `chmod +x hooks/*.py`
- Verify Python 3 available: `python3 --version`

**HelixDB not accessible:**
- Start HelixDB: `memory start`
- Check status: `memory status`
- Verify port 6969: `curl http://localhost:6969/health`

**No memories stored:**
- Hooks silently skip if HelixDB unavailable
- Check stderr output for warnings
- Verify conversation has detectable patterns

## Files

```
hooks/
├── README.md                  # This file
├── common.py                  # Shared utilities
├── reflect_and_store.py       # Stop hook
├── load_memories.py           # UserPromptSubmit hook
└── session_summary.py         # SessionEnd hook
```

## Resources

- **HelixDB Docs:** https://docs.helix-db.com
- **Claude Code Hooks:** https://docs.anthropic.com/en/docs/claude-code/hooks
