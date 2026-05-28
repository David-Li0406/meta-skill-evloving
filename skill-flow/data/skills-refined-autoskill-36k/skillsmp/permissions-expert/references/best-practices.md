# Best Practices for Frappe Permissions

## Table of Contents

- [Security Best Practices](#security-best-practices)
- [Performance Best Practices](#performance-best-practices)
- [Maintainability Best Practices](#maintainability-best-practices)
- [Testing Best Practices](#testing-best-practices)
- [Code Organization Best Practices](#code-organization-best-practices)
- [Common Anti-Patterns to Avoid](#common-anti-patterns-to-avoid)
- [Security Checklist](#security-checklist)

## Security Best Practices

### 1. Always Escape User Input

When building SQL conditions, use `frappe.db.escape()`:

```python
# WRONG - SQL injection vulnerability
return f"`tabDoc`.`owner` = '{user}'"

# CORRECT - Properly escaped
return f"`tabDoc`.`owner` = {frappe.db.escape(user)}"
```

### 2. Fail Secure

Default to denying access when in doubt:

```python
# If no conditions match, deny access
return "1=0"  # SQL condition that's always false
```

### 3. Validate Hook Returns

Ensure hooks return expected types:

```python
# has_permission should return bool or None
# permission_query_conditions should return string

def get_permission_query_conditions(user):
    # WRONG: returns None when it should return empty string
    if administrator:
        return None
    
    # CORRECT: returns empty string for no restrictions
    if administrator:
        return ""
```

### 4. Test Permission Boundaries

Test with users having minimal permissions:
- Users with no roles
- Users with only read access
- Users with User Permissions
- Portal users

### 5. Avoid Side Effects

Permission checks should be read-only, no database modifications:

```python
# WRONG - modifies data
def has_permission(doc, ptype, user):
    doc.last_checked_by = user
    doc.save()
    return True

# CORRECT - read-only check
def has_permission(doc, ptype, user):
    return doc.owner == user
```

### 6. Check Administrator First

Administrator should always bypass checks:

```python
def has_permission(doc, ptype, user):
    # ALWAYS check Administrator first
    if user == "Administrator":
        return True
    
    # Your custom logic
    pass
```

## Performance Best Practices

### 1. Optimize SQL Conditions

Use indexed columns in WHERE clauses:

```python
# Better - uses indexed field
return f"`tabDoc`.`company` = {frappe.db.escape(company)}"

# Slower - function on indexed field
return f"DATE(`tabDoc`.`creation`) = CURDATE()"
```

### 2. Cache User Data

Cache frequently accessed user properties:

```python
@frappe.whitelist()
def get_permission_query_conditions(user=None):
    # Cache user's company
    user_company = frappe.cache.hget("user_companies", user, 
        lambda: frappe.db.get_value("User", user, "company"))
    return f"`tabDoc`.`company` = {frappe.db.escape(user_company)}"
```

### 3. Minimize Hook Complexity

Keep permission logic simple and fast:

```python
# GOOD - simple check
def has_permission(doc, ptype, user):
    return doc.owner == user

# BAD - expensive operations
def has_permission(doc, ptype, user):
    # Multiple database queries
    user_teams = frappe.get_all("Team", filters={"user": user})
    for team in user_teams:
        team_members = frappe.get_all("Team Member", filters={"parent": team.name})
        # More nested queries...
    return some_complex_logic
```

### 4. Use Appropriate Hooks

- Use `permission_query_conditions` for list filtering
- Use `has_permission` for complex document-specific logic

```python
# List filtering - use permission_query_conditions
def get_permission_query_conditions(user):
    return f"`tabDoc`.`company` = {frappe.db.escape(get_user_company(user))}"

# Document-specific logic - use has_permission
def has_permission(doc, ptype, user):
    # Check if user is in document's team
    return user in doc.get_team_members()
```

## Maintainability Best Practices

### 1. Document Permission Logic

Add docstrings explaining the rules:

```python
def has_permission(doc, ptype, user):
    """
    Permission Rules:
    - Owners can always read/write their documents
    - Managers can read all documents in their department
    - Directors can read/write all documents
    """
    if doc.owner == user:
        return True
    
    if "Manager" in frappe.get_roles(user):
        return doc.department == get_user_department(user)
    
    if "Director" in frappe.get_roles(user):
        return True
    
    return False
```

### 2. Separate Concerns

Keep permission logic separate from business logic:

```python
# GOOD - separate files/modules
# permissions.py
def has_permission(doc, ptype, user):
    return check_team_access(doc, user)

# utils.py  
def check_team_access(doc, user):
    user_teams = get_user_teams(user)
    return doc.team in user_teams

# BAD - mixed concerns
def has_permission(doc, ptype, user):
    # Business logic mixed in
    if doc.status == "Draft":
        doc.calculate_totals()
    return doc.owner == user
```

### 3. Use Constants

Define permission-related constants:

```python
MANAGER_ROLES = ["Sales Manager", "Purchase Manager", "HR Manager"]
READONLY_STATUSES = ["Approved", "Finalized", "Closed"]
EDITABLE_STATUSES = ["Draft", "Pending"]

def has_permission(doc, ptype, user):
    if ptype == "write" and doc.status in READONLY_STATUSES:
        return "Manager" in frappe.get_roles(user)
    return None
```

### 4. Consistent Return Values

Be explicit about what you're returning:

```python
# Clear intent
def has_permission(doc, ptype, user):
    if is_manager:
        return None  # Defer to role permissions
    elif doc.owner == user:
        return True  # Explicitly allow
    else:
        return False  # Explicitly deny
```

### 5. Version Control

Track permission changes in git with clear commit messages:

```
git commit -m "Add permission query conditions for company-based filtering

- Filter Sales Orders by user's company
- Managers see all companies
- Regular users see only their company
- Fixes issue #123"
```

## Testing Best Practices

### 1. Test Different Roles

```python
def test_permissions(self):
    # Test as regular user
    frappe.set_user("user@example.com")
    self.assertFalse(frappe.has_permission("DocType", "write", doc))
    
    # Test as manager
    frappe.set_user("manager@example.com")
    self.assertTrue(frappe.has_permission("DocType", "write", doc))
    
    # Test as admin
    frappe.set_user("Administrator")
    self.assertTrue(frappe.has_permission("DocType", "write", doc))
```

### 2. Test Edge Cases

- Empty values
- None values
- Non-existent users
- Disabled users
- Users with no roles

### 3. Test List Views

```python
def test_list_filtering(self):
    # Create documents in different companies
    doc_a = create_doc(company="Company A")
    doc_b = create_doc(company="Company B")
    
    # User with Company A permission
    frappe.set_user("user.a@example.com")
    docs = frappe.get_all("DocType")
    
    # Should only see Company A documents
    self.assertEqual(len(docs), 1)
    self.assertEqual(docs[0].name, doc_a.name)
```

## Code Organization Best Practices

### 1. Group Related Permissions

```python
# permissions.py
def has_company_permission(doc, user):
    """Check company-based permission."""
    pass

def has_territory_permission(doc, user):
    """Check territory-based permission."""
    pass

def has_permission(doc, ptype, user):
    """Main permission check."""
    if not has_company_permission(doc, user):
        return False
    if not has_territory_permission(doc, user):
        return False
    return None
```

### 2. Reuse Permission Logic

```python
# common_permissions.py
def check_owner_or_manager(doc, user):
    """Reusable check for owner or manager."""
    if doc.owner == user:
        return True
    if "Manager" in frappe.get_roles(user):
        return True
    return False

# sales_order.py
def has_permission(doc, ptype, user):
    return check_owner_or_manager(doc, user)

# purchase_order.py  
def has_permission(doc, ptype, user):
    return check_owner_or_manager(doc, user)
```

## Common Anti-Patterns to Avoid

### 1. Forgetting to Escape SQL

```python
# WRONG
return f"`tabDoc`.`owner` = '{user}'"

# RIGHT
return f"`tabDoc`.`owner` = {frappe.db.escape(user)}"
```

### 2. Returning None Instead of Empty String

```python
# WRONG
def get_permission_query_conditions(user):
    if user == "Administrator":
        return None  # Will break!

# RIGHT
def get_permission_query_conditions(user):
    if user == "Administrator":
        return ""  # Correct
```

### 3. Expensive Operations in Permission Checks

```python
# WRONG - expensive in list views
def get_permission_query_conditions(user):
    # This runs for EVERY query
    all_users = frappe.get_all("User")  # Bad!
    # ...

# RIGHT - use simple SQL conditions
def get_permission_query_conditions(user):
    return f"`tabDoc`.`owner` = {frappe.db.escape(user)}"
```

### 4. Not Checking Document Existence

```python
# WRONG
def has_permission(doc, ptype, user):
    return doc.owner == user  # May fail if doc is string

# RIGHT
def has_permission(doc, ptype, user):
    if isinstance(doc, str):
        doc = frappe.get_doc(doctype, doc)
    return doc.owner == user
```

## Security Checklist

- [ ] All SQL conditions use `frappe.db.escape()`
- [ ] Administrator check is first in hooks
- [ ] Hooks return correct types (bool/None or string)
- [ ] No database modifications in permission checks
- [ ] Tested with minimal permission users
- [ ] Edge cases handled (None, empty values)
- [ ] No hardcoded passwords or secrets
- [ ] Permission logic documented
- [ ] Code reviewed for security issues
