# Workflow Hooks

This document details all workflow extension hooks with comprehensive examples.

## Overview

Frappe provides five main hooks for extending workflow behavior:

1. **before_transition**: Controller method called before state change
2. **after_transition**: Controller method called after state change
3. **filter_workflow_transitions**: Hook to customize available transitions
4. **has_workflow_action_permission**: Hook to control who gets workflow actions
5. **workflow_safe_eval_globals**: Hook to extend available globals in transition conditions

## 1. before_transition Hook

### Purpose

Execute custom logic before a workflow state transition occurs. Use this for validation, preparation, or preventing unwanted transitions.

### Location

Implement as a method in your DocType's Python controller.

### Signature

```python
def before_transition(self, transition):
    """
    Called before workflow state changes.
    
    Args:
        transition (dict): Transition information containing:
            - action: Action name (e.g., "Approve")
            - state: Current state
            - next_state: State transitioning to
            - allowed: Role allowed for transition
            - allow_self_approval: Boolean
            - condition: Condition expression (if any)
    
    Raises:
        frappe.ValidationError: To prevent the transition
    """
```

### The Transition Object

```python
{
    "action": "Approve",
    "state": "Pending",
    "next_state": "Approved",
    "allowed": "Approver",
    "allow_self_approval": 1,
    "condition": "doc.amount > 1000"
}
```

### Examples

#### Example 1: Validation Before Approval

```python
class PurchaseOrder(Document):
    def before_transition(self, transition):
        """Validate data before approval."""
        if transition.action == "Approve":
            # Ensure all items have been verified
            if not all(item.verified for item in self.items):
                frappe.throw("All items must be verified before approval")
            
            # Check budget availability
            if not self.check_budget_available():
                frappe.throw("Insufficient budget for this purchase order")
            
            # Validate supplier is active
            supplier_status = frappe.db.get_value("Supplier", self.supplier, "disabled")
            if supplier_status:
                frappe.throw(f"Cannot approve. Supplier {self.supplier} is disabled")
```

#### Example 2: Update Related Documents

```python
class LeaveApplication(Document):
    def before_transition(self, transition):
        """Update leave balance before approval."""
        if transition.action == "Approve":
            # Check if employee has sufficient leave balance
            leave_balance = self.get_leave_balance()
            if leave_balance < self.total_leave_days:
                frappe.throw(
                    f"Insufficient leave balance. Available: {leave_balance}, "
                    f"Requested: {self.total_leave_days}"
                )
```

#### Example 3: Create Notifications

```python
class Expense Claim(Document):
    def before_transition(self, transition):
        """Notify stakeholders before state change."""
        if transition.action == "Submit for Approval":
            # Notify finance team about new claim
            self.send_notification_to_finance_team()
        
        elif transition.action == "Reject":
            # Notify employee about rejection
            self.add_comment(
                "Comment",
                f"Expense claim rejected. Please review and resubmit."
            )
```

#### Example 4: Prevent Transition Based on Conditions

```python
class SalesOrder(Document):
    def before_transition(self, transition):
        """Prevent approval during certain conditions."""
        if transition.action == "Approve":
            # Check if customer has outstanding invoices
            outstanding = frappe.db.get_value(
                "Customer",
                self.customer,
                "outstanding_amount"
            )
            
            if outstanding > 100000:
                frappe.throw(
                    f"Cannot approve. Customer has outstanding amount of "
                    f"{frappe.format_value(outstanding, {'fieldtype': 'Currency'})}"
                )
            
            # Prevent approval on weekends
            from datetime import datetime
            if datetime.now().weekday() >= 5:  # Saturday or Sunday
                frappe.throw("Orders cannot be approved on weekends")
```

#### Example 5: Lock Related Documents

```python
class PayrollEntry(Document):
    def before_transition(self, transition):
        """Lock timesheets before processing payroll."""
        if transition.action == "Submit for Approval":
            # Lock all related timesheets
            for employee in self.employees:
                timesheets = frappe.get_all(
                    "Timesheet",
                    filters={
                        "employee": employee.employee,
                        "start_date": [">=", self.start_date],
                        "end_date": ["<=", self.end_date],
                        "docstatus": 1
                    }
                )
                
                for ts in timesheets:
                    frappe.db.set_value("Timesheet", ts.name, "locked", 1)
```

