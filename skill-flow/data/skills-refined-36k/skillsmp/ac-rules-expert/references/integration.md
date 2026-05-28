# Integration with Frappe Permissions

This document explains how AC Rules integrate with Frappe's permission system for DocTypes, Reports, and future Workflow integration.

## Implementation Status

**Current State**:
- ✅ **DocTypes**: Fully implemented - Automatic permission enforcement via Frappe hooks
- ✅ **Reports**: Fully functional - Manual integration required (call API and inject SQL)
- ✅ **Workflows**: Fully implemented - Automatic transition filtering and permission enforcement
- 🔄 **Migration Plan**: Migration from deprecated systems can now begin

**Deprecated Systems** (Do Not Use):
- ❌ **Event Scripts** - Legacy system, deprecated in favor of AC Rules
- ❌ **Server Script Permission Policy** - Legacy permission system, deprecated in favor of AC Rules

## DocType Integration (Automatic)

DocType integration is **fully available** and automatically enforces AC Rules through Frappe's permission query condition hooks.

### How It Works

Implemented in `tweaks/hooks.py`:

```python
permission_query_conditions = {
    "*": (
        event_script_hooks["permission_query_conditions"]["*"]
        + permission_hooks["permission_query_conditions"]["*"]
        + ["tweaks.tweaks.doctype.ac_rule.ac_rule_utils.get_permission_query_conditions"]
    )
}

write_permission_query_conditions = {
    "*": ["tweaks.tweaks.doctype.ac_rule.ac_rule_utils.get_write_permission_query_conditions"]
}
```

### Permission Query Conditions Hook

Filters list views and queries for read/select operations:
- Called by Frappe when loading list views and performing read queries
- Returns SQL WHERE clause to filter records based on AC Rules with action="read"
- Administrator always has full access
- Unmanaged resources return empty string (fall through to standard Frappe permissions)

### Write Permission Query Conditions Hook

Filters queries for write operations:
- Called by Frappe when performing write operations
- Accepts `ptype` parameter with actions: write, create, submit, cancel, delete
- Returns SQL WHERE clause to filter records based on AC Rules for the specified action
- Administrator always has full access
- Unmanaged resources return empty string (fall through to standard Frappe permissions)

### Implementation Details

- Both hooks use a shared internal helper function `_get_permission_query_conditions_for_doctype(doctype, user, action)`
- Actions are normalized using `scrub()` to ensure consistent formatting
- The write hook maps the ptype parameter to the appropriate AC Action using `scrub(ptype or "write")`

### Key Features

- Works alongside existing permission systems (Event Scripts, Server Script Permission Policy)
- Administrator always has full access
- Unmanaged doctypes fall through to standard Frappe permissions
- Supports Permit/Forbid rule logic
- Handles resource filters for both read and write operations
- **No manual integration required** for DocTypes (unlike Reports)

## Report Integration (Manual)

Reports must **manually** integrate AC Rules by calling the API to get filter queries.

### Integration Steps

1. Import the utility function
2. Call `get_resource_filter_query()` in your report
3. Check the access level
4. Inject the SQL filter into your query

### Example Implementation

```python
# In your report's get_data() or execute() function
from tweaks.tweaks.doctype.ac_rule.ac_rule_utils import get_resource_filter_query

def execute(filters=None):
    # Get AC Rule filter query for this report
    result = get_resource_filter_query(
        report="Your Report Name",
        action="read",
        user=frappe.session.user
    )
    
    # Build your SQL query with the AC Rule filter
    if result.get("access") == "none":
        return [], []  # User has no access
    
    ac_filter = result.get("query", "1=1")
    
    data = frappe.db.sql(f"""
        SELECT * FROM `tabYourDocType`
        WHERE {ac_filter}
        AND your_other_conditions
    """, as_dict=True)
    
    return columns, data
```

### Access Levels

The `access` field in the result can be:

- **total**: User has access to all records
  - Query = "1=1"
  - No filtering needed
  
- **partial**: User has conditional access
  - Query contains SQL WHERE clause
  - Must inject into report query
  
- **none**: User has no access
  - Query = "1=0"
  - Should return empty results
  
- **unmanaged**: Resource not managed by AC Rules
  - Query may be empty or "1=1"
  - Fall through to standard Frappe permissions

