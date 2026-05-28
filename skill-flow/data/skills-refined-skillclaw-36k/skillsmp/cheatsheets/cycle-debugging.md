---
name: cycle-debugging
description: "Cycle debugging and troubleshooting patterns for fixing common cycle issues. Use when asking 'cycle debugging', 'cycle errors', 'cycle troubleshooting', 'infinite cycles', 'cycle not converging', or 'cycle issues'."
---

# ⚠️ CYCLIC WORKFLOWS - PLANNED FEATURE

> **STATUS**: Cyclic workflows are NOT YET IMPLEMENTED in SDK v0.9.31.
>
> This skill documents the planned CycleBuilder API and debugging patterns.
> Use current alternatives: Python loops, recursive workflows, or SwitchNode state machines.

---

# Cycle Debugging & Troubleshooting (PLANNED)

Quick fixes and debugging patterns for common cycle issues (when implemented).

> **Skill Metadata**
> Category: `core-patterns`
> Priority: `HIGH`
> SDK Version: `Future Release`

## Quick Reference

- **Primary Use**: Debugging cyclic workflows and fixing common issues
- **Category**: core-patterns
- **Priority**: HIGH
- **Trigger Keywords**: cycle debugging, cycle errors, troubleshooting, infinite cycles

## Most Common Issues

### 1. PythonCodeNode Parameter Access (NameError)

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# ❌ Problem: NameError on first iteration
workflow = WorkflowBuilder()
workflow.add_node("PythonCodeNode", "counter", {
    "code": "result = {'count': count + 1}"  # NameError: name 'count' not defined
})

# ✅ Solution: Always use try/except pattern
workflow = WorkflowBuilder()
workflow.add_node("PythonCodeNode", "counter", {
    "code": """
try:
    current_count = input_data.get('count', 0)
except NameError:
    current_count = 0  # Default for first iteration

result = {
    'count': current_count + 1,
    'done': current_count >= 5
}
"""
})
```

### 2. Infinite Cycles (Never Converge)

```python
# ❌ Problem: Convergence condition never satisfied
workflow = WorkflowBuilder()
workflow.add_node("PythonCodeNode", "processor", {
    "code": "result = {'done': False}"  # Never changes
})

built_workflow = workflow.build()
cycle = built_workflow.create_cycle("infinite_cycle")
cycle.connect("processor", "processor", mapping={"result.done": "input_data"}) \
     .max_iterations(10) \
     .converge_when("done == True") \  # Never True!
     .build()

# ✅ Solution: Add debug logging and proper convergence logic
workflow = WorkflowBuilder()
workflow.add_node("PythonCodeNode", "processor", {
    "code": """
count = input_data.get('count', 0) if input_data else 0
count += 1

# Debug: Print convergence field
print(f"Iteration count: {count}")

# Proper convergence logic
done = count >= 5

result = {'count': count, 'done': done}
"""
})

built_workflow = workflow.build()
cycle = built_workflow.create_cycle("fixed_cycle")
cycle.connect("processor", "processor", mapping={"result.count": "input_data"}) \
     .max_iterations(10) \
     .converge_when("done == True") \
     .build()
```

### 3. Wrong Mapping Prefix

```python
# ❌ WRONG: Missing result.* prefix for PythonCodeNode
cycle.connect("python_node", "python_node",
              mapping={"quality": "input_data"})  # Will fail!

# ✅ CORRECT: Use result.* prefix
cycle.connect("python_node", "python_node",
              mapping={"result.quality": "input_data"})
```

### 4. Building After Cycle Creation

```python
# ❌ WRONG: Creating cycle before build
cycle = workflow.create_cycle("my_cycle")  # Will fail!

# ✅ CORRECT: Build first, then create cycle
built_workflow = workflow.build()
cycle = built_workflow.create_cycle("my_cycle")
```

## Debug Techniques

### Add Logging Node

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Add debug logging to track cycle progress
workflow = WorkflowBuilder()
workflow.add_node("PythonCodeNode", "processor", {
    "code": """
count = input_data.get('count', 0) if input_data else 0
count += 1

result = {'count': count, 'done': count >= 3}
"""
})

# Insert logger for debugging
workflow.add_node("PythonCodeNode", "logger", {
    "code": """
print(f"=== Cycle Debug ===")
print(f"Input: {input_data}")
print(f"Count: {input_data.get('count', 0)}")
print(f"Done: {input_data.get('done', False)}")

result = input_data  # Pass through unchanged
"""
})

workflow.add_connection("processor", "result", "logger", "input_data")

# Build and create cycle
built_workflow = workflow.build()
cycle = built_workflow.create_cycle("debug_cycle")
cycle.connect("logger", "processor", mapping={"result.count": "input_data"}) \
     .max_iterations(5) \
     .converge_when("done == True") \
     .build()

runtime = LocalRuntime()
results, run_id = runtime.execute(built_workflow)
```

