# Workflow Troubleshooting

This document provides solutions to common workflow issues and debugging techniques.

## Common Issues

### 1. Workflow Not Appearing on Form

**Symptoms:**
- No workflow buttons visible
- No workflow state field on form
- Document behaves as if no workflow exists

**Possible Causes & Solutions:**

#### Cause 1: Workflow Not Active
```python
# Check if workflow is active
workflow = frappe.get_doc("Workflow", "My Workflow")
print(f"Is Active: {workflow.is_active}")

# Solution: Activate workflow
workflow.is_active = 1
workflow.save()
```

#### Cause 2: Wrong DocType
```python
# Verify workflow's document type
workflow = frappe.get_doc("Workflow", "My Workflow")
print(f"Document Type: {workflow.document_type}")

# Check if it matches your form
print(f"Form DocType: {frappe.form_dict.doctype}")
```

#### Cause 3: User Lacks Permissions
```python
# Check if user can read the doctype
has_perm = frappe.has_permission("DocType Name", "read")
print(f"User has read permission: {has_perm}")

# Solution: Grant appropriate role
frappe.get_doc("User", user).add_roles("Required Role")
```

#### Cause 4: Workflow State Field Not Created
```python
# Check if field exists
meta = frappe.get_meta("DocType Name")
field = meta.get_field("workflow_state")
print(f"Field exists: {field is not None}")

# Solution: Resave workflow to trigger field creation
workflow = frappe.get_doc("Workflow", "My Workflow")
workflow.save()
```

#### Cause 5: Cache Issue
```python
# Clear cache
frappe.clear_cache(doctype="DocType Name")

# Or clear all cache
frappe.clear_cache()

# Reload page
```

### 2. Workflow Transitions Not Showing

**Symptoms:**
- Workflow active but no action buttons
- Expected transitions not available
- Empty workflow action dropdown

**Debugging Steps:**

#### Step 1: Check Available Transitions
```python
from frappe.model.workflow import get_transitions

doc = frappe.get_doc("DocType Name", "DOC-001")
transitions = get_transitions(doc)
print(f"Available transitions: {transitions}")
```

#### Step 2: Verify User Role
```python
# Check user's roles
user_roles = frappe.get_roles()
print(f"User roles: {user_roles}")

# Check required role for transition
workflow = frappe.get_doc("Workflow", "My Workflow")
for t in workflow.transitions:
    if t.state == doc.workflow_state:
        print(f"Transition: {t.action}, Required role: {t.allowed}")
```

#### Step 3: Check Current State
```python
# Verify document's current state
doc = frappe.get_doc("DocType Name", "DOC-001")
print(f"Current workflow state: {doc.workflow_state}")

# Check if state exists in workflow
workflow = frappe.get_doc("Workflow", "My Workflow")
states = [s.state for s in workflow.states]
print(f"Valid states: {states}")
print(f"Current state valid: {doc.workflow_state in states}")
```

#### Step 4: Test Transition Conditions
```python
# Check if condition is satisfied
transition_condition = "doc.grand_total > 10000"
doc_dict = doc.as_dict()

try:
    result = frappe.safe_eval(transition_condition, {"doc": doc_dict})
    print(f"Condition '{transition_condition}' result: {result}")
except Exception as e:
    print(f"Condition error: {str(e)}")
```

#### Step 5: Check Self-Approval
```python
# If user is document owner and allow_self_approval=0
print(f"Document owner: {doc.owner}")
print(f"Current user: {frappe.session.user}")
print(f"Is owner: {doc.owner == frappe.session.user}")

# Check transition's allow_self_approval setting
for t in workflow.transitions:
    print(f"{t.action}: allow_self_approval={t.allow_self_approval}")
```

### 3. Workflow State Not Changing

**Symptoms:**
- Click workflow action but state doesn't change
- No error message shown
- Document appears unchanged

**Debugging Steps:**

#### Step 1: Check for Validation Errors
```python
# Enable debug mode to see errors
frappe.conf.developer_mode = 1

# Check error logs
errors = frappe.get_all("Error Log",
    filters={"creation": [">", frappe.utils.add_to_date(None, hours=-1)]},
    fields=["error", "creation"],
    order_by="creation desc",
    limit=5
)
for e in errors:
    print(f"{e.creation}: {e.error}")
```

