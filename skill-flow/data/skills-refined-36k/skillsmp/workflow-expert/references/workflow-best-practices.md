# Workflow Best Practices

This document provides comprehensive best practices for designing, implementing, and maintaining workflows in Frappe.

## Design Best Practices

### 1. Start Simple

**Do:**
- Begin with minimal states (3-5)
- Add complexity only when needed
- Test simple workflow first
- Get user feedback before adding features

**Don't:**
- Create overly complex workflows initially
- Add states "just in case"
- Try to handle every edge case upfront

**Example:**
```python
# Good: Simple and clear
States: Draft → Pending → Approved/Rejected

# Too Complex Initially:
States: Draft → Initial Review → Secondary Review → Manager Review → 
        Director Review → CFO Review → Final Approval → Post-Approval → 
        Implementation → Verification → Completed
```

### 2. Use Clear, Business-Friendly Names

**State Names:**
```python
✅ Good:
- "Pending Manager Approval"
- "Awaiting Customer Response"
- "In Quality Check"
- "Approved"

❌ Bad:
- "State1", "State2"
- "PendAppr"
- "InProgress"
- "OK"
```

**Action Names:**
```python
✅ Good:
- "Submit for Approval"
- "Approve"
- "Send Back for Revision"
- "Mark as Complete"

❌ Bad:
- "Next"
- "OK"
- "Process"
- "Go"
```

### 3. Plan DocStatus Carefully

**Guidelines:**
- Use docstatus=0 for all non-final states
- Use docstatus=1 only when document is officially approved/completed
- Use docstatus=2 only for true cancellations
- Consider whether users need to edit after submission

**Example Mapping:**
```python
# Purchase Order Workflow
Draft → docstatus=0                # Still being created
Pending Approval → docstatus=0     # Not yet official
Manager Approved → docstatus=0     # Interim approval, not final
Approved → docstatus=1             # Official, locked
Rejected → docstatus=0             # Can be revised
Cancelled → docstatus=2            # Void, no longer valid
```

### 4. Handle Rejections Properly

**Always provide a path back:**
```python
# Good: Rejected documents can be revised
Draft → Pending → Approved/Rejected
         ↑________________↓
         (Revise action)

# Bad: No way to fix rejected documents
Draft → Pending → Approved/Rejected (dead end)
```

**Best Practice:**
```python
{
    "state": "Rejected",
    "action": "Revise and Resubmit",
    "next_state": "Draft",
    "allowed": "Original Submitter",
    "allow_self_approval": 1
}
```

### 5. Avoid Circular Workflows

**Problem:**
```python
# Bad: Infinite loop possible
State A → State B → State C → State A (repeat forever)
```

**Solution:**
```python
# Good: Linear or converging flow
State A → State B → State C → Final State
  ↓         ↓         ↓
Rejected ← Rejected ← Rejected → Can Revise
```

### 6. Consider User Experience

**Think about:**
- Who sees what actions?
- Are action names clear?
- Is the workflow intuitive?
- Do users understand current state?
- Are there too many steps?

**Example:**
```python
# Good: Clear progression
Employee: "Submit Leave" → "Resubmit if Rejected"
Manager: "Approve" or "Reject"

# Confusing:
Employee: "Process" → "Next Step"
Manager: "Action1" or "Action2"
```

## Implementation Best Practices

### 1. Use Conditions Wisely

**Good Condition Use:**
```python
# Clear business rule
condition = "doc.grand_total >= 100000"

# Time-based
condition = "doc.creation > frappe.utils.add_to_date(frappe.utils.now_datetime(), days=-30, as_datetime=True)"

# Status check
condition = "doc.verification_status == 'Complete'"
```

**Bad Condition Use:**
```python
# Too complex (use hooks instead)
condition = "doc.grand_total > 50000 and frappe.db.get_value('Customer', doc.customer, 'credit_limit') > doc.grand_total and doc.payment_terms in ['Net 30', 'Net 60'] and frappe.session.user != doc.owner"

# Database-heavy (performance issue)
condition = "len(frappe.get_all('Sales Order', filters={'customer': doc.customer, 'docstatus': 0})) < 5"
```

