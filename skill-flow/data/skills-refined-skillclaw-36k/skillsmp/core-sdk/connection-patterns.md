---
name: connection-patterns
description: "Node connection patterns with 4-parameter syntax for data flow mapping. Use when asking 'connect nodes', 'add_connection', 'connection syntax', '4 parameters', 'data flow', 'port mapping', 'fan-out', 'fan-in', 'nested data', 'dot notation', or 'workflow connections'."
---

# Connection Patterns

Essential patterns for connecting workflow nodes using the 4-parameter connection syntax with data flow mapping.

> **Skill Metadata**
> Category: `core-sdk`
> Priority: `CRITICAL`
> SDK Version: `0.9.25+`

## Quick Reference

- **Syntax**: `add_connection(from_node, from_output, to_node, to_input)`
- **CRITICAL**: Always use 4 parameters (source + output → target + input)
- **Dot Notation**: Access nested fields: `"result.metrics.accuracy"`
- **Fan-Out**: One source → multiple targets
- **Fan-In**: Multiple sources → one target

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

workflow = WorkflowBuilder()

# Add nodes
workflow.add_node("CSVReaderNode", "reader", {"file_path": "data.csv"})
workflow.add_node("PythonCodeNode", "processor", {"code": "result = len(data)"})

# ✅ CORRECT: 4-parameter connection
workflow.add_connection("reader", "data", "processor", "data")
#                      ^source  ^output   ^target    ^input

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

## Common Use Cases

- **Linear Pipeline**: Sequential data processing
- **Conditional Routing**: Split data based on conditions
- **Fan-Out**: Broadcast data to multiple processors
- **Fan-In**: Merge data from multiple sources
- **Nested Data Access**: Extract specific fields from complex outputs

## Connection Types

### Type 1: Direct Mapping (Most Common)
```python
workflow = WorkflowBuilder()

workflow.add_node("CSVReaderNode", "reader", {"file_path": "input.csv"})
workflow.add_node("PythonCodeNode", "processor", {"code": "result = len(data)"})
workflow.add_node("JSONWriterNode", "writer", {"file_path": "output.json"})

# Sequential connections
workflow.add_connection("reader", "data", "processor", "data")
workflow.add_connection("processor", "result", "writer", "data")
```

### Type 2: Port Name Mapping
```python
# Different port names - explicit mapping
workflow.add_node("HTTPRequestNode", "api", {"url": "https://api.example.com"})
workflow.add_node("PythonCodeNode", "process", {"code": "result = {'parsed': data}"})

# Map 'response' output to 'data' input
workflow.add_connection("api", "response", "process", "data")
```

### Type 3: Dot Notation for Nested Data
```python
# Extract nested fields from complex outputs
workflow.add_node("PythonCodeNode", "analyzer", {
    "code": """
result = {
    'summary': 'Analysis complete',
    'metrics': {
        'accuracy': 0.95,
        'confidence': 0.87
    },
    'metadata': {
        'timestamp': '2024-01-01',
        'version': '1.0'
    }
}
"""
})

workflow.add_node("PythonCodeNode", "reporter", {
    "code": "result = f'Accuracy: {accuracy}'"
})

# Extract nested field
workflow.add_connection("analyzer", "result.metrics.accuracy", "reporter", "accuracy")
```

### Type 4: Fan-Out (One-to-Many)
```python
# Send same data to multiple processors
workflow.add_node("CSVReaderNode", "reader", {"file_path": "data.csv"})

# Parallel processors
workflow.add_node("PythonCodeNode", "validator", {"code": "result = {'valid': True}"})
workflow.add_node("PythonCodeNode", "logger", {"code": "result = {'logged': True}"})
workflow.add_node("PythonCodeNode", "analyzer", {"code": "result = {'analyzed': True}"})

# Fan-out: reader → multiple targets
workflow.add_connection("reader", "data", "validator", "data")
workflow.add_connection("reader", "data", "logger", "data")
workflow.add_connection("reader", "data", "analyzer", "data")
```

### Type 5: Fan-In with MergeNode
```python
# Combine multiple data sources
workflow.add_node("CSVReaderNode", "source1", {"file_path": "data1.csv"})
workflow.add_node("JSONReaderNode", "source2", {"file_path": "data2.json"})
workflow.add_node("HTTPRequestNode", "source3", {"url": "https://api.example.com"})

workflow.add_node("MergeNode", "merger", {})

# Fan-in: multiple sources → merger
workflow.add_connection("source1", "data", "merger", "input1")
workflow.add_connection("source2", "data", "merger", "input2")
workflow.add_connection("source3", "response", "merger", "input3")

# Process merged data
workflow.add_node("PythonCodeNode", "processor", {"code": "result = {'count': 3}"})
workflow.add_connection("merger", "result", "processor", "data")
```

