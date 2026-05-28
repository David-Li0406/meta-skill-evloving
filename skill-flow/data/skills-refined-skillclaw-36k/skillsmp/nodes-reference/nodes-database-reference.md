---
name: nodes-database-reference
description: "Database nodes reference (AsyncSQL, MySQL, PostgreSQL, Connection Pool). Use when asking 'database node', 'SQL node', 'AsyncSQL', 'connection pool', or 'query routing'."
---

# Database Nodes Reference

Complete reference for database operations and connection management.

> **Skill Metadata**
> Category: `nodes`
> Priority: `HIGH`
> SDK Version: `0.9.25+`
> Related Skills: [`nodes-data-reference`](nodes-data-reference.md), [`nodes-quick-index`](nodes-quick-index.md)
> Related Subagents: `pattern-expert` (database workflows)

## Quick Reference

```python
from kailash.nodes.data import (
    AsyncSQLDatabaseNode,  # ⭐⭐⭐ Production recommended
    WorkflowConnectionPool,  # ⭐⭐ Connection pooling
    QueryRouterNode,  # ⭐⭐⭐ Intelligent routing
    SQLDatabaseNode,  # Simple queries
    OptimisticLockingNode  # ⭐⭐ Concurrency control
)
```

## Production Database Node

### AsyncSQLDatabaseNode ⭐ (Recommended)
```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

# Production-grade async SQL with transactions
workflow.add_node("AsyncSQLDatabaseNode", "db", {
    "database_type": "postgresql",
    "host": "localhost",
    "database": "myapp",
    "user": "dbuser",
    "password": "dbpass",
    "transaction_mode": "auto"  # auto, manual, or none
})

# Execute query
workflow.add_node("AsyncSQLDatabaseNode", "query", {
    "query": "SELECT * FROM users WHERE active = :active",
    "params": {"active": True},
    "fetch_mode": "all"
})
```

## Connection Pooling

### WorkflowConnectionPool ⭐
```python
from kailash.nodes.data import WorkflowConnectionPool

# Create connection pool
pool = WorkflowConnectionPool(
    name="main_pool",
    database_type="postgresql",
    host="localhost",
    database="myapp",
    min_connections=5,
    max_connections=20,
    adaptive_sizing=True,
    enable_query_routing=True
)

# Initialize pool
workflow.add_node("WorkflowConnectionPool", "pool_init", {
    "operation": "initialize"
})
```

## Query Routing

### QueryRouterNode ⭐
```python
from kailash.nodes.data import QueryRouterNode

# Intelligent query routing with caching
workflow.add_node("QueryRouterNode", "router", {
    "name": "query_router",
    "connection_pool": "smart_pool",
    "enable_read_write_split": True,
    "cache_size": 2000,
    "pattern_learning": True
})
```

## Simple SQL Node

### SQLDatabaseNode
```python
workflow.add_node("SQLDatabaseNode", "simple_query", {
    "connection_string": "postgresql://user:pass@localhost/db",
    "query": "SELECT * FROM users WHERE id = :user_id",
    "parameters": {"user_id": 123},
    "operation": "fetch_one"
})
```

## Concurrency Control

### OptimisticLockingNode ⭐
```python
from kailash.nodes.data import OptimisticLockingNode

# Version-based concurrency control
lock_manager = OptimisticLockingNode(
    version_field="version",
    max_retries=3,
    default_conflict_resolution="retry"
)

workflow.add_node("OptimisticLockingNode", "lock", {
    "action": "update_with_version",
    "table_name": "users",
    "record_id": 123,
    "update_data": {"name": "John Updated"},
    "expected_version": 5
})
```

## Related Skills

- **Data Nodes**: [`nodes-data-reference`](nodes-data-reference.md)
- **Node Index**: [`nodes-quick-index`](nodes-quick-index.md)

## Documentation

- **Data Nodes**: [`sdk-users/2-core-concepts/nodes/03-data-nodes.md`](../../../../sdk-users/2-core-concepts/nodes/03-data-nodes.md)

<!-- Trigger Keywords: database node, SQL node, AsyncSQL, connection pool, query routing, AsyncSQLDatabaseNode, WorkflowConnectionPool, QueryRouterNode -->
