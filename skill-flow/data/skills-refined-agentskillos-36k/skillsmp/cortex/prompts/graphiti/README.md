# Graphiti-Inspired Prompts

These prompts are adapted from [Graphiti](https://github.com/getzep/graphiti), Zep's open-source temporal knowledge graph framework.

## Pipeline Overview

The extraction pipeline uses **split prompts** (Graphiti-style) for better accuracy:

```
1. EXTRACT ENTITIES (extract-entities.prompt.md)
   └─ Graph-independent: extract entities from episode content
   └─ Output: [{name, entity_type_id}, ...]
   
2. RESOLVE ENTITIES (code + optional LLM)
   └─ Match extracted entities to existing nodes (deduplication)
   └─ Uses graph context for disambiguation
   └─ Output: uuid_map{} mapping temp IDs to resolved UUIDs
   
3. EXTRACT RELATIONSHIPS (extract-relationships.prompt.md)
   └─ Graph-independent: extract relationships using resolved entity UUIDs
   └─ Identity/temporal relationships use target_literal
   └─ Output: relationships with temporal bounds
   
4. RESOLVE EDGES (resolve-edges.prompt.md)
   └─ Match extracted edges to existing edges (deduplication)
   
5. IDENTITY PROMOTION (code, not prompt)
   └─ HAS_EMAIL, HAS_PHONE, HAS_HANDLE → entity_aliases table
   └─ Provenance stored in episode_relationship_mentions.target_literal
   
6. DETECT CONTRADICTIONS (detect-contradictions.prompt.md)
   └─ Find existing facts that new facts contradict
   └─ Set invalid_at on old edges

7. SUMMARIZE ENTITY (summarize-entity.prompt.md) [deferred]
   └─ Update entity summaries with new information
```

## Key Concepts

### Graph-Independent Extraction

Extraction prompts don't query the existing graph. This keeps extraction:
- Parallelizable (process multiple episodes concurrently)
- Reproducible (same input → same output)
- Clean (bad graph data doesn't corrupt extraction)

Resolution uses the graph to disambiguate extracted entities.

### Entity Types (8 total)

Entities are things you want to traverse to/from:

```json
{
  "entity_types": [
    {"id": 0, "name": "Entity", "description": "Default/unknown type"},
    {"id": 1, "name": "Person", "description": "A human being"},
    {"id": 2, "name": "Company", "description": "Business or organization"},
    {"id": 3, "name": "Project", "description": "A project, product, or codebase"},
    {"id": 4, "name": "Location", "description": "A place (city, address, venue)"},
    {"id": 5, "name": "Event", "description": "A meeting or occurrence"},
    {"id": 6, "name": "Document", "description": "A file or written work"},
    {"id": 7, "name": "Pet", "description": "An animal companion"}
  ]
}
```

**NOT entities:**
- Dates — stored as `target_literal` (ISO 8601)
- AI agents — no durable identity
- Concepts, activities, professions — searchable via episode embeddings

### target_literal vs target_entity_id

Relationships point to either an entity or a literal value:

| Target Type | Relationship Types | Format | Promoted to Alias? |
|-------------|-------------------|--------|-------------------|
| **Literal → Alias** | HAS_EMAIL, HAS_PHONE, HAS_HANDLE, HAS_USERNAME, ALSO_KNOWN_AS | Various | Yes |
| **Literal → Date** | BORN_ON, ANNIVERSARY_ON, OCCURRED_ON, SCHEDULED_FOR, STARTED_ON, ENDED_ON | ISO 8601 | No |
| **Entity** | Everything else | UUID | No |

### Entity-to-Entity Relationships

| Category | Relationships | Target Type |
|----------|---------------|-------------|
| Personal | BORN_IN, LIVES_IN | Location |
| Personal | HAS_PET | Pet |
| Professional | WORKS_AT, OWNS, FOUNDED | Company |
| Professional | ATTENDED | Company or Event |
| Social | KNOWS, FRIEND_OF, SPOUSE_OF, PARENT_OF, DATING | Person |
| Projects | CREATED, BUILDING, WORKING_ON | Project |
| Events | ATTENDED, HOSTED | Event |
| Content | AUTHORED, REFERENCES | Document |

### Bi-Temporal Model

Relationships track when facts are true in reality:
- `valid_at`: When the relationship became true
- `invalid_at`: When the relationship stopped being true

Plus system time:
- `created_at`: When we learned about it

### Date Format

All dates must be **ISO 8601**:
- Full date: `YYYY-MM-DD` (e.g., `1990-05-15`)
- Month precision: `YYYY-MM` (e.g., `2024-01`)
- Year precision: `YYYY` (e.g., `2020`)

## Custom Instructions

Each prompt accepts `{{custom_extraction_instructions}}` for domain-specific guidance:

```
Focus on extracting:
- Trading system components and their relationships
- Client names and project associations
- Technical decisions and their rationale
```

## References

- [Graphiti GitHub](https://github.com/getzep/graphiti)
- [Graphiti Docs](https://help.getzep.com/graphiti)
- [Zep Paper: Temporal Knowledge Graph Architecture](https://arxiv.org/abs/2501.13956)
- [MEMORY_SYSTEM_SPEC.md](../../docs/MEMORY_SYSTEM_SPEC.md) — Full specification
