---
name: gobby-memory
description: Use this skill when you want to manage persistent memories across sessions, including storing, recalling, deleting, and listing memories.
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

Example: 
```
/gobby-memory remember Always use pytest fixtures for test setup
```
→ `create_memory(content="Always use pytest fixtures for test setup", tags="testing")`

Example: 
```
/gobby-memory remember [critical] Never commit .env files
```
→ `create_memory(content="Never commit .env files", tags="critical,security", importance="0.9")`

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

Example: 
```
/gobby-memory recall testing best practices
```
→ `search_memories(query="testing best practices")`

Example: 
```
/gobby-memory recall tag:security
```
→ `search_memories(tags_any="security")`

### `/gobby-memory forget <memory-id>` - Delete a memory
Call `gobby-memory.delete_memory` with:
- `memory_id`: (required) The memory ID to delete

Example: 
```
/gobby-memory forget mm-abc123
```
→ `delete_memory(memory_id="mm-abc123")`

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

Example: 
```
/gobby-memory list
```
→ `list_memories(limit="20")`