## 2. after_transition Hook

### Purpose

Execute custom logic after a workflow state transition has been successfully completed. Use this for follow-up actions, integrations, or cascading updates.

### Location

Implement as a method in your DocType's Python controller.

### Signature

```python
def after_transition(self, transition):
    """
    Called after workflow state changes and document is saved.
    
    Args:
        transition (dict): Same transition information as before_transition
        
    Note:
        Document is already saved at this point.
        Any changes made here require calling self.db_update() or self.save()
    """
```

### Examples

#### Example 1: Create Follow-up Tasks

```python
class Project(Document):
    def after_transition(self, transition):
        """Create tasks based on project approval."""
        if transition.action == "Approve":
            # Create initial project tasks
            tasks = [
                {"title": "Project Kickoff Meeting", "priority": "High"},
                {"title": "Resource Allocation", "priority": "High"},
                {"title": "Create Project Plan", "priority": "Medium"}
            ]
            
            for task_data in tasks:
                task = frappe.get_doc({
                    "doctype": "Task",
                    "project": self.name,
                    "subject": task_data["title"],
                    "priority": task_data["priority"],
                    "exp_start_date": self.start_date
                })
                task.insert()
```

#### Example 2: Update Inventory

```python
class StockEntry(Document):
    def after_transition(self, transition):
        """Reserve stock after approval."""
        if transition.action == "Approve":
            # Reserve items in warehouse
            for item in self.items:
                self.reserve_stock(item.item_code, item.qty, item.warehouse)
            
            # Create delivery note if applicable
            if self.purpose == "Material Transfer":
                self.create_delivery_note()
```

#### Example 3: Send External Notifications

```python
class Invoice(Document):
    def after_transition(self, transition):
        """Send invoice to customer after approval."""
        if transition.action == "Approve":
            # Send invoice via email
            self.send_invoice_email()
            
            # Update accounting system
            self.post_to_accounting_system()
            
            # Notify CRM
            self.update_crm_status()
```

#### Example 4: Update Parent Document

```python
class TimelogDetail(Document):
    def after_transition(self, transition):
        """Update project status when timelog is approved."""
        if transition.action == "Approve":
            # Update total billed hours in project
            project = frappe.get_doc("Project", self.project)
            project.total_billed_hours = project.total_billed_hours + self.hours
            project.db_update()
            
            # If all timelogs approved, mark project phase complete
            if self.is_last_timelog_in_phase():
                project.mark_phase_complete(self.phase)
```

#### Example 5: Cascade Approvals

```python
class PurchaseOrder(Document):
    def after_transition(self, transition):
        """Auto-approve related documents after PO approval."""
        if transition.action == "Approve":
            # Auto-approve linked purchase receipts
            receipts = frappe.get_all(
                "Purchase Receipt",
                filters={"purchase_order": self.name, "workflow_state": "Pending"},
                pluck="name"
            )
            
            for receipt_name in receipts:
                receipt = frappe.get_doc("Purchase Receipt", receipt_name)
                from frappe.model.workflow import apply_workflow
                apply_workflow(receipt, "Approve")
```

#### Example 6: Create Audit Trail

```python
class ComplianceDocument(Document):
    def after_transition(self, transition):
        """Create detailed audit trail."""
        # Log transition details
        frappe.get_doc({
            "doctype": "Compliance Audit Log",
            "document_type": self.doctype,
            "document_name": self.name,
            "transition_date": frappe.utils.now(),
            "from_state": transition.state,
            "to_state": transition.next_state,
            "action": transition.action,
            "user": frappe.session.user,
            "remarks": self.get_transition_remarks()
        }).insert()
```

## 3. filter_workflow_transitions Hook

### Purpose

Filter or modify the list of available workflow transitions before displaying them to users. This allows dynamic transition visibility based on custom logic.

### Location

Register in `hooks.py` file of your app.

### Registration

```python
# hooks.py
filter_workflow_transitions = [
    "myapp.workflows.custom_transition_filter"
]
```

### Signature

