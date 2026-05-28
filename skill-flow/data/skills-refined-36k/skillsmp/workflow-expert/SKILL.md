---
name: workflow-expert
description: Expert guidance on Frappe Workflow system including workflow structure, states and transitions, workflow actions, email notifications, permission hooks (before_transition, after_transition, filter_workflow_transitions, has_workflow_action_permission), and best practices. Use when creating workflows, implementing workflow logic, understanding state transitions, working with workflow actions, configuring email notifications, or troubleshooting workflow-related issues.
---

# Frappe Workflow Expert

This skill provides comprehensive guidance for understanding and working with Frappe's Workflow system.

## Overview

Frappe's Workflow system enables document state management with configurable states, transitions, and approval processes. Workflows automate business processes by:

- Defining multiple states a document can be in (e.g., "Draft", "Pending Approval", "Approved", "Rejected")
- Specifying transitions between states with role-based permissions
- Automating actions when documents change state (e.g., updating fields, changing docstatus)
- Sending email notifications to users for pending actions
- Creating workflow action records for approval tracking

## Key Concepts

### Core Components

1. **Workflow**: Master configuration that applies to a specific DocType
2. **Workflow State**: Represents states a document can be in (e.g., "Pending", "Approved")
3. **Workflow Document State**: Links states to the document's docstatus (0=Draft, 1=Submitted, 2=Cancelled)
4. **Workflow Transition**: Defines allowed transitions from one state to another with roles and actions
5. **Workflow Action Master**: Pre-defined action names (e.g., "Approve", "Reject")
6. **Workflow Action**: Records created for users who can approve/take action on documents

### Workflow Structure

```
Workflow (e.g., "Leave Approval")
├── document_type: "Leave Application"
├── workflow_state_field: "workflow_state"
├── is_active: 1
├── send_email_alert: 1
├── States (Workflow Document State)
│   ├── State: "Applied" (docstatus=0, allow_edit="Employee")
│   ├── State: "Approved" (docstatus=1, allow_edit="HR Manager")
│   └── State: "Rejected" (docstatus=0, allow_edit="HR Manager")
└── Transitions (Workflow Transition)
    ├── Applied → Approved (action="Approve", allowed="HR Manager")
    ├── Applied → Rejected (action="Reject", allowed="HR Manager")
    └── Rejected → Applied (action="Review", allowed="Employee")
```

## Quick Reference

### Main Workflow Functions

```python
# Get workflow for a doctype
from frappe.model.workflow import get_workflow
workflow = get_workflow("Leave Application")

# Get available transitions for a document
from frappe.model.workflow import get_transitions
transitions = get_transitions(doc)

# Apply workflow action
from frappe.model.workflow import apply_workflow
updated_doc = apply_workflow(doc, action="Approve")

# Get workflow name for doctype
from frappe.model.workflow import get_workflow_name
workflow_name = get_workflow_name("Leave Application")
```

### Workflow DocType Fields

- **workflow_name**: Unique name for the workflow
- **document_type**: DocType this workflow applies to
- **is_active**: Only one active workflow per DocType
- **workflow_state_field**: Field storing current state (default: "workflow_state")
- **override_status**: Don't override document status with workflow state
- **send_email_alert**: Send email notifications for workflow actions
- **states**: Table of Workflow Document States
- **transitions**: Table of Workflow Transitions

### Workflow Document State Fields

- **state**: Link to Workflow State
- **doc_status**: Document status (0=Draft, 1=Submitted, 2=Cancelled)
- **allow_edit**: Role that can edit document in this state
- **update_field**: Optional field to update on entering this state
- **update_value**: Value to set for update_field
- **is_optional_state**: Skip creating workflow actions for optional states
- **send_email**: Send email when transitioning to this state
- **next_action_email_template**: Custom email template for notifications

### Workflow Transition Fields

- **state**: Current state (starting point)
- **action**: Workflow Action Master (e.g., "Approve")
- **next_state**: State to transition to
- **allowed**: Role allowed to perform this transition
- **allow_self_approval**: Whether document owner can approve
- **condition**: Python expression to conditionally show transition

