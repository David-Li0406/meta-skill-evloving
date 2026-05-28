---
name: performance-optimization
description: "Performance optimization patterns for workflows. Use when asking 'performance', 'optimize workflows', 'workflow speed', 'performance tuning', or 'workflow optimization'."
---

# Performance Optimization

Performance Optimization guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `production`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Performance Optimization
- **Category**: production
- **Priority**: HIGH
- **Trigger Keywords**: performance, optimize workflows, workflow speed, performance tuning

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Performance Optimization implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/performance-optimization.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Performance-Optimization Core Functionality**: Primary operations and common patterns
- **Integration Patterns**: Connect with other nodes, workflows, external systems
- **Error Handling**: Robust error handling with retries, fallbacks, and logging
- **Performance**: Optimization techniques, caching, batch operations, async execution
- **Production Use**: Enterprise-grade patterns with monitoring, security, and reliability

## Related Patterns

- **For fundamentals**: See [`workflow-quickstart`](#)
- **For patterns**: See [`workflow-patterns-library`](#)
- **For parameters**: See [`param-passing-quick`](#)

## When to Escalate to Subagent

Use specialized subagents when:
- **pattern-expert**: Complex patterns, multi-node workflows
- **sdk-navigator**: Error resolution, parameter issues
- **testing-specialist**: Comprehensive testing strategies

## Documentation References

### Primary Sources
- [`sdk-users/2-core-concepts/cheatsheet/`](../../../sdk-users/2-core-concepts/cheatsheet/)

## Quick Tips

- 💡 **Tip 1**: Follow best practices from documentation
- 💡 **Tip 2**: Test patterns incrementally
- 💡 **Tip 3**: Reference examples for complex cases

## Keywords for Auto-Trigger

<!-- Trigger Keywords: performance, optimize workflows, workflow speed, performance tuning -->