### Complete Example

```python
from tweaks.tweaks.doctype.ac_rule.ac_rule_utils import get_resource_filter_query

def execute(filters=None):
    columns = get_columns()
    
    # Get AC Rule filter
    result = get_resource_filter_query(
        report="Sales Customer Report",
        action="read"
    )
    
    # Handle different access levels
    if result.get("access") == "none":
        return columns, []
    
    ac_filter = result.get("query", "1=1")
    
    # Build your query with AC filter
    conditions = []
    
    # Add report filters
    if filters.get("from_date"):
        conditions.append(f"creation >= '{filters.get('from_date')}'")
    if filters.get("to_date"):
        conditions.append(f"creation <= '{filters.get('to_date')}'")
    
    # Add AC filter
    conditions.append(f"({ac_filter})")
    
    where_clause = " AND ".join(conditions)
    
    data = frappe.db.sql(f"""
        SELECT 
            name,
            customer_name,
            account_manager,
            status,
            creation
        FROM `tabCustomer`
        WHERE {where_clause}
        ORDER BY creation DESC
    """, as_dict=True)
    
    return columns, data
```

## API Endpoints

All endpoints are whitelisted with `@frappe.whitelist()`:

### 1. Get Rule Map

```python
@frappe.whitelist()
def get_rule_map()
```

Returns the complete rule map structure.

### 2. Get Resource Rules

```python
@frappe.whitelist()
def get_resource_rules(
    resource="",      # AC Resource name
    doctype="",       # DocType name
    report="",        # Report name
    type="",          # "doctype" or "report"
    key="",           # DocType/Report name
    fieldname="",     # Optional field name
    action="",        # Action name (default: "read")
    user="",          # User (default: current user)
)
```

Returns rules that apply to a specific resource/action for a user.

**Response**:
```python
{
    "rules": [
        {
            "name": "ACL-2025-0001",
            "title": "Sales Team Read Access",
            "type": "Permit",
            "principals": [...],
            "resources": [...]
        }
    ],
    "unmanaged": False  # True if resource not managed by AC Rules
}
```

### 3. Get Resource Filter Query

```python
@frappe.whitelist()
def get_resource_filter_query(
    resource="",
    doctype="",
    report="",
    type="",
    key="",
    fieldname="",
    action="",
    user="",
)
```

Returns the SQL WHERE clause for filtering records.

**Response**:
```python
{
    "query": "(status = 'Active') AND NOT (status = 'Archived')",
    "access": "partial",  # "total", "none", "partial", or "unmanaged"
    "unmanaged": False
}
```

### 4. Check Resource Access

```python
@frappe.whitelist()
def has_resource_access(
    resource="",
    doctype="",
    report="",
    type="",
    key="",
    fieldname="",
    action="",
    user="",
)
```

Checks if a user has any access to a resource/action.

**Note**: This function only checks if the user has ANY rule for the doctype/action combination. It does NOT verify permission for a specific document. For document-level permission checks, use `has_ac_permission` instead.

**Response**:
```python
{
    "access": True,
    "unmanaged": False
}
```

### 5. Check AC Permission (Document-Level)

```python
@frappe.whitelist()
def has_ac_permission(
    docname="",
    doctype="",
    action="",
    user="",
)
```

Checks if a user has AC Rules permission for a specific document and action.

**This is the recommended function for workflow and action permission checks** as it verifies that the user has permission to perform the action on the specific document, not just any document of that type.

**Key Features**:
- Generates SQL to verify if the specific document matches the AC Rules filters
- Executes SQL to determine permission
- Validates doctype to prevent SQL injection
- Handles unmanaged resources, Administrator user, and all access levels (total, partial, none)
- Only System Manager can check permissions for other users

**Arguments**:
- `docname`: Document name
- `doctype`: DocType name
- `action`: Action name (e.g., "read", "write", "approve", "reject")
- `user`: User name (defaults to current user, only System Manager can check for other users)

**Response**:
```python
True  # User has permission for this specific document
False # User does not have permission
```

