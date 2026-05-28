# Permission Hooks

Permission hooks extend Frappe's permission system with custom logic.

## Core Permission Hooks

### has_permission

Custom document-level permission check.

```python
has_permission = {
    "DocType Name": "my_app.permissions.has_permission",
}
```

**Function signature:**
```python
def has_permission(doc, ptype=None, user=None, debug=False):
    """
    Args:
        doc: Document instance or dict
        ptype: Permission type ("read", "write", "create", etc.)
        user: User email (defaults to current user)
        debug: Enable debug logging

    Returns:
        bool or None:
            True - Explicitly grant permission
            False - Explicitly deny permission
            None - No opinion, continue with other checks
    """
```

**Example:**
```python
def has_permission(doc, ptype=None, user=None, debug=False):
    # Owner can always access
    if doc.owner == user:
        return True

    # Manager can access all
    if "Manager" in frappe.get_roles(user):
        return True

    # Department members can read
    if ptype == "read":
        user_dept = frappe.db.get_value("User", user, "department")
        if doc.department == user_dept:
            return True

    # No opinion for other cases
    return None
```

### permission_query_conditions

Filter documents in list views and validate document access.

```python
permission_query_conditions = {
    "DocType Name": "my_app.permissions.get_permission_query_conditions",
}
```

**Function signature:**
```python
def get_permission_query_conditions(user=None, doctype=None):
    """
    Returns:
        str: SQL WHERE clause (without "WHERE" keyword)
             Empty string "" to allow all documents
    """
```

**Example:**
```python
def get_permission_query_conditions(user=None, doctype=None):
    if not user:
        user = frappe.session.user

    # Administrator sees everything
    if user == "Administrator":
        return ""

    # Manager sees all
    if "Manager" in frappe.get_roles(user):
        return ""

    # Others see only their department
    user_dept = frappe.db.get_value("User", user, "department")
    return f"`tabDocType Name`.department = {frappe.db.escape(user_dept)}"
```

**Security Note:** Always escape user inputs:
```python
# WRONG - SQL injection risk
return f"field = {value}"

# CORRECT - Escaped
return f"field = {frappe.db.escape(value)}"
```

### write_permission_query_conditions

Validate writes before database commit.

```python
write_permission_query_conditions = {
    "DocType Name": "my_app.permissions.get_write_permission_query_conditions",
}
```

**Use for:** Validating that saved documents meet certain conditions.

**How it works:** Automatically called during `has_permission()` checks for write/create/submit/cancel/delete operations.

**Example:**
```python
def get_write_permission_query_conditions(user=None, doctype=None, ptype="write"):
    """
    Automatically checked during has_permission() for write operations.
    Checked AFTER write but BEFORE commit.
    If validation fails, transaction is rolled back.
    """
    if not user:
        user = frappe.session.user

    # Can only edit documents in their region
    user_region = frappe.db.get_value("User", user, "region")
    return f"`tabDocType Name`.region = {frappe.db.escape(user_region)}"
```

### has_website_permission

Control document access on website/portal (not desk).

```python
has_website_permission = {
    "DocType Name": "my_app.permissions.has_website_permission",
}
```

**Function signature:**
```python
def has_website_permission(doc, ptype=None, user=None, debug=False):
    """
    Returns:
        bool: True if user can access on website, False otherwise
    """
```

**Example:**
```python
def has_website_permission(doc, ptype=None, user=None, debug=False):
    if not user:
        user = frappe.session.user

    # Guest can see published content
    if user == "Guest":
        return doc.get("published") == 1

    # Owner can always see
    if doc.owner == user:
        return True

    # Customer can see their orders
    customer = frappe.db.get_value("User", user, "customer")
    if doc.customer == customer:
        return True

    return False
```

## Workflow Permission Hooks

### filter_workflow_transitions

Filter available workflow transitions based on custom logic.

```python
filter_workflow_transitions = [
    "my_app.workflow.filter_transitions",
]
```

**Function signature:**
```python
def filter_transitions(doc, transitions, workflow):
    """
    Args:
        doc: Document instance
        transitions: List of available transition dicts
        workflow: Workflow document

    Returns:
        List of filtered transitions or None (no filtering)
    """
```