### Type 6: Multi-Input Processing
```python
# Custom multi-input node
workflow.add_node("CSVReaderNode", "customers", {"file_path": "customers.csv"})
workflow.add_node("CSVReaderNode", "orders", {"file_path": "orders.csv"})

workflow.add_node("PythonCodeNode", "join", {
    "code": """
customers_data = customers if customers else []
orders_data = orders if orders else []

# Join logic
result = {
    'customers': len(customers_data),
    'orders': len(orders_data),
    'combined': customers_data + orders_data
}
"""
})

# Multiple inputs to same node
workflow.add_connection("customers", "data", "join", "customers")
workflow.add_connection("orders", "data", "join", "orders")
```

### Type 7: Complex Nested Extraction
```python
workflow.add_node("LLMAgentNode", "llm", {
    "model": "gpt-4",
    "system_prompt": "Analyze data"
})

workflow.add_node("PythonCodeNode", "metrics_reporter", {
    "code": """
report = {
    'accuracy': accuracy,
    'summary': summary,
    'confidence': confidence
}
result = report
"""
})

# Extract multiple nested fields
workflow.add_connection("llm", "result.metrics.accuracy", "metrics_reporter", "accuracy")
workflow.add_connection("llm", "result.summary", "metrics_reporter", "summary")
workflow.add_connection("llm", "result.confidence", "metrics_reporter", "confidence")
```

## Common Mistakes

### ❌ Mistake 1: Using 3-Parameter Syntax (Deprecated)
```python
# Wrong - Old 3-parameter syntax
workflow.add_connection("reader", "processor", "data")  # DEPRECATED
```

### ✅ Fix: Use 4-Parameter Syntax
```python
# Correct - Modern 4-parameter syntax
workflow.add_connection("reader", "data", "processor", "data")
```

### ❌ Mistake 2: Wrong Port Names
```python
# Wrong - Using non-existent ports
workflow.add_connection("csv_reader", "output", "processor", "input")  # Error
```

### ✅ Fix: Use Correct Port Names
```python
# Correct - CSVReaderNode outputs to 'data' port
workflow.add_connection("csv_reader", "data", "processor", "data")
```

### ❌ Mistake 3: Missing Dot Notation for Nested Data
```python
# Wrong - Trying to pass entire result when you need one field
workflow.add_connection("analyzer", "result", "reporter", "accuracy")  # Gets dict, not number
```

### ✅ Fix: Use Dot Notation
```python
# Correct - Extract specific field
workflow.add_connection("analyzer", "result.accuracy", "reporter", "accuracy")
```

### ❌ Mistake 4: Incorrect Node IDs
```python
# Wrong - Node ID mismatch
workflow.add_node("CSVReaderNode", "csv_reader", {})
workflow.add_connection("reader", "data", "processor", "data")  # Error: 'reader' not found
```

### ✅ Fix: Match Node IDs Exactly
```python
# Correct - Consistent node IDs
workflow.add_node("CSVReaderNode", "csv_reader", {})
workflow.add_connection("csv_reader", "data", "processor", "data")
```

## Related Patterns

- **For workflow creation**: See [`workflow-quickstart`](#)
- **For parameter passing**: See [`param-passing-quick`](#)
- **For node patterns**: See [`node-patterns-common`](#)
- **For cyclic workflows**: See [`cycle-workflows-basics`](#)

## When to Escalate to Subagent

Use `pattern-expert` subagent when:
- Designing complex connection patterns
- Implementing advanced data flow
- Debugging connection issues
- Optimizing workflow architecture

Use `sdk-navigator` subagent when:
- Finding node port names
- Understanding node input/output structure
- Resolving connection errors

## Documentation References

### Primary Sources
- **Connection Patterns**: [`sdk-users/2-core-concepts/cheatsheet/005-connection-patterns.md`](../../../sdk-users/2-core-concepts/cheatsheet/005-connection-patterns.md)
- **Workflow Creation**: [`sdk-users/3-development/02-workflows-creation.md`](../../../sdk-users/3-development/02-workflows-creation.md)

### Related Documentation
- **Common Patterns**: [`sdk-users/2-core-concepts/cheatsheet/012-common-workflow-patterns.md`](../../../sdk-users/2-core-concepts/cheatsheet/012-common-workflow-patterns.md)
- **Advanced Features**: [`sdk-users/3-development/03-advanced-features.md`](../../../sdk-users/3-development/03-advanced-features.md)

### Gold Standards
- **Parameter Passing**: [`sdk-users/7-gold-standards/parameter_passing_comprehensive.md`](../../../sdk-users/7-gold-standards/parameter_passing_comprehensive.md)

## Quick Tips

- 💡 **Always 4 parameters**: Source node + output port → Target node + input port
- 💡 **Check port names**: Verify ports exist on nodes before connecting
- 💡 **Use dot notation**: Access nested data with `"result.field.subfield"`
- 💡 **Plan data flow**: Map out connections before coding
- 💡 **Test incrementally**: Add connections one at a time, verify each works

## Version Notes

- **v0.9.20+**: 4-parameter connection syntax required
- **v0.8.0+**: Dot notation supported for nested field access

## Keywords for Auto-Trigger

<!-- Trigger Keywords: connect nodes, add_connection, connection syntax, 4 parameters, data flow, port mapping, fan-out, fan-in, nested data, dot notation, workflow connections, node connections, data mapping, connection patterns -->
