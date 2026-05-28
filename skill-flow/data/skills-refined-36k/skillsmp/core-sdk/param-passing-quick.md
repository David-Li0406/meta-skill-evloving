---
name: param-passing-quick
description: "Three methods of parameter passing in Kailash SDK: node configuration, workflow connections, and runtime parameters. Use when asking 'parameter passing', 'pass parameters', 'runtime parameters', 'node config', 'how to pass data', '3 methods', 'parameter methods', 'node parameters', or 'workflow parameters'."
---

# Parameter Passing - Three Methods

Three methods to pass parameters to nodes in Kailash SDK workflows.

> **Skill Metadata**
> Category: `core-sdk`
> Priority: `CRITICAL`
> SDK Version: `0.9.31+`
> Related Skills: [`workflow-quickstart`](workflow-quickstart.md), [`connection-patterns`](connection-patterns.md), [`error-parameter-validation`](../ 15-error-troubleshooting/error-parameter-validation.md)
> Related Subagents: `pattern-expert` (complex parameter patterns)

## Quick Reference

**Three Methods:**
1. **Node Configuration** (Static) - Most reliable ⭐⭐⭐⭐⭐
2. **Workflow Connections** (Dynamic) - Most reliable ⭐⭐⭐⭐⭐
3. **Runtime Parameters** (Override) - Reliable (unwrapped automatically) ⭐⭐⭐⭐⭐

**CRITICAL**: Every required parameter must come from one of these methods or workflow fails at build time.

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

workflow = WorkflowBuilder()

# Method 1: Node Configuration (static values)
workflow.add_node("EmailNode", "send", {
    "to": "user@example.com",
    "subject": "Welcome"
})

# Method 2: Workflow Connection (dynamic from another node)
workflow.add_node("UserLookupNode", "lookup", {"user_id": 123})
workflow.add_connection("lookup", "email", "send", "to")

# Method 3: Runtime Parameter (override at execution)
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build(), parameters={
    "send": {"to": "override@example.com"}
})
```

## Parameter Scoping (v0.9.31+)

**Node-specific parameters are automatically unwrapped:**

```python
# What you pass to runtime:
parameters = {
    "api_key": "global-key",      # Global param (all nodes)
    "node1": {"value": 10},        # Node-specific for node1
    "node2": {"value": 20}         # Node-specific for node2
}

runtime.execute(workflow.build(), parameters=parameters)

# What node1 receives (unwrapped automatically):
{
    "api_key": "global-key",       # Global param
    "value": 10                     # Unwrapped from {"node1": {"value": 10}}
}
# node1 does NOT receive node2's parameters (isolated)
```

**Scoping rules:**
- **Node-specific params**: Nested under node ID → unwrapped automatically
- **Global params**: Top-level (not node IDs) → go to all nodes
- **Parameter isolation**: Each node receives only its params + globals
- **No leakage**: Node1's params never reach Node2

## The Three Methods

### Method 1: Node Configuration (Static)
**Use when**: Values known at design time

```python
workflow.add_node("UserCreateNode", "create", {
    "name": "Alice",
    "email": "alice@example.com",
    "active": True
})
```

**Advantages:**
- Most reliable
- Clear and explicit
- Easy to debug
- Ideal for testing

### Method 2: Workflow Connections (Dynamic)
**Use when**: Values come from other nodes

```python
workflow.add_node("FormDataNode", "form", {})
workflow.add_node("UserCreateNode", "create", {
    "name": "Alice"
    # 'email' comes from connection
})

# 4-parameter syntax: from_node, output_key, to_node, input_key
workflow.add_connection("form", "email_field", "create", "email")
```

**Advantages:**
- Dynamic data flow
- Loose coupling
- Enables pipelines
- Natural for transformations

### Method 3: Runtime Parameters (Override)
**Use when**: Values determined at execution time

```python
workflow.add_node("ReportNode", "generate", {
    "template": "monthly"
    # 'start_date' and 'end_date' from runtime
})

runtime.execute(workflow.build(), parameters={
    "generate": {
        "start_date": "2025-01-01",
        "end_date": "2025-01-31"
    }
})
```

## Common Mistakes

### ❌ Mistake: Missing Required Parameter
```python
workflow.add_node("UserCreateNode", "create", {
    "name": "Alice"
    # ERROR: Missing required 'email'!
})
```

### ✅ Fix: Use One of Three Methods
```python
# Method 1: Add to config
workflow.add_node("UserCreateNode", "create", {
    "name": "Alice",
    "email": "alice@example.com"
})

# OR Method 2: Connect from another node
workflow.add_connection("form", "email", "create", "email")

# OR Method 3: Provide at runtime
runtime.execute(workflow.build(), parameters={
    "create": {"email": "alice@example.com"}
})
```

## Related Patterns

- **For connections**: [`connection-patterns`](connection-patterns.md)
- **For workflow creation**: [`workflow-quickstart`](workflow-quickstart.md)
- **For parameter errors**: [`error-parameter-validation`](../15-error-troubleshooting/error-parameter-validation.md)
- **Gold standard**: [`gold-parameter-passing`](../17-gold-standards/gold-parameter-passing.md)

## When to Escalate to Subagent

Use `pattern-expert` when:
- Complex parameter flow across many nodes
- Custom node parameter validation
- Enterprise parameter governance
- Advanced parameter patterns

## Documentation References

### Primary Sources
- **Parameter Guide**: [`sdk-users/3-development/parameter-passing-guide.md`](../../../sdk-users/3-development/parameter-passing-guide.md)
- **Gold Standard**: [`sdk-users/7-gold-standards/parameter_passing_comprehensive.md`](../../../sdk-users/7-gold-standards/parameter_passing_comprehensive.md)

### Related Documentation
- **Common Mistakes**: [`sdk-users/2-core-concepts/validation/common-mistakes.md`](../../../sdk-users/2-core-concepts/validation/common-mistakes.md)

## Quick Tips

- 💡 **Method 1 for tests**: Most reliable and deterministic
- 💡 **Method 2 for pipelines**: Natural for data flows
- 💡 **Method 3 for user input**: Dynamic values at runtime
- 💡 **Combine methods**: You can use all three together
- 💡 **Parameter scoping**: Automatic unwrapping prevents leakage

## Version Notes

- **v0.9.31+**: Parameter scoping with automatic unwrapping
- **v0.7.0+**: Strict parameter validation enforced (security feature)
- **v0.6.0+**: Three methods established as standard pattern

<!-- Trigger Keywords: parameter passing, pass parameters, runtime parameters, node config, how to pass data, 3 methods, parameter methods, node parameters, workflow parameters, parameter flow, provide parameters, parameter scoping, unwrap parameters -->
