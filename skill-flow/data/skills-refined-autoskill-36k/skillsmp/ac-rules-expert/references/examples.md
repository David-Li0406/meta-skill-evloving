# Usage Examples and Patterns

Complete examples demonstrating common AC Rule patterns and use cases.

## Example 1: Sales Team Access Control (Report)

**Goal**: Create a Sales Report that only shows customers managed by the current user.

### Step 1: Create Query Filter for Sales Team Users

```python
# Via UI or code
sales_team_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Sales Team Members",
    "reference_doctype": "User",
    "filters_type": "JSON",
    "filters": frappe.as_json([["email", "like", "%@sales.company.com"]])
}).insert()
```

### Step 2: Create Query Filter for Managed Customers

```python
managed_customers_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "My Managed Customers",
    "reference_doctype": "Customer",
    "filters_type": "Python",
    "filters": """
# The 'user' variable is automatically available in Python filters
conditions = f"`tabCustomer`.`account_manager` = {frappe.db.escape(user)}"
"""
}).insert()
```

### Step 3: Create AC Resource

```python
resource = frappe.get_doc({
    "doctype": "AC Resource",
    "type": "Report",
    "report": "Sales Customer Report",
    "managed_actions": "Select",
    "actions": [{"action": "Read"}]
}).insert()
```

### Step 4: Create AC Rule

```python
rule = frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Sales Team Read Managed Customers",
    "type": "Permit",
    "resource": resource.name,
    "actions": [{"action": "Read"}],
    "principals": [
        {"filter": sales_team_filter.name, "exception": 0}
    ],
    "resources": [
        {"filter": managed_customers_filter.name, "exception": 0}
    ]
}).insert()
```

### Step 5: Integrate in Report Code

```python
# In your report's execute() function
from tweaks.tweaks.doctype.ac_rule.ac_rule_utils import get_resource_filter_query

def execute(filters=None):
    columns = get_columns()
    
    # Get AC Rule filter
    result = get_resource_filter_query(
        report="Sales Customer Report",
        action="read"
    )
    
    if result.get("access") == "none":
        return columns, []
    
    ac_filter = result.get("query", "1=1")
    
    # Use the filter in your query
    data = frappe.db.sql(f"""
        SELECT 
            name,
            customer_name,
            account_manager,
            status
        FROM `tabCustomer`
        WHERE {ac_filter}
        ORDER BY name
    """, as_dict=True)
    
    return columns, data
```

## Example 2: Restrict Archived Records (DocType)

**Goal**: Prevent all users (except Administrator) from reading archived customer records.

### Step 1: Create Query Filter for Archived Records

```python
archived_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Archived Customers",
    "reference_doctype": "Customer",
    "filters_type": "JSON",
    "filters": frappe.as_json([["status", "=", "Archived"]])
}).insert()
```

### Step 2: Create Query Filter for All Users

```python
all_users_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "All Users",
    "reference_doctype": "Role",
    "filters_type": "JSON",
    "filters": frappe.as_json([["name", "=", "All"]])
}).insert()
```

### Step 3: Create AC Resource

```python
resource = frappe.get_doc({
    "doctype": "AC Resource",
    "type": "DocType",
    "document_type": "Customer",
    "managed_actions": "Select",
    "actions": [{"action": "Read"}]
}).insert()
```

### Step 4: Create Forbid AC Rule

```python
rule = frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Forbid Archived Customer Access",
    "type": "Forbid",
    "resource": resource.name,
    "actions": [{"action": "Read"}],
    "principals": [
        {"filter": all_users_filter.name, "exception": 0}
    ],
    "resources": [
        {"filter": archived_filter.name, "exception": 0}
    ]
}).insert()
```

**Note**: No code integration needed for DocTypes - this rule is automatically enforced!

## Example 3: Tenant-Based Multi-Tenancy

**Goal**: Multi-tenant setup where users only see their tenant's data.

### Step 1: Create Query Filter for Tenant Users

```python
tenant_users_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Tenant Users",
    "reference_doctype": "User",
    "filters_type": "Python",
    "filters": """
tenant_id = frappe.db.get_value("User", frappe.session.user, "tenant_id")
conditions = f"`tabUser`.`tenant_id` = {tenant_id}"
"""
}).insert()
```

### Step 2: Create Query Filter for Tenant Records

```python
tenant_orders_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Tenant Sales Orders",
    "reference_doctype": "Sales Order",
    "filters_type": "Python",
    "filters": """
tenant_id = frappe.db.get_value("User", frappe.session.user, "tenant_id")
conditions = f"`tabSales Order`.`tenant_id` = {tenant_id}"
"""
}).insert()
```

