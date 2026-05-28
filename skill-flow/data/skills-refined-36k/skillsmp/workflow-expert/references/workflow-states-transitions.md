# Workflow States and Transitions

This document provides detailed information about configuring workflow states and transitions.

## Workflow States

Workflow states represent the different stages a document can be in during its lifecycle.

### State Properties

Each state has the following properties:

#### state (Required)
- **Type**: Link to Workflow State
- **Description**: The name of the state
- **Example**: "Pending Approval", "Approved", "Rejected"
- **Note**: States are created separately in the Workflow State DocType

#### doc_status (Required)
- **Type**: Select (0, 1, 2)
- **Description**: Document status for this state
- **Values**:
  - **0 (Draft)**: Document is in draft, editable
  - **1 (Submitted)**: Document is submitted, restricted editing
  - **2 (Cancelled)**: Document is cancelled, no editing
- **Impact**: Determines document's editable state and validity

#### allow_edit (Required)
- **Type**: Link to Role
- **Description**: Role that can edit document in this state
- **Special Value**: "All" allows any role with document permissions
- **Example**: "HR Manager", "Purchase Manager", "All"
- **Note**: This is enforced by Frappe's permission system

#### update_field (Optional)
- **Type**: Select (populated from DocType fields)
- **Description**: Field to automatically update when entering this state
- **Use Cases**:
  - Update status field
  - Set approval date
  - Mark as processed
- **Example**: "status", "approval_date", "stage"

#### update_value (Optional)
- **Type**: Data
- **Description**: Value to set for update_field
- **Example**: If update_field="status", value could be "Approved"
- **Note**: Must be compatible with the field type

#### is_optional_state (Optional)
- **Type**: Check
- **Default**: 0 (unchecked)
- **Description**: If checked, workflow actions are NOT created for this state
- **Use Cases**:
  - Intermediate automated states
  - Terminal states (no further actions needed)
  - States that don't require user intervention

#### avoid_status_override (Optional)
- **Type**: Check
- **Default**: 0
- **Description**: If checked, this state won't override document status in list view
- **Per-State**: More granular than workflow-level override_status

#### send_email (Optional)
- **Type**: Check
- **Default**: 1 (checked)
- **Description**: Whether to send email when document transitions TO this state
- **Use Case**: Disable for automated or intermediate states

#### next_action_email_template (Optional)
- **Type**: Link to Email Template
- **Description**: Custom email template for workflow action notifications
- **Fallback**: Uses default template if not specified
- **Context**: Template has access to doc and actions

#### message (Optional)
- **Type**: Text
- **Description**: Message to display to users when document is in this state
- **Display**: Shows as alert/info message in document form
- **Use Case**: Provide context or instructions

### State Design Guidelines

#### Naming Conventions

**Good Names:**
- "Pending Approval" - Clear and descriptive
- "Approved" - Simple and direct
- "Manager Review" - Indicates who acts
- "Awaiting Payment" - Describes wait condition

**Avoid:**
- "State 1", "State 2" - Not descriptive
- "InProgress" - Use proper spacing
- Abbreviations unless widely understood

#### DocStatus Mapping

Choose docstatus based on business meaning:

| DocStatus | Meaning | When to Use |
|-----------|---------|-------------|
| 0 (Draft) | Editable, not final | Initial states, rejected states, revision states |
| 1 (Submitted) | Locked, officially recorded | Approved states, completed states |
| 2 (Cancelled) | Void, no longer valid | Cancelled or voided states |

**Example Mapping:**
```
Draft → docstatus=0 (still being created)
Pending Approval → docstatus=0 (not yet official)
Approved → docstatus=1 (official and locked)
Rejected → docstatus=0 (can be revised)
Cancelled → docstatus=2 (voided)
```

#### Edit Permissions

Set allow_edit based on who should modify the document:

```python
# Only HR can edit when pending approval
{"state": "Pending Approval", "allow_edit": "HR Manager"}

# Only submitter can edit rejected documents
{"state": "Rejected", "allow_edit": "Employee"}

# Anyone with permissions can edit approved docs
{"state": "Approved", "allow_edit": "All"}

# Restrict critical state to senior role
{"state": "Final Approval", "allow_edit": "Director"}
```

