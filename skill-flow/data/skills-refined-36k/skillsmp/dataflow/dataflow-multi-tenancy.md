---
name: dataflow-multi-tenancy
description: "Multi-tenant patterns with DataFlow. Use when multi-tenant, tenant isolation, SaaS, __dataflow__ config, or tenant_id field."
---

# DataFlow Multi-Tenancy

Automatic tenant isolation for SaaS applications using DataFlow enterprise features.

> **Skill Metadata**
> Category: `dataflow`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+ / DataFlow 0.6.0`
> Related Skills: [`dataflow-models`](#), [`dataflow-crud-operations`](#)
> Related Subagents: `dataflow-specialist` (enterprise architecture)

## Quick Reference

- **Enable**: `__dataflow__ = {'multi_tenant': True}`
- **Auto-Adds**: `tenant_id` field to model
- **Auto-Filter**: All queries filtered by current tenant
- **Validation**: Prevents cross-tenant access

## Core Pattern

```python
from dataflow import DataFlow

db = DataFlow()

@db.model
class Order:
    customer_id: int
    total: float
    status: str = 'pending'

    __dataflow__ = {
        'multi_tenant': True,     # Automatic tenant isolation
        'soft_delete': True,      # Preserve deleted data
        'audit_log': True         # Track all changes
    }

# Automatically adds tenant_id field
# All queries filtered by tenant automatically

workflow = WorkflowBuilder()
workflow.add_node("OrderCreateNode", "create", {
    "customer_id": 123,
    "total": 250.00,
    "tenant_id": "tenant_abc"  # Automatic isolation
})

# List only shows current tenant's orders
workflow.add_node("OrderListNode", "list", {
    "filter": {"status": "completed"},
    "tenant_id": "tenant_abc"  # Filters automatically
})
```

## Multi-Tenant Features

- **Tenant Isolation**: Automatic filtering by tenant_id
- **Data Partitioning**: Separate data per tenant
- **Security**: Prevents cross-tenant access
- **Audit Trails**: Track tenant-specific changes

## Documentation References

### Primary Sources
- **README**: [`sdk-users/apps/dataflow/README.md`](../../../../sdk-users/apps/dataflow/README.md#L841-L860)
- **Multi-Tenant Guide**: [`sdk-users/apps/dataflow/docs/advanced/multi-tenant.md`](../../../../sdk-users/apps/dataflow/docs/advanced/multi-tenant.md)
- **Enterprise Multi-Tenant**: [`sdk-users/apps/dataflow/docs/enterprise/multi-tenant.md`](../../../../sdk-users/apps/dataflow/docs/enterprise/multi-tenant.md)

### Specialist Reference
- **DataFlow Specialist**: [`.claude/skills/dataflow-specialist.md`](../../dataflow-specialist.md#L296-L303)

## Quick Tips

- Add `multi_tenant: True` to `__dataflow__`
- tenant_id automatically added to model
- All queries filtered by tenant
- Prevents cross-tenant access
- Perfect for SaaS applications

## Keywords for Auto-Trigger

<!-- Trigger Keywords: multi-tenant, tenant isolation, SaaS, __dataflow__ config, tenant_id, multi-tenancy, tenant data -->