**Example:**
```python
def filter_transitions(doc, transitions, workflow):
    # Amount-based routing
    filtered = []
    for transition in transitions:
        if transition.action == "Approve":
            # Only show approve if under user's limit
            user_limit = get_approval_limit(frappe.session.user)
            if doc.total_amount <= user_limit:
                filtered.append(transition)
        else:
            filtered.append(transition)

    return filtered
```

### has_workflow_action_permission

Control who receives workflow action notifications.

```python
has_workflow_action_permission = [
    "my_app.workflow.has_action_permission",
]
```

**Function signature:**
```python
def has_action_permission(user, transition, doc):
    """
    Args:
        user: User email
        transition: Transition dict
        doc: Document instance

    Returns:
        bool: True if user should receive action, False otherwise
    """
```

**Example:**
```python
def has_action_permission(user, transition, doc):
    # Hierarchical approval
    if transition.action == "Approve":
        # Only manager of document owner can approve
        doc_owner = doc.owner
        owner_manager = frappe.db.get_value("User", doc_owner, "reports_to")
        return user == owner_manager

    # Region-based routing
    if transition.action == "Regional Approval":
        user_region = frappe.db.get_value("User", user, "region")
        return doc.region == user_region

    return True
```

### workflow_safe_eval_globals

Extend available globals in workflow transition conditions.

```python
workflow_safe_eval_globals = [
    "my_app.workflow.get_workflow_globals",
]
```

**Function signature:**
```python
def get_workflow_globals(current_globals):
    """
    Args:
        current_globals: Dict of currently available globals

    Returns:
        dict: Additional globals to make available in workflow conditions
    """
```

**Available by default in workflow conditions:**
- `doc` - Document as dict
- `frappe.db.get_value` - Get a single value from database
- `frappe.db.get_list` - Get list of records
- `frappe.session` - Current session object
- `frappe.utils.now_datetime` - Current datetime
- `frappe.utils.add_to_date` - Add/subtract date intervals
- `frappe.utils.get_datetime` - Parse datetime
- `frappe.utils.now` - Current timestamp

**Use case:** Add custom functions or data for workflow transition conditions.

**Example 1: Add custom helper function:**
```python
def get_workflow_globals(current_globals):
    def get_approval_limit(user):
        """Helper to get user's approval limit"""
        return frappe.db.get_value("User", user, "approval_limit") or 0

    return {
        "get_approval_limit": get_approval_limit,
    }

# In Workflow Transition condition field:
# doc.grand_total <= get_approval_limit(frappe.session.user)
```

**Example 2: Add business logic functions:**
```python
def get_workflow_globals(current_globals):
    def is_business_hours():
        """Check if current time is during business hours"""
        from datetime import datetime
        now = datetime.now()
        return 9 <= now.hour < 17 and now.weekday() < 5

    def get_regional_manager(region):
        """Get manager for a region"""
        return frappe.db.get_value("Region", region, "manager")

    return {
        "is_business_hours": is_business_hours,
        "get_regional_manager": get_regional_manager,
    }

# In Workflow Transition conditions:
# is_business_hours() and doc.urgency == "High"
# doc.assigned_to == get_regional_manager(doc.region)
```

**Example 3: Add cached configuration data:**
```python
def get_workflow_globals(current_globals):
    # Load configuration once per request
    config = frappe.cache().get_value("workflow_config")
    if not config:
        config = frappe.get_single("Workflow Settings").as_dict()
        frappe.cache().set_value("workflow_config", config)

    return {
        "workflow_config": config,
    }

# In Workflow Transition condition:
# doc.total_amount >= workflow_config.min_amount_for_approval
```

**Security Note:**
- Functions added via this hook are available in workflow transition conditions
- Use safe_eval internally; avoid exposing dangerous operations
- Validate inputs in your functions to prevent misuse

## Examples by Use Case

### 1. Department-Based Access

```python
# hooks.py
permission_query_conditions = {
    "Project": "my_app.permissions.project_query",
}
has_permission = {
    "Project": "my_app.permissions.project_permission",
}

# permissions.py
def project_query(user=None, doctype=None):
    user = user or frappe.session.user

    if "Project Manager" in frappe.get_roles(user):
        return ""  # See all

    dept = frappe.db.get_value("User", user, "department")
    return f"`tabProject`.department = {frappe.db.escape(dept)}"

def project_permission(doc, ptype=None, user=None, debug=False):
    user = user or frappe.session.user

    # Team members can read
    if ptype == "read":
        team_members = [d.user for d in doc.team]
        if user in team_members:
            return True

    return None
```

