# Best Practices for Frappe Hooks

Guidelines for writing maintainable, performant, and secure hooks.

## Design Principles

### 1. Single Responsibility

Each hook should do one thing well.

**Bad:**
```python
def on_update(doc, method=None):
    validate_data(doc)
    send_email(doc)
    sync_to_api(doc)
    update_dashboard(doc)
    log_changes(doc)
```

**Good:**
```python
doc_events = {
    "Sales Order": {
        "on_update": [
            "my_app.validations.validate_sales_order",
            "my_app.notifications.send_order_notification",
            "my_app.integrations.sync_order_to_api",
        ]
    }
}
```

### 2. Fail Fast

Validate early, throw exceptions for invalid states.

```python
def before_submit(doc, method=None):
    # Validate first
    if not doc.items:
        frappe.throw("Cannot submit without items")
    
    if doc.total_amount > get_credit_limit(doc.customer):
        frappe.throw("Exceeds credit limit")
    
    # Then process
    process_order(doc)
```

### 3. Idempotency

Design hooks to be safely re-runnable.

```python
def after_insert(doc, method=None):
    # Check if already processed
    if frappe.db.exists("Related Doc", {"reference": doc.name}):
        return  # Already created
    
    # Create related document
    create_related_doc(doc)
```

## Performance

### 1. Minimize Database Queries

**Bad:**
```python
def on_update(doc, method=None):
    for item in doc.items:
        # N+1 query problem
        rate = frappe.db.get_value("Item", item.item_code, "standard_rate")
        item.rate = rate
```

**Good:**
```python
def on_update(doc, method=None):
    # Single query
    item_codes = [item.item_code for item in doc.items]
    rates = dict(frappe.db.sql("""
        SELECT name, standard_rate
        FROM `tabItem`
        WHERE name IN %s
    """, [item_codes]))
    
    for item in doc.items:
        item.rate = rates.get(item.item_code, 0)
```

### 2. Use Caching

```python
def get_user_department(user):
    cache_key = f"user_dept:{user}"
    dept = frappe.cache().get_value(cache_key)
    
    if not dept:
        dept = frappe.db.get_value("User", user, "department")
        frappe.cache().set_value(cache_key, dept, expires_in_sec=3600)
    
    return dept
```

### 3. Conditional Execution

Skip unnecessary work:

```python
def on_update(doc, method=None):
    # Only process if status changed
    if not doc.has_value_changed("status"):
        return
    
    # Only for specific status
    if doc.status != "Approved":
        return
    
    process_approval(doc)
```

### 4. Async for Slow Operations

```python
def after_submit(doc, method=None):
    # Quick operations synchronously
    update_status(doc)
    
    # Slow operations asynchronously
    frappe.enqueue(
        "my_app.tasks.generate_report",
        doc=doc.name,
        queue="long"
    )
```

## Error Handling

### 1. Graceful Degradation

```python
def on_update(doc, method=None):
    try:
        # Critical operation
        update_inventory(doc)
    except Exception as e:
        # Critical: re-raise
        raise
    
    try:
        # Non-critical: log and continue
        sync_to_analytics(doc)
    except Exception as e:
        frappe.log_error(f"Analytics sync failed: {str(e)}")
```

### 2. Informative Errors

```python
def before_submit(doc, method=None):
    # Bad
    if not doc.customer:
        frappe.throw("Error")
    
    # Good
    if not doc.customer:
        frappe.throw(
            "Customer is required before submission",
            title="Missing Customer"
        )
```

### 3. Transaction Safety

```python
def after_insert(doc, method=None):
    try:
        # Database operations
        create_related_records(doc)
        frappe.db.commit()
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(str(e))
        raise
```

## Security

### 1. Permission Checks

```python
def on_update(doc, method=None):
    # Don't bypass permissions
    if not frappe.has_permission("Related DocType", "write"):
        return
    
    # Or use ignore_permissions carefully
    related_doc.save(ignore_permissions=True)  # Only if necessary
```

### 2. SQL Injection Prevention

```python
# Bad
def get_permission_query_conditions(user=None):
    return f"owner = '{user}'"  # SQL injection risk!

# Good
def get_permission_query_conditions(user=None):
    return f"owner = {frappe.db.escape(user)}"
```

### 3. Validate User Input

```python
def before_save(doc, method=None):
    # Validate and sanitize
    if doc.custom_field:
        doc.custom_field = frappe.utils.sanitize_html(doc.custom_field)
```

## Code Organization

### 1. Separate Concerns

