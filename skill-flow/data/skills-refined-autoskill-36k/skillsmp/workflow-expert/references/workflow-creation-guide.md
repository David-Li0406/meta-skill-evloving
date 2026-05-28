# Workflow Creation Guide

This document provides a step-by-step guide to creating workflows in Frappe.

## Prerequisites

Before creating a workflow, ensure you have:

1. **System Manager Role**: Required to create workflows
2. **DocType Ready**: The DocType you want to add workflow to must exist
3. **Business Process Mapped**: Clear understanding of states and transitions needed

## Step-by-Step Guide

### Step 1: Create Workflow States

Workflow States are reusable across multiple workflows.

1. Navigate to **Workflow State** list (`/app/workflow-state`)
2. Click **New**
3. Fill in details:
   - **State**: Name of the state (e.g., "Pending Approval")
   - **Style**: Choose color (Success/Danger/Warning/Info/Primary)
4. Save

**Example States to Create:**
```
- Draft (Primary - Blue)
- Pending Approval (Warning - Orange)
- Approved (Success - Green)
- Rejected (Danger - Red)
- Cancelled (Inverse - Black)
```

**Tip**: Create generic states that can be reused across multiple workflows.

### Step 2: Create Workflow Action Masters

Workflow Action Masters define the actions users can take.

1. Navigate to **Workflow Action Master** list (`/app/workflow-action-master`)
2. Click **New**
3. Fill in:
   - **Workflow Action Name**: Action name (e.g., "Approve")
4. Save

**Common Actions to Create:**
```
- Submit for Approval
- Approve
- Reject
- Send Back
- Review
- Cancel
- Revise
```

**Tip**: Use clear, action-oriented names that users will understand.

### Step 3: Create the Workflow

Now create the actual workflow configuration.

1. Navigate to **Workflow** list (`/app/workflow`)
2. Click **New**
3. Fill in basic details:
   - **Workflow Name**: Descriptive name (e.g., "Leave Application Approval")
   - **Document Type**: Select the DocType
   - **Workflow State Field**: Leave as "workflow_state" or customize
   - **Is Active**: Check to activate
   - **Don't Override Status**: Check if you don't want workflow state to override document status
   - **Send Email Alert**: Check to enable email notifications

### Step 4: Add Document States

Define all possible states the document can be in.

1. In the **States** table, add rows for each state:
   - **State**: Select from Workflow State master
   - **Doc Status**: Choose 0 (Draft), 1 (Submitted), or 2 (Cancelled)
   - **Only Allow Edit For**: Select role that can edit in this state
   - **Update Field** (Optional): Field to update when entering this state
   - **Update Value** (Optional): Value to set for the update field
   - **Is Optional State**: Check if workflow actions should not be created
   - **Don't Override Status**: Per-state status override control
   - **Send Email On State**: Whether to send email when entering this state
   - **Next Action Email Template**: Custom email template (optional)
   - **Message**: Message to show users in this state

**Example State Configuration:**

| State | Doc Status | Allow Edit | Update Field | Update Value |
|-------|-----------|------------|--------------|--------------|
| Draft | 0 | Employee | - | - |
| Pending Approval | 0 | HR Manager | status | Pending |
| Approved | 1 | HR Manager | status | Approved |
| Rejected | 0 | HR Manager | status | Rejected |

### Step 5: Add Transitions

Define allowed transitions between states.

1. In the **Transitions** table, add rows for each possible transition:
   - **State**: Starting state
   - **Action**: Select from Workflow Action Master
   - **Next State**: Destination state
   - **Allowed**: Role allowed to perform this action
   - **Allow Self Approval**: Check if document owner can approve
   - **Send Email To Creator**: Send email to document creator
   - **Condition**: Python expression for conditional transitions (optional)

**Example Transition Configuration:**

| State | Action | Next State | Allowed | Self Approval | Condition |
|-------|--------|-----------|---------|---------------|-----------|
| Draft | Submit for Approval | Pending Approval | Employee | Yes | - |
| Pending Approval | Approve | Approved | HR Manager | No | - |
| Pending Approval | Reject | Rejected | HR Manager | No | - |
| Rejected | Revise | Draft | Employee | Yes | - |

### Step 6: Save and Activate

1. Click **Save**
2. Ensure **Is Active** is checked
3. Click **Save** again

**What happens on save:**
- If workflow_state_field doesn't exist, a Custom Field is created
- All other workflows for this DocType are deactivated
- Existing documents get default workflow state

### Step 7: Test the Workflow

