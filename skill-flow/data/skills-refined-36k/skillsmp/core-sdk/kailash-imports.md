---
name: kailash-imports
description: "Essential import statements for Kailash SDK. Use when asking 'how to import', 'kailash imports', 'from kailash', 'import WorkflowBuilder', 'import LocalRuntime', 'import nodes', 'SDK imports', 'basic imports', 'what to import', or 'import statement'."
---

# Kailash SDK Essential Imports

Essential import statements and patterns for the Kailash SDK covering core components, nodes, and runtime.

> **Skill Metadata**
> Category: `core-sdk`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Core**: `WorkflowBuilder`, `LocalRuntime`, `AsyncLocalRuntime`
- **Nodes**: String-based (no imports needed), or import for type hints
- **Pattern**: Minimal imports for most use cases
- **CRITICAL**: Use absolute imports, never relative imports

## Core Pattern

```python
# Minimal imports for basic workflows
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Create workflow
workflow = WorkflowBuilder()

# Execute workflow
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

## Common Use Cases

- **Basic Workflows**: Import WorkflowBuilder and LocalRuntime
- **Async Workflows**: Import AsyncLocalRuntime for Docker/FastAPI
- **Type Hints**: Import nodes for IDE support (optional)
- **Access Control**: Import security components
- **Custom Nodes**: Import base classes for extensions

## Step-by-Step Guide

### 1. Core Workflow Imports (Required)
```python
# Essential workflow components
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime
```

### 2. Async Runtime (Docker/FastAPI)
```python
# For async contexts (Docker, FastAPI, etc.)
from kailash.runtime.async_local import AsyncLocalRuntime
```

### 3. Node Imports (Optional - Only for Type Hints)
```python
# String-based nodes don't require imports
# But you can import for type hints/IDE support
from kailash.nodes.code import PythonCodeNode
from kailash.nodes.data import CSVReaderNode, CSVWriterNode
from kailash.nodes.logic import SwitchNode, MergeNode
from kailash.nodes.ai import LLMAgentNode
```

### 4. Access Control & Security
```python
# For access-controlled workflows
from kailash.runtime.access_controlled import AccessControlledRuntime
from kailash.access_control import UserContext, PermissionRule
```

### 5. Custom Node Development
```python
# For creating custom nodes
from kailash.nodes.base import Node, NodeParameter
from typing import Dict, Any
```

## Key Import Patterns

| Component | Import | When to Use |
|-----------|--------|-------------|
| **WorkflowBuilder** | `from kailash.workflow.builder import WorkflowBuilder` | Always (core) |
| **LocalRuntime** | `from kailash.runtime.local import LocalRuntime` | Sync workflows |
| **AsyncLocalRuntime** | `from kailash.runtime.async_local import AsyncLocalRuntime` | Docker/FastAPI |
| **Nodes** | String-based (no import) | Production workflows |
| **Node classes** | `from kailash.nodes.<category> import <Node>` | Type hints only |

## Common Mistakes

### ❌ Mistake 1: Importing Node Instances
```python
# Wrong - Don't import nodes for string-based workflows
from kailash.nodes.code import PythonCodeNode
from kailash.nodes.data import CSVReaderNode

# Then using string-based API anyway
workflow.add_node("CSVReaderNode", "reader", {})  # Imports unnecessary
```

### ✅ Fix: Minimal Imports
```python
# Correct - Only import core components
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# String-based nodes don't need imports
workflow.add_node("CSVReaderNode", "reader", {})
workflow.add_node("PythonCodeNode", "processor", {})
```

### ❌ Mistake 2: Wrong Runtime Import
```python
# Wrong - Using wrong runtime module
from kailash.runtime import LocalRuntime  # May not work
```

### ✅ Fix: Correct Module Path
```python
# Correct - Full module path
from kailash.runtime.local import LocalRuntime
from kailash.runtime.async_local import AsyncLocalRuntime
```

### ❌ Mistake 3: Relative Imports in SDK Usage
```python
# Wrong - Relative imports in user code
from .workflow.builder import WorkflowBuilder  # Error
from ..kailash import LocalRuntime  # Error
```

### ✅ Fix: Always Use Absolute Imports
```python
# Correct - Absolute imports only
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime
```

## Examples

### Example 1: Basic Data Processing
```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