### Step 3: Create AC Resource

```python
resource = frappe.get_doc({
    "doctype": "AC Resource",
    "type": "DocType",
    "document_type": "Sales Order",
    "managed_actions": "All Actions"
}).insert()
```

### Step 4: Create Permit AC Rule

```python
rule = frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Tenant Data Isolation",
    "type": "Permit",
    "resource": resource.name,
    "actions": [
        {"action": "Read"},
        {"action": "Write"},
        {"action": "Create"},
        {"action": "Delete"}
    ],
    "principals": [
        {"filter": tenant_users_filter.name, "exception": 0}
    ],
    "resources": [
        {"filter": tenant_orders_filter.name, "exception": 0}
    ]
}).insert()
```

## Example 4: Department-Based Access with Exceptions

**Goal**: Allow department members to access their department's documents, except suspended users.

### Step 1: Create Principal Filters

```python
# Department members
dept_users_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Department Users",
    "reference_doctype": "User",
    "filters_type": "Python",
    "filters": """
user_dept = frappe.db.get_value("User", frappe.session.user, "department")
conditions = f"`tabUser`.`department` = {frappe.db.escape(user_dept)}"
"""
}).insert()

# Suspended users (exception)
suspended_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Suspended Users",
    "reference_doctype": "User",
    "filters_type": "JSON",
    "filters": frappe.as_json([["enabled", "=", 0]])
}).insert()
```

### Step 2: Create Resource Filters

```python
# Department documents
dept_docs_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Department Projects",
    "reference_doctype": "Project",
    "filters_type": "Python",
    "filters": """
user_dept = frappe.db.get_value("User", frappe.session.user, "department")
conditions = f"`tabProject`.`department` = {frappe.db.escape(user_dept)}"
"""
}).insert()
```

### Step 3: Create AC Rule with Exceptions

```python
resource = frappe.get_doc({
    "doctype": "AC Resource",
    "type": "DocType",
    "document_type": "Project",
    "managed_actions": "Select",
    "actions": [{"action": "Read"}, {"action": "Write"}]
}).insert()

rule = frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Department Access (Exclude Suspended)",
    "type": "Permit",
    "resource": resource.name,
    "actions": [{"action": "Read"}, {"action": "Write"}],
    "principals": [
        {"filter": dept_users_filter.name, "exception": 0},  # Include dept users
        {"filter": suspended_filter.name, "exception": 1}    # Exclude suspended
    ],
    "resources": [
        {"filter": dept_docs_filter.name, "exception": 0}
    ]
}).insert()
```

## Example 5: Complex SQL Filter with Subqueries

**Goal**: Allow users to access customers based on their user permissions.

### Step 1: Create Resource Filter with Subquery

```python
permitted_customers_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Permitted Customers",
    "reference_doctype": "Customer",
    "filters_type": "SQL",
    "filters": """
customer_type IN (
    SELECT allowed_type 
    FROM `tabUser Permissions` 
    WHERE parent = '{user}'
    AND doctype = 'Customer Type'
) 
AND status != 'Cancelled'
"""
}).insert()
```

### Step 2: Create AC Rule

```python
resource = frappe.get_doc({
    "doctype": "AC Resource",
    "type": "DocType",
    "document_type": "Customer",
    "managed_actions": "All Actions"
}).insert()

all_users_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "All Users",
    "reference_doctype": "Role",
    "filters_type": "JSON",
    "filters": frappe.as_json([["name", "=", "All"]])
}).insert()

rule = frappe.get_doc({
    "doctype": "AC Rule",
    "title": "User Permission Based Access",
    "type": "Permit",
    "resource": resource.name,
    "actions": [
        {"action": "Read"},
        {"action": "Write"}
    ],
    "principals": [
        {"filter": all_users_filter.name, "exception": 0}
    ],
    "resources": [
        {"filter": permitted_customers_filter.name, "exception": 0}
    ]
}).insert()
```

## Example 6: Combining Multiple Permit Rules

**Goal**: Allow both managers and team leaders to access team documents.

### Step 1: Create Principal Filters

```python
managers_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Managers",
    "reference_doctype": "Role",
    "filters_type": "JSON",
    "filters": frappe.as_json([["name", "=", "Manager"]])
}).insert()

team_leaders_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Team Leaders",
    "reference_doctype": "Role",
    "filters_type": "JSON",
    "filters": frappe.as_json([["name", "=", "Team Leader"]])
}).insert()
```

### Step 2: Create Resource Filter

