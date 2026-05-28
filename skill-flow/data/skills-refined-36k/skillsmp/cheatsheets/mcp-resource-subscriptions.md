---
name: mcp-resource-subscriptions
description: "MCP resource subscription patterns. Use when asking 'MCP subscriptions', 'resource subscriptions', 'MCP resources', 'subscribe resources', or 'MCP events'."
---

# Mcp Resource Subscriptions

Mcp Resource Subscriptions for MCP server integration and deployment.

> **Skill Metadata**
> Category: `mcp`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Mcp Resource Subscriptions
- **Category**: mcp
- **Priority**: HIGH
- **Trigger Keywords**: MCP subscriptions, resource subscriptions, MCP resources, subscribe resources

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Mcp Resource Subscriptions implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/mcp-resource-subscriptions.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Real-time Resource Notifications**: WebSocket-based pub/sub for file changes, config updates, API events with wildcard pattern matching
- **GraphQL-style Field Selection**: Request only needed fields to reduce bandwidth and improve client performance
- **Server-side Transformation Pipeline**: Enrich data, convert formats (CSV→JSON), aggregate from multiple sources before delivery
- **Batch Subscribe/Unsubscribe**: Efficiently manage 100s of subscriptions with atomic batch operations
- **Distributed MCP Servers**: Redis-backed multi-instance coordination with automatic failover and load balancing

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

- 💡 **Enable WebSocket Compression**: Set enable_websocket_compression=True with 1KB threshold for 60-80% bandwidth reduction
- 💡 **Use Pattern Matching**: Subscribe to `file://*.json` or `config://**/*` to match multiple resources efficiently
- 💡 **Field Selection for Mobile**: Request minimal fields for mobile clients to reduce data transfer and improve performance
- 💡 **Redis for Multi-Instance**: Use DistributedSubscriptionManager with Redis for production deployments with multiple MCP servers
- 💡 **Monitor Subscription Leaks**: Check active_subscriptions metrics and run cleanup_expired_subscriptions() periodically

## Keywords for Auto-Trigger

<!-- Trigger Keywords: MCP subscriptions, resource subscriptions, MCP resources, subscribe resources -->
