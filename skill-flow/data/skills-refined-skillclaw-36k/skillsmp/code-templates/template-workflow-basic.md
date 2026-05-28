---
name: template-workflow-basic
description: "Generate basic Kailash workflow template boilerplate code. Use when requesting 'workflow template', 'workflow boilerplate', 'scaffold workflow', 'starter code', or 'create new workflow from scratch'."
---

# Basic Workflow Template

Ready-to-use Kailash workflow template with all essential imports, structure, and execution pattern.

> **Skill Metadata**
> Category: `cross-cutting` (code-generation)
> Priority: `CRITICAL`
> SDK Version: `0.9.25+`
> Related Skills: [`workflow-quickstart`](../../01-core-sdk/workflow-quickstart.md), [`connection-patterns`](../../01-core-sdk/connection-patterns.md), [`node-patterns-common`](../../01-core-sdk/node-patterns-common.md)
> Related Subagents: `pattern-expert` (complex workflows), `tdd-implementer` (test-first development)

## Quick Start Template

Copy-paste this template to start any Kailash workflow:

```python
"""
Basic Kailash Workflow Template
Replace placeholders with your specific nodes and logic
"""

from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

def main():
    # 1. Create workflow builder
    workflow = WorkflowBuilder()

    # 2. Add nodes (replace with your nodes)
    workflow.add_node("PythonCodeNode", "step1", {
        "code": "result = {'data': 'value'}"
    })

    workflow.add_node("PythonCodeNode", "step2", {
        "code": "result = {'processed': input_data}"
    })

    # 3. Connect nodes (define data flow)
    workflow.add_connection("step1", "result", "step2", "input_data")

    # 4. Build workflow (CRITICAL)
    built_workflow = workflow.build()

    # 5. Execute
    runtime = LocalRuntime()
    results, run_id = runtime.execute(built_workflow)

    # 6. Access results
    print(f"Run ID: {run_id}")
    print(f"Step2 result: {results['step2']['result']}")  # Access via 'result' key
    return results

if __name__ == "__main__":
    main()
```

## Template Variations

### CLI/Script Template (Sync)
```python
#!/usr/bin/env python3
"""CLI Workflow Template for synchronous execution"""

from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime
import sys

def create_workflow():
    """Create and return built workflow"""
    workflow = WorkflowBuilder()

    # TODO: Add your nodes here
    workflow.add_node("PythonCodeNode", "process", {
        "code": "result = {'status': 'completed'}"
    })

    return workflow.build()

def main():
    workflow = create_workflow()
    runtime = LocalRuntime()

    try:
        results, run_id = runtime.execute(workflow)
        print(f"✓ Success (Run ID: {run_id})")
        print(f"Results: {results}")
        return 0
    except Exception as e:
        print(f"✗ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

### Docker/FastAPI Template (Async)
```python
"""FastAPI Workflow Template for asynchronous execution"""

from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import AsyncLocalRuntime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class WorkflowRequest(BaseModel):
    input_data: dict = {}

def create_workflow():
    """Create and return built workflow"""
    workflow = WorkflowBuilder()

    # TODO: Add your nodes here
    workflow.add_node("PythonCodeNode", "process", {
        "code": "result = {'processed': True}"
    })

    return workflow.build()

