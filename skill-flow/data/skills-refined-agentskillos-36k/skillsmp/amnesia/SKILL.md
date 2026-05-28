---
name: amnesia
description: Search and save conversation memories using semantic search. Use this skill when the user mentions past conversations, asks "do you remember", or when historical context from previous sessions would help solve the current problem.
---

# Amnesia - Conversation Memory Skill

A simple, local-first memory system for AI coding assistants. Store and retrieve conversation summaries using semantic search (vector embeddings).

## When to Use This Skill

Invoke this skill when:

- **User references past conversations**: Phrases like "we discussed this before", "remember when", "last time"
- **Recurring problems**: The user encounters an issue that might have been solved previously
- **Building on previous work**: Extending or modifying solutions from past conversations
- **User asks about history**: Questions about past work, decisions, or implementations

## Querying Memories

```bash
~/.config/opencode/skills/amnesia/save.py query "search terms" [--limit N] [--full]
```

### Query Parameters

- First argument: Search query (required)
- `--limit N` or `-n N`: Number of results (default: 5)
- `--full` or `-f`: Show full conversation content (not just summary)
- `--init`: Initialize database if it doesn't exist

### Examples

```bash
# Semantic search - finds by meaning
~/.config/opencode/skills/amnesia/save.py query "container networking"
~/.config/opencode/skills/amnesia/save.py query "login flow"

# More results
~/.config/opencode/skills/amnesia/save.py query "authentication" --limit 10
```

## Saving Memories

Memories are saved using the session ID. The full conversation is automatically extracted from opencode.

```bash
echo 'YOUR_SUMMARY_MARKDOWN' | ~/.config/opencode/skills/amnesia/save.py save \
    --id "SESSION_ID" \
    --title "Title" \
    --tags "tag1,tag2"
```

### Save Parameters

- `--id ID`: Session ID (required)
- `--title TEXT` or `-t TEXT`: Title for the memory (required)
- `--tags TEXT`: Comma-separated tags (optional)
- `--summary-file FILE`: Read summary from file instead of stdin
- `--init`: Initialize database if it doesn't exist

## /sum Command

When the user runs `/sum`, summarize and save the conversation. The full conversation transcript is automatically extracted - you only need to write the summary.

## How It Works

```
save.py
    ↓
opencode export → Extract conversation
    ↓
sentence-transformers → Generate embeddings
    ↓
sqlite-vec → Store and search
```

## Database Location

- **Database**: `~/amnesia/memories.db`
- **Override**: Set `AMNESIA_DB` environment variable

## Best Practices

1. **Search first**: Before asking the user to re-explain, search for relevant memories
2. **Use natural language**: "how did we handle errors" works better than "error handling"
3. **Cite sources**: Tell the user which memory you found the information in
4. **Verify information**: Past solutions might be outdated

## Dependencies

- **Required**: [uv](https://github.com/astral-sh/uv) for running Python with dependencies
- **Required**: opencode CLI (for session export)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```
