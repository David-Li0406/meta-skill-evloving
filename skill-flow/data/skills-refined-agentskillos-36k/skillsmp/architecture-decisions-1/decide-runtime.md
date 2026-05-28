---
name: decide-runtime
description: "Choose between LocalRuntime and AsyncLocalRuntime based on deployment context. Use when asking 'which runtime', 'LocalRuntime vs Async', 'runtime choice', 'sync vs async', 'runtime selection', or 'choose runtime'."
---

# Decision: Runtime Selection

Decision: Runtime Selection guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `cross-cutting`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Decision: Runtime Selection
- **Category**: cross-cutting
- **Priority**: HIGH
- **Trigger Keywords**: which runtime, LocalRuntime vs Async, runtime choice, sync vs async, runtime selection

## Decision Matrix

### Use LocalRuntime When:

- CLI applications and scripts
- Synchronous execution contexts
- Testing in pytest (without async fixtures)
- Simple sequential workflows
- Legacy code integration

```python
from kailash.runtime.local import LocalRuntime

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

### Use AsyncLocalRuntime When:

- Docker deployments
- FastAPI applications
- High-concurrency scenarios
- Async execution contexts
- Production APIs (10-100x faster)

```python
from kailash.runtime import AsyncLocalRuntime

runtime = AsyncLocalRuntime()
results = await runtime.execute_workflow_async(workflow.build(), inputs={})
```

### Auto-Detection (Recommended):

```python
from kailash.runtime import get_runtime

# Automatically selects appropriate runtime based on context
runtime = get_runtime()  # Defaults to "async"
runtime = get_runtime("sync")  # Force synchronous
runtime = get_runtime("async")  # Force asynchronous
```


## Comparison Table

| Feature | LocalRuntime | AsyncLocalRuntime |
|---------|--------------|-------------------|
| **Execution Model** | Synchronous | Asynchronous |
| **Best For** | CLI, Scripts, Tests | Docker, FastAPI, APIs |
| **Performance** | Standard | 10-100x faster |
| **Threading** | ThreadPoolExecutor | No threads (async/await) |
| **Return Value** | `(results, run_id)` | `results` |
| **Method** | `execute(workflow.build())` | `await execute_workflow_async(workflow.build(), inputs={})` |
| **Context** | Sync contexts | Async contexts |

## Shared Architecture

Both runtimes inherit from BaseRuntime and use shared mixins, ensuring identical behavior:

**BaseRuntime Foundation**:
- 29 configuration parameters: `debug`, `enable_cycles`, `conditional_execution`, `connection_validation`, `max_iterations`, etc.
- Execution metadata: Run ID generation, workflow caching, metadata management
- Common initialization and validation modes (strict, warn, off)

**Shared Mixins**:
- **CycleExecutionMixin**: Cycle execution delegation to CyclicWorkflowExecutor with validation and error wrapping
- **ValidationMixin**: Workflow structure validation (5 methods)
  - validate_workflow(): Checks workflow structure, node connections, parameter mappings
  - _validate_connection_contracts(): Validates connection parameter contracts
  - _validate_conditional_execution_prerequisites(): Validates conditional execution setup
  - _validate_switch_results(): Validates switch node results
  - _validate_conditional_execution_results(): Validates conditional execution results
- **ConditionalExecutionMixin**: Conditional execution and branching logic with SwitchNode support
  - Pattern detection and cycle detection
  - Node skipping and hierarchical execution
  - Conditional workflow orchestration

**LocalRuntime-Specific Features**:
- _generate_enhanced_validation_error(): Enhanced error messages
- _build_connection_context(): Connection context for errors
- get_validation_metrics(): Public API for validation metrics
- reset_validation_metrics(): Public API for metrics reset

**ParameterHandlingMixin Not Used**:
LocalRuntime uses WorkflowParameterInjector for enterprise parameter handling instead of ParameterHandlingMixin (architectural boundary for complex workflows).

The shared architecture ensures consistent behavior, with the only differences being execution model and async-specific optimizations.

## AsyncLocalRuntime-Specific Features

AsyncLocalRuntime extends LocalRuntime with async-optimized capabilities:

### Automatic Strategy Selection

AsyncLocalRuntime automatically chooses the optimal execution strategy:

**Pure Async Strategy**:
- When: All nodes are AsyncNode subclasses
- Benefit: Maximum concurrency, fastest execution
- Example: Workflows with AsyncPythonCodeNode, async HTTP calls

**Mixed Strategy**:
- When: Combination of sync and async nodes
- Benefit: Balanced performance, wide compatibility
- Example: Most real-world workflows

**Sync-Only Strategy**:
- When: All sync nodes
- Benefit: Compatibility with existing workflows
- Example: Legacy workflows without async nodes

### Level-Based Parallelism

Executes independent nodes concurrently within dependency levels:

```python
# Example workflow structure:
# A (no deps) ─┐
# B (no deps) ─┼─→ D (deps: A, B, C) ─→ F (deps: D, E)
# C (no deps) ─┘                    └─→ E (deps: C)

