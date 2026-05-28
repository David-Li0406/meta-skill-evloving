---
name: dataflow-nexus-integration
description: "Integrate DataFlow with Nexus for multi-channel APIs. Use when DataFlow Nexus, Nexus blocking, Nexus integration, enable_model_persistence auto_discovery, or prevent blocking startup."
---

# DataFlow + Nexus Integration

Critical configuration patterns to prevent startup blocking when integrating DataFlow with Nexus for multi-channel APIs.

> **Skill Metadata**
> Category: `dataflow`
> Priority: `CRITICAL`
> Related Skills: [`nexus-quickstart`](#), [`dataflow-models`](#), [`dataflow-existing-database`](#)
> Related Subagents: `dataflow-specialist`, `nexus-specialist`

## Quick Reference

- **CRITICAL**: Use `enable_model_persistence=False` + `auto_discovery=False` to prevent blocking
- **Cause**: DataFlow table creation blocks Nexus startup
- **Fix**: Defer schema operations, disable auto-discovery
- **Pattern**: Initialize DataFlow before Nexus with proper config

## Core Pattern

```python
from dataflow import DataFlow
from nexus import Nexus

# CRITICAL CONFIGURATION to prevent blocking
db = DataFlow(
    database_url="postgresql://user:pass@localhost/db",
    auto_migrate=False,              # Don't create tables during init (prevents 5-10s startup delay)
    enable_model_persistence=False,  # Skip model registry for fast startup
    existing_schema_mode=True        # Work with existing schema only
)

# CRITICAL: auto_migrate=False is REQUIRED for Docker/FastAPI deployments.
# Despite async_safe_run() improvements, auto_migrate=True still fails due to
# event loop boundary issues (connections created in wrong loop).

# Define models AFTER init
@db.model
class Product:
    name: str
    price: float
    active: bool = True

# Create Nexus with DataFlow integration
nexus = Nexus(
    title="E-commerce API",
    enable_api=True,
    enable_cli=True,
    enable_mcp=True,

    # DataFlow configuration
    dataflow_config={
        "integration": db,
        "auto_discovery": False,              # CRITICAL: Prevent auto-model-discovery
        "auto_generate_endpoints": True,      # Generate API endpoints
        "auto_generate_cli_commands": True,   # Generate CLI commands
        "auto_generate_mcp_tools": True,      # Generate MCP tools
        "expose_bulk_operations": True        # Include bulk operation endpoints
    }
)

# All 9 DataFlow nodes now available through:
# - REST API: POST /api/workflows/ProductCreateNode/execute
# - CLI: nexus execute ProductCreateNode --name "Test" --price 100
# - MCP: Available to AI agents for data operations
```

## Common Use Cases

- **Multi-Channel Database APIs**: Expose DataFlow operations via API/CLI/MCP
- **AI Agent Integration**: Enable AI agents to query/modify database
- **Enterprise Platforms**: Unified database access across channels
- **Rapid API Development**: Auto-generated CRUD endpoints
- **Microservices**: Database-first service architecture

## Critical Configuration Parameters

### DataFlow Initialization

```python
db = DataFlow(
    database_url="postgresql://...",

    # CRITICAL: auto_migrate=False is REQUIRED for Docker/FastAPI deployments
    auto_migrate=False,              # Prevents event loop conflicts (connections bound to wrong loop)
    enable_model_persistence=False,  # Skip model registry for fast startup
    existing_schema_mode=True,       # Maximum safety

    # Note: Despite async_safe_run() improvements in v0.10.7+, auto_migrate=True
    # STILL FAILS in Docker/FastAPI due to asyncio event loop boundary issues.

    # Performance
    pool_size=20,
    pool_max_overflow=30,

    # Monitoring
    monitoring=True,
    slow_query_threshold=100
)
```

### Nexus DataFlow Config

```python
nexus = Nexus(
    title="API Platform",

    dataflow_config={
        "integration": db,

        # CRITICAL: Control auto-generation
        "auto_discovery": False,              # Prevent blocking
        "auto_generate_endpoints": True,      # API endpoints
        "auto_generate_cli_commands": True,   # CLI commands
        "auto_generate_mcp_tools": True,      # MCP tools

        # Features
        "expose_bulk_operations": True,       # Bulk endpoints
        "expose_analytics": True,             # Analytics endpoints
        "enable_caching": True,               # Response caching
        "cache_ttl": 300,                     # 5 minutes

        # Security
        "authentication_required": True,      # Require auth
        "rate_limiting": True,                # Rate limits
        "rbac_enabled": True                  # Role-based access
    },

    # Authentication
    auth_config={
        "providers": ["oauth2", "apikey"],
        "rbac_enabled": True
    }
)
```

## Common Mistakes

### Mistake 1: Default DataFlow + Nexus (BLOCKS!)

```python
# WRONG - Will block Nexus startup for minutes
db = DataFlow()  # Default settings cause blocking
nexus = Nexus(dataflow_config={"integration": db})
# Nexus hangs during startup!
```

**Fix: Use Critical Configuration**

```python
# CORRECT - Non-blocking startup
db = DataFlow(
    auto_migrate=False,
    enable_model_persistence=False,
    existing_schema_mode=True
)

@db.model
class Product:
    name: str

nexus = Nexus(
    dataflow_config={
        "integration": db,
        "auto_discovery": False  # CRITICAL
    }
)
```

### Mistake 2: Auto-Discovery Enabled

```python
# WRONG - auto_discovery causes blocking
nexus = Nexus(
    dataflow_config={
        "integration": db,
        "auto_discovery": True  # BLOCKS!
    }
)
```

**Fix: Disable Auto-Discovery**

```python
# CORRECT
nexus = Nexus(
    dataflow_config={
        "integration": db,
        "auto_discovery": False  # Prevents blocking
    }
)
```

### Mistake 3: Schema Operations During Init

```python
# WRONG - Table creation blocks startup
db = DataFlow(auto_migrate=True)  # Creates tables immediately

@db.model
class Product:
    name: str  # Table created here - blocks!

nexus = Nexus(dataflow_config={"integration": db})
```

**Fix: Defer Schema Operations**

```python
# CORRECT - Deferred schema operations
db = DataFlow(
    auto_migrate=False,           # Don't create tables
    existing_schema_mode=True     # Assume schema exists
)

@db.model
class Product:
    name: str  # Model registered, no table created

nexus = Nexus(dataflow_config={"integration": db})
# Fast startup, schema operations happen during first request
```

## Related Patterns

- **For Nexus basics**: See [`nexus-quickstart`](#)
- **For DataFlow models**: See [`dataflow-models`](#)
- **For existing databases**: See [`dataflow-existing-database`](#)
- **For multi-instance**: See [`dataflow-multi-instance`](#)

## When to Escalate to Subagent

Use `dataflow-specialist` or `nexus-specialist` when:
- Nexus still blocking despite configuration
- Complex authentication/authorization setup
- Performance optimization needed
- Multi-database Nexus integration
- Custom endpoint generation logic
- WebSocket integration for real-time updates

## Documentation References

### Primary Sources
- **Nexus Integration Analysis**: [`sdk-users/apps/dataflow/docs/integration/nexus-blocking-issue-analysis.md`](../../../../sdk-users/apps/dataflow/docs/integration/nexus-blocking-issue-analysis.md)
- **Nexus Integration Guide**: [`sdk-users/apps/dataflow/docs/integration/nexus.md`](../../../../sdk-users/apps/dataflow/docs/integration/nexus.md)
- **Full Features Guide**: [`sdk-users/apps/dataflow/docs/integration/dataflow-nexus-full-features.md`](../../../../sdk-users/apps/dataflow/docs/integration/dataflow-nexus-full-features.md)

### Related Documentation
- **DataFlow CLAUDE**: [`sdk-users/apps/dataflow/CLAUDE.md`](../../../../sdk-users/apps/dataflow/CLAUDE.md#L583-L655)
- **Nexus README**: [`sdk-users/apps/nexus/README.md`](../../../../sdk-users/apps/nexus/README.md)

### Specialist References
- **DataFlow Specialist**: [`.claude/skills/dataflow-specialist.md`](../../dataflow-specialist.md#L13-L25)
- **Nexus Specialist**: [`.claude/skills/nexus-specialist.md`](../../nexus-specialist.md#L320-L386)

## Examples

### Example 1: Complete Non-Blocking Setup

```python
from dataflow import DataFlow
from nexus import Nexus
from kailash.workflow.builder import WorkflowBuilder

# Step 1: Initialize DataFlow with critical config
db = DataFlow(
    database_url="postgresql://user:pass@localhost/ecommerce",
    auto_migrate=False,
    enable_model_persistence=False,
    existing_schema_mode=True
)

# Step 2: Define models
@db.model
class Product:
    sku: str
    name: str
    price: float
    stock: int
    active: bool = True

@db.model
class Order:
    customer_id: int
    total: float
    status: str = 'pending'

# Step 3: Create Nexus with proper config
nexus = Nexus(
    title="E-commerce Platform",
    version="1.0.0",
    enable_api=True,
    enable_cli=True,
    enable_mcp=True,

    dataflow_config={
        "integration": db,
        "auto_discovery": False,              # CRITICAL
        "auto_generate_endpoints": True,
        "auto_generate_cli_commands": True,
        "auto_generate_mcp_tools": True,
        "expose_bulk_operations": True
    }
)

# Step 4: Start Nexus (non-blocking!)
nexus.run(port=8000)
```

### Example 2: Multi-Channel DataFlow Access

```python
# After setup from Example 1, all channels work:

# 1. REST API
# POST http://localhost:8000/api/workflows/ProductCreateNode/execute
# Body: {"name": "Laptop", "sku": "LAP-001", "price": 1299.99, "stock": 50}

# 2. CLI
# $ nexus execute ProductListNode --filter '{"active": true}' --limit 10

# 3. MCP (AI agents)
# Agent can call: create_product, list_products, update_product, etc.

# 4. Python workflows (still work as before)
workflow = WorkflowBuilder()
workflow.add_node("ProductCreateNode", "create", {
    "sku": "PHONE-001",
    "name": "Smartphone",
    "price": 799.99,
    "stock": 100
})
```

### Example 3: Existing Database + Nexus

```python
# Connect to existing production database
db = DataFlow(
    database_url="postgresql://readonly:pass@prod-db:5432/commerce",
    auto_migrate=False,              # Never modify production
    enable_model_persistence=False,  # Skip model registry for fast startup
    existing_schema_mode=True        # Maximum safety
)

# Discover existing schema
schema = db.discover_schema(use_real_inspection=True)
result = db.register_schema_as_models(
    tables=['products', 'orders', 'customers']
)

# Create read-only API
nexus = Nexus(
    title="Commerce Read API",
    dataflow_config={
        "integration": db,
        "auto_discovery": False,
        "auto_generate_endpoints": True,
        "read_only": True,             # Only expose List and Read nodes
        "expose_bulk_operations": False
    },
    auth_config={
        "authentication_required": True,
        "providers": ["apikey"]
    }
)

nexus.run(port=8000)
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Nexus hangs on startup | enable_model_persistence=True or auto_discovery=True | Set enable_model_persistence=False and auto_discovery=False |
| "Table not found" error | existing_schema_mode without actual tables | Either create schema or set existing_schema_mode=False |
| Endpoints not generated | auto_generate_endpoints=False | Set to True |
| Permission denied | RBAC enabled without roles | Configure auth_config properly |
| Slow API responses | No caching | Enable caching in dataflow_config |

## Quick Tips

- ALWAYS use `enable_model_persistence=False` + `auto_discovery=False`
- Define models AFTER DataFlow init, BEFORE Nexus init
- Use `existing_schema_mode=True` for production databases
- Enable caching for read-heavy workloads
- Test startup time - should be <2 seconds
- Monitor slow query threshold
- Use read-only mode for analytics APIs

## Keywords for Auto-Trigger

<!-- Trigger Keywords: DataFlow Nexus, Nexus blocking, Nexus integration, enable_model_persistence, auto_discovery, prevent blocking, Nexus startup, DataFlow API, multi-channel, Nexus configuration, blocking startup, slow startup -->
