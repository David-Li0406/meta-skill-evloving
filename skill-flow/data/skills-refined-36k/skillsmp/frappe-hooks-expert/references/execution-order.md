# Hook Execution Order

Understanding the order in which hooks execute is crucial for predictable behavior.

## Document Lifecycle Execution Order

### Insert Flow

1. `doc.validate()` (controller method)
2. **before_insert** hook
3. Database INSERT
4. `doc.after_insert()` (controller method)
5. **after_insert** hook
6. `doc.on_update()` (controller method)
7. **on_update** hook
8. **on_change** hook (if fields changed)

### Update Flow

1. `doc.validate()` (controller method)
2. **before_save** hook
3. Database UPDATE
4. `doc.after_save()` (controller method)
5. **after_save** hook
6. `doc.on_update()` (controller method)
7. **on_update** hook
8. **on_change** hook (if fields changed)

### Submit Flow

1. `doc.validate()` (controller method)
2. **before_submit** hook
3. Set `docstatus = 1`
4. Database UPDATE
5. `doc.after_submit()` (controller method)
6. **after_submit** hook
7. `doc.on_update()` (controller method)
8. **on_update** hook

### Cancel Flow

1. **before_cancel** hook
2. Set `docstatus = 2`
3. Database UPDATE
4. `doc.after_cancel()` (controller method)
5. **after_cancel** hook
6. **on_cancel** hook

### Update After Submit Flow

1. `doc.validate()` (controller method)
2. **before_update_after_submit** hook
3. Database UPDATE
4. **after_update_after_submit** hook
5. `doc.on_update()` (controller method)
6. **on_update** hook

### Delete Flow

1. `doc.before_trash()` (controller method)
2. **on_trash** hook
3. Database DELETE
4. **after_delete** hook

### Rename Flow

1. **before_rename** hook
2. Database updates (rename + update references)
3. **after_rename** hook

## Permission Evaluation Order

When checking document access:

1. **Administrator check** - Bypass all if Administrator
2. **Role permissions** - Check DocType role permissions
3. **has_permission hook** - Custom document permission logic
4. **permission_query_conditions hook** - SQL filter validation
5. **User permissions** - Document-level user restrictions
6. **Share permissions** - Explicit shares

For writes, additionally:

7. **write_permission_query_conditions hook** - Post-write validation

## Request Lifecycle Order

HTTP request flow:

1. **before_request** hooks (in order of registration)
2. Route matching and handler execution
3. **after_request** hooks (in order of registration)
4. Response sent to client

## Background Job Order

Job execution flow:

1. **before_job** hooks
2. Job function execution
3. **after_job** hooks

## App Installation Order

Multi-app installation:

1. For each app in dependency order:
   - **before_install** hook
   - Database migrations
   - Fixtures import
   - **after_install** hook

2. For each other app:
   - **after_app_install** hook (with new app name)

## Migration Order

During `bench migrate`:

1. **before_migrate** hooks (all apps)
2. For each app:
   - Execute patches in order
   - Update DocTypes
   - Import fixtures
3. **after_migrate** hooks (all apps)

## Multiple Hook Registration

When multiple functions registered for same hook:

### Within Same App

Execute in list order:
```python
doc_events = {
    "Task": {
        "on_update": [
            "my_app.tasks.first_function",   # Runs first
            "my_app.tasks.second_function",  # Runs second
        ]
    }
}
```

### Across Multiple Apps

Execute in app installation order (as listed in `apps.txt`):

1. frappe
2. erpnext
3. custom_app_1
4. custom_app_2

If all apps have `on_update` hook for Task:
```
frappe's hook → erpnext's hook → custom_app_1's hook → custom_app_2's hook
```

## Controller vs Hook Order

Controller methods run before hooks:

**Example: Save operation**
1. `doc.validate()` - Controller
2. `doc.before_save()` - Controller
3. **before_save** - Hook
4. Database UPDATE
5. `doc.after_save()` - Controller
6. **after_save** - Hook
7. `doc.on_update()` - Controller
8. **on_update** - Hook

## Scheduler Event Order

Multiple scheduler types running simultaneously:

- `all` events run every ~3 minutes (most frequent)
- `cron` events run at specified times
- `hourly` events run ~hourly
- `daily` events run once per day
- etc.

Within same event type, functions execute in registration order.

## Session Event Order

Login flow:

1. Authentication validation
2. **auth_hooks** (if registered)
3. Session creation
4. **on_session_creation** hooks
5. **on_login** hooks
6. Redirect to desk

Logout flow:

1. **on_logout** hooks
2. Session destruction
3. Redirect to login

## Important Considerations

### Stop Execution

- Throwing exception stops further execution
- Later hooks won't run
- Transaction rolled back (for database operations)

```python
def before_save(doc, method=None):
    if invalid_condition:
        frappe.throw("Error")  # Stops here, after_save won't run
```

### Hook Dependencies

If Hook B depends on Hook A's changes:

```python
# Ensure correct order
doc_events = {
    "DocType": {
        "on_update": [
            "app.module.hook_a",  # Must run first
            "app.module.hook_b",  # Depends on A
        ]
    }
}
```

### Commit Timing

Database commits happen after all hooks:

```python
def on_update(doc, method=None):
    # Changes not yet committed
    # Other processes won't see changes yet
    pass

# After all hooks complete → commit
```

### Async Considerations

- Most hooks run synchronously
- Scheduler hooks run in background
- Use `frappe.enqueue` for async tasks in hooks

## Testing Hook Order

```python
def test_hook_order():
    # Track execution
    execution_log = []
    
    def hook_a(doc, method=None):
        execution_log.append("A")
    
    def hook_b(doc, method=None):
        execution_log.append("B")
    
    # After test
    assert execution_log == ["A", "B"]
```

## Best Practices

1. **Document Dependencies**: Comment which hooks must run first
2. **Independent Hooks**: Design hooks to work independently when possible
3. **Explicit Order**: List dependent hooks in correct order
4. **Test Order**: Verify execution order in tests
5. **Avoid Assumptions**: Don't assume hook order across apps

## Common Patterns

### Pre and Post Processing

```python
doc_events = {
    "Order": {
        "before_submit": "validate_inventory",  # Check first
        "after_submit": "reserve_inventory",    # Then reserve
    }
}
```

### Cascading Updates

```python
doc_events = {
    "Sales Order": {
        "on_update": [
            "update_customer_totals",     # Update customer
            "update_territory_stats",     # Then territory
            "sync_to_analytics",          # Finally analytics
        ]
    }
}
```

### Cleanup Order

```python
doc_events = {
    "Project": {
        "on_trash": [
            "delete_tasks",           # Delete children first
            "delete_timesheets",      # Then related docs
            "cleanup_files",          # Finally files
        ]
    }
}
```