@app.post("/execute")
async def execute_workflow(request: WorkflowRequest):
    """Execute workflow with async runtime"""
    workflow = create_workflow()
    runtime = AsyncLocalRuntime()

    try:
        results = await runtime.execute_workflow_async(
            workflow,
            inputs=request.input_data
        )
        return {"status": "success", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run with: uvicorn your_module:app --reload
```

### Data Processing Template
```python
"""Data Processing Workflow Template"""

from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

def create_etl_workflow(input_file: str, output_file: str):
    """Create ETL workflow"""
    workflow = WorkflowBuilder()

    # Extract
    workflow.add_node("CSVReaderNode", "extract", {
        "file_path": input_file,
        "has_header": True
    })

    # Transform
    workflow.add_node("PythonCodeNode", "transform", {
        "code": """
import pandas as pd
df = pd.DataFrame(data)
# TODO: Add your transformation logic
df['processed'] = df['value'] * 2
result = df.to_dict('records')
"""
    })

    # Load
    workflow.add_node("CSVWriterNode", "load", {
        "file_path": output_file,
        "include_header": True
    })

    # Connect pipeline
    workflow.add_connection("extract", "data", "transform", "data")
    workflow.add_connection("transform", "result", "load", "data")

    return workflow.build()

def main():
    workflow = create_etl_workflow("input.csv", "output.csv")
    runtime = LocalRuntime()
    results, run_id = runtime.execute(workflow)
    print(f"Processed {len(results['transform']['result'])} records")

if __name__ == "__main__":
    main()
```

## Template Customization Guide

### Step 1: Choose Your Nodes
Replace placeholders with actual node types based on your needs:

| Need | Node Type | Example Config |
|------|-----------|----------------|
| **Read CSV** | `CSVReaderNode` | `{"file_path": "data.csv"}` |
| **Read JSON** | `JSONReaderNode` | `{"file_path": "data.json"}` |
| **API Call** | `HTTPRequestNode` | `{"url": "https://...", "method": "GET"}` |
| **Database Query** | `AsyncSQLDatabaseNode` | `{"connection_string": "...", "query": "..."}` |
| **LLM Processing** | `LLMAgentNode` | `{"provider": "openai", "model": "gpt-4"}` |
| **Custom Logic** | `PythonCodeNode` | `{"code": "result = {...}"}` |
| **Write CSV** | `CSVWriterNode` | `{"file_path": "output.csv"}` |

### Step 2: Define Data Flow
Connect your nodes using the 4-parameter pattern:

```python
workflow.add_connection(
    "source_node_id",    # from_node
    "output_field",      # from_output
    "target_node_id",    # to_node
    "input_field"        # to_input
)
```

### Step 3: Add Error Handling
```python
try:
    results, run_id = runtime.execute(workflow.build())
except Exception as e:
    print(f"Workflow failed: {e}")
    # Handle error appropriately
```

## Related Patterns

- **Node selection**: [`node-selection-guide`](../../08-nodes-reference/node-selection-guide.md)
- **Connection patterns**: [`connection-patterns`](../../01-core-sdk/connection-patterns.md)
- **Parameter passing**: [`param-passing-quick`](../../01-core-sdk/param-passing-quick.md)
- **Runtime selection**: [`decide-runtime`](../decisions/decide-runtime.md)
- **Complete guide**: [`workflow-quickstart`](../../01-core-sdk/workflow-quickstart.md)

## When to Escalate to Subagent

Use `pattern-expert` subagent when:
- Need custom node development
- Implementing complex cyclic workflows
- Advanced parameter passing patterns
- Performance optimization required

Use `tdd-implementer` subagent when:
- Implementing test-first development
- Need complete test coverage strategy
- Building production-grade workflows

## Documentation References

### Primary Sources
- **Essential Pattern**: [`CLAUDE.md` (lines 106-137)](../../../../CLAUDE.md#L106-L137)
- **Quick Workflow Creation**: [`sdk-users/2-core-concepts/cheatsheet/003-quick-workflow-creation.md`](../../../../sdk-users/2-core-concepts/cheatsheet/003-quick-workflow-creation.md)
- **Workflow Patterns**: [`sdk-users/2-core-concepts/cheatsheet/012-common-workflow-patterns.md`](../../../../sdk-users/2-core-concepts/cheatsheet/012-common-workflow-patterns.md)

### Related Documentation
- **Workflow Creation Guide**: [`sdk-users/3-development/02-workflows-creation.md`](../../../../sdk-users/3-development/02-workflows-creation.md)
- **Workflow Design Process**: [`sdk-users/2-core-concepts/cheatsheet/033-workflow-design-process.md`](../../../../sdk-users/2-core-concepts/cheatsheet/033-workflow-design-process.md)
- **Examples**: [`sdk-users/2-core-concepts/workflows/by-pattern/`](../../../../sdk-users/2-core-concepts/workflows/by-pattern/)

## Quick Tips

- 💡 **Start simple**: Use PythonCodeNode for prototyping before specialized nodes
- 💡 **Build function**: Extract workflow creation into separate function for reusability
- 💡 **Type hints**: Add type hints to improve code maintainability
- 💡 **Docstrings**: Document what your workflow does
- 💡 **Error handling**: Always wrap execution in try-except for production
- 💡 **Logging**: Add logging for debugging and monitoring

<!-- Trigger Keywords: workflow template, workflow boilerplate, scaffold workflow, starter code, create new workflow from scratch, workflow skeleton, basic workflow template, empty workflow, workflow starter, generate workflow code -->
