---
name: conversation-memory
description: Use this skill when the user references past conversations or when historical context from previous sessions would help solve the current problem.
---

# Conversation Memory Skill

This skill provides access to a local-first memory system for AI coding assistants, allowing for the storage and retrieval of conversation summaries using semantic search. It supports both **retrieving** past conversations and **saving** new conversation summaries.

## When to Use This Skill

Invoke this skill when:

- **User references past conversations**: Phrases like "we discussed this before", "remember when", "last time we talked about"
- **Recurring problems**: The user encounters an issue that might have been solved previously
- **Building on previous work**: Extending or modifying solutions from past conversations
- **User asks about history**: Questions about past work, decisions, or implementations

## Querying Memories

To retrieve past conversations, use the following command:

```bash
~/.config/opencode/skills/conversation-memory/query.sh --query "your search query" [--count N] [--verbose]
```

### Query Parameters

- `--query TEXT` or `-q TEXT`: The search query (required)
- `--count NUMBER` or `-n NUMBER`: Number of results to return (default: 5)
- `--verbose` or `-v`: Show full document content
- `--help` or `-h`: Show help message

### Example Queries

```bash
# User: "I'm getting a CORS error, have we dealt with this before?"
~/.config/opencode/skills/conversation-memory/query.sh --query "CORS error" --count 3

# User: "What database did we choose for the user service?"
~/.config/opencode/skills/conversation-memory/query.sh --query "database choice user service" --count 5 --verbose
```

## Saving Memories

To save a new conversation summary, use the following command:

```bash
echo 'YOUR_SUMMARY_MARKDOWN' | ~/.config/opencode/skills/conversation-memory/save-summary.sh --title "Title"
```

### Save Parameters

- `--title TEXT` or `-t TEXT`: Title for the summary (optional but recommended)
- `--tags TEXT`: Comma-separated tags (optional)
- `--help` or `-h`: Show help message

### Summary Format

When saving a summary, use this structure:

```markdown
# Descriptive Title

## Date
YYYY-MM-DD

## Project Context
- **Working Directory**: /path/to/project
- **Project Root**: /path/to/project

## Summary
2-3 paragraph summary of what was discussed and key decisions made.

## Key Topics
- Topic 1
- Topic 2

## Technical Details
Important technical information, code patterns, or solutions.

## Code Changes
List of files modified with brief descriptions.

## Outcome
What was the result? Was the problem solved?

## Tags
python, docker, authentication, bug-fix
```

## How It Works

1. User Query
2. Bash Script (query.sh)
3. VectorCode CLI
4. ChromaDB (local instance)
5. Semantic Search Results

The skill wraps the VectorCode CLI tool, queries a local ChromaDB database, and uses semantic embeddings to return results sorted by relevance.

## Database Information

- **Database Location**: `~/.local/share/vectorcode/chromadb/chroma.sqlite3`
- **Summaries**: `~/codecompanion-history/summaries/*.md`
- **Embedding Model**: SentenceTransformer (all-MiniLM-L6-v2)

## Best Practices

1. **Start broad, then narrow**: Begin with general queries, then refine based on results.
2. **Use verbose mode selectively**: Only when you need full context to answer the user's question.
3. **Cite your sources**: Tell the user which conversation(s) you found the information in.
4. **Verify information**: Past solutions might be outdated; always validate before applying.

## Example Workflow

```
User: "I'm stuck on the same authentication bug we had last month"

Step 1: Search for relevant conversations
$ ./query.sh --query "authentication bug fix" --count 5

Step 2: Review results, identify the most relevant conversation
> Result 3 seems most relevant (Path: 1763841695.md)

Step 3: Read full summary if needed
$ cat ~/codecompanion-history/summaries/1763841695.md

Step 4: Apply the solution or adapt it to current context

Step 5: Inform user
> "I found a similar issue we solved in conversation 1763841695. 
   The problem was related to session token expiration. 
   Here's what we did..."
```

---

**Status**: Production ready  
**Location**: `~/.config/opencode/skills/conversation-memory/`  
**Last Updated**: 2026-01-20