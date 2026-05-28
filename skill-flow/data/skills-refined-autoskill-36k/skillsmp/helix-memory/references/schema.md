# HelixDB Memory Schema Reference

Complete schema definition for Claude Code's long-term memory system.

## Schema Location
`db/schema.hx` (in the helix-memory repo root)

## Node Types

### N::Memory
Stores individual memory entries.

**Fields:**
- `content: String` - The actual memory content (required)
- `category: String` - Category: "preference", "fact", "context", "decision", "task" (required)
- `timestamp: Date` - When created, set to NOW automatically
- `importance: U32` - Importance level 1-10 (required)
- `tags: String` - Comma-separated tags for organization (required)

**Example:**
```hx
N::Memory {
    content: "User prefers concise responses",
    category: "preference",
    timestamp: NOW,
    importance: 9,
    tags: "communication,style"
}
```

**Usage Notes:**
- Always set importance appropriately (see skill.md for guidelines)
- Use consistent tag naming
- Keep content concise but complete
- Use category to organize different types of info

### V::MemoryEmbedding
Stores vector embeddings for semantic search. Vector type declared with `V::`.

**Fields:**
- `content: String` - Copy of memory content for context

**Vector Storage:**
Vectors are stored via `AddV()` in queries, not as schema fields.

**Example:**
```hx
V::MemoryEmbedding {
    content: "User prefers concise responses"
}
```

**Usage Notes:**
- Always create embedding for every memory
- Content copy enables context when searching
- Link to Memory via HasEmbedding edge

### N::Context
Groups memories by project, session, or topic.

**Fields:**
- `name: String` - Context identifier (e.g., "helix-memory-project", "session-2024-11-17")
- `description: String` - What this context represents
- `type: String` - Type: "project", "session", "topic", "user"
- `timestamp: Date` - When created, set to NOW automatically

**Example:**
```hx
N::Context {
    name: "wordpress-plugin-dev",
    description: "WordPress plugin development context",
    type: "project",
    timestamp: NOW
}
```

**Usage Notes:**
- Create project contexts for long-term work
- Create session contexts for daily work
- Use type for filtering and organization
- Link memories to contexts for easy retrieval

## Edge Types

### E::HasEmbedding
Connects Memory to its vector embedding.

**Structure:**
```hx
E::HasEmbedding {
    From: Memory,
    To: MemoryEmbedding,
    Properties: {}
}
```

**Usage:**
Always create after storing both Memory and MemoryEmbedding.

**Query Pattern:**
```hx
memory <- N<Memory>(memory_id)
embedding <- AddV<MemoryEmbedding>(vector, {content: content})
AddE<HasEmbedding>::From(memory)::To(embedding)
```

### E::BelongsTo
Connects Memory to Context for grouping.

**Structure:**
```hx
E::BelongsTo {
    From: Memory,
    To: Context,
    Properties: {
        relevance: U32  // 1-10 score
    }
}
```

**Properties:**
- `relevance: U32` - How relevant is this memory to this context (1-10)

**Usage:**
Link memories to projects, sessions, or topics.

**Query Pattern:**
```hx
memory <- N<Memory>(memory_id)
context <- N<Context>(context_id)
AddE<BelongsTo>::From(memory)::To(context)
```

### E::RelatesTo
Connects related memories for graph traversal.

**Structure:**
```hx
E::RelatesTo {
    From: Memory,
    To: Memory,
    Properties: {
        relationship: String,  // Type of relationship
        strength: U32          // 1-10 score
    }
}
```

**Properties:**
- `relationship: String` - Type of edge (see table below)
- `strength: U32` - Relationship strength (1-10)

**Relationship Types:**

| Type | Direction | Use Case |
|------|-----------|----------|
| `related` | A ↔ B | Generic relationship (default) |
| `solves` | solution → problem | Link fix to bug |
| `solved_by` | problem → solution | Link bug to fix |
| `supersedes` | new → old | New replaces old |
| `implies` | A → B | Logical implication |
| `contradicts` | A ↔ B | Conflicting info |
| `leads_to` | cause → effect | Causation |
| `supports` | evidence → claim | Evidence |

**Usage:**
Create graph of related information for rich context retrieval.

**Query Pattern:**
```hx
from_memory <- N<Memory>(from_id)
to_memory <- N<Memory>(to_id)
AddE<RelatesTo>::From(from_memory)::To(to_memory)
```

### E::Solves
Connects solutions to problems they solve (causal fix relationship).

**Structure:**
```hx
E::Solves {
    From: Memory,  // solution
    To: Memory,    // problem
    Properties: {
        strength: U32,      // 1-10 how directly it solves
        verified: Boolean   // has fix been verified
    }
}
```

**Usage:**
Link solution memories to problem memories.

**CLI:**
```bash
memory link <solution_id> <problem_id> --type solves
memory store "Fix: use pooling" -t solution --solves <problem_id>
```

**Display:**
`memory show <problem_id>` displays `--SOLVED BY--` section.
`memory show <solution_id>` displays `--SOLVES--` section.

## Type System

### Scalar Types
- `String` - Text data
- `U32` - Unsigned 32-bit integer (0 to 4,294,967,295)
- `I64` - Signed 64-bit integer
- `Date` - Timestamp, use NOW for current time
- `Boolean` - true/false
- `[F64]` - Array of 64-bit floats (for vectors)

### Special Values
- `NOW` - Current timestamp for Date fields

## Graph Structure

```
Memory (content, category, importance, tags)
  |
  ├─[HasEmbedding]──> MemoryEmbedding (vector)
  |
  ├─[BelongsTo]────> Context (project/session)
  |
  ├─[RelatesTo]────> Memory (related info)
  |
  └─[Solves]───────> Memory (problem)  // solution → problem
```

## Schema Evolution

To modify schema:
1. Edit `db/schema.hx`
2. Update queries in `db/queries.hx` if needed
3. Rebuild: `helix build dev`
4. Redeploy: `helix push dev`

**Warning:** Schema changes may require data migration.

## Best Practices

### Field Naming
- Use lowercase with underscores for multi-word fields
- Be consistent across schema
- Use descriptive names

### Node Design
- Keep nodes focused (single responsibility)
- Store related data together
- Use edges for relationships, not nested data

### Edge Design
- Use meaningful relationship names
- Add properties for relationship metadata
- Keep edge properties minimal

### Type Selection
- Use U32 for scores/ratings (0-10)
- Use String for text, IDs
- Use Date for timestamps
- Use [F64] for vector embeddings

## Common Patterns

### Memory with Context
```hx
1. Create Memory
2. Create MemoryEmbedding
3. Link Memory -> MemoryEmbedding (HasEmbedding)
4. Get or Create Context
5. Link Memory -> Context (BelongsTo)
```

### Related Memories
```hx
1. Create Memory A
2. Create Memory B
3. Link A -> B (RelatesTo)
4. Set relationship type and strength
```

### Contextual Search
```hx
1. Search by vector similarity
2. Filter by Context
3. Follow RelatesTo edges
4. Rank by importance
```