#### Step 2: Check before_transition Hook
```python
# Add debug logging in before_transition
class MyDocType(Document):
    def before_transition(self, transition):
        frappe.log_error(
            f"Before transition: {transition}",
            f"Debug - {self.name}"
        )
        # Your validation code here
```

#### Step 3: Verify DocStatus Transition
```python
# Check if docstatus transition is valid
current_docstatus = doc.docstatus
current_state = next(s for s in workflow.states if s.state == doc.workflow_state)
next_state = next(s for s in workflow.states if s.state == transition.next_state)

print(f"Current docstatus: {current_docstatus}")
print(f"Next docstatus: {next_state.doc_status}")

# Invalid transitions:
# 1 → 0 (submitted to draft) ❌
# 0 → 2 (draft to cancelled) ❌
# 2 → any (from cancelled) ❌
```

#### Step 4: Check Transaction Rollback
```python
# If error occurs after state change, transaction rolls back
def after_transition(self, transition):
    try:
        self.critical_operation()
    except Exception as e:
        # This will rollback the entire transition
        frappe.log_error(str(e))
        raise
```

### 4. Email Notifications Not Sending

**Symptoms:**
- Workflow actions created but no emails sent
- Users not receiving notifications
- Email queue empty

**Debugging Steps:**

#### Step 1: Check Workflow Settings
```python
workflow = frappe.get_doc("Workflow", "My Workflow")
print(f"Send Email Alert: {workflow.send_email_alert}")

# Check state-specific settings
for state in workflow.states:
    if state.state == doc.workflow_state:
        print(f"Send Email for state: {state.send_email}")
```

#### Step 2: Check SMTP Configuration
```python
# Verify email account exists
email_accounts = frappe.get_all("Email Account",
    filters={"enable_outgoing": 1})
print(f"Outgoing email accounts: {email_accounts}")

# Test email sending
frappe.sendmail(
    recipients=["test@example.com"],
    subject="Test Email",
    message="Testing workflow emails"
)
```

#### Step 3: Check Users with Role
```python
# Get users with required role
role = "Approver"
users = frappe.get_all("Has Role",
    filters={"role": role, "parenttype": "User"},
    fields=["parent as user"]
)
print(f"Users with {role} role: {users}")

# Check if users have email
for user in users:
    email = frappe.db.get_value("User", user.user, "email")
    print(f"{user.user}: {email}")
```

#### Step 4: Check Email Queue
```python
# Check for failed emails
failed_emails = frappe.get_all("Email Queue",
    filters={"status": "Error"},
    fields=["name", "error", "recipients"],
    order_by="creation desc",
    limit=10
)
for email in failed_emails:
    print(f"Failed: {email.recipients} - {email.error}")

# Check pending emails
pending = frappe.db.count("Email Queue", {"status": "Not Sent"})
print(f"Pending emails: {pending}")
```

#### Step 5: Check Email Queue Service
```bash
# In terminal, check if email queue is running
bench --site mysite doctor

# Manually flush email queue
bench --site mysite send-queued-emails
```

### 5. Workflow Actions Not Created

**Symptoms:**
- No Workflow Action records created
- Users don't see pending actions
- Notifications missing

**Debugging Steps:**

#### Step 1: Check if State is Optional
```python
workflow = frappe.get_doc("Workflow", "My Workflow")
current_state = doc.workflow_state

for state in workflow.states:
    if state.state == current_state:
        print(f"State: {state.state}")
        print(f"Is Optional: {state.is_optional_state}")
```

#### Step 2: Check for Outgoing Transitions
```python
# Workflow actions only created if there are next transitions
transitions = [t for t in workflow.transitions if t.state == current_state]
print(f"Outgoing transitions from {current_state}: {len(transitions)}")
```

#### Step 3: Check Workflow Action Processing
```python
# Manual check
from frappe.workflow.doctype.workflow_action.workflow_action import process_workflow_actions

process_workflow_actions(doc, state="on_update")

# Check created actions
actions = frappe.get_all("Workflow Action",
    filters={"reference_name": doc.name, "status": "Open"},
    fields=["*"]
)
print(f"Workflow actions: {actions}")
```

### 6. Permission Denied Errors

**Symptoms:**
- "Insufficient Permission" error
- User has role but can't take action
- Transition fails with permission error

**Debugging Steps:**