1. Create or open a document of the workflow's DocType
2. Verify the workflow state field appears (check in Customize Form if hidden)
3. Check that workflow buttons appear in the form
4. Test each transition:
   - Log in as user with appropriate role
   - Click workflow action button
   - Verify state changes correctly
   - Check email notifications (if enabled)
   - Verify document status changes as configured

## Using the Visual Workflow Builder

Frappe provides a visual workflow builder for easier workflow creation.

### Access Workflow Builder

1. Navigate to **Workflow Builder** page (`/app/workflow-builder`)
2. Choose "Create New" or "Edit Existing"
3. Select DocType
4. Click Create/Edit

### Using the Builder

1. **Add States**: Click "Add State" button to add state nodes
2. **Connect States**: Drag from one state to another to create transitions
3. **Configure State**: Click on state node to edit:
   - State name
   - Doc status
   - Allow edit role
   - Field updates
   - Email settings

4. **Configure Transition**: Click on transition arrow to edit:
   - Action name
   - Allowed role
   - Self approval
   - Condition

5. **Save**: Click Save button to create/update workflow

**Benefits of Visual Builder:**
- Visual representation of workflow
- Easier to understand state transitions
- Drag-and-drop interface
- Validates workflow configuration

## Advanced Configuration

### Conditional Transitions

Add Python conditions to show transitions only when certain criteria are met.

**Example Conditions:**

```python
# Amount-based condition
doc.grand_total > 50000

# Date-based condition
doc.posting_date >= frappe.utils.today()

# Status-based condition
doc.status == "Verified"

# Lookup-based condition
frappe.db.get_value("Customer", doc.customer, "customer_type") == "Corporate"

# Complex condition
doc.grand_total > 10000 and frappe.session.user != doc.owner
```

**Available in Conditions:**
- `doc`: Document dict
- `frappe.db.get_value()`
- `frappe.db.get_list()`
- `frappe.session`
- `frappe.utils.now_datetime()`
- `frappe.utils.get_datetime()`
- `frappe.utils.add_to_date()`
- `frappe.utils.now()`

### Custom Email Templates

Create custom email templates for workflow notifications.

1. Navigate to **Email Template** (`/app/email-template`)
2. Create new template
3. Use Jinja templating:
   ```html
   <p>Hello,</p>
   <p>A new {{ doc.doctype }} requires your attention:</p>
   <p><strong>{{ doc.name }}</strong></p>
   <p>Amount: {{ doc.grand_total }}</p>
   ```
4. Select template in Workflow Document State

### Field Updates

Automatically update fields when entering a state.

**Common Use Cases:**
- Update status field: `status` → `"Approved"`
- Set approval date: `approval_date` → Current date
- Update stage: `stage` → `"Processing"`

**Note**: The update happens before document save during transition.

### Optional States

Mark states as optional to skip workflow action creation.

**Use Cases:**
- Automated states that don't require user action
- Intermediate processing states
- Terminal states (no further actions needed)

## Common Workflow Patterns

### Pattern 1: Simple Two-Level Approval

```
States:
1. Draft (docstatus=0, allow_edit=Submitter)
2. Pending Approval (docstatus=0, allow_edit=Approver)
3. Approved (docstatus=1, allow_edit=Approver)
4. Rejected (docstatus=0, allow_edit=Submitter)

Transitions:
1. Draft → Pending Approval (Submit, Submitter, self_approval=yes)
2. Pending Approval → Approved (Approve, Approver, self_approval=no)
3. Pending Approval → Rejected (Reject, Approver, self_approval=no)
4. Rejected → Draft (Revise, Submitter, self_approval=yes)
```

### Pattern 2: Multi-Level Approval

```
States:
1. Draft (docstatus=0, allow_edit=Employee)
2. Manager Review (docstatus=0, allow_edit=Manager)
3. Director Approval (docstatus=0, allow_edit=Director)
4. Approved (docstatus=1, allow_edit=Director)
5. Rejected (docstatus=0, allow_edit=Employee)

Transitions:
1. Draft → Manager Review (Submit, Employee)
2. Manager Review → Director Approval (Approve L1, Manager)
3. Director Approval → Approved (Approve L2, Director)
4. Any → Rejected (Reject, Manager/Director)
5. Rejected → Draft (Resubmit, Employee)
```

### Pattern 3: Parallel Approval

```
States:
1. Draft (docstatus=0)
2. Finance Review (docstatus=0, allow_edit=Finance)
3. Legal Review (docstatus=0, allow_edit=Legal)
4. Both Approved (docstatus=1)

Note: Requires custom logic in hooks to track both approvals
```

### Pattern 4: Conditional Routing

```
Transitions with conditions:
1. Draft → Manager Approval (if amount < 100000)
2. Draft → Director Approval (if amount >= 100000)
3. Use condition: doc.grand_total >= 100000
```

