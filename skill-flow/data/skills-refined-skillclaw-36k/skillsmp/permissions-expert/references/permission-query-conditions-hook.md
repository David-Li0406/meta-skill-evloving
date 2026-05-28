# permission_query_conditions Hook - List View Filtering and Document Access

## Purpose

Return SQL WHERE conditions to filter documents in list views, reports, and database queries. These conditions are also checked within `has_permission()` when verifying read/select access to individual documents.

## Location

In your doctype's `.py` file or registered in `hooks.py`

## Signature

```python
def get_permission_query_conditions(user=None, doctype=None):
    """
    Return SQL WHERE conditions to filter queryable documents.
    
    Args:
        user: User being checked (defaults to current user)
        doctype: DocType being queried
        
    Returns:
        str: SQL WHERE clause without the "WHERE" keyword
             Returns empty string "" to allow all documents
             
    Security Note:
        The returned SQL is inserted directly into queries.
        ALWAYS escape user input using frappe.db.escape()
    """
    pass
```

## Important Notes

- Return empty string `""` to show all documents (no filtering)
- Always escape dynamic values with `frappe.db.escape()`
- Conditions are combined with AND logic
- Used for **both** list filtering AND individual document access validation
- When `has_permission(doctype, "read", doc)` is called, these conditions are checked against the specific document
- Multiple hooks can be registered and are combined

## Where It's Used

- List views
- Report generation
- Database queries via `frappe.get_list()` and `frappe.get_all()`
- Link field searches
- **Individual document access** - When `has_permission()` is called with a document for read/select operations

## Security Warning

**CRITICAL**: When a user tries to open a specific document (e.g., via URL or direct access), `has_permission()` will validate the document against these conditions. If the document doesn't match (e.g., wrong company), access will be denied even if the user has the correct role permissions.

## Examples

### Example 1: Show only documents from user's company

```python
def get_permission_query_conditions(user=None, doctype=None):
    """Filter documents by user's company.
    
    This will filter list views AND prevent access to individual documents
    from other companies even if user has role permissions.
    """
    if not user:
        user = frappe.session.user
        
    # Administrator sees everything
    if user == "Administrator":
        return ""
    
    # Get user's company
    user_company = frappe.db.get_value("User", user, "company")
    
    if not user_company:
        # No company assigned, show nothing
        return "1=0"
    
    # Escape the company value for SQL safety
    # This condition will be checked both in lists AND when accessing individual docs
    return f"`tabYour DocType`.`company` = {frappe.db.escape(user_company)}"
```

### Example 2: Show documents based on role and territory

```python
def get_permission_query_conditions(user=None, doctype=None):
    """Filter documents by territory based on user role."""
    if not user:
        user = frappe.session.user
        
    if user == "Administrator":
        return ""
    
    roles = frappe.get_roles(user)
    
    # Sales managers see everything
    if "Sales Manager" in roles:
        return ""
    
    # Sales users see only their territory
    if "Sales User" in roles:
        user_territory = frappe.db.get_value("User", user, "territory")
        if user_territory:
            return f"`tabSales Order`.`territory` = {frappe.db.escape(user_territory)}"
    
    # Default: show nothing
    return "1=0"
```

### Example 3: Complex conditions with multiple criteria

```python
def get_permission_query_conditions(user=None, doctype=None):
    """Show documents based on status, owner, or team membership."""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return ""
    
    conditions = []
    
    # Always show published documents
    conditions.append("`tabYour DocType`.`status` = 'Published'")
    
    # Always show own documents
    conditions.append(f"`tabYour DocType`.`owner` = {frappe.db.escape(user)}")
    
    # Show team documents if user has a team
    user_team = frappe.db.get_value("User", user, "team")
    if user_team:
        conditions.append(f"`tabYour DocType`.`team` = {frappe.db.escape(user_team)}")
    
    # Combine with OR logic (at least one condition must be true)
    return "(" + " OR ".join(conditions) + ")"
```

### Example 4: Role-based region filtering

```python
def get_permission_query_conditions(user=None, doctype=None):
    """Filter by user's region unless user is a manager."""
    if not user:
        user = frappe.session.user
    
    if "Regional Manager" in frappe.get_roles(user):
        return ""  # See all regions
    
    user_region = frappe.db.get_value("User", user, "region")
    return f"`tabDoc`.`region` = {frappe.db.escape(user_region)}"
```

### Example 5: Time-based access

```python
def get_permission_query_conditions(user=None, doctype=None):
    """Show only documents from current fiscal year."""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return ""
    
    from frappe.utils import get_fiscal_year
    
    fy = get_fiscal_year(frappe.utils.today())[0]
    fy_start, fy_end = frappe.db.get_value(
        "Fiscal Year", fy, ["year_start_date", "year_end_date"]
    )
    
    return f"`tabDoc`.`posting_date` BETWEEN {frappe.db.escape(fy_start)} AND {frappe.db.escape(fy_end)}"
```

### Example 6: Multi-tenant access

```python
def get_permission_query_conditions(user=None, doctype=None):
    """Multi-company access control."""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return ""
    
    allowed_companies = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": "Company"},
        pluck="for_value"
    )
    
    if not allowed_companies:
        return "1=0"  # No companies assigned
    
    companies_str = ", ".join([frappe.db.escape(c) for c in allowed_companies])
    return f"`tabDoc`.`company` IN ({companies_str})"
```

### Example 7: Combined role and territory access

```python
def get_permission_query_conditions(user=None, doctype=None):
    """Complex filtering based on role hierarchy and territory."""
    if not user:
        user = frappe.session.user
    
    roles = frappe.get_roles(user)
    
    # Sales Directors see everything
    if "Sales Director" in roles:
        return ""
    
    conditions = []
    
    # Sales Managers see their region
    if "Sales Manager" in roles:
        user_region = frappe.db.get_value("User", user, "region")
        if user_region:
            conditions.append(f"`tabSales Order`.`region` = {frappe.db.escape(user_region)}")
    
    # Sales Users see only their territory within their region
    if "Sales User" in roles:
        user_territory = frappe.db.get_value("User", user, "territory")
        if user_territory:
            conditions.append(f"`tabSales Order`.`territory` = {frappe.db.escape(user_territory)}")
    
    # Always show own documents
    conditions.append(f"`tabSales Order`.`owner` = {frappe.db.escape(user)}")
    
    # Combine with OR logic
    return "(" + " OR ".join(conditions) + ")" if conditions else "1=0"
```

## Registration in hooks.py

```python
permission_query_conditions = {
    "Your DocType": "your_app.your_module.your_doctype.get_permission_query_conditions",
    "*": "your_app.permissions.global_query_conditions",  # Applied to all doctypes
}
```

## Best Practices

1. **Always escape user input**: Use `frappe.db.escape()` for all dynamic values
2. **Return empty string for no restrictions**: Don't return None
3. **Fail secure**: Return "1=0" (always false) when in doubt
4. **Use indexed fields**: Query on indexed columns for performance
5. **Test edge cases**: Test with users having no permissions, multiple companies, etc.
6. **Cache user data**: Cache frequently accessed user properties for performance
7. **Consider individual document access**: Remember these conditions block direct document access too

## Common Patterns

### Deny all access

```python
return "1=0"  # SQL condition that's always false
```

### Allow all access

```python
return ""  # Empty condition means no filtering
```

### OR logic

```python
conditions = ["condition1", "condition2", "condition3"]
return "(" + " OR ".join(conditions) + ")"
```

### AND logic (default)

Multiple hooks are combined with AND, so just return your condition:

```python
return "your_condition"
```
