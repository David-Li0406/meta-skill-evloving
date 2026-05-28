---
name: mcp-integration-guide
description: "Model Context Protocol (MCP) integration for tool calling and resource management. Use when asking 'MCP', 'Model Context Protocol', 'MCP integration', 'MCP server', 'tool calling', 'MCP resources', 'MCP client', 'protocol integration', or 'MCP setup'."
---

# MCP Integration Guide

MCP Integration Guide guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `mcp`
> Priority: `CRITICAL`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: MCP Integration Guide
- **Category**: mcp
- **Priority**: CRITICAL
- **Trigger Keywords**: MCP, Model Context Protocol, MCP integration, MCP server, tool calling

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Mcp Integration Guide implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/mcp-integration-guide.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Mcp-Integration-Guide Processing**: Extract, transform, load data from various sources with validation
- **Format Conversion**: CSV, JSON, XML, Parquet conversions with schema validation and type handling
- **API Integration**: REST, GraphQL, WebSocket integrations with authentication and error handling
- **Batch Processing**: High-volume data processing with streaming, pagination, and memory optimization
- **Data Quality**: Validation, deduplication, enrichment, normalization for clean data pipelines

## Related Patterns

- **For fundamentals**: See [`workflow-quickstart`](#)
- **For connections**: See [`connection-patterns`](#)
- **For parameters**: See [`param-passing-quick`](#)

## When to Escalate to Subagent

Use specialized subagents when:
- Complex implementation needed
- Production deployment required
- Deep analysis necessary
- Enterprise patterns needed

## Documentation References

### Primary Sources
- [`sdk-users/2-core-concepts/cheatsheet/025-mcp-integration.md`](../../../sdk-users/2-core-concepts/cheatsheet/025-mcp-integration.md)
- [`sdk-users/3-development/17-mcp-development-guide.md`](../../../sdk-users/3-development/17-mcp-development-guide.md)

## Quick Tips

- 💡 **Tip 1**: Always follow MCP Integration Guide best practices
- 💡 **Tip 2**: Test patterns incrementally
- 💡 **Tip 3**: Reference documentation for details

## Keywords for Auto-Trigger

<!-- Trigger Keywords: MCP, Model Context Protocol, MCP integration, MCP server, tool calling -->
