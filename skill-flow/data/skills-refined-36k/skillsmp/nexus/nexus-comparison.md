---
name: nexus-comparison
description: "Nexus vs alternatives (FastAPI, Flask, Typer). Use when asking 'nexus vs fastapi', 'why nexus', or 'nexus benefits'."
---

# Nexus vs Alternatives

> **Skill Metadata**
> Category: `nexus`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`

## Nexus vs FastAPI

| Feature | Nexus | FastAPI |
|---------|-------|---------|
| **API** | ✅ Built-in | ✅ Native |
| **CLI** | ✅ Built-in | ❌ Need Typer |
| **MCP** | ✅ Built-in | ❌ Manual setup |
| **Session Management** | ✅ Unified | ❌ Manual |
| **Workflow Integration** | ✅ Native | ❌ Manual |
| **Learning Curve** | Low | Medium |

## When to Use Nexus

```python
# ✅ Use Nexus when you need:
# - API + CLI + MCP in one app
# - Session management across channels
# - Direct workflow execution
# - Minimal boilerplate

from nexus import Nexus

app = Nexus(workflow, name="MyApp")
app.run()  # All channels ready!
```

## When to Use FastAPI

```python
# ✅ Use FastAPI when you need:
# - Pure REST API only
# - Custom middleware/auth
# - Full control over routing
# - Non-workflow logic

from fastapi import FastAPI

app = FastAPI()

@app.post("/execute")
def execute():
    # Manual workflow execution
    pass
```

## Migration from FastAPI to Nexus

```python
# Before (FastAPI)
from fastapi import FastAPI
app = FastAPI()

@app.post("/chat")
def chat(message: str):
    # Build workflow
    # Execute workflow
    # Return results
    pass

# After (Nexus)
from nexus import Nexus

app = Nexus(chat_workflow, name="ChatApp")
app.run()  # API + CLI + MCP!
```

## Key Benefits

1. **Zero boilerplate** - One line deploys all channels
2. **Unified sessions** - Same session across API/CLI/MCP
3. **Native workflows** - Direct workflow execution
4. **Built-in CLI** - Automatic CLI generation
5. **MCP ready** - Claude Desktop integration

## Documentation

- **Nexus Guide**: [`sdk-users/apps/nexus/README.md`](../../../../sdk-users/apps/nexus/README.md)
- **FastAPI Comparison**: [`sdk-users/apps/nexus/10-comparison.md`](../../../../sdk-users/apps/nexus/10-comparison.md)

<!-- Trigger Keywords: nexus vs fastapi, why nexus, nexus benefits, nexus vs flask, nexus alternatives -->
