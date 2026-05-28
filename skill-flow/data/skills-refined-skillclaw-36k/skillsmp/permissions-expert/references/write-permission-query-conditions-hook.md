# write_permission_query_conditions Hook - Post-Write Validation

## Purpose

Validate that saved/updated documents satisfy custom conditions before committing to database.

## Location

In your doctype's `.py` file or registered in `hooks.py`

## Signature

```python
def get_write_permission_query_conditions(user=None, doctype=None, ptype="write"):
    """
    Return SQL WHERE conditions to validate written documents.

    Args:
        user: User performing the operation
        doctype: DocType being written
        ptype: Type of operation (create, write, submit, cancel, delete)

    Returns:
        str: SQL WHERE clause without the "WHERE" keyword
             Returns empty string "" to allow all operations

    Security Note:
        Automatically checked during has_permission() calls for write operations.
        Called AFTER database write but BEFORE commit.
        If validation fails, transaction is rolled back.
    """
    pass
```

## Important Notes

- **Automatically called via `has_permission()`** for write/create/submit/cancel/delete operations
- Called after DB write but before commit
- If check fails, transaction is rolled back
- Used for write operations: create, write, submit, cancel, delete
- When checking create/submit/cancel/delete, also checks "write" conditions
- Always escape dynamic values with `frappe.db.escape()`
- For delete operations, the check happens before the document is deleted from the database

## Checked Operations

- Create operations (`ptype="create"`)
- Update operations (`ptype="write"`)
- Submit operations (`ptype="submit"`)
- Cancel operations (`ptype="cancel"`)
- Delete operations (`ptype="delete"`)

## Examples

### Example 1: Prevent editing documents outside user's region

```python
def get_write_permission_query_conditions(user=None, doctype=None, ptype="write"):
    """Only allow editing documents from user's region."""
    if not user:
        user = frappe.session.user

    if user == "Administrator":
        return ""

    # Only apply to write operations
    if ptype not in ("write", "create"):
        return ""

    user_region = frappe.db.get_value("User", user, "region")
    if not user_region:
        return "1=0"  # No region assigned, deny all writes

    return f"`tabYour DocType`.`region` = {frappe.db.escape(user_region)}"
```

### Example 2: Prevent deletion of finalized documents

```python
def get_write_permission_query_conditions(user=None, doctype=None, ptype="write"):
    """Prevent deletion of finalized documents."""
    if not user:
        user = frappe.session.user

    if user == "Administrator":
        return ""

    # Only restrict delete operations
    if ptype == "delete":
        # Cannot delete finalized documents
        return "`tabYour DocType`.`status` != 'Finalized'"

    return ""
```

### Example 3: Restrict edits based on document age

```python
def get_write_permission_query_conditions(user=None, doctype=None, ptype="write"):
    """Prevent editing documents older than 30 days."""
    if not user:
        user = frappe.session.user

    if user == "Administrator":
        return ""

    if ptype == "write":
        return "DATEDIFF(NOW(), `tabYour DocType`.`creation`) <= 30"

    return ""
```

### Example 4: Allow only certain users to submit

```python
def get_write_permission_query_conditions(user=None, doctype=None, ptype="write"):
    """Only allow submitters to submit documents."""
    if not user:
        user = frappe.session.user

    if user == "Administrator":
        return ""

    if ptype == "submit":
        # Check if user is in the list of allowed submitters
        roles = frappe.get_roles(user)
        if "Submitter" not in roles:
            return "1=0"  # Deny all submits for non-submitters

    return ""
```

## Registration in hooks.py

```python
write_permission_query_conditions = {
    "Your DocType": "your_app.your_module.your_doctype.get_write_permission_query_conditions",
}
```

## Best Practices

1. **Always check ptype**: Different operations may need different conditions
2. **Escape user input**: Use `frappe.db.escape()` for all dynamic values
3. **Return empty string for no restrictions**: Don't return None
4. **Fail secure**: Return "1=0" when denying access
5. **Test rollback scenarios**: Ensure transactions roll back correctly when validation fails
6. **No need to manually call**: The check is automatically performed by `has_permission()` for write operations

## Common Use Cases

- Prevent modification of documents in certain status
- Restrict writes based on document age
- Enforce regional or departmental boundaries
- Prevent deletion of important records
- Implement custom approval workflows