## Workflow Lifecycle

### 1. Document Creation
- Document gets default workflow state (first state in workflow)
- Custom field for workflow_state_field is auto-created if needed

### 2. Workflow Actions
When a document enters a state:
1. Previous workflow actions are marked as "Completed"
2. New Workflow Action records are created for next possible transitions
3. Email notifications sent to users with required roles (if enabled)

### 3. Transition Execution
When a user applies a workflow action:
1. Permission checks (role, self-approval)
2. Condition evaluation (if specified)
3. `before_transition` hook called (if exists)
4. Workflow state field updated
5. Additional fields updated (if configured)
6. Document saved/submitted/cancelled based on new state's docstatus
7. Comment added to document timeline
8. `after_transition` hook called (if exists)

### 4. Transition Filtering
Before showing available transitions:
1. Check user has required role
2. Evaluate transition conditions
3. Call `filter_workflow_transitions` hook (if registered)

## Extension Hooks

Frappe provides five main hooks for extending workflow behavior:

### 1. `before_transition` - Controller Method

**Purpose**: Execute custom logic before state transition

**Location**: In your doctype's `.py` file

**Signature**:
```python
def before_transition(self, transition):
    """
    Called before workflow state change.
    Args:
        transition: dict with action, state, next_state, allowed, etc.
    """
```

**Use Cases**:
- Validate business rules before transition
- Update related documents
- Create notifications or logs

### 2. `after_transition` - Controller Method

**Purpose**: Execute custom logic after state transition

**Location**: In your doctype's `.py` file

**Signature**:
```python
def after_transition(self, transition):
    """
    Called after workflow state change and document save.
    Args:
        transition: dict with action, state, next_state, allowed, etc.
    """
```

**Use Cases**:
- Update related documents after approval
- Trigger external integrations
- Create follow-up tasks

### 3. `filter_workflow_transitions` - Hook

**Purpose**: Customize available transitions based on custom logic

**Location**: Registered in `hooks.py`

**Signature**:
```python
def filter_workflow_transitions(doc, transitions, workflow):
    """
    Filter or modify transitions before displaying to user.
    
    Args:
        doc: Document instance
        transitions: List of available transition dicts
        workflow: Workflow document
        
    Returns:
        List of filtered/modified transitions or None
    """
```

**Use Cases**:
- Hide transitions based on field values
- Apply time-based restrictions
- Implement dynamic approval routing

### 4. `has_workflow_action_permission` - Hook

**Purpose**: Control who receives workflow action notifications

**Location**: Registered in `hooks.py`

**Signature**:
```python
def has_workflow_action_permission(user, transition, doc):
    """
    Check if user should receive workflow action for this transition.
    
    Args:
        user: User email
        transition: Transition dict
        doc: Document instance
        
    Returns:
        bool: True if user should get action, False otherwise
    """
```

**Use Cases**:
- Hierarchical approval routing
- Amount-based approval limits
- Department/region-based routing

### 5. `workflow_safe_eval_globals` - Hook

**Purpose**: Extend available globals in workflow transition conditions

**Location**: Registered in `hooks.py`

**Signature**:
```python
def get_workflow_globals(current_globals):
    """
    Add custom functions or data for workflow conditions.
    
    Args:
        current_globals: Dict of currently available globals
        
    Returns:
        dict: Additional globals to make available
    """
```

**Use Cases**:
- Add helper functions for approval limits
- Provide business logic functions for conditions
- Expose configuration data to transition conditions

**When to read:** See [references/workflow-hooks.md](references/workflow-hooks.md) for detailed examples of all workflow hooks.

## Workflow States and Transitions

### State Configuration

Each Workflow Document State defines:
- **Document Status**: Maps to docstatus (0=Draft, 1=Submitted, 2=Cancelled)
- **Edit Permissions**: Role that can edit in this state
- **Field Updates**: Optional field to update when entering state
- **Email Settings**: Whether to send email when entering state

