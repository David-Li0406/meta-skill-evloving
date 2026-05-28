---
name: schema-ref
description: Database schema reference for haios_memory.db. MUST be used before any SQL query to verify table and column names. Use when verifying schema, checking table structure, or before database operations.
---
# generated: 2025-12-09
# System Auto: last updated on: 2025-12-10 18:37:23
# Schema Reference

## Requirement Level

**MUST NOT** use this skill directly. Use via the **schema-verifier** subagent, which is **REQUIRED** for any SQL query (enforced by PreToolUse hook).

**UPDATED Session 53:** Use MCP tools instead of direct SQL commands.

## MCP Tools (Preferred)

Use these tools from the haios-memory MCP server:

```
mcp__haios-memory__schema_info()          # List all tables
mcp__haios-memory__schema_info("concepts") # Get columns for specific table
mcp__haios-memory__db_query("SELECT ...") # Run read-only queries
```

## Common Tables

| Table | Purpose |
|-------|---------|
| concepts | Extracted concepts with embeddings |
| entities | Named entities (people, files, etc.) |
| reasoning_traces | ReasoningBank query history |
| synthesis_clusters | Grouped similar concepts |
| synthesis_provenance | Bridge insight sources |
| artifacts | Processed file metadata |

## Full Schema Reference

For complete schema definition:
@docs/specs/memory_db_schema_v3.sql

## Output Format

Return ONLY:
1. Table name (verified exists)
2. Column names and types
3. Any relevant constraints

Do NOT return the full schema file content.