### 2. Hierarchical Access

```python
def has_permission(doc, ptype=None, user=None, debug=False):
    user = user or frappe.session.user

    # Owner can access
    if doc.owner == user:
        return True

    # Check reporting hierarchy
    current_user = user
    for i in range(5):  # Max 5 levels
        manager = frappe.db.get_value("User", current_user, "reports_to")
        if not manager:
            break
        if manager == doc.owner:
            return True  # User reports to document owner
        current_user = manager

    return None
```

### 3. Time-Based Access

```python
def get_permission_query_conditions(user=None, doctype=None):
    from frappe.utils import now_datetime, add_days

    # Show only documents from last 30 days
    cutoff_date = add_days(now_datetime(), -30)

    return f"`tabDocType Name`.creation >= '{cutoff_date}'"
```

### 4. Status-Based Write Protection

```python
def get_write_permission_query_conditions(user=None, doctype=None, permtype="write"):
    user = user or frappe.session.user

    # Can only edit draft documents
    conditions = ["`tabDocType Name`.status = 'Draft'"]

    # Or own documents
    conditions.append(f"`tabDocType Name`.owner = {frappe.db.escape(user)}")

    return " OR ".join(f"({c})" for c in conditions)
```

### 5. Portal Customer Access

```python
def has_website_permission(doc, ptype=None, user=None, debug=False):
    user = user or frappe.session.user

    if user == "Guest":
        return False

    # Get customer linked to user
    customer = frappe.db.get_value("Contact", {"user": user}, "customer")

    # Check if document is for this customer
    if doc.get("customer") == customer:
        return True

    # Check through related documents
    if doc.get("order_id"):
        order_customer = frappe.db.get_value("Sales Order", doc.order_id, "customer")
        return order_customer == customer

    return False
```

### 6. Multi-Tenant Access

```python
def get_permission_query_conditions(user=None, doctype=None):
    user = user or frappe.session.user

    # Administrator sees all tenants
    if user == "Administrator":
        return ""

    # Get user's tenant
    tenant = frappe.db.get_value("User", user, "tenant")
    if not tenant:
        return "1=0"  # No access

    return f"`tabDocType Name`.tenant = {frappe.db.escape(tenant)}"
```

## Best Practices

1. **Return None for No Opinion**: Let other checks continue
2. **Escape SQL Values**: Always use `frappe.db.escape()`
3. **Cache Lookups**: Cache frequently accessed data
4. **Test Edge Cases**: Test with different roles and users
5. **Document Logic**: Add comments explaining permission rules
6. **Performance**: Keep queries fast, especially in list views
7. **Security**: Default to denying access when uncertain

## Common Patterns

### Combine Multiple Conditions

```python
def get_permission_query_conditions(user=None, doctype=None):
    conditions = []

    # Condition 1: User's company
    company = frappe.db.get_value("User", user, "company")
    conditions.append(f"company = {frappe.db.escape(company)}")

    # Condition 2: User's department
    dept = frappe.db.get_value("User", user, "department")
    conditions.append(f"department = {frappe.db.escape(dept)}")

    # Combine with AND
    return " AND ".join(f"({c})" for c in conditions)
```

### Role-Based Filtering

```python
def get_permission_query_conditions(user=None, doctype=None):
    roles = frappe.get_roles(user)

    if "CEO" in roles:
        return ""  # See all

    if "Manager" in roles:
        # See department documents
        dept = frappe.db.get_value("User", user, "department")
        return f"department = {frappe.db.escape(dept)}"

    # Default: own documents only
    return f"owner = {frappe.db.escape(user)}"
```

## Debugging

Enable debug mode:
```python
frappe.has_permission("DocType", "read", doc, debug=True)
```

Check permission logs:
```python
logs = frappe.local.permission_debug_log
for log in logs:
    print(log)
```

## Notes

- Permission hooks run frequently; optimize for performance
- `permission_query_conditions` affects both list views AND individual document access
- Return empty string `""` to allow all documents
- Return `"1=0"` to deny all documents
- Always escape user inputs in SQL
- Test with different user roles and scenarios
