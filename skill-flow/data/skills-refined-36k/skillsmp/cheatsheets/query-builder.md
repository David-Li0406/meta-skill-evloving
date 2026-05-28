---
name: query-builder
description: "Query builder patterns for dynamic SQL. Use when asking 'query builder', 'build queries', 'dynamic SQL', 'SQL construction', or 'query patterns'."
---

# Query Builder

Query Builder for database operations and query management.

> **Skill Metadata**
> Category: `database`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Query Builder
- **Category**: database
- **Priority**: HIGH
- **Trigger Keywords**: query builder, build queries, dynamic SQL, SQL construction

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Query Builder implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/query-builder.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Query-Builder Operations**: Execute, optimize, and manage database queries with advanced patterns
- **Performance Optimization**: Query routing, caching, connection pooling for high-performance database access
- **Transaction Management**: Coordinate database operations with ACID guarantees, savepoints, distributed transactions
- **Error Handling**: Retry logic, circuit breakers, fallback strategies for database connectivity issues
- **Monitoring**: Track query performance, slow query detection, connection pool health, execution metrics

## Related Patterns

- **For fundamentals**: See [`workflow-quickstart`](#)
- **For patterns**: See [`workflow-patterns-library`](#)
- **For parameters**: See [`param-passing-quick`](#)

## When to Escalate to Subagent

Use specialized subagents when:
- **pattern-expert**: Complex patterns, multi-node workflows
- **sdk-navigator**: Error resolution, parameter issues
- **testing-specialist**: Comprehensive testing strategies

## Documentation References

### Primary Sources
- [`sdk-users/2-core-concepts/cheatsheet/`](../../../sdk-users/2-core-concepts/cheatsheet/)

## Quick Tips

- 💡 **Tip 1**: Follow best practices from documentation
- 💡 **Tip 2**: Test patterns incrementally
- 💡 **Tip 3**: Reference examples for complex cases

## Keywords for Auto-Trigger

<!-- Trigger Keywords: query builder, build queries, dynamic SQL, SQL construction -->
