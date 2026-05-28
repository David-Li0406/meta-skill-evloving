---
name: decide-node-for-task
description: "Select appropriate nodes from 110+ options for specific tasks and use cases. Use when asking 'which node', 'node for task', 'choose node', 'node selection', 'what node', or 'node recommendation'."
---

# Decision: Node Selection

Decision: Node Selection guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `cross-cutting`
> Priority: `CRITICAL`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Decision: Node Selection
- **Category**: cross-cutting
- **Priority**: CRITICAL
- **Trigger Keywords**: which node, node for task, choose node, node selection, what node

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Decide Node For Task implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/decide-node-for-task.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Decide-Node-For-Task Core Functionality**: Primary operations and common patterns
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
- [`sdk-users/2-core-concepts/cheatsheet/041-choosing-the-right-node.md`](../../../sdk-users/2-core-concepts/cheatsheet/041-choosing-the-right-node.md)
- [`sdk-users/2-core-concepts/nodes/comprehensive-node-catalog.md`](../../../sdk-users/2-core-concepts/nodes/comprehensive-node-catalog.md)

## Quick Tips

- 💡 **Tip 1**: Always follow Decision: Node Selection best practices
- 💡 **Tip 2**: Test patterns incrementally
- 💡 **Tip 3**: Reference documentation for details

## Keywords for Auto-Trigger

<!-- Trigger Keywords: which node, node for task, choose node, node selection, what node -->
