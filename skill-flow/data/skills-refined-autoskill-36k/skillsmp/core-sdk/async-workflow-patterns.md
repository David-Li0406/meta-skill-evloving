---
name: async-workflow-patterns
description: "Asynchronous workflow execution with AsyncLocalRuntime for Docker and FastAPI deployments. Use when asking 'async workflow', 'AsyncLocalRuntime', 'async execution', 'Docker deployment', 'FastAPI workflow', 'async patterns', 'concurrent execution', 'async runtime', or 'asynchronous processing'."
---

# Async Workflow Patterns

Async Workflow Patterns guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `core-sdk`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Async Workflow Patterns
- **Category**: core-sdk
- **Priority**: HIGH
- **Trigger Keywords**: async workflow, AsyncLocalRuntime, async execution, Docker deployment, FastAPI workflow

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Async Workflow Patterns implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/async-workflow-patterns.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Async-Workflow-Patterns Workflows**: Pre-built patterns for common use cases with best practices built-in
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
- [`sdk-users/2-core-concepts/cheatsheet/async-workflow-patterns.md`](../../../sdk-users/2-core-concepts/cheatsheet/async-workflow-patterns.md)
- [`CLAUDE.md#L117-132`](../../{doc})

## Quick Tips

- 💡 **Tip 1**: Always follow Async Workflow Patterns best practices
- 💡 **Tip 2**: Test patterns incrementally
- 💡 **Tip 3**: Reference documentation for details

## Keywords for Auto-Trigger

<!-- Trigger Keywords: async workflow, AsyncLocalRuntime, async execution, Docker deployment, FastAPI workflow -->
