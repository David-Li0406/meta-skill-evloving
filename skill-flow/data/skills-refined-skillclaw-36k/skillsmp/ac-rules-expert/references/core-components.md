# Core Components

The AC Rule system consists of four main DocTypes that work together to provide fine-grained access control.

## AC Rule (Main DocType)

**Location**: `tweaks/tweaks/doctype/ac_rule/`

The central component that defines access control rules.

**Key Fields**:
- `title`: Human-readable name for the rule
- `type`: Either "Permit" or "Forbid"
- `resource`: Link to AC Resource (what is being accessed)
- `actions`: List of actions this rule applies to (read, write, delete, etc.)
- `principals`: Table of Query Filters defining who this rule applies to
- `resources`: Table of Query Filters defining which records this rule applies to
- `valid_from`/`valid_upto`: Optional date range for rule validity
- `disabled`: Flag to disable the rule

**Logic**:
```python
# Principal filtering (WHO has access)
allowed_users = (M1 OR M2) AND NOT (E1 OR E2)

# Resource filtering (WHAT records they can access)
allowed_records = (M1 OR M2) AND NOT (E1 OR E2)

# If no resource filters are defined, applies to ALL records
```

**Important Methods**:
- `validate()`: Validates rule configuration and resource filters
- `resolve_principals()`: Resolves principal filters into metadata
- `resolve_resources()`: Resolves resource filters into metadata
- `validate_resource_filters()`: Ensures filters match the resource's doctype/report

## Query Filter

**Location**: `tweaks/tweaks/doctype/query_filter/`

Reusable filter definitions used in both principal and resource filtering.

**Key Fields**:
- `filter_name`: Human-readable name
- `reference_doctype`: DocType this filter applies to (e.g., "User", "Role", "Customer")
- `reference_docname`: Specific document name (for single-record filters)
- `reference_report`: Report this filter applies to
- `filters_type`: "JSON", "Python", or "SQL"
- `filters`: The actual filter code/definition

**Filter Types**:

### 1. JSON Filters (Default)
- Uses Frappe's standard filter syntax
- Example: `[["status", "=", "Active"]]`
- Most common for doctype filtering
- Automatically converted to SQL using `frappe.get_all()`

### 2. SQL Filters
- Direct SQL WHERE clause
- Example: `status = 'Active' AND tenant_id = 1`
- Used for complex conditions

### 3. Python Filters
- Python code that sets `conditions` variable OR `filters` variable
- **Available variables in context**:
  - `resource`: The Query Filter document dict
  - `conditions`: String variable to set SQL WHERE clause (returned as-is)
  - `filters`: Dict/array variable to set Frappe filters (converted to SQL)
  - `user`: Username being evaluated (defaults to `frappe.session.user`, but can be overridden)
- **Two output options**:
  1. **conditions**: Set SQL WHERE clause directly (returned as-is)
  2. **filters**: Set Frappe filter dict/array (converted to SQL like JSON filters)
- If both are set, `conditions` takes precedence
- If neither is set, returns "1=0" (no match)
- Used for dynamic filtering based on context

**Examples**:
```python
# Option 1: Using conditions (direct SQL)
# The 'user' variable is automatically available in Python filters
conditions = f"status = 'Active' AND tenant_id = {frappe.db.get_value('User', user, 'tenant_id')}"

# Option 2: Using filters (like JSON)
filters = [["status", "=", "Active"], ["tenant_id", "=", 1]]
# or
filters = {"status": "Active", "tenant_id": 1}
```

