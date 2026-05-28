---
skill: nexus-quickstart
description: Zero-config Nexus() setup and basic workflow registration. Start here for all Nexus applications.
priority: CRITICAL
tags: [nexus, quickstart, zero-config, setup]
---

# Nexus Quickstart

Zero-configuration platform deployment. Get running in 30 seconds.

## Instant Start

```python
from nexus import Nexus

# Zero configuration required
app = Nexus()
app.start()
```

That's it! You now have:
- API Server on `http://localhost:8000`
- Health Check at `http://localhost:8000/health`
- MCP Server on port 3001
- Auto-discovery enabled

## Add Your First Workflow

```python
from nexus import Nexus
from kailash.workflow.builder import WorkflowBuilder

# Create platform
app = Nexus()

# Create workflow
workflow = WorkflowBuilder()
workflow.add_node("HTTPRequestNode", "fetch", {
    "url": "https://httpbin.org/json",
    "method": "GET"
})

# Register once, available everywhere
app.register("fetch-data", workflow.build())  # Must call .build()

# Start platform
app.start()
```

## Test All Three Channels

**API (HTTP)**:
```bash
curl -X POST http://localhost:8000/workflows/fetch-data/execute
```

**CLI**:
```bash
nexus run fetch-data
```

**MCP** (for AI agents):
```json
{
  "method": "tools/call",
  "params": {"name": "fetch-data", "arguments": {}}
}
```

## Critical Patterns

### Always Call .build()
```python
# CORRECT
app.register("workflow-name", workflow.build())

# WRONG - Will fail
app.register("workflow-name", workflow)
```

### Correct Parameter Order
```python
# CORRECT - name first, workflow second
app.register("name", workflow.build())

# WRONG - reversed
app.register(workflow.build(), "name")
```

## Common Issues

### Port Conflicts
```python
# Use custom ports if defaults are taken
app = Nexus(api_port=8001, mcp_port=3002)
```

### Import Errors
```bash
pip install kailash-nexus
```

### Workflow Not Found
```python
# Ensure .build() is called
workflow = WorkflowBuilder()
workflow.add_node("PythonCodeNode", "test", {"code": "result = {'ok': True}"})
app.register("test", workflow.build())  # Don't forget .build()
```

## Next Steps

- Add parameters: See [nexus-workflow-registration](#)
- Use multiple channels: See [nexus-multi-channel](#)
- Integrate DataFlow: See [nexus-dataflow-integration](#)

## Key Takeaways

- Zero configuration: Just `Nexus()` and go
- Always call `.build()` before registration
- Single registration creates API + CLI + MCP
- Default ports: 8000 (API), 3001 (MCP)
