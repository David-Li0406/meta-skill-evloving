# Workflow Examples

This document provides complete, working examples of common workflow patterns in Frappe.

## Example 1: Simple Leave Application Workflow

A basic two-level approval workflow for leave applications.

### Business Process

1. Employee submits leave application
2. HR Manager approves or rejects
3. If rejected, employee can revise and resubmit

### Workflow Configuration

**States:**
```python
states = [
    {
        "state": "Draft",
        "doc_status": "0",
        "allow_edit": "Employee"
    },
    {
        "state": "Pending Approval",
        "doc_status": "0",
        "allow_edit": "HR Manager"
    },
    {
        "state": "Approved",
        "doc_status": "1",
        "allow_edit": "HR Manager",
        "update_field": "status",
        "update_value": "Approved"
    },
    {
        "state": "Rejected",
        "doc_status": "0",
        "allow_edit": "Employee"
    }
]
```

**Transitions:**
```python
transitions = [
    {
        "state": "Draft",
        "action": "Submit for Approval",
        "next_state": "Pending Approval",
        "allowed": "Employee",
        "allow_self_approval": 1
    },
    {
        "state": "Pending Approval",
        "action": "Approve",
        "next_state": "Approved",
        "allowed": "HR Manager",
        "allow_self_approval": 0
    },
    {
        "state": "Pending Approval",
        "action": "Reject",
        "next_state": "Rejected",
        "allowed": "HR Manager",
        "allow_self_approval": 0
    },
    {
        "state": "Rejected",
        "action": "Resubmit",
        "next_state": "Pending Approval",
        "allowed": "Employee",
        "allow_self_approval": 1
    }
]
```

### Custom Logic

```python
# leave_application.py
class LeaveApplication(Document):
    def before_transition(self, transition):
        """Validate leave balance before approval."""
        if transition.action == "Approve":
            # Check leave balance
            balance = self.get_leave_balance()
            if balance < self.total_leave_days:
                frappe.throw(f"Insufficient leave balance. Available: {balance} days")
    
    def after_transition(self, transition):
        """Update leave ledger after approval."""
        if transition.action == "Approve":
            self.update_leave_ledger()
            self.notify_employee()
```

## Example 2: Purchase Order Multi-Level Approval

Amount-based routing with multiple approval levels.

### Business Process

1. Purchase User creates PO
2. If amount < $10,000: Manager can approve
3. If amount $10,000-$100,000: Manager + Director approval
4. If amount > $100,000: Manager + Director + CFO approval

### Workflow Configuration

**States:**
```python
states = [
    {"state": "Draft", "doc_status": "0", "allow_edit": "Purchase User"},
    {"state": "Pending Manager", "doc_status": "0", "allow_edit": "Purchase Manager"},
    {"state": "Pending Director", "doc_status": "0", "allow_edit": "Purchase Director"},
    {"state": "Pending CFO", "doc_status": "0", "allow_edit": "CFO"},
    {"state": "Approved", "doc_status": "1", "allow_edit": "Purchase Manager"},
    {"state": "Rejected", "doc_status": "0", "allow_edit": "Purchase User"}
]
```

**Transitions (with conditions):**
```python
transitions = [
    {
        "state": "Draft",
        "action": "Submit",
        "next_state": "Pending Manager",
        "allowed": "Purchase User",
        "allow_self_approval": 1
    },
    # Low amount - Manager can approve directly
    {
        "state": "Pending Manager",
        "action": "Approve",
        "next_state": "Approved",
        "allowed": "Purchase Manager",
        "allow_self_approval": 0,
        "condition": "doc.grand_total < 10000"
    },
    # Medium amount - needs Director
    {
        "state": "Pending Manager",
        "action": "Forward to Director",
        "next_state": "Pending Director",
        "allowed": "Purchase Manager",
        "allow_self_approval": 0,
        "condition": "doc.grand_total >= 10000 and doc.grand_total < 100000"
    },
    # High amount - needs Director then CFO
    {
        "state": "Pending Manager",
        "action": "Forward to Director",
        "next_state": "Pending Director",
        "allowed": "Purchase Manager",
        "allow_self_approval": 0,
        "condition": "doc.grand_total >= 100000"
    },
    # Director approves medium amount
    {
        "state": "Pending Director",
        "action": "Approve",
        "next_state": "Approved",
        "allowed": "Purchase Director",
        "allow_self_approval": 0,
        "condition": "doc.grand_total < 100000"
    },
    # Director forwards high amount to CFO
    {
        "state": "Pending Director",
        "action": "Forward to CFO",
        "next_state": "Pending CFO",
        "allowed": "Purchase Director",
        "allow_self_approval": 0,
        "condition": "doc.grand_total >= 100000"
    },
    # CFO final approval
    {
        "state": "Pending CFO",
        "action": "Approve",
        "next_state": "Approved",
        "allowed": "CFO",
        "allow_self_approval": 0
    },
    # Rejection from any level
    {
        "state": "Pending Manager",
        "action": "Reject",
        "next_state": "Rejected",
        "allowed": "Purchase Manager"
    },
    {
        "state": "Pending Director",
        "action": "Reject",
        "next_state": "Rejected",
        "allowed": "Purchase Director"
    },
    {
        "state": "Pending CFO",
        "action": "Reject",
        "next_state": "Rejected",
        "allowed": "CFO"
    },
    # Revision
    {
        "state": "Rejected",
        "action": "Revise",
        "next_state": "Draft",
        "allowed": "Purchase User",
        "allow_self_approval": 1
    }
]
```