```python
def custom_transition_filter(doc, transitions, workflow):
    """
    Filter transitions before displaying to user.
    
    Args:
        doc: Document instance (frappe.model.document.Document)
        transitions: List of available transition dicts
        workflow: Workflow document instance
        
    Returns:
        List of filtered transitions, or None to keep all
        
    Note:
        Return None to pass through without changes
        Return [] to hide all transitions
        Return modified list to customize
    """
```

### Examples

#### Example 1: Amount-Based Transition Filtering

```python
def filter_workflow_transitions(doc, transitions, workflow):
    """Show different transitions based on amount."""
    if doc.doctype != "Purchase Order":
        return None
    
    filtered_transitions = []
    amount = doc.grand_total
    
    for transition in transitions:
        # High-value orders require CFO approval
        if amount > 100000 and transition.action == "Approve":
            if frappe.has_role("CFO"):
                filtered_transitions.append(transition)
        # Medium-value orders require Manager approval
        elif amount > 10000 and transition.action == "Approve":
            if frappe.has_role("Purchase Manager"):
                filtered_transitions.append(transition)
        # Low-value orders can be auto-approved
        else:
            filtered_transitions.append(transition)
    
    return filtered_transitions
```

#### Example 2: Time-Based Restrictions

```python
def filter_workflow_transitions(doc, transitions, workflow):
    """Restrict approvals during certain time periods."""
    from datetime import datetime, time
    
    if doc.doctype != "Expense Claim":
        return None
    
    current_time = datetime.now().time()
    current_day = datetime.now().weekday()
    
    # No approvals on weekends
    if current_day >= 5:  # Saturday or Sunday
        return []
    
    # Approvals only during business hours (9 AM - 6 PM)
    business_start = time(9, 0)
    business_end = time(18, 0)
    
    if not (business_start <= current_time <= business_end):
        return []
    
    return transitions
```

#### Example 3: Role-Based Transition Customization

```python
def filter_workflow_transitions(doc, transitions, workflow):
    """Customize transitions based on user's specific role."""
    if doc.doctype != "Leave Application":
        return None
    
    user = frappe.session.user
    filtered = []
    
    for transition in transitions:
        # Only show 'Cancel' to HR
        if transition.action == "Cancel":
            if frappe.has_role("HR Manager"):
                filtered.append(transition)
        
        # Only show 'Override Reject' to Admin
        elif transition.action == "Override Reject":
            if frappe.has_role("System Manager"):
                filtered.append(transition)
        
        # Other transitions available to all
        else:
            filtered.append(transition)
    
    return filtered
```

#### Example 4: Dependent Document Status

```python
def filter_workflow_transitions(doc, transitions, workflow):
    """Filter based on related document status."""
    if doc.doctype != "Sales Order":
        return None
    
    # Check if quotation is approved
    if doc.quotation:
        quotation_state = frappe.db.get_value(
            "Quotation",
            doc.quotation,
            "workflow_state"
        )
        
        if quotation_state != "Approved":
            # Don't allow approval if quotation not approved
            return [
                t for t in transitions
                if t.action != "Approve"
            ]
    
    return transitions
```

#### Example 5: Sequential Approvals

```python
def filter_workflow_transitions(doc, transitions, workflow):
    """Enforce sequential approval order."""
    if doc.doctype != "Budget Request":
        return None
    
    current_state = doc.workflow_state
    
    # Define approval sequence
    approval_sequence = {
        "Pending": ["Department Head Approval"],
        "Dept Head Approved": ["Finance Manager Approval"],
        "Finance Approved": ["CFO Approval"]
    }
    
    allowed_actions = approval_sequence.get(current_state, [])
    
    return [
        t for t in transitions
        if t.action in allowed_actions or t.action in ["Reject", "Send Back"]
    ]
```

#### Example 6: Hide Transitions Based on Custom Logic

```python
def filter_workflow_transitions(doc, transitions, workflow):
    """Hide specific transitions based on document fields."""
    if doc.doctype != "Quality Inspection":
        return None
    
    filtered = []
    
    for transition in transitions:
        # Hide 'Accept' if any items failed inspection
        if transition.action == "Accept":
            if doc.status == "Rejected":
                continue
        
        # Hide 'Conditional Accept' if all items passed
        elif transition.action == "Conditional Accept":
            if doc.status == "Accepted":
                continue
        
        filtered.append(transition)
    
    return filtered
```

## 4. has_workflow_action_permission Hook

