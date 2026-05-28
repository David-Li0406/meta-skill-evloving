# Workflow Structure

This document details the complete structure of the Workflow DocType and its related components.

## Workflow DocType

The Workflow DocType is the master configuration that defines how a specific DocType's documents transition between states.

### Primary Fields

#### workflow_name
- **Type**: Data
- **Required**: Yes
- **Unique**: Yes
- **Description**: Name of the workflow (used as document name)
- **Example**: "Purchase Order Approval", "Leave Application Workflow"

#### document_type
- **Type**: Link (DocType)
- **Required**: Yes
- **Description**: The DocType this workflow applies to
- **Note**: Only one active workflow per DocType
- **Example**: "Leave Application", "Purchase Order"

#### is_active
- **Type**: Check
- **Default**: 0
- **Description**: Whether this workflow is active
- **Behavior**: When enabled, all other workflows for the same DocType are automatically disabled

#### workflow_state_field
- **Type**: Data
- **Default**: "workflow_state"
- **Required**: Yes
- **Description**: Name of the field that stores the current workflow state
- **Behavior**: If field doesn't exist, a Custom Field is auto-created

#### override_status
- **Type**: Check
- **Default**: 0
- **Description**: If checked, workflow status will NOT override document status in list view
- **Use Case**: When you want to keep the original document status visible

#### send_email_alert
- **Type**: Check
- **Default**: 0
- **Description**: Whether to send email alerts when workflow actions are available
- **Effect**: Enables automatic email notifications to users with next actions

### Child Tables

#### states (Workflow Document State)
- **Description**: Defines all possible states a document can be in
- **Fields**: See Workflow Document State section below

#### transitions (Workflow Transition)
- **Description**: Defines allowed transitions between states
- **Fields**: See Workflow Transition section below

### Hidden Fields

#### workflow_data
- **Type**: JSON
- **Description**: Stores visual workflow builder data (node positions, etc.)
- **Usage**: Internal use by Workflow Builder UI

## Workflow Document State

Child table that defines each state in the workflow.

### Fields

#### state
- **Type**: Link (Workflow State)
- **Required**: Yes
- **Description**: Reference to Workflow State master
- **Example**: "Pending", "Approved", "Rejected"

#### doc_status
- **Type**: Select
- **Options**: 0, 1, 2
- **Default**: 0
- **Required**: Yes
- **Description**: Document status for this state
  - **0**: Draft
  - **1**: Submitted
  - **2**: Cancelled
- **Note**: Determines if document is editable, submitted, or cancelled

#### allow_edit
- **Type**: Link (Role)
- **Required**: Yes
- **Description**: Role allowed to edit document in this state
- **Special Value**: "All" allows any role with permissions
- **Example**: "HR Manager", "Purchase Manager"

#### update_field
- **Type**: Select
- **Description**: Field to update when entering this state
- **Behavior**: Dynamically populated with fields from the document type
- **Use Case**: Automatically set status or other fields

#### update_value
- **Type**: Data
- **Description**: Value to set for update_field
- **Example**: If update_field="status", value could be "Closed"

#### is_optional_state
- **Type**: Check
- **Default**: 0
- **Description**: If checked, workflow actions are NOT created for this state
- **Use Case**: For intermediate or automated states

#### avoid_status_override
- **Type**: Check
- **Default**: 0
- **Description**: If checked, this state won't override document status in list view
- **Per-State Control**: More granular than workflow-level override_status

#### send_email
- **Type**: Check
- **Default**: 1
- **Description**: Whether to send email when document transitions TO this state
- **Use Case**: Disable for automated or intermediate states

#### next_action_email_template
- **Type**: Link (Email Template)
- **Description**: Custom email template for workflow action notifications
- **Fallback**: Uses default template if not specified

#### message
- **Type**: Text
- **Description**: Message to display to users when document is in this state
- **Display**: Shows as alert/message in document form

#### workflow_builder_id
- **Type**: Data
- **Hidden**: Yes
- **Description**: Internal ID used by visual workflow builder

## Workflow Transition

Child table that defines allowed transitions between states.

### Fields

#### state
- **Type**: Link (Workflow State)
- **Required**: Yes
- **Description**: Starting state (current state)
- **Example**: "Pending"

#### action
- **Type**: Link (Workflow Action Master)
- **Required**: Yes
- **Description**: Action name displayed to user
- **Example**: "Approve", "Reject", "Review"

#### next_state
- **Type**: Link (Workflow State)
- **Required**: Yes
- **Description**: Destination state after transition
- **Example**: "Approved"

#### allowed
- **Type**: Link (Role)
- **Required**: Yes
- **Description**: Role allowed to perform this transition
- **Special Value**: "All" allows any role with document access
- **Example**: "HR Manager"

#### allow_self_approval
- **Type**: Check
- **Default**: 1
- **Description**: Whether document owner can approve their own document
- **Security**: Set to 0 to prevent self-approval

#### send_email_to_creator
- **Type**: Check
- **Default**: 0
- **Depends On**: allow_self_approval == 1
- **Description**: Whether to send workflow action email to document creator
- **Use Case**: When self-approval is allowed but creator should still get notified

#### condition
- **Type**: Code (Python)
- **Description**: Python expression that must evaluate to True for transition to be available
- **Context**: Has access to `doc` variable and safe functions
- **Example**: `doc.grand_total > 10000`

#### workflow_builder_id
- **Type**: Data
- **Hidden**: Yes
- **Description**: Internal ID used by visual workflow builder

## Transition Condition Safe Functions

When writing transition conditions, you have access to:

### Available Objects