### Transition Rules

Transitions must follow these rules:
1. Cannot transition FROM a Cancelled state (docstatus=2)
2. Cannot go from Submitted (docstatus=1) back to Draft (docstatus=0)
3. Cannot cancel (docstatus=2) before submitting
4. Conditions are evaluated before showing transition

### Transition Conditions

Add Python expressions to conditionally show transitions:

```python
# Transition only if grand_total > 10000
doc.grand_total > 10000

# Transition only if created within last 7 days
doc.creation > frappe.utils.add_to_date(
    frappe.utils.now_datetime(), 
    days=-7, 
    as_datetime=True
)
```

**Available functions in conditions:**
- `frappe.db.get_value`
- `frappe.db.get_list`
- `frappe.session`
- `frappe.utils.now_datetime`
- `frappe.utils.get_datetime`
- `frappe.utils.add_to_date`
- `frappe.utils.now`

**Extending available globals:** Apps can use the `workflow_safe_eval_globals` hook to add custom functions or data to workflow transition conditions. See [Frappe Hooks documentation](https://frappeframework.com/docs/user/en/basics/hooks) for details.

**When to read:** See [references/workflow-states-transitions.md](references/workflow-states-transitions.md) for detailed state and transition configuration.

## Workflow Actions

The Workflow Action system tracks pending approvals:

### Workflow Action Records

Created automatically when document enters a state with outgoing transitions:
- **reference_doctype**: Document type
- **reference_name**: Document name
- **workflow_state**: Current workflow state
- **status**: "Open" or "Completed"
- **permitted_roles**: Roles that can take action
- **user**: Specific user (backwards compatibility)

### Email Notifications

When `send_email_alert` is enabled:
1. Users with required roles receive email with action links
2. Email includes document details and possible actions
3. Custom email templates can be configured per state
4. Users can approve via email link without logging in

**Note**: Workflow action creation and email notification details are covered in [references/workflow-hooks.md](references/workflow-hooks.md) and [references/workflow-structure.md](references/workflow-structure.md).

## Workflow Permissions

Workflows interact with Frappe's permission system:

### Permission Evaluation

1. User must have base read permission for the doctype
2. User must have role specified in transition's "allowed" field
3. Self-approval check (if `allow_self_approval=0`, owner cannot approve)
4. Custom `has_workflow_action_permission` hook (if registered)

### Edit Permissions in States

The `allow_edit` field in each state controls:
- Which role can edit document in that state
- Used by permission system to grant write access

**Note**: Workflow permission hooks (`has_workflow_action_permission`) are detailed in [references/workflow-hooks.md](references/workflow-hooks.md).

## Creating a Workflow

### Quick Start

1. **Create Workflow States**:
   - Navigate to Workflow State list
   - Create states like "Pending", "Approved", "Rejected"

2. **Create Workflow Action Masters**:
   - Navigate to Workflow Action Master
   - Create actions like "Approve", "Reject"

3. **Create Workflow**:
   - Navigate to Workflow list
   - Set document type and workflow name
   - Add states with docstatus and roles
   - Add transitions with actions and allowed roles
   - Enable and save

4. **Test**:
   - Create/open a document of the workflow's DocType
   - Verify workflow state field appears
   - Test transitions with different users

**When to read:** See [references/workflow-creation-guide.md](references/workflow-creation-guide.md) for detailed step-by-step instructions.

## Common Patterns

### Simple Approval Workflow
- Draft → Pending Approval → Approved/Rejected
- Two roles: Submitter, Approver

### Multi-Level Approval
- Draft → L1 Approval → L2 Approval → Approved
- Multiple approver roles with escalation

### Review and Rework
- Draft → Review → Approved/Needs Rework → Draft
- Allows sending back for corrections

### Amount-Based Routing
- Use conditions to route based on amount thresholds
- Different approval paths for different amounts

**When to read:** See [references/workflow-examples.md](references/workflow-examples.md) for complete working examples.

## Best Practices

### Design
1. **Keep It Simple**: Start with minimal states and transitions
2. **Clear State Names**: Use business-friendly names like "Pending Approval"
3. **Avoid Cycles**: Minimize circular transitions
4. **Plan Docstatus**: Think through when documents should be submitted/cancelled

### Implementation
1. **Test with Real Users**: Verify permissions work as expected
2. **Use Conditions Sparingly**: Keep transition logic simple
3. **Handle Errors**: Add validation in before_transition hooks
4. **Document Workflow**: Add comments explaining business process

### Performance
1. **Optimize Email Sending**: Use background jobs for large user lists
2. **Index Workflow Fields**: Ensure workflow_state_field is indexed
3. **Limit Workflow Actions**: Mark states as optional when appropriate

### Security
1. **Validate Self-Approval**: Set allow_self_approval appropriately
2. **Check Permissions**: Don't bypass permission system
3. **Audit Transitions**: Use comments to track who did what

**When to read:** See [references/workflow-best-practices.md](references/workflow-best-practices.md) for comprehensive guidelines.

## Debugging and Troubleshooting

### Common Issues

1. **Workflow not appearing**: Check is_active and user permissions
2. **Transitions not showing**: Verify role, conditions, and state configuration
3. **Email not sending**: Check send_email_alert and SMTP configuration
4. **Self-approval blocked**: Review allow_self_approval setting
5. **State field not created**: Check Custom Field creation in workflow

### Debugging Tools

```python
# Check workflow configuration
workflow = frappe.get_doc("Workflow", "My Workflow")
print(workflow.as_dict())

# Check available transitions
transitions = get_transitions(doc)
print(transitions)

# Check workflow actions
actions = frappe.get_all("Workflow Action", 
    filters={"reference_name": doc.name, "status": "Open"},
    fields=["*"]
)
print(actions)
```

**When to read:** See [references/workflow-troubleshooting.md](references/workflow-troubleshooting.md) for detailed debugging guide.

## Reference Files

For detailed information on specific topics:

- **[workflow-structure.md](references/workflow-structure.md)** - Workflow DocType structure, fields, and schema
- **[workflow-states-transitions.md](references/workflow-states-transitions.md)** - States and transitions configuration
- **[workflow-hooks.md](references/workflow-hooks.md)** - All workflow extension hooks with 30+ examples
- **[workflow-creation-guide.md](references/workflow-creation-guide.md)** - Step-by-step workflow creation
- **[workflow-examples.md](references/workflow-examples.md)** - 8 complete workflow patterns
- **[workflow-best-practices.md](references/workflow-best-practices.md)** - Best practices and gotchas
- **[workflow-troubleshooting.md](references/workflow-troubleshooting.md)** - Common issues and debugging

## Core Implementation Files

Key files in Frappe codebase:
- `/frappe/model/workflow.py` - Core workflow engine
- `/frappe/workflow/doctype/workflow/workflow.py` - Workflow DocType controller
- `/frappe/workflow/doctype/workflow_action/workflow_action.py` - Workflow action processing
- `/frappe/workflow/page/workflow_builder/` - Visual workflow builder

## Usage

When working with workflows:

1. **Understand the business process**: Map out states and transitions first
2. **Choose appropriate hooks**: Use before_transition for validation, after_transition for actions
3. **Configure permissions**: Set up roles and self-approval settings
4. **Test thoroughly**: Test all transitions with different users and scenarios
5. **Monitor workflow actions**: Check that emails are sent and actions are created
6. **Debug when needed**: Use debug logs and database queries

## Important Notes

- Only one active workflow per DocType at a time
- Workflow state field is automatically created as Custom Field if it doesn't exist
- Administrator can always take any workflow action
- Workflow actions are automatically cleaned up when documents are deleted
- Bulk workflow approval is supported (up to 500 documents)
- Transition conditions use safe_eval with limited function access
- Workflow state overrides document status in list view (unless override_status is checked)
