---
name: error-connection-params
description: "Fix connection parameter errors in Kailash workflows. Use when encountering 'target node not found', 'connection parameter order', 'wrong connection syntax', or '4-parameter connection' errors."
---

# Error: Connection Parameter Issues

Fix connection-related errors including wrong parameter order, missing parameters, and target node not found issues.

> **Skill Metadata**
> Category: `cross-cutting` (error-resolution)
> Priority: `CRITICAL` (Very common error #2)
> SDK Version: `0.9.0+`
> Related Skills: [`workflow-quickstart`](../../01-core-sdk/workflow-quickstart.md), [`connection-patterns`](../../01-core-sdk/connection-patterns.md)
> Related Subagents: `pattern-expert` (complex connection debugging)

## Common Error Messages

```
Node 'result' not found in workflow
Node 'X' not found in workflow
TypeError: add_connection() takes 5 positional arguments but 4 were given
Connection mapping error: output key 'X' not found
```

## Root Causes

1. **Wrong parameter order** - Swapping from_output and to_node
2. **Missing node ID** - Referencing non-existent node
3. **Wrong number of parameters** - Using deprecated 3-parameter syntax
4. **Nested output access** - Missing dot notation for nested fields

## Quick Fixes

### ❌ Error 1: Wrong Parameter Order (VERY COMMON)
```python
# Wrong - parameters swapped (from_output and to_node positions)
workflow.add_connection(
    "prepare_filters",   # from_node ✓
    "execute_search",    # from_output ✗ (should be "result")
    "result",            # to_node ✗ (should be "execute_search")
    "input"              # to_input ✓
)
# Error: "Target node 'result' not found in workflow"
```

### ✅ Fix: Correct Parameter Order
```python
# Correct - proper order: from_node, from_output, to_node, to_input
workflow.add_connection(
    "prepare_filters",   # from_node: source node ID
    "result",            # from_output: output field from source
    "execute_search",    # to_node: target node ID
    "input"              # to_input: input field on target
)
```

**Mnemonic**: **Source first** (node + output), **then Target** (node + input)

### ❌ Error 2: Only 3 Parameters (Deprecated)
```python
# Wrong - old 3-parameter syntax (deprecated in v0.8.0+)
workflow.add_connection("reader", "processor", "data")
```

### ✅ Fix: Use 4 Parameters
```python
# Correct - modern 4-parameter syntax
workflow.add_connection("reader", "data", "processor", "data")
#                       ^source ^output  ^target   ^input
```

### ❌ Error 3: Missing Nested Path
```python
# If node outputs: {'result': {'filters': {...}, 'limit': 50}}

# Wrong - missing nested path
workflow.add_connection(
    "prepare_filters", "filters",  # ✗ 'filters' is nested under 'result'
    "search", "filter"
)
# Error: "Output key 'filters' not found on node 'prepare_filters'"
```

### ✅ Fix: Use Dot Notation
```python
# Correct - full path to nested value
workflow.add_connection(
    "prepare_filters", "result.filters",  # ✓ Full nested path
    "search", "filter"
)

workflow.add_connection(
    "prepare_filters", "result.limit",
    "search", "limit"
)
```

## Complete Example: Before & After

### ❌ Wrong Code (All Common Mistakes)
```python
workflow = WorkflowBuilder()

workflow.add_node("PythonCodeNode", "prep", {
    "code": "result = {'filters': {'status': 'active'}, 'limit': 10}"
})

workflow.add_node("UserListNode", "search", {})

# WRONG: Only 3 parameters
workflow.add_connection("prep", "search", "filters")

# WRONG: Wrong order (swapped output and target)
workflow.add_connection("prep", "search", "filters", "filter")

# WRONG: Missing nested path
workflow.add_connection("prep", "filters", "search", "filter")
```

### ✅ Correct Code
```python
workflow = WorkflowBuilder()

workflow.add_node("PythonCodeNode", "prep", {
    "code": "result = {'filters': {'status': 'active'}, 'limit': 10}"
})

workflow.add_node("UserListNode", "search", {})

# CORRECT: 4 parameters in right order with nested path
workflow.add_connection("prep", "result.filters", "search", "filter")
workflow.add_connection("prep", "result.limit", "search", "limit")
```

## 4-Parameter Connection Pattern

### Parameter Breakdown
```python
workflow.add_connection(
    from_node,    # 1. Source node ID (string)
    from_output,  # 2. Output field name from source (use dot notation for nested)
    to_node,      # 3. Target node ID (string)
    to_input      # 4. Input parameter name on target
)
```

### Common Patterns

| Scenario | from_output | Example |
|----------|-------------|---------|
| **Simple field** | `"data"` | `workflow.add_connection("reader", "data", "processor", "input")` |
| **Nested field** | `"result.data"` | `workflow.add_connection("prep", "result.data", "process", "input")` |
| **Deep nesting** | `"result.user.email"` | `workflow.add_connection("fetch", "result.user.email", "send", "to")` |
| **Array element** | `"result.items[0]"` | Not supported - use PythonCodeNode to extract |

## Debugging Connection Errors

### Step 1: Verify Node IDs Exist
```python
# List all node IDs in your workflow
node_ids = ["prep", "search", "process"]  # Your nodes

# Check connection references match
workflow.add_connection("prep", "result", "search", "input")  # ✓ Both exist
workflow.add_connection("prep", "result", "missing", "input")  # ✗ 'missing' not in workflow
```

### Step 2: Check Output Structure
```python
# Debug by printing node outputs
results, run_id = runtime.execute(workflow.build())

print(f"prep outputs: {results['prep'].keys()}")  # See available keys
# If output is: {'result': {'filters': {}, 'limit': 10}}
# Then use: "result.filters" and "result.limit"
```

### Step 3: Verify Parameter Order
```python
# Remember the order: from_node, from_output, to_node, to_input
#                     ^SOURCE^^  ^SOURCE^^^  ^TARGET^  ^TARGET^
workflow.add_connection(
    "source_node",     # 1. from_node
    "output_field",    # 2. from_output
    "target_node",     # 3. to_node
    "input_param"      # 4. to_input
)
```

## Related Patterns

- **Connection basics**: [`connection-patterns`](../../01-core-sdk/connection-patterns.md)
- **Workflow creation**: [`workflow-quickstart`](../../01-core-sdk/workflow-quickstart.md)
- **Other errors**: [`error-missing-build`](error-missing-build.md), [`error-parameter-validation`](error-parameter-validation.md)
- **Parameter passing**: [`param-passing-quick`](../../01-core-sdk/param-passing-quick.md)

## When to Escalate to Subagent

Use `pattern-expert` subagent when:
- Complex multi-node connection patterns
- Cyclic workflow connection issues
- Advanced parameter mapping
- Connection optimization for performance

## Documentation References

### Primary Sources
- **Pattern Expert**: [`.claude/agents/pattern-expert.md` (lines 294-338)](../../../../.claude/agents/pattern-expert.md#L294-L338)
- **Common Mistakes**: [`sdk-users/2-core-concepts/validation/common-mistakes.md` (lines 200-213)](../../../../sdk-users/2-core-concepts/validation/common-mistakes.md#L200-L213)
- **Connection Cheatsheet**: [`sdk-users/2-core-concepts/cheatsheet/005-connection-patterns.md`](../../../../sdk-users/2-core-concepts/cheatsheet/005-connection-patterns.md)

### Related Documentation
- **Parameter Passing Guide**: [`sdk-users/3-development/parameter-passing-guide.md`](../../../../sdk-users/3-development/parameter-passing-guide.md)
- **Critical Rules**: [`CLAUDE.md` (line 140)](../../../../CLAUDE.md#L140)

## Quick Tips

- 💡 **Mnemonic**: Source (node + output) → Target (node + input)
- 💡 **Debug order**: If "node not found", check if you swapped from_output and to_node
- 💡 **Nested access**: Use dot notation (`result.data`) for nested fields
- 💡 **Verify IDs**: Ensure all referenced node IDs actually exist in workflow
- 💡 **Check output**: Print `results[node].keys()` to see available output fields

## Version Notes

- **v0.9.0+**: 4-parameter syntax became standard
- **v0.8.0+**: 3-parameter syntax deprecated
- **All versions**: Parameter order critical for correct execution

<!-- Trigger Keywords: target node not found, connection error, connection parameter order, wrong connection syntax, 4-parameter connection, add_connection error, connection mapping error, node not found in workflow, connection issues -->
