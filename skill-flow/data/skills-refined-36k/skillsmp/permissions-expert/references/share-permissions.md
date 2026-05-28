# Share Permissions

## Overview

Share Permissions allow explicit document sharing between users. A user can share a specific document with another user, granting them access even if they don't have role-based permissions.

## Creating Share Permissions

```python
# Share a document
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

## Parameters

- **doctype**: DocType of the document to share
- **name**: Name of the specific document
- **user**: User to share with
- **read**: Allow read access (1 or 0)
- **write**: Allow write access (1 or 0)
- **share**: Allow user to share with others (1 or 0)
- **submit**: Allow submit access (1 or 0)
- **notify**: Send notification to user (1 or 0)

## Supported Permission Types

Share permissions only support:
- read
- write
- share
- submit
- email
- print

Other permission types (create, delete, cancel, amend) cannot be shared.

## Checking Share Permissions

```python
# Check if shared
is_shared = frappe.share.get_shared(
    doctype="Sales Order",
    user="user@example.com",
    rights=["read"],
    filters=[["share_name", "=", "SO-0001"]]
)
```

## Removing Share Permissions

```python
# Remove share
frappe.share.remove(
    doctype="Sales Order",
    name="SO-0001",
    user="user@example.com"
)
```

## Getting List of Shared Documents

```python
# Get all documents of a type shared with user
shared_docs = frappe.share.get_shared(
    doctype="Sales Order",
    user="user@example.com",
    rights=["read"]
)
```

## System Settings

Share permissions can be disabled globally:

System Settings > Disable Document Sharing

When disabled, users cannot share documents.

## How Share Permissions Work in Permission Flow

1. Checked after role permissions and User Permissions
2. If role permission check fails, system checks if document is shared
3. If shared with appropriate rights, access is granted
4. Share permissions are checked in `has_permission()` unless `ignore_share_permissions=True`

## Example Use Cases

### Use Case 1: Share a draft with reviewer

```python
# User creates a draft and shares with manager for review
frappe.share.add(
    doctype="Sales Order",
    name="SO-0001",
    user="manager@example.com",
    read=1,
    write=1,
    submit=0,
    notify=1
)
```

### Use Case 2: Temporary access

```python
# Grant temporary access to a consultant
frappe.share.add(
    doctype="Project",
    name="PRO-0001",
    user="consultant@example.com",
    read=1,
    write=0,
    notify=1
)

# Later remove access
frappe.share.remove(
    doctype="Project",
    name="PRO-0001",
    user="consultant@example.com"
)
```

### Use Case 3: Cross-department collaboration

```python
# HR shares employee record with Finance for payroll
frappe.share.add(
    doctype="Employee",
    name="EMP-0001",
    user="finance@example.com",
    read=1,
    write=0,
    notify=1
)
```

## DocShare DocType

Share permissions are stored in the "DocShare" doctype with fields:
- user: User to share with
- share_doctype: DocType being shared
- share_name: Document name being shared
- read, write, share, submit: Permission flags
- everyone: If checked, shared with all users (rare)

## Checking if Sharing is Enabled

```python
sharing_enabled = not frappe.get_system_settings("disable_document_sharing")
```

## Validations

1. **User must have System User role**: Only desk users can receive shared documents
2. **Share permission needed**: User sharing must have "share" permission on the document
3. **Supported permission types**: Only read, write, share, submit, email, print can be shared

## Best Practices

1. **Use for collaboration**: Ideal for temporary or cross-functional access
2. **Not for regular access**: Use roles and User Permissions for regular access patterns
3. **Monitor shares**: Keep track of who has access to sensitive documents
4. **Clean up**: Remove shares when no longer needed
5. **Notify users**: Use notify=1 to inform users of shared documents

## UI Access

Users can share documents via:
1. Document menu > Share
2. Select user and permissions
3. Click Share

Users can see shared documents in:
- Shared With Me workspace
- Standard list views (if they have share access)

## Limitations

1. **Cannot share create permission**: Users cannot be granted create access via sharing
2. **Cannot share delete permission**: Delete access cannot be shared
3. **Requires System User**: Portal users cannot receive shared documents
4. **No bulk sharing**: Must share documents individually (no folder/tag-based sharing)

## Integration with has_permission

```python
# In has_permission flow
if not perm:
    # Check if document is shared
    if ptype in ("read", "write", "share", "submit", "email", "print"):
        perm = false_if_not_shared()
```

## Debugging Share Permissions

```python
# Check shares for a document
shares = frappe.get_all("DocShare", filters={
    "share_doctype": "Sales Order",
    "share_name": "SO-0001"
}, fields=["user", "read", "write", "share", "submit"])

# Check with debug
frappe.has_permission("Sales Order", "read", "SO-0001", 
                      user="user@example.com", debug=True)
```

## Common Patterns

### Pattern 1: Share with team

```python
team_members = ["user1@example.com", "user2@example.com", "user3@example.com"]
for member in team_members:
    frappe.share.add("Project", "PRO-0001", member, read=1, write=1, notify=1)
```

### Pattern 2: Share based on document field

```python
def after_insert(self):
    """Share document with assigned user"""
    if self.assigned_to:
        frappe.share.add(
            self.doctype,
            self.name,
            self.assigned_to,
            read=1,
            write=1,
            notify=1
        )
```

### Pattern 3: Remove all shares

```python
def before_cancel(self):
    """Remove all shares when document is cancelled"""
    frappe.db.delete("DocShare", {
        "share_doctype": self.doctype,
        "share_name": self.name
    })
```
