# has_website_permission Hook - Website/Portal Access

## Purpose

Control access to documents on the website/portal (not desk).

## Location

In your doctype's `.py` file or registered in `hooks.py`

## Signature

```python
def has_website_permission(doc, ptype="read", user=None):
    """
    Check if a website/portal user can access this document.
    
    Args:
        doc: Document instance
        ptype: Permission type (usually "read" for portal)
        user: User being checked (portal user)
        
    Returns:
        bool: True if user can access, False otherwise
    """
    pass
```

## Important Notes

- Only applies to website/portal access, not desk
- Website users are typically customers, suppliers, or other external users
- Use this for portal pages where documents are displayed to external users
- Does not require returning None (unlike `has_permission`)

## Examples

### Example 1: Allow customers to view their own orders

```python
def has_website_permission(doc, ptype="read", user=None):
    """Allow customers to view only their own orders on portal."""
    if not user:
        user = frappe.session.user
    
    # Get the customer linked to this user
    customer = frappe.db.get_value("Contact", {"user": user}, "parent_name")
    
    # Allow if this order belongs to the customer
    return doc.customer == customer
```

### Example 2: Allow access based on document status

```python
def has_website_permission(doc, ptype="read", user=None):
    """Only show published content on website."""
    return doc.published == 1
```

### Example 3: Check contact relationship

```python
def has_website_permission(doc, ptype="read", user=None):
    """Allow access if user is linked as a contact."""
    if not user:
        user = frappe.session.user
    
    # Check if user is linked to this document via Contact
    contact = frappe.db.get_value("Contact", {"user": user})
    if not contact:
        return False
    
    # Check if contact is linked to the document
    linked = frappe.db.exists("Dynamic Link", {
        "parent": contact,
        "link_doctype": doc.doctype,
        "link_name": doc.name
    })
    
    return bool(linked)
```

### Example 4: Allow access to shared documents

```python
def has_website_permission(doc, ptype="read", user=None):
    """Allow access to documents shared with user's organization."""
    if not user:
        user = frappe.session.user
    
    # Get user's organization (customer/supplier)
    contact = frappe.db.get_value("Contact", {"user": user})
    if not contact:
        return False
    
    org = frappe.db.get_value("Dynamic Link", {
        "parent": contact,
        "link_doctype": ["in", ["Customer", "Supplier"]]
    }, "link_name")
    
    # Check if document is for this organization
    return doc.get("customer") == org or doc.get("supplier") == org
```

### Example 5: Time-based access

```python
def has_website_permission(doc, ptype="read", user=None):
    """Only show documents during valid date range."""
    from frappe.utils import now_datetime, getdate
    
    if not doc.valid_from or not doc.valid_till:
        return False
    
    today = getdate()
    return doc.valid_from <= today <= doc.valid_till
```

## Registration in hooks.py

```python
has_website_permission = {
    "Your DocType": "your_app.your_module.your_doctype.has_website_permission"
}
```

## Best Practices

1. **Always check user is logged in**: Handle guest users appropriately
2. **Return boolean**: Unlike `has_permission`, always return True or False
3. **Use for portal views**: Only applies to website/portal, not desk
4. **Check relationships**: Verify user's connection to the document
5. **Consider status**: Published/approved status is common check
6. **Test with portal users**: Test with actual portal user accounts

## Common Patterns

### Pattern 1: Owner check

```python
return doc.user == user
```

### Pattern 2: Customer relationship

```python
customer = frappe.db.get_value("Contact", {"user": user}, "parent_name")
return doc.customer == customer
```

### Pattern 3: Status check

```python
return doc.status in ["Published", "Approved"]
```

### Pattern 4: Combined checks

```python
if doc.status != "Published":
    return False

customer = frappe.db.get_value("Contact", {"user": user}, "parent_name")
return doc.customer == customer
```

## Difference from has_permission

| Aspect | has_permission | has_website_permission |
|--------|---------------|----------------------|
| Scope | Desk access | Website/Portal access |
| Users | Internal users | External users (customers, suppliers) |
| Return values | True/False/None | True/False |
| Complexity | Multi-layered checks | Simple boolean check |
| When called | Desk operations | Portal page views |
