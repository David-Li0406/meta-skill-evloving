---
name: decide-database-postgresql-sqlite
description: "Choose between PostgreSQL and SQLite for DataFlow applications based on requirements. Use when asking 'PostgreSQL vs SQLite', 'database choice', 'which database', 'database selection', or 'DB comparison'."
---

# Decision: Database Selection

Decision: Database Selection guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `cross-cutting`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Decision: Database Selection
- **Category**: cross-cutting
- **Priority**: MEDIUM
- **Trigger Keywords**: PostgreSQL vs SQLite, database choice, which database, database selection

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Decide Database Postgresql Sqlite implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/decide-database-postgresql-sqlite.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Decide-Database-Postgresql-Sqlite Processing**: Extract, transform, load data from various sources with validation
- **Format Conversion**: CSV, JSON, XML, Parquet conversions with schema validation and type handling
- **API Integration**: REST, GraphQL, WebSocket integrations with authentication and error handling
- **Batch Processing**: High-volume data processing with streaming, pagination, and memory optimization
- **Data Quality**: Validation, deduplication, enrichment, normalization for clean data pipelines

## Related Patterns

- **For fundamentals**: See [`workflow-quickstart`](#)
- **For connections**: See [`connection-patterns`](#)
- **For parameters**: See [`param-passing-quick`](#)

## When to Escalate to Subagent

Use specialized subagents when:
- Complex implementation needed
- Production deployment required
- Deep analysis necessary
- Enterprise patterns needed

## Documentation References

### Primary Sources
- [`sdk-users/apps/dataflow/docs/reference/dialects.md`](../../../sdk-users/apps/dataflow/docs/reference/dialects.md)

## Quick Tips

- 💡 **Tip 1**: Always follow Decision: Database Selection best practices
- 💡 **Tip 2**: Test patterns incrementally
- 💡 **Tip 3**: Reference documentation for details

## Keywords for Auto-Trigger

<!-- Trigger Keywords: PostgreSQL vs SQLite, database choice, which database, database selection -->