**Rule of Thumb:**
- Conditions should be simple and fast
- Complex logic belongs in hooks
- Avoid multiple database queries in conditions

### 2. Implement Validation in Hooks

**Use before_transition for validation:**
```python
def before_transition(self, transition):
    """Validate before state change."""
    if transition.action == "Approve":
        # Clear validation
        if not self.all_items_verified():
            frappe.throw("All items must be verified before approval")
        
        # Business rule
        if not self.within_budget():
            frappe.throw("Amount exceeds available budget")
        
        # Permission check
        if not self.user_can_approve_amount(frappe.session.user, self.grand_total):
            frappe.throw("You don't have authority to approve this amount")
```

### 3. Use after_transition for Actions

**Use after_transition for follow-up actions:**
```python
def after_transition(self, transition):
    """Execute actions after state change."""
    if transition.action == "Approve":
        # Update related documents
        self.update_inventory_reservation()
        
        # Create follow-up tasks
        self.create_delivery_task()
        
        # Send notifications
        self.notify_warehouse()
        
        # Update external systems
        self.sync_to_erp()
```

### 4. Handle Errors Gracefully

**In before_transition:**
```python
def before_transition(self, transition):
    """Validate with clear error messages."""
    try:
        if transition.action == "Approve":
            self.validate_approval_requirements()
    except Exception as e:
        # Provide helpful error message
        frappe.throw(
            f"Cannot approve: {str(e)}<br><br>"
            "Please ensure all requirements are met.",
            title="Approval Failed"
        )
```

**In after_transition:**
```python
def after_transition(self, transition):
    """Handle non-critical failures."""
    if transition.action == "Approve":
        # Critical: Must succeed
        self.update_inventory()
        
        # Non-critical: Can fail
        try:
            self.send_email_notification()
        except Exception as e:
            # Log but don't fail the transition
            frappe.log_error(f"Failed to send email: {str(e)}")
```

### 5. Test Thoroughly

**Test Matrix:**
```
For each transition:
├── Test with correct role ✓
├── Test with wrong role ✓
├── Test with document owner ✓
├── Test with different user ✓
├── Test condition evaluation ✓
├── Test validation in before_transition ✓
├── Test actions in after_transition ✓
├── Test email notifications ✓
└── Test edge cases ✓
```

**Example Test:**
```python
def test_workflow_complete_cycle(self):
    """Test complete workflow cycle."""
    # Create document
    doc = self.create_test_document()
    self.assertEqual(doc.workflow_state, "Draft")
    
    # Submit
    apply_workflow(doc, "Submit")
    self.assertEqual(doc.workflow_state, "Pending")
    
    # Verify workflow action created
    actions = frappe.get_all("Workflow Action", 
        filters={"reference_name": doc.name})
    self.assertGreater(len(actions), 0)
    
    # Approve
    frappe.set_user("approver@example.com")
    apply_workflow(doc, "Approve")
    
    # Verify final state
    doc.reload()
    self.assertEqual(doc.workflow_state, "Approved")
    self.assertEqual(doc.docstatus, 1)
    
    # Verify workflow action completed
    actions = frappe.get_all("Workflow Action",
        filters={"reference_name": doc.name, "status": "Completed"})
    self.assertGreater(len(actions), 0)
```

### 6. Document Your Workflow

**Add Documentation:**
```python
# In DocType controller
class PurchaseOrder(Document):
    """
    Workflow States:
    - Draft: Initial creation by Purchase User
    - Pending Manager: Awaiting manager approval (amounts < 100k)
    - Pending Director: Awaiting director approval (amounts >= 100k)
    - Approved: Approved and submitted
    - Rejected: Rejected, can be revised
    
    Business Rules:
    - Orders under $100k: Manager can approve
    - Orders $100k+: Requires Director approval
    - Self-approval not allowed for approvers
    - Budget availability checked before approval
    """
```

## Performance Best Practices

### 1. Optimize Email Sending

**Use Background Jobs:**
```python
# In workflow configuration or custom code
def after_transition(self, transition):
    if transition.action == "Approve":
        # Don't send emails synchronously
        frappe.enqueue(
            send_approval_notifications,
            queue="short",
            doc=self,
            enqueue_after_commit=True
        )
```

### 2. Index Workflow Fields

