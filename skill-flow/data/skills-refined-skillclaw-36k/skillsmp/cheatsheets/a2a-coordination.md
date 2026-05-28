---
name: a2a-coordination
description: "Multi-agent coordination using A2A protocol for distributed AI systems. Use when asking 'A2A', 'agent coordination', 'multi-agent', 'agent-to-agent', 'distributed agents', 'A2A protocol', or 'agent collaboration'."
---

# Agent-to-Agent (A2A) Coordination

Agent-to-Agent (A2A) Coordination guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `kaizen`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Agent-to-Agent (A2A) Coordination
- **Category**: kaizen
- **Priority**: HIGH
- **Trigger Keywords**: A2A, agent coordination, multi-agent, agent-to-agent, distributed agents

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# A2A Coordination implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/a2a-coordination.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **A2A-Coordination Core Functionality**: Primary operations and common patterns
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
- [`sdk-users/2-core-concepts/cheatsheet/023-a2a-agent-coordination.md`](../../../sdk-users/2-core-concepts/cheatsheet/023-a2a-agent-coordination.md)

## Quick Tips

- 💡 **Tip 1**: Always follow Agent-to-Agent (A2A) Coordination best practices
- 💡 **Tip 2**: Test patterns incrementally
- 💡 **Tip 3**: Reference documentation for details

## Keywords for Auto-Trigger

<!-- Trigger Keywords: A2A, agent coordination, multi-agent, agent-to-agent, distributed agents -->
