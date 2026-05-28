# ⚠️ CYCLIC WORKFLOWS - PLANNED FEATURE

> **STATUS**: Cyclic workflows are NOT YET IMPLEMENTED in SDK v0.9.31.
>
> This guide documents the planned CycleBuilder API and cyclic patterns.
> **Current alternatives**: Python loops, recursive workflows, SwitchNode state machines.

---

# Cyclic Guide Comprehensive (PLANNED)

Expert guidance for cyclic workflows and loops with Kailash SDK (when implemented).

## Source Documentation
- `/Users/esperie/repos/dev/kailash_python_sdk/sdk-users/3-development/31-cyclic-workflows-guide.md`

## Core Responsibilities (Future)

### 1. Cyclic Workflow Patterns (Planned)
- Simple loops and iterations
- Convergence-based cycles
- Multi-path cyclic patterns
- Error handling in cycles
- Performance optimization

### 2. Simple Cyclic Pattern (CORRECT - Build First)

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

# CORRECT: Build first, then execute
workflow = WorkflowBuilder()

# Initialize counter
workflow.add_node("PythonCodeNode", "init", {
    "code": "result = {'counter': 0, 'max_iterations': 5}"
})

# Process iteration
workflow.add_node("PythonCodeNode", "process", {
    "code": """
counter = data.get('counter', 0) + 1
result = {
    'counter': counter,
    'value': counter * 10,
    'continue': counter < data.get('max_iterations', 5)
}
"""
})

# Check continuation
workflow.add_node("SwitchNode", "check", {
    "cases": [
        {"condition": "continue == True", "target": "process"},
        {"condition": "continue == False", "target": "output"}
    ]
})

workflow.add_node("PythonCodeNode", "output", {
    "code": "result = {'final_counter': counter, 'completed': True}"
})

# Connections (including cycle)
workflow.add_connection("init", "process", "result", "data")
workflow.add_connection("process", "check", "result", "input")
workflow.add_connection("check", "process", "output", "data")  # Cycle back
workflow.add_connection("check", "output", "output", "data")  # Exit path

# CRITICAL: Build first!
workflow_def = workflow.build()

# Then execute
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow_def)

print(f"Final counter: {results['output']['result']['final_counter']}")
```

### 3. Convergence-Based Cycle

```python
workflow = WorkflowBuilder()

# Initialize
workflow.add_node("PythonCodeNode", "init", {
    "code": """
result = {
    'current_value': 100.0,
    'target_value': 50.0,
    'iteration': 0,
    'tolerance': 0.1
}
"""
})

# Iterative refinement
workflow.add_node("PythonCodeNode", "refine", {
    "code": """
import math

current = data.get('current_value')
target = data.get('target_value')
iteration = data.get('iteration', 0) + 1

# Apply refinement step
adjustment = (target - current) * 0.5
new_value = current + adjustment

# Check convergence
difference = abs(new_value - target)
tolerance = data.get('tolerance', 0.1)
converged = difference < tolerance

result = {
    'current_value': new_value,
    'target_value': target,
    'iteration': iteration,
    'difference': difference,
    'tolerance': tolerance,
    'converged': converged
}
"""
})

# Check convergence
workflow.add_node("SwitchNode", "check_convergence", {
    "cases": [
        {"condition": "converged == False", "target": "refine"},
        {"condition": "converged == True", "target": "finalize"}
    ]
})

workflow.add_node("PythonCodeNode", "finalize", {
    "code": """
result = {
    'final_value': current_value,
    'iterations': iteration,
    'converged': True,
    'final_difference': difference
}
"""
})

# Connections
workflow.add_connection("init", "refine", "result", "data")
workflow.add_connection("refine", "check_convergence", "result", "input")
workflow.add_connection("check_convergence", "refine", "output", "data")  # Loop
workflow.add_connection("check_convergence", "finalize", "output", "data")  # Exit

# Execute with build-first pattern
workflow_def = workflow.build()
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow_def)
```

### 4. Multi-Path Cyclic Pattern

```python
workflow = WorkflowBuilder()

# Entry point
workflow.add_node("PythonCodeNode", "input", {
    "code": "result = {'value': input_value, 'iteration': 0}"
})

# Path selector
workflow.add_node("SwitchNode", "router", {
    "cases": [
        {"condition": "value % 2 == 0", "target": "even_processor"},
        {"condition": "value % 2 != 0", "target": "odd_processor"}
    ]
})

# Even path processing
workflow.add_node("PythonCodeNode", "even_processor", {
    "code": """
result = {
    'value': value // 2,
    'iteration': iteration + 1,
    'path': 'even'
}
"""
})

# Odd path processing
workflow.add_node("PythonCodeNode", "odd_processor", {
    "code": """
result = {
    'value': value * 3 + 1,
    'iteration': iteration + 1,
    'path': 'odd'
}
"""
})

# Convergence check
workflow.add_node("SwitchNode", "check_done", {
    "cases": [
        {"condition": "value == 1", "target": "output"},
        {"condition": "value != 1 and iteration < 100", "target": "router"}
    ]
})

workflow.add_node("PythonCodeNode", "output", {
    "code": "result = {'final_iteration': iteration, 'completed': True}"
})

# Connections (both paths cycle back)
workflow.add_connection("input", "router", "result", "input")
workflow.add_connection("router", "even_processor", "output", "input")
workflow.add_connection("router", "odd_processor", "output", "input")
workflow.add_connection("even_processor", "check_done", "result", "input")
workflow.add_connection("odd_processor", "check_done", "result", "input")
workflow.add_connection("check_done", "router", "output", "input")  # Cycle
workflow.add_connection("check_done", "output", "output", "input")  # Exit

