---
name: workflow-quickstart
description: "Create basic Kailash workflows with WorkflowBuilder. Use when asking 'create workflow', 'workflow template', 'basic workflow', 'how to start', 'workflow setup', 'make workflow', 'build workflow', or 'new workflow'."
---

# Workflow Quick Start

Create basic Kailash workflows using WorkflowBuilder pattern with string-based nodes and 4-parameter connections.

> **Skill Metadata**
> Category: `core-sdk`
> Priority: `CRITICAL`
> SDK Version: `0.9.25+`
> Related Skills: [`connection-patterns`](../connection-patterns.md), [`node-patterns-common`](../node-patterns-common.md), [`runtime-execution`](../runtime-execution.md), [`param-passing-quick`](../param-passing-quick.md)
> Related Subagents: `pattern-expert` (complex workflows), `sdk-navigator` (finding nodes)

## Quick Reference

- **Import**: `from kailash.workflow.builder import WorkflowBuilder`
- **Pattern**: `WorkflowBuilder() → add_node() → add_connection() → build()`
- **Execution**: `runtime.execute(workflow.build())`
- **CRITICAL**: Always call `.build()` before execution
- **Node API**: String-based (e.g., `"CSVReaderNode"`) not instance-based

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# 1. Create workflow builder
workflow = WorkflowBuilder()

# 2. Add nodes (string-based, ALWAYS)
workflow.add_node("CSVReaderNode", "reader", {
    "file_path": "data.csv"
})

workflow.add_node("PythonCodeNode", "processor", {
    "code": "result = {'count': len(data)}"
})

# 3. Connect nodes (4 parameters: from_node, from_output, to_node, to_input)
workflow.add_connection("reader", "data", "processor", "data")

# 4. Build workflow (CRITICAL)
built_workflow = workflow.build()

# 5. Execute
runtime = LocalRuntime()
results, run_id = runtime.execute(built_workflow)

print(results["processor"]["result"]["count"])  # Access via 'result' key
```

## Common Use Cases

- **Data Processing**: Read files, transform data, write results
- **API Integration**: Fetch data from APIs, process, store in database
- **AI Workflows**: LLM agents with pre/post-processing steps
- **ETL Pipelines**: Extract, transform, load data workflows
- **Business Logic**: Multi-step business processes

## Enhanced API Patterns (v0.6.6+)

### Auto ID Generation
```python
workflow = WorkflowBuilder()

# Auto-generate node IDs for rapid prototyping (new feature!)
reader_id = workflow.add_node("CSVReaderNode", {"file_path": "data.csv"})
processor_id = workflow.add_node("PythonCodeNode", {"code": "result = len(input_data)"})

# Use returned IDs for connections
workflow.add_connection(reader_id, "result", processor_id, "input_data")
```

### Flexible API Styles
All these patterns are equivalent and work correctly:

```python
# 1. Current/Preferred Pattern
workflow.add_node("PythonCodeNode", "processor", {"code": "..."})

# 2. Keyword-Only Pattern
workflow.add_node(node_type="PythonCodeNode", node_id="processor", config={"code": "..."})

# 3. Mixed Pattern (common in existing code)
workflow.add_node("PythonCodeNode", node_id="processor", config={"code": "..."})

