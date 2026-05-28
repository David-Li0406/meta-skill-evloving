# HelixDB Query Reference

Complete query documentation for Claude Code's memory system.

## Query Location
`db/queries.hx` (in the helix-memory repo root)

## Query Syntax Basics

HelixQL query structure:
```hx
QUERY QueryName(param: Type, ...) =>
    variable <- Operation
    RETURN variable
```

## Memory Operations

### StoreMemory
Create a new memory entry.

**Signature:**
```hx
QUERY StoreMemory(
    content: String,
    category: String,
    importance: U32,
    tags: String
) => ...
```

**Parameters:**
- `content` - Memory content (required)
- `category` - One of: "preference", "fact", "context", "decision", "task"
- `importance` - 1-10 rating
- `tags` - Comma-separated tags

**Returns:** Memory node

**Example Usage:**
```json
{
    "content": "User prefers pytest for Python testing",
    "category": "preference",
    "importance": 8,
    "tags": "python,testing,tools"
}
```

**When to Use:**
- User expresses a preference
- Important fact discovered
- Decision made
- Context established
- Task created

### StoreMemoryEmbedding
Add vector embedding to existing memory for semantic search.

**Signature:**
```hx
QUERY StoreMemoryEmbedding(
    memory_id: ID,
    vector: [F64],
    content: String
) => ...
```

**Parameters:**
- `memory_id` - ID of the memory node
- `vector` - Embedding vector (array of floats)
- `content` - Copy of memory content

**Returns:** MemoryEmbedding node

**Example Usage:**
```json
{
    "memory_id": "mem_123",
    "vector": [0.1, 0.2, ..., 0.9],
    "content": "User prefers pytest for Python testing"
}
```

**When to Use:**
Immediately after creating a memory to enable semantic search.

**Note:** Generate embeddings using Claude's understanding of the content.

## Context Operations

### CreateContext
Create a new context for grouping memories.

**Signature:**
```hx
QUERY CreateContext(
    name: String,
    description: String,
    type: String
) => ...
```

**Parameters:**
- `name` - Context identifier
- `description` - What this context represents
- `type` - One of: "project", "session", "topic", "user"

**Returns:** Context node

**Example Usage:**
```json
{
    "name": "wordpress-plugin-dev",
    "description": "WordPress plugin development work",
    "type": "project"
}
```

**When to Use:**
- Starting new project
- Beginning session
- Creating topic area
- First use of system

### LinkMemoryToContext
Associate memory with a context.

**Signature:**
```hx
QUERY LinkMemoryToContext(
    memory_id: ID,
    context_id: ID
) => ...
```

**Parameters:**
- `memory_id` - Memory to link
- `context_id` - Target context

**Returns:** "success"

**Example Usage:**
```json
{
    "memory_id": "mem_123",
    "context_id": "ctx_wp_dev"
}
```

**When to Use:**
After storing memory that belongs to specific project/session/topic.

## Relationship Operations

### LinkRelatedMemories
Create relationship between two memories.

**Signature:**
```hx
QUERY LinkRelatedMemories(
    from_id: ID,
    to_id: ID,
    relationship: String,  // optional
    strength: U32          // optional
) => ...
```

**Parameters:**
- `from_id` - Source memory
- `to_id` - Target memory
- `relationship` - Edge type (see below)
- `strength` - 1-10 strength rating

**Available Edge Types:**
| Type | Direction | Use Case |
|------|-----------|----------|
| `related` | A ↔ B | Generic relationship (default) |
| `solves` | solution → problem | Link fix to bug |
| `solved_by` | problem → solution | Link bug to fix |
| `supersedes` | new → old | Replacement |
| `implies` | A → B | Logical implication |
| `contradicts` | A ↔ B | Conflict |
| `leads_to` | cause → effect | Causation |
| `supports` | evidence → claim | Evidence |

**Returns:** "success"

**Example Usage:**
```json
{
    "from_id": "sol_123",
    "to_id": "prob_456",
    "relationship": "solves",
    "strength": 9
}
```

**When to Use:**
- Memories on similar topics
- Sequential decisions
- Contradicting information
- Superseding updates
- **Problem-solution linking**

**CLI Equivalent:**
```bash
memory link sol_123 prob_456 --type solves
```

**Relationship Types:** See schema.md for edge properties.

## Search Operations

### SearchMemoriesBySimilarity
Find memories semantically similar to query.

**Signature:**
```hx
QUERY SearchMemoriesBySimilarity(
    query_vector: [F64],
    k: I64
) => ...
```

**Parameters:**
- `query_vector` - Embedding of search query
- `k` - Number of results to return

**Returns:** Array of memories (ranked by similarity)

**Example Usage:**
```json
{
    "query_vector": [0.15, 0.23, ..., 0.87],
    "k": 5
}
```

**When to Use:**
- Session start (find relevant past context)
- User mentions topic (recall related info)
- Similar problem encountered
- General context retrieval

**Workflow:**
1. Generate embedding for search query
2. Execute SearchMemoriesBySimilarity
3. Review results by importance
4. Follow RelatesTo edges for more context

## Retrieval Operations

### GetAllMemories
Retrieve all stored memories.

**Signature:**
```hx
QUERY GetAllMemories() => ...
```

