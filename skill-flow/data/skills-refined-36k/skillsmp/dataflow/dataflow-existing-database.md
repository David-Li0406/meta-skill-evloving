---
name: dataflow-existing-database
description: "Connect DataFlow to existing databases safely. Use when existing database, discover schema, legacy database, register_schema_as_models, existing_schema_mode, or connect to production database."
---

# DataFlow Existing Database Integration

Connect DataFlow to existing databases without @db.model decorators using dynamic schema discovery.

> **Skill Metadata**
> Category: `dataflow`
> Priority: `HIGH`
> Related Skills: [`dataflow-models`](#), [`dataflow-connection-config`](#), [`dataflow-nexus-integration`](#)
> Related Subagents: `dataflow-specialist` (complex schemas, migration planning)

## Quick Reference

- **Safe Mode**: `existing_schema_mode=True` prevents ALL schema changes
- **Discover**: `db.discover_schema(use_real_inspection=True)`
- **Register**: `db.register_schema_as_models(tables=['users', 'orders'])`
- **Perfect For**: Legacy databases, production readonly, LLM agents

## Core Pattern

```python
from dataflow import DataFlow

# Connect safely to existing database
db = DataFlow(
    database_url="postgresql://user:pass@localhost/existing_db",
    auto_migrate=False,           # Don't modify schema
    existing_schema_mode=True     # Maximum safety - prevents ALL changes
)

# Discover existing tables
schema = db.discover_schema(use_real_inspection=True)
print(f"Found tables: {list(schema.keys())}")

# Register tables as DataFlow models
result = db.register_schema_as_models(tables=['users', 'orders', 'products'])

# Now use generated nodes immediately
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

workflow = WorkflowBuilder()
user_nodes = result['generated_nodes']['users']

workflow.add_node(user_nodes['list'], "get_users", {
    "filter": {"active": True},
    "limit": 10
})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

## Common Use Cases

- **Legacy Integration**: Connect to existing applications
- **Production Readonly**: Safe read access to production
- **LLM Agents**: Dynamic database exploration
- **Cross-Session**: Models shared between users
- **Migration Planning**: Analyze before migrating

## Key Methods

### discover_schema()

```python
schema = db.discover_schema(
    use_real_inspection=True  # Use actual database inspection
)

# Returns: Dict[table_name, table_structure]
# {
#   'users': {
#     'columns': [
#       {'name': 'id', 'type': 'INTEGER', 'nullable': False},
#       {'name': 'email', 'type': 'VARCHAR(255)', 'nullable': False}
#     ],
#     'primary_key': ['id'],
#     'foreign_keys': [...],
#     'indexes': [...]
#   }
# }
```

### register_schema_as_models()

```python
result = db.register_schema_as_models(
    tables=['users', 'orders', 'products']
)

# Returns:
# {
#   'registered_models': ['User', 'Order', 'Product'],
#   'generated_nodes': {
#     'User': {
#       'create': 'UserCreateNode',
#       'read': 'UserReadNode',
#       'update': 'UserUpdateNode',
#       'delete': 'UserDeleteNode',
#       'list': 'UserListNode',
#       # + 4 bulk operation nodes
#     }
#   },
#   'success_count': 3,
#   'error_count': 0
# }
```

### reconstruct_models_from_registry()

```python
# In different session/process
db2 = DataFlow(
    database_url="postgresql://...",
    existing_schema_mode=True
)

# Reconstruct models registered by others
models = db2.reconstruct_models_from_registry()
print(f"Available models: {models['reconstructed_models']}")
```

## Common Mistakes

### Mistake 1: Modifying Production Schema

```python
# DANGER - Will modify production!
db = DataFlow(
    database_url="postgresql://prod-db/database",
    auto_migrate=True  # BAD - could alter schema!
)
```

**Fix: Use Safe Mode**

```python
# Safe - readonly access
db = DataFlow(
    database_url="postgresql://prod-db/database",
    auto_migrate=False,
    existing_schema_mode=True
)
```

### Mistake 2: Assuming Tables Exist

```python
# Wrong - assumes tables exist
db = DataFlow(existing_schema_mode=True)

@db.model
class NewModel:
    name: str
# Model registered but NO table created!
```

**Fix: Check Schema First**

```python
db = DataFlow(existing_schema_mode=True)
schema = db.discover_schema(use_real_inspection=True)

if 'new_models' not in schema:
    print("Table doesn't exist - schema changes blocked")
```

## Related Patterns

- **For model definition**: See [`dataflow-models`](#)
- **For connection config**: See [`dataflow-connection-config`](#)
- **For Nexus integration**: See [`dataflow-nexus-integration`](#)

## When to Escalate to Subagent

Use `dataflow-specialist` when:
- Complex legacy schema analysis
- Migration planning from existing database
- Multi-database integration
- Custom schema mapping
- Performance optimization for large schemas

## Documentation References

### Primary Sources
- **README Dynamic Models**: [`sdk-users/apps/dataflow/README.md`](../../../../sdk-users/apps/dataflow/README.md#L249-L536)
- **DataFlow CLAUDE**: [`sdk-users/apps/dataflow/CLAUDE.md`](../../../../sdk-users/apps/dataflow/CLAUDE.md#L182-L196)

### Related Documentation
- **Multi-Database**: [`sdk-users/apps/dataflow/docs/features/multi-database.md`](../../../../sdk-users/apps/dataflow/docs/features/multi-database.md)
- **Schema Management**: [`sdk-users/apps/dataflow/docs/workflows/schema-management.md`](../../../../sdk-users/apps/dataflow/docs/workflows/schema-management.md)

## Examples

### Example 1: Production Readonly Access

```python
# Safe readonly access to production
db_prod = DataFlow(
    database_url="postgresql://readonly:pass@prod-db:5432/ecommerce",
    auto_migrate=False,
    existing_schema_mode=True
)

# Discover production schema
schema = db_prod.discover_schema(use_real_inspection=True)
print(f"Production has {len(schema)} tables")

# Register only needed tables
result = db_prod.register_schema_as_models(
    tables=['products', 'orders', 'customers']
)

# Safe read operations
workflow = WorkflowBuilder()
product_nodes = result['generated_nodes']['products']

workflow.add_node(product_nodes['list'], "active_products", {
    "filter": {"active": True},
    "limit": 100
})
```

### Example 2: LLM Agent Database Exploration

```python
# LLM agent explores unknown database
db_agent = DataFlow(
    database_url="postgresql://...",
    existing_schema_mode=True
)

# Agent discovers structure
schema = db_agent.discover_schema(use_real_inspection=True)
interesting_tables = [
    t for t in schema.keys()
    if not t.startswith('dataflow_')  # Skip system tables
]

# Agent registers tables
result = db_agent.register_schema_as_models(
    tables=interesting_tables[:5]  # First 5 tables
)

# Agent builds exploration workflow
workflow = WorkflowBuilder()
for model_name in result['registered_models']:
    nodes = result['generated_nodes'][model_name]
    workflow.add_node(nodes['list'], f"sample_{model_name}", {
        "limit": 3
    })

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())

