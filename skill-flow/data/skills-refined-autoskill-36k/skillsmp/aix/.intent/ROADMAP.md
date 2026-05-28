# aix Roadmap

## Current Status (v0.1)

aix provides AI session intelligence for Cursor conversations:
- Direct parsing from Cursor's SQLite database
- Exports raw sessions to `~/nexus/home/sessions/` for git-tracked durability
- Imports into `aix.db` for analysis and querying
- Extracts rich metadata: model used, capabilities, linter errors, file references, code blocks
- Message-level embeddings with semantic search

## Planned: Conversation Chunking

### Problem
Currently we embed at the message level, which is useful for finding specific exchanges.
However, for higher-level analysis (e.g., "what projects did I work on last week?",
"summarize my coding patterns"), we need conversation-level or cluster-level embeddings.

### Approach: Temporal Splitting (from eve)

Adopt the temporal splitting pattern from `eve`:
- **Gap Threshold**: 3 hours (10800 seconds) between messages signals end of a "conversation"
- A single Cursor session may contain multiple logical conversations
- Group sequential messages within the gap threshold into conversation chunks

### Implementation Plan

1. **Add `conversations` table**:
   ```sql
   CREATE TABLE conversations (
       id TEXT PRIMARY KEY,
       session_id TEXT NOT NULL REFERENCES sessions(id),
       start_message_id TEXT REFERENCES messages(id),
       end_message_id TEXT REFERENCES messages(id),
       start_time INTEGER,
       end_time INTEGER,
       message_count INTEGER,
       token_estimate INTEGER,
       summary TEXT
   );
   ```

2. **Chunking logic** (in sync or as post-processing):
   - Sort messages by timestamp within session
   - Split when gap > 3 hours
   - Assign conversation IDs

3. **Conversation embeddings**:
   - Concatenate messages in a conversation (respecting token limits)
   - Generate embedding for the chunk
   - Store in embeddings table with `entity_type = 'conversation'`

4. **Search enhancement**:
   - `aix search --level message|conversation|session`
   - Default to message for specific queries
   - Use conversation for broader context

### Token Splitting Alternative

For very long conversations, also support token-based splitting:
- Split at ~4000 tokens (leaving room for query in context)
- Maintain overlap (e.g., 200 tokens) for context continuity

### Priority

This is a **Phase 3** enhancement. Current message-level embeddings are sufficient
for initial semantic search. Conversation chunking will be valuable for:
- Generating session summaries
- Higher-level analysis queries
- Feeding context into AI for "what did we discuss about X" queries

## Other Planned Features

### Multi-Source Support
- Claude Desktop sessions
- ChatGPT exports
- OpenCode sessions
- Codex sessions

### Analysis Commands
- `aix analyze --project <name>` - Generate insights about a project
- `aix timeline` - Visual timeline of AI usage
- `aix patterns` - Identify coding patterns from sessions

### Integration
- Cartographer lenses for rich queries
- Export to Obsidian/markdown for knowledge management
