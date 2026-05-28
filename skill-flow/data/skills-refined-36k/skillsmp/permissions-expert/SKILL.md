---
name: permissions-expert
description: Expert guidance on Frappe permissions system including permission evaluation flow, extension hooks (has_permission, permission_query_conditions, write_permission_query_conditions, has_website_permission, filter_workflow_transitions, has_workflow_action_permission), role-based permissions, user permissions, share permissions, permission levels, and workflow permissions. Use when implementing custom permission logic, troubleshooting permission issues, understanding permission query conditions, working with child table permissions, virtual DocType permissions, workflow transition filtering, approval routing, or debugging access control problems.
---

# Frappe Permissions Expert

This skill provides comprehensive guidance for understanding and extending Frappe's permission system.

## Overview

Frappe's permission system is multi-layered and evaluates permissions in a specific order:

1. **Administrator Check**: Administrator user bypasses all permission checks
2. **Role-Based Permissions**: DocType permissions configured through Permission Manager
3. **Controller Permissions**: Custom `has_permission` hooks in doctypes
4. **User Permissions**: Document-level restrictions based on user-specific rules
5. **Permission Query Conditions**: SQL-based filters for list views and reports
6. **Share Permissions**: Explicit document sharing between users

## Permission Types

Frappe supports the following permission types (ptypes):

```python
rights = (
    "select",    # View in list (limited fields)
    "read",      # Full read access
    "write",     # Edit existing documents
    "create",    # Create new documents
    "delete",    # Delete documents
    "submit",    # Submit submittable documents
    "cancel",    # Cancel submitted documents
    "amend",     # Amend cancelled documents
    "print",     # Print documents
    "email",     # Email documents
    "report",    # Access reports
    "import",    # Import documents
    "export",    # Export documents
    "share",     # Share documents with others
)
```

## Quick Reference

### Main Permission Check Function

```python
frappe.has_permission(
    doctype="DocType Name",
    ptype="read",              # Permission type to check
    doc=None,                  # Optional: specific document instance
    user=None,                 # Optional: defaults to current user
    raise_exception=True,      # Display error message if False
    parent_doctype=None,       # Required for child doctypes
    debug=False,               # Enable debug logging
    ignore_share_permissions=False
)
```

### Key Concepts

- **Child Tables**: Don't have their own permissions; permissions are checked on the parent document
- **Virtual DocTypes**: Permission query conditions don't apply; only `has_permission` hook and role permissions apply
- **Permission Levels**: Provide field-level access control within a document (permlevel 0, 1, 2, etc.)

## Extension Hooks

Frappe provides seven main hooks for extending permission logic:

### 1. `has_permission` - Controller Permission Check

**Purpose**: Implement custom document-level permission logic

**Location**: In your doctype's `.py` file or registered in `hooks.py`

**Signature**:
```python
def has_permission(doc, ptype=None, user=None, debug=False):
    """
    Returns:
        bool or None:
            - True: Explicitly grant permission
            - False: Explicitly deny permission
            - None: No opinion, continue with other checks
    """
```

**Important Notes**:
- Return `None` to defer to other permission checks (recommended default)
- Return `False` to explicitly deny permission (overrides role permissions)
- Return `True` to explicitly grant permission (use with caution)

**When to read:** See [references/has-permission-hook.md](references/has-permission-hook.md) when implementing document-level permission logic with 7 detailed examples covering owner access, team hierarchies, status restrictions, and more.

### 2. `permission_query_conditions` - List View Filtering and Document Access

**Purpose**: Return SQL WHERE conditions to filter documents in list views and validate individual document access

**Location**: In your doctype's `.py` file or registered in `hooks.py`

**Signature**:
```python
def get_permission_query_conditions(user=None, doctype=None):
    """
    Returns:
        str: SQL WHERE clause without the "WHERE" keyword
             Returns empty string "" to allow all documents
    """
```

**Security**: Always escape dynamic values with `frappe.db.escape()`

**Important**: These conditions are checked both in list views AND when accessing individual documents via `has_permission()` for read/select operations.