### Purpose

Control which users receive workflow action notifications and permissions. This enables sophisticated approval routing based on custom logic.

### Location

Register in `hooks.py` file of your app.

### Registration

```python
# hooks.py
has_workflow_action_permission = [
    "myapp.workflows.custom_action_permission"
]
```

### Signature

```python
def custom_action_permission(user, transition, doc):
    """
    Check if user should receive workflow action for this transition.
    
    Args:
        user (str): User email
        transition (dict): Transition information
        doc: Document instance or dict
        
    Returns:
        bool: True if user should get action, False otherwise
        
    Note:
        Called AFTER role check, so user already has the required role
        Use this to add additional filtering
    """
```

### Examples

#### Example 1: Hierarchical Approval

```python
def has_workflow_action_permission(user, transition, doc):
    """Route approvals through management hierarchy."""
    if doc.get("doctype") != "Leave Application":
        return True
    
    if transition.get("action") != "Approve":
        return True
    
    # Get employee's reporting manager
    employee = doc.get("employee")
    reports_to = frappe.db.get_value("Employee", employee, "reports_to")
    user_employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
    
    # Only direct manager gets the action
    return user_employee == reports_to
```

#### Example 2: Amount-Based Routing

```python
def has_workflow_action_permission(user, transition, doc):
    """Route to specific approvers based on amount."""
    if doc.get("doctype") != "Purchase Order":
        return True
    
    if transition.get("action") != "Approve":
        return True
    
    amount = doc.get("grand_total", 0)
    
    # Get user's approval limit
    approval_limit = frappe.db.get_value(
        "Approver",
        {"user": user},
        "approval_limit"
    ) or 0
    
    # User can only approve within their limit
    return amount <= approval_limit
```

#### Example 3: Department-Based Routing

```python
def has_workflow_action_permission(user, transition, doc):
    """Route to department heads."""
    if doc.get("doctype") != "Expense Claim":
        return True
    
    # Get document's department
    doc_department = doc.get("department")
    
    # Get user's department (if they're a department head)
    user_department = frappe.db.get_value(
        "Employee",
        {"user_id": user, "designation": ["like", "%Head%"]},
        "department"
    )
    
    # Only department head of the same department gets action
    return user_department == doc_department
```

#### Example 4: Region-Based Routing

```python
def has_workflow_action_permission(user, transition, doc):
    """Route to regional managers."""
    if doc.get("doctype") not in ["Sales Order", "Quotation"]:
        return True
    
    # Get document's territory
    territory = doc.get("territory")
    
    # Get user's assigned territories
    user_territories = frappe.get_all(
        "User Territory",
        filters={"parent": user},
        pluck="territory"
    )
    
    # Check if territory matches or is child of user's territory
    return is_territory_in_user_region(territory, user_territories)

def is_territory_in_user_region(territory, user_territories):
    """Check if territory is under user's region."""
    if territory in user_territories:
        return True
    
    # Check parent territories
    parent = frappe.db.get_value("Territory", territory, "parent_territory")
    if parent and parent != "All Territories":
        return is_territory_in_user_region(parent, user_territories)
    
    return False
```

#### Example 5: Skill-Based Routing

```python
def has_workflow_action_permission(user, transition, doc):
    """Route to users with specific skills."""
    if doc.get("doctype") != "Task":
        return True
    
    # Get required skills for this task
    required_skills = [
        skill.skill for skill in doc.get("required_skills", [])
    ]
    
    if not required_skills:
        return True
    
    # Get user's skills
    user_skills = frappe.get_all(
        "Employee Skill",
        filters={
            "parent": frappe.db.get_value("Employee", {"user_id": user}, "name")
        },
        pluck="skill"
    )
    
    # User must have at least one required skill
    return bool(set(required_skills) & set(user_skills))
```

#### Example 6: Workload-Based Routing

```python
def has_workflow_action_permission(user, transition, doc):
    """Route to approvers with lowest workload."""
    if doc.get("doctype") != "Support Ticket":
        return True
    
    # Get user's current open workflow actions
    open_actions = frappe.db.count(
        "Workflow Action",
        filters={"user": user, "status": "Open"}
    )
    
    # Don't route to users with more than 10 pending actions
    return open_actions < 10
```

