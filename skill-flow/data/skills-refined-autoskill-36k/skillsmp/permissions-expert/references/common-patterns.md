# Common Permission Patterns

This file contains ready-to-use permission patterns for common scenarios.

## Table of Contents

- [Pattern 1: Owner-Only Access](#pattern-1-owner-only-access)
- [Pattern 2: Role-Based Region Filtering](#pattern-2-role-based-region-filtering)
- [Pattern 3: Hierarchical Access](#pattern-3-hierarchical-access-teamdepartment)
- [Pattern 4: Status-Based Restrictions](#pattern-4-status-based-restrictions)
- [Pattern 5: Time-Based Access](#pattern-5-time-based-access)
- [Pattern 6: Multi-Tenant Access](#pattern-6-multi-tenant-access)
- [Pattern 7: Permission Level Filtering](#pattern-7-permission-level-filtering)
- [Pattern 8: Child Table Permissions](#pattern-8-child-table-permissions)
- [Pattern 9: Conditional Field Visibility](#pattern-9-conditional-field-visibility)
- [Pattern 10: Combined Role and Territory Access](#pattern-10-combined-role-and-territory-access)
- [Pattern 11: Department-Based Access](#pattern-11-department-based-access)
- [Pattern 12: Approval Workflow Access](#pattern-12-approval-workflow-access)
- [Pattern 13: Customer Portal Access](#pattern-13-customer-portal-access)
- [Pattern 14: Project-Based Access](#pattern-14-project-based-access)
- [Pattern 15: Published/Draft Content](#pattern-15-publisheddraft-content)
- [Pattern Combination Example](#pattern-combination-example)
- [Tips for Using Patterns](#tips-for-using-patterns)

## Pattern 1: Owner-Only Access

Allow only the document owner to access the document.

```python
def has_permission(doc, ptype, user):
    """Only document owner can access."""
    return doc.owner == user
```

## Pattern 2: Role-Based Region Filtering

Filter documents by user's region, with managers seeing all.

```python
def get_permission_query_conditions(user):
    """Filter by user's region unless user is a manager."""
    if not user:
        user = frappe.session.user
    
    if "Regional Manager" in frappe.get_roles(user):
        return ""  # See all regions
    
    user_region = frappe.db.get_value("User", user, "region")
    if not user_region:
        return "1=0"
    
    return f"`tabDoc`.`region` = {frappe.db.escape(user_region)}"
```

## Pattern 3: Hierarchical Access (Team/Department)

Allow access to documents in user's team hierarchy.

```python
def has_permission(doc, ptype, user):
    """Allow access to documents in user's team hierarchy."""
    if not user:
        user = frappe.session.user
    
    user_teams = get_user_team_hierarchy(user)
    return doc.team in user_teams

def get_user_team_hierarchy(user):
    """Get all teams user belongs to, including parent teams."""
    teams = []
    user_team = frappe.db.get_value("User", user, "team")
    
    if user_team:
        teams.append(user_team)
        # Add parent teams if it's a tree structure
        # Implementation depends on your team structure
    
    return teams
```

## Pattern 4: Status-Based Restrictions

Restrict write access based on document status.

```python
def has_permission(doc, ptype, user):
    """Restrict write access to draft documents."""
    if not user:
        user = frappe.session.user
    
    if ptype in ("write", "delete") and doc.status != "Draft":
        # Only admins can modify non-draft documents
        return user == "Administrator"
    
    return None
```

## Pattern 5: Time-Based Access

Show only documents from current fiscal year.

```python
def get_permission_query_conditions(user):
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

## Pattern 6: Multi-Tenant Access

Multi-company access control using User Permissions.

```python
def get_permission_query_conditions(user):
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

## Pattern 7: Permission Level Filtering

Restrict edit access to sensitive fields based on role.

```python
def has_permission(doc, ptype, user):
    """Restrict edit access to sensitive fields based on role."""
    if not user:
        user = frappe.session.user
    
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

## Pattern 8: Child Table Permissions

Control access to sensitive child tables.

```python
# In parent doctype
def has_permission(doc, ptype, user):
    """Control access to sensitive child tables."""
    if not user:
        user = frappe.session.user
    
    if ptype == "write":
        # Check if user can edit the cost details child table
        meta = frappe.get_meta(doc.doctype)
        cost_field = meta.get_field("cost_details")
        
        if cost_field and cost_field.permlevel > 0:
            accessible_permlevels = meta.get_permlevel_access("write", user=user)
            if cost_field.permlevel not in accessible_permlevels:
                # User can edit document but not cost details
                doc.flags.ignore_children_type = ["Cost Details"]
    
    return None
```

## Pattern 9: Conditional Field Visibility

Hide certain fields based on document status and user role.

```python
def has_permission(doc, ptype, user):
    """Hide certain fields based on document status and user role."""
    if not user:
        user = frappe.session.user
    
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

## Pattern 10: Combined Role and Territory Access

Complex filtering based on role hierarchy and territory.

```python
def get_permission_query_conditions(user):
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

## Pattern 11: Department-Based Access

Filter documents by user's department.

```python
def get_permission_query_conditions(user):
    """Show only documents from user's department."""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return ""
    
    # Department heads see all in their department
    if "Department Head" in frappe.get_roles(user):
        user_dept = frappe.db.get_value("User", user, "department")
        if user_dept:
            return f"`tabDoc`.`department` = {frappe.db.escape(user_dept)}"
    
    # Regular users see only own documents
    return f"`tabDoc`.`owner` = {frappe.db.escape(user)}"
```

## Pattern 12: Approval Workflow Access

Control access based on approval status.

```python
def has_permission(doc, ptype, user):
    """Control access based on approval workflow."""
    if not user:
        user = frappe.session.user
    
    roles = frappe.get_roles(user)
    
    # Approvers can access pending documents
    if "Approver" in roles and doc.status == "Pending Approval":
        return None  # Defer to role permissions
    
    # Creators can only access their own drafts
    if doc.status == "Draft":
        return doc.owner == user
    
    # Everyone can read approved documents
    if ptype == "read" and doc.status == "Approved":
        return None
    
    return False
```

## Pattern 13: Customer Portal Access

Allow customers to view their own documents.

```python
def has_website_permission(doc, ptype="read", user=None):
    """Allow customers to view only their own orders on portal."""
    if not user:
        user = frappe.session.user
    
    # Get the customer linked to this user
    customer = frappe.db.get_value("Contact", {"user": user}, "parent_name")
    
    # Allow if this document belongs to the customer
    return doc.customer == customer
```

## Pattern 14: Project-Based Access

Filter documents by project membership.

```python
def get_permission_query_conditions(user):
    """Show only documents from projects user is member of."""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return ""
    
    # Get user's projects
    user_projects = frappe.get_all(
        "Project User",
        filters={"user": user},
        pluck="parent"
    )
    
    if not user_projects:
        return "1=0"
    
    projects_str = ", ".join([frappe.db.escape(p) for p in user_projects])
    return f"`tabDoc`.`project` IN ({projects_str})"
```

## Pattern 15: Published/Draft Content

Show published content to all, drafts only to creators.

```python
def get_permission_query_conditions(user):
    """Show published content to all, drafts only to owner."""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator" or "Editor" in frappe.get_roles(user):
        return ""  # Editors see everything
    
    # Regular users see published + own drafts
    return f"(`tabDoc`.`published` = 1 OR `tabDoc`.`owner` = {frappe.db.escape(user)})"
```

## Pattern Combination Example

Combine multiple patterns for complex requirements.

```python
def get_permission_query_conditions(user):
    """
    Complex permission logic combining:
    - Company filtering
    - Department filtering
    - Status-based access
    - Owner access
    """
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return ""
    
    conditions = []
    
    # Company filter
    user_company = frappe.db.get_value("User", user, "company")
    if user_company:
        conditions.append(f"`tabDoc`.`company` = {frappe.db.escape(user_company)}")
    
    # Department filter for non-managers
    roles = frappe.get_roles(user)
    if "Manager" not in roles:
        user_dept = frappe.db.get_value("User", user, "department")
        if user_dept:
            conditions.append(f"`tabDoc`.`department` = {frappe.db.escape(user_dept)}")
    
    # Status filter - approved documents visible to all
    status_condition = f"(`tabDoc`.`status` = 'Approved' OR `tabDoc`.`owner` = {frappe.db.escape(user)})"
    conditions.append(status_condition)
    
    # Combine all with AND
    return " AND ".join(f"({c})" for c in conditions) if conditions else "1=0"
```

## Tips for Using Patterns

1. **Start simple**: Begin with basic patterns and add complexity as needed
2. **Test thoroughly**: Test each pattern with different user roles
3. **Document well**: Add comments explaining the permission logic
4. **Escape values**: Always use `frappe.db.escape()` for SQL conditions
5. **Check Administrator**: Always allow Administrator access first
6. **Combine wisely**: Multiple patterns can be combined but keep it maintainable