#### Field Updates

Common field update patterns:

```python
# Update status field
{
    "update_field": "status",
    "update_value": "Approved"
}

# Set approval date
{
    "update_field": "approval_date",
    "update_value": frappe.utils.today()  # Note: This is conceptual; use hooks for dynamic values
}

# Mark as processed
{
    "update_field": "processed",
    "update_value": "1"
}

# Set priority
{
    "update_field": "priority",
    "update_value": "High"
}
```

**Limitations:**
- update_value must be a string literal (no dynamic values)
- For dynamic values (like dates), use after_transition hook instead

#### Optional States

Mark states as optional when:

```python
# Automated intermediate state
{
    "state": "Auto Processing",
    "is_optional_state": 1,
    "send_email": 0  # No email needed for automated state
}

# Terminal state (no further actions)
{
    "state": "Completed",
    "doc_status": "1",
    "is_optional_state": 1  # No actions needed after completion
}

# System state
{
    "state": "System Approved",
    "is_optional_state": 1,
    "message": "Automatically approved by system rules"
}
```

## Workflow Transitions

Transitions define how documents move from one state to another.

### Transition Properties

#### state (Required)
- **Type**: Link to Workflow State
- **Description**: Starting state (current state)
- **Example**: "Pending Approval"
- **Note**: Must be defined in states table

#### action (Required)
- **Type**: Link to Workflow Action Master
- **Description**: Action name displayed to user
- **Example**: "Approve", "Reject", "Submit"
- **User Sees**: This as a button in the form

#### next_state (Required)
- **Type**: Link to Workflow State
- **Description**: Destination state after transition
- **Example**: "Approved"
- **Validation**: Must be defined in states table

#### allowed (Required)
- **Type**: Link to Role
- **Description**: Role allowed to perform this transition
- **Special Value**: "All" allows any role with document access
- **Example**: "HR Manager", "Purchase Approver"
- **Note**: User must have this role to see the action

#### allow_self_approval (Optional)
- **Type**: Check
- **Default**: 1 (checked)
- **Description**: Whether document owner can approve their own document
- **Security**: Set to 0 to prevent self-approval
- **Example**: Expense claims should have self-approval disabled

#### send_email_to_creator (Optional)
- **Type**: Check
- **Default**: 0
- **Depends On**: allow_self_approval == 1
- **Description**: Whether to send workflow action email to document creator
- **Use Case**: When self-approval is allowed but creator should still be notified

#### condition (Optional)
- **Type**: Code (Python expression)
- **Description**: Python expression that must evaluate to True for transition to be available
- **Context**: Has access to `doc` variable
- **Example**: `doc.grand_total > 10000`

### Transition Design Guidelines

#### Naming Actions

**Good Action Names:**
- "Approve" - Clear intent
- "Submit for Approval" - Descriptive
- "Send Back" - User-friendly
- "Request Changes" - Specific

**Avoid:**
- "OK" - Too vague
- "Next" - Not descriptive
- "Process" - Unclear

#### State Flow

Design logical state flows:

```
✅ Good: Draft → Pending → Approved
✅ Good: Approved → Cancelled (valid cancellation)
❌ Bad: Approved → Draft (can't un-submit)
❌ Bad: Cancelled → Any (can't revive cancelled)
```

#### DocStatus Transitions

Valid docstatus transitions:

```
Draft (0) → Draft (0) ✅
Draft (0) → Submitted (1) ✅
Draft (0) → Cancelled (2) ❌ (must submit first)
Submitted (1) → Draft (0) ❌ (can't un-submit)
Submitted (1) → Submitted (1) ✅
Submitted (1) → Cancelled (2) ✅
Cancelled (2) → Any ❌ (cannot transition from cancelled)
```

#### Role Assignment

Assign roles strategically:

```python
# Submitter can initiate
{
    "state": "Draft",
    "action": "Submit",
    "allowed": "Employee",
    "allow_self_approval": 1
}

# Approver can't self-approve
{
    "state": "Pending",
    "action": "Approve",
    "allowed": "Manager",
    "allow_self_approval": 0
}

# Anyone can view-only transition
{
    "state": "Approved",
    "action": "Archive",
    "allowed": "All",
    "allow_self_approval": 1
}
```

#### Self-Approval Rules

Guidelines for self-approval:

```python
# Allow self-approval for submissions
allow_self_approval = 1  # Employee submits own request

# Prevent self-approval for approvals
allow_self_approval = 0  # Manager can't approve if they submitted

# Consider business rules
if transition_is_approval:
    allow_self_approval = 0
elif transition_is_submission or transition_is_revision:
    allow_self_approval = 1
```

### Transition Conditions

Conditions allow dynamic transition availability based on document data.

#### Basic Conditions

```python
# Amount-based
"doc.grand_total > 50000"

# Status-based
"doc.status == 'Verified'"

# Date-based
"doc.posting_date == frappe.utils.today()"

# Boolean field
"doc.is_urgent == 1"

# Comparison
"doc.quantity > 100 and doc.rate < 1000"
```

#### Advanced Conditions

```python
# Lookup value
"frappe.db.get_value('Customer', doc.customer, 'customer_type') == 'Corporate'"

# Check list membership
"doc.category in ['A', 'B', 'C']"

# Multiple conditions
"doc.grand_total > 10000 and doc.payment_terms != 'Cash' and doc.docstatus == 0"

# Session-based
"frappe.session.user != doc.owner"

# Date comparison
"doc.creation > frappe.utils.add_to_date(frappe.utils.now_datetime(), days=-7, as_datetime=True)"
```

#### Available Functions in Conditions

```python
# Database queries
frappe.db.get_value(doctype, name, fieldname)
frappe.db.get_list(doctype, filters={}, fields=[])

# Session info
frappe.session.user
frappe.session.data

# Date utilities
frappe.utils.now_datetime()
frappe.utils.get_datetime(date_string)
frappe.utils.add_to_date(date, days=0, months=0, years=0)
frappe.utils.now()
```

#### Condition Best Practices

1. **Keep Simple**: Complex logic should be in hooks, not conditions
2. **Test Thoroughly**: Conditions that always fail block transitions
3. **Document**: Add comments explaining the business rule
4. **Performance**: Avoid expensive operations in conditions
5. **Error Handling**: Conditions should return bool, not raise errors

#### Condition Examples by Use Case

**Amount-Based Routing:**
```python
# Small orders go to Manager
condition = "doc.grand_total < 10000"

# Large orders go to Director
condition = "doc.grand_total >= 10000 and doc.grand_total < 100000"

# Very large orders go to CFO
condition = "doc.grand_total >= 100000"
```

**Time-Based Restrictions:**
```python
# Only during business hours (requires custom implementation)
condition = "doc.is_business_hours == 1"

# Recent documents only
condition = "doc.creation > frappe.utils.add_to_date(frappe.utils.now_datetime(), days=-30, as_datetime=True)"

# Future-dated documents
condition = "doc.posting_date > frappe.utils.today()"
```

**Status-Based:**
```python
# Only verified documents
condition = "doc.verification_status == 'Verified'"

# Exclude certain categories
condition = "doc.category not in ['Internal', 'Test']"

# Combined status check
condition = "doc.status == 'Ready' and doc.quality_check == 'Passed'"
```

**User-Based:**
```python
# Not the creator
condition = "frappe.session.user != doc.owner"

# Specific users only (use with caution)
condition = "frappe.session.user in ['user1@example.com', 'user2@example.com']"

# Based on user property
condition = "frappe.db.get_value('User', frappe.session.user, 'user_type') == 'System User'"
```

## State Transition Diagrams

### Linear Workflow
```
Draft → Pending → Approved
  ↓         ↓
Cancelled  Rejected
```

### Branching Workflow
```
Draft → Pending Approval
          ↓         ↓
       Approved  Rejected
                    ↓
                  Draft (revise)
```

### Multi-Level Approval
```
Draft → Manager Review → Director Review → CFO Review → Approved
          ↓                ↓                 ↓
        Rejected        Rejected          Rejected
```