```python
active_tasks_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Active Tasks",
    "reference_doctype": "Task",
    "filters_type": "JSON",
    "filters": frappe.as_json([["status", "!=", "Completed"]])
}).insert()
```

### Step 3: Create Two Permit Rules

```python
resource = frappe.get_doc({
    "doctype": "AC Resource",
    "type": "DocType",
    "document_type": "Task",
    "managed_actions": "Select",
    "actions": [{"action": "Read"}, {"action": "Write"}]
}).insert()

# Rule 1: Managers
manager_rule = frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Managers Access Tasks",
    "type": "Permit",
    "resource": resource.name,
    "actions": [{"action": "Read"}, {"action": "Write"}],
    "principals": [
        {"filter": managers_filter.name, "exception": 0}
    ],
    "resources": [
        {"filter": active_tasks_filter.name, "exception": 0}
    ]
}).insert()

# Rule 2: Team Leaders
leader_rule = frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Team Leaders Access Tasks",
    "type": "Permit",
    "resource": resource.name,
    "actions": [{"action": "Read"}, {"action": "Write"}],
    "principals": [
        {"filter": team_leaders_filter.name, "exception": 0}
    ],
    "resources": [
        {"filter": active_tasks_filter.name, "exception": 0}
    ]
}).insert()
```

**Result**: Users with either Manager OR Team Leader role can access active tasks.

## Common Patterns Summary

### 1. User-Based Filtering

```python
filters = """
user = frappe.session.user
conditions = f"`tabDocType`.`owner` = {frappe.db.escape(user)}"
"""
```

### 2. Role-Based Filtering

```python
# JSON filter for Role
filters = frappe.as_json([["name", "in", ["Sales User", "Sales Manager"]]])
```

### 3. Dynamic Field-Based Filtering (using conditions)

```python
# Python filter - using conditions variable
filters = """
user_value = frappe.db.get_value("User", frappe.session.user, "custom_field")
conditions = f"`tabDocType`.`field` = {frappe.db.escape(user_value)}"
"""
```

### 3b. Dynamic Field-Based Filtering (using filters)

```python
# Python filter - using filters variable (like JSON)
filters = """
user_value = frappe.db.get_value("User", frappe.session.user, "custom_field")
filters = [["field", "=", user_value]]
"""
# This is converted to SQL just like JSON filters
```

### 4. Time-Based Filtering

```python
filters = frappe.as_json([
    ["creation", ">=", "2024-01-01"],
    ["creation", "<=", "2024-12-31"]
])
```

### 5. Status-Based Filtering

```python
filters = frappe.as_json([
    ["status", "in", ["Draft", "Pending", "Approved"]]
])
```

### 6. Hierarchical Filtering (using conditions)

```python
# Python filter - using conditions variable for complex SQL
filters = """
conditions = f'''EXISTS (
    SELECT 1 FROM `tabEmployee`
    WHERE reports_to = {frappe.db.escape(frappe.session.user)}
    AND name = `tabDocType`.`employee`
)'''
"""
```

### 7. Python Filter with Fallback

```python
# Python filter - try conditions first, fallback to filters
filters = """
# Try to build complex SQL condition
try:
    user_dept = frappe.db.get_value("User", frappe.session.user, "department")
    if user_dept:
        conditions = f"`tabDocType`.`department` = {frappe.db.escape(user_dept)}"
    else:
        # Fallback to filters dict
        filters = [["department", "is", "set"]]
except:
    # Error case - block all
    conditions = "1=0"
"""
```

## Example 7: Workflow - Territory-Based Approval

**Goal**: Sales Managers can only approve Sales Orders in their assigned territories.

### Step 1: Create Principal Filter (Sales Managers)

```python
principal_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Sales Managers",
    "reference_doctype": "User",
    "filters_type": "JSON",
    "filters": frappe.as_json([["role", "=", "Sales Manager"]])
}).insert()
```

### Step 2: Create Resource Filter (Territory-Based Orders)

```python
resource_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Sales Orders in My Territory",
    "reference_doctype": "Sales Order",
    "filters_type": "SQL",
    "filters": """
        territory IN (
            SELECT territory FROM `tabSales Team`
            WHERE parent = '{user}' AND parenttype = 'User'
        )
    """
}).insert()
```

### Step 3: Create AC Action for Workflow

```python
# Note: Use scrubbed name (lowercase, underscored)
# "Approve" workflow action -> "approve" AC Action
frappe.get_doc({
    "doctype": "AC Action",
    "action": "approve"
}).insert()
```

### Step 4: Create AC Resource

