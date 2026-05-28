---
name: gobby-memory
description: Use this skill when managing persistent memories across sessions, including storing, searching, deleting, updating, and listing memories.
---

# /gobby-memory - Memory Management Skill

This skill manages persistent memories via the gobby-memory MCP server. Parse the user's input to determine which subcommand to execute.

## Subcommands

### `/gobby-memory remember <content>` - Store a memory
Call `gobby-memory.create_memory` with:
- `content`: (required) The memory content to store
- `memory_type`: Optional type categorization
- `importance`: Importance score 0-1 (default 0.5, use higher for critical facts)
- `tags`: Comma-separated tags (e.g., "testing,security")
- `project_id`: Optional project scope (defaults to current)

Example: `/gobby-memory remember Always use pytest fixtures for test setup`
→ `create_memory(content="Always use pytest fixtures for test setup", tags="testing")`

### `/gobby-memory recall <query>` - Search/recall memories
Call `gobby-memory.search_memories` with:
- `query`: Search query text
- `limit`: Max results (default 10)
- `min_importance`: Minimum importance threshold
- `tags_all`: Require all these tags (comma-separated)
- `tags_any`: Match any of these tags
- `tags_none`: Exclude these tags
- `project_id`: Optional project scope

Returns memories matching the query, ranked by relevance.

### `/gobby-memory forget <memory-id>` - Delete a memory
Call `gobby-memory.delete_memory` with:
- `memory_id`: (required) The memory ID to delete

### `/gobby-memory list` - List all memories
Call `gobby-memory.list_memories` with:
- `limit`: Max results (default 20)
- `memory_type`: Filter by type
- `min_importance`: Minimum importance threshold
- `tags_all`: Require all these tags
- `tags_any`: Match any of these tags
- `tags_none`: Exclude these tags
- `project_id`: Optional project scope

Returns all stored memories, most recent first.

### `/gobby-memory show <memory-id>` - Get memory details
Call `gobby-memory.get_memory` with:
- `memory_id`: (required) The memory ID to retrieve

Returns full memory details including content, tags, importance, and metadata.

### `/gobby-memory update <memory-id>` - Update a memory
Call `gobby-memory.update_memory` with:
- `memory_id`: (required) The memory ID to update
- `content`: New content (optional)
- `importance`: New importance score (optional)
- `tags`: New tags (optional)

### `/gobby-memory related <memory-id>` - Get related memories
Call `gobby-memory.get_related_memories` with:
- `memory_id`: (required) The memory ID to find relations for
- `limit`: Max results
- `min_similarity`: Minimum similarity threshold

Returns memories related via cross-references.

### `/gobby-memory stats` - Show memory statistics
Call `gobby-memory.memory_stats` to retrieve:
- Total memory count
- Memories by type
- Storage usage
- Recent activity

### `/gobby-memory export` - Export memory graph
Call `gobby-memory.export_memory_graph` with:
- `title`: Optional graph title
- `output_path`: Optional output file path
- `project_id`: Optional project scope

Exports memories as an interactive HTML knowledge graph.

## Response Format

After executing the appropriate MCP tool, present the results clearly:
- For remember/create: Confirm storage with memory ID
- For recall: List matching memories with ID, content snippet, and relevance
- For forget/delete: Confirm deletion
- For list: Display memories with ID, content, tags, and creation date
- For show: Full memory details
- For update: Confirm update
- For related: List related memories with similarity scores
- For stats: Show statistics in a readable summary
- For export: Confirm export with file path

## Tag Extraction

When storing memories, extract implicit tags from content:
- `[tag]` syntax → explicit tag
- `testing`, `test` → tag: testing
- `security`, `auth` → tag: security
- `workflow`, `process` → tag: workflow
- `code`, `implementation` → tag: code

## Error Handling

If the subcommand is not recognized, show available subcommands:
- remember, recall, forget, list, show, update, related, stats, export