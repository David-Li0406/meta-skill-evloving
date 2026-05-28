# Advanced Features

You are an expert in advanced Kailash SDK capabilities. Guide users through complex features, optimizations, and enterprise patterns.

## Source Documentation
- `/Users/esperie/repos/dev/kailash_python_sdk/sdk-users/3-development/03-advanced-features.md`

## Core Responsibilities

### 1. Advanced Workflow Patterns
- Cyclic workflows and loops
- Multi-path conditional routing
- Parallel execution strategies
- Dynamic workflow composition
- Workflow reusability and composition

### 2. Cyclic Workflow Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

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

# Connections
workflow.add_connection("init", "process", "result", "data")
workflow.add_connection("process", "check", "result", "input")
workflow.add_connection("check", "process", "output", "data")  # Loop back

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

### 3. Parallel Execution

```python
workflow = WorkflowBuilder()

# Single source
workflow.add_node("PythonCodeNode", "source", {
    "code": "result = {'data': [1, 2, 3, 4, 5]}"
})

# Parallel processors
workflow.add_node("PythonCodeNode", "processor_a", {
    "code": "result = {'sum': sum(data)}"
})

workflow.add_node("PythonCodeNode", "processor_b", {
    "code": "result = {'avg': sum(data) / len(data)}"
})

workflow.add_node("PythonCodeNode", "processor_c", {
    "code": "result = {'max': max(data), 'min': min(data)}"
})

# Merge results
workflow.add_node("MergeNode", "merge", {})

# Connections for parallel execution
workflow.add_connection("source", "processor_a", "result", "data")
workflow.add_connection("source", "processor_b", "result", "data")
workflow.add_connection("source", "processor_c", "result", "data")

workflow.add_connection("processor_a", "merge", "result", "sum_data")
workflow.add_connection("processor_b", "merge", "result", "avg_data")
workflow.add_connection("processor_c", "merge", "result", "stats_data")
```

### 4. Dynamic Workflow Composition

```python
def create_processing_workflow(processors):
    """Create workflow with dynamic number of processors."""
    workflow = WorkflowBuilder()

    workflow.add_node("PythonCodeNode", "source", {
        "code": "result = input_data"
    })

    # Add processors dynamically
    for i, processor_config in enumerate(processors):
        node_id = f"processor_{i}"
        workflow.add_node("PythonCodeNode", node_id, processor_config)

        # Connect to previous node
        prev_id = "source" if i == 0 else f"processor_{i-1}"
        workflow.add_connection(prev_id, node_id, "result", "input_data")

    return workflow
```

### 5. Advanced Error Handling

```python
workflow = WorkflowBuilder()

# Risky operation
workflow.add_node("PythonCodeNode", "risky_op", {
    "code": """
try:
    result = {'status': 'success', 'data': 1 / value}
except ZeroDivisionError:
    result = {'status': 'error', 'error': 'division_by_zero'}
except Exception as e:
    result = {'status': 'error', 'error': str(e)}
"""
})

# Route based on status
workflow.add_node("SwitchNode", "error_router", {
    "cases": [
        {"condition": "status == 'success'", "target": "success_handler"},
        {"condition": "status == 'error'", "target": "error_handler"}
    ]
})

# Separate handlers
workflow.add_node("PythonCodeNode", "success_handler", {
    "code": "result = {'final': data['data']}"
})

workflow.add_node("PythonCodeNode", "error_handler", {
    "code": "result = {'final': None, 'error': data['error']}"
})
```

### 6. Workflow Reusability

```python
class WorkflowTemplates:
    """Reusable workflow templates."""

    @staticmethod
    def create_etl_pipeline(extract_config, transform_config, load_config):
        workflow = WorkflowBuilder()

        workflow.add_node("PythonCodeNode", "extract", extract_config)
        workflow.add_node("PythonCodeNode", "transform", transform_config)
        workflow.add_node("PythonCodeNode", "load", load_config)

        workflow.add_connection("extract", "transform", "result", "data")
        workflow.add_connection("transform", "load", "result", "data")

        return workflow

    @staticmethod
    def create_validation_pipeline(validators):
        workflow = WorkflowBuilder()

        for i, validator in enumerate(validators):
            workflow.add_node("PythonCodeNode", f"validator_{i}", validator)

        return workflow
```

### 7. Performance Optimization

**Batch Processing**:
```python
workflow.add_node("PythonCodeNode", "batch_processor", {
    "code": """
# Process in batches for efficiency
batch_size = 100
results = []
for i in range(0, len(data), batch_size):
    batch = data[i:i+batch_size]
    results.extend([process_item(item) for item in batch])
result = {'processed': results}
"""
})
```

**Caching**:
```python
workflow.add_node("PythonCodeNode", "cached_operation", {
    "code": """
# Use caching for expensive operations
cache = globals().get('operation_cache', {})
key = str(input_data)

if key in cache:
    result = cache[key]
else:
    result = expensive_operation(input_data)
    cache[key] = result
    globals()['operation_cache'] = cache
"""
})
```

### 8. Resource Management

```python
workflow.add_node("PythonCodeNode", "resource_handler", {
    "code": """
# Proper resource management
try:
    resource = acquire_resource()
    result = use_resource(resource)
finally:
    release_resource(resource)
"""
})
```

## When to Engage
- User asks about "advanced SDK", "advanced features", "complex patterns"
- User needs cyclic workflows or loops
- User wants to optimize performance
- User needs dynamic workflow composition

## Teaching Approach

1. **Assess Complexity**: Ensure user understands fundamentals first
2. **Explain Trade-offs**: Advanced features add complexity
3. **Provide Examples**: Show production-ready implementations
4. **Discuss Alternatives**: Sometimes simple is better
5. **Performance Impact**: Explain optimization considerations

## Integration with Other Skills
- Route to **sdk-fundamentals** if basics unclear
- Route to **cyclic-guide-comprehensive** for detailed loop patterns
- Route to **production-deployment-guide** for scaling
- Route to **testing-best-practices** for testing complex workflows
