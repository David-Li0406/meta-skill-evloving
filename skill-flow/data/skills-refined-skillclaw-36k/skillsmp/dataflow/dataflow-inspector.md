---
name: dataflow-inspector
description: "Inspector API for DataFlow workflow introspection, debugging, and validation. Use when debugging workflows, tracing parameters, analyzing connections, finding broken links, validating structure, or need workflow analysis."
---

# DataFlow Inspector - Workflow Introspection API

Self-service debugging API for workflows, nodes, connections, and parameters with 18 inspection methods.

> **Skill Metadata**
> Category: `dataflow/dx`
> Priority: `CRITICAL`
> SDK Version: `0.8.0+ / DataFlow 0.8.0`
> Related Skills: [`dataflow-error-enhancer`](#), [`dataflow-validation`](#), [`dataflow-debugging`](#)
> Related Subagents: `dataflow-specialist` (complex workflows), `testing-specialist` (test workflows)

## Quick Reference

- **18 Inspector Methods**: Connection, parameter, node, and workflow analysis
- **<1ms Per Method**: Cached operations for fast introspection
- **Automatic Validation**: Built-in workflow structure checks
- **CLI Integration**: Works with `dataflow-validate`, `dataflow-debug`
- **Zero Configuration**: Works with any DataFlow workflow

## Basic Usage

```python
from dataflow import DataFlow
from dataflow.platform.inspector import Inspector
from kailash.workflow.builder import WorkflowBuilder

db = DataFlow("postgresql://localhost/mydb")

@db.model
class User:
    id: str
    name: str
    email: str

# Build workflow
workflow = WorkflowBuilder()
workflow.add_node("UserCreateNode", "create", {
    "data": {"name": "Alice", "email": "alice@example.com"}
})

# Create inspector
inspector = Inspector(db)
inspector.workflow_obj = workflow.build()

# Analyze workflow
connections = inspector.connections()  # List all connections
order = inspector.execution_order()    # Topological sort
summary = inspector.workflow_summary() # High-level overview
```

## Inspector Methods (18 Total)

### Connection Analysis (5 methods)

#### 1. connections() - List All Connections
```python
connections = inspector.connections()
# Returns: [
#     {
#         'source': 'prepare_data',
#         'source_output': 'result',
#         'target': 'create_user',
#         'target_input': 'data'
#     },
#     ...
# ]
```

#### 2. validate_connections() - Check Connection Validity
```python
result = inspector.validate_connections()
# Returns: {
#     'is_valid': True/False,
#     'errors': [...],
#     'warnings': [...]
# }
```

#### 3. find_broken_connections() - Find Issues
```python
broken = inspector.find_broken_connections()
# Returns: [
#     {
#         'connection': {...},
#         'reason': 'Source output not found'
#     },
#     ...
# ]
```

#### 4. connection_chain() - Trace Connection Path
```python
chain = inspector.connection_chain("prepare_data", "create_user")
# Returns: [
#     ('prepare_data', 'result'),
#     ('create_user', 'data')
# ]
```

#### 5. connection_graph() - Build Connection Graph
```python
graph = inspector.connection_graph()
# Returns: NetworkX-compatible graph structure
```

### Parameter Tracing (5 methods)

#### 1. trace_parameter() - Find Parameter Source
```python
trace = inspector.trace_parameter("create_user", "data")
# Returns: {
#     'node': 'create_user',
#     'parameter': 'data',
#     'source_node': 'prepare_data',
#     'source_output': 'result',
#     'value_type': 'dict'
# }
```

#### 2. parameter_flow() - Trace Complete Flow
```python
flow = inspector.parameter_flow("initial_input", "final_output")
# Returns: [
#     ('initial_input', 'data'),
#     ('transform_1', 'input'),
#     ('transform_2', 'input'),
#     ('final_output', 'data')
# ]
```

#### 3. find_parameter_source() - Locate Source Node
```python
source = inspector.find_parameter_source("create_user", "data")
# Returns: {
#     'node': 'prepare_data',
#     'output': 'result'
# }
```

#### 4. parameter_dependencies() - Find All Dependencies
```python
deps = inspector.parameter_dependencies("create_user")
# Returns: {
#     'data': {
#         'source_node': 'prepare_data',
#         'source_output': 'result'
#     },
#     ...
# }
```

#### 5. parameter_consumers() - Find All Consumers
```python
consumers = inspector.parameter_consumers("prepare_data", "result")
# Returns: [
#     {'node': 'create_user', 'parameter': 'data'},
#     {'node': 'validate_data', 'parameter': 'input'},
#     ...
# ]
```

### Node Analysis (5 methods)

#### 1. node_dependencies() - Upstream Dependencies
```python
deps = inspector.node_dependencies("create_user")
# Returns: ['prepare_data', 'validate_input']
```

#### 2. node_dependents() - Downstream Dependents
```python
dependents = inspector.node_dependents("create_user")
# Returns: ['send_email', 'log_creation']
```

#### 3. execution_order() - Topological Sort
```python
order = inspector.execution_order()
# Returns: [
#     'input',
#     'validate',
#     'prepare_data',
#     'create_user',
#     'send_email'
# ]
```

#### 4. node_schema() - Get Node Schema
```python
schema = inspector.node_schema("create_user")
# Returns: {
#     'inputs': {'data': 'dict'},
#     'outputs': {'result': 'dict'},
#     'node_type': 'UserCreateNode'
# }
```

#### 5. compare_nodes() - Compare Two Nodes
```python
diff = inspector.compare_nodes("create_user", "create_product")
# Returns: {
#     'common_inputs': ['data'],
#     'unique_inputs_1': [],
#     'unique_inputs_2': [],
#     'schema_differences': [...]
# }
```

### Workflow Analysis (3 methods)

#### 1. workflow_summary() - High-Level Overview
```python
summary = inspector.workflow_summary()
# Returns: {
#     'total_nodes': 5,
#     'total_connections': 4,
#     'entry_nodes': ['input'],
#     'exit_nodes': ['send_email'],
#     'longest_path': 4,
#     'cyclic': False
# }
```

#### 2. workflow_metrics() - Detailed Metrics
```python
metrics = inspector.workflow_metrics()
# Returns: {
#     'complexity': 'medium',
#     'branching_factor': 1.8,
#     'avg_dependencies': 2.3,
#     'max_fan_out': 3,
#     'critical_path_length': 5
# }
```

#### 3. workflow_validation_report() - Comprehensive Validation
```python
report = inspector.workflow_validation_report()
# Returns: {
#     'is_valid': True/False,
#     'errors': [...],      # Structural errors
#     'warnings': [...],    # Best practice violations
#     'suggestions': [...]  # Optimization opportunities
# }
```

## Common Use Cases

### 1. Diagnose "Missing Parameter" Errors

```python
# Problem: DF-101 Missing required parameter 'data'

inspector = Inspector(db)
inspector.workflow_obj = workflow.build()

# Find parameter source
trace = inspector.trace_parameter("create_user", "data")
if trace is None:
    print("❌ Parameter 'data' has no source!")
    # Check if it should come from another node
    deps = inspector.parameter_dependencies("create_user")
    print(f"Current dependencies: {deps}")
else:
    print(f"✅ Parameter 'data' comes from: {trace['source_node']}")
```

### 2. Find Broken Connections

```python
# Find all broken connections in workflow
broken = inspector.find_broken_connections()

if broken:
    print(f"🔴 Found {len(broken)} broken connections:")
    for item in broken:
        conn = item['connection']
        reason = item['reason']
        print(f"  - {conn['source']}.{conn['source_output']} → {conn['target']}.{conn['target_input']}")
        print(f"    Reason: {reason}")
else:
    print("✅ All connections are valid!")
```

### 3. Trace Parameter Flow Through Workflow

```python
# Trace how data flows from input to output
flow = inspector.parameter_flow("input", "final_output")

print("Parameter flow:")
for node, param in flow:
    schema = inspector.node_schema(node)
    print(f"  {node}.{param} ({schema['node_type']})")
```

### 4. Validate Workflow Before Execution

```python
# Comprehensive validation before runtime.execute()
report = inspector.workflow_validation_report()

if not report['is_valid']:
    print("🔴 Workflow validation failed!")
    print(f"\nErrors ({len(report['errors'])}):")
    for error in report['errors']:
        print(f"  - {error}")

    print(f"\nWarnings ({len(report['warnings'])}):")
    for warning in report['warnings']:
        print(f"  - {warning}")

    print(f"\nSuggestions ({len(report['suggestions'])}):")
    for suggestion in report['suggestions']:
        print(f"  - {suggestion}")
else:
    print("✅ Workflow is valid!")
    # Safe to execute
    results, run_id = runtime.execute(workflow.build())
```

### 5. Generate Workflow Documentation

```python
# Auto-generate workflow documentation
summary = inspector.workflow_summary()
metrics = inspector.workflow_metrics()
order = inspector.execution_order()

print(f"# Workflow Documentation")
print(f"\n## Overview")
print(f"- Total Nodes: {summary['total_nodes']}")
print(f"- Total Connections: {summary['total_connections']}")
print(f"- Complexity: {metrics['complexity']}")
print(f"- Cyclic: {summary['cyclic']}")

print(f"\n## Execution Order")
for i, node in enumerate(order, 1):
    deps = inspector.node_dependencies(node)
    print(f"{i}. {node}")
    if deps:
        print(f"   Depends on: {', '.join(deps)}")
```

### 6. Debug Complex Workflows

```python
# Interactive debugging session
inspector = Inspector(db)
inspector.workflow_obj = workflow.build()

# 1. Check execution order
order = inspector.execution_order()
print(f"Execution order: {' → '.join(order)}")

# 2. Inspect specific node
node_id = "create_user"
schema = inspector.node_schema(node_id)
deps = inspector.node_dependencies(node_id)
dependents = inspector.node_dependents(node_id)

print(f"\nNode: {node_id}")
print(f"  Type: {schema['node_type']}")
print(f"  Inputs: {schema['inputs']}")
print(f"  Outputs: {schema['outputs']}")
print(f"  Depends on: {deps}")
print(f"  Used by: {dependents}")

# 3. Trace specific parameter
param_trace = inspector.trace_parameter(node_id, "data")
print(f"\nParameter 'data':")
print(f"  Source: {param_trace['source_node']}.{param_trace['source_output']}")
```

## Combining Inspector with ErrorEnhancer

Inspector provides **proactive validation** before errors occur, while ErrorEnhancer provides **reactive solutions** when errors happen:

```python
from dataflow import DataFlow
from dataflow.platform.inspector import Inspector

db = DataFlow("postgresql://localhost/mydb")

@db.model
class User:
    id: str
    name: str
    email: str

# Build workflow
workflow = WorkflowBuilder()
workflow.add_node("UserCreateNode", "create", {})  # ← Missing 'data'

# STEP 1: Proactive validation with Inspector
inspector = Inspector(db)
inspector.workflow_obj = workflow.build()
report = inspector.workflow_validation_report()

if not report['is_valid']:
    print("🔴 Inspector found issues:")
    for error in report['errors']:
        print(f"  - {error}")

    # Fix issues before execution
    workflow.add_node("UserCreateNode", "create", {
        "data": {"name": "Alice", "email": "alice@example.com"}
    })

# STEP 2: Execute workflow
try:
    results, run_id = runtime.execute(workflow.build())
except Exception as e:
    # ErrorEnhancer provides detailed solutions if execution fails
    print(e)  # Shows DF-101 with code templates
```

## CLI Integration

Inspector powers CLI validation and debugging tools:

```bash
# Validate workflow structure
dataflow-validate workflow.py --output text
# Uses Inspector.workflow_validation_report()

# Analyze workflow metrics
dataflow-analyze workflow.py --verbosity 2
# Uses Inspector.workflow_metrics()

# Debug workflow with breakpoints
dataflow-debug workflow.py --inspect-node create_user
# Uses Inspector.node_schema(), Inspector.parameter_dependencies()

# Generate workflow documentation
dataflow-generate workflow.py docs --output-dir ./docs
# Uses Inspector.workflow_summary(), Inspector.execution_order()
```

## Performance

Inspector operations are **highly optimized**:

| Operation | Complexity | Typical Time |
|-----------|-----------|--------------|
| connections() | O(n) | <1ms |
| execution_order() | O(n + e) | <2ms |
| node_dependencies() | O(d) | <1ms |
| trace_parameter() | O(d) | <1ms |
| workflow_summary() | O(n + e) | <2ms |
| workflow_validation_report() | O(n + e) | <5ms |

Where:
- n = number of nodes
- e = number of connections
- d = depth of dependency chain

**Caching**: Results are cached per workflow instance for instant subsequent calls.

## Best Practices

### 1. Validate Before Execution
Always validate workflows before runtime.execute():
```python
# ✅ CORRECT - Validate first
inspector = Inspector(db)
inspector.workflow_obj = workflow.build()
report = inspector.workflow_validation_report()

if report['is_valid']:
    results, run_id = runtime.execute(workflow.build())
else:
    print(f"Fix {len(report['errors'])} errors first")

# ❌ WRONG - Execute without validation
results, run_id = runtime.execute(workflow.build())  # May fail
```

### 2. Use Inspector for Debugging
When encountering errors, use Inspector to understand the workflow:
```python
# ❌ WRONG - Guess what went wrong
print("Something broke, let me guess...")

# ✅ CORRECT - Use Inspector to analyze
inspector = Inspector(db)
inspector.workflow_obj = workflow.build()

# Check execution order
order = inspector.execution_order()
print(f"Execution: {' → '.join(order)}")

# Check specific node
node_id = "problematic_node"
deps = inspector.node_dependencies(node_id)
param_deps = inspector.parameter_dependencies(node_id)
print(f"Dependencies: {deps}")
print(f"Parameter sources: {param_deps}")
```

### 3. Generate Documentation Automatically
Use Inspector to document complex workflows:
```python
# ✅ CORRECT - Auto-generate docs
def document_workflow(workflow, db):
    inspector = Inspector(db)
    inspector.workflow_obj = workflow.build()

    summary = inspector.workflow_summary()
    metrics = inspector.workflow_metrics()
    order = inspector.execution_order()

    # Generate markdown documentation
    doc = f"# Workflow\n\n"
    doc += f"- Nodes: {summary['total_nodes']}\n"
    doc += f"- Complexity: {metrics['complexity']}\n"
    doc += f"- Execution: {' → '.join(order)}\n"

    return doc
```

### 4. CI/CD Integration
Validate workflows in CI pipelines:
```bash
# In CI/CD pipeline (e.g., GitHub Actions)
- name: Validate DataFlow workflows
  run: |
    dataflow-validate src/workflows/*.py --output json > report.json
    # Fail build if validation errors found
    python -c "import json; report = json.load(open('report.json')); exit(1 if not report['is_valid'] else 0)"
```

### 5. Combine with ErrorEnhancer
Use Inspector (proactive) + ErrorEnhancer (reactive):
```python
# Proactive validation
inspector = Inspector(db)
report = inspector.workflow_validation_report()

if not report['is_valid']:
    # Fix validation errors first
    fix_errors(report['errors'])

try:
    # Execute with confidence
    results, run_id = runtime.execute(workflow.build())
except Exception as e:
    # ErrorEnhancer provides detailed solutions
    print(e)  # Shows DF-XXX code with fixes
```

## Version Compatibility

- **DataFlow 0.8.0+**: Full Inspector API with 18 methods
- **DataFlow 0.7.x and earlier**: No Inspector API

**Upgrade Command:**
```bash
pip install --upgrade kailash-dataflow>=0.8.0
```

## Related Resources

- **[dataflow-error-enhancer](dataflow-error-enhancer.md)** - Actionable error messages with DF-XXX codes
- **[dataflow-validation](dataflow-validation.md)** - Build-time validation modes
- **[dataflow-debugging](dataflow-debugging.md)** - Interactive debugging with CLI tools
- **[inspector.md](../../../sdk-users/apps/dataflow/guides/inspector.md)** - Comprehensive Inspector guide

## When to Use This Skill

Use Inspector when you:
- Debug complex DataFlow workflows
- Validate workflows before execution
- Trace parameter flow through workflows
- Find broken connections
- Generate workflow documentation
- Analyze workflow complexity and metrics
- Integrate validation in CI/CD pipelines
- Train team members on workflow structure