**When to read:** See [references/permission-query-conditions-hook.md](references/permission-query-conditions-hook.md) when implementing list filtering or document access validation with 7 examples including company filtering, role-based regions, time-based access, and multi-tenant patterns.

### 3. `write_permission_query_conditions` - Post-Write Validation

**Purpose**: Validate that saved/updated documents satisfy custom conditions before committing to database

**Location**: In your doctype's `.py` file or registered in `hooks.py`

**Signature**:
```python
def get_write_permission_query_conditions(user=None, doctype=None, ptype="write"):
    """
    Return SQL WHERE conditions to validate written documents.

    This is automatically called during has_permission() checks
    for write/create/submit/cancel/delete operations.

    Checked AFTER database write but BEFORE commit.
    If validation fails, transaction is rolled back.
    """
```

**When to read:** See [references/write-permission-query-conditions-hook.md](references/write-permission-query-conditions-hook.md) when validating writes before commit with examples for regional restrictions, document age limits, and status-based validation.

### 4. Server Scripts - Permission Query

**Purpose**: Define permission query conditions using Server Scripts (Python code in the UI)

**Location**: Created through Frappe UI at `/app/server-script`

**Script Type**: "Permission Query"

**When to read:** See [references/server-scripts.md](references/server-scripts.md) when prototyping permission logic via UI before moving to code, with examples for department filtering and role-based access.

### 5. `has_website_permission` - Website/Portal Access

**Purpose**: Control access to documents on the website/portal (not desk)

**Location**: In your doctype's `.py` file or registered in `hooks.py`

**When to read:** See [references/has-website-permission-hook.md](references/has-website-permission-hook.md) when implementing portal/website access control with examples for customer orders, published content, and contact relationships.

## Workflow Permission Hooks

Frappe provides two additional hooks specifically for workflow-based permissions:

### 6. `filter_workflow_transitions` - Custom Transition Filtering

**Purpose**: Filter and customize the list of available workflow transitions based on custom logic

**Location**: Registered in `hooks.py`

**Use Cases**:
- Hide specific transitions based on document field values
- Apply time-based or date-based restrictions
- Implement dynamic transition visibility

### 7. `has_workflow_action_permission` - Action-Level Permission

**Purpose**: Control which users should receive workflow action notifications and have permission to execute specific actions

**Location**: Registered in `hooks.py`

**Use Cases**:
- Implement approval hierarchies
- Department or region-based approval routing
- Amount-based approval limits

**When to read:** See [references/workflow-permission-hooks.md](references/workflow-permission-hooks.md) when implementing workflow transition filtering or approval routing with 10+ examples covering hierarchical approvals, time restrictions, and regional routing.

## User Permissions

User Permissions restrict access to specific document values for link fields.

**Creating User Permissions**:
```python
from frappe.permissions import add_user_permission

add_user_permission(
    doctype="Company",
    name="Company A",
    user="user@example.com",
    applicable_for="Sales Order",  # Optional
    is_default=1,                  # Optional
    ignore_permissions=True        # Optional
)
```

**Use Cases**:
- Restrict sales users to their own territory
- Limit employees to their branch/department
- Multi-company access control

**When to read:** See [references/user-permissions.md](references/user-permissions.md) when implementing document-level restrictions using User Permissions with comprehensive examples for multi-company, territory, and department-based access.

## Share Permissions

Documents can be explicitly shared with specific users:

```python
frappe.share.add(
    doctype="Sales Order",
    name="SO-0001",
    user="user@example.com",
    read=1,
    write=1,
    share=0,
    submit=0,
    notify=1
)
```

**When to read:** See [references/share-permissions.md](references/share-permissions.md) when implementing explicit document sharing between users with examples for collaboration, temporary access, and cross-department workflows.

## Permission Levels

Permission levels provide field-level access control:

- Each field can have a permlevel (0, 1, 2, etc.)
- Users must have role permission with that permlevel to see/edit the field
- Permlevel 0 is default and always checked

