---
name: workflow-patterns-library
description: "Library of common workflow patterns including ETL, RAG, API integration, and data processing. Use when asking 'workflow patterns', 'common patterns', 'pattern library', 'ETL pattern', 'RAG pattern', 'workflow examples', or 'design patterns'."
---

# Workflow Patterns Library

Workflow Patterns Library guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `patterns`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Workflow Patterns Library
- **Category**: patterns
- **Priority**: HIGH
- **Trigger Keywords**: workflow patterns, common patterns, pattern library, ETL pattern, RAG pattern

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Workflow Patterns Library implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/workflow-patterns-library.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Workflow-Patterns-Library Workflows**: Pre-built patterns for common use cases with best practices built-in
- **Composition Patterns**: Combine multiple workflows, create reusable sub-workflows, build complex orchestrations
- **Error Handling**: Built-in retry logic, fallback paths, compensation actions for resilient workflows
- **Performance Optimization**: Parallel execution, batch operations, async patterns for high-throughput processing
- **Production Readiness**: Health checks, monitoring, logging, metrics collection for enterprise deployments

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
- [`sdk-users/2-core-concepts/cheatsheet/012-common-workflow-patterns.md`](../../../sdk-users/2-core-concepts/cheatsheet/012-common-workflow-patterns.md)
- [`sdk-users/2-core-concepts/workflows/by-pattern/`](../../../sdk-users/2-core-concepts/workflows/by-pattern/)

## Quick Tips

- 💡 **Tip 1**: Always follow Workflow Patterns Library best practices
- 💡 **Tip 2**: Test patterns incrementally
- 💡 **Tip 3**: Reference documentation for details

## Keywords for Auto-Trigger

<!-- Trigger Keywords: workflow patterns, common patterns, pattern library, ETL pattern, RAG pattern -->