workflow = WorkflowBuilder()

workflow.add_node("CSVReaderNode", "reader", {
    "file_path": "data.csv"
})

workflow.add_node("PythonCodeNode", "processor", {
    "code": "result = {'count': len(data)}"
})

workflow.add_connection("reader", "data", "processor", "data")

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

### Example 2: Async Workflow for Docker
```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.async_local import AsyncLocalRuntime

workflow = WorkflowBuilder()

workflow.add_node("HTTPRequestNode", "api_call", {
    "url": "https://api.example.com/data",
    "method": "GET"
})

workflow.add_node("PythonCodeNode", "process", {
    "code": "result = {'status': 'processed'}"
})

workflow.add_connection("api_call", "response", "process", "data")

# Use async runtime for Docker/FastAPI
runtime = AsyncLocalRuntime()
results = await runtime.execute_workflow_async(workflow.build(), inputs={})
```

### Example 3: Type Hints for IDE Support
```python
# Import for type hints and IDE autocomplete
from kailash.nodes.code import PythonCodeNode
from kailash.nodes.data import CSVReaderNode
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

workflow = WorkflowBuilder()

# Using imported classes for type checking (still use string-based API)
workflow.add_node("CSVReaderNode", "reader", {
    "file_path": "data.csv"
})

workflow.add_node("PythonCodeNode", "processor", {
    "code": "result = {'count': len(data) if data else 0}"
})

workflow.add_connection("reader", "data", "processor", "data")

runtime = LocalRuntime()
# Imports help IDE understand node types, but string-based API still used
```

## Related Patterns

- **For installation**: See [`kailash-installation`](#)
- **For workflow creation**: See [`workflow-quickstart`](#)
- **For runtime selection**: See [`decide-runtime`](#)
- **For absolute imports standard**: See [`gold-absolute-imports`](#)

## When to Escalate to Subagent

Use `sdk-navigator` subagent when:
- Finding specific node imports
- Exploring advanced SDK features
- Understanding module structure
- Resolving import errors

Use `pattern-expert` subagent when:
- Designing complex import patterns
- Structuring large projects
- Creating reusable components

## Documentation References

### Primary Sources
- **Basic Imports**: [`sdk-users/2-core-concepts/cheatsheet/002-basic-imports.md`](../../../sdk-users/2-core-concepts/cheatsheet/002-basic-imports.md)
- **Fundamentals**: [`sdk-users/3-development/01-fundamentals-core-concepts.md`](../../../sdk-users/3-development/01-fundamentals-core-concepts.md)

### Related Documentation
- **Node Catalog**: [`sdk-users/2-core-concepts/nodes/comprehensive-node-catalog.md`](../../../sdk-users/2-core-concepts/nodes/comprehensive-node-catalog.md)
- **Custom Nodes**: [`sdk-users/2-core-concepts/cheatsheet/011-custom-node-creation.md`](../../../sdk-users/2-core-concepts/cheatsheet/011-custom-node-creation.md)

### Gold Standards
- **Absolute Imports**: [`sdk-users/7-gold-standards/absolute-imports-gold-standard.md`](../../../sdk-users/7-gold-standards/absolute-imports-gold-standard.md)

## Quick Tips

- 💡 **Minimal imports**: Only import what you need (WorkflowBuilder + Runtime)
- 💡 **String-based nodes**: Don't import nodes for production workflows
- 💡 **Absolute imports**: Always use full module paths
- 💡 **Async runtime**: Import AsyncLocalRuntime for Docker/FastAPI
- 💡 **Type hints**: Import nodes only if you want IDE support

## Version Notes

- **v0.9.25+**: AsyncLocalRuntime recommended for Docker/FastAPI
- **v0.9.20+**: String-based nodes recommended (no imports needed)
- **v0.8.0+**: Absolute imports required for all SDK usage

## Keywords for Auto-Trigger

<!-- Trigger Keywords: how to import, kailash imports, from kailash, import WorkflowBuilder, import LocalRuntime, import nodes, SDK imports, basic imports, what to import, import statement, import pattern, essential imports -->
