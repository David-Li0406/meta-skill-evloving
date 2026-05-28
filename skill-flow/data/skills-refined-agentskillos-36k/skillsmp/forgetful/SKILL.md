---
name: forgetful
description: Forgetful MCP semantic memory system. Use when storing architectural decisions, querying patterns, managing projects, or creating memories, documents, code artifacts, and entities.
user-invocable: true
---

# Forgetful MCP Memory System

Forgetful is a semantic memory system for persistent knowledge across Claude sessions. Use it to store architectural decisions, patterns, lessons learned, and retrieve context.

## Core Concepts

| Type | Purpose | Size Limit |
|------|---------|------------|
| **Memory** | Atomic knowledge units (single concept) | <400 words, 2000 chars |
| **Document** | Long-form content (guides, analysis) | >300 words |
| **Code Artifact** | Reusable code snippets/patterns | Any size |
| **Entity** | Real-world things (people, orgs, devices) | N/A |
| **Project** | Organizes items by context | N/A |

## Invocation Pattern

All operations use `execute_forgetful_tool`:

```python
execute_forgetful_tool("tool_name", {"arg1": value1, "arg2": value2})
```

## Memory Operations

### Query (Semantic Search)

```python
# Basic search
execute_forgetful_tool("query_memory", {
    "query": "event sourcing patterns",
    "query_context": "Implementing new aggregate"
})

# With filters
execute_forgetful_tool("query_memory", {
    "query": "projection architecture",
    "query_context": "Adding CRM projections",
    "k": 5,                      # Number of results (default 3)
    "importance_threshold": 7,   # Min importance (1-10)
    "project_ids": [1],          # Filter to projects
    "include_links": true        # Include linked memories
})
```

### Create Memory

**Required fields:** title, content, context, keywords, tags, importance

```python
execute_forgetful_tool("create_memory", {
    "title": "Short descriptive title",
    "content": "The actual knowledge (single concept, <400 words)",
    "context": "WHY this matters, HOW it relates",
    "keywords": ["keyword1", "keyword2"],  # For search (max 10)
    "tags": ["architecture", "pattern"],    # For categorization (max 10)
    "importance": 8,  # 1-10 scale (see below)

    # Optional linking
    "project_ids": [1],
    "code_artifact_ids": [5],
    "document_ids": [2],

    # Optional provenance
    "source_repo": "oakesjoshuad/substruct",
    "source_files": ["src/file.rs"],
    "confidence": 0.95,
    "encoding_agent": "claude-opus-4-5"
})
```

### Importance Scale

| Score | Meaning | Examples |
|-------|---------|----------|
| 9-10 | Foundational/Personal | Core architecture decisions, user preferences |
| 8-9 | Critical solutions | Bug fixes, key patterns that solved problems |
| 7-8 | Useful patterns | Reusable approaches, implementation patterns |
| 6-7 | Milestones | Progress markers, completed features |
| 1-5 | Reference | Minor notes, temporary context |

### Other Memory Operations

```python
# Get by ID
execute_forgetful_tool("get_memory", {"memory_id": 42})

# Update (PATCH semantics - only specified fields change)
execute_forgetful_tool("update_memory", {
    "memory_id": 42,
    "importance": 9,
    "content": "Updated content"
})

# Link memories bidirectionally
execute_forgetful_tool("link_memories", {
    "memory_id": 42,
    "related_ids": [10, 15, 20]
})

# Unlink
execute_forgetful_tool("unlink_memories", {
    "source_id": 42,
    "target_id": 57
})

# Mark obsolete (soft delete with audit trail)
execute_forgetful_tool("mark_memory_obsolete", {
    "memory_id": 42,
    "reason": "Superseded by newer approach",
    "superseded_by": 100  # Optional replacement ID
})

# Recent memories
execute_forgetful_tool("get_recent_memories", {"limit": 10})
```

## Project Operations

Projects organize memories, documents, and artifacts by context.

```python
# List projects
execute_forgetful_tool("list_projects", {})
execute_forgetful_tool("list_projects", {"status": "active"})

# Create project
execute_forgetful_tool("create_project", {
    "name": "substruct",
    "description": "Rust business management system",
    "project_type": "development",  # See types below
    "repo_name": "oakesjoshuad/substruct",
    "status": "active"  # active, archived, completed
})

# Get/Update/Delete
execute_forgetful_tool("get_project", {"project_id": 1})
execute_forgetful_tool("update_project", {"project_id": 1, "status": "archived"})
execute_forgetful_tool("delete_project", {"project_id": 1})
```

**Project Types:** personal, work, learning, development, infrastructure, template, product, marketing, finance, documentation, development-environment, third-party-library, open-source

## Document Operations

For long-form content (>300 words): guides, analysis, specifications.

