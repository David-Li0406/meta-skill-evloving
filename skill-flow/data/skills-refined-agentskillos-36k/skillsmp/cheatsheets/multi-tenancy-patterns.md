---
name: multi-tenancy-patterns
description: "Multi-tenant architecture patterns with tenant isolation and access control. Use when asking 'multi-tenant', 'multi-tenancy', 'tenant isolation', 'multi tenant', 'tenant ID', 'tenant context', or 'isolation patterns'."
---

# Multi-Tenancy Patterns

Multi-Tenancy Patterns guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `patterns`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Multi-Tenancy Patterns
- **Category**: patterns
- **Priority**: MEDIUM
- **Trigger Keywords**: multi-tenant, multi-tenancy, tenant isolation, multi tenant, tenant ID

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Multi Tenancy Patterns implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/multi-tenancy-patterns.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Multi-Tenancy-Patterns Workflows**: Pre-built patterns for common use cases with best practices built-in
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
- [`sdk-users/2-core-concepts/cheatsheet/014-access-control-multi-tenancy.md`](../../../sdk-users/2-core-concepts/cheatsheet/014-access-control-multi-tenancy.md)

## Quick Tips

- 💡 **Tip 1**: Always follow Multi-Tenancy Patterns best practices
- 💡 **Tip 2**: Test patterns incrementally
- 💡 **Tip 3**: Reference documentation for details

## Keywords for Auto-Trigger

<!-- Trigger Keywords: multi-tenant, multi-tenancy, tenant isolation, multi tenant, tenant ID -->