```python
# Document being transitioned
doc  # Dict representation of the document

# Frappe utilities
frappe.db.get_value()
frappe.db.get_list()
frappe.session  # Current session info
frappe.utils.now_datetime()
frappe.utils.get_datetime()
frappe.utils.add_to_date()
frappe.utils.now()
```

### Condition Examples

```python
# Amount-based condition
doc.grand_total > 100000

# Date-based condition
doc.creation > frappe.utils.add_to_date(frappe.utils.now_datetime(), days=-7, as_datetime=True)

# Status-based condition
doc.status == "Verified"

# User-based condition
frappe.session.user in ["user1@example.com", "user2@example.com"]

# Lookup-based condition
frappe.db.get_value("Customer", doc.customer, "customer_group") == "VIP"

# Complex condition
doc.grand_total > 50000 and doc.docstatus == 0 and frappe.session.user != doc.owner
```

## Workflow State Master

Separate DocType that stores state definitions.

### Fields

#### workflow_state_name
- **Type**: Data
- **Required**: Yes
- **Unique**: Yes
- **Description**: Name of the state
- **Example**: "Pending Approval", "Approved", "Rejected"

#### icon
- **Type**: Select
- **Hidden**: Yes (deprecated)
- **Description**: Icon for the state button

#### style
- **Type**: Select
- **Options**: Primary, Info, Success, Warning, Danger, Inverse
- **Description**: Button color style for the state
- **Examples**:
  - Success (Green): For approved/completed states
  - Danger (Red): For rejected/cancelled states
  - Warning (Orange): For pending/review states
  - Primary (Dark Blue): For initial states
  - Info (Light Blue): For information states

## Workflow Action Master

Separate DocType that stores action definitions.

### Fields

#### workflow_action_name
- **Type**: Data
- **Required**: Yes
- **Unique**: Yes
- **Description**: Name of the action
- **Example**: "Approve", "Reject", "Review", "Send Back"

**Note**: Actions are reusable across multiple workflows.

## Database Schema Considerations

### Indexes

The Workflow Action table has a composite index:
```sql
INDEX idx_workflow_action (reference_name, reference_doctype, status)
```

This optimizes queries for finding open workflow actions for specific documents.

### Custom Field Creation

When a workflow is saved, if `workflow_state_field` doesn't exist:

```python
Custom Field created with:
- fieldname: workflow_state_field value (e.g., "workflow_state")
- fieldtype: Link
- options: Workflow State
- hidden: 1
- allow_on_submit: 1
- no_copy: 1
```

## Workflow State Field Behavior

The workflow state field is special:

1. **Auto-created**: Created automatically as Custom Field if missing
2. **Hidden**: Not shown in form by default (can be made visible)
3. **Allow on Submit**: Can be changed even after submission
4. **No Copy**: Not copied when duplicating documents
5. **Link Field**: Links to Workflow State for validation

## Validation Rules

The Workflow DocType enforces these validation rules on save:

1. **Cannot transition from Cancelled**: No transitions can start from a state with docstatus=2
2. **Cannot un-submit**: Cannot go from docstatus=1 to docstatus=0
3. **Cannot cancel draft**: Cannot go from docstatus=0 to docstatus=2
4. **State must exist**: All states referenced in transitions must be defined in states table
5. **Condition syntax**: Transition conditions must be valid Python expressions

## DocStatus Flow

Understanding how docstatus changes:

```
Draft (0) → Submitted (1) → Draft (0)   ❌ Not allowed
Draft (0) → Cancelled (2)                ❌ Not allowed
Draft (0) → Submitted (1) → Cancelled (2) ✅ Allowed
Draft (0) → Draft (0)                    ✅ Allowed
Submitted (1) → Submitted (1)            ✅ Allowed
Submitted (1) → Cancelled (2)            ✅ Allowed
Cancelled (2) → Any                      ❌ Not allowed
```

## Example: Complete Workflow Structure

```python
{
    "doctype": "Workflow",
    "workflow_name": "Purchase Order Approval",
    "document_type": "Purchase Order",
    "is_active": 1,
    "workflow_state_field": "workflow_state",
    "send_email_alert": 1,
    "states": [
        {
            "state": "Draft",
            "doc_status": "0",
            "allow_edit": "Purchase User"
        },
        {
            "state": "Pending Approval",
            "doc_status": "0",
            "allow_edit": "Purchase Manager",
            "send_email": 1
        },
        {
            "state": "Approved",
            "doc_status": "1",
            "allow_edit": "Purchase Manager",
            "update_field": "status",
            "update_value": "Approved"
        },
        {
            "state": "Rejected",
            "doc_status": "0",
            "allow_edit": "Purchase Manager"
        }
    ],
    "transitions": [
        {
            "state": "Draft",
            "action": "Submit for Approval",
            "next_state": "Pending Approval",
            "allowed": "Purchase User",
            "allow_self_approval": 1
        },
        {
            "state": "Pending Approval",
            "action": "Approve",
            "next_state": "Approved",
            "allowed": "Purchase Manager",
            "allow_self_approval": 0,
            "condition": "doc.grand_total < 100000"
        },
        {
            "state": "Pending Approval",
            "action": "Reject",
            "next_state": "Rejected",
            "allowed": "Purchase Manager",
            "allow_self_approval": 0
        },
        {
            "state": "Rejected",
            "action": "Revise",
            "next_state": "Draft",
            "allowed": "Purchase User",
            "allow_self_approval": 1
        }
    ]
}
```

This structure creates a simple approval workflow with:
- 4 states: Draft, Pending Approval, Approved, Rejected
- 4 transitions: Submit, Approve, Reject, Revise
- Conditional approval (only for amounts < 100000)
- No self-approval for manager actions
- Email notifications enabled