**Ensure workflow_state_field is indexed:**
```python
# In doctype_name.py
def on_doctype_update():
    frappe.db.add_index("DocType Name", ["workflow_state"])
```

### 3. Cache Expensive Lookups

**Cache user data:**
```python
@frappe.cache
def get_user_approval_limit(user):
    """Cache approval limits."""
    return frappe.db.get_value(
        "Approval Settings",
        {"user": user},
        "approval_limit"
    ) or 0
```

### 4. Use Optional States

**Mark automated/terminal states as optional:**
```python
{
    "state": "Auto Processed",
    "is_optional_state": 1,  # Don't create workflow actions
    "send_email": 0          # Don't send emails
}
```

### 5. Limit Workflow Actions

**Clean up completed actions periodically:**
```python
# Scheduled task
def cleanup_old_workflow_actions():
    """Remove completed actions older than 90 days."""
    from datetime import timedelta
    cutoff = frappe.utils.add_to_date(None, days=-90)
    
    frappe.db.delete("Workflow Action", {
        "status": "Completed",
        "modified": ["<", cutoff]
    })
```

## Security Best Practices

### 1. Validate Self-Approval Settings

**Guidelines:**
```python
# Allow self-approval for:
- Submissions (user submits their own document)
- Revisions (user revises their rejected document)
- Cancellations by owner

# Prevent self-approval for:
- Approvals (approver can't approve own submission)
- Financial authorizations
- Sensitive operations
```

**Configuration:**
```python
# Submission: allow self-approval
{
    "state": "Draft",
    "action": "Submit",
    "next_state": "Pending",
    "allowed": "Employee",
    "allow_self_approval": 1  # ✓ OK
}

# Approval: prevent self-approval
{
    "state": "Pending",
    "action": "Approve",
    "next_state": "Approved",
    "allowed": "Manager",
    "allow_self_approval": 0  # ✓ Secure
}
```

### 2. Don't Bypass Permission System

**Don't:**
```python
# Bad: Bypassing permissions
def before_transition(self, transition):
    doc = frappe.get_doc("Related Doc", name)
    doc.flags.ignore_permissions = True  # ❌ Dangerous
    doc.save()
```

**Do:**
```python
# Good: Respect permissions
def before_transition(self, transition):
    if frappe.has_permission("Related Doc", "write"):
        doc = frappe.get_doc("Related Doc", name)
        doc.save()
    else:
        frappe.throw("Insufficient permissions")
```

### 3. Validate Transition Logic

**Prevent unauthorized transitions:**
```python
def before_transition(self, transition):
    """Add extra security checks."""
    # Ensure user has proper authority
    if transition.action == "Approve":
        if self.requires_special_authority():
            if not self.user_has_special_authority(frappe.session.user):
                frappe.throw("This approval requires special authority")
```

### 4. Audit Workflow Actions

**Log important transitions:**
```python
def after_transition(self, transition):
    """Create audit trail."""
    if transition.action in ["Approve", "Reject", "Cancel"]:
        frappe.get_doc({
            "doctype": "Audit Log",
            "transaction_type": self.doctype,
            "transaction_name": self.name,
            "action": transition.action,
            "from_state": transition.state,
            "to_state": transition.next_state,
            "user": frappe.session.user,
            "timestamp": frappe.utils.now(),
            "ip_address": frappe.local.request_ip
        }).insert(ignore_permissions=True)
```

### 5. Protect Sensitive Data

**Control field visibility by state:**
```python
# In doctype_name.js
frappe.ui.form.on('DocType Name', {
    refresh: function(frm) {
        // Hide sensitive fields in certain states
        if (frm.doc.workflow_state != "Final Approval") {
            frm.set_df_property("confidential_data", "hidden", 1);
        }
    }
});
```

## Maintenance Best Practices

### 1. Version Control Workflows

**Export and commit:**
```bash
# Export workflow
bench --site sitename export-json "Workflow" "My Workflow" 

# Add to version control
git add fixtures/workflow_my_workflow.json
git commit -m "Add/Update My Workflow"
```

### 2. Monitor Workflow Health