### Parameter Monitoring

```python
# Monitor which parameters are received in each iteration
workflow.add_node("PythonCodeNode", "monitor", {
    "code": """
# Check received parameters
received = list(input_data.keys()) if input_data else []
print(f"Received parameters: {received}")

# Check for expected parameters
expected = ["data", "quality", "threshold"]
missing = [p for p in expected if p not in (input_data or {})]
if missing:
    print(f"WARNING: Missing parameters: {missing}")

result = input_data if input_data else {}
"""
})
```

## Testing Patterns

### Simple Test Cycle

```python
def test_cycle_execution():
    from kailash.workflow.builder import WorkflowBuilder
    from kailash.runtime.local import LocalRuntime

    workflow = WorkflowBuilder()

    # Simple counter node
    workflow.add_node("PythonCodeNode", "counter", {
        "code": """
try:
    count = input_data.get('count', 0)
except NameError:
    count = 0

result = {
    'count': count + 1,
    'done': count >= 2
}
"""
    })

    # Build before creating cycle
    built_workflow = workflow.build()

    # Create cycle with result.* prefix
    cycle = built_workflow.create_cycle("counter_cycle")
    cycle.connect("counter", "counter", mapping={"result.count": "input_data"}) \
         .max_iterations(5) \
         .converge_when("done == True") \
         .build()

    # Execute and verify
    runtime = LocalRuntime()
    results, run_id = runtime.execute(built_workflow)

    final_result = results.get("counter", {})
    assert final_result.get("result", {}).get("count") == 3
```

### Flexible Test Assertions

```python
def test_cycle_with_ranges():
    # ✅ Test patterns, not exact values
    final_result = results.get("processor", {})
    quality = final_result.get("result", {}).get("quality", 0)

    # Allow variation in iteration count
    iteration = final_result.get("result", {}).get("iteration", 0)
    assert 3 <= iteration <= 7, f"Expected 3-7 iterations, got {iteration}"

    # Check convergence was achieved
    converged = final_result.get("result", {}).get("converged", False)
    assert converged, "Cycle should have converged"

    # ❌ Avoid exact assertions
    # assert quality == 0.85  # Too rigid!
```

## Common Error Patterns

### Error: Missing input_data

```python
# ❌ Problem
result = input_data['field']  # KeyError if input_data is None

# ✅ Solution
result = (input_data or {}).get('field', default_value)
```

### Error: State Not Persisting

```python
# ❌ Problem: Generic mapping loses state
cycle.connect("node", "node", mapping={"output": "input"})

# ✅ Solution: Specific field mapping
cycle.connect("node", "node", mapping={"result.field": "input_data"})
```

### Error: Convergence Never Met

```python
# ❌ Problem: Wrong field type
converge_when("count == '5'")  # String comparison

# ✅ Solution: Correct type
converge_when("count >= 5")  # Numeric comparison
```

## Common Use Cases

- **Fix Infinite Cycles**: Add debug logging, check convergence conditions
- **Debug Parameter Loss**: Use specific field mapping, add parameter monitoring
- **Troubleshoot NameErrors**: Add try/except patterns, check input_data access
- **Test Cycle Logic**: Write flexible tests, use range assertions

## Related Patterns

- **For cycle basics**: See [`cycle-aware-nodes`](#)
- **For testing**: See [`cycle-testing`](#)
- **For state**: See [`cycle-state-persistence`](#)

## When to Escalate to Subagent

Use specialized subagents when:
- **pattern-expert**: Complex cycle patterns, multi-node debugging
- **sdk-navigator**: Persistent errors, unclear error messages
- **testing-specialist**: Comprehensive test strategies

## Documentation References

### Primary Sources
- [`sdk-users/2-core-concepts/cheatsheet/022-cycle-debugging-troubleshooting.md`](../../../sdk-users/2-core-concepts/cheatsheet/022-cycle-debugging-troubleshooting.md)

## Quick Tips

- 💡 **Build First**: Always call workflow.build() before creating cycles
- 💡 **Debug Early**: Add logging nodes to track cycle progress
- 💡 **Test Ranges**: Use range assertions, not exact values
- 💡 **Check Mappings**: Verify result.* prefix for PythonCodeNode

## Keywords for Auto-Trigger

<!-- Trigger Keywords: cycle debugging, cycle errors, cycle troubleshooting, infinite cycles, cycle not converging, cycle issues -->