```python
# Create document
execute_forgetful_tool("create_document", {
    "title": "EventStore Implementation Guide",
    "description": "How to implement event stores in Substruct",
    "content": "# Full markdown content here...",
    "document_type": "markdown",  # text, markdown, code
    "tags": ["guide", "event-sourcing"],
    "project_id": 1
})

# List/Get/Update/Delete
execute_forgetful_tool("list_documents", {"project_id": 1})
execute_forgetful_tool("get_document", {"document_id": 5})
execute_forgetful_tool("update_document", {"document_id": 5, "content": "Updated..."})
execute_forgetful_tool("delete_document", {"document_id": 5})
```

## Code Artifact Operations

For reusable code snippets and patterns.

```python
# Create artifact
execute_forgetful_tool("create_code_artifact", {
    "title": "Aggregate Trait Implementation",
    "description": "Canonical pattern for implementing Aggregate trait",
    "code": "impl Aggregate for User { ... }",
    "language": "rust",
    "tags": ["pattern", "aggregate"],
    "project_id": 1
})

# List/Get/Update/Delete
execute_forgetful_tool("list_code_artifacts", {"language": "rust"})
execute_forgetful_tool("get_code_artifact", {"artifact_id": 3})
execute_forgetful_tool("update_code_artifact", {"artifact_id": 3, "code": "..."})
execute_forgetful_tool("delete_code_artifact", {"artifact_id": 3})
```

## Entity Operations

For real-world entities: people, organizations, teams, devices.

```python
# Create entity
execute_forgetful_tool("create_entity", {
    "name": "Joshua",
    "entity_type": "individual",  # organization, individual, team, device, other
    "notes": "Project owner",
    "aka": ["Josh", "J"],  # Searchable aliases
    "tags": ["developer"],
    "project_ids": [1]
})

# Search entities (searches name AND aka)
execute_forgetful_tool("search_entities", {"query": "Josh"})

# Link entity to memory
execute_forgetful_tool("link_entity_to_memory", {
    "entity_id": 1,
    "memory_id": 42
})

# Get memories linked to entity
execute_forgetful_tool("get_entity_memories", {"entity_id": 1})

# Entity relationships (knowledge graph)
execute_forgetful_tool("create_entity_relationship", {
    "source_entity_id": 1,
    "target_entity_id": 2,
    "relationship_type": "works_for",  # works_for, member_of, owns, reports_to, collaborates_with
    "strength": 0.9,
    "confidence": 0.95
})

execute_forgetful_tool("get_entity_relationships", {
    "entity_id": 1,
    "direction": "outgoing"  # outgoing, incoming, both
})
```

## Referencing Items

When referencing Forgetful items in Beads issues, documentation, or memories:

| Item Type | Reference Format | Example |
|-----------|------------------|---------|
| Memory | `Forgetful #ID (title)` | `Forgetful #42 (EventStore Design)` |
| Document | `Forgetful doc #ID` | `Forgetful doc #5` |
| Code Artifact | `Forgetful artifact #ID` | `Forgetful artifact #3` |
| Entity | `Forgetful entity #ID` | `Forgetful entity #1` |
| Project | `Forgetful project #ID` | `Forgetful project #1` |

## Linking Best Practices

**Always link related items for discoverability:**

```python
# When creating memory, link to related items
execute_forgetful_tool("create_memory", {
    # ... required fields ...
    "project_ids": [1],           # Link to project
    "document_ids": [5],          # Link to related docs
    "code_artifact_ids": [3]      # Link to code examples
})

# Link memories to each other
execute_forgetful_tool("link_memories", {
    "memory_id": 42,
    "related_ids": [10, 15]
})

# Link entities to memories they're mentioned in
execute_forgetful_tool("link_entity_to_memory", {
    "entity_id": 1,
    "memory_id": 42
})
```

## Substruct Project Context

**Project ID:** 1 (substruct)

**Common Tags:**
- `architecture` - Architectural decisions
- `pattern` - Implementation patterns
- `event-sourcing` - Event sourcing related
- `actor-model` - Actor system patterns
- `hexagonal` - Hexagonal architecture
- `testing` - Testing strategies
- `refactoring` - Refactoring notes
- `lesson-learned` - What worked/didn't

**When to Create Memories:**
- After making architectural decisions (with rationale)
- When discovering patterns that work well
- After debugging tricky issues (lessons learned)
- When evaluating trade-offs and choosing approaches
- To document "why" behind non-obvious code

**Provenance for Substruct:**
```python
{
    "source_repo": "oakesjoshuad/substruct",
    "source_files": ["path/to/relevant/file.rs"],
    "encoding_agent": "claude-opus-4-5",
    "confidence": 0.95  # Lower if uncertain
}
```

## Discovery Tools

```python
# See all available tools
execute_forgetful_tool("discover_forgetful_tools", {})

# Filter by category
execute_forgetful_tool("discover_forgetful_tools", {"category": "memory"})

# Get detailed docs for a tool
how_to_use_forgetful_tool("create_memory")
```

## Tips

- Query before creating to avoid duplicates
- Use `query_context` to improve search relevance
- Link memories bidirectionally for graph traversal
- Mark obsolete instead of deleting (preserves audit trail)
- Use importance 8+ for decisions, 7 for patterns, 6 for milestones
- Include provenance for traceability
