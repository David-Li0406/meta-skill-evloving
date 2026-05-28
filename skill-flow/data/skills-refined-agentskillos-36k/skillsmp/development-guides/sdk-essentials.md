# SDK Essentials

You are an expert in Kailash SDK essentials - the quick reference for essential patterns and workflows.

## Source Documentation
- `/Users/esperie/repos/dev/kailash_python_sdk/sdk-users/2-core-concepts/workflows/quick-start/sdk-essentials.md`
- `/Users/esperie/repos/dev/kailash_python_sdk/sdk-users/2-core-concepts/workflows/quick-start/30-second-workflows.md`

## Core Responsibilities

### 1. Essential Pattern (Copy-Paste Ready)
```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

# 1. Create workflow
workflow = WorkflowBuilder()

# 2. Add nodes
workflow.add_node("PythonCodeNode", "processor", {
    "code": "result = {'status': 'processed', 'data': input_data}"
})

# 3. Add connections (4-parameter syntax)
workflow.add_connection("source", "output", "processor", "input_data")

# 4. Execute - ALWAYS call .build()
runtime = LocalRuntime()  # For CLI/scripts
results, run_id = runtime.execute(workflow.build())

# For Docker/FastAPI (async)
# from kailash.runtime import AsyncLocalRuntime
# runtime = AsyncLocalRuntime()
# results = await runtime.execute_workflow_async(workflow.build(), inputs={})
```

### 2. Quick Data Processing
```python
workflow = WorkflowBuilder()

# Read CSV
workflow.add_node("CSVReaderNode", "reader", {
    "file_path": "data.csv"
})

# Process
workflow.add_node("PythonCodeNode", "process", {
    "code": """
import pandas as pd
df = pd.DataFrame(data)
result = {'count': len(df), 'summary': df.describe().to_dict()}
"""
})

# Write output
workflow.add_node("CSVWriterNode", "writer", {
    "file_path": "output.csv"
})

# Connect (4-parameter syntax: from_node, output_key, to_node, input_key)
workflow.add_connection("reader", "data", "process", "data")
workflow.add_connection("process", "result", "writer", "data")
```

### 3. Quick API Integration
```python
workflow = WorkflowBuilder()

workflow.add_node("HTTPRequestNode", "api_call", {
    "url": "https://api.example.com/data",
    "method": "GET"
})

workflow.add_node("PythonCodeNode", "transform", {
    "code": "result = {'data': response.get('data'), 'count': len(response.get('data', []))}"
})

workflow.add_connection("api_call", "response", "transform", "response")
```

### 4. Quick AI Integration
```python
workflow = WorkflowBuilder()

workflow.add_node("LLMAgentNode", "ai", {
    "provider": "ollama",
    "model": "llama3.2",
    "messages": [{"role": "user", "content": "Summarize this data"}]
})

workflow.add_node("PythonCodeNode", "format", {
    "code": "result = {'summary': response}"
})

workflow.add_connection("ai", "response", "format", "response")
```

### 5. Essential Runtime Patterns
```python
# For CLI/Scripts (sync)
from kailash.runtime import LocalRuntime
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())

# For Docker/FastAPI (async)
from kailash.runtime import AsyncLocalRuntime
runtime = AsyncLocalRuntime()
results = await runtime.execute_workflow_async(workflow.build(), inputs={})

# Auto-detection
from kailash.runtime import get_runtime
runtime = get_runtime()  # Defaults to async
```

### 6. Essential Error Handling
```python
workflow.add_node("PythonCodeNode", "safe_operation", {
    "code": """
try:
    result = risky_operation(input_data)
except Exception as e:
    result = {'error': str(e), 'success': False}
"""
})
```

### 7. Essential Parameter Patterns
```python
# Static parameters
workflow.add_node("HTTPRequestNode", "api", {
    "url": "https://api.example.com"
})

# Dynamic parameters
runtime.execute(workflow.build(), parameters={
    "api": {"url": "https://different-api.com"}
})

# Environment variables
workflow.add_node("HTTPRequestNode", "api", {
    "url": "${API_URL}",
    "headers": {"Authorization": "Bearer ${API_TOKEN}"}
})
```

### 8. Essential Connection Pattern
```python
# Connect nodes: source → target (4-parameter syntax)
workflow.add_connection(
    "source_node_id",    # From this node
    "output_key",        # This output key
    "target_node_id",    # To this node
    "input_key"          # Maps to this input key
)
```

## When to Engage
- User asks about "SDK essentials", "essential patterns", "SDK quick reference"
- User needs quick patterns
- User wants copy-paste solutions
- User needs rapid prototyping

## Integration with Other Skills
- Route to **sdk-fundamentals** for detailed concepts
- Route to **workflow-creation-guide** for complete workflow building
- Route to **production-deployment-guide** for deployment
