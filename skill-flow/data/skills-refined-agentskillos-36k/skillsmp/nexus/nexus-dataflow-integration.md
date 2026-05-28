---
skill: nexus-dataflow-integration
description: CRITICAL DataFlow + Nexus integration patterns with blocking fix configuration (auto_discovery=False, enable_model_persistence=False)
priority: CRITICAL
tags: [nexus, dataflow, integration, blocking-fix, performance]
---

# Nexus DataFlow Integration

CRITICAL: Proper configuration to prevent blocking and slow startup.

## The Problem

Without proper configuration, Nexus + DataFlow causes:
1. **Infinite blocking** during initialization
2. **5-10 second delay** per DataFlow model

## The Solution

```python
from nexus import Nexus
from dataflow import DataFlow

# Step 1: Create Nexus with auto_discovery=False
app = Nexus(
    api_port=8000,
    mcp_port=3001,
    auto_discovery=False  # CRITICAL: Prevents blocking
)

# Step 2: Create DataFlow with optimized settings
db = DataFlow(
    database_url="postgresql://user:pass@host:port/db",
    enable_model_persistence=False,  # CRITICAL: Skip model registry for fast startup
    auto_migrate=False,
    skip_migration=True
)

# Step 3: Register models (now instant!)
@db.model
class User:
    id: str
    email: str
    name: str

# Step 4: Register workflows manually
workflow = WorkflowBuilder()
workflow.add_node("UserCreateNode", "create", {"email": "{{email}}"})
app.register("create_user", workflow.build())

# Step 5: Start (fast!)
app.start()
```

## Why This Configuration

### `auto_discovery=False` (Nexus)
- Prevents scanning filesystem for workflows
- Avoids re-importing Python modules
- Eliminates infinite blocking issue
- **When to use**: Always when integrating with DataFlow

### `enable_model_persistence=False` (DataFlow)
- Skips creating registry tables in database
- Avoids synchronous workflow execution during init
- Disables persisting model metadata to database
- Prevents workflow execution for each model registration
- Models stored in memory only, still work normally for CRUD operations
- **Impact**: <0.1s per model vs 5-10s with registry, instant model registration

## Performance Comparison

### With Default Settings
```
Nexus init: 1-2s
DataFlow init with enable_model_persistence=True: 5-10s per model
Total for 3 models: 15-30s
```

### With Optimized Settings (enable_model_persistence=False)
```
Nexus init: <1s
DataFlow init with enable_model_persistence=False: <0.1s per model
Total for 3 models: <2s
```

## Complete Working Example

```python
from nexus import Nexus
from dataflow import DataFlow
from kailash.workflow.builder import WorkflowBuilder

# Fast initialization
app = Nexus(
    api_port=8000,
    mcp_port=3001,
    auto_discovery=False  # CRITICAL
)

db = DataFlow(
    database_url="postgresql://localhost:5432/mydb",
    enable_model_persistence=False,  # CRITICAL: Skip model registry for fast startup
    auto_migrate=False,
    skip_migration=True,
    enable_metrics=True,  # Keep monitoring
    enable_caching=True,  # Keep caching
    connection_pool_size=20  # Keep pooling
)

# Define models (instant!)
@db.model
class Contact:
    id: str
    name: str
    email: str
    company: str

@db.model
class Company:
    id: str
    name: str
    industry: str

# Create workflow using DataFlow nodes
def create_contact_workflow():
    workflow = WorkflowBuilder()

    # Use DataFlow's auto-generated nodes
    workflow.add_node("ContactCreateNode", "create", {
        "name": "{{name}}",
        "email": "{{email}}",
        "company": "{{company}}"
    })

    return workflow.build()

# Register workflow
app.register("create_contact", create_contact_workflow())

# Start (fast!)
app.start()
```

## What You Keep

With optimized settings, you still get:
- All CRUD operations (9 nodes per model)
- Connection pooling, caching, metrics
- All Nexus channels (API, CLI, MCP)
- Fast <2 second total startup time

## What You Lose

With optimized settings, you lose:
- Model persistence across restarts
- Automatic migration tracking
- Runtime model discovery
- Auto-discovery of workflows

## Trade-off Decision

### Use Optimized Settings When:
- Fast startup is critical (<2s)
- Running in Docker/Kubernetes
- Frequent container restarts
- Development/testing environments

### Use Full Features When:
- Model persistence required across restarts
- Automatic migration tracking needed
- Multiple applications share models
- Startup time acceptable (10-30s)

## Full Features Configuration

