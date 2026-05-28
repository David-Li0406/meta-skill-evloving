---
name: nodes-api-reference
description: "API nodes reference (HTTP, REST, GraphQL). Use when asking 'API node', 'HTTP', 'REST', 'GraphQL', or 'API request'."
---

# API Nodes Reference

Complete reference for HTTP, REST, and GraphQL API operations.

> **Skill Metadata**
> Category: `nodes`
> Priority: `HIGH`
> SDK Version: `0.9.25+`
> Related Skills: [`nodes-quick-index`](nodes-quick-index.md)
> Related Subagents: `pattern-expert` (API workflows)

## Quick Reference

```python
from kailash.nodes.api import (
    HTTPRequestNode,
    AsyncHTTPRequestNode,
    RESTClientNode,
    AsyncRESTClientNode,
    GraphQLClientNode
)
```

## HTTP Nodes

### HTTPRequestNode
```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

workflow.add_node("HTTPRequestNode", "api_call", {
    "url": "https://api.example.com/data",
    "method": "GET",
    "headers": {
        "Authorization": "Bearer ${API_TOKEN}",
        "Content-Type": "application/json"
    },
    "params": {"page": 1, "limit": 100}
})
```

### AsyncHTTPRequestNode
```python
workflow.add_node("AsyncHTTPRequestNode", "async_api", {
    "url": "https://api.example.com/users",
    "method": "POST",
    "json": {"name": "John", "email": "john@example.com"},
    "timeout": 30
})
```

## REST Nodes

### RESTClientNode
```python
workflow.add_node("RESTClientNode", "rest_api", {
    "base_url": "https://api.example.com",
    "endpoint": "/users/123",
    "method": "GET",
    "auth": {"type": "bearer", "token": "${API_TOKEN}"}
})
```

## GraphQL Nodes

### GraphQLClientNode
```python
workflow.add_node("GraphQLClientNode", "graphql", {
    "url": "https://api.example.com/graphql",
    "query": """
        query GetUser($id: ID!) {
            user(id: $id) {
                id
                name
                email
            }
        }
    """,
    "variables": {"id": "123"}
})
```

## Related Skills

- **Node Index**: [`nodes-quick-index`](nodes-quick-index.md)

## Documentation

- **API Nodes**: [`sdk-users/2-core-concepts/nodes/04-api-nodes.md`](../../../../sdk-users/2-core-concepts/nodes/04-api-nodes.md)

<!-- Trigger Keywords: API node, HTTP, REST, GraphQL, API request, HTTPRequestNode, RESTClientNode, GraphQLClientNode -->