# 4. Auto ID Pattern (returns generated ID)
processor_id = workflow.add_node("PythonCodeNode", {"code": "..."})
```

## Key Parameters / Options

### add_node(node_type, node_id, config)
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `node_type` | str | Yes | Node class name as string (e.g., "CSVReaderNode") |
| `node_id` | str | Yes* | Unique identifier for this node (*optional with auto-ID) |
| `config` | dict | Yes | Node configuration parameters |

### add_connection(from_node, from_output, to_node, to_input)
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `from_node` | str | Yes | Source node ID |
| `from_output` | str | Yes | Output field name from source |
| `to_node` | str | Yes | Target node ID |
| `to_input` | str | Yes | Input field name on target |

## Common Mistakes

### ❌ Mistake 1: Missing .build() Call
```python
# Wrong - missing .build()
results, run_id = runtime.execute(workflow)  # ERROR!
```

### ✅ Fix: Always Call .build()
```python
# Correct
results, run_id = runtime.execute(workflow.build())  # ✓
```

### ❌ Mistake 2: Wrong Connection Parameters (Only 3)
```python
# Wrong - only 3 parameters (deprecated)
workflow.add_connection("reader", "processor", "data")
```

### ✅ Fix: Use 4 Parameters
```python
# Correct - 4 parameters (source + output → target + input)
workflow.add_connection("reader", "data", "processor", "data")
```

### ❌ Mistake 3: Instance-Based Nodes
```python
# Wrong - instance-based (deprecated)
from kailash.nodes import CSVReaderNode
workflow.add_node("reader", CSVReaderNode(file_path="data.csv"))
```

### ✅ Fix: String-Based Nodes
```python
# Correct - string-based (production pattern)
workflow.add_node("CSVReaderNode", "reader", {"file_path": "data.csv"})
```

### ❌ Mistake 4: Wrong Execution Pattern
```python
# Wrong - workflow doesn't have execute() method
workflow.execute(runtime)  # ERROR!
```

### ✅ Fix: Runtime Executes Workflow
```python
# Correct - runtime executes workflow
runtime.execute(workflow.build())  # ✓
```

## Related Patterns

- **For node connections**: [`connection-patterns`](../connection-patterns.md)
- **For parameter passing**: [`param-passing-quick`](../param-passing-quick.md)
- **For runtime options**: [`runtime-execution`](../runtime-execution.md)
- **For common nodes**: [`node-patterns-common`](../node-patterns-common.md)
- **For cyclic workflows**: [`cycle-workflows-basics`](../../06-cheatsheets/cycle-workflows-basics.md)
- **For code templates**: [`template-workflow-basic`](../../5-cross-cutting/templates/template-workflow-basic.md)

## When to Escalate to Subagent

Use `pattern-expert` subagent when:
- Implementing complex cyclic workflows
- Designing multi-path conditional logic
- Debugging advanced parameter passing issues
- Creating custom nodes from scratch
- Optimizing workflow performance

Use `sdk-navigator` subagent when:
- Need to find specific nodes for your use case
- Looking for workflow examples in specific domains (finance, healthcare, etc.)
- Exploring advanced features and enterprise patterns

## Documentation References

### Primary Sources
- **Cheatsheet**: [`sdk-users/2-core-concepts/cheatsheet/003-quick-workflow-creation.md`](../../../sdk-users/2-core-concepts/cheatsheet/003-quick-workflow-creation.md)
- **Essential Pattern**: [`CLAUDE.md` (lines 106-137)](../../../CLAUDE.md#L106-L137)
- **Workflow Examples**: [`sdk-users/2-core-concepts/workflows/`](../../../sdk-users/2-core-concepts/workflows/)

### Related Documentation
- **Advanced Features**: [`sdk-users/3-development/02-workflows-creation.md`](../../../sdk-users/3-development/02-workflows-creation.md)
- **Common Patterns**: [`sdk-users/2-core-concepts/cheatsheet/012-common-workflow-patterns.md`](../../../sdk-users/2-core-concepts/cheatsheet/012-common-workflow-patterns.md)
- **Workflow Design Process**: [`sdk-users/2-core-concepts/cheatsheet/033-workflow-design-process.md`](../../../sdk-users/2-core-concepts/cheatsheet/033-workflow-design-process.md)

### Gold Standards
- **Parameter Passing**: [`sdk-users/7-gold-standards/parameter_passing_comprehensive.md`](../../../sdk-users/7-gold-standards/parameter_passing_comprehensive.md)

## Examples

### Example 1: Simple CSV Processing
```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

workflow = WorkflowBuilder()

# Read CSV file
workflow.add_node("CSVReaderNode", "read_data", {
    "file_path": "input.csv"
})

# Transform data with PythonCodeNode
workflow.add_node("PythonCodeNode", "transform", {
    "code": """
import pandas as pd
df = pd.DataFrame(data)
df['total'] = df['quantity'] * df['price']
result = df.to_dict('records')
"""
})

