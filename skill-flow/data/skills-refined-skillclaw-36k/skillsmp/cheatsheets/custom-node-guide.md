---
name: custom-node-guide
description: "Create custom nodes by extending Node base class with parameters and execution logic. Use when asking 'custom node', 'create node', 'extend node', 'node development', 'NodeParameter', 'custom logic', or 'build node'."
---

# Custom Node Creation Guide

Custom Node Creation Guide guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `patterns`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Custom Node Creation Guide
- **Category**: patterns
- **Priority**: MEDIUM
- **Trigger Keywords**: custom node, create node, extend node, node development, NodeParameter

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Custom Node Guide implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/custom-node-guide.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Custom-Node-Guide Core Functionality**: Primary operations and common patterns
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
- [`sdk-users/2-core-concepts/cheatsheet/011-custom-node-creation.md`](../../../sdk-users/2-core-concepts/cheatsheet/011-custom-node-creation.md)
- [`sdk-users/7-gold-standards/custom-node-development-guide.md`](../../../sdk-users/7-gold-standards/custom-node-development-guide.md)

## Quick Tips

- 💡 **Tip 1**: Always follow Custom Node Creation Guide best practices
- 💡 **Tip 2**: Test patterns incrementally
- 💡 **Tip 3**: Reference documentation for details

## Keywords for Auto-Trigger

<!-- Trigger Keywords: custom node, create node, extend node, node development, NodeParameter -->