**Usage Example**:
```python
from tweaks.tweaks.doctype.ac_rule.ac_rule_utils import has_ac_permission

# Check if user can approve a specific Purchase Order
has_permission = has_ac_permission(
    docname="PO-0001",
    doctype="Purchase Order",
    action="approve",
    user="user@example.com"  # Only System Manager can pass different user
)

if has_permission:
    # User has permission to approve this specific PO
    doc = frappe.get_doc("Purchase Order", "PO-0001")
    doc.approve()
else:
    frappe.throw("You don't have permission to approve this Purchase Order")
```

**Comparison with has_resource_access**:
```python
# has_resource_access: Checks if user has ANY rule
result1 = has_resource_access(doctype="Purchase Order", action="approve")
# Returns True if user has some rule for PO approval (even if not for this specific PO)

# has_ac_permission: Checks if user can act on THIS document
result2 = has_ac_permission(docname="PO-0001", doctype="Purchase Order", action="approve")
# Returns True only if user has permission to approve THIS specific PO
```

## Deprecated Systems

### Server Script Permission Policy (Deprecated)

Located in `tweaks/custom/utils/permissions.py` - **DO NOT USE**:

```python
# DEPRECATED - Do not use
permission_hooks = {
    "permission_query_conditions": {
        "*": ["tweaks.custom.utils.permissions.get_permission_policy_query_conditions"]
    },
    "has_permission": {
        "*": ["tweaks.custom.utils.permissions.has_permission_policy"]
    },
}
```

### Event Scripts (Deprecated)

- Location: `tweaks/tweaks/doctype/event_script/`
- Status: Deprecated in favor of AC Rules
- These will be removed as users migrate to AC Rules

### Migration Path

With DocType AC Rules now implemented, all permission logic should migrate to use AC Rules exclusively. The deprecated systems will be removed in a future release.

## Workflow Integration (Automatic)

Workflow integration is **fully available** and automatically enforces AC Rules through Frappe's workflow permission hooks.

### How It Works

Implemented in `tweaks/hooks.py` and `tweaks/utils/workflow.py`:

```python
# In tweaks/hooks.py
filter_workflow_transitions = ["tweaks.utils.workflow.filter_transitions_by_ac_rules"]

has_workflow_action_permission = [
    "tweaks.utils.workflow.has_workflow_action_permission_via_ac_rules"
]
```

### Integration Points

#### 1. Transition Filtering Hook

**Hook**: `filter_workflow_transitions`  
**Function**: `filter_transitions_by_ac_rules(doc, transitions, workflow)`

Called when displaying available workflow transitions to a user. Filters out transitions the user doesn't have permission for via AC Rules.

**Behavior**:
- Gets all available transitions (already filtered by role)
- For each transition, checks if AC Rules manage that action
- If managed and user has no access → removes transition
- If unmanaged → keeps transition (standard Frappe permissions apply)

#### 2. Transition Permission Check

**Doc Event**: `before_transition`  
**Function**: `check_workflow_transition_permission(doc, method, transition)`

Called before executing a workflow transition. Blocks the transition if user lacks AC Rules permission.

**Behavior**:
- Checks if AC Rules manage the workflow action
- If managed and user has no access → raises `frappe.PermissionError`
- If unmanaged or has access → allows transition to proceed

#### 3. Workflow Action List Filtering

**Hook**: `permission_query_conditions` for "Workflow Action" doctype  
**Function**: `get_workflow_action_permission_query_conditions(user, doctype)`

Filters the Workflow Action list view to only show actions the user can perform.

**Behavior**:
- Gets all distinct (doctype, state, action) triples from open workflow actions
- For each action, checks AC Rules permissions
- Returns SQL WHERE clause that filters based on AC Rules access
- Groups by (doctype, state) and ORs action queries together

#### 4. Action-Level Permission Check

**Hook**: `has_workflow_action_permission`  
**Function**: `has_workflow_action_permission_via_ac_rules(user, transition, doc)`

Called to check if a user should receive workflow action notifications and can execute actions.

**Behavior**:
- Checks if user has AC Rules access to the transition action
- If unmanaged → returns True (user passed role check)
- If managed → returns AC Rules access result

### Action Naming Convention

Workflow actions are automatically normalized using `frappe.scrub()` for AC Rules matching:

- "Approve" → "approve"
- "Reject" → "reject"
- "Submit for Review" → "submit_for_review"
- "Send Back" → "send_back"

