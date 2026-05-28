---
name: mcp-resources
description: "MCP resource templates, subscriptions, and URIs. Use when asking 'MCP resources', 'resource template', 'subscriptions', 'mcp uri', or 'resource management'."
---

# MCP Resources

Manage MCP resources with templates, subscriptions, and URI-based access.

> **Skill Metadata**
> Category: `mcp`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`
> Related Skills: [`mcp-structured-tools`](mcp-structured-tools.md), [`mcp-integration-guide`](../../01-core-sdk/mcp-integration-guide.md)
> Related Subagents: `mcp-specialist` (resource lifecycles, subscriptions)

## Quick Reference

- **Resources**: Named entities exposing structured data (documents, databases, APIs)
- **Templates**: Parameterized resource definitions
- **Subscriptions**: Real-time resource change notifications
- **URIs**: Unique identifiers for resource access

## Basic Resource Access

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

workflow = WorkflowBuilder()

workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Get document content"}],
    "mcp_servers": [{
        "name": "docs",
        "transport": "http",
        "url": "https://api.company.com/mcp",
        "resources": [
            {
                "uri": "doc://company/reports/2024/annual",
                "name": "Annual Report 2024",
                "mimeType": "application/pdf"
            }
        ]
    }]
})
```

## Resource Templates

```python
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "mcp_servers": [{
        "name": "db",
        "transport": "http",
        "url": "https://db-api.com/mcp",
        "resource_templates": [
            {
                "uriTemplate": "db://users/{user_id}/profile",
                "name": "User Profile",
                "description": "Get user profile by ID",
                "mimeType": "application/json"
            },
            {
                "uriTemplate": "db://orders/{order_id}",
                "name": "Order Details",
                "mimeType": "application/json"
            }
        ]
    }]
})

# Agent can request: db://users/123/profile
```

## Resource Subscriptions

```python
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "mcp_servers": [{
        "name": "metrics",
        "transport": "websocket",
        "url": "wss://metrics-api.com/mcp",
        "resources": [
            {
                "uri": "metrics://system/cpu",
                "name": "CPU Metrics",
                "subscriptions": {
                    "enabled": True,
                    "update_interval": 5  # seconds
                }
            },
            {
                "uri": "metrics://system/memory",
                "name": "Memory Metrics",
                "subscriptions": {
                    "enabled": True,
                    "update_interval": 10
                }
            }
        ]
    }]
})
```

## Related Patterns

- **Structured Tools**: [`mcp-structured-tools`](mcp-structured-tools.md)
- **MCP Integration**: [`mcp-integration-guide`](../../01-core-sdk/mcp-integration-guide.md)

## When to Escalate

Use `mcp-specialist` for complex resource lifecycles and subscription management.

<!-- Trigger Keywords: MCP resources, resource template, subscriptions, mcp uri, resource management -->