```
my_app/
├── hooks.py
├── validations/
│   ├── sales_order.py
│   └── customer.py
├── notifications/
│   ├── email.py
│   └── push.py
└── integrations/
    ├── api_sync.py
    └── webhook.py
```

### 2. Reusable Functions

```python
# utils.py
def send_notification(recipient, subject, message):
    """Reusable notification function"""
    frappe.sendmail(
        recipients=recipient,
        subject=subject,
        message=message
    )

# hooks implementation
def after_submit(doc, method=None):
    send_notification(
        doc.owner,
        f"{doc.doctype} Submitted",
        f"Your {doc.doctype} {doc.name} has been submitted"
    )
```

### 3. Configuration Over Code

```python
# Instead of hardcoding
def on_update(doc, method=None):
    if doc.status == "Approved":
        send_email("manager@example.com", ...)

# Use settings
def on_update(doc, method=None):
    if doc.status == "Approved":
        recipients = frappe.db.get_single_value(
            "Notification Settings",
            "approval_recipients"
        )
        send_email(recipients, ...)
```

## Testing

### 1. Unit Tests

```python
def test_sales_order_validation():
    so = frappe.get_doc({
        "doctype": "Sales Order",
        "customer": "Test Customer"
    })
    
    # Should fail without items
    with pytest.raises(frappe.ValidationError):
        so.insert()
```

### 2. Integration Tests

```python
def test_order_workflow():
    # Create order
    so = create_test_sales_order()
    
    # Submit triggers hooks
    so.submit()
    
    # Verify hook effects
    assert frappe.db.exists("Delivery Note", {"sales_order": so.name})
```

### 3. Mock External Services

```python
from unittest.mock import patch

def test_api_sync():
    with patch('my_app.integrations.api_call') as mock_api:
        mock_api.return_value = {"success": True}
        
        doc = create_test_doc()
        doc.save()  # Triggers hook
        
        mock_api.assert_called_once()
```

## Documentation

### 1. Document Hook Purpose

```python
def before_submit(doc, method=None):
    """
    Validate sales order before submission.
    
    Checks:
    - Items exist
    - Credit limit not exceeded
    - Required approvals obtained
    
    Raises:
        ValidationError: If validation fails
    """
```

### 2. Document Dependencies

```python
doc_events = {
    "Sales Order": {
        "after_submit": [
            # Must run in this order:
            "my_app.inventory.reserve_stock",      # 1. Reserve first
            "my_app.sales.create_delivery_note",   # 2. Then create DN
            "my_app.accounting.create_gl_entry",   # 3. Finally accounting
        ]
    }
}
```

### 3. Configuration Notes

```python
# hooks.py

# Sync to external CRM every hour
# Requires: CRM API credentials in Site Config
# See: my_app/docs/crm_setup.md
scheduler_events = {
    "hourly": [
        "my_app.integrations.sync_to_crm"
    ]
}
```

## Common Pitfalls

### 1. Infinite Loops

**Problem:**
```python
def on_update(doc, method=None):
    doc.custom_field = calculate_value()
    doc.save()  # Triggers on_update again!
```

**Solution:**
```python
def on_update(doc, method=None):
    if doc.has_value_changed("trigger_field"):
        doc.db_set("custom_field", calculate_value(), update_modified=False)
```

### 2. Modifying Uncommitted Data

**Problem:**
```python
def after_insert(doc, method=None):
    # Doc not yet committed!
    child_doc = frappe.get_doc({
        "doctype": "Child",
        "parent_ref": doc.name  # Might fail in other process
    })
    child_doc.insert()
```

**Solution:**
```python
def after_insert(doc, method=None):
    frappe.enqueue(
        create_child_doc,
        doc_name=doc.name,
        queue="short"
    )
```

### 3. Ignoring Hook Errors

**Problem:**
```python
def on_update(doc, method=None):
    try:
        important_operation()
    except:
        pass  # Silently fails
```

**Solution:**
```python
def on_update(doc, method=None):
    try:
        important_operation()
    except Exception as e:
        frappe.log_error(
            title=f"Failed: {doc.doctype} {doc.name}",
            message=str(e)
        )
        # Re-raise if critical
        if is_critical():
            raise
```

## Checklist

Before deploying hooks:

- [ ] Tested with different user roles
- [ ] Handled edge cases
- [ ] Added error handling
- [ ] Optimized database queries
- [ ] Documented purpose and dependencies
- [ ] Checked for infinite loops
- [ ] Verified transaction safety
- [ ] Added appropriate logging
- [ ] Considered performance impact
- [ ] Reviewed security implications