**Track key metrics:**
```python
# Average time in each state
def get_state_duration_stats():
    return frappe.db.sql("""
        SELECT workflow_state, 
               AVG(TIMESTAMPDIFF(HOUR, creation, modified)) as avg_hours
        FROM `tabDocType Name`
        GROUP BY workflow_state
    """, as_dict=True)

# Stuck documents
def find_stuck_documents(days=7):
    cutoff = frappe.utils.add_to_date(None, days=-days)
    return frappe.get_all(
        "DocType Name",
        filters={
            "workflow_state": ["!=", "Approved"],
            "modified": ["<", cutoff],
            "docstatus": ["!=", 2]
        }
    )
```

### 3. Gather User Feedback

**Questions to ask:**
- Is the workflow clear?
- Are there too many/too few steps?
- Do action names make sense?
- Are notifications helpful?
- What bottlenecks exist?

### 4. Refactor When Needed

**Signs you need to refactor:**
- Users constantly confused
- Many rejected documents
- Bottlenecks at specific states
- Workflow actions pile up
- Complex workarounds needed

### 5. Keep Documentation Updated

**Maintain:**
- Workflow diagram
- State descriptions
- Role responsibilities
- Business rules
- Known issues
- Change history

## Common Gotchas

### 1. Forgotten Workflow State Field

**Problem:** Workflow not working, no errors
**Solution:** Check if workflow_state_field was created

```python
# Verify field exists
frappe.get_meta("DocType Name").get_field("workflow_state")
```

### 2. Conditions Always False

**Problem:** Transition never shows
**Solution:** Test condition in console

```python
doc = frappe.get_doc("DocType Name", "DOC-001")
condition = "doc.grand_total > 10000"
result = frappe.safe_eval(condition, {"doc": doc.as_dict()})
print(f"Condition result: {result}")
```

### 3. Circular Imports

**Problem:** Import errors in hooks
**Solution:** Import inside functions

```python
# Bad
from myapp.doctypes.doctype import function

def has_workflow_action_permission(user, transition, doc):
    return function(user, doc)

# Good
def has_workflow_action_permission(user, transition, doc):
    from myapp.doctypes.doctype import function
    return function(user, doc)
```

### 4. Email Not Sending

**Common Causes:**
- SMTP not configured
- send_email_alert not checked
- No users with required role
- Email queue not running

**Solution:**
```python
# Check workflow settings
workflow = frappe.get_doc("Workflow", "My Workflow")
print(f"Send email: {workflow.send_email_alert}")

# Check users with role
users = frappe.get_all("Has Role",
    filters={"role": "Approver", "parenttype": "User"},
    fields=["parent"])
print(f"Users: {users}")

# Check email queue
frappe.get_all("Email Queue", filters={"status": "Error"})
```

### 5. Transaction Rollback Issues

**Problem:** Changes in hooks get rolled back
**Solution:** Be careful with exceptions

```python
def after_transition(self, transition):
    # This will rollback if it fails
    self.critical_operation()
    
    # This won't rollback the transition
    try:
        self.optional_operation()
    except Exception as e:
        frappe.log_error(str(e))
```

## Checklist for Production Workflows

Before deploying a workflow:

- [ ] All states have clear, business-friendly names
- [ ] All actions are intuitive
- [ ] Docstatus mapping makes sense
- [ ] Self-approval settings are correct
- [ ] Conditions have been tested
- [ ] before_transition validations work correctly
- [ ] after_transition actions complete successfully
- [ ] Email notifications are configured
- [ ] Tested with all relevant roles
- [ ] Tested rejection and revision paths
- [ ] Performance is acceptable
- [ ] Documentation is complete
- [ ] Stakeholders have reviewed
- [ ] Audit trail is adequate
- [ ] Error handling is robust
- [ ] Edge cases are handled

## Summary

Key takeaways:

1. **Start simple, add complexity gradually**
2. **Use clear, business-friendly names**
3. **Plan docstatus carefully**
4. **Always provide rejection paths**
5. **Use conditions for simple logic, hooks for complex logic**
6. **Test thoroughly with all roles**
7. **Monitor and optimize performance**
8. **Validate security settings**
9. **Document everything**
10. **Gather feedback and iterate**

Remember: A good workflow is **simple**, **intuitive**, **secure**, and **maintainable**.
