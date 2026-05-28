---
name: switchnode-patterns
description: "Conditional data routing with SwitchNode using conditions and operators. Use when asking 'SwitchNode', 'conditional routing', 'if else workflow', 'route data', 'conditional logic', 'switch patterns', 'branch workflow', 'conditional flow', or 'routing patterns'."
---

# SwitchNode Conditional Routing

SwitchNode Conditional Routing guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `core-sdk`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: SwitchNode Conditional Routing
- **Category**: core-sdk
- **Priority**: HIGH
- **Trigger Keywords**: SwitchNode, conditional routing, if else workflow, route data, conditional logic

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Basic SwitchNode conditional routing
workflow = WorkflowBuilder()

workflow.add_node("SwitchNode", "switch", {
    "condition_field": "status",
    "operator": "==",
    "value": "active"
})

# Connect both branches
workflow.add_connection("switch", "true_output", "active_processor", "input")
workflow.add_connection("switch", "false_output", "inactive_processor", "input")

# Use skip_branches mode for best performance
runtime = LocalRuntime(conditional_execution="skip_branches")
results, run_id = runtime.execute(workflow.build())
```

## ⚠️ Dot Notation: Execution Mode Dependent

SwitchNode outputs are **mutually exclusive** - when `true_output` has data, `false_output` is `None`, and vice versa.

### ✅ skip_branches Mode (Recommended)
**Dot notation works perfectly** - inactive branches are automatically skipped:

```python
# Dot notation on SwitchNode outputs
workflow.add_connection("switch", "true_output.name", "processor", "name")
workflow.add_connection("switch", "false_output.name", "alt_processor", "name")

# Use skip_branches mode (default for new code)
runtime = LocalRuntime(conditional_execution="skip_branches")
# Only the active branch executes - inactive is skipped intelligently
```

**Why it works**: Runtime detects `None` values and skips nodes automatically.

### ⚠️ route_data Mode
**Avoid dot notation** - connect full output and extract fields in node code:

```python
# Connect full output (no dot notation)
workflow.add_connection("switch", "true_output", "processor", "data")

# Extract field INSIDE node code
workflow.add_node("PythonCodeNode", "processor", {
    "code": """
if data is not None:
    name = data.get('name', 'Unknown')
    result = f'Processing: {name}'
else:
    result = 'No data (inactive branch)'
"""
})

runtime = LocalRuntime(conditional_execution="route_data")
```

**Why avoid**: Accessing `None.field_name` fails navigation. Node receives empty input and raises NameError.


## Common Use Cases

- **Switchnode-Patterns Workflows**: Pre-built patterns for common use cases with best practices built-in
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
- [`sdk-users/2-core-concepts/cheatsheet/020-switchnode-conditional-routing.md`](../../../sdk-users/2-core-concepts/cheatsheet/020-switchnode-conditional-routing.md)

## Quick Tips

- 💡 **Tip 1**: Always follow SwitchNode Conditional Routing best practices
- 💡 **Tip 2**: Test patterns incrementally
- 💡 **Tip 3**: Reference documentation for details

## Keywords for Auto-Trigger

<!-- Trigger Keywords: SwitchNode, conditional routing, if else workflow, route data, conditional logic -->
