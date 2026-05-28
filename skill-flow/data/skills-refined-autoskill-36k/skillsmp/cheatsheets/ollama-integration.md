---
name: ollama-integration
description: "Integrate Ollama for local LLM execution without external API dependencies. Use when asking 'Ollama', 'local LLM', 'Ollama integration', 'local models', 'self-hosted LLM', or 'Ollama patterns'."
---

# Ollama Integration Patterns

Ollama Integration Patterns guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `patterns`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Ollama Integration Patterns
- **Category**: patterns
- **Priority**: HIGH
- **Trigger Keywords**: Ollama, local LLM, Ollama integration, local models, self-hosted LLM

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Ollama Integration implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/ollama-integration.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Ollama-Integration Processing**: Extract, transform, load data from various sources with validation
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
- [`sdk-users/2-core-concepts/cheatsheet/045-ollama-integration-patterns.md`](../../../sdk-users/2-core-concepts/cheatsheet/045-ollama-integration-patterns.md)

## Quick Tips

- 💡 **Tip 1**: Always follow Ollama Integration Patterns best practices
- 💡 **Tip 2**: Test patterns incrementally
- 💡 **Tip 3**: Reference documentation for details

## Keywords for Auto-Trigger

<!-- Trigger Keywords: Ollama, local LLM, Ollama integration, local models, self-hosted LLM -->
