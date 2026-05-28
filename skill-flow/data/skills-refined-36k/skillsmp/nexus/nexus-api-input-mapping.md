---
skill: nexus-api-input-mapping
description: CRITICAL - How API inputs map to workflow node parameters, including try/except patterns and connection usage
priority: CRITICAL
tags: [nexus, api, input-mapping, parameters, pythoncode]
---

# Nexus API Input Mapping

CRITICAL: Understanding how API inputs map to node parameters.

## The Complete Flow

```
API Request: {"inputs": {"sector": "Tech", "limit": 10}}
     ↓
Nexus receives as WorkflowRequest.inputs
     ↓
Runtime executes: runtime.execute(workflow, parameters={...})
     ↓
ALL nodes receive the FULL inputs dict as parameters
     ↓
PythonCodeNode accesses via try/except pattern
```

## Key Concepts

### Terminology Mapping

| API Layer | Runtime Layer | Node Layer |
|-----------|---------------|------------|
| `{"inputs": {...}}` | `parameters={...}` | Variable access |
| Request body field | Runtime execution parameter | Injected local variable |

**Important**: The API uses `"inputs"` for clarity, but internally it becomes `parameters` in the runtime.

### Broadcasting Behavior

**CRITICAL**: Nexus broadcasts the ENTIRE inputs dict to ALL nodes in the workflow.

```python
# API Request
{
  "inputs": {
    "sector": "Technology",
    "geography": "North America",
    "limit": 50
  }
}

# What EVERY node receives as parameters:
{
  "sector": "Technology",
  "geography": "North America",
  "limit": 50
}
```

## PythonCodeNode Parameter Access

### WRONG Patterns

```python
# ❌ NO 'inputs' variable exists
sector = inputs.get('sector')

# ❌ locals() is restricted
sector = locals().get('sector')

# ❌ globals() is also restricted
sector = globals().get('sector')
```

### CORRECT Pattern

```python
# ✅ Use try/except for optional parameters
try:
    s = sector  # Will be injected if provided in API inputs
except NameError:
    s = None

try:
    g = geography
except NameError:
    g = None

try:
    lim = limit
except NameError:
    lim = 100  # Default value

# Now use s, g, lim safely
filters = {}
if s:
    filters['sector'] = s
if g:
    filters['geography'] = g

result = {'filters': filters, 'limit': lim}
```

## Complete Working Example

```python
from nexus import Nexus
from kailash.workflow.builder import WorkflowBuilder

app = Nexus()

# Build workflow
workflow = WorkflowBuilder()

# Node 1: Build filters from API inputs
workflow.add_node("PythonCodeNode", "prepare_filters", {
    "code": """
# Access optional parameters via try/except
try:
    s = sector
except NameError:
    s = None

try:
    g = geography
except NameError:
    g = None

try:
    lim = limit
except NameError:
    lim = 100

# Build filters
filters = {}
if s and str(s).strip():
    filters['sector'] = str(s).strip()
if g and str(g).strip():
    filters['geography'] = str(g).strip()

# Output for next node
result = {
    'filters': filters,
    'limit': lim
}
"""
})

# Node 2: Execute search
workflow.add_node("ContactListNode", "search", {
    "filter": {},   # Will be populated via connection
    "limit": 100
})

# Connect filter data from prepare_filters to search
workflow.add_connection(
    "prepare_filters", "result.filters",
    "search", "filter"
)

workflow.add_connection(
    "prepare_filters", "result.limit",
    "search", "limit"
)

# Register
app.register("contact_search", workflow.build())
app.start()
```

## API Usage

```bash
# Example 1: Search Technology sector
curl -X POST http://localhost:8000/workflows/contact_search/execute \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {
      "sector": "Technology",
      "limit": 10
    }
  }'

# Example 2: Search with geography
curl -X POST http://localhost:8000/workflows/contact_search/execute \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {
      "sector": "Healthcare",
      "geography": "Europe",
      "limit": 5
    }
  }'

# Example 3: No filters (get all)
curl -X POST http://localhost:8000/workflows/contact_search/execute \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {
      "limit": 100
    }
  }'
```