#### Step 1: Check Document Permissions
```python
# Check if user can read/write document
doc = frappe.get_doc("DocType Name", "DOC-001")
can_read = frappe.has_permission(doc.doctype, "read", doc)
can_write = frappe.has_permission(doc.doctype, "write", doc)

print(f"Can read: {can_read}")
print(f"Can write: {can_write}")
```

#### Step 2: Check State Edit Permissions
```python
# Check allow_edit role for current state
workflow = frappe.get_doc("Workflow", "My Workflow")
current_state_config = next(
    (s for s in workflow.states if s.state == doc.workflow_state),
    None
)
if current_state_config:
    print(f"Allow edit: {current_state_config.allow_edit}")
    print(f"User has role: {current_state_config.allow_edit in frappe.get_roles()}")
```

#### Step 3: Check Workflow Action Permission
```python
# If has_workflow_action_permission hook is registered
from frappe.model.workflow import has_approval_access

user = frappe.session.user
transition = {...}  # transition dict
has_access = has_approval_access(user, doc, transition)
print(f"Has approval access: {has_access}")
```

### 7. Bulk Approval Failures

**Symptoms:**
- Bulk approval partially fails
- Some documents approved, others not
- Inconsistent results

**Debugging Steps:**

#### Step 1: Check Error Messages
```python
# Bulk approval logs errors
# Check Error Log
errors = frappe.get_all("Error Log",
    filters={
        "error": ["like", "%Workflow%"],
        "creation": [">", frappe.utils.add_to_date(None, hours=-1)]
    },
    fields=["name", "error"],
    limit=20
)
```

#### Step 2: Process One by One
```python
# Test individual documents
from frappe.model.workflow import apply_workflow

doc_names = ["DOC-001", "DOC-002", "DOC-003"]

for name in doc_names:
    try:
        doc = frappe.get_doc("DocType Name", name)
        apply_workflow(doc, "Approve")
        print(f"✓ {name}")
    except Exception as e:
        print(f"✗ {name}: {str(e)}")
```

### 8. Condition Syntax Errors

**Symptoms:**
- Workflow save fails
- Error about invalid Python code
- Condition not evaluating

**Solutions:**

#### Fix Syntax Errors
```python
# Bad syntax
❌ "doc.amount = 1000"  # Assignment, not comparison
❌ "doc.amount > "     # Incomplete
❌ "doc.items[0]"      # Not safe

# Good syntax
✓ "doc.amount == 1000"
✓ "doc.amount > 0"
✓ "doc.get('items') and len(doc.get('items')) > 0"
```

#### Test Conditions
```python
# Test condition before saving
condition = "doc.grand_total > 10000"
doc_dict = frappe.get_doc("DocType", "DOC-001").as_dict()

try:
    result = frappe.safe_eval(condition, {"doc": doc_dict})
    print(f"Condition evaluates to: {result}")
except Exception as e:
    print(f"Condition error: {str(e)}")
```

## Debugging Tools

### 1. Enable Developer Mode

```bash
# In site_config.json
{
    "developer_mode": 1
}
```

### 2. Check Workflow Configuration
```python
def debug_workflow(workflow_name):
    """Print workflow configuration."""
    workflow = frappe.get_doc("Workflow", workflow_name)
    
    print(f"\n=== Workflow: {workflow_name} ===")
    print(f"Document Type: {workflow.document_type}")
    print(f"Active: {workflow.is_active}")
    print(f"Send Email: {workflow.send_email_alert}")
    
    print(f"\n--- States ({len(workflow.states)}) ---")
    for state in workflow.states:
        print(f"  {state.state} (docstatus={state.doc_status}, edit={state.allow_edit})")
    
    print(f"\n--- Transitions ({len(workflow.transitions)}) ---")
    for t in workflow.transitions:
        condition = f" [if {t.condition}]" if t.condition else ""
        print(f"  {t.state} --[{t.action}]--> {t.next_state} ({t.allowed}){condition}")

# Usage
debug_workflow("My Workflow")
```

### 3. Check Document Workflow State