### Conditional Routing
```
Draft → Submit
          ↓
    (if amount < 10k)  → Manager → Approved
          ↓
    (if amount >= 10k) → Director → Approved
```

## Common Patterns

### Pattern 1: Simple Approval
```python
states = [
    {"state": "Draft", "doc_status": "0", "allow_edit": "User"},
    {"state": "Pending", "doc_status": "0", "allow_edit": "Approver"},
    {"state": "Approved", "doc_status": "1", "allow_edit": "Approver"}
]

transitions = [
    {"state": "Draft", "action": "Submit", "next_state": "Pending", "allowed": "User"},
    {"state": "Pending", "action": "Approve", "next_state": "Approved", "allowed": "Approver"}
]
```

### Pattern 2: Approval with Rejection
```python
transitions = [
    {"state": "Draft", "action": "Submit", "next_state": "Pending", "allowed": "User"},
    {"state": "Pending", "action": "Approve", "next_state": "Approved", "allowed": "Approver"},
    {"state": "Pending", "action": "Reject", "next_state": "Rejected", "allowed": "Approver"},
    {"state": "Rejected", "action": "Revise", "next_state": "Draft", "allowed": "User"}
]
```

### Pattern 3: Multi-Level with Skip
```python
transitions = [
    # Low amount - skip to approved
    {
        "state": "Pending L1",
        "action": "Approve",
        "next_state": "Approved",
        "allowed": "Manager",
        "condition": "doc.amount < 10000"
    },
    # High amount - needs L2
    {
        "state": "Pending L1",
        "action": "Forward",
        "next_state": "Pending L2",
        "allowed": "Manager",
        "condition": "doc.amount >= 10000"
    }
]
```

## Validation Rules

Frappe enforces these rules on workflow save:

1. **All referenced states must exist**: States in transitions must be in states table
2. **Cannot transition from Cancelled**: No transitions can start from docstatus=2
3. **Cannot un-submit**: Cannot go from docstatus=1 to docstatus=0
4. **Cannot cancel draft**: Cannot go from docstatus=0 to docstatus=2
5. **Valid conditions**: Conditions must be valid Python expressions

## Testing State Transitions

```python
def test_state_transitions():
    """Test that all transitions work correctly."""
    doc = create_test_document()
    
    # Test each transition
    assert doc.workflow_state == "Draft"
    
    apply_workflow(doc, "Submit")
    assert doc.workflow_state == "Pending"
    assert doc.docstatus == 0
    
    apply_workflow(doc, "Approve")
    assert doc.workflow_state == "Approved"
    assert doc.docstatus == 1
```

## Troubleshooting

### Transition Not Showing

**Check:**
1. Does user have the required role?
2. Is the condition (if any) satisfied?
3. Is current state correct?
4. Is the transition configured correctly?

**Debug:**
```python
# Check available transitions
from frappe.model.workflow import get_transitions
transitions = get_transitions(doc)
print(transitions)

# Check user roles
print(frappe.get_roles())

# Test condition
condition = "doc.grand_total > 10000"
result = frappe.safe_eval(condition, {"doc": doc.as_dict()})
print(f"Condition result: {result}")
```

### State Not Changing

**Check:**
1. Is there a validation error?
2. Check before_transition hook
3. Review error logs
4. Verify transition is valid per docstatus rules

### Field Not Updating

**Check:**
1. Is update_field spelled correctly?
2. Does the field exist in DocType?
3. Is update_value compatible with field type?
4. Check field permissions

## Best Practices

1. **Start Simple**: Begin with basic states, add complexity as needed
2. **Clear Names**: Use business-friendly state and action names
3. **Logical Flow**: Ensure state transitions make business sense
4. **Test Thoroughly**: Test all transitions with all roles
5. **Document Conditions**: Add comments explaining business rules
6. **Handle Rejections**: Always provide a path back for rejected items
7. **Plan Docstatus**: Think through submission and cancellation points
8. **Use Optional States**: For automated or terminal states
9. **Validate Early**: Use conditions to prevent invalid transitions
10. **Monitor Usage**: Track which transitions are actually used
