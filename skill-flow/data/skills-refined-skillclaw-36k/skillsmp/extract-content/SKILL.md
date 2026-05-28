---
name: extract-content
description: Extract entities and concepts from documents using HAIOS memory system.
  Use when ingesting new documents, analyzing content structure, or populating the
  knowledge base.
generated: '2026-01-07'
last_updated: '2026-01-07T20:49:16'
---

# Extract Content

Extract entities (people, systems, concepts) and concepts (decisions, directives, proposals) from documents using LLM-based extraction.

## Requirement Level

**MAY** use for document ingestion. For storing learnings, **SHOULD** use `ingester_ingest` directly instead (simpler path).

## When to Use

**MAY** use when:
- Ingesting new documents into HAIOS memory
- Analyzing document structure and key concepts
- Identifying entities mentioned in specifications
- Populating the knowledge graph

## Instructions

### Via MCP Tool (Recommended)

Use the `extract_content` MCP tool:

```
extract_content(
    file_path="path/to/document.md",
    content="<content of the file>",
    extraction_mode="full"  # or "entities_only", "concepts_only"
)
```

### Via Python (Direct)

**Note:** `haios_etl` is deprecated. For most use cases, the MCP tool `extract_content` above is recommended.

## Extraction Types

### Entities
- **Agent**: AI agents, systems, tools
- **User**: Human actors, roles
- **ADR**: Architecture Decision Records
- **System**: Technical systems, services

### Concepts
- **Decision**: Architectural or design decisions
- **Directive**: Instructions, guidelines
- **Proposal**: Suggested approaches
- **Critique**: Objections, concerns

## Example Workflow

1. Read document content
2. Call `extract_content` with the content
3. Review extracted entities and concepts
4. Use `ingester_ingest` to persist relevant items

```
# Step 1: Extract
result = extract_content(file_path="docs/ADR/ADR-001.md", content=doc_content)

# Step 2: Store important concepts
ingester_ingest(
    content="Use SQLite for the memory database",
    source_path="docs/ADR/ADR-001.md",
    content_type_hint="techne"
)
```

## Related Tools

- `ingester_ingest`: **PRIMARY** - Store extracted content with auto-classification
- `memory_search_with_experience`: Search stored memories
- `marketplace_list_agents`: Find agents that can help with extraction
- `memory_store`: **MUST NOT** use - deprecated, use `ingester_ingest`