**When to read:** See [references/permission-levels.md](references/permission-levels.md) when implementing field-level access control with examples for hiding pricing, cost fields, and internal notes from specific roles.

## Best Practices

### Security

1. **Always Escape User Input**: Use `frappe.db.escape()` when building SQL conditions
2. **Fail Secure**: Default to denying access when in doubt
3. **Validate Hook Returns**: Ensure hooks return expected types
4. **Test Permission Boundaries**: Test with users having minimal permissions
5. **Avoid Side Effects**: Permission checks should be read-only

### Performance

1. **Optimize SQL Conditions**: Use indexed columns in WHERE clauses
2. **Cache User Data**: Cache frequently accessed user properties
3. **Minimize Hook Complexity**: Keep permission logic simple and fast
4. **Use Appropriate Hooks**:
   - Use `permission_query_conditions` for list filtering
   - Use `has_permission` for complex document-specific logic

### Maintainability

1. **Document Permission Logic**: Add docstrings explaining the rules
2. **Separate Concerns**: Keep permission logic separate from business logic
3. **Use Constants**: Define permission-related constants
4. **Consistent Return Values**: Be explicit about what you're returning

**When to read:** See [references/best-practices.md](references/best-practices.md) when writing production-ready permission code with comprehensive guidelines for security, performance, and maintainability.

## Debugging Permissions

### Enable Debug Mode

```python
# In Python
result = frappe.has_permission("DocType", "read", doc, debug=True)
# Logs will show the permission evaluation flow

# Or enable globally
frappe.conf.developer_mode = 1
```

### Check Permission Debug Logs

```python
# After permission check with debug=True
logs = frappe.local.permission_debug_log
for log in logs:
    print(log)
```

**When to read:** See [references/debugging.md](references/debugging.md) when troubleshooting permission issues with comprehensive debugging workflows, common scenarios, and logging techniques.

## Common Issues and Solutions

**When to read:** See [references/common-issues.md](references/common-issues.md) when facing permission problems with detailed troubleshooting for:

- User Can't See Documents in List View
- Can See Document in List but Can't Open
- Permission Query Hook Not Working
- Write Operations Fail Silently
- Virtual DocType Permission Issues
- Share Permissions Not Working
- Administrator Not Seeing All Documents

## Common Patterns

**When to read:** See [references/common-patterns.md](references/common-patterns.md) for 15 ready-to-use permission patterns including:

- Owner-Only Access
- Role-Based Region Filtering
- Hierarchical Access (Team/Department)
- Status-Based Restrictions
- Time-Based Access
- Multi-Tenant Access
- Permission Level Filtering
- Child Table Permissions
- Conditional Field Visibility
- Combined Role and Territory Access

## Testing Permission Hooks

**When to read:** See [references/testing.md](references/testing.md) when writing unit and integration tests for permission logic with comprehensive examples and patterns.

## Migration Guide

**When to read:** See [references/migration-guide.md](references/migration-guide.md) for a step-by-step guide when adding custom permissions to existing DocTypes.

## Core Implementation Files

Key files in Frappe codebase:
- `/frappe/permissions.py` - Main permission system
- `/frappe/model/db_query.py` - Permission query integration
- `/frappe/model/document.py` - Document lifecycle and permission checks
- `/frappe/core/doctype/user_permission/` - User permission management

## Usage

When working with permissions:

1. **Identify the requirement**: What access control is needed?
2. **Choose appropriate hook**: Select based on use case
3. **Reference appropriate guide**: Use reference files for detailed patterns
4. **Follow best practices**: Security, performance, maintainability
5. **Test thoroughly**: With different roles and edge cases
6. **Debug when needed**: Use debug mode and logging

## Important Notes

- Administrator always bypasses all permission checks
- Permission query conditions are applied to both list views AND individual document access
- Virtual doctypes don't support permission query conditions
- Child tables inherit parent document permissions
- Always escape user input in SQL conditions to prevent SQL injection
- Permission checks should be read-only operations
