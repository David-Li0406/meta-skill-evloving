---
name: dataflow-error-enhancer
description: "ErrorEnhancer system for actionable DataFlow error messages with DF-XXX codes, root cause analysis, and solutions. Use when debugging DataFlow errors, missing parameters, type mismatches, validation errors, or need error context and fixes."
---

# DataFlow ErrorEnhancer - Actionable Error Messages

Automatic error enhancement with DF-XXX codes, context, root causes, and actionable solutions for DataFlow applications.

> **Skill Metadata**
> Category: `dataflow/dx`
> Priority: `CRITICAL`
> Related Skills: [`dataflow-inspector`](#), [`dataflow-validation`](#), [`top-10-errors`](#)
> Related Subagents: `dataflow-specialist` (complex errors), `testing-specialist` (test errors)

## Quick Reference

- **60+ Error Codes**: DF-1XX (parameters) through DF-8XX (runtime)
- **Automatic Integration**: Built into DataFlow engine
- **Rich Context**: Node, parameters, workflow state, stack traces
- **Actionable Solutions**: Code templates with variable substitution
- **Color-Coded Output**: Emojis and formatting for readability
- **Documentation Links**: Direct links to relevant guides

## ⚠️ CRITICAL: ErrorEnhancer is Automatic

ErrorEnhancer is **automatically integrated** into DataFlow. You do NOT need to:
- ❌ Import ErrorEnhancer manually
- ❌ Wrap code in try/except to enable it
- ❌ Configure error enhancement

It **automatically enhances** all DataFlow exceptions with rich context and solutions.

## Error Code Categories

### DF-1XX: Parameter Errors
Missing, invalid, or malformed parameters in workflow nodes.

| Code | Error | Common Cause |
|------|-------|--------------|
| DF-101 | Missing required parameter | Forgot to pass `data`, `filter`, or `fields` |
| DF-102 | Type mismatch | Passed string instead of dict |
| DF-103 | Auto-managed field conflict | Manually set `created_at` or `updated_at` |
| DF-104 | Wrong node pattern | Used CreateNode parameters for UpdateNode |
| DF-105 | Primary key issue | Missing `id` field or wrong name |

### DF-2XX: Connection Errors
Invalid or broken connections between workflow nodes.

| Code | Error | Common Cause |
|------|-------|--------------|
| DF-201 | Invalid connection | Source output doesn't exist |
| DF-202 | Circular dependency | Node depends on itself |
| DF-203 | Type mismatch | Output type incompatible with input |
| DF-204 | Missing connection | Required parameter not connected |

### DF-3XX: Migration Errors
Database schema and migration issues.

| Code | Error | Common Cause |
|------|-------|--------------|
| DF-301 | Migration failed | Table already exists |
| DF-302 | Schema mismatch | Model doesn't match database |
| DF-303 | Constraint violation | Foreign key or unique constraint |

### DF-4XX: Configuration Errors
DataFlow instance configuration issues.

| Code | Error | Common Cause |
|------|-------|--------------|
| DF-401 | Invalid connection string | Malformed database URL |
| DF-402 | Missing database | Database doesn't exist |
| DF-403 | Authentication failed | Wrong credentials |

### DF-5XX: Runtime Errors
Errors during workflow execution.

| Code | Error | Common Cause |
|------|-------|--------------|
| DF-501 | Sync method in async context | Called `create_tables()` from async function - use `create_tables_async()` |
| DF-502 | Transaction failed | Deadlock or timeout |
| DF-503 | Connection pool exhausted | Too many concurrent queries |
| DF-504 | Query execution failed | Invalid SQL or database error |

### DF-6XX: Model Errors
Issues with @db.model definitions.

| Code | Error | Common Cause |
|------|-------|--------------|
| DF-601 | Invalid model definition | Missing fields or wrong types |
| DF-602 | Duplicate model | Model registered twice |
| DF-603 | Invalid field type | Unsupported Python type |

### DF-7XX: Node Errors
Issues with auto-generated DataFlow nodes.

| Code | Error | Common Cause |
|------|-------|--------------|
| DF-701 | Node generation failed | Invalid model configuration |
| DF-702 | Node not found | Model not registered |
| DF-703 | Invalid node parameters | Wrong parameter structure |

### DF-8XX: Workflow Errors
High-level workflow validation and execution errors.

| Code | Error | Common Cause |
|------|-------|--------------|
| DF-801 | Workflow validation failed | Invalid structure |
| DF-802 | Execution timeout | Query too slow |
| DF-803 | Resource exhaustion | Out of memory |

## Enhanced Error Format

ErrorEnhancer transforms basic Python exceptions into rich error messages:

### Before ErrorEnhancer
```python
KeyError: 'data'
```

### After ErrorEnhancer
```
🔴 DF-101: Missing Required Parameter 'data'

📍 Context:
  Node: UserCreateNode (create_user)
  Operation: CREATE
  Model: User
  Database: postgresql://localhost/app_db

🔎 Root Cause (Probability: 95%):
  The 'data' parameter is required for CreateNode operations but was not provided.

💡 Solution 1: Add 'data' parameter with required fields
  workflow.add_node("UserCreateNode", "create_user", {
      "data": {
          "name": "Alice",
          "email": "alice@example.com"
      }
  })

💡 Solution 2: Connect 'data' from previous node
  workflow.add_connection("prepare_data", "result", "create_user", "data")

📖 Documentation:
  - CreateNode Guide: sdk-users/apps/dataflow/guides/create-vs-update.md
  - Top 10 Errors: sdk-users/apps/dataflow/troubleshooting/top-10-errors.md
```

## Common Errors and Solutions

### DF-101: Missing Required Parameter

**Error Message:**
```
🔴 DF-101: Missing Required Parameter 'data'
```

**Cause:** CreateNode requires `data` parameter with model fields.

**Solution:**
```python
# ✅ CORRECT - Provide data parameter
workflow.add_node("UserCreateNode", "create", {
    "data": {
        "name": "Alice",
        "email": "alice@example.com"
    }
})

# ❌ WRONG - Missing data parameter
workflow.add_node("UserCreateNode", "create", {})
```

---

### DF-102: Type Mismatch

**Error Message:**
```
🔴 DF-102: Type Mismatch - Expected dict, got str
```

**Cause:** Parameter expects dictionary but received string.

**Solution:**
```python
# ✅ CORRECT - Pass dict for filter
workflow.add_node("UserReadNode", "read", {
    "filter": {"id": "user-123"}  # ← dict
})

# ❌ WRONG - Passed string instead of dict
workflow.add_node("UserReadNode", "read", {
    "filter": "user-123"  # ← string
})
```

---

### DF-103: Auto-Managed Field Conflict

**Error Message:**
```
🔴 DF-103: Auto-Managed Field Conflict - 'created_at' is managed automatically
```

**Cause:** Attempted to manually set `created_at` or `updated_at`.

**Solution:**
```python
# ✅ CORRECT - Let DataFlow manage timestamps
workflow.add_node("UserCreateNode", "create", {
    "data": {
        "name": "Alice",
        "email": "alice@example.com"
        # created_at/updated_at auto-generated
    }
})

# ❌ WRONG - Manually setting auto-managed fields
workflow.add_node("UserCreateNode", "create", {
    "data": {
        "name": "Alice",
        "created_at": datetime.now()  # ← Error!
    }
})
```

---

### DF-104: Wrong Node Pattern

**Error Message:**
```
🔴 DF-104: Wrong Node Pattern - CreateNode expects flat fields, not nested filter
```

**Cause:** Used UpdateNode parameter structure for CreateNode.

**Solution:**
```python
# ✅ CORRECT - CreateNode uses FLAT fields
workflow.add_node("UserCreateNode", "create", {
    "name": "Alice",            # ← Flat structure
    "email": "alice@example.com"
})

# ✅ CORRECT - UpdateNode uses NESTED filter + fields
workflow.add_node("UserUpdateNode", "update", {
    "filter": {"id": 1},        # ← Nested structure
    "fields": {"name": "Alice Updated"}
})

# ❌ WRONG - Used UpdateNode pattern for CreateNode
workflow.add_node("UserCreateNode", "create", {
    "filter": {"id": 1},  # ← CreateNode doesn't use filter!
    "fields": {"name": "Alice"}
})
```

**See:** `sdk-users/apps/dataflow/guides/create-vs-update.md` (comprehensive guide)

---

### DF-501: Sync Method in Async Context (v0.10.7+)

**Error Message:**
```
🔴 DF-501: Sync Method in Async Context

You called create_tables() from an async context (running event loop detected).

In async contexts (FastAPI, pytest-asyncio, etc.), you MUST use the async methods:
  - create_tables() → create_tables_async()
  - close() → close_async()
  - _ensure_migration_tables() → _ensure_migration_tables_async()

See: sdk-users/apps/dataflow/troubleshooting/common-errors.md#DF-501
```

**Cause:** Called a sync method (`create_tables()`, `close()`) from within an async function or event loop.

**Solution:**
```python
# ❌ WRONG - Sync method in async context (FastAPI/pytest)
@app.on_event("startup")
async def startup():
    db.create_tables()  # ← RuntimeError: DF-501

# ✅ CORRECT - Use async methods in async context
@app.on_event("startup")
async def startup():
    await db.create_tables_async()  # ← Works!

# ✅ CORRECT - FastAPI lifespan pattern (recommended)
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.create_tables_async()
    yield
    # Shutdown
    await db.close_async()

app = FastAPI(lifespan=lifespan)

# ✅ CORRECT - pytest async fixtures
@pytest.fixture
async def db():
    db = DataFlow(":memory:")
    @db.model
    class User:
        id: str
        name: str
    await db.create_tables_async()
    yield db
    await db.close_async()
```

**Async Methods Available (v0.10.7+):**
| Sync Method | Async Method | When to Use |
|-------------|--------------|-------------|
| `create_tables()` | `create_tables_async()` | Table creation |
| `close()` | `close_async()` | Connection cleanup |
| `_ensure_migration_tables()` | `_ensure_migration_tables_async()` | Migration system |

**Detection:** DataFlow detects async context via `asyncio.get_running_loop()`. If a running loop exists, sync methods raise `RuntimeError` with DF-501.

**See:** `sdk-users/apps/dataflow/troubleshooting/common-errors.md#DF-501`

---

### DF-201: Invalid Connection

**Error Message:**
```
🔴 DF-201: Invalid Connection - Source output 'user_data' not found
```

**Cause:** Connected to non-existent node output.

**Solution:**
```python
# ✅ CORRECT - Use Inspector to find available outputs
from dataflow.platform.inspector import Inspector

inspector = Inspector(db)
inspector.workflow_obj = workflow.build()
outputs = inspector.node_schema("prepare_data")
print(f"Available outputs: {outputs}")

# ✅ CORRECT - Connect to existing output
workflow.add_connection("prepare_data", "result", "create_user", "data")

# ❌ WRONG - Non-existent output name
workflow.add_connection("prepare_data", "user_data", "create_user", "data")
```

## Using ErrorEnhancer with Inspector

Combine ErrorEnhancer with Inspector for powerful debugging:

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

# Use Inspector to validate before execution
inspector = Inspector(db)
inspector.workflow_obj = workflow.build()

# Get validation report
report = inspector.workflow_validation_report()
if not report['is_valid']:
    print(f"Errors: {report['errors']}")
    print(f"Warnings: {report['warnings']}")
    print(f"Suggestions: {report['suggestions']}")
    # ErrorEnhancer will provide detailed fixes for each error

# When execution fails, ErrorEnhancer provides rich error messages
try:
    results, run_id = runtime.execute(workflow.build())
except Exception as e:
    # ErrorEnhancer automatically enhances this exception
    # Shows: DF-101 with specific fixes for missing 'data' parameter
    pass
```

## ErrorEnhancer CLI Integration

ErrorEnhancer integrates with CLI validation tools:

```bash
# Validate workflow and get enhanced error messages
dataflow-validate workflow.py --output text

# Output shows DF-XXX codes with solutions:
# 🔴 DF-101: Missing Required Parameter 'data' in node 'create_user'
# 💡 Solution: Add 'data' parameter with required fields
#   workflow.add_node("UserCreateNode", "create_user", {
#       "data": {"name": "Alice", "email": "alice@example.com"}
#   })

# Auto-fix common issues
dataflow-validate workflow.py --fix
```

## Best Practices

### 1. Read Error Codes First
DF-XXX codes immediately identify the error category:
- **DF-1XX**: Check node parameters
- **DF-2XX**: Check connections
- **DF-3XX**: Check database schema
- **DF-4XX**: Check DataFlow configuration
- **DF-5XX**: Check runtime execution
- **DF-6XX**: Check model definitions
- **DF-7XX**: Check node generation
- **DF-8XX**: Check workflow structure

### 2. Use Suggested Solutions
ErrorEnhancer provides **code templates** - copy and modify them:
```python
# ErrorEnhancer shows:
# 💡 Solution 1: Add 'data' parameter
#   workflow.add_node("UserCreateNode", "create_user", {
#       "data": {"name": "Alice", "email": "alice@example.com"}
#   })

# ✅ Copy template and modify:
workflow.add_node("UserCreateNode", "create_user", {
    "data": {
        "name": user_input["name"],
        "email": user_input["email"]
    }
})
```

### 3. Check Documentation Links
ErrorEnhancer provides direct links to guides:
- **CreateNode vs UpdateNode**: `sdk-users/apps/dataflow/guides/create-vs-update.md`
- **Top 10 Errors**: `sdk-users/apps/dataflow/troubleshooting/top-10-errors.md`
- **Inspector Guide**: `sdk-users/apps/dataflow/guides/inspector.md`
- **Error Handling**: `sdk-users/apps/dataflow/guides/error-handling.md`

### 4. Combine with Inspector
Use Inspector for **proactive validation** before errors occur:
```python
# Validate before execution
inspector = Inspector(db)
inspector.workflow_obj = workflow.build()
report = inspector.workflow_validation_report()

if not report['is_valid']:
    # Fix errors before execution
    for error in report['errors']:
        print(error)  # ErrorEnhancer provides rich context
```

### 5. CI/CD Integration
Validate workflows in CI/CD pipelines:
```bash
# In CI/CD pipeline
dataflow-validate src/workflows/*.py --output json > validation-report.json

# Parse JSON report for DF-XXX error codes
# Fail build if critical errors (DF-1XX, DF-2XX, DF-6XX) found
```

## Performance Impact

ErrorEnhancer has **negligible performance impact**:
- **Build-time**: <1ms overhead per model
- **Runtime**: Only activates on exceptions (no overhead for successful executions)
- **Memory**: <100KB for error catalog

## Related Resources

- **[top-10-errors](../../../sdk-users/apps/dataflow/troubleshooting/top-10-errors.md)** - Quick fix guide for 90% of issues
- **[dataflow-inspector](dataflow-inspector.md)** - Proactive workflow validation
- **[create-vs-update](../../../sdk-users/apps/dataflow/guides/create-vs-update.md)** - CreateNode vs UpdateNode patterns
- **[dataflow-validation](dataflow-validation.md)** - Build-time validation modes

## When to Use This Skill

Use ErrorEnhancer when you:
- Encounter DataFlow exceptions during development
- Need to understand error causes quickly
- Want actionable solutions instead of stack traces
- Debug complex workflows with multiple nodes
- Integrate DataFlow validation in CI/CD
- Train team members on DataFlow best practices