### Custom Hooks

```python
# hooks.py
has_workflow_action_permission = [
    "myapp.purchase_order.has_po_action_permission"
]

# purchase_order.py
def has_po_action_permission(user, transition, doc):
    """Route to users with sufficient approval limit."""
    if doc.get("doctype") != "Purchase Order":
        return True
    
    # Get user's approval limit
    approval_limit = frappe.db.get_value(
        "Approver Settings",
        {"user": user},
        "purchase_order_limit"
    ) or 0
    
    amount = doc.get("grand_total", 0)
    return amount <= approval_limit
```

## Example 3: Quality Control Workflow

Workflow with inspection and conditional acceptance.

### Business Process

1. Item arrives, QC inspection requested
2. Inspector performs quality check
3. If pass: Accept
4. If minor issues: Conditional Accept (requires manager approval)
5. If fail: Reject (requires manager confirmation)

### Workflow Configuration

**States:**
```python
states = [
    {"state": "Pending Inspection", "doc_status": "0", "allow_edit": "QC Inspector"},
    {"state": "Passed", "doc_status": "1", "allow_edit": "QC Inspector"},
    {"state": "Conditionally Accepted", "doc_status": "1", "allow_edit": "QC Manager"},
    {"state": "Rejected", "doc_status": "2", "allow_edit": "QC Manager"},
    {"state": "Pending Manager Review", "doc_status": "0", "allow_edit": "QC Manager"}
]
```

**Transitions:**
```python
transitions = [
    {
        "state": "Pending Inspection",
        "action": "Pass",
        "next_state": "Passed",
        "allowed": "QC Inspector",
        "condition": "doc.inspection_result == 'Passed'"
    },
    {
        "state": "Pending Inspection",
        "action": "Minor Issues",
        "next_state": "Pending Manager Review",
        "allowed": "QC Inspector",
        "condition": "doc.inspection_result == 'Minor Issues'"
    },
    {
        "state": "Pending Inspection",
        "action": "Fail",
        "next_state": "Pending Manager Review",
        "allowed": "QC Inspector",
        "condition": "doc.inspection_result == 'Failed'"
    },
    {
        "state": "Pending Manager Review",
        "action": "Accept with Conditions",
        "next_state": "Conditionally Accepted",
        "allowed": "QC Manager",
        "condition": "doc.inspection_result == 'Minor Issues'"
    },
    {
        "state": "Pending Manager Review",
        "action": "Confirm Rejection",
        "next_state": "Rejected",
        "allowed": "QC Manager",
        "condition": "doc.inspection_result == 'Failed'"
    }
]
```

### Custom Logic

```python
class QualityInspection(Document):
    def before_transition(self, transition):
        """Ensure inspection is complete."""
        if not self.inspection_completed:
            frappe.throw("Please complete the inspection before taking action")
        
        if transition.action == "Pass":
            # Verify all parameters are within limits
            for param in self.parameters:
                if not param.within_limits:
                    frappe.throw(f"Parameter {param.parameter} is out of limits")
    
    def after_transition(self, transition):
        """Update inventory status."""
        if transition.next_state == "Passed":
            self.update_stock_status("Accepted")
        elif transition.next_state == "Rejected":
            self.update_stock_status("Rejected")
            self.create_return_request()
```

## Example 4: Expense Claim with Delegation

Workflow that supports delegation and out-of-office scenarios.

### Business Process

1. Employee submits expense claim
2. Manager approves
3. Finance verifies and processes
4. Handle manager absence through delegation

### Workflow Configuration

**States:**
```python
states = [
    {"state": "Draft", "doc_status": "0", "allow_edit": "Employee"},
    {"state": "Pending Manager", "doc_status": "0", "allow_edit": "Manager"},
    {"state": "Pending Finance", "doc_status": "0", "allow_edit": "Finance Manager"},
    {"state": "Approved", "doc_status": "1", "allow_edit": "Finance Manager"},
    {"state": "Rejected", "doc_status": "0", "allow_edit": "Employee"}
]
```

