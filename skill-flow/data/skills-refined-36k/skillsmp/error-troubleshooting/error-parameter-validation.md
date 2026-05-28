---
name: error-parameter-validation
description: "Fix 'missing required inputs' and parameter validation errors in Kailash workflows. Use when encountering 'Node missing required inputs', 'parameter validation failed', 'required parameter not provided', or parameter-related errors."
---

# Error: Missing Required Parameters

Fix parameter validation errors including missing required inputs, wrong parameter names, and the 3 parameter passing methods.

> **Skill Metadata**
> Category: `cross-cutting` (error-resolution)
> Priority: `CRITICAL` (Common error #3)
> SDK Version: `0.7.0+`
> Related Skills: [`param-passing-quick`](../../01-core-sdk/param-passing-quick.md), [`workflow-quickstart`](../../01-core-sdk/workflow-quickstart.md)
> Related Subagents: `pattern-expert` (complex parameter debugging)

## Common Error Messages

```
Node 'create' missing required inputs: ['email']
ValueError: Missing required parameter 'X'
ValueError: Invalid validation mode 'invalid'
Required parameter 'file_path' not provided
Parameter validation failed for node 'X'
```

## Root Cause

Kailash SDK raises `ValueError` for validation errors including:
- Missing required parameters
- Invalid validation modes
- Parameter type mismatches

Parameters must be provided through one of **3 methods**.

## Quick Fix: The 3 Methods

### Method 1: Node Configuration (Most Reliable)
```python
# ✅ Provide parameters directly in node config
workflow.add_node("UserCreateNode", "create", {
    "name": "Alice",
    "email": "alice@example.com"  # Required parameter provided
})
```

### Method 2: Workflow Connections (Dynamic)
```python
# ✅ Connect parameter from another node's output
workflow.add_connection("form_data", "email", "create", "email")
```

### Method 3: Runtime Parameters (Override)
```python
# ✅ Provide at runtime execution
runtime.execute(workflow.build(), parameters={
    "create": {"email": "alice@example.com"}
})
```

## Complete Example

### ❌ Wrong: Missing Required Parameter
```python
workflow = WorkflowBuilder()

# Missing required 'email' parameter
workflow.add_node("UserCreateNode", "create", {
    "name": "Alice"
    # ERROR: email is required!
})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
# Error: Node 'create' missing required inputs: ['email']
```

### ✅ Fix Option 1: Add to Node Config
```python
workflow = WorkflowBuilder()

workflow.add_node("UserCreateNode", "create", {
    "name": "Alice",
    "email": "alice@example.com"  # Required parameter provided
})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())  # ✓ Works!
```

### ✅ Fix Option 2: Use Connection
```python
workflow = WorkflowBuilder()

# Get email from form data
workflow.add_node("PythonCodeNode", "form", {
    "code": "result = {'email': 'alice@example.com', 'name': 'Alice'}"
})

workflow.add_node("UserCreateNode", "create", {
    "name": "Alice"
    # email will come from connection
})

# Connect email from form to create node
workflow.add_connection("form", "result.email", "create", "email")

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())  # ✓ Works!
```

### ✅ Fix Option 3: Runtime Parameters
```python
workflow = WorkflowBuilder()

workflow.add_node("UserCreateNode", "create", {
    "name": "Alice"
    # email will come from runtime
})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build(), parameters={
    "create": {"email": "alice@example.com"}  # Provided at runtime
})  # ✓ Works!
```

## Parameter Method Selection Guide

| Scenario | Best Method | Why |
|----------|-------------|-----|
| **Static values** | Method 1 (Config) | Clear, explicit, easy to test |
| **Dynamic data flow** | Method 2 (Connections) | Data from previous nodes |
| **User input** | Method 3 (Runtime) | Dynamic values at execution |
| **Environment config** | Method 3 (Runtime) | Different per environment |
| **Testing** | Method 1 (Config) | Most reliable, deterministic |

## Common Variations

### Missing Multiple Parameters
```python
# ❌ Multiple missing parameters
workflow.add_node("HTTPRequestNode", "api", {
    # Missing: url, method
})

# ✅ Provide all required parameters
workflow.add_node("HTTPRequestNode", "api", {
    "url": "https://api.example.com",
    "method": "GET"
})
```

### Optional vs Required Parameters
```python
# Some parameters are optional (have defaults)
workflow.add_node("CSVReaderNode", "reader", {
    "file_path": "data.csv"  # Required
    # has_header: optional (defaults to True)
    # delimiter: optional (defaults to ",")
})
```

## Edge Case Warning

**Method 3 Edge Case** - Fails when ALL conditions met:
```python
# ❌ DANGEROUS combination
workflow.add_node("CustomNode", "node", {})  # 1. Empty config
# + All parameters optional (required=False)  # 2. No required params
# + No connections provide parameters         # 3. No connections
# = Runtime parameters won't be injected!

# ✅ FIX: Provide minimal config
workflow.add_node("CustomNode", "node", {
    "_init": True  # Minimal config prevents edge case
})
```

## Related Patterns

- **3 Methods Guide**: [`param-passing-quick`](../../01-core-sdk/param-passing-quick.md)
- **Connection patterns**: [`connection-patterns`](../../01-core-sdk/connection-patterns.md)
- **Gold standard**: [`gold-parameter-passing`](../../17-gold-standards/gold-parameter-passing.md)

## When to Escalate to Subagent

Use `pattern-expert` subagent when:
- Complex parameter flow across many nodes
- Custom node parameter definition issues
- Advanced parameter validation requirements
- Enterprise parameter governance patterns

## Documentation References

### Primary Sources
- **Common Mistakes**: [`sdk-users/2-core-concepts/validation/common-mistakes.md` (lines 24-51)](../../../../sdk-users/2-core-concepts/validation/common-mistakes.md#L24-L51)
- **Parameter Passing Guide**: [`sdk-users/3-development/parameter-passing-guide.md`](../../../../sdk-users/3-development/parameter-passing-guide.md)
- **Gold Standard**: [`sdk-users/7-gold-standards/parameter_passing_comprehensive.md`](../../../../sdk-users/7-gold-standards/parameter_passing_comprehensive.md)

### Related Documentation
- **Node Parameters**: [`sdk-users/2-core-concepts/nodes/node-parameters.md`](../../../../sdk-users/2-core-concepts/nodes/node-parameters.md)
- **Critical Rules**: [`CLAUDE.md` (lines 139-145)](../../../../CLAUDE.md#L139-L145)

## Quick Tips

- 💡 **Default to Method 1**: Most reliable for static values
- 💡 **Check node docs**: See which parameters are required
- 💡 **Combine methods**: You can use all 3 methods together
- 💡 **Test first**: Use Method 1 in tests for reliability
- 💡 **Avoid edge case**: Never use empty config `{}` with all optional params

## Version Notes

- **v0.7.0+**: Parameter validation improved with better error messages
- **v0.6.0+**: Explicit parameter requirement enforced (security feature)

<!-- Trigger Keywords: missing required inputs, parameter validation, required parameter not provided, parameter error, node missing inputs, validation error, missing parameter, required param, parameter validation failed -->
