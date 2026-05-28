---
name: cycle-testing
description: "Testing patterns for cyclic workflows with flexible assertions. Use when asking 'cycle testing', 'test cycles', 'cyclic workflow tests', 'cycle assertions', or 'test patterns for cycles'."
---

# Cycle Testing Patterns

Essential testing patterns for cyclic workflows with flexible assertions and best practices.

> **Skill Metadata**
> Category: `core-patterns`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Testing cyclic workflows effectively
- **Category**: core-patterns
- **Priority**: HIGH
- **Trigger Keywords**: cycle testing, test cycles, cyclic workflow tests

## Core Testing Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

def test_simple_counter_cycle():
    workflow = WorkflowBuilder()
    workflow.add_node("PythonCodeNode", "counter", {
        "code": """
try:
    count = input_data.get('count', 0)
except NameError:
    count = 0

result = {
    'count': count + 1,
    'done': count >= 3
}
"""
    })

    # Build BEFORE creating cycle
    built_workflow = workflow.build()

    # Create cycle with result.* prefix
    cycle = built_workflow.create_cycle("counter_cycle")
    cycle.connect("counter", "counter", mapping={"result.count": "input_data"}) \
         .max_iterations(5) \
         .converge_when("done == True") \
         .build()

    runtime = LocalRuntime()
    results, run_id = runtime.execute(built_workflow)

    # Test final state
    final_result = results.get("counter", {}).get("result", {})
    assert final_result.get("count") == 4
    assert final_result.get("done") == True
```

## Flexible Test Assertions

```python
# ✅ CORRECT: Test patterns, not exact values
def test_quality_improvement():
    # ... execute workflow ...

    final_quality = results.get("improver", {}).get("result", {}).get("quality", 0)

    # Test for progress, not exact values
    assert final_quality > 0.0, "Quality should improve from zero"
    assert final_quality >= 0.8, "Should reach target quality"

    # Use ranges for iteration count
    iteration = results.get("improver", {}).get("result", {}).get("iteration", 0)
    assert 3 <= iteration <= 10, f"Expected 3-10 iterations, got {iteration}"

    # Verify convergence
    converged = results.get("improver", {}).get("result", {}).get("converged", False)
    assert converged, "Cycle should have converged"

# ❌ WRONG: Too rigid
def test_quality_improvement_rigid():
    assert final_quality == 0.85  # May fail due to floating point!
    assert iteration == 5  # Too specific!
```

## Input_data Pattern

```python
# Always use try/except for input_data access
workflow.add_node("PythonCodeNode", "processor", {
    "code": """
# Handle first iteration when input_data may not exist
try:
    value = input_data.get('value', 0)
    target = input_data.get('target', 0.8)
except NameError:
    # First iteration - use defaults
    value = 0
    target = 0.8

# Process
new_value = min(value + 0.1, 1.0)
converged = new_value >= target

result = {
    'value': new_value,
    'converged': converged
}
"""
})
```

## Common Test Patterns

### Quality Improvement Test
```python
def test_quality_improvement_cycle():
    workflow = WorkflowBuilder()
    workflow.add_node("PythonCodeNode", "improver", {
        "code": """
try:
    quality = input_data.get('quality', 0.0)
    target = input_data.get('target', 0.8)
except NameError:
    quality = 0.0
    target = 0.8

new_quality = min(1.0, quality + 0.1)
converged = new_quality >= target

result = {
    'quality': new_quality,
    'converged': converged,
    'target': target
}
"""
    })

    built_workflow = workflow.build()
    cycle = built_workflow.create_cycle("quality_cycle")
    cycle.connect("improver", "improver", mapping={
        "result.quality": "input_data",
        "result.target": "target"
    }) \
         .max_iterations(10) \
         .converge_when("converged == True") \
         .build()

    runtime = LocalRuntime()
    results, run_id = runtime.execute(built_workflow, parameters={
        "improver": {"quality": 0.0, "target": 0.8}
    })

    # Flexible assertions
    final_result = results.get("improver", {}).get("result", {})
    assert final_result.get("quality", 0) >= 0.8
    assert final_result.get("converged") == True
