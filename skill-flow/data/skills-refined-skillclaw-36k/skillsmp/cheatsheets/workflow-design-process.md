---
name: workflow-design-process
description: "Systematic workflow design process and methodology. Use when asking 'workflow design', 'design process', 'workflow methodology', 'design patterns', or 'design workflow'."
---

# Workflow Design Process

Workflow Design Process guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `advanced`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Workflow Design Process
- **Category**: advanced
- **Priority**: HIGH
- **Trigger Keywords**: workflow design, design process, workflow methodology, design patterns

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Workflow Design Process implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/workflow-design-process.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Requirements to Workflow Mapping**: Systematic process to translate business requirements into workflow nodes and connections
- **Design Pattern Selection**: Choose appropriate patterns (ETL, RAG, API orchestration, cyclic) based on use case
- **Node Selection Strategy**: Identify right nodes for each task - database, API, AI, logic, transform, monitoring
- **Error Handling Design**: Plan error boundaries, retry policies, fallback paths, compensation logic upfront
- **Testing Strategy Planning**: Define test tiers (unit, integration, end-to-end) and test data requirements

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

- 💡 **Start with Workflow Diagram**: Draw nodes and connections before coding to visualize data flow and identify issues
- 💡 **Break Down Complex Logic**: Use multiple smaller nodes connected by data flow instead of one giant PythonCodeNode
- 💡 **Plan Error Paths Early**: Design SwitchNode branches, retry logic, and fallback workflows during design phase
- 💡 **Identify Reusable Patterns**: Check workflow-patterns-library for pre-built solutions before building from scratch
- 💡 **Consider Scale**: Design for production from start - connection pooling, batch operations, async execution

## Keywords for Auto-Trigger

<!-- Trigger Keywords: workflow design, design process, workflow methodology, design patterns -->
