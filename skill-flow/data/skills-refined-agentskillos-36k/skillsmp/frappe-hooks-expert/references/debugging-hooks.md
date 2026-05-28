# Debugging Frappe Hooks

Guide for troubleshooting and testing hooks.

## Common Issues

### 1. Hook Not Firing

**Symptoms:**
- Hook function never executes
- Expected behavior doesn't occur

**Troubleshooting:**

Check hooks.py syntax:
```python
# Wrong - string instead of list
doc_events = {
    "Task": {
        "on_update": "my_app.tasks.on_update"  # Correct for single hook
    }
}

# Wrong - missing quotes
doc_events = {
    "Task": {
        "on_update": [
            my_app.tasks.on_update  # Should be string!
        ]
    }
}
```

Verify function path:
```bash
# In bench console
bench console

# Test import
from my_app.tasks import on_update
# If this fails, path is wrong
```

Check for errors:
```bash
# View error logs
tail -f logs/bench.log

# Or in Frappe
frappe.get_all("Error Log", limit=10, order_by="creation desc")
```

Restart bench:
```bash
bench restart
# Changes to hooks.py require restart
```

### 2. Hook Runs Multiple Times

**Causes:**
- Duplicate registration
- Recursive saves
- Multiple apps with same hook

**Debug:**
```python
def on_update(doc, method=None):
    import traceback
    frappe.logger().debug(f"Stack: {traceback.format_stack()}")
```

**Fix recursive saves:**
```python
# Bad - triggers on_update again
def on_update(doc, method=None):
    doc.custom_field = "value"
    doc.save()  # Recursion!

# Good - direct DB update
def on_update(doc, method=None):
    doc.db_set("custom_field", "value", update_modified=False)
```

### 3. Hook Errors Breaking Operations

**Symptoms:**
- Document save/submit fails
- No clear error message

**Debug with try-except:**
```python
def on_update(doc, method=None):
    try:
        your_logic()
    except Exception as e:
        frappe.log_error(
            title=f"Hook Error: {doc.doctype}",
            message=frappe.get_traceback()
        )
        raise  # Re-raise to see in UI
```

### 4. Permission Hook Not Working

**Debug permission checks:**
```python
# Enable debug mode
result = frappe.has_permission(
    "DocType",
    "read",
    doc,
    debug=True  # Shows evaluation steps
)

# Check logs
logs = frappe.local.permission_debug_log
for log in logs:
    print(log)
```

**Common issues:**
- Returning wrong type (must be bool or None)
- SQL syntax error in query conditions
- Forgetting to escape values

### 5. Scheduler Tasks Not Running

**Check scheduler status:**
```bash
bench --site mysite scheduler status

# If disabled
bench --site mysite scheduler enable
```

**Check scheduler logs:**
```bash
tail -f logs/scheduler.log
```

**Test manually:**
```python
# In bench console
from my_app.tasks import my_scheduled_task
my_scheduled_task()
```

## Debugging Techniques

### 1. Logging

**Basic logging:**
```python
def on_update(doc, method=None):
    frappe.logger().info(f"Processing {doc.name}")
    frappe.logger().debug(f"Status: {doc.status}")
```

**Detailed logging:**
```python
def on_update(doc, method=None):
    import json
    frappe.logger().debug(f"Doc data: {json.dumps(doc.as_dict(), default=str)}")
```

**Custom log file:**
```python
import logging

logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)

def on_update(doc, method=None):
    logger.debug(f"Custom log: {doc.name}")
```

### 2. Print Debugging

**In hooks:**
```python
def on_update(doc, method=None):
    print(f"DEBUG: {doc.name} - {doc.status}")
    # Output appears in bench logs
```

**View in console:**
```bash
bench --site mysite console

# Or watch logs
tail -f logs/bench.log | grep DEBUG
```

### 3. Breakpoint Debugging

**Using pdb:**
```python
def on_update(doc, method=None):
    import pdb; pdb.set_trace()  # Debugger stops here
    process_doc(doc)
```

**Using ipdb (better):**
```bash
pip install ipdb
```

```python
def on_update(doc, method=None):
    import ipdb; ipdb.set_trace()
```

### 4. Stack Traces

**Get full traceback:**
```python
def on_update(doc, method=None):
    import traceback
    try:
        risky_operation()
    except Exception:
        frappe.log_error(
            title="Hook Failed",
            message=traceback.format_exc()
        )
```

### 5. Timing Analysis

**Measure execution time:**
```python
import time

def on_update(doc, method=None):
    start = time.time()
    
    your_logic()
    
    duration = time.time() - start
    if duration > 1.0:  # Log slow operations
        frappe.logger().warning(f"Slow hook: {duration}s")
```

**Profile performance:**
```python
import cProfile
import pstats
from io import StringIO

def on_update(doc, method=None):
    pr = cProfile.Profile()
    pr.enable()
    
    your_logic()
    
    pr.disable()
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    print(s.getvalue())
```

## Testing Hooks

### 1. Manual Testing