#### Example 7: Availability-Based Routing

```python
def has_workflow_action_permission(user, transition, doc):
    """Only route to available users."""
    if doc.get("doctype") != "Leave Application":
        return True
    
    # Check if user is on leave
    on_leave = frappe.db.exists(
        "Leave Application",
        {
            "leave_approver": user,
            "status": "Approved",
            "from_date": ["<=", frappe.utils.today()],
            "to_date": [">=", frappe.utils.today()]
        }
    )
    
    return not on_leave
```

## 5. workflow_safe_eval_globals Hook

### Purpose

Extend the available globals (functions and data) in workflow transition conditions. By default, workflow conditions have limited access to functions for security. This hook allows apps to add custom functions or data that can be used in transition condition expressions.

### Location

Registered in `hooks.py`.

### Signature

```python
def get_workflow_globals(current_globals):
    """
    Extend available globals for workflow transition conditions.
    
    Args:
        current_globals (dict): Currently available globals including:
            - frappe.db.get_value
            - frappe.db.get_list
            - frappe.session
            - frappe.utils.now_datetime
            - frappe.utils.add_to_date
            - frappe.utils.get_datetime
            - frappe.utils.now
    
    Returns:
        dict: Additional globals to make available in workflow conditions
    """
```

### Registration

```python
# In hooks.py
workflow_safe_eval_globals = [
    "my_app.workflow.get_workflow_globals",
]
```

### Default Available Globals

Without any hooks, workflow transition conditions have access to:
- `doc` - The document as a dict
- `frappe.db.get_value` - Fetch single value from database
- `frappe.db.get_list` - Fetch list of records
- `frappe.session` - Current session object (user, roles, etc.)
- `frappe.utils.now_datetime` - Current datetime
- `frappe.utils.add_to_date` - Add/subtract date intervals
- `frappe.utils.get_datetime` - Parse datetime string
- `frappe.utils.now` - Current timestamp

### Examples

#### Example 1: Add Helper Function for Approval Limits

```python
# my_app/workflow.py
def get_workflow_globals(current_globals):
    """Add approval limit checker."""
    
    def get_approval_limit(user):
        """Get user's approval limit from their role or user settings."""
        # Check user-specific limit first
        limit = frappe.db.get_value("User", user, "approval_limit")
        if limit:
            return limit
        
        # Otherwise get from highest role
        roles = frappe.get_roles(user)
        limits = frappe.db.get_all(
            "Role",
            filters={"name": ["in", roles]},
            fields=["approval_limit"],
            order_by="approval_limit desc",
            limit=1
        )
        
        return limits[0].approval_limit if limits else 0
    
    return {
        "get_approval_limit": get_approval_limit,
    }

# In Workflow Transition condition field:
# doc.grand_total <= get_approval_limit(frappe.session.user)
```

#### Example 2: Add Business Logic Functions

```python
# my_app/workflow.py
def get_workflow_globals(current_globals):
    """Add business-specific helper functions."""
    
    def is_business_hours():
        """Check if current time is during business hours (9 AM - 5 PM, Mon-Fri)."""
        from datetime import datetime
        now = datetime.now()
        return 9 <= now.hour < 17 and now.weekday() < 5
    
    def get_regional_manager(region):
        """Get the manager assigned to a specific region."""
        return frappe.db.get_value("Region", region, "manager")
    
    def has_sufficient_stock(item_code, qty):
        """Check if item has sufficient stock across all warehouses."""
        total_stock = frappe.db.get_value(
            "Bin",
            {"item_code": item_code},
            "sum(actual_qty)"
        ) or 0
        return total_stock >= qty
    
    return {
        "is_business_hours": is_business_hours,
        "get_regional_manager": get_regional_manager,
        "has_sufficient_stock": has_sufficient_stock,
    }

# In Workflow Transition conditions:
# Urgent approvals only during business hours:
# doc.priority == "Urgent" and is_business_hours()

# Route to regional manager:
# doc.assigned_to == get_regional_manager(doc.region)

# Approve only if stock available:
# has_sufficient_stock(doc.item_code, doc.qty)
```

#### Example 3: Add Configuration Data