**Important**: Create AC Actions using the scrubbed (lowercase, underscored) version.

### Creating Workflow AC Rules

#### Step 1: Create AC Action for Workflow Action

```python
# Create AC Action matching workflow action (scrubbed)
frappe.get_doc({
    "doctype": "AC Action",
    "action": "approve",  # matches "Approve" workflow action
}).insert()
```

#### Step 2: Create AC Resource for DocType

```python
frappe.get_doc({
    "doctype": "AC Resource",
    "type": "DocType",
    "doctype": "Purchase Order",
    "managed_actions": "Select",  # Manage specific actions
    "actions": [
        {"action": "approve"},
        {"action": "reject"}
    ]
}).insert()
```

#### Step 3: Create Principal Filter (Who can perform action)

```python
# Example: Only managers can approve
frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Managers",
    "reference_doctype": "User",
    "filters_type": "JSON",
    "filters": frappe.as_json([["role", "=", "Manager"]])
}).insert()
```

#### Step 4: Create Resource Filter (What can be approved)

```python
# Example: Only POs in user's territory
frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "My Territory POs",
    "reference_doctype": "Purchase Order",
    "filters_type": "SQL",
    "filters": """
        territory IN (
            SELECT territory FROM `tabUser Territory`
            WHERE parent = '{user}'
        )
    """
}).insert()
```

#### Step 5: Create AC Rule

```python
frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Managers Can Approve Territory POs",
    "rule_type": "Permit",
    "resource": "Purchase Order",  # AC Resource name
    "principals": [{"principal": "Managers"}],
    "resources": [{"resource": "My Territory POs"}],
    "actions": [{"action": "approve"}],
    "disabled": 0
}).insert()
```

### Workflow Examples

#### Example 1: Territory-Based Approval

**Goal**: Sales Managers can only approve Sales Orders in their assigned territories.

```python
# Principal: Sales Managers
principal_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Sales Managers",
    "reference_doctype": "User",
    "filters_type": "JSON",
    "filters": frappe.as_json([["role", "=", "Sales Manager"]])
}).insert()

# Resource: Sales Orders in user's territory
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

# AC Resource
ac_resource = frappe.get_doc({
    "doctype": "AC Resource",
    "type": "DocType",
    "doctype": "Sales Order",
    "managed_actions": "Select",
    "actions": [{"action": "approve"}]
}).insert()

# AC Rule
frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Territory-Based Sales Order Approval",
    "rule_type": "Permit",
    "resource": ac_resource.name,
    "principals": [{"principal": principal_filter.name}],
    "resources": [{"resource": resource_filter.name}],
    "actions": [{"action": "approve"}]
}).insert()
```

#### Example 2: Amount-Based Approval Hierarchy

**Goal**: Regular managers approve up to 50k, senior managers up to 200k, directors approve all.

```python
# Resource filters for different amounts
low_amount_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "PO Under 50k",
    "reference_doctype": "Purchase Order",
    "filters_type": "SQL",
    "filters": "grand_total <= 50000"
}).insert()

medium_amount_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "PO 50k-200k",
    "reference_doctype": "Purchase Order",
    "filters_type": "SQL",
    "filters": "grand_total > 50000 AND grand_total <= 200000"
}).insert()

high_amount_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "PO Over 200k",
    "reference_doctype": "Purchase Order",
    "filters_type": "SQL",
    "filters": "grand_total > 200000"
}).insert()

# Principal filters
manager_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Regular Managers",
    "reference_doctype": "User",
    "filters_type": "JSON",
    "filters": frappe.as_json([["role", "=", "Manager"]])
}).insert()

senior_manager_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Senior Managers",
    "reference_doctype": "User",
    "filters_type": "JSON",
    "filters": frappe.as_json([["role", "=", "Senior Manager"]])
}).insert()

director_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Directors",
    "reference_doctype": "User",
    "filters_type": "JSON",
    "filters": frappe.as_json([["role", "=", "Director"]])
}).insert()

# AC Resource
ac_resource = frappe.get_doc({
    "doctype": "AC Resource",
    "type": "DocType",
    "doctype": "Purchase Order",
    "managed_actions": "Select",
    "actions": [{"action": "approve"}]
}).insert()

# Rules for each level
frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Managers Approve PO Under 50k",
    "rule_type": "Permit",
    "resource": ac_resource.name,
    "principals": [{"principal": manager_filter.name}],
    "resources": [{"resource": low_amount_filter.name}],
    "actions": [{"action": "approve"}]
}).insert()

frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Senior Managers Approve PO 50k-200k",
    "rule_type": "Permit",
    "resource": ac_resource.name,
    "principals": [{"principal": senior_manager_filter.name}],
    "resources": [{"resource": medium_amount_filter.name}],
    "actions": [{"action": "approve"}]
}).insert()

frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Directors Approve PO Over 200k",
    "rule_type": "Permit",
    "resource": ac_resource.name,
    "principals": [{"principal": director_filter.name}],
    "resources": [{"resource": high_amount_filter.name}],
    "actions": [{"action": "approve"}]
}).insert()
```