```

### Conditional Routing Test
```python
def test_conditional_cycle():
    workflow = WorkflowBuilder()
    workflow.add_node("PythonCodeNode", "processor", {
        "code": """
try:
    data = input_data.get('data', [1, 2, 3])
    iteration = input_data.get('iteration', 0)
except NameError:
    data = [1, 2, 3]
    iteration = 0

current_iteration = iteration + 1
processed_sum = sum(data) + current_iteration
should_exit = processed_sum >= 20

result = {
    'data': data,
    'iteration': current_iteration,
    'sum': processed_sum,
    'should_exit': should_exit
}
"""
    })

    workflow.add_node("SwitchNode", "switch", {})
    workflow.add_connection("processor", "result", "switch", "input_data")

    built_workflow = workflow.build()
    cycle = built_workflow.create_cycle("conditional_cycle")
    cycle.connect("switch", "processor", mapping={
        "result.data": "input_data",
        "result.iteration": "iteration"
    }) \
         .max_iterations(10) \
         .converge_when("should_exit == True") \
         .build()

    runtime = LocalRuntime()
    results, run_id = runtime.execute(built_workflow, parameters={
        "processor": {"data": [1, 2, 3]},
        "switch": {"condition_field": "should_exit", "operator": "==", "value": True}
    })

    processor_result = results.get("processor", {}).get("result", {})
    assert processor_result is not None
    assert processor_result.get("should_exit") == True
```

## Testing Principles

### 1. Test Patterns, Not Exact Values
```python
# ✅ Good
assert final_quality > initial_quality  # Progress made
assert 3 <= iteration <= 7  # Reasonable range

# ❌ Bad
assert final_quality == 0.85  # Too rigid
assert iteration == 5  # Too specific
```

### 2. Use input_data with try/except
```python
# ✅ Good: Handle both first iteration and cycles
try:
    value = input_data.get('value', default)
except NameError:
    value = default

# ❌ Bad: Assumes input_data always exists
value = input_data.get('value', default)
```

### 3. Build Before Creating Cycles
```python
# ✅ CORRECT
built_workflow = workflow.build()
cycle = built_workflow.create_cycle("my_cycle")

# ❌ WRONG
cycle = workflow.create_cycle("my_cycle")  # Will fail!
```

### 4. Use result.* Prefix for PythonCodeNode
```python
# ✅ CORRECT
cycle.connect("python_node", "python_node",
              mapping={"result.quality": "input_data"})

# ❌ WRONG
cycle.connect("python_node", "python_node",
              mapping={"quality": "input_data"})
```

## Common Use Cases

- **Quality Improvement**: Test progressive refinement cycles
- **Counter Logic**: Verify iteration counting and limits
- **Conditional Routing**: Test SwitchNode in cycles
- **State Persistence**: Verify state preservation across iterations
- **Convergence**: Test various convergence conditions

## Related Patterns

- **For cycle basics**: See [`cycle-aware-nodes`](#)
- **For debugging**: See [`cycle-debugging`](#)
- **For state**: See [`cycle-state-persistence`](#)

## When to Escalate to Subagent

Use specialized subagents when:
- **testing-specialist**: Comprehensive test strategies, tier-3 tests
- **pattern-expert**: Complex multi-node cycle tests
- **sdk-navigator**: Test failures, unclear errors

## Documentation References

### Primary Sources
- [`sdk-users/2-core-concepts/cheatsheet/027-cycle-aware-testing-patterns.md`](../../../sdk-users/2-core-concepts/cheatsheet/027-cycle-aware-testing-patterns.md)

## Quick Tips

- 💡 **Flexible Assertions**: Use ranges, not exact values
- 💡 **Try/Except**: Always wrap input_data access
- 💡 **Build First**: Call workflow.build() before cycles
- 💡 **Result Prefix**: Use result.* for PythonCodeNode mappings

## Keywords for Auto-Trigger

<!-- Trigger Keywords: cycle testing, test cycles, cyclic workflow tests, cycle assertions, test patterns for cycles -->
