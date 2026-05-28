---
name: dataflow-strict-mode
description: "Strict mode validation for DataFlow with 4-layer validation system (models, parameters, connections, workflows). Use when building production applications that require enhanced validation, catching errors before runtime, or enforcing data integrity constraints."
---

# DataFlow Strict Mode - Production-Ready Validation

Opt-in validation system with 4 validation layers providing enhanced error detection before workflow execution. Catch parameter errors, connection mismatches, model schema issues, and workflow structure problems at build time instead of runtime.

> **Skill Metadata**
> Category: `dataflow/validation`
> Priority: `HIGH`
> SDK Version: `0.8.0+ / DataFlow 0.8.0`
> Related Skills: [`dataflow-error-enhancer`](#), [`dataflow-models`](#), [`dataflow-gotchas`](#)
> Related Subagents: `dataflow-specialist` (enterprise patterns), `gold-standards-validator` (compliance)

## Quick Reference

- **4 Validation Layers**: Models → Parameters → Connections → Workflows
- **3-Tier Configuration**: Per-model > Global > Environment variable
- **Fail-Fast Mode**: Stop on first validation error (production default)
- **Verbose Mode**: Detailed validation messages (development/debugging)
- **Zero Performance Impact**: Validation only at build time, not execution
- **Backward Compatible**: Opt-in per model or globally

## ⚡ Quick Start

### Enable Strict Mode (3 Ways)

#### Method 1: Per-Model (Recommended)

```python
from dataflow import DataFlow

db = DataFlow("postgresql://localhost/mydb")

# Enable strict mode for specific model
@db.model
class User:
    id: str
    email: str
    name: str

    __dataflow__ = {
        'strict_mode': True  # Opt-in for this model only
    }

# Normal model without strict mode
@db.model
class Log:
    id: str
    message: str
    # No __dataflow__ flag = strict mode disabled
```

**When to use**: Production models requiring validation, while allowing flexibility for logging/temporary models.

#### Method 2: Global Configuration

```python
from dataflow import DataFlow

# Enable strict mode for all models
db = DataFlow("postgresql://localhost/mydb", strict_mode=True)

@db.model
class User:
    id: str
    email: str
    name: str
    # Strict mode enabled automatically

@db.model
class Order:
    id: str
    user_id: str
    total: float
    # Strict mode enabled automatically
```

**When to use**: Enterprise applications where all models require validation.

#### Method 3: Environment Variable

```bash
# .env file
DATAFLOW_STRICT_MODE=true
```

```python
from dataflow import DataFlow
import os
from dotenv import load_dotenv

load_dotenv()

db = DataFlow("postgresql://localhost/mydb")
# Strict mode enabled for all models via environment variable

@db.model
class User:
    id: str
    email: str
    # Strict mode enabled via DATAFLOW_STRICT_MODE
```

**When to use**: Deployment-specific configuration (production vs development).

## Configuration Priority (3-Tier System)

Strict mode uses a 3-tier priority system:

**Priority 1 (Highest)**: Per-model `__dataflow__` configuration
**Priority 2**: Global DataFlow instance configuration
**Priority 3 (Lowest)**: Environment variable `DATAFLOW_STRICT_MODE`

```python
# Example: Priority resolution
import os
os.environ['DATAFLOW_STRICT_MODE'] = 'true'  # Priority 3

db = DataFlow("postgresql://...", strict_mode=False)  # Priority 2 (overrides env var)

@db.model
class User:
    id: str
    email: str
    __dataflow__ = {'strict_mode': True}  # Priority 1 (overrides instance)

# Result: User model has strict mode ENABLED (per-model config wins)

@db.model
class Log:
    id: str
    message: str
    # No per-model config, falls back to instance config (False)

# Result: Log model has strict mode DISABLED (instance config wins)
```

## 4-Layer Validation System

### Layer 1: Model Validation

Validates model schema and field definitions.

**Checks**:
- Primary key field `id` exists
- Field types are valid Python types
- No reserved field conflicts
- Field annotations are correct

```python
# ✅ VALID - Correct model schema
@db.model
class User:
    id: str  # Primary key present
    email: str
    name: str
    __dataflow__ = {'strict_mode': True}

# ❌ INVALID - Missing primary key
@db.model
class InvalidModel:
    email: str
    name: str
    __dataflow__ = {'strict_mode': True}
# ValidationError: Model 'InvalidModel' must have 'id' field as primary key

# ❌ INVALID - Invalid field type
@db.model
class InvalidModel2:
    id: str
    data: CustomClass  # Unsupported type
    __dataflow__ = {'strict_mode': True}
# ValidationError: Field 'data' has unsupported type 'CustomClass'
```

**File Reference**: `src/dataflow/validation/model_validator.py:1-248`

### Layer 2: Parameter Validation

Validates node parameters before workflow execution.

**Checks**:
- Required parameters present (e.g., `id` for CreateNode)
- Parameter types match model field types
- No reserved fields (created_at, updated_at) in user parameters
- Parameter values are valid (not empty strings, not out of range)
- CreateNode vs UpdateNode structure correctness

```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

# ✅ VALID - All required parameters present
workflow.add_node("UserCreateNode", "create", {
    "id": "user-123",  # Required
    "email": "alice@example.com",
    "name": "Alice"
})

# ❌ INVALID - Missing required 'id' parameter
workflow.add_node("UserCreateNode", "create", {
    "email": "alice@example.com",
    "name": "Alice"
})
# ValidationError: Missing required parameter 'id' for UserCreateNode

# ❌ INVALID - Reserved field in parameters
workflow.add_node("UserCreateNode", "create", {
    "id": "user-123",
    "email": "alice@example.com",
    "name": "Alice",
    "created_at": "2025-01-01"  # Reserved field
})
# ValidationError: Cannot manually set reserved field 'created_at'

# ❌ INVALID - Wrong UpdateNode structure
workflow.add_node("UserUpdateNode", "update", {
    "id": "user-123",  # Wrong structure
    "name": "Alice Updated"
})
# ValidationError: UpdateNode requires 'filter' and 'fields' structure

# ✅ VALID - Correct UpdateNode structure
workflow.add_node("UserUpdateNode", "update", {
    "filter": {"id": "user-123"},
    "fields": {"name": "Alice Updated"}
})
```

**File Reference**: `src/dataflow/validation/parameter_validator.py:1-312`

### Layer 3: Connection Validation

Validates connections between workflow nodes.

**Checks**:
- Source and target nodes exist
- Parameter names are valid
- Types are compatible
- No circular dependencies
- Connection contracts satisfied

```python
workflow = WorkflowBuilder()

# Add nodes
workflow.add_node("UserCreateNode", "create", {
    "id": "user-123",
    "email": "alice@example.com",
    "name": "Alice"
})
workflow.add_node("UserReadNode", "read", {"id": "user-123"})

# ✅ VALID - Connection between existing nodes
workflow.add_connection("create", "id", "read", "id")

# ❌ INVALID - Source node doesn't exist
workflow.add_connection("nonexistent", "id", "read", "id")
# ValidationError: Source node 'nonexistent' not found in workflow

# ❌ INVALID - Parameter doesn't exist
workflow.add_connection("create", "invalid_field", "read", "id")
# ValidationError: Source parameter 'invalid_field' not found in 'create' node

# ❌ INVALID - Type mismatch
workflow.add_node("UserUpdateNode", "update", {
    "filter": {"id": "user-123"},
    "fields": {"email": 12345}  # int instead of str
})
# ValidationError: Parameter 'email' expects str, got int
```

**File Reference**: `src/dataflow/validation/connection_validator.py:1-285`

### Layer 4: Workflow Validation

Validates complete workflow structure before execution.

**Checks**:
- All nodes are reachable
- No orphaned nodes (except terminal nodes)
- Execution order is valid
- All required connections present
- No conflicting parameter sources

```python
from kailash.runtime import LocalRuntime

runtime = LocalRuntime()

# ✅ VALID - Complete workflow
workflow = WorkflowBuilder()
workflow.add_node("UserCreateNode", "create", {
    "id": "user-123",
    "email": "alice@example.com",
    "name": "Alice"
})
workflow.add_node("UserReadNode", "read", {"id": "user-123"})
workflow.add_connection("create", "id", "read", "id")

results, _ = runtime.execute(workflow.build())  # Validation passes

# ❌ INVALID - Orphaned node (no connections)
workflow2 = WorkflowBuilder()
workflow2.add_node("UserCreateNode", "create", {
    "id": "user-123",
    "email": "alice@example.com",
    "name": "Alice"
})
workflow2.add_node("UserReadNode", "read", {"id": "user-123"})
# No connection between nodes

results, _ = runtime.execute(workflow2.build())
# ValidationWarning: Node 'read' has no incoming connections (orphaned)
```

**File Reference**: `src/dataflow/validation/validators.py:1-198`

## Configuration Options

### StrictModeConfig

```python
from dataflow.validation.strict_mode import StrictModeConfig

# Default configuration
config = StrictModeConfig(
    enabled=True,
    validate_models=True,
    validate_parameters=True,
    validate_connections=True,
    validate_workflows=True,
    fail_fast=False,  # Collect all errors
    verbose=False     # Minimal output
)

# Production configuration (recommended)
prod_config = StrictModeConfig(
    enabled=True,
    validate_models=True,
    validate_parameters=True,
    validate_connections=True,
    validate_workflows=True,
    fail_fast=True,   # Stop on first error
    verbose=False     # Minimal output
)

# Development configuration
dev_config = StrictModeConfig(
    enabled=True,
    validate_models=True,
    validate_parameters=True,
    validate_connections=True,
    validate_workflows=True,
    fail_fast=False,  # Collect all errors
    verbose=True      # Detailed messages
)

# Apply configuration
db = DataFlow("postgresql://...", strict_mode_config=prod_config)
```

**File Reference**: `src/dataflow/validation/strict_mode.py:1-156`

### Validation Levels

```python
# Level 1: Model validation only
config = StrictModeConfig(
    enabled=True,
    validate_models=True,
    validate_parameters=False,
    validate_connections=False,
    validate_workflows=False
)

# Level 2: Model + Parameter validation
config = StrictModeConfig(
    enabled=True,
    validate_models=True,
    validate_parameters=True,
    validate_connections=False,
    validate_workflows=False
)

# Level 3: Model + Parameter + Connection validation
config = StrictModeConfig(
    enabled=True,
    validate_models=True,
    validate_parameters=True,
    validate_connections=True,
    validate_workflows=False
)

# Level 4: Full validation (recommended for production)
config = StrictModeConfig(
    enabled=True,
    validate_models=True,
    validate_parameters=True,
    validate_connections=True,
    validate_workflows=True
)
```

## Production Patterns

### Pattern 1: Per-Environment Configuration

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Production: Strict mode enabled via environment
# Development: Strict mode disabled via environment

db = DataFlow("postgresql://localhost/mydb")

# Critical models always use strict mode
@db.model
class User:
    id: str
    email: str
    password_hash: str
    __dataflow__ = {'strict_mode': True}  # Always validate

# Logging models can be flexible
@db.model
class Log:
    id: str
    message: str
    # Uses environment variable (disabled in dev, enabled in prod)
```

**Environment files**:
```bash
# .env.development
DATAFLOW_STRICT_MODE=false

# .env.production
DATAFLOW_STRICT_MODE=true
```

### Pattern 2: Fail-Fast in CI/CD

```python
from dataflow.validation.strict_mode import StrictModeConfig

# CI/CD pipeline configuration
config = StrictModeConfig(
    enabled=True,
    validate_models=True,
    validate_parameters=True,
    validate_connections=True,
    validate_workflows=True,
    fail_fast=True,   # Stop on first error (fast CI feedback)
    verbose=True      # Detailed error messages for debugging
)

db = DataFlow("postgresql://...", strict_mode_config=config)

# All tests run with strict mode enabled
# Catches validation errors before deployment
```

### Pattern 3: Selective Validation

```python
# Enterprise pattern: Critical models with strict mode
db = DataFlow("postgresql://...", strict_mode=False)  # Global disabled

@db.model
class User:
    id: str
    email: str
    __dataflow__ = {'strict_mode': True}  # Critical - always validate

@db.model
class Order:
    id: str
    user_id: str
    total: float
    __dataflow__ = {'strict_mode': True}  # Critical - always validate

@db.model
class AuditLog:
    id: str
    message: str
    # Non-critical - no validation overhead

@db.model
class TempData:
    id: str
    data: dict
    # Temporary - no validation overhead
```

## Error Messages

### Validation Errors

```python
# Example validation error
"""
ValidationError: Validation failed for UserCreateNode

Layer: PARAMETER
Node: create
Issue: Missing required parameter 'id'

Expected:
  workflow.add_node("UserCreateNode", "create", {
      "id": "user-123",  # Required parameter
      "email": "alice@example.com",
      "name": "Alice"
  })

Actual:
  workflow.add_node("UserCreateNode", "create", {
      "email": "alice@example.com",
      "name": "Alice"
  })

Solution: Add required 'id' parameter to node parameters
"""
```

### Verbose Mode Output

```python
# Enable verbose mode
config = StrictModeConfig(enabled=True, verbose=True)
db = DataFlow("postgresql://...", strict_mode_config=config)

# Validation output
"""
[STRICT MODE] Validating model: User
  ✓ Primary key 'id' present
  ✓ Field types valid
  ✓ No reserved field conflicts

[STRICT MODE] Validating parameters: UserCreateNode
  ✓ Required parameter 'id' present
  ✓ Parameter types match model
  ✓ No reserved fields in parameters

[STRICT MODE] Validating connections: create -> read
  ✓ Source node exists
  ✓ Target node exists
  ✓ Parameters compatible

[STRICT MODE] Validating workflow structure
  ✓ All nodes reachable
  ✓ No orphaned nodes
  ✓ Execution order valid

[STRICT MODE] Validation passed (4 layers, 0 errors)
"""
```

## Performance Impact

### Build-Time Validation Only

```python
# Validation happens ONLY at workflow.build()
# NO performance impact during runtime.execute()

from kailash.runtime import LocalRuntime
import time

workflow = WorkflowBuilder()
workflow.add_node("UserCreateNode", "create", {
    "id": "user-123",
    "email": "alice@example.com",
    "name": "Alice"
})

# Validation happens here (one-time cost: ~1-5ms)
built_workflow = workflow.build()

runtime = LocalRuntime()

# NO validation overhead during execution
start = time.time()
results, _ = runtime.execute(built_workflow)
end = time.time()

print(f"Execution time: {(end - start) * 1000:.2f}ms")  # Same as non-strict mode
```

**Benchmark Results**:
- **Build time**: +1-5ms (one-time validation cost)
- **Execution time**: 0ms overhead (no runtime impact)
- **Memory**: <1KB per validated node

## Troubleshooting

### Issue: Validation too strict for development

**Solution**: Disable strict mode globally, enable per-model for critical models only.

```python
db = DataFlow("postgresql://...", strict_mode=False)

@db.model
class User:
    id: str
    email: str
    __dataflow__ = {'strict_mode': True}  # Only critical model validated
```

### Issue: Too many validation errors

**Solution**: Use fail_fast=True to stop on first error.

```python
config = StrictModeConfig(enabled=True, fail_fast=True)
db = DataFlow("postgresql://...", strict_mode_config=config)
```

### Issue: Unclear validation messages

**Solution**: Enable verbose mode for detailed output.

```python
config = StrictModeConfig(enabled=True, verbose=True)
db = DataFlow("postgresql://...", strict_mode_config=config)
```

## Testing with Strict Mode

### Integration Tests

```python
# tests/integration/test_strict_mode_integration.py
import pytest
from dataflow import DataFlow
from dataflow.validation.strict_mode import StrictModeConfig

@pytest.mark.integration
async def test_strict_mode_parameter_validation(db):
    """Test strict mode catches parameter errors."""

    # Enable strict mode
    config = StrictModeConfig(enabled=True, fail_fast=True)
    db_strict = DataFlow(":memory:", strict_mode_config=config)

    @db_strict.model
    class User:
        id: str
        email: str
        __dataflow__ = {'strict_mode': True}

    await db_strict.initialize()

    # Missing required parameter should raise ValidationError
    workflow = WorkflowBuilder()
    with pytest.raises(ValidationError, match="Missing required parameter 'id'"):
        workflow.add_node("UserCreateNode", "create", {
            "email": "alice@example.com"
        })
        workflow.build()  # Validation happens here
```

**File Reference**: `tests/integration/test_parameter_validation_integration.py:1-150`

## Documentation References

### Comprehensive Guides
- **Strict Mode Guide**: `sdk-users/apps/dataflow/guides/strict-mode.md` (comprehensive validation guide)
- **Architecture Decision**: `docs/architecture/ADR-003-STRICT-MODE.md` (design rationale)
- **Validation Guide**: `docs/guides/strict-mode-validation.md` (implementation details)

### Testing
- **Parameter Validation Tests**: `tests/integration/test_parameter_validation_integration.py` (38 tests)
- **Connection Validation Tests**: `tests/integration/test_connection_validation_integration.py` (28 tests)
- **Model Validation Tests**: `tests/integration/test_model_validation_integration.py` (22 tests)

### Integration
- **CLAUDE.md**: Strict Mode section with Quick Start
- **dataflow-specialist**: Enterprise patterns and production configuration

## Requirements

- **Python**: 3.10+
- **Dependencies**: `kailash>=0.10.0`

## When to Use Strict Mode

**Use Strict Mode when**:
- ✅ Building production applications requiring data integrity
- ✅ Need to catch parameter errors before runtime
- ✅ Working with critical models (User, Order, Payment)
- ✅ Enforcing team coding standards
- ✅ Running CI/CD pipelines with validation

**Don't Use Strict Mode when**:
- ❌ Rapid prototyping or experimentation
- ❌ Logging or temporary data models
- ❌ Performance-critical code paths (though impact is minimal)
- ❌ Legacy code migration (enable gradually per model)

**Recommended Approach**:
Start with global strict mode disabled, enable per-model for critical models, then gradually enable globally as codebase matures.
