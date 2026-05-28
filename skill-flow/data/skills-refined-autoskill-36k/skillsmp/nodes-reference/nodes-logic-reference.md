---
name: nodes-logic-reference
description: "Logic nodes reference (Switch, Merge, Conditional). Use when asking 'Switch node', 'Merge node', 'conditional', 'routing', or 'logic nodes'."
---

# Logic Nodes Reference

Complete reference for control flow and logic nodes.

> **Skill Metadata**
> Category: `nodes`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`
> Related Skills: [`switchnode-patterns`](../../01-core-sdk/switchnode-patterns.md), [`nodes-quick-index`](nodes-quick-index.md)
> Related Subagents: `pattern-expert` (control flow patterns)

## Quick Reference

```python
from kailash.nodes.logic import (
    SwitchNode,
    MergeNode,
    ConditionalRouterNode,
    LoopNode,
    WhileNode
)
```

## Switch Node

### SwitchNode
```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

workflow = WorkflowBuilder()

# Boolean routing (true_output/false_output)
workflow.add_node("SwitchNode", "router", {
    "condition_field": "score",
    "operator": ">=",
    "value": 80
})

# Multi-case routing (case_X outputs)
workflow.add_node("SwitchNode", "status_router", {
    "condition_field": "status",
    "cases": ["active", "inactive", "pending"]
})
```

### ⚠️ Dot Notation Limitation

SwitchNode outputs are **mutually exclusive** (one is always `None`). Dot notation behavior depends on execution mode:

**✅ skip_branches mode** (recommended): Dot notation works - inactive branches skipped
```python
workflow.add_connection("router", "true_output.name", "processor", "name")
runtime = LocalRuntime(conditional_execution="skip_branches")
```

**⚠️ route_data mode**: Avoid dot notation - connect full output
```python
workflow.add_connection("router", "true_output", "processor", "data")
# Extract field in code: name = data.get('name') if data else None
runtime = LocalRuntime(conditional_execution="route_data")
```

## Merge Node

### MergeNode
```python
workflow.add_node("MergeNode", "combine", {
    "strategy": "all",  # or "any", "first"
    "input_sources": ["branch_a", "branch_b", "branch_c"]
})
```

## Conditional Router

### ConditionalRouterNode
```python
workflow.add_node("ConditionalRouterNode", "conditional", {
    "filter": [
        {"condition": "age > 18", "route": "adult_flow"},
        {"condition": "age < 13", "route": "child_flow"},
        {"condition": "True", "route": "default_flow"}  # Default
    ]
})
```

## Loop Nodes

### LoopNode
```python
workflow.add_node("LoopNode", "loop", {
    "iterations": 5,
    "body": "process_item"
})
```

### WhileNode
```python
workflow.add_node("WhileNode", "while_loop", {
    "condition": "count < 100",
    "body": "increment_counter"
})
```

## Related Skills

- **SwitchNode Patterns**: [`switchnode-patterns`](../../01-core-sdk/switchnode-patterns.md)
- **Node Index**: [`nodes-quick-index`](nodes-quick-index.md)

## Documentation

- **Logic Nodes**: [`sdk-users/2-core-concepts/nodes/05-logic-nodes.md`](../../../../sdk-users/2-core-concepts/nodes/05-logic-nodes.md)

<!-- Trigger Keywords: Switch node, Merge node, conditional, routing, logic nodes, SwitchNode, MergeNode, ConditionalRouterNode -->
