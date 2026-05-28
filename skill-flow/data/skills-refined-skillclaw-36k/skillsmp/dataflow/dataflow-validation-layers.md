---
name: dataflow-validation-layers
description: "4-layer validation system architecture for DataFlow: Models → Parameters → Connections → Workflows. Use when understanding DataFlow's validation pipeline, implementing custom validators, or debugging validation issues."
---

# DataFlow Validation Layers - Architecture Guide

Complete reference for DataFlow's 4-layer validation system that validates models, parameters, connections, and workflows before execution. Learn how each layer works, what it validates, and how to extend validation for custom use cases.

> **Skill Metadata**
> Category: `dataflow/architecture`
> Priority: `MEDIUM`
> Related Skills: [`dataflow-strict-mode`](#), [`dataflow-gotchas`](#), [`dataflow-models`](#)
> Related Subagents: `dataflow-specialist` (enterprise patterns), `pattern-expert` (workflow patterns)

## Quick Reference

- **Layer 1 (Model)**: Validates model schema and field definitions
- **Layer 2 (Parameter)**: Validates node parameters before workflow execution
- **Layer 3 (Connection)**: Validates connections between workflow nodes
- **Layer 4 (Workflow)**: Validates complete workflow structure
- **Execution Order**: Models → Parameters → Connections → Workflows (bottom-up)
- **Performance**: Build-time validation only (<5ms overhead)

## Architecture Overview

### Validation Flow

```
┌─────────────────────────────────────────────────────────────┐
│                                                               │
│  @db.model class User: id, email, name                      │
│                                                               │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │  Layer 1: Model     │
         │  ModelValidator     │
         └──────────┬──────────┘
                    │ Validates: Primary key, field types, reserved fields
                    ▼
         ┌─────────────────────┐
         │  Layer 2: Parameter │
         │  ParameterValidator │
         └──────────┬──────────┘
                    │ Validates: Required params, types, reserved fields
                    ▼
         ┌─────────────────────┐
         │ Layer 3: Connection │
         │ ConnectionValidator │
         └──────────┬──────────┘
                    │ Validates: Node exists, param exists, type compatibility
                    ▼
         ┌─────────────────────┐
         │ Layer 4: Workflow   │
         │  WorkflowValidator  │
         └──────────┬──────────┘
                    │ Validates: Reachability, orphans, execution order
                    ▼
         ┌─────────────────────┐
         │   Execution Ready   │
         │  runtime.execute()  │
         └─────────────────────┘
```

### Validation Timing

```python
from dataflow import DataFlow
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

db = DataFlow("postgresql://...")

@db.model
class User:
    id: str
    email: str
    __dataflow__ = {'strict_mode': True}

# Layer 1: Model validation happens here (at decoration time)
# ✓ Validates: Primary key exists, field types valid

workflow = WorkflowBuilder()

# Layer 2: Parameter validation happens here (at add_node time)
workflow.add_node("UserCreateNode", "create", {
    "id": "user-123",
    "email": "alice@example.com"
})
# ✓ Validates: Required parameters present, types match model

# Layer 3: Connection validation happens here (at add_connection time)
workflow.add_node("UserReadNode", "read", {"id": "user-123"})
workflow.add_connection("create", "id", "read", "id")
# ✓ Validates: Source/target nodes exist, parameters compatible

runtime = LocalRuntime()

# Layer 4: Workflow validation happens here (at build time)
built_workflow = workflow.build()
# ✓ Validates: All nodes reachable, no orphans, execution order valid

# NO validation during execution (zero overhead)
results, _ = runtime.execute(built_workflow)
```

## Layer 1: Model Validation

**File**: `src/dataflow/validation/model_validator.py:1-248`

### What It Validates

```python
class ModelValidator:
    """Layer 1: Validate model schema and field definitions."""

    def validate_model(self, model_class: type) -> None:
        """
        Validates:
        - Primary key 'id' field exists
        - Field types are valid Python types (str, int, float, bool, dict, list)
        - No reserved field conflicts (created_at, updated_at)
        - Field annotations are correct
        - No duplicate field names
        """
```

### Examples

#### Valid Models

```python
# ✅ VALID - Standard model
@db.model
class User:
    id: str  # Primary key present
    email: str
    name: str
    __dataflow__ = {'strict_mode': True}

# ✅ VALID - Optional fields
@db.model
class Profile:
    id: str
    bio: Optional[str]  # Optional field
    avatar_url: Optional[str]
    __dataflow__ = {'strict_mode': True}

# ✅ VALID - Complex types
@db.model
class Order:
    id: str
    items: List[dict]  # List of dicts
    metadata: dict
    total: float
    __dataflow__ = {'strict_mode': True}
```

#### Invalid Models

```python
# ❌ INVALID - Missing primary key 'id'
@db.model
class InvalidModel1:
    user_id: str  # Wrong name, must be 'id'
    email: str
    __dataflow__ = {'strict_mode': True}
# ValidationError: Model must have 'id' field as primary key

# ❌ INVALID - Reserved field conflict
@db.model
class InvalidModel2:
    id: str
    email: str
    created_at: str  # Reserved field, auto-managed by DataFlow
    __dataflow__ = {'strict_mode': True}
# ValidationError: Field 'created_at' is reserved and cannot be manually defined

# ❌ INVALID - Unsupported field type
@db.model
class InvalidModel3:
    id: str
    data: MyCustomClass  # Unsupported type
    __dataflow__ = {'strict_mode': True}
# ValidationError: Field 'data' has unsupported type 'MyCustomClass'
```

### Validation API

```python
from dataflow.validation.model_validator import ModelValidator

validator = ModelValidator()

# Validate model
try:
    validator.validate_model(User)
    print("Model valid!")
except ValidationError as e:
    print(f"Model invalid: {e}")

# Check specific field
is_valid = validator.check_field_type(User, "email", str)
print(f"Field 'email' type valid: {is_valid}")

# Get model errors
errors = validator.get_model_errors(User)
if errors:
    print(f"Errors: {errors}")
```

### Supported Types

| Python Type | PostgreSQL | MySQL | SQLite | Notes |
|-------------|------------|-------|--------|-------|
| `str` | TEXT | TEXT | TEXT | String fields |
| `int` | INTEGER | INTEGER | INTEGER | Integer fields |
| `float` | REAL | REAL | REAL | Float fields |
| `bool` | BOOLEAN | BOOLEAN | BOOLEAN | Boolean fields |
| `dict` | JSONB | JSON | TEXT | JSON fields |
| `List[str]` | TEXT[] (PostgreSQL), JSON (others) | JSON | TEXT | String arrays |
| `List[int]` | INTEGER[] (PostgreSQL), JSON (others) | JSON | TEXT | Integer arrays |
| `List[float]` | REAL[] (PostgreSQL), JSON (others) | JSON | TEXT | Float arrays |
| `List[dict]` | JSONB | JSON | TEXT | Array of objects |
| `Optional[T]` | T NULL | T NULL | T NULL | Nullable fields |

## Layer 2: Parameter Validation

**File**: `src/dataflow/validation/parameter_validator.py:1-312`

### What It Validates

```python
class ParameterValidator:
    """Layer 2: Validate node parameters before workflow execution."""

    def validate_parameters(self, node_name: str, node_id: str, params: dict) -> None:
        """
        Validates:
        - Required parameters present (e.g., 'id' for CreateNode)
        - Parameter types match model field types
        - No reserved fields in user parameters
        - Parameter values are valid (not empty, not None for required)
        - CreateNode vs UpdateNode structure correctness
        """
```

### Node-Specific Validation

#### CreateNode Validation

```python
# ✅ VALID - All required parameters
workflow.add_node("UserCreateNode", "create", {
    "id": "user-123",  # Required
    "email": "alice@example.com",
    "name": "Alice"
})

# ❌ INVALID - Missing required 'id'
workflow.add_node("UserCreateNode", "create", {
    "email": "alice@example.com",
    "name": "Alice"
})
# ValidationError: Missing required parameter 'id' for UserCreateNode

# ❌ INVALID - Type mismatch
workflow.add_node("UserCreateNode", "create", {
    "id": 123,  # Should be str, not int
    "email": "alice@example.com",
    "name": "Alice"
})
# ValidationError: Parameter 'id' expects str, got int

# ❌ INVALID - Reserved field
workflow.add_node("UserCreateNode", "create", {
    "id": "user-123",
    "email": "alice@example.com",
    "name": "Alice",
    "created_at": "2025-01-01"  # Reserved field
})
# ValidationError: Cannot manually set reserved field 'created_at'
```

#### UpdateNode Validation

```python
# ✅ VALID - Correct structure (filter + fields)
workflow.add_node("UserUpdateNode", "update", {
    "filter": {"id": "user-123"},  # Which record
    "fields": {"name": "Alice Updated"}  # What to update
})

# ❌ INVALID - Missing 'filter' field
workflow.add_node("UserUpdateNode", "update", {
    "fields": {"name": "Alice Updated"}
})
# ValidationError: UPDATE request must contain 'filter' field

# ❌ INVALID - Wrong structure (flat params like CreateNode)
workflow.add_node("UserUpdateNode", "update", {
    "id": "user-123",
    "name": "Alice Updated"
})
# ValidationError: UpdateNode requires 'filter' and 'fields' structure

# ❌ INVALID - Reserved field in 'fields'
workflow.add_node("UserUpdateNode", "update", {
    "filter": {"id": "user-123"},
    "fields": {
        "name": "Alice Updated",
        "updated_at": "2025-01-01"  # Reserved field
    }
})
# ValidationError: Cannot manually set reserved field 'updated_at'
```

#### DeleteNode Validation

```python
# ✅ VALID - Filter specified
workflow.add_node("UserDeleteNode", "delete", {
    "filter": {"id": "user-123"}
})

# ❌ INVALID - Missing filter (dangerous!)
workflow.add_node("UserDeleteNode", "delete", {})
# ValidationError: DELETE request must contain 'filter' field (prevents accidental delete all)
```

### Validation API

```python
from dataflow.validation.parameter_validator import ParameterValidator

validator = ParameterValidator(db)

# Validate CREATE node parameters
try:
    validator.validate_parameters("UserCreateNode", "create", {
        "id": "user-123",
        "email": "alice@example.com"
    })
    print("Parameters valid!")
except ValidationError as e:
    print(f"Parameters invalid: {e}")

# Check parameter type
is_valid = validator.check_parameter_type("User", "email", "alice@example.com")
print(f"Parameter type valid: {is_valid}")
```

## Layer 3: Connection Validation

**File**: `src/dataflow/validation/connection_validator.py:1-285`

### What It Validates

```python
class ConnectionValidator:
    """Layer 3: Validate connections between workflow nodes."""

    def validate_connection(
        self,
        source_node_id: str,
        source_param: str,
        target_node_id: str,
        target_param: str,
        workflow: WorkflowBuilder
    ) -> None:
        """
        Validates:
        - Source node exists in workflow
        - Target node exists in workflow
        - Source parameter exists in source node
        - Target parameter exists in target node
        - Types are compatible
        - No circular dependencies
        """
```

### Examples

#### Valid Connections

```python
workflow = WorkflowBuilder()

# Add nodes first
workflow.add_node("UserCreateNode", "create", {
    "id": "user-123",
    "email": "alice@example.com",
    "name": "Alice"
})
workflow.add_node("UserReadNode", "read", {"id": "user-123"})

# ✅ VALID - Connection between existing nodes
workflow.add_connection("create", "id", "read", "id")

# ✅ VALID - Multiple connections
workflow.add_node("UserUpdateNode", "update", {
    "filter": {"id": "user-123"},
    "fields": {"name": "Alice Updated"}
})
workflow.add_connection("create", "id", "update", "id")  # create -> update
workflow.add_connection("update", "id", "read", "id")    # update -> read
```

#### Invalid Connections

```python
# ❌ INVALID - Source node doesn't exist
workflow.add_connection("nonexistent", "id", "read", "id")
# ValidationError: Source node 'nonexistent' not found in workflow

# ❌ INVALID - Target node doesn't exist
workflow.add_connection("create", "id", "nonexistent", "id")
# ValidationError: Target node 'nonexistent' not found in workflow

# ❌ INVALID - Source parameter doesn't exist
workflow.add_connection("create", "invalid_field", "read", "id")
# ValidationError: Source parameter 'invalid_field' not found in node 'create'

# ❌ INVALID - Type mismatch
workflow.add_node("OrderCreateNode", "create_order", {
    "id": "order-123",
    "total": 99.99  # float
})
workflow.add_node("UserReadNode", "read_user", {"id": "user-123"})
workflow.add_connection("create_order", "total", "read_user", "id")
# ValidationError: Type mismatch: 'total' (float) cannot connect to 'id' (str)

# ❌ INVALID - Circular dependency
workflow.add_connection("create", "id", "update", "id")
workflow.add_connection("update", "id", "create", "id")  # Creates cycle
# ValidationError: Circular dependency detected: create -> update -> create
```

### Validation API

```python
from dataflow.validation.connection_validator import ConnectionValidator

validator = ConnectionValidator()

# Validate connection
try:
    validator.validate_connection(
        source_node_id="create",
        source_param="id",
        target_node_id="read",
        target_param="id",
        workflow=workflow
    )
    print("Connection valid!")
except ValidationError as e:
    print(f"Connection invalid: {e}")

# Check for circular dependencies
has_cycle = validator.has_circular_dependency(workflow)
print(f"Has circular dependency: {has_cycle}")
```

## Layer 4: Workflow Validation

**File**: `src/dataflow/validation/validators.py:1-198`

### What It Validates

```python
class WorkflowValidator:
    """Layer 4: Validate complete workflow structure."""

    def validate_workflow(self, workflow: WorkflowBuilder) -> None:
        """
        Validates:
        - All nodes are reachable from entry points
        - No orphaned nodes (except terminal nodes)
        - Execution order is valid (topological sort possible)
        - All required connections present
        - No conflicting parameter sources
        """
```

### Examples

#### Valid Workflows

```python
# ✅ VALID - Linear workflow
workflow = WorkflowBuilder()
workflow.add_node("UserCreateNode", "create", {
    "id": "user-123",
    "email": "alice@example.com"
})
workflow.add_node("UserReadNode", "read", {"id": "user-123"})
workflow.add_connection("create", "id", "read", "id")

built = workflow.build()  # Validation passes

# ✅ VALID - Branching workflow
workflow2 = WorkflowBuilder()
workflow2.add_node("UserCreateNode", "create", {
    "id": "user-123",
    "email": "alice@example.com"
})
workflow2.add_node("UserReadNode", "read1", {"id": "user-123"})
workflow2.add_node("UserUpdateNode", "update", {
    "filter": {"id": "user-123"},
    "fields": {"name": "Alice"}
})
workflow2.add_connection("create", "id", "read1", "id")
workflow2.add_connection("create", "id", "update", "id")

built2 = workflow2.build()  # Validation passes

# ✅ VALID - Terminal node (no outgoing connections)
workflow3 = WorkflowBuilder()
workflow3.add_node("UserCreateNode", "create", {
    "id": "user-123",
    "email": "alice@example.com"
})
workflow3.add_node("UserReadNode", "read", {"id": "user-123"})
workflow3.add_connection("create", "id", "read", "id")
# 'read' is terminal node (no outgoing connections) - this is fine

built3 = workflow3.build()  # Validation passes
```

#### Invalid Workflows

```python
# ❌ INVALID - Orphaned node (no incoming connections)
workflow_invalid1 = WorkflowBuilder()
workflow_invalid1.add_node("UserCreateNode", "create", {
    "id": "user-123",
    "email": "alice@example.com"
})
workflow_invalid1.add_node("UserReadNode", "read", {"id": "user-123"})
# No connection between nodes

built = workflow_invalid1.build()
# ValidationWarning: Node 'read' has no incoming connections (orphaned)

# ❌ INVALID - Unreachable nodes
workflow_invalid2 = WorkflowBuilder()
workflow_invalid2.add_node("UserCreateNode", "create1", {
    "id": "user-123",
    "email": "alice@example.com"
})
workflow_invalid2.add_node("UserCreateNode", "create2", {
    "id": "user-456",
    "email": "bob@example.com"
})
workflow_invalid2.add_node("UserReadNode", "read", {"id": "user-123"})
workflow_invalid2.add_connection("create1", "id", "read", "id")
# 'create2' is unreachable (no connections to it or from it)

built = workflow_invalid2.build()
# ValidationWarning: Node 'create2' is unreachable
```

### Validation API

```python
from dataflow.validation.validators import WorkflowValidator

validator = WorkflowValidator()

# Validate workflow
try:
    validator.validate_workflow(workflow)
    print("Workflow valid!")
except ValidationError as e:
    print(f"Workflow invalid: {e}")

# Check for orphaned nodes
orphaned = validator.find_orphaned_nodes(workflow)
print(f"Orphaned nodes: {orphaned}")

# Check execution order
order = validator.get_execution_order(workflow)
print(f"Execution order: {order}")
```

## Integration with Strict Mode

All 4 validation layers integrate with Strict Mode configuration:

```python
from dataflow import DataFlow
from dataflow.validation.strict_mode import StrictModeConfig

# Configure strict mode with specific layers
config = StrictModeConfig(
    enabled=True,
    validate_models=True,      # Layer 1
    validate_parameters=True,  # Layer 2
    validate_connections=True, # Layer 3
    validate_workflows=True,   # Layer 4
    fail_fast=True,
    verbose=True
)

db = DataFlow("postgresql://...", strict_mode_config=config)

# All 4 layers will validate
@db.model
class User:
    id: str
    email: str
    __dataflow__ = {'strict_mode': True}
```

### Selective Layer Enablement

```python
# Enable only model and parameter validation
config = StrictModeConfig(
    enabled=True,
    validate_models=True,      # Layer 1 enabled
    validate_parameters=True,  # Layer 2 enabled
    validate_connections=False, # Layer 3 disabled
    validate_workflows=False    # Layer 4 disabled
)

db = DataFlow("postgresql://...", strict_mode_config=config)
```

## Error Messages by Layer

### Layer 1: Model Errors

```
ValidationError: Model validation failed

Model: User
Issue: Missing primary key field 'id'

Expected:
  @db.model
  class User:
      id: str  # Primary key required
      email: str

Actual:
  @db.model
  class User:
      email: str

Solution: Add 'id' field to model
```

### Layer 2: Parameter Errors

```
ValidationError: Parameter validation failed

Node: UserCreateNode (id: create)
Issue: Missing required parameter 'id'

Expected:
  workflow.add_node("UserCreateNode", "create", {
      "id": "user-123",  # Required parameter
      "email": "alice@example.com"
  })

Actual:
  workflow.add_node("UserCreateNode", "create", {
      "email": "alice@example.com"
  })

Solution: Add required 'id' parameter
```

### Layer 3: Connection Errors

```
ValidationError: Connection validation failed

Connection: create -> read
Issue: Source node 'create' not found in workflow

Solution: Add source node before creating connection
  workflow.add_node("UserCreateNode", "create", {...})
  workflow.add_connection("create", "id", "read", "id")
```

### Layer 4: Workflow Errors

```
ValidationWarning: Workflow structure issue

Workflow: user_workflow
Issue: Node 'read' has no incoming connections (orphaned)

Potential causes:
  1. Missing connection from source node
  2. Node should be removed
  3. Node should be entry point

Solution: Either connect the node or remove it
  workflow.add_connection("create", "id", "read", "id")
```

## Performance Characteristics

### Validation Overhead

| Layer | Timing | Overhead | When |
|-------|--------|----------|------|
| Layer 1 (Model) | Model decoration | ~0.5ms | One-time per model |
| Layer 2 (Parameter) | add_node() call | ~0.5ms | Per node added |
| Layer 3 (Connection) | add_connection() call | ~0.5ms | Per connection added |
| Layer 4 (Workflow) | workflow.build() call | ~2ms | One-time per workflow |
| **Total** | **Build time** | **~4ms** | **Zero runtime overhead** |

### Zero Runtime Overhead

```python
import time

# Build workflow (validation happens here)
start_build = time.time()
built_workflow = workflow.build()  # ~4ms with validation
end_build = time.time()

print(f"Build time (with validation): {(end_build - start_build) * 1000:.2f}ms")

# Execute workflow (NO validation overhead)
runtime = LocalRuntime()

start_exec = time.time()
results, _ = runtime.execute(built_workflow)  # Same speed as non-validated
end_exec = time.time()

print(f"Execution time: {(end_exec - start_exec) * 1000:.2f}ms")
# Execution time identical to non-strict mode!
```

## Extending Validation

### Custom Validator

```python
from dataflow.validation.validators import BaseValidator

class CustomValidator(BaseValidator):
    """Custom validation logic."""

    def validate_custom_rule(self, model: type) -> None:
        """Validate custom business rule."""
        # Example: Ensure 'email' field exists
        if not hasattr(model, 'email'):
            raise ValidationError("Model must have 'email' field")

# Use custom validator
validator = CustomValidator()
validator.validate_custom_rule(User)
```

### Plugin Validators

```python
from dataflow import DataFlow

db = DataFlow("postgresql://...")

# Register custom validator
@db.register_validator
class EmailValidator:
    """Validate email field format."""

    def validate(self, model: type) -> None:
        if hasattr(model, 'email'):
            # Validate email format
            pass

# Validator runs automatically during Layer 1 validation
```

## Testing Validation

### Unit Tests

```python
# tests/unit/test_model_validator.py
import pytest
from dataflow.validation.model_validator import ModelValidator

@pytest.mark.unit
def test_model_validator_missing_id():
    """Test model validation catches missing 'id' field."""

    validator = ModelValidator()

    class InvalidModel:
        email: str

    with pytest.raises(ValidationError, match="must have 'id' field"):
        validator.validate_model(InvalidModel)
```

### Integration Tests

```python
# tests/integration/test_validation_layers_integration.py
import pytest
from dataflow import DataFlow
from dataflow.validation.strict_mode import StrictModeConfig

@pytest.mark.integration
async def test_all_validation_layers():
    """Test complete validation pipeline."""

    config = StrictModeConfig(enabled=True, fail_fast=True, verbose=True)
    db = DataFlow(":memory:", strict_mode_config=config)

    @db.model
    class User:
        id: str
        email: str
        __dataflow__ = {'strict_mode': True}

    await db.initialize()

    workflow = WorkflowBuilder()

    # Layer 2: Parameter validation should pass
    workflow.add_node("UserCreateNode", "create", {
        "id": "user-123",
        "email": "alice@example.com"
    })

    # Layer 4: Workflow validation should pass
    built = workflow.build()

    assert built is not None
```

## Documentation References

### Architecture
- **ADR-003**: `docs/architecture/ADR-003-STRICT-MODE.md` (validation design)
- **Validation Guide**: `docs/guides/strict-mode-validation.md` (implementation)

### Testing
- **Model Validation**: `tests/unit/test_model_validator.py` (45 tests)
- **Parameter Validation**: `tests/unit/test_parameter_validation.py` (62 tests)
- **Connection Validation**: `tests/unit/test_connection_validation.py` (38 tests)
- **Integration Tests**: `tests/integration/test_*_validation_integration.py` (120+ tests)

### Related
- **dataflow-strict-mode**: Strict mode configuration and usage
- **dataflow-gotchas**: Common validation errors to avoid
- **dataflow-models**: Model definition best practices

## Requirements

- **Python**: 3.10+
- **Dependencies**: `kailash>=0.10.0`