**Transitions:**
```python
transitions = [
    {
        "state": "Draft",
        "action": "Submit",
        "next_state": "Pending Manager",
        "allowed": "Employee",
        "allow_self_approval": 1
    },
    {
        "state": "Pending Manager",
        "action": "Approve",
        "next_state": "Pending Finance",
        "allowed": "Manager",
        "allow_self_approval": 0
    },
    {
        "state": "Pending Finance",
        "action": "Verify and Approve",
        "next_state": "Approved",
        "allowed": "Finance Manager",
        "allow_self_approval": 0
    },
    {
        "state": "Pending Manager",
        "action": "Reject",
        "next_state": "Rejected",
        "allowed": "Manager"
    },
    {
        "state": "Pending Finance",
        "action": "Reject",
        "next_state": "Rejected",
        "allowed": "Finance Manager"
    }
]
```

### Delegation Logic

```python
# hooks.py
has_workflow_action_permission = [
    "myapp.expense_claim.has_expense_action_permission"
]

def has_expense_action_permission(user, transition, doc):
    """Handle delegation for absent managers."""
    if doc.get("doctype") != "Expense Claim":
        return True
    
    # Get employee's manager
    employee = doc.get("employee")
    reports_to = frappe.db.get_value("Employee", employee, "reports_to")
    manager_user = frappe.db.get_value("Employee", reports_to, "user_id")
    
    # Check if user is the manager
    if user == manager_user:
        return True
    
    # Check if manager is on leave and user is delegate
    is_on_leave = frappe.db.exists(
        "Leave Application",
        {
            "employee": reports_to,
            "status": "Approved",
            "from_date": ["<=", frappe.utils.today()],
            "to_date": [">=", frappe.utils.today()],
            "leave_approver": user  # User is the delegate
        }
    )
    
    return bool(is_on_leave)
```

## Example 5: Document Review Cycle

Iterative review workflow with multiple rounds.

### Business Process

1. Author submits document for review
2. Reviewer can approve or request changes
3. If changes requested, author revises
4. Process repeats until approved
5. Final publication by editor

### Workflow Configuration

**States:**
```python
states = [
    {"state": "Draft", "doc_status": "0", "allow_edit": "Author"},
    {"state": "In Review", "doc_status": "0", "allow_edit": "Reviewer"},
    {"state": "Changes Requested", "doc_status": "0", "allow_edit": "Author"},
    {"state": "Approved", "doc_status": "0", "allow_edit": "Editor"},
    {"state": "Published", "doc_status": "1", "allow_edit": "Editor"}
]
```

**Transitions:**
```python
transitions = [
    {
        "state": "Draft",
        "action": "Submit for Review",
        "next_state": "In Review",
        "allowed": "Author",
        "allow_self_approval": 1
    },
    {
        "state": "In Review",
        "action": "Approve",
        "next_state": "Approved",
        "allowed": "Reviewer",
        "allow_self_approval": 0
    },
    {
        "state": "In Review",
        "action": "Request Changes",
        "next_state": "Changes Requested",
        "allowed": "Reviewer",
        "allow_self_approval": 0
    },
    {
        "state": "Changes Requested",
        "action": "Resubmit",
        "next_state": "In Review",
        "allowed": "Author",
        "allow_self_approval": 1
    },
    {
        "state": "Approved",
        "action": "Publish",
        "next_state": "Published",
        "allowed": "Editor",
        "allow_self_approval": 0
    }
]
```

### Tracking Review History

```python
class Document(Document):
    def after_transition(self, transition):
        """Track review history."""
        if transition.action in ["Request Changes", "Approve"]:
            # Add review comment
            self.add_comment(
                "Workflow",
                f"{transition.action} by {frappe.session.user}"
            )
            
            # Increment review count
            if transition.action == "Request Changes":
                self.review_count = (self.review_count or 0) + 1
                self.db_update()
```

## Example 6: Parallel Approval Workflow

Requires approval from multiple departments simultaneously.

### Business Process

1. Submit for both Finance and Legal review
2. Both must approve before final approval
3. Either can reject

### Implementation Strategy

Since Frappe workflows are linear, implement parallel approval using custom logic:

**States:**
```python
states = [
    {"state": "Draft", "doc_status": "0", "allow_edit": "Submitter"},
    {"state": "Pending Reviews", "doc_status": "0", "allow_edit": "All"},
    {"state": "Finance Approved", "doc_status": "0", "allow_edit": "All"},
    {"state": "Legal Approved", "doc_status": "0", "allow_edit": "All"},
    {"state": "Both Approved", "doc_status": "1", "allow_edit": "All"},
    {"state": "Rejected", "doc_status": "0", "allow_edit": "Submitter"}
]
```

