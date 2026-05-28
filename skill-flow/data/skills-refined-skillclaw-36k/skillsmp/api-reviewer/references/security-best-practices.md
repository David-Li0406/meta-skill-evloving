# API Security Best Practices for Frappe

This document outlines security best practices when creating API endpoints in Frappe using the `@frappe.whitelist()` decorator.

## Common Security Issues

### 1. Missing Role Validation

**Problem**: API endpoints exposed without any role restrictions allow any authenticated user to access them.

**Bad Example**:
```python
@frappe.whitelist()
def delete_all_records(doctype):
    frappe.db.delete(doctype)  # ANY user can call this!
```

**Good Example**:
```python
@frappe.whitelist()
def delete_all_records(doctype):
    frappe.only_for("System Manager")  # Restricted to System Manager role
    frappe.db.delete(doctype)
```

### 2. Using frappe.get_all Instead of frappe.get_list

**Problem**: `frappe.get_all()` bypasses permission checks, returning all records regardless of user permissions.

**Bad Example**:
```python
@frappe.whitelist()
def get_user_data():
    return frappe.get_all("User", fields=["name", "email"])  # Bypasses permissions!
```

**Good Example**:
```python
@frappe.whitelist()
def get_user_data():
    return frappe.get_list("User", fields=["name", "email"])  # Respects permissions
```

### 3. Missing Document Permission Checks

**Problem**: Accessing or modifying documents without checking if the user has permission.

**Bad Example**:
```python
@frappe.whitelist()
def update_document(doctype, name, field, value):
    doc = frappe.get_doc(doctype, name)
    doc.set(field, value)
    doc.save()  # No permission check!
```

**Good Example**:
```python
@frappe.whitelist()
def update_document(doctype, name, field, value):
    if not frappe.has_permission(doctype, "write", name):
        frappe.throw("No permission to update this document")
    
    doc = frappe.get_doc(doctype, name)
    doc.set(field, value)
    doc.save()
```

### 4. SQL Injection Vulnerabilities

**Problem**: Constructing SQL queries with user input without proper sanitization.

**Bad Example**:
```python
@frappe.whitelist()
def search_users(query):
    return frappe.db.sql(f"SELECT * FROM `tabUser` WHERE name LIKE '%{query}%'")  # SQL injection!
```

**Good Example**:
```python
@frappe.whitelist()
def search_users(query):
    return frappe.db.sql(
        "SELECT * FROM `tabUser` WHERE name LIKE %s",
        ("%" + query + "%",)  # Parameterized query
    )
```

### 5. Unrestricted Data Access

**Problem**: Returning sensitive information without validation.

**Bad Example**:
```python
@frappe.whitelist()
def get_user_password_hash(user):
    return frappe.db.get_value("User", user, "password")  # Exposing password hash!
```

**Good Example**:
```python
@frappe.whitelist()
def get_user_info(user):
    frappe.only_for("System Manager")
    # Only return safe fields
    return frappe.db.get_value("User", user, ["name", "email", "full_name"], as_dict=True)
```

## Security Checklist for API Endpoints

When reviewing or creating API endpoints with `@frappe.whitelist()`, ensure:

- [ ] **Role restrictions**: Use `frappe.only_for("Role")` to restrict access to specific roles
- [ ] **Permission checks**: Use `frappe.has_permission()` to validate document/DocType access
- [ ] **Safe queries**: Use `frappe.get_list()` instead of `frappe.get_all()` to respect permissions
- [ ] **SQL safety**: Use parameterized queries, never string concatenation with user input
- [ ] **Input validation**: Validate and sanitize all user inputs
- [ ] **Sensitive data**: Avoid exposing sensitive information (passwords, API keys, tokens)
- [ ] **Resource limits**: Implement pagination and rate limiting for expensive operations
- [ ] **Audit logging**: Log security-relevant actions for audit trails

## Common Security Functions

### frappe.only_for(role)

Restricts endpoint access to users with specific role(s).

```python
@frappe.whitelist()
def admin_function():
    frappe.only_for("System Manager")
    # Only System Managers can execute this
```

### frappe.has_permission(doctype, ptype, doc, user)

Checks if a user has permission for a specific action on a DocType or document.

```python
@frappe.whitelist()
def get_document(doctype, name):
    if not frappe.has_permission(doctype, "read", name):
        frappe.throw("No permission to read this document")
    return frappe.get_doc(doctype, name)
```

### frappe.get_list() vs frappe.get_all()

- **frappe.get_list()**: Respects user permissions (PREFERRED)
- **frappe.get_all()**: Bypasses permissions (use only when necessary with proper role checks)

```python
# Good - respects permissions
@frappe.whitelist()
def get_my_documents(doctype):
    return frappe.get_list(doctype, fields=["name", "title"])

# Acceptable - with role restriction
@frappe.whitelist()
def get_all_documents(doctype):
    frappe.only_for("System Manager")
    return frappe.get_all(doctype, fields=["name", "title"])
```

## Review Workflow

1. **Scan for endpoints**: Use `scan_api_endpoints.py` to find all `@frappe.whitelist()` functions
2. **Review security checks**: Check that each endpoint has appropriate security measures
3. **Mark as reviewed**: Update the YAML file with review status and notes
4. **Document concerns**: Add notes for endpoints that need attention or refactoring
5. **Regular audits**: Re-scan periodically to catch new endpoints

## Common Patterns

### Pattern: Admin-only endpoint
```python
@frappe.whitelist()
def admin_operation():
    frappe.only_for("System Manager")
    # Implementation
```

### Pattern: Document operation with permission check
```python
@frappe.whitelist()
def update_record(doctype, name, data):
    if not frappe.has_permission(doctype, "write", name):
        frappe.throw("No permission")
    
    doc = frappe.get_doc(doctype, name)
    doc.update(data)
    doc.save()
    return doc
```

### Pattern: Query with permission filtering
```python
@frappe.whitelist()
def search_documents(doctype, filters=None):
    # frappe.get_list respects permissions automatically
    return frappe.get_list(
        doctype,
        filters=filters,
        fields=["name", "title", "status"],
        limit_page_length=100
    )
```

### Pattern: Current user context only
```python
@frappe.whitelist()
def get_my_profile():
    # Safe - returns only current user's data
    return frappe.get_doc("User", frappe.session.user)
```

## Additional Resources

- [Frappe Framework Security](https://frappeframework.com/docs/user/en/security)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [Frappe Whitelisting Documentation](https://frappeframework.com/docs/user/en/api/whitelisting)
