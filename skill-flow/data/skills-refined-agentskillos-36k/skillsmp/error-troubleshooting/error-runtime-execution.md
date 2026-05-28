---
name: error-runtime-execution
description: "Fix runtime execution errors in Kailash workflows. Use when encountering 'execute() failed', 'runtime error', 'workflow execution error', 'LocalRuntime error', or execution-related failures."
---

# Error: Runtime Execution Failures

Fix common runtime execution errors including wrong runtime usage, execution failures, and runtime configuration issues.

> **Skill Metadata**
> Category: `cross-cutting` (error-resolution)
> Priority: `HIGH`
> SDK Version: `0.9.0+`
> Related Skills: [`workflow-quickstart`](../../01-core-sdk/workflow-quickstart.md), [`runtime-execution`](../../01-core-sdk/runtime-execution.md), [`decide-runtime`](../decisions/decide-runtime.md)
> Related Subagents: `pattern-expert` (complex debugging)

## Common Errors

### Wrong Runtime Parameter Name
```python
# ❌ Error
runtime.execute(workflow.build(), config={"node": {"param": "value"}})
runtime.execute(workflow.build(), inputs={"node": {"param": "value"}})
runtime.execute(workflow.build(), overrides={"node": {"param": "value"}})

# ✅ Fix: Use 'parameters'
runtime.execute(workflow.build(), parameters={"node": {"param": "value"}})
```

### Wrong Runtime Selection
```python
# ❌ Error: Using sync runtime in async context (FastAPI)
from kailash.runtime import LocalRuntime

@app.post("/execute")
async def execute_workflow():
    runtime = LocalRuntime()  # ✗ Sync runtime in async function
    results, run_id = runtime.execute(workflow.build())  # Blocks async loop!

# ✅ Fix: Use AsyncLocalRuntime for async contexts
from kailash.runtime import AsyncLocalRuntime

@app.post("/execute")
async def execute_workflow():
    runtime = AsyncLocalRuntime()  # ✓ Async runtime
    results = await runtime.execute_workflow_async(workflow.build(), inputs={})
```

### Missing Return Values
```python
# ❌ Error: Not capturing run_id
results = runtime.execute(workflow.build())  # Missing run_id

# ✅ Fix: Capture both results and run_id
results, run_id = runtime.execute(workflow.build())
```

## Runtime Selection Guide

| Context | Runtime | Method |
|---------|---------|--------|
| **CLI/Scripts** | `LocalRuntime()` | `execute(workflow.build())` |
| **FastAPI/Docker** | `AsyncLocalRuntime()` | `await execute_workflow_async(workflow.build(), inputs={})` |
| **Parallel** | `ParallelRuntime(max_workers=4)` | `execute(workflow.build())` |
| **Auto-detect** | `get_runtime()` | Context-aware |

## Complete Examples

### CLI/Script Pattern
```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

workflow = WorkflowBuilder()
workflow.add_node("PythonCodeNode", "process", {
    "code": "result = {'status': 'completed'}"
})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
print(f"Completed: {run_id}")
```

### FastAPI/Async Pattern
```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import AsyncLocalRuntime
from fastapi import FastAPI

app = FastAPI()

@app.post("/execute")
async def execute():
    workflow = WorkflowBuilder()
    workflow.add_node("PythonCodeNode", "process", {
        "code": "result = {'status': 'completed'}"
    })

    runtime = AsyncLocalRuntime()
    results = await runtime.execute_workflow_async(workflow.build(), inputs={})
    return results
```

## Related Patterns

- **Runtime selection**: [`decide-runtime`](../decisions/decide-runtime.md)
- **Execution guide**: [`runtime-execution`](../../01-core-sdk/runtime-execution.md)
- **Parameter errors**: [`error-parameter-validation`](error-parameter-validation.md)

## When to Escalate to Subagent

Use `pattern-expert` subagent when:
- Complex runtime configuration needed
- Performance optimization required
- Custom runtime development

## Documentation References

### Primary Sources
- **Common Mistakes**: [`sdk-users/2-core-concepts/validation/common-mistakes.md` (lines 134-167)](../../../../sdk-users/2-core-concepts/validation/common-mistakes.md#L134-L167)
- **Runtime Guide**: [`sdk-users/2-core-concepts/cheatsheet/006-execution-options.md`](../../../../sdk-users/2-core-concepts/cheatsheet/006-execution-options.md)
- **CLAUDE.md**: [`CLAUDE.md` (lines 106-137)](../../../../CLAUDE.md#L106-L137)

## Quick Tips

- 💡 **Right parameter name**: Always use `parameters={}` not `inputs` or `config`
- 💡 **Async contexts**: Use AsyncLocalRuntime for FastAPI/Docker
- 💡 **Capture both**: Always get `results, run_id = runtime.execute(...)`

<!-- Trigger Keywords: execute() failed, runtime error, workflow execution error, LocalRuntime error, execution failed, runtime.execute error, execution failure, runtime issue -->
