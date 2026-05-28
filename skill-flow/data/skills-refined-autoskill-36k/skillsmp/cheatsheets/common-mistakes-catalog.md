---
name: common-mistakes-catalog
description: "Catalog of common mistakes and anti-patterns with solutions and fixes. Use when asking 'common mistakes', 'errors', 'gotchas', 'anti-patterns', 'what not to do', 'mistakes to avoid', or 'error catalog'."
---

# Common Mistakes Catalog

Common Mistakes Catalog guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `patterns`
> Priority: `CRITICAL`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Common Mistakes Catalog
- **Category**: patterns
- **Priority**: CRITICAL
- **Trigger Keywords**: common mistakes, errors, gotchas, anti-patterns, what not to do, mistakes to avoid

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Common Mistakes Catalog implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/common-mistakes-catalog.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Common-Mistakes-Catalog Core Functionality**: Primary operations and common patterns
- **Integration Patterns**: Connect with other nodes, workflows, external systems
- **Error Handling**: Robust error handling with retries, fallbacks, and logging
- **Performance**: Optimization techniques, caching, batch operations, async execution
- **Production Use**: Enterprise-grade patterns with monitoring, security, and reliability

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
- [`sdk-users/2-core-concepts/cheatsheet/018-common-mistakes-to-avoid.md`](../../../sdk-users/2-core-concepts/cheatsheet/018-common-mistakes-to-avoid.md)

## Quick Tips

- 💡 **Tip 1**: Always follow Common Mistakes Catalog best practices
- 💡 **Tip 2**: Test patterns incrementally
- 💡 **Tip 3**: Reference documentation for details

## Keywords for Auto-Trigger

<!-- Trigger Keywords: common mistakes, errors, gotchas, anti-patterns, what not to do, mistakes to avoid -->