**API Call:**
```bash
curl -X POST http://localhost:6969/GetAllMemories \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Returns:**
```json
{
  "memories": [
    {
      "id": "...",
      "category": "preference",
      "content": "...",
      "importance": 8,
      "tags": "...",
      "timestamp": null,
      "label": "Memory"
    }
  ]
}
```
Returns empty array `{"memories": []}` when no memories exist.

**When to Use:**
- System overview
- Debugging
- Export/backup
- Memory audit

**Warning:** May return large dataset.

**Python Example:**
```python
from hooks.common import get_all_memories
memories = get_all_memories()  # Returns list of dicts
```

### GetMemoriesInContext
Get all memories belonging to specific context.

**Signature:**
```hx
QUERY GetMemoriesInContext(context_id: ID) => ...
```

**Parameters:**
- `context_id` - Target context

**Returns:** Array of memories in context

**Example Usage:**
```json
{
    "context_id": "ctx_wp_dev"
}
```

**When to Use:**
- Loading project-specific memories
- Session continuation
- Topic exploration

### GetRelatedMemories
Follow RelatesTo edges from a memory.

**Signature:**
```hx
QUERY GetRelatedMemories(memory_id: ID) => ...
```

**Parameters:**
- `memory_id` - Source memory

**Returns:** Array of related memories

**Example Usage:**
```json
{
    "memory_id": "mem_123"
}
```

**When to Use:**
- Exploring memory graph
- Finding related context
- Decision tracing

### GetMemory
Retrieve specific memory by ID.

**Signature:**
```hx
QUERY GetMemory(id: ID) => ...
```

**Parameters:**
- `id` - Memory node ID

**Returns:** Memory node

**When to Use:**
Direct access to known memory.

### GetContext
Retrieve specific context by ID.

**Signature:**
```hx
QUERY GetContext(id: ID) => ...
```

**Parameters:**
- `id` - Context node ID

**Returns:** Context node

**When to Use:**
Direct access to known context.

### GetAllContexts
List all contexts.

**Signature:**
```hx
QUERY GetAllContexts() => ...
```

**Returns:** Array of all Context nodes

**When to Use:**
- Session start (pick context)
- Context overview
- System audit

### GetMemoryEmbedding
Get embedding for specific memory.

**Signature:**
```hx
QUERY GetMemoryEmbedding(memory_id: ID) => ...
```

**Parameters:**
- `memory_id` - Source memory

**Returns:** MemoryEmbedding node

**When to Use:**
- Debugging embeddings
- Vector analysis
- Similarity comparisons

## Common Query Patterns

### Pattern 1: Store Complete Memory
```
1. StoreMemory(content, category, importance, tags)
   -> Returns memory with ID
2. StoreMemoryEmbedding(memory_id, vector, content)
   -> Links embedding
3. LinkMemoryToContext(memory_id, context_id)
   -> Associates with context
```

### Pattern 2: Session Start
```
1. GetAllContexts()
   -> Pick relevant context
2. GetMemoriesInContext(context_id)
   -> Load project memories
3. SearchMemoriesBySimilarity(session_topic_vector, 5)
   -> Find related info
```

### Pattern 3: Contextual Recall
```
1. SearchMemoriesBySimilarity(query_vector, 10)
   -> Get candidates
2. For each result:
   GetRelatedMemories(memory_id)
   -> Expand context
3. Filter by importance >= threshold
```

### Pattern 4: Graph Exploration
```
1. GetMemory(id)
   -> Start point
2. GetRelatedMemories(id)
   -> First-degree connections
3. For each related:
   GetRelatedMemories(related_id)
   -> Second-degree connections
```

## Query Execution

### Via API (When Deployed)
```bash
curl -X POST http://localhost:6969/query/StoreMemory \
  -H "Content-Type: application/json" \
  -d '{
    "content": "User prefers pytest",
    "category": "preference",
    "importance": 8,
    "tags": "python,testing"
  }'
```

### Via Python SDK (Future)
```python
from helix import Helix

helix = Helix("http://localhost:6969")

memory = helix.StoreMemory(
    content="User prefers pytest",
    category="preference",
    importance=8,
    tags="python,testing"
)
```

### Via Helper Script
```bash
python scripts/memory_helper.py store \
  --content "User prefers pytest" \
  --category "preference" \
  --importance 8 \
  --tags "python,testing"
```

## Query Optimization

### Use Specific Queries
❌ `GetAllMemories()` then filter in code
✅ `GetMemoriesInContext(id)` or `SearchMemoriesBySimilarity()`

### Limit Results
Always specify `k` parameter in searches:
```hx
SearchMemoriesBySimilarity(query_vector, 5)  // Top 5 only
```

### Follow Edges Selectively
❌ Get all memories then find relationships
✅ Use `GetRelatedMemories()` to traverse graph

### Cache Context IDs
Store frequently-used context IDs to avoid `GetAllContexts()` calls.

## Error Handling

### Common Errors

**Unknown ID:**
- Error: Node not found
- Cause: Invalid memory_id or context_id
- Fix: Verify ID exists with `GetMemory()` or `GetContext()`

**Type Mismatch:**
- Error: Expected Type, got Type
- Cause: Wrong parameter type
- Fix: Check query signature

**Missing Parameters:**
- Error: Required parameter missing
- Fix: Provide all required parameters

**Connection Failed:**
- Error: Cannot connect to database
- Cause: DB not running
- Fix: `helix push dev`

## Future Queries (Planned)

These queries are not yet implemented but planned:

- `UpdateMemoryImportance(id, new_importance)` - Adjust importance
- `UpdateMemoryTags(id, new_tags)` - Update tags
- `DeleteMemory(id)` - Remove memory
- `GetMemoriesByCategory(category)` - Filter by category
- `GetImportantMemories(min_importance)` - High-priority only
- `SearchMemoriesByTags(tag)` - Tag-based search
- `GetRecentMemories(since_timestamp)` - Time-based filter

To add these, edit `db/queries.hx` and rebuild with `helix push dev`.