#### Example 3: Department-Based Workflow Actions

**Goal**: Users can only approve expense claims from their own department.

```python
# Resource: Expense Claims from user's department
resource_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "My Department Expense Claims",
    "reference_doctype": "Expense Claim",
    "filters_type": "Python",
    "filters": """
user_dept = frappe.db.get_value('User', '{user}', 'department')
conditions = f"`tabExpense Claim`.`department` = {frappe.db.escape(user_dept)}"
    """
}).insert()

# Principal: Department approvers
principal_filter = frappe.get_doc({
    "doctype": "Query Filter",
    "filter_name": "Expense Approvers",
    "reference_doctype": "User",
    "filters_type": "JSON",
    "filters": frappe.as_json([["role", "=", "Expense Approver"]])
}).insert()

# AC Resource
ac_resource = frappe.get_doc({
    "doctype": "AC Resource",
    "type": "DocType",
    "doctype": "Expense Claim",
    "managed_actions": "Select",
    "actions": [{"action": "approve"}, {"action": "reject"}]
}).insert()

# AC Rule
frappe.get_doc({
    "doctype": "AC Rule",
    "title": "Department-Based Expense Approval",
    "rule_type": "Permit",
    "resource": ac_resource.name,
    "principals": [{"principal": principal_filter.name}],
    "resources": [{"resource": resource_filter.name}],
    "actions": [
        {"action": "approve"},
        {"action": "reject"}
    ]
}).insert()
```

### Key Features

- **No manual integration needed**: Workflow integration is automatic
- **Works alongside role-based permissions**: AC Rules layer on top of standard workflow roles
- **Multiple permission checks**: Filters transitions AND validates before execution
- **Workflow Action list filtering**: Users only see actionable workflow items
- **Action naming**: Use scrubbed action names (lowercase, underscored) in AC Actions
- **Administrator bypass**: Administrator always has full access

### Testing Workflow AC Rules

```python
# Test if user can see a transition
from tweaks.custom.doctype.workflow import get_transitions

doc = frappe.get_doc("Purchase Order", "PO-0001")
transitions = get_transitions(doc, user="test@example.com")
print([t.action for t in transitions])  # Should only show allowed actions

# Test AC Rules for a specific action
from tweaks.tweaks.doctype.ac_rule.ac_rule_utils import has_resource_access

result = has_resource_access(
    doctype="Purchase Order",
    action="approve",
    user="test@example.com"
)
print(result)  # {"access": True/False, "unmanaged": True/False}
```

## Best Practices

1. **For DocTypes**: No integration needed - AC Rules are automatically enforced
2. **For Reports**: Always call `get_resource_filter_query()` and inject SQL
3. **For Workflows**: No integration needed - AC Rules automatically filter transitions and check permissions
4. **Action naming**: Use scrubbed names for workflow actions ("Approve" → "approve")
5. **Check access levels**: Handle "none", "partial", and "total" access appropriately
6. **Combine filters**: Use AND logic to combine AC filter with report filters
7. **Test thoroughly**: Verify access control works as expected for all user roles
8. **Monitor performance**: Complex filters may impact query performance
9. **Use appropriate actions**: Use "read" for reports, "write" for edits, workflow action names for transitions
10. **Handle unmanaged resources**: Fall back to standard Frappe permissions