**Custom Logic:**
```python
class Contract(Document):
    def before_transition(self, transition):
        """Handle parallel approvals."""
        current_state = self.workflow_state
        
        if transition.action == "Finance Approve":
            if current_state == "Legal Approved":
                # Both approved, move to final state
                transition.next_state = "Both Approved"
            else:
                transition.next_state = "Finance Approved"
        
        elif transition.action == "Legal Approve":
            if current_state == "Finance Approved":
                # Both approved, move to final state
                transition.next_state = "Both Approved"
            else:
                transition.next_state = "Legal Approved"
    
    def after_transition(self, transition):
        """Notify when both approvals received."""
        if transition.next_state == "Both Approved":
            self.send_final_approval_notification()
```

## Example 7: Time-Sensitive Workflow

Workflow with auto-escalation for time-sensitive approvals.

### Business Process

1. Submit request
2. If not approved within 24 hours, escalate to senior manager
3. If not approved within 48 hours, escalate to director

### Workflow Configuration

**States:**
```python
states = [
    {"state": "Pending Manager", "doc_status": "0", "allow_edit": "Manager"},
    {"state": "Escalated to Senior", "doc_status": "0", "allow_edit": "Senior Manager"},
    {"state": "Escalated to Director", "doc_status": "0", "allow_edit": "Director"},
    {"state": "Approved", "doc_status": "1", "allow_edit": "All"},
]
```

**Scheduled Job:**
```python
# scheduled_tasks.py
def escalate_pending_approvals():
    """Run hourly to check for escalations."""
    from frappe.model.workflow import apply_workflow
    from datetime import datetime, timedelta
    
    # Find requests pending for > 24 hours
    requests = frappe.get_all(
        "Request",
        filters={
            "workflow_state": "Pending Manager",
            "modified": ["<", datetime.now() - timedelta(hours=24)]
        }
    )
    
    for req in requests:
        doc = frappe.get_doc("Request", req.name)
        apply_workflow(doc, "Escalate")
        frappe.db.commit()
```

## Example 8: Budget Approval with Availability Check

Validate budget availability before approval.

### Workflow Configuration

Standard approval workflow with custom validation.

### Custom Logic

```python
class BudgetRequest(Document):
    def before_transition(self, transition):
        """Check budget availability before approval."""
        if transition.action == "Approve":
            # Check if budget is available
            cost_center = self.cost_center
            fiscal_year = self.fiscal_year
            account = self.account
            
            available_budget = self.get_available_budget(
                cost_center, fiscal_year, account
            )
            
            if available_budget < self.amount:
                frappe.throw(
                    f"Insufficient budget. Available: {available_budget}, "
                    f"Requested: {self.amount}"
                )
            
            # Reserve the budget
            self.reserve_budget(cost_center, fiscal_year, account, self.amount)
    
    def after_transition(self, transition):
        """Update budget ledger after approval."""
        if transition.action == "Approve":
            self.update_budget_ledger()
        
        elif transition.action == "Reject":
            # Release reserved budget
            self.release_reserved_budget()
```

## Testing Workflows

Example test case for workflow:

```python
# test_workflow.py
import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.model.workflow import apply_workflow, get_transitions

class TestLeaveWorkflow(FrappeTestCase):
    def setUp(self):
        self.create_test_workflow()
    
    def test_leave_approval_workflow(self):
        """Test complete leave approval cycle."""
        # Create leave application
        leave = frappe.get_doc({
            "doctype": "Leave Application",
            "employee": "EMP-001",
            "from_date": "2024-01-01",
            "to_date": "2024-01-05",
            "leave_type": "Casual Leave",
            "total_leave_days": 5
        }).insert()
        
        # Check initial state
        self.assertEqual(leave.workflow_state, "Draft")
        
        # Submit for approval
        apply_workflow(leave, "Submit for Approval")
        leave.reload()
        self.assertEqual(leave.workflow_state, "Pending Approval")
        
        # Manager approves
        frappe.set_user("hr.manager@example.com")
        apply_workflow(leave, "Approve")
        leave.reload()
        
        # Check final state
        self.assertEqual(leave.workflow_state, "Approved")
        self.assertEqual(leave.docstatus, 1)
```

## Summary

These examples demonstrate:

1. **Simple Approval**: Basic two-level workflow
2. **Conditional Routing**: Amount-based approval routing
3. **Quality Control**: Inspection with conditional acceptance
4. **Delegation**: Handling absent approvers
5. **Review Cycles**: Iterative review process
6. **Parallel Approval**: Multiple department approval
7. **Time-Sensitive**: Auto-escalation workflows
8. **Budget Validation**: Pre-approval validation

Each pattern can be adapted to your specific business needs. The key is to:
- Start with clear business requirements
- Map states and transitions carefully
- Use conditions for dynamic routing
- Implement custom logic in hooks when needed
- Test thoroughly with different scenarios
