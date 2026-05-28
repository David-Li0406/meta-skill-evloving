---
name: nodes-admin-reference
description: "Admin nodes reference (AdminUser, AdminDB, Role, Permission). Use when asking 'admin node', 'AdminUser', 'AdminDB', 'role management', or 'permission check'."
---

# Admin Nodes Reference

Complete reference for administrative and access control nodes.

> **Skill Metadata**
> Category: `nodes`
> Priority: `LOW`
> SDK Version: `0.9.25+`
> Related Skills: [`nodes-quick-index`](nodes-quick-index.md)
> Related Subagents: `pattern-expert` (admin workflows)

## Quick Reference

```python
from kailash.nodes.admin import (
    UserManagementNode,
    RoleManagementNode,
    PermissionCheckNode,
    AccessControlNode
)
```

## User Management

### UserManagementNode
```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

workflow.add_node("UserManagementNode", "user_mgmt", {
    "operation": "create",
    "user_data": {
        "username": "john_doe",
        "email": "john@example.com",
        "roles": ["user", "editor"]
    }
})
```

## Role Management

### RoleManagementNode
```python
workflow.add_node("RoleManagementNode", "role_mgmt", {
    "operation": "assign",
    "user_id": "user_123",
    "role": "admin"
})
```

## Permission Checking

### PermissionCheckNode
```python
workflow.add_node("PermissionCheckNode", "perm_check", {
    "user_id": "user_123",
    "resource": "documents",
    "action": "write"
})
```

## Access Control

### AccessControlNode
```python
workflow.add_node("AccessControlNode", "access_control", {
    "operation": "verify",
    "user_id": "user_123",
    "resource_id": "doc_456",
    "required_permission": "read"
})
```

## Related Skills

- **Node Index**: [`nodes-quick-index`](nodes-quick-index.md)

## Documentation

- **Admin Nodes**: [`sdk-users/2-core-concepts/nodes/10-admin-nodes.md`](../../../../sdk-users/2-core-concepts/nodes/10-admin-nodes.md)
- **Admin Quick Reference**: [`sdk-users/2-core-concepts/nodes/admin-nodes-quick-reference.md`](../../../../sdk-users/2-core-concepts/nodes/admin-nodes-quick-reference.md)

<!-- Trigger Keywords: admin node, AdminUser, AdminDB, role management, permission check, UserManagementNode, RoleManagementNode -->