If you need all features and accept 10-30s startup:

```python
app = Nexus(
    api_port=8000,
    mcp_port=3001,
    auto_discovery=False  # Still recommended with DataFlow
)

db = DataFlow(
    database_url="postgresql://localhost:5432/mydb",
    enable_model_persistence=True,   # Enable persistence (slower startup)
    auto_migrate=True,
    skip_migration=False
)
```

See [Full Features Guide](../../sdk-users/apps/dataflow/docs/integration/dataflow-nexus-full-features.md) for details.

## Using DataFlow Nodes

```python
# DataFlow auto-generates 9 nodes per model:
# - Create, Read, Update, Delete
# - List, Search, Count
# - Bulk operations

workflow = WorkflowBuilder()

# Create node
workflow.add_node("ContactCreateNode", "create", {
    "name": "{{name}}",
    "email": "{{email}}"
})

# Search node
workflow.add_node("ContactSearchNode", "search", {
    "filter": {"company": "{{company}}"},
    "limit": 10
})

# Connect nodes
workflow.add_connection("create", "result", "search", "input")

app.register("contact_workflow", workflow.build())
```

## API Usage

```bash
# Create contact via Nexus API
curl -X POST http://localhost:8000/workflows/create_contact/execute \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {
      "name": "John Doe",
      "email": "john@example.com",
      "company": "Acme Corp"
    }
  }'
```

## Production Pattern

```python
import os

def create_production_app():
    # Fast initialization for production
    app = Nexus(
        api_port=int(os.getenv("API_PORT", "8000")),
        mcp_port=int(os.getenv("MCP_PORT", "3001")),
        auto_discovery=False,
        enable_auth=True,
        enable_monitoring=True
    )

    db = DataFlow(
        database_url=os.getenv("DATABASE_URL"),
        enable_model_persistence=False,  # Skip model registry for fast startup
        auto_migrate=False,
        skip_migration=True,
        enable_metrics=True,
        enable_caching=True,
        connection_pool_size=20
    )

    # Register models
    from .models import Contact, Company  # Import after DataFlow creation

    # Register workflows
    register_workflows(app, db)

    return app

app = create_production_app()
```

## Common Issues

### Slow Startup
```python
# Ensure both settings are configured
app = Nexus(auto_discovery=False)
db = DataFlow(enable_model_persistence=False)
```

### Blocking on Start
```python
# Must disable auto_discovery
app = Nexus(auto_discovery=False)
```

### Workflows Not Found
```python
# Register manually since auto_discovery is off
app.register("workflow-name", workflow.build())
```

### Models Not Persisting
```python
# Expected behavior with enable_model_persistence=False
# Models only exist while app is running
# Use full features config if persistence needed
```

## Testing Strategy

```python
import pytest
import requests

def test_nexus_dataflow_integration():
    # Test fast startup
    start_time = time.time()

    app = Nexus(auto_discovery=False)
    db = DataFlow(enable_model_persistence=False)

    @db.model
    class TestModel:
        id: str
        name: str

    startup_time = time.time() - start_time
    assert startup_time < 2.0, f"Startup too slow: {startup_time}s"

    # Test workflow execution
    workflow = WorkflowBuilder()
    workflow.add_node("TestModelCreateNode", "create", {"name": "test"})
    app.register("test", workflow.build())

    # Test via API
    response = requests.post(
        "http://localhost:8000/workflows/test/execute",
        json={"inputs": {"name": "test"}}
    )
    assert response.status_code == 200
```

## Key Takeaways

- **CRITICAL**: Use `auto_discovery=False` with DataFlow
- **CRITICAL**: Use `enable_model_persistence=False` for fast startup and instant models
- Optimized config: <2s startup
- Full features config: 10-30s startup
- All CRUD operations work with both configs
- Manual workflow registration required

## Related Documentation

- [Main Integration Guide](../../sdk-users/guides/dataflow-nexus-integration.md)
- [Full Features Config](../../sdk-users/apps/dataflow/docs/integration/dataflow-nexus-full-features.md)
- [Blocking Issue Analysis](../../sdk-users/apps/dataflow/docs/integration/nexus-blocking-issue-analysis.md)
- [Working Examples](../../sdk-users/apps/nexus/examples/dataflow-integration/)

## Related Skills

- [nexus-quickstart](#) - Basic Nexus setup
- [dataflow-quickstart](#) - Basic DataFlow setup
- [nexus-production-deployment](#) - Production patterns
- [nexus-troubleshooting](#) - Fix integration issues