# Write results
workflow.add_node("CSVWriterNode", "write_data", {
    "file_path": "output.csv"
})

# Connect the pipeline
workflow.add_connection("read_data", "data", "transform", "data")
workflow.add_connection("transform", "result", "write_data", "data")

# Execute
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
print(f"Processed {len(results['transform']['result']['result'])} records")  # Nested 'result' keys
```

### Example 2: Data Processing ETL
```python
workflow = WorkflowBuilder()

# Extract (simulate data source)
workflow.add_node("PythonCodeNode", "extract", {
    "code": "result = {'data': [{'amount': 150}, {'amount': 50}, {'amount': 200}]}"
})

# Transform (filter and process)
workflow.add_node("PythonCodeNode", "transform", {
    "code": """
data = input_data.get('data', [])
filtered = [item for item in data if item.get('amount', 0) > 100]
transformed = [{'id': i, 'total': item['amount'] * 1.1} for i, item in enumerate(filtered)]
result = transformed
"""
})

# Load (save results)
workflow.add_node("PythonCodeNode", "load", {
    "code": "result = {'saved': len(input_data), 'status': 'complete'}"
})

# Connect the pipeline
workflow.add_connection("extract", "result", "transform", "input_data")
workflow.add_connection("transform", "result", "load", "input_data")

# Execute
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
print(f"Processed {results['load']['result']['saved']} items")
```

### Example 3: API Data Collection
```python
workflow = WorkflowBuilder()

# Fetch from API
workflow.add_node("HTTPRequestNode", "fetch_data", {
    "url": "https://api.example.com/data",
    "method": "GET",
    "headers": {"Authorization": "Bearer TOKEN"}
})

# Process response
workflow.add_node("PythonCodeNode", "extract", {
    "code": """
import json
data = json.loads(response)
result = [item for item in data['items'] if item['active']]
"""
})

# Store in database
workflow.add_node("AsyncSQLDatabaseNode", "store", {
    "connection_string": "postgresql://localhost/db",
    "query": "INSERT INTO data_table (json_data) VALUES (:data)",
    "params": {"data": "${extract.result}"}
})

workflow.add_connection("fetch_data", "response", "extract", "response")
workflow.add_connection("extract", "result", "store", "data")

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `AttributeError: 'WorkflowBuilder' object has no attribute 'execute'` | Calling `.execute()` on workflow instead of runtime | Use `runtime.execute(workflow.build())` - see [`error-missing-build`](../../5-cross-cutti../15-error-troubleshooting/error-missing-build.md) |
| `Node 'X' not found in workflow` | Node ID mismatch in connections | Verify node IDs match exactly between `add_node()` and `add_connection()` |
| `TypeError: add_connection() takes 5 positional arguments but 4 were given` | Using old 3-parameter syntax | Update to 4 parameters: `(from_node, from_output, to_node, to_input)` |
| `ValidationError: Missing required parameter 'X'` | Node config missing required fields | Check node documentation or use `node-patterns-common` for examples |

## Quick Tips

- 💡 **Always build first**: Call `.build()` before `.execute()` - this is the #1 mistake
- 💡 **String-based nodes**: Use `"CSVReaderNode"` (string), not `CSVReaderNode()` (instance)
- 💡 **Unique node IDs**: Each node needs a unique ID within the workflow (or use auto-ID)
- 💡 **4-parameter connections**: Source (node + output) → Target (node + input)
- 💡 **Nested output access**: Use dot notation: `"result.data"` for nested fields
- 💡 **Check examples**: Browse `sdk-users/2-core-concepts/workflows/by-pattern/` for domain-specific examples

## Version Notes

- **v0.9.25+**: AsyncLocalRuntime now default for Docker/FastAPI (no changes to this pattern)
- **v0.9.20+**: String-based nodes became the recommended production pattern
- **v0.6.6+**: Auto ID generation and flexible API patterns added

<!-- Trigger Keywords: create workflow, workflow template, basic workflow, how to start, workflow setup, make workflow, build workflow, new workflow, workflow example, workflow quickstart, WorkflowBuilder, workflow pattern, create kailash workflow, how to create workflow -->
