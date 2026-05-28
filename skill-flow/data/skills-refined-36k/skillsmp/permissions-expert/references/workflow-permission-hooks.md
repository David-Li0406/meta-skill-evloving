# Workflow Permission Hooks

## Table of Contents

- [Overview](#overview)
- [Hook 1: filter_workflow_transitions](#hook-1-filter_workflow_transitions---custom-transition-filtering)
  - [Purpose](#purpose)
  - [Signature](#signature)
  - [Examples](#examples)
  - [Registration](#registration-in-hookspy)
- [Hook 2: has_workflow_action_permission](#hook-2-has_workflow_action_permission---action-level-permission)
  - [Purpose](#purpose-1)
  - [Signature](#signature-1)
  - [Examples](#examples-1)
  - [Registration](#registration-in-hookspy-1)
- [Comparison with Standard Permission Hooks](#comparison-with-standard-permission-hooks)
- [Integration with Standard Permissions](#integration-with-standard-permissions)
- [Best Practices](#best-practices)
- [Debugging](#debugging)
- [Common Patterns](#common-patterns)
- [Testing](#testing)

## Overview

Frappe provides two additional hooks specifically for controlling workflow-based permissions and transitions. These hooks extend the standard permission system to provide fine-grained control over workflow actions.

## Hook 1: `filter_workflow_transitions` - Custom Transition Filtering

### Purpose

Filter and customize the list of available workflow transitions for a document based on custom logic.

### Location

Registered in `hooks.py`

### Signature

```python
def filter_workflow_transitions(doc, transitions, workflow):
    """
    Filter workflow transitions based on custom logic.
    
    Args:
        doc: Document instance for which transitions are being fetched
        transitions: List of transition dictionaries that passed initial checks
        workflow: Workflow document instance
        
    Returns:
        list: Filtered list of transitions (or None to keep all)
    """
    pass
```

### When It's Called

This hook is called in `get_transitions()` after:
1. Role-based filtering (user has the allowed role)
2. Transition condition checks (if any conditions are satisfied)

But before returning the final list of available transitions to the user.

### Use Cases

- Hide specific transitions based on document field values
- Restrict transitions based on time/date conditions
- Apply complex business logic for transition availability
- Implement dynamic transition visibility based on external factors

### Example 1: Hide Transitions Based on Document Amount

```python
def filter_workflow_transitions(doc, transitions, workflow):
    """Hide 'Approve' transition if amount exceeds limit."""
    if doc.doctype == "Purchase Order":
        # Users cannot approve POs above 100,000
        if doc.total_amount > 100000:
            transitions = [t for t in transitions if t.get("action") != "Approve"]
    
    return transitions
```

### Example 2: Time-Based Transition Restrictions

```python
def filter_workflow_transitions(doc, transitions, workflow):
    """Restrict certain transitions to business hours."""
    from frappe.utils import now_datetime
    
    if doc.doctype == "Leave Application":
        current_hour = now_datetime().hour
        
        # Cannot approve leave applications outside business hours (9 AM - 5 PM)
        if current_hour < 9 or current_hour > 17:
            transitions = [t for t in transitions if t.get("action") != "Approve"]
    
    return transitions
```

### Example 3: Department-Based Filtering

```python
def filter_workflow_transitions(doc, transitions, workflow):
    """Filter transitions based on user's department."""
    if doc.doctype == "Expense Claim":
        user_dept = frappe.db.get_value("User", frappe.session.user, "department")
        doc_dept = doc.department
        
        # Only same department can reject
        if user_dept != doc_dept:
            transitions = [t for t in transitions if t.get("action") != "Reject"]
    
    return transitions
```

### Example 4: Sequential Approval Logic

```python
def filter_workflow_transitions(doc, transitions, workflow):
    """Enforce sequential approvals."""
    if doc.doctype == "Sales Order":
        # Must get sales approval before finance approval
        if not doc.sales_approved and doc.workflow_state == "Pending Finance Approval":
            # Hide all transitions - user must go back
            return []
    
    return transitions
```

### Registration in hooks.py

```python
filter_workflow_transitions = [
    "your_app.workflow.filter_transitions"
]
```

### Important Notes

1. **Return the filtered list**: Either return modified `transitions` list or `None` to keep all
2. **Don't modify transition objects**: Filter the list, don't change transition properties
3. **Multiple hooks**: If multiple hooks are registered, they're called sequentially
4. **Performance**: Keep logic fast as this is called frequently when showing workflow actions

## Hook 2: `has_workflow_action_permission` - Action-Level Permission

### Purpose

Control which users should receive workflow action notifications and have permission to execute specific workflow actions.

### Location

Registered in `hooks.py`

### Signature

```python
def has_workflow_action_permission(user, transition, doc):
    """
    Check if a user has permission to execute a workflow action.
    
    Args:
        user: User email to check permission for
        transition: Transition dictionary being checked
        doc: Document instance
        
    Returns:
        bool: True if user has permission, False otherwise
    """
    pass
```

### When It's Called

This hook is called in `get_users_next_action_data()` after:
1. Getting users with the required role
2. Checking `has_approval_access()` 
3. Checking standard document permissions

It filters the list of users who will:
- Receive workflow action notifications
- See the action in their Workflow Action list
- Be able to execute the transition

### Use Cases

- Restrict approvals to users in specific hierarchy
- Limit actions based on user properties (department, branch, etc.)
- Implement complex approval routing logic
- Dynamic approval assignment based on document values

### Example 1: Hierarchical Approval

```python
def has_workflow_action_permission(user, transition, doc):
    """Only allow approval from users senior to document creator."""
    if transition.get("action") == "Approve":
        # Get user levels
        user_level = frappe.db.get_value("User", user, "grade_level")
        creator_level = frappe.db.get_value("User", doc.owner, "grade_level")
        
        # User must be senior (higher level) than creator
        return user_level > creator_level
    
    return True  # Allow other actions
```

### Example 2: Department-Based Approval

```python
def has_workflow_action_permission(user, transition, doc):
    """Only allow approval from specific departments."""
    if doc.doctype == "Purchase Order" and transition.get("action") == "Approve":
        user_dept = frappe.db.get_value("User", user, "department")
        
        # Only Finance department can approve
        return user_dept == "Finance"
    
    return True
```

### Example 3: Amount-Based Approval Routing

```python
def has_workflow_action_permission(user, transition, doc):
    """Route approvals based on document amount."""
    if doc.doctype == "Sales Order" and transition.get("action") == "Approve":
        # Get user's approval limit
        approval_limit = frappe.db.get_value("User", user, "approval_limit")
        
        # User can only approve if document is within their limit
        return doc.total_amount <= approval_limit
    
    return True
```

### Example 4: Regional Approval

```python
def has_workflow_action_permission(user, transition, doc):
    """Restrict approvals to users from same region."""
    if transition.get("action") == "Approve":
        user_region = frappe.db.get_value("User", user, "region")
        doc_region = getattr(doc, "region", None)
        
        # Must be from same region
        if doc_region:
            return user_region == doc_region
    
    return True
```

### Example 5: Exclude Specific Users

```python
def has_workflow_action_permission(user, transition, doc):
    """Exclude certain users from workflow actions."""
    # Don't send to users on leave
    on_leave = frappe.db.get_value("User", user, "on_leave")
    if on_leave:
        return False
    
    # Don't allow self-approval even if allowed by transition
    if user == doc.owner and not transition.get("allow_self_approval"):
        return False
    
    return True
```

### Registration in hooks.py

```python
has_workflow_action_permission = [
    "your_app.workflow.check_workflow_permission"
]
```

### Important Notes

1. **Return boolean**: Must return `True` or `False`
2. **Called per user**: This hook is called for each potential user, so keep it efficient
3. **Multiple hooks**: If multiple hooks registered, ALL must return True for user to have permission
4. **Affects notifications**: Users filtered out won't receive workflow notifications
5. **Cache user data**: Cache frequently accessed user properties for performance

## Comparison with Standard Permission Hooks

| Aspect | Standard Permission Hooks | Workflow Permission Hooks |
|--------|--------------------------|---------------------------|
| Scope | All documents | Workflow-enabled documents only |
| Timing | Document access/save | Workflow transition time |
| Granularity | Document-level | Transition/Action-level |
| User notifications | Not affected | Directly affects who gets notified |
| Purpose | Access control | Workflow routing and approval logic |

## Integration with Standard Permissions

Workflow permission hooks work **in addition to** standard permissions:

1. User must have standard document permissions (read, write)
2. User must have the role specified in the workflow transition
3. Document must pass permission query conditions
4. Then workflow permission hooks are applied

All layers must pass for a user to execute a workflow action.

## Best Practices

### For filter_workflow_transitions

1. **Keep it fast**: This is called every time workflow actions are fetched
2. **Return filtered list**: Don't return None unless you want to keep all transitions
3. **Log reasoning**: Log why transitions were filtered for debugging
4. **Test thoroughly**: Ensure users can still complete workflows
5. **Document logic**: Clear comments on why transitions are filtered

### For has_workflow_action_permission

1. **Be restrictive**: Return False only when absolutely necessary
2. **Cache user data**: Avoid repeated DB queries for same user
3. **Consider edge cases**: Handle missing fields, None values gracefully
4. **Test notification flow**: Verify the right users receive notifications
5. **Performance**: This is called for each user in each transition

## Debugging

### Debug filter_workflow_transitions

```python
def filter_workflow_transitions(doc, transitions, workflow):
    """Debug transition filtering."""
    original_count = len(transitions)
    
    # Your filtering logic
    filtered_transitions = [t for t in transitions if your_condition(t)]
    
    # Log what was filtered
    if len(filtered_transitions) < original_count:
        removed = [t.get("action") for t in transitions if t not in filtered_transitions]
        frappe.log_error(
            f"Filtered out transitions: {removed} for {doc.doctype} {doc.name}",
            "Workflow Transition Filter"
        )
    
    return filtered_transitions
```

### Debug has_workflow_action_permission

```python
def has_workflow_action_permission(user, transition, doc):
    """Debug permission checks."""
    result = your_permission_check(user, transition, doc)
    
    if not result:
        frappe.log_error(
            f"Denied workflow action {transition.get('action')} "
            f"for user {user} on {doc.doctype} {doc.name}",
            "Workflow Permission Denied"
        )
    
    return result
```

## Common Patterns

### Pattern 1: Exclude Document Owner

```python
def has_workflow_action_permission(user, transition, doc):
    """Prevent self-approval."""
    return user != doc.owner
```

### Pattern 2: Approval Hierarchy

```python
def has_workflow_action_permission(user, transition, doc):
    """Only allow approvals from reporting manager."""
    if transition.get("action") == "Approve":
        reporting_manager = frappe.db.get_value("User", doc.owner, "reports_to")
        return user == reporting_manager
    return True
```

### Pattern 3: Conditional Transitions

```python
def filter_workflow_transitions(doc, transitions, workflow):
    """Show different transitions based on document status."""
    if doc.get("requires_special_approval"):
        # Remove quick approve, force normal approval flow
        transitions = [t for t in transitions if t.get("action") != "Quick Approve"]
    return transitions
```

## Testing

```python
def test_workflow_transition_filtering(self):
    """Test workflow transition filtering."""
    doc = create_test_document("Purchase Order", total_amount=150000)
    
    # Get transitions
    transitions = frappe.model.workflow.get_transitions(doc)
    
    # Should not have "Approve" for high value PO
    action_names = [t.get("action") for t in transitions]
    self.assertNotIn("Approve", action_names)
```

```python
def test_workflow_action_permission(self):
    """Test workflow action permission filtering."""
    doc = create_test_document("Sales Order")
    transition = frappe._dict({"action": "Approve", "allowed": "Sales Manager"})
    
    # Junior user should not have permission
    result = has_workflow_action_permission("junior@example.com", transition, doc)
    self.assertFalse(result)
    
    # Senior user should have permission
    result = has_workflow_action_permission("senior@example.com", transition, doc)
    self.assertTrue(result)
```

## See Also

- [has-permission-hook.md](has-permission-hook.md) - Standard document permissions
- [permission-query-conditions-hook.md](permission-query-conditions-hook.md) - List filtering
- Frappe Workflow Documentation
