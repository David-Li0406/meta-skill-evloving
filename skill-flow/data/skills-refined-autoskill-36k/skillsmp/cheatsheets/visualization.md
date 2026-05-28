---
name: workflow-visualization
description: "Visualize workflows as diagrams, flowcharts, or graphs for documentation and debugging. Use when asking 'visualize workflow', 'workflow diagram', 'flow chart', 'workflow graph', 'visualize nodes', or 'workflow visualization'."
---

# Workflow Visualization

Workflow Visualization guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `patterns`
> Priority: `LOW`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Workflow Visualization
- **Category**: patterns
- **Priority**: LOW
- **Trigger Keywords**: visualize workflow, workflow diagram, flow chart, workflow graph, visualize nodes

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Visualization implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/visualization.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Visualization Core Functionality**: Primary operations and common patterns
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
- [`sdk-users/2-core-concepts/cheatsheet/010-visualization.md`](../../../sdk-users/2-core-concepts/cheatsheet/010-visualization.md)

## Quick Tips

- 💡 **Tip 1**: Always follow Workflow Visualization best practices
- 💡 **Tip 2**: Test patterns incrementally
- 💡 **Tip 3**: Reference documentation for details

## Keywords for Auto-Trigger

<!-- Trigger Keywords: visualize workflow, workflow diagram, flow chart, workflow graph, visualize nodes -->