```python
# my_app/workflow.py
def get_workflow_globals(current_globals):
    """Add cached configuration data."""
    
    # Load workflow configuration (cached for performance)
    config = frappe.cache().get_value("workflow_config")
    if not config:
        workflow_settings = frappe.get_single("Workflow Settings")
        config = {
            "min_amount_for_approval": workflow_settings.min_amount_for_approval,
            "max_auto_approve_amount": workflow_settings.max_auto_approve_amount,
            "require_dual_approval_above": workflow_settings.require_dual_approval_above,
            "approval_timeout_hours": workflow_settings.approval_timeout_hours,
        }
        frappe.cache().set_value("workflow_config", config, expires_in_sec=3600)
    
    return {
        "workflow_config": config,
    }

# In Workflow Transition conditions:
# doc.grand_total >= workflow_config["min_amount_for_approval"]
# doc.grand_total <= workflow_config["max_auto_approve_amount"]
```

#### Example 4: Department and Hierarchy Checks

```python
# my_app/workflow.py
def get_workflow_globals(current_globals):
    """Add organization hierarchy helpers."""
    
    def is_users_department(dept):
        """Check if department belongs to current user."""
        user_dept = frappe.db.get_value("User", frappe.session.user, "department")
        return dept == user_dept
    
    def is_subordinate_department(dept):
        """Check if department reports to user's department."""
        user_dept = frappe.db.get_value("User", frappe.session.user, "department")
        parent_dept = frappe.db.get_value("Department", dept, "parent_department")
        return parent_dept == user_dept
    
    def get_employee_level(employee):
        """Get employee's level in organization hierarchy."""
        return frappe.db.get_value("Employee", employee, "grade_level") or 0
    
    return {
        "is_users_department": is_users_department,
        "is_subordinate_department": is_subordinate_department,
        "get_employee_level": get_employee_level,
    }

# In Workflow Transition conditions:
# Show transition only for user's department:
# is_users_department(doc.department)

# Require higher approval for senior employees:
# get_employee_level(doc.employee) >= 5
```

#### Example 5: Date and Time Calculations

```python
# my_app/workflow.py
def get_workflow_globals(current_globals):
    """Add date/time helper functions."""
    
    def is_weekend():
        """Check if today is weekend."""
        from datetime import datetime
        return datetime.now().weekday() >= 5
    
    def days_since_creation(doc):
        """Calculate days since document creation."""
        from frappe.utils import date_diff, nowdate
        return date_diff(nowdate(), doc.get("creation"))
    
    def is_month_end():
        """Check if today is last 3 days of month."""
        from datetime import datetime
        import calendar
        now = datetime.now()
        last_day = calendar.monthrange(now.year, now.month)[1]
        return now.day >= (last_day - 2)
    
    return {
        "is_weekend": is_weekend,
        "days_since_creation": days_since_creation,
        "is_month_end": is_month_end,
    }

# In Workflow Transition conditions:
# Escalate if pending for too long:
# days_since_creation(doc) > 7

# Different routing for month-end:
# is_month_end() and doc.affects_closing == 1
```

### Security Considerations

1. **Safe Evaluation**: All functions run in a safe evaluation context (safe_eval)
2. **Input Validation**: Validate inputs in your functions to prevent misuse
3. **No Destructive Operations**: Don't allow functions that modify data
4. **Limited Scope**: Only add what's needed for conditions, not general-purpose functions
5. **Performance**: Keep functions fast; they run during transition evaluation
6. **Error Handling**: Handle errors gracefully to avoid breaking workflows

### Best Practices

1. **Keep Functions Pure**: Functions should return consistent results for same inputs
2. **Cache Expensive Operations**: Use frappe.cache() for data that doesn't change often
3. **Document Your Functions**: Add clear docstrings explaining what each function does
4. **Test Thoroughly**: Test functions with various inputs and edge cases
5. **Avoid Side Effects**: Functions shouldn't modify documents or database
6. **Use Descriptive Names**: Make function names clear about what they check or return

### Testing

```python
# test_workflow.py
def test_workflow_globals():
    """Test custom workflow globals."""
    from my_app.workflow import get_workflow_globals
    
    # Get the globals
    current_globals = {}
    custom_globals = get_workflow_globals(current_globals)
    
    # Test approval limit function
    assert "get_approval_limit" in custom_globals
    limit = custom_globals["get_approval_limit"]("test@example.com")
    assert isinstance(limit, (int, float))
    
    # Test business hours function
    assert "is_business_hours" in custom_globals
    result = custom_globals["is_business_hours"]()
    assert isinstance(result, bool)
```

