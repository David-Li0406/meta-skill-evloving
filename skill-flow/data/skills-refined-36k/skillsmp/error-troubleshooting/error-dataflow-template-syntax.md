---
name: error-dataflow-template-syntax
description: "Fix DataFlow template syntax errors. Use when encountering '{{}}' template errors, 'invalid literal for int()', 'template validation failed', or DataFlow parameter validation errors with template syntax."
---

# Error: DataFlow Template Syntax

Fix template syntax errors in DataFlow - using wrong `{{}}` syntax instead of correct `${}` or connections.

> **Skill Metadata**
> Category: `cross-cutting` (error-resolution)
> Priority: `HIGH`
> SDK Version: `0.5.0+`
> Related Skills: [`dataflow-quickstart`](../../02-dataflow/dataflow-quickstart.md), [`connection-patterns`](../../01-core-sdk/connection-patterns.md)
> Related Subagents: `dataflow-specialist` (DataFlow patterns)

## The Error

### Common Error Message
```
invalid literal for int() with base 10: '{{customer.id}}'
ValidationError: Template syntax error
Parameter validation failed for '{{...}}'
```

### Root Cause
**Kailash template syntax is `${}` NOT `{{}}`**. DataFlow node parameters should use **connections**, not template syntax.

## Quick Fix

### ❌ WRONG: Using {{}} Template Syntax
```python
from dataflow import DataFlow
from kailash.workflow.builder import WorkflowBuilder

db = DataFlow()

@db.model
class Order:
    customer_id: int
    total: float

workflow = WorkflowBuilder()
workflow.add_node("OrderCreateNode", "create", {
    "customer_id": "{{customer.id}}",  # ❌ ERROR! Wrong syntax
    "total": 100.0
})
```

### ✅ FIX: Use Connections Instead
```python
from dataflow import DataFlow
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

db = DataFlow()

@db.model
class Order:
    customer_id: int
    total: float

workflow = WorkflowBuilder()

# Create customer first
workflow.add_node("CustomerCreateNode", "customer", {
    "name": "Alice",
    "email": "alice@example.com"
})

# Create order with connection (not template)
workflow.add_node("OrderCreateNode", "create", {
    "total": 100.0
    # customer_id comes from connection
})

# ✅ CORRECT: Use explicit connection
workflow.add_connection("customer", "id", "create", "customer_id")

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

## Template Syntax Reference

### Kailash SDK Template Syntax (Core SDK Only)
```python
# ✅ Kailash uses ${} syntax (in specific contexts)
"${node.output}"          # Valid in some nodes
"${prepare.result}"       # Valid reference

# ❌ NOT {{}} syntax
"{{node.output}}"         # INVALID
"{{ node.output }}"       # INVALID
"{node.output}"           # Missing $
```

**Important**: For DataFlow, **use connections instead of templates**

## Why DataFlow Doesn't Use Templates

DataFlow nodes expect **native Python types**:
- `customer_id: int` expects `int`, not `str` template
- Templates would bypass type validation
- Connections preserve type safety

## Complete Example

### ❌ Wrong Code (Template Approach)
```python
db = DataFlow()

@db.model
class Order:
    customer_id: int
    total: float

workflow = WorkflowBuilder()
workflow.add_node("OrderCreateNode", "create", {
    "customer_id": "{{customer.id}}",  # ❌ Template causes int() error
    "total": "{{cart.total}}"          # ❌ Template breaks validation
})
```

### ✅ Correct Code (Connection Approach)
```python
db = DataFlow()

@db.model
class Order:
    customer_id: int
    total: float

workflow = WorkflowBuilder()

# Source nodes
workflow.add_node("CustomerReadNode", "customer", {
    "id": 123
})

workflow.add_node("PythonCodeNode", "cart", {
    "code": "result = {'total': 150.50}"
})

# Target node (DataFlow)
workflow.add_node("OrderCreateNode", "create", {})

# ✅ Use connections for dynamic values
workflow.add_connection("customer", "id", "create", "customer_id")
workflow.add_connection("cart", "result.total", "create", "total")

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

## Related Patterns

- **DataFlow basics**: [`dataflow-quickstart`](../../02-dataflow/dataflow-quickstart.md)
- **Connection patterns**: [`connection-patterns`](../../01-core-sdk/connection-patterns.md)
- **DataFlow models**: [`dataflow-models`](../../02-dataflow/dataflow-models.md)

## When to Escalate to Subagent

Use `dataflow-specialist` subagent when:
- Complex DataFlow architecture
- Enterprise DataFlow patterns
- Migration system usage
- Performance optimization

## Documentation References

### Primary Sources
- **DataFlow Specialist**: [`.claude/agents/frameworks/dataflow-specialist.md` (lines 30-33)](../../../../.claude/agents/frameworks/dataflow-specialist.md#L30-L33)
- **Template Syntax**: [`sdk-users/apps/dataflow/CLAUDE.md` (search for "template")](../../../../sdk-users/apps/dataflow/CLAUDE.md)

### Related Documentation
- **DataFlow README**: [`sdk-users/apps/dataflow/README.md`](../../../../sdk-users/apps/dataflow/README.md)
- **Connection Guide**: [`sdk-users/2-core-concepts/cheatsheet/005-connection-patterns.md`](../../../../sdk-users/2-core-concepts/cheatsheet/005-connection-patterns.md)

## Quick Tips

- 💡 **No templates in DataFlow**: Use connections instead
- 💡 **Type safety**: Connections preserve Python types
- 💡 **If you see {{}}**: Replace with connection
- 💡 **Core SDK uses ${}**: But DataFlow prefers connections

<!-- Trigger Keywords: {{}} template error, invalid literal for int, template validation failed, DataFlow parameter error, template syntax error, DataFlow template, {{customer.id}} error, template issue DataFlow -->