```python
ac_resource = frappe.get_doc({
    "doctype": "AC Resource",
    "type": "DocType",
    "doctype": "Sales Order",
    "managed_actions": "Select",
    "actions": [{"action": "approve"}]
}).insert()
```

### Step 5: Create AC Rule

```python
frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Territory-Based Sales Order Approval",
    "rule_type": "Permit",
    "resource": ac_resource.name,
    "principals": [{"principal": principal_filter.name}],
    "resources": [{"resource": resource_filter.name}],
    "actions": [{"action": "approve"}],
    "disabled": 0
}).insert()
```

### Testing

```python
# Test if user can see the approve transition
from tweaks.custom.doctype.workflow import get_transitions

doc = frappe.get_doc("Sales Order", "SO-0001")
transitions = get_transitions(doc, user="sales.manager@example.com")
print([t.action for t in transitions])  # Should include "Approve" if in territory

# Test AC Rules directly
from tweaks.tweaks.doctype.ac_rule.ac_rule_utils import has_resource_access

result = has_resource_access(
    doctype="Sales Order",
    action="approve",
    user="sales.manager@example.com"
)
print(result)  # {"access": True/False, "unmanaged": False}
```

## Example 8: Workflow - Amount-Based Approval Hierarchy

**Goal**: Different approval limits based on manager level:
- Regular managers: up to 50k
- Senior managers: 50k-200k
- Directors: over 200k

### Step 1: Create Amount-Based Resource Filters

```python
# POs under 50k
low_amount = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "PO Under 50k",
    "reference_doctype": "Purchase Order",
    "filters_type": "SQL",
    "filters": "grand_total <= 50000"
}).insert()

# POs 50k-200k
medium_amount = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "PO 50k-200k",
    "reference_doctype": "Purchase Order",
    "filters_type": "SQL",
    "filters": "grand_total > 50000 AND grand_total <= 200000"
}).insert()

# POs over 200k
high_amount = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "PO Over 200k",
    "reference_doctype": "Purchase Order",
    "filters_type": "SQL",
    "filters": "grand_total > 200000"
}).insert()
```

### Step 2: Create Role-Based Principal Filters

```python
manager = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Regular Managers",
    "reference_doctype": "User",
    "filters_type": "JSON",
    "filters": frappe.as_json([["role", "=", "Manager"]])
}).insert()

senior_manager = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Senior Managers",
    "reference_doctype": "User",
    "filters_type": "JSON",
    "filters": frappe.as_json([["role", "=", "Senior Manager"]])
}).insert()

director = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Directors",
    "reference_doctype": "User",
    "filters_type": "JSON",
    "filters": frappe.as_json([["role", "=", "Director"]])
}).insert()
```

### Step 3: Create AC Resource

```python
ac_resource = frappe.get_doc({
    "doctype": "AC Resource",
    "type": "DocType",
    "doctype": "Purchase Order",
    "managed_actions": "Select",
    "actions": [{"action": "approve"}]
}).insert()
```

### Step 4: Create Hierarchical Rules

```python
# Managers approve up to 50k
frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Managers Approve PO Under 50k",
    "rule_type": "Permit",
    "resource": ac_resource.name,
    "principals": [{"principal": manager.name}],
    "resources": [{"resource": low_amount.name}],
    "actions": [{"action": "approve"}]
}).insert()

# Senior Managers approve 50k-200k
frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Senior Managers Approve PO 50k-200k",
    "rule_type": "Permit",
    "resource": ac_resource.name,
    "principals": [{"principal": senior_manager.name}],
    "resources": [{"resource": medium_amount.name}],
    "actions": [{"action": "approve"}]
}).insert()

# Directors approve over 200k
frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Directors Approve PO Over 200k",
    "rule_type": "Permit",
    "resource": ac_resource.name,
    "principals": [{"principal": director.name}],
    "resources": [{"resource": high_amount.name}],
    "actions": [{"action": "approve"}]
}).insert()
```

## Example 9: Workflow - Multiple Actions with Different Rules

**Goal**: Control both Approve and Reject actions with different logic:
- Anyone with role can reject (no restrictions)
- Only territory managers can approve

### Step 1: Create Filters

```python
# Territory managers
territory_mgr = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Territory Managers",
    "reference_doctype": "User",
    "filters_type": "SQL",
    "filters": """
        EXISTS (
            SELECT 1 FROM `tabUser Territory`
            WHERE parent = `tabUser`.name
        )
    """
}).insert()

# Approvers (for reject)
approvers = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Sales Approvers",
    "reference_doctype": "User",
    "filters_type": "JSON",
    "filters": frappe.as_json([["role", "=", "Sales Approver"]])
}).insert()
```