### Common Use Cases

1. **Amount-Based Routing**: Different approvers based on amounts
2. **Hierarchical Approvals**: Route based on org structure
3. **Time-Based Logic**: Different behavior for urgent/time-sensitive requests
4. **Stock/Inventory Checks**: Validate availability before approval
5. **Configuration-Driven**: Use settings to control transition logic
6. **Department/Region Routing**: Route to appropriate approvers
7. **Holiday/Calendar Checks**: Special handling for holidays
8. **Compliance Checks**: Ensure regulatory requirements are met

## Best Practices

### For before_transition

1. **Validate Early**: Check conditions before expensive operations
2. **Clear Error Messages**: Use descriptive error messages with frappe.throw()
3. **Keep it Fast**: Avoid slow operations that delay user experience
4. **Don't Modify State**: Avoid changing document state here (use after_transition)
5. **Use Transactions**: Wrap multiple DB operations in transactions if needed

### For after_transition

1. **Handle Errors Gracefully**: Use try-except for non-critical operations
2. **Update Efficiently**: Use db_update() for field updates instead of save()
3. **Background Jobs**: Use enqueue() for time-consuming tasks
4. **Clear Cache**: Clear relevant caches after updates
5. **Notify Users**: Send appropriate notifications

### For filter_workflow_transitions

1. **Return Quickly**: Keep logic fast to avoid UI delays
2. **Return None When Not Applicable**: Don't process irrelevant doctypes
3. **Preserve Original**: Don't modify the transitions list, create a new one
4. **Consider All Users**: Think about different user perspectives
5. **Document Logic**: Add comments explaining filtering rules

### For has_workflow_action_permission

1. **Default to True**: Return True for irrelevant cases
2. **Cache Lookups**: Cache frequently accessed data
3. **Optimize Queries**: Use efficient database queries
4. **Handle Missing Data**: Check for None values
5. **Log Decisions**: Log routing decisions for debugging

## Testing Workflow Hooks

```python
# test_workflow_hooks.py
import frappe
from frappe.tests.utils import FrappeTestCase

class TestWorkflowHooks(FrappeTestCase):
    def test_before_transition_validation(self):
        """Test before_transition prevents invalid transitions."""
        doc = frappe.get_doc({
            "doctype": "Purchase Order",
            "supplier": "Test Supplier",
            "items": []  # Empty items
        })
        doc.insert()
        
        # Should raise error due to empty items
        with self.assertRaises(frappe.ValidationError):
            from frappe.model.workflow import apply_workflow
            apply_workflow(doc, "Approve")
    
    def test_after_transition_creates_tasks(self):
        """Test after_transition creates follow-up tasks."""
        doc = self.create_test_project()
        apply_workflow(doc, "Approve")
        
        # Check tasks were created
        tasks = frappe.get_all("Task", filters={"project": doc.name})
        self.assertGreater(len(tasks), 0)
    
    def test_filter_transitions_by_amount(self):
        """Test transition filtering based on amount."""
        doc = self.create_test_po(amount=150000)
        transitions = get_transitions(doc)
        
        # High-value PO should only show CFO approval
        self.assertEqual(len(transitions), 1)
        self.assertEqual(transitions[0].allowed, "CFO")
```

## Debugging Workflow Hooks

```python
# Add logging to hooks
import frappe

def before_transition(self, transition):
    frappe.log_error(
        f"Before transition: {transition}",
        f"Workflow Debug - {self.name}"
    )
    # Your logic here

# Check hook execution
hooks_called = frappe.get_all(
    "Error Log",
    filters={"error": ["like", "%Workflow Debug%"]},
    order_by="creation desc",
    limit=10
)
```

## Common Issues

1. **Hook Not Called**: Check hook registration in hooks.py
2. **Infinite Loops**: Avoid triggering workflows from within hooks
3. **Permission Errors**: Don't bypass permissions in hooks
4. **Performance**: Cache frequently accessed data
5. **Transaction Issues**: Be careful with db commits in hooks