**In bench console:**
```python
bench --site mysite console

# Create test document
doc = frappe.get_doc({
    "doctype": "Sales Order",
    "customer": "Test Customer",
    "items": [{"item_code": "Test Item", "qty": 1}]
})

# Insert triggers hooks
doc.insert()

# Update triggers hooks
doc.status = "Confirmed"
doc.save()

# Submit triggers hooks
doc.submit()
```

### 2. Unit Tests

```python
# tests/test_hooks.py
import frappe
import unittest

class TestSalesOrderHooks(unittest.TestCase):
    def setUp(self):
        # Create test data
        self.customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": "Test Customer"
        }).insert()
    
    def tearDown(self):
        # Cleanup
        frappe.db.rollback()
    
    def test_on_update_hook(self):
        """Test that on_update hook executes"""
        so = frappe.get_doc({
            "doctype": "Sales Order",
            "customer": self.customer.name
        })
        so.insert()
        
        # Modify and save (triggers on_update)
        so.status = "Confirmed"
        so.save()
        
        # Verify hook effects
        self.assertEqual(so.custom_field, "expected_value")
    
    def test_before_submit_validation(self):
        """Test before_submit validation"""
        so = frappe.get_doc({
            "doctype": "Sales Order",
            "customer": self.customer.name
        })
        so.insert()
        
        # Should fail validation
        with self.assertRaises(frappe.ValidationError):
            so.submit()
```

**Run tests:**
```bash
bench --site mysite run-tests --module my_app.tests.test_hooks
```

### 3. Integration Tests

```python
def test_order_workflow():
    """Test complete workflow with hooks"""
    # Create order
    so = create_test_sales_order()
    
    # Submit (triggers multiple hooks)
    so.submit()
    
    # Verify workflow effects
    assert frappe.db.exists("Delivery Note", {"sales_order": so.name})
    assert frappe.db.exists("Journal Entry", {"reference_name": so.name})
    
    # Cancel (triggers cancel hooks)
    so.cancel()
    
    # Verify cleanup
    assert not frappe.db.exists("Delivery Note", {"sales_order": so.name})
```

### 4. Mock External Services

```python
from unittest.mock import patch, MagicMock

def test_api_integration_hook():
    """Test hook with external API call"""
    with patch('my_app.integrations.api_client') as mock_api:
        # Setup mock
        mock_api.sync_order.return_value = {"status": "success"}
        
        # Trigger hook
        so = create_test_sales_order()
        so.submit()
        
        # Verify API called
        mock_api.sync_order.assert_called_once_with(so.name)
```

## Debugging Tools

### 1. Error Log Viewer

```python
# View recent errors
errors = frappe.get_all("Error Log",
    fields=["*"],
    filters={"error": ["like", "%hook%"]},
    order_by="creation desc",
    limit=10
)

for err in errors:
    print(f"{err.creation}: {err.error}")
```

### 2. SQL Query Log

**Enable query debugging:**
```python
frappe.conf.allow_tests = True
frappe.flags.in_test = True

# Queries will be logged
```

**Or manually:**
```python
queries = []

old_sql = frappe.db.sql
def logged_sql(*args, **kwargs):
    queries.append(args[0])
    return old_sql(*args, **kwargs)

frappe.db.sql = logged_sql

# Run your code
your_function()

# View queries
for q in queries:
    print(q)
```

### 3. Check Hook Registration

```python
# View all registered hooks
hooks = frappe.get_hooks()

# View specific hook
doc_events = frappe.get_hooks("doc_events")
print(doc_events.get("Sales Order", {}))

# View permission hooks
perm_hooks = frappe.get_hooks("permission_query_conditions")
print(perm_hooks)
```

### 4. Verify Function Exists

```python
# Check if hook function can be imported
from frappe import get_attr

try:
    func = get_attr("my_app.tasks.on_update")
    print(f"Function found: {func}")
except Exception as e:
    print(f"Error: {e}")
```

## Performance Debugging

### 1. Identify Slow Hooks

```python
# Add timing to all hooks
import functools
import time

def time_hook(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        
        if duration > 0.5:  # Log slow hooks
            frappe.logger().warning(
                f"Slow hook: {func.__name__} took {duration:.2f}s"
            )
        
        return result
    return wrapper

# Use decorator
@time_hook
def on_update(doc, method=None):
    your_logic()
```

### 2. Database Query Analysis

```python
# Count queries
query_count = len(frappe.db._cursor.queries)

your_function()

new_count = len(frappe.db._cursor.queries)
print(f"Queries executed: {new_count - query_count}")
```

## Best Practices

1. **Add Logging Early**: Add debug logs before deploying
2. **Test Thoroughly**: Write tests for all hooks
3. **Handle Errors**: Always use try-except in hooks
4. **Monitor Production**: Set up error notifications
5. **Document**: Add comments explaining hook purpose
6. **Version Control**: Track hook changes in git

## Quick Debug Checklist

When hook isn't working:

- [ ] Function path correct in hooks.py?
- [ ] Function import works in console?
- [ ] Bench restarted after hooks.py change?
- [ ] Any errors in logs?
- [ ] Hook actually being called? (add print)
- [ ] Correct function signature?
- [ ] Returns correct type (for permission hooks)?
- [ ] SQL syntax correct (for query hooks)?
- [ ] Transaction committed?
- [ ] Permissions sufficient?