**Important Methods**:
- `get_sql(user=None)`: Converts filter to SQL WHERE clause
  - `user`: Optional username to evaluate the filter for (defaults to `frappe.session.user`)
  - Useful when evaluating rules for a different user (e.g., admin checking another user's permissions)
- Uses `@frappe.request_cache` for performance optimization

**User Parameter**:
The `user` parameter allows evaluating filters in the context of a specific user, which is essential when:
- An administrator needs to preview what another user can see
- Testing permissions for different users
- Auditing access control rules

```python
# Evaluate filter for current user (default)
sql = query_filter.get_sql()

# Evaluate filter for specific user
sql = query_filter.get_sql(user="john@example.com")

# In Python-type filters, the user variable is available
filters = """
# user variable is automatically available
user_dept = frappe.db.get_value("User", user, "department")
conditions = f"`tabCustomer`.`account_manager` = {frappe.db.escape(user)}"
"""
```

**SQL Generation Logic**:
```python
def get_sql(query_filter):
    if filters_type == "SQL":
        return filters  # Direct SQL
    
    if filters_type == "Python":
        # Execute Python code with conditions and filters variables
        safe_exec(filters, ...)
        # Check conditions first
        if conditions:
            return conditions
        # Fall back to filters dict/array
        if filters is not None:
            return build_sql_from_filters(filters)
        return "1=0"  # Neither set
    
    if filters_type == "JSON":
        # Use frappe.get_all() to generate SQL
        sql = frappe.get_all(reference_doctype, filters=filters, run=0)
        return f"`tab{reference_doctype}`.`name` IN ({sql})"
```

## AC Resource

**Location**: `tweaks/tweaks/doctype/ac_resource/`

Defines what is being accessed (the "resource").

**Resource Types**:
- **DocType**: Access control for a specific DocType
- **Report**: Access control for a specific Report

**Key Fields**:
- `type`: Type of resource
- `document_type`: DocType name (for DocType resources)
- `report`: Report name (for Report resources)
- `fieldname`: Optional field-level access control (Reports only)
- `managed_actions`: "All Actions" or "Select"
- `actions`: Table of specific actions (if "Select" is chosen)

**Important Limitations**:

⚠️ **Fieldname is NOT supported for DocType resources** - The `fieldname` field is automatically hidden when creating a DocType resource. Field-level access control is only available for Report resources. When type is set to "DocType", access control applies to the entire doctype, not individual fields.

## AC Action

**Location**: `tweaks/tweaks/doctype/ac_action/`

Defines the actions that can be controlled (read, write, delete, create, etc.).

Standard actions are inserted on install via `after_install()` hook.

Common actions include:
- read
- write
- create
- delete
- submit
- cancel
- amend
- print
- email
- import
- export
- set_user_permissions
- share
- report

## Creating Components

### Create Query Filter

```python
# Create a reusable principal filter
principal_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Sales Team",
    "reference_doctype": "User",
    "filters_type": "JSON",
    "filters": frappe.as_json([["department", "=", "Sales"]])
}).insert()

# Create a reusable resource filter
resource_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Active Customers",
    "reference_doctype": "Customer",
    "filters_type": "JSON",
    "filters": frappe.as_json([["status", "=", "Active"]])
}).insert()
```

### Create AC Resource

```python
# Create AC Resource for a DocType
resource = frappe.get_doc({
    "doctype": "AC Resource",
    "type": "DocType",
    "document_type": "Customer",
    "managed_actions": "Select",
    "actions": [
        {"action": "Read"},
        {"action": "Write"},
        {"action": "Delete"}
    ]
}).insert()

# Create AC Resource for a Report
resource = frappe.get_doc({
    "doctype": "AC Resource",
    "type": "Report",
    "report": "Sales Report",
    "managed_actions": "Select",
    "actions": [{"action": "Read"}]
}).insert()
```

### Create AC Rule

```python
rule = frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Sales Team Active Customer Access",
    "type": "Permit",
    "resource": "Customer",  # Must be created first
    "actions": [
        {"action": "Read"},
        {"action": "Write"}
    ],
    "principals": [
        {"filter": principal_filter.name, "exception": 0}
    ],
    "resources": [
        {"filter": resource_filter.name, "exception": 0}
    ]
}).insert()
```

## Using Exceptions

Exceptions allow you to exclude specific users or records from a rule:

```python
# Allow all sales team EXCEPT specific users
rule.principals = [
    {"filter": "Sales Team", "exception": 0},  # Include sales team
    {"filter": "Suspended Users", "exception": 1}  # Exclude suspended
]

# Allow all active customers EXCEPT VIP customers (handled differently)
rule.resources = [
    {"filter": "Active Customers", "exception": 0},  # Include active
    {"filter": "VIP Customers", "exception": 1}  # Exclude VIP
]
```

## Dynamic Filters with Python

Use current user context for filtering:

```python
# Principal filter based on user metadata
# The 'user' variable is automatically provided in Python filters
filters = """
user_dept = frappe.db.get_value("User", user, "department")
conditions = f"`tabUser`.`department` = {frappe.db.escape(user_dept)}"
"""

# Resource filter based on user's assigned records
filters = """
# 'user' variable contains the username being evaluated
conditions = f"`tabCustomer`.`account_manager` = {frappe.db.escape(user)}"
"""
```

## Complex SQL Filters

Multi-table joins or complex conditions:

```python
# Resource filter with subquery
filters = """
customer_type IN (
    SELECT allowed_type 
    FROM `tabUser Permissions` 
    WHERE parent = '{user}'
) 
AND status != 'Cancelled'
"""

# Principal filter with EXISTS clause
filters = """
EXISTS (
    SELECT 1 
    FROM `tabTeam Member` tm
    WHERE tm.user = `tabUser`.`name`
    AND tm.team = 'Sales Team'
)
"""
```