### Step 2: Create AC Actions

```python
# Both workflow actions as AC Actions
frappe.get_doc({
    "doctype": "AC Action",
    "action": "approve"
}).insert()

frappe.get_doc({
    "doctype": "AC Action",
    "action": "reject"
}).insert()
```

### Step 3: Create AC Resource

```python
ac_resource = frappe.get_doc({
    "doctype": "AC Resource",
    "type": "DocType",
    "doctype": "Sales Order",
    "managed_actions": "Select",
    "actions": [
        {"action": "approve"},
        {"action": "reject"}
    ]
}).insert()
```

### Step 4: Create Separate Rules

```python
# Approve: Only territory managers
approve_rule = frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Territory Managers Can Approve",
    "rule_type": "Permit",
    "resource": ac_resource.name,
    "principals": [{"principal": territory_mgr.name}],
    "resources": [],  # All records
    "actions": [{"action": "approve"}]
}).insert()

# Reject: Anyone with role
reject_rule = frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Approvers Can Reject",
    "rule_type": "Permit",
    "resource": ac_resource.name,
    "principals": [{"principal": approvers.name}],
    "resources": [],  # All records
    "actions": [{"action": "reject"}]
}).insert()
```

**Result**: Territory managers see both "Approve" and "Reject", non-territory approvers only see "Reject"

## Example 9: Testing Permissions for Different Users

**Goal**: Allow administrators to preview what another user can see, useful for testing and debugging permissions.

### Step 1: Create Query Filter with User Context

```python
# Query filter that uses the 'user' variable
user_dept_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "User Department Customers",
    "reference_doctype": "Customer",
    "filters_type": "Python",
    "filters": """
# The 'user' variable is automatically provided
user_dept = frappe.db.get_value("User", user, "department")
if user_dept:
    conditions = f"`tabCustomer`.`territory` = {frappe.db.escape(user_dept)}"
else:
    conditions = "1=0"  # No access if no department
"""
}).insert()
```

### Step 2: Test Filter for Different Users

```python
# Get the filter document
query_filter = frappe.get_doc("Query Filter", "User Department Customers")

# Test for current user (default behavior)
sql_for_current_user = query_filter.get_sql()
print(f"Current user SQL: {sql_for_current_user}")

# Test for another user (admin preview)
sql_for_john = query_filter.get_sql(user="john@example.com")
print(f"John's SQL: {sql_for_john}")

sql_for_jane = query_filter.get_sql(user="jane@example.com")
print(f"Jane's SQL: {sql_for_jane}")
```

### Step 3: Use in Report with Preview Feature

```python
def execute(filters=None):
    columns = get_columns()
    
    # Check if admin wants to preview for another user
    preview_user = filters.get("preview_for_user")
    
    if preview_user and frappe.has_permission("User", "read"):
        # Admin can preview for another user
        result = get_resource_filter_query(
            report="Customer Report",
            action="read",
            user=preview_user
        )
    else:
        # Normal evaluation for current user
        result = get_resource_filter_query(
            report="Customer Report",
            action="read"
        )
    
    if result.get("access") == "none":
        return columns, []
    
    ac_filter = result.get("query", "1=1")
    
    data = frappe.db.sql(f"""
        SELECT * FROM `tabCustomer`
        WHERE {ac_filter}
    """, as_dict=True)
    
    return columns, data
```

### Step 4: Add Filter to Report

```python
# In get_filters() function
def get_filters():
    filters = [
        # ... other filters ...
    ]
    
    # Add preview option for users with permission
    if frappe.has_permission("User", "read"):
        filters.append({
            "fieldname": "preview_for_user",
            "label": "Preview For User",
            "fieldtype": "Link",
            "options": "User",
            "description": "See what this user can access (admin only)"
        })
    
    return filters
```

**Use Cases**:
- **Testing**: Verify permissions work correctly for different users without switching accounts
- **Debugging**: Troubleshoot why a user can't see certain records
- **Auditing**: Generate access reports showing what different users can see
- **Support**: Help users understand their access without needing their credentials

**Important Notes**:
- The `user` parameter flows through the entire AC Rule evaluation chain:
  - `get_resource_filter_query(user=...)` → passes to `get_resource_filter_sql()`
  - `get_resource_filter_sql(user=...)` → passes to `get_sql()`
  - `get_sql(user=...)` → available as `user` variable in Python filters
- By default, `user` is set to `frappe.session.user` if not provided
- Use `frappe.session.user` for normal operations; use explicit `user` parameter only for preview/testing
- Always check permissions before allowing users to preview other users' access