## Common Pitfalls

### Pitfall 1: Template Syntax in Node Config

```python
# ❌ WRONG: Template syntax not evaluated
workflow.add_node("ContactListNode", "search", {
    "filter": "${prepare_filters.result.filters}",  # Not evaluated!
    "limit": "${prepare_filters.result.limit}"
})

# ✅ CORRECT: Use explicit connections
workflow.add_node("ContactListNode", "search", {
    "filter": {},   # Default value
    "limit": 100
})

workflow.add_connection(
    "prepare_filters", "result.filters",
    "search", "filter"
)

workflow.add_connection(
    "prepare_filters", "result.limit",
    "search", "limit"
)
```

### Pitfall 2: Accessing Nested Output Incorrectly

```python
# ❌ WRONG: Missing 'result.' prefix
workflow.add_connection(
    "prepare_filters", "filters",  # Missing result.
    "search", "filter"
)

# ✅ CORRECT: Full path with dot notation
workflow.add_connection(
    "prepare_filters", "result.filters",  # Full path
    "search", "filter"
)
```

### Pitfall 3: Node-Specific vs Broadcast Parameters

```python
# ❌ WRONG: Trying to target specific nodes
{
  "inputs": {
    "prepare_filters": {"sector": "Tech"},  # Not supported
    "search": {"limit": 50}
  }
}

# ✅ CORRECT: Flat inputs + connections
{
  "inputs": {
    "sector": "Tech",
    "limit": 50
  }
}

# Use connections for node-to-node data flow
workflow.add_connection(
    "prepare_filters", "result",
    "search", "input"
)
```

## Backward Compatibility

Nexus supports both formats:

```python
# Modern format (preferred)
{"inputs": {"key": "value"}}

# Legacy format (still works)
{"parameters": {"key": "value"}}
```

## Debugging Tips

### Inspect Parameters

```python
workflow.add_node("PythonCodeNode", "debug", {
    "code": """
import json

# Debug what parameters are available
try:
    s = sector
    has_sector = True
except NameError:
    has_sector = False

try:
    lim = limit
    has_limit = True
except NameError:
    has_limit = False

result = {
    'debug_info': {
        'has_sector': has_sector,
        'sector_value': s if has_sector else None,
        'has_limit': has_limit,
        'limit_value': lim if has_limit else None
    }
}
"""
})
```

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Verify API Request

```bash
curl -v -X POST http://localhost:8000/workflows/contact_search/execute \
  -H "Content-Type: application/json" \
  -d '{"inputs": {"sector": "Technology"}}'
```

## Key Takeaways

1. API `{"inputs": {...}}` → Runtime `parameters={...}` → Node variables
2. ALL nodes receive the FULL inputs dict (broadcast)
3. Use try/except to access optional parameters in PythonCodeNode
4. Use explicit connections, NOT template syntax in node config
5. Access nested outputs with dot notation: `"result.filters"`
6. Nexus broadcasts inputs; use connections for node-to-node data flow

## Common Pattern Template

```python
# API Request
{"inputs": {"param1": "value1", "param2": 10}}

# Inside PythonCodeNode
try:
    p1 = param1  # "value1"
except NameError:
    p1 = None

try:
    p2 = param2  # 10
except NameError:
    p2 = 0

# Output
result = {'processed': True, 'data': {'p1': p1, 'p2': p2}}

# Connection to next node
workflow.add_connection(
    "process", "result.data",
    "next_node", "input"
)
```

## Related Documentation

- [Nexus API Reference](../../sdk-users/apps/nexus/docs/reference/api-reference.md)
- [Multi-Channel Usage](../../sdk-users/apps/nexus/docs/user-guides/multi-channel-usage.md)
- [PythonCodeNode Best Practices](../../2-core-concepts/cheatsheet/031-pythoncode-best-practices.md)

## Related Skills

- [nexus-api-patterns](#) - REST API usage
- [nexus-multi-channel](#) - API, CLI, MCP overview
- [nexus-troubleshooting](#) - Fix parameter issues
- [pythoncode-parameters](#) - PythonCodeNode parameter access