# Agent analyzes sample data
for node_id, result_data in results.items():
    print(f"Sampled {node_id}: {len(result_data.get('result', []))} records")
```

### Example 3: Cross-Session Model Sharing

```python
# SESSION 1: Data engineer discovers and registers
db_engineer = DataFlow(
    database_url="postgresql://...",
    existing_schema_mode=True
)

schema = db_engineer.discover_schema(use_real_inspection=True)
result = db_engineer.register_schema_as_models(
    tables=['users', 'products', 'orders']
)
print(f"Registered for team: {result['registered_models']}")

# SESSION 2: Developer uses registered models
db_developer = DataFlow(
    database_url="postgresql://...",
    existing_schema_mode=True
)

# Reconstruct from registry
models = db_developer.reconstruct_models_from_registry()
print(f"Available: {models['reconstructed_models']}")

# Build workflow immediately
workflow = WorkflowBuilder()
user_nodes = models['generated_nodes']['users']
workflow.add_node(user_nodes['list'], "users", {"limit": 20})
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| "Table not found" | existing_schema_mode without tables | Verify tables exist with discover_schema() |
| "Permission denied" | Readonly user trying to modify | Correct - existing_schema_mode working |
| Models not available | Not registered yet | Call register_schema_as_models() |
| Schema discovery empty | Wrong database or no tables | Check database_url |

## Quick Tips

- ALWAYS use existing_schema_mode=True for production
- discover_schema() before register_schema_as_models()
- Skip system tables (dataflow_*) when exploring
- Models persist across sessions via registry
- Perfect for legacy database integration
- No @db.model needed - fully dynamic

## Keywords for Auto-Trigger

<!-- Trigger Keywords: existing database, discover schema, legacy database, register_schema_as_models, existing_schema_mode, production database, readonly database, dynamic models, schema discovery, connect existing -->