# Execution:
# Level 0: [A, B, C] → Execute concurrently
# Level 1: [D, E]    → Execute concurrently
# Level 2: [F]       → Execute alone

runtime = AsyncLocalRuntime(max_concurrent_nodes=10)
results = await runtime.execute_workflow_async(workflow.build(), inputs={})
```

### Concurrency Control

```python
runtime = AsyncLocalRuntime(
    max_concurrent_nodes=20,   # Limit concurrent executions
    thread_pool_size=8,        # Threads for sync nodes
    enable_analysis=True,      # Enable WorkflowAnalyzer
    enable_profiling=True      # Track performance metrics
)
```

### Resource Integration

```python
from kailash.resources import ResourceRegistry

registry = ResourceRegistry()
runtime = AsyncLocalRuntime(resource_registry=registry)

# Nodes can access: context.resource_registry.get_resource("db")
```

## Common Patterns

### Pattern 1: CLI Script

```python
# CLI script - use LocalRuntime
from kailash.runtime.local import LocalRuntime

runtime = LocalRuntime(debug=True)
results, run_id = runtime.execute(workflow.build())
print(f"Workflow {run_id} completed: {results}")
```

### Pattern 2: FastAPI Deployment

```python
# FastAPI app - use AsyncLocalRuntime
from fastapi import FastAPI
from kailash.runtime import AsyncLocalRuntime

app = FastAPI()
runtime = AsyncLocalRuntime()

@app.post("/execute")
async def execute_workflow():
    results = await runtime.execute_workflow_async(workflow.build(), inputs={})
    return results
```

### Pattern 3: Testing

```python
# Testing - typically LocalRuntime
import pytest
from kailash.runtime.local import LocalRuntime

def test_workflow():
    runtime = LocalRuntime()
    results, run_id = runtime.execute(workflow.build())
    assert results["node"]["output"] == expected
```

## Migration Between Runtimes

Both runtimes share the same configuration parameters:

```python
# Configuration works identically for both
config = {
    "debug": True,
    "enable_cycles": True,
    "conditional_execution": True,
    "connection_validation": "strict",  # or "warn" or "off"
    "content_aware_success_detection": True
}

# LocalRuntime
sync_runtime = LocalRuntime(**config)

# AsyncLocalRuntime
async_runtime = AsyncLocalRuntime(**config)
```

## Related Patterns

- **For execution options**: See [`runtime-execution`](#)
- **For parameter passing**: See [`gold-parameter-passing`](#)
- **For workflow basics**: See [`workflow-quickstart`](#)

## Documentation References

### Primary Sources
- [`CLAUDE.md#L111-177`](../../../CLAUDE.md)
- [`sdk-users/2-core-concepts/cheatsheet/006-execution-options.md`](../../../sdk-users/2-core-concepts/cheatsheet/006-execution-options.md)

### Internal Architecture
- `src/kailash/runtime/base.py` - Shared BaseRuntime
- `src/kailash/runtime/local.py` - LocalRuntime implementation
- `src/kailash/runtime/async_local.py` - AsyncLocalRuntime implementation

## Quick Tips

- Default to AsyncLocalRuntime for production deployments (faster, Docker-optimized)
- Use LocalRuntime for CLI tools and simple scripts
- Both runtimes share identical configuration and validation logic
- Migration between runtimes only requires changing import and execution method

## Keywords for Auto-Trigger

<!-- Trigger Keywords: which runtime, LocalRuntime vs Async, runtime choice, sync vs async, runtime selection -->
