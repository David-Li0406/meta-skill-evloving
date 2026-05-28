---
name: conversation-memory
description: Use this skill when the user references past conversations or when historical context from previous sessions would help solve the current problem.
---

# Conversation Memory Skill

This skill provides access to a searchable history of previous conversations stored in a vector database. It supports both **retrieving** past conversations via semantic search and **saving** new conversation summaries.

## When to Use This Skill

Invoke this skill when:

- **User references past conversations**: Phrases like "we discussed this before", "remember when", or "last time we talked about".
- **Recurring problems**: The user encounters an issue that might have been solved previously.
- **Context would be helpful**: Previous solutions, decisions, or architectural discussions could inform the current task.
- **User asks about their codebase**: Questions about past work, project history, or previous implementations.
- **Building on previous work**: Extending or modifying solutions from past conversations.

## Querying Memories

```bash
~/.config/opencode/skills/conversation-memory/query.sh --query "your search query"
```

### Query Parameters

- `--query TEXT` or `-q TEXT`: The search query (required).
  - Use natural language.
  - Be specific but not too narrow.
  - Examples: "fixing Docker networking", "Go error handling patterns", "setting up ChromaDB".

- `--limit NUMBER` or `-n NUMBER`: Number of results to return (default: 5).
  - More results = more context but also more noise.
  - Recommended: 3-5 for focused queries, 10+ for exploratory searches.

- `--full` or `-f`: Show full document content.
  - Without this flag, only previews (first 200 chars) are shown.
  - Use when you need to read the full conversation summary.

- `--help` or `-h`: Show help message.

## Saving Memories

To save a new conversation summary:

```bash
echo 'YOUR_SUMMARY_MARKDOWN' | ~/.config/opencode/skills/conversation-memory/save-summary.sh --title "Title"
```

### Save Parameters

- `--title TEXT` or `-t TEXT`: Title for the summary (optional but recommended).
- `--id ID`: Session ID (required).
- `--tags TEXT`: Comma-separated tags (optional).
- `--summary-file FILE`: Read summary from file instead of stdin.
- `--init`: Initialize database if it doesn't exist.

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

- **Database**: `~/.config/opencode/skills/conversation-memory/database`