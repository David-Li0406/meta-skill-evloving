# has_permission Hook - Controller Permission Check

## Purpose

Implement custom document-level permission logic that cannot be expressed through role permissions or user permissions.

## Location

In your doctype's `.py` file or registered in `hooks.py`

## Signature

```python
def has_permission(doc, ptype=None, user=None, debug=False):
    """
    Custom permission check for individual documents.
    
    Args:
        doc: Document instance or document name (string)
        ptype: Permission type being checked (read, write, create, etc.)
        user: User being checked (defaults to current user)
        debug: Enable debug logging
        
    Returns:
        bool or None: 
            - True: Explicitly grant permission
            - False: Explicitly deny permission
            - None: No opinion, continue with other checks
    """
    pass
```

## Important Notes

- Return `None` to defer to other permission checks (recommended default)
- Return `False` to explicitly deny permission (overrides role permissions)
- Return `True` to explicitly grant permission (use with caution)
- Controllers can only deny permissions, not grant new ones that weren't already present via roles

## Examples

### Example 1: Allow access only to document owner

```python
# In your_doctype/your_doctype.py
def has_permission(doc, ptype=None, user=None, debug=False):
    """Only allow owner to access this document."""
    if not user:
        user = frappe.session.user
        
    # Allow if user is the owner
    if doc.owner == user:
        return True
        
    # Deny access to others
    return False
```

### Example 2: Allow managers to access team documents

```python
def has_permission(doc, ptype=None, user=None, debug=False):
    """Allow managers to access their team's documents."""
    if not user:
        user = frappe.session.user
    
    # Get user's team
    user_team = frappe.db.get_value("User", user, "team")
    
    # Allow if document belongs to user's team
    if doc.team == user_team:
        return None  # Defer to role permissions
        
    # Check if user is a manager with access to all teams
    if "Team Manager" in frappe.get_roles(user):
        return None  # Defer to role permissions
    
    # Otherwise deny
    return False
```

### Example 3: Restrict write access to draft documents

```python
def has_permission(doc, ptype=None, user=None, debug=False):
    """Restrict write access to draft documents."""
    if ptype in ("write", "delete") and doc.status != "Draft":
        # Only admins can modify non-draft documents
        return user == "Administrator"
    return None
```

### Example 4: Hierarchical access (team/department)

```python
def has_permission(doc, ptype=None, user=None, debug=False):
    """Allow access to documents in user's team hierarchy."""
    if not user:
        user = frappe.session.user
    
    user_teams = get_user_team_hierarchy(user)
    return doc.team in user_teams
```

### Example 5: Permission level filtering

```python
def has_permission(doc, ptype=None, user=None, debug=False):
    """Restrict edit access to sensitive fields based on role."""
    if ptype in ("write", "submit"):
        # Check if user has access to permlevel 1 (pricing fields)
        meta = frappe.get_meta(doc.doctype)
        accessible_permlevels = meta.get_permlevel_access(ptype, user=user)
        
        # If pricing fields were modified, check access
        if doc.has_value_changed("discount_percentage"):
            if 1 not in accessible_permlevels:
                frappe.throw("You don't have permission to modify pricing")
    
    return None
```

### Example 6: Conditional field visibility

```python
def has_permission(doc, ptype=None, user=None, debug=False):
    """Hide certain fields based on document status and user role."""
    if ptype == "read":
        roles = frappe.get_roles(user)
        
        # Hide internal comments from external users
        if "Customer" in roles and doc.status != "Completed":
            doc.internal_comments = None
        
        # Hide cost fields from non-finance users
        if "Accounts User" not in roles:
            doc.total_cost = None
            doc.profit_margin = None
    
    return None
```

### Example 7: Child table permissions

```python
# In parent doctype
def has_permission(doc, ptype=None, user=None, debug=False):
    """Control access to sensitive child tables."""
    if ptype == "write":
        # Check if user can edit the cost details child table
        meta = frappe.get_meta(doc.doctype)
        cost_field = meta.get_field("cost_details")
        
        if cost_field.permlevel > 0:
            accessible_permlevels = meta.get_permlevel_access("write", user=user)
            if cost_field.permlevel not in accessible_permlevels:
                # User can edit document but not cost details
                doc.flags.ignore_children_type = ["Cost Details"]
    
    return None
```

## Registration in hooks.py

```python
has_permission = {
    "Your DocType": "your_app.your_module.your_doctype.has_permission",
    "*": "your_app.permissions.global_permission_check",  # Applied to all doctypes
}
```

## Best Practices

1. **Always check Administrator first**: Administrator should bypass all checks
2. **Use None for deferral**: Return None to continue with other permission checks
3. **Document the logic**: Add clear docstrings explaining permission rules
4. **Keep it fast**: Avoid expensive database queries in this hook
5. **Test edge cases**: Test with different roles, owners, and document states
