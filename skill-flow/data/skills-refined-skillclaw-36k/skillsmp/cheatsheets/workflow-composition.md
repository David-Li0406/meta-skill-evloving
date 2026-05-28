---
name: workflow-composition
description: "Composing workflows from reusable components. Use when asking 'workflow composition', 'compose workflows', 'reusable workflows', 'modular workflows', or 'workflow components'."
---

# Workflow Composition

Workflow Composition guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `core-patterns`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Workflow Composition
- **Category**: core-patterns
- **Priority**: HIGH
- **Trigger Keywords**: workflow composition, compose workflows, reusable workflows, modular workflows

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Workflow Composition implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/workflow-composition.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Workflow-Composition Workflows**: Pre-built patterns for common use cases with best practices built-in
- **Composition Patterns**: Combine multiple workflows, create reusable sub-workflows, build complex orchestrations
- **Error Handling**: Built-in retry logic, fallback paths, compensation actions for resilient workflows
- **Performance Optimization**: Parallel execution, batch operations, async patterns for high-throughput processing
- **Production Readiness**: Health checks, monitoring, logging, metrics collection for enterprise deployments

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

<!-- Trigger Keywords: workflow composition, compose workflows, reusable workflows, modular workflows -->