# Build and execute
workflow_def = workflow.build()
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow_def, parameters={
    "input": {"input_value": 27}
})
```

### 5. Cyclic Error Handling

```python
workflow = WorkflowBuilder()

# Initialize with retry config
workflow.add_node("PythonCodeNode", "init", {
    "code": """
result = {
    'attempts': 0,
    'max_attempts': 3,
    'success': False,
    'error': None
}
"""
})

# Risky operation
workflow.add_node("PythonCodeNode", "risky_operation", {
    "code": """
import random

attempts = data.get('attempts', 0) + 1

try:
    # Simulate operation that might fail
    if random.random() < 0.7:  # 70% failure rate
        raise Exception("Temporary failure")

    result = {
        'attempts': attempts,
        'success': True,
        'data': 'Operation successful!',
        'error': None
    }

except Exception as e:
    result = {
        'attempts': attempts,
        'success': False,
        'data': None,
        'error': str(e),
        'max_attempts': data.get('max_attempts', 3)
    }
"""
})

# Retry logic
workflow.add_node("SwitchNode", "retry_check", {
    "cases": [
        {"condition": "success == True", "target": "success_handler"},
        {"condition": "success == False and attempts < max_attempts", "target": "risky_operation"},
        {"condition": "success == False and attempts >= max_attempts", "target": "failure_handler"}
    ]
})

workflow.add_node("PythonCodeNode", "success_handler", {
    "code": "result = {'status': 'success', 'attempts': attempts, 'data': data}"
})

workflow.add_node("PythonCodeNode", "failure_handler", {
    "code": "result = {'status': 'failed', 'attempts': attempts, 'error': error}"
})

# Connections
workflow.add_connection("init", "risky_operation", "result", "data")
workflow.add_connection("risky_operation", "retry_check", "result", "input")
workflow.add_connection("retry_check", "risky_operation", "output", "data")  # Retry
workflow.add_connection("retry_check", "success_handler", "output", "input")
workflow.add_connection("retry_check", "failure_handler", "output", "input")

# Execute
workflow_def = workflow.build()
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow_def)
```

### 6. Performance Optimization for Cycles

```python
workflow = WorkflowBuilder()

# Use batch processing in cycles
workflow.add_node("PythonCodeNode", "batch_processor", {
    "code": """
# Process items in batches to reduce overhead
batch = data.get('batch', [])
batch_index = data.get('batch_index', 0)
batch_size = data.get('batch_size', 100)

# Get next batch
start = batch_index * batch_size
end = start + batch_size
current_batch = batch[start:end]

# Process batch
processed = [process_item(item) for item in current_batch]

result = {
    'processed': processed,
    'batch_index': batch_index + 1,
    'batch': batch,
    'batch_size': batch_size,
    'has_more': end < len(batch),
    'total_processed': end
}
"""
})

# Continue if more batches
workflow.add_node("SwitchNode", "check_batches", {
    "cases": [
        {"condition": "has_more == True", "target": "batch_processor"},
        {"condition": "has_more == False", "target": "finalize"}
    ]
})

workflow.add_connection("batch_processor", "check_batches", "result", "input")
workflow.add_connection("check_batches", "batch_processor", "output", "data")
```

### 7. Cyclic with State Accumulation

```python
workflow = WorkflowBuilder()

# Initialize accumulator
workflow.add_node("PythonCodeNode", "init", {
    "code": """
result = {
    'items': [1, 2, 3, 4, 5],
    'current_index': 0,
    'accumulated_sum': 0,
    'accumulated_product': 1
}
"""
})

# Process item and accumulate
workflow.add_node("PythonCodeNode", "accumulate", {
    "code": """
items = data.get('items', [])
index = data.get('current_index', 0)
acc_sum = data.get('accumulated_sum', 0)
acc_product = data.get('accumulated_product', 1)

if index < len(items):
    current_item = items[index]
    acc_sum += current_item
    acc_product *= current_item

result = {
    'items': items,
    'current_index': index + 1,
    'accumulated_sum': acc_sum,
    'accumulated_product': acc_product,
    'done': index + 1 >= len(items)
}
"""
})

# Check if done
workflow.add_node("SwitchNode", "check_done", {
    "cases": [
        {"condition": "done == False", "target": "accumulate"},
        {"condition": "done == True", "target": "output"}
    ]
})

workflow.add_connection("init", "accumulate", "result", "data")
workflow.add_connection("accumulate", "check_done", "result", "input")
workflow.add_connection("check_done", "accumulate", "output", "data")  # Loop
```

## Critical Cyclic Rules

1. **ALWAYS use build-first pattern**: `workflow_def = workflow.build()` then `runtime.execute(workflow_def)`
2. **Define exit condition**: Every cycle must have a way to exit
3. **Prevent infinite loops**: Use max iteration counters
4. **State management**: Pass state through cycle connections
5. **Performance**: Use batch processing for large datasets

## When to Engage
- User asks about "cyclic guide", "loop guide", "comprehensive cycles"
- User needs iterative processing
- User wants convergence-based algorithms
- User has questions about cycle performance

## Integration with Other Skills
- Route to **sdk-fundamentals** for basic concepts
- Route to **workflow-creation-guide** for workflow basics
- Route to **advanced-features** for complex patterns
- Route to **production-deployment-guide** for deployment