```python
def debug_document_workflow(doctype, name):
    """Debug document's workflow state."""
    doc = frappe.get_doc(doctype, name)
    workflow = frappe.get_doc("Workflow", frappe.model.workflow.get_workflow_name(doctype))
    
    print(f"\n=== Document: {name} ===")
    print(f"Workflow State: {doc.workflow_state}")
    print(f"DocStatus: {doc.docstatus}")
    print(f"Owner: {doc.owner}")
    print(f"Modified By: {doc.modified_by}")
    
    print(f"\n--- Available Transitions ---")
    from frappe.model.workflow import get_transitions
    transitions = get_transitions(doc)
    for t in transitions:
        print(f"  [{t.action}] → {t.next_state} (role: {t.allowed})")
    
    print(f"\n--- Workflow Actions ---")
    actions = frappe.get_all("Workflow Action",
        filters={"reference_name": name, "status": "Open"},
        fields=["name", "status", "workflow_state"]
    )
    for action in actions:
        print(f"  {action.name}: {action.workflow_state} ({action.status})")

# Usage
debug_document_workflow("Purchase Order", "PO-001")
```

### 4. Test Workflow Programmatically

```python
def test_workflow_transition(doctype, name, action):
    """Test a workflow transition."""
    from frappe.model.workflow import apply_workflow
    
    doc = frappe.get_doc(doctype, name)
    
    print(f"Before: {doc.workflow_state}")
    
    try:
        apply_workflow(doc, action)
        print(f"After: {doc.workflow_state}")
        print("✓ Success")
    except Exception as e:
        print(f"✗ Failed: {str(e)}")
        import traceback
        traceback.print_exc()

# Usage
test_workflow_transition("Leave Application", "LA-001", "Approve")
```

### 5. Monitor Workflow Performance

```python
def workflow_performance_stats(doctype):
    """Get workflow performance statistics."""
    
    # Average time in each state
    stats = frappe.db.sql("""
        SELECT 
            workflow_state,
            COUNT(*) as count,
            AVG(TIMESTAMPDIFF(HOUR, creation, modified)) as avg_hours,
            MAX(TIMESTAMPDIFF(HOUR, creation, modified)) as max_hours
        FROM `tab{doctype}`
        WHERE workflow_state IS NOT NULL
        GROUP BY workflow_state
    """.format(doctype=doctype), as_dict=True)
    
    print(f"\n=== Workflow Performance: {doctype} ===")
    for stat in stats:
        print(f"{stat.workflow_state}:")
        print(f"  Count: {stat.count}")
        print(f"  Avg time: {stat.avg_hours:.2f} hours")
        print(f"  Max time: {stat.max_hours:.2f} hours")

# Usage
workflow_performance_stats("Purchase Order")
```

## Quick Fixes

### Reset Workflow State

```python
# Reset document to first state
doc = frappe.get_doc("DocType Name", "DOC-001")
workflow = frappe.get_doc("Workflow", workflow_name)
first_state = workflow.states[0].state
doc.workflow_state = first_state
doc.save()
```

### Clear Stuck Workflow Actions

```python
# Clear all open actions for a document
frappe.db.delete("Workflow Action", {
    "reference_name": "DOC-001",
    "status": "Open"
})

# Recreate them
from frappe.workflow.doctype.workflow_action.workflow_action import process_workflow_actions
doc = frappe.get_doc("DocType Name", "DOC-001")
process_workflow_actions(doc, "on_update")
```

### Force Workflow Action Creation

```python
# Manually create workflow action
from frappe.workflow.doctype.workflow_action.workflow_action import create_workflow_actions_for_roles

doc = frappe.get_doc("DocType Name", "DOC-001")
roles = ["Approver"]
create_workflow_actions_for_roles(roles, doc)
```

## Getting Help

If you're still stuck:

1. **Check Error Logs**: `/app/error-log`
2. **Review Documentation**: Frappe docs on workflows
3. **Search Forum**: discuss.frappe.io
4. **Ask Community**: Frappe Discord/Forum
5. **Check Source Code**: `frappe/model/workflow.py`

## Summary

Most workflow issues are caused by:
1. Configuration errors (inactive workflow, wrong roles)
2. Permission problems (user lacks required role/permissions)
3. State/transition misconfigurations
4. Condition evaluation errors
5. Custom hook errors

**Debugging Strategy:**
1. Check if workflow is active
2. Verify user has required role
3. Check current state is valid
4. Test transition conditions
5. Review error logs
6. Test transitions programmatically
7. Check email configuration (for notifications)

Remember: Use developer mode and error logs for detailed debugging information!