## Testing Checklist

After creating a workflow, verify:

- [ ] Workflow is active
- [ ] Workflow state field exists on form
- [ ] Default state is set on new documents
- [ ] Workflow buttons appear for users with roles
- [ ] Transitions work correctly for each state
- [ ] Email notifications are sent (if enabled)
- [ ] Document status changes correctly
- [ ] Self-approval rules are enforced
- [ ] Conditional transitions work as expected
- [ ] Field updates happen correctly
- [ ] Workflow actions are created and completed
- [ ] Comments are added to document timeline
- [ ] Permissions work correctly in each state

## Troubleshooting During Creation

### Workflow Not Showing

**Check:**
- Is workflow active?
- Does user have read permission for DocType?
- Is workflow_state_field created?

**Solution:**
- Ensure "Is Active" is checked
- Grant user appropriate role
- Check Custom Field list

### Transitions Not Appearing

**Check:**
- Does user have required role?
- Is condition satisfied?
- Is current state correct?

**Solution:**
- Verify role assignment
- Test condition in console
- Check document's workflow_state value

### Email Not Sending

**Check:**
- Is "Send Email Alert" enabled?
- Is SMTP configured?
- Are users assigned to roles?

**Solution:**
- Check workflow settings
- Configure email account
- Verify user-role mapping

### State Not Changing

**Check:**
- Is transition valid?
- Are there validation errors?
- Check before_transition hook

**Solution:**
- Verify transition configuration
- Check error logs
- Review custom code in hooks

## Best Practices for Workflow Creation

1. **Start Simple**: Begin with minimal states and transitions
2. **Use Clear Names**: State and action names should be self-explanatory
3. **Test Incrementally**: Test after adding each state/transition
4. **Document the Process**: Add comments explaining business logic
5. **Plan Docstatus**: Think through when submission should happen
6. **Consider Self-Approval**: Decide if owners should approve their own documents
7. **Use Optional States**: For automated or terminal states
8. **Test with Multiple Users**: Verify different roles work correctly
9. **Monitor Email Delivery**: Check if emails are being sent
10. **Version Control**: Export workflow JSON and commit to git

## Example: Complete Workflow Setup

Let's create a complete Purchase Order Approval workflow.

### 1. Create States

```
- Draft (Primary)
- Pending Approval (Warning)
- Manager Approved (Info)
- Director Approved (Success)
- Rejected (Danger)
```

### 2. Create Actions

```
- Submit for Approval
- Approve Level 1
- Approve Level 2
- Reject
- Revise
```

### 3. Create Workflow

**Basic Details:**
- Name: "Purchase Order Approval"
- DocType: "Purchase Order"
- Active: Yes
- Send Email: Yes

**States:**
| State | Status | Role | Update Field | Update Value |
|-------|--------|------|--------------|--------------|
| Draft | 0 | Purchase User | status | Draft |
| Pending Approval | 0 | Purchase Manager | status | Pending |
| Manager Approved | 0 | Purchase Director | status | Manager Approved |
| Director Approved | 1 | Purchase Director | status | Approved |
| Rejected | 0 | Purchase User | status | Rejected |

**Transitions:**
| From | Action | To | Role | Self Approve | Condition |
|------|--------|---|------|--------------|-----------|
| Draft | Submit | Pending | Purchase User | Yes | |
| Pending | Approve L1 | Manager Approved | Purchase Manager | No | grand_total < 1000000 |
| Pending | Approve L1 | Director Approved | Purchase Manager | No | grand_total >= 1000000 |
| Manager Approved | Approve L2 | Director Approved | Purchase Director | No | |
| Pending | Reject | Rejected | Purchase Manager | No | |
| Manager Approved | Reject | Rejected | Purchase Director | No | |
| Rejected | Revise | Draft | Purchase User | Yes | |

### 4. Save and Test

1. Save workflow
2. Create test Purchase Order
3. Submit for approval as Purchase User
4. Login as Purchase Manager, approve
5. Login as Purchase Director, approve
6. Verify state changes and emails

## Next Steps

After creating your workflow:

1. **Add Custom Hooks**: Implement before_transition/after_transition if needed
2. **Customize Emails**: Create custom email templates
3. **Monitor Usage**: Check Workflow Action list for pending actions
4. **Gather Feedback**: Get user feedback and refine
5. **Document Process**: Create user guide for the workflow
6. **Export Configuration**: Export and version control workflow JSON

## Resources

- Frappe Documentation: https://frappeframework.com/docs/user/en/desk/workflows
- Workflow Builder Guide: See visual builder documentation
- Example Workflows: Check ERPNext for real-world examples
