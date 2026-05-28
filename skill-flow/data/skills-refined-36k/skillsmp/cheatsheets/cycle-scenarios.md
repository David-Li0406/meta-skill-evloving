---
name: cycle-scenarios
description: "Real-world cycle scenario patterns for ETL, polling, quality improvement. Use when asking 'cycle scenarios', 'cycle patterns', 'ETL retry', 'API polling', or 'quality improvement'."
---

# Cycle Scenarios

Cycle Scenarios patterns for building robust cyclic workflows.

> **Skill Metadata**
> Category: `core-patterns`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Cycle Scenarios
- **Category**: core-patterns
- **Priority**: HIGH
- **Trigger Keywords**: cycle scenarios, cycle patterns, ETL retry, API polling, quality improvement

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Cycle Scenarios implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/cycle-scenarios.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Cycle-Scenarios Workflows**: Implement loops, iterative processing, feedback loops with cycle-aware nodes
- **State Management**: Track iteration count, accumulate results, persist state across cycles
- **Termination Conditions**: Max iterations, threshold checks, convergence criteria, timeout handling
- **Performance**: Cycle limit optimization, memory management, state cleanup, resource pooling
- **Testing**: Validate cycle behavior, test termination, check for infinite loops, memory leak detection

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

<!-- Trigger Keywords: cycle scenarios, cycle patterns, ETL retry, API polling, quality improvement -->
