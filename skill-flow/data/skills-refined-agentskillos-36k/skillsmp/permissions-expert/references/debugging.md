# Debugging Frappe Permissions

## Table of Contents

- [Enable Debug Mode](#enable-debug-mode)
- [Check Permission Debug Logs](#check-permission-debug-logs)
- [Test Permissions as Different User](#test-permissions-as-different-user)
- [Inspect Role Permissions](#inspect-role-permissions)
- [Check Permission Query Conditions](#check-permission-query-conditions)
- [Check User Permissions](#check-user-permissions)
- [Check Document Permissions](#check-document-permissions)
- [Check Share Permissions](#check-share-permissions)
- [Verify Hook Registration](#verify-hook-registration)
- [Check for Server Scripts](#check-for-server-scripts)
- [Common Debug Scenarios](#common-debug-scenarios)
- [Logging and Monitoring](#logging-and-monitoring)
- [Bench Commands for Debugging](#bench-commands-for-debugging)
- [Browser Developer Tools](#browser-developer-tools)
- [Advanced Debugging](#advanced-debugging)
- [Debugging Checklist](#debugging-checklist)
- [Tips](#tips)

## Enable Debug Mode

### Method 1: Per-Check Debug

```python
# In Python
result = frappe.has_permission("DocType", "read", doc, debug=True)
# Logs will show the permission evaluation flow
```

### Method 2: Global Developer Mode

```python
# In site_config.json or common_site_config.json
{
    "developer_mode": 1
}

# Or via command line
bench set-config developer_mode 1
```

### Method 3: Debug Flag

```python
frappe.conf.developer_mode = 1
```

## Check Permission Debug Logs

```python
# After permission check with debug=True
logs = frappe.local.permission_debug_log
for log in logs:
    print(log)

# Or use _pop_debug_log to get and clear logs
logs = frappe.permissions._pop_debug_log()
```

## Test Permissions as Different User

```python
# Temporarily switch user
original_user = frappe.session.user
frappe.set_user("test@example.com")
try:
    has_perm = frappe.has_permission("Sales Order", "read", doc)
    print(f"Has permission: {has_perm}")
finally:
    frappe.set_user(original_user)
```

## Inspect Role Permissions

```python
# Get role permissions for a doctype
from frappe.permissions import get_role_permissions

perms = get_role_permissions("Sales Order", user="test@example.com")
print(perms)  # {"read": 1, "write": 0, ...}

# Check specific user's roles
roles = frappe.get_roles("test@example.com")
print(f"User roles: {roles}")
```

## Check Permission Query Conditions

```python
# See what SQL conditions are applied
from frappe.model.db_query import DatabaseQuery

query = DatabaseQuery("Sales Order", user="test@example.com")
conditions = query.get_permission_query_conditions()
print(f"SQL conditions: {conditions}")

# Test if specific document passes conditions
from frappe.permissions import check_permission_query_conditions_for_doc

doc = frappe.get_doc("Sales Order", "SO-0001")
passes = check_permission_query_conditions_for_doc(doc, user="test@example.com", debug=True)
print(f"Document passes conditions: {passes}")
```

## Check User Permissions

```python
# Debug: Check user permissions
from frappe.permissions import get_user_permissions

user_perms = get_user_permissions("user@example.com")
print(f"User permissions: {user_perms}")

# Example output:
# {
#     "Company": [
#         {"doc": "Company A", "applicable_for": None, "is_default": 1}
#     ],
#     "Territory": [
#         {"doc": "North", "applicable_for": "Sales Order", "is_default": 0}
#     ]
# }
```

## Check Document Permissions

```python
# Debug: Check document permissions
from frappe.permissions import get_doc_permissions

doc = frappe.get_doc("Sales Order", "SO-0001")
perms = get_doc_permissions(doc, user="user@example.com", debug=True)
print(f"Document permissions: {perms}")

# Example output:
# {"read": 1, "write": 0, "delete": 0, "submit": 1, ...}
```

## Check Share Permissions

```python
# Check if document is shared
shares = frappe.get_all("DocShare", filters={
    "share_doctype": "Sales Order",
    "share_name": "SO-0001",
    "user": "user@example.com"
}, fields=["read", "write", "share", "submit"])

print(f"Shares: {shares}")

# Check if sharing is enabled
sharing_enabled = not frappe.get_system_settings("disable_document_sharing")
print(f"Sharing enabled: {sharing_enabled}")
```

## Verify Hook Registration

```python
# Check if hooks are registered
hooks = frappe.get_hooks("permission_query_conditions")
print(f"Registered permission_query_conditions hooks: {hooks}")

hooks = frappe.get_hooks("has_permission")
print(f"Registered has_permission hooks: {hooks}")

# Test hook directly
from your_app.your_module.your_doctype import get_permission_query_conditions
condition = get_permission_query_conditions(user="user@example.com")
print(f"Returned condition: {condition}")
```

## Check for Server Scripts

```python
# Check if Server Script exists for permission query
from frappe.core.doctype.server_script.server_script_utils import get_server_script_map

script_map = get_server_script_map()
permission_scripts = script_map.get("permission_query", {})
print(f"Permission query scripts: {permission_scripts}")

# Get specific script
if doctype_script := permission_scripts.get("Your DocType"):
    script = frappe.get_doc("Server Script", doctype_script)
    print(f"Script: {script.script}")
```

## Common Debug Scenarios

### Scenario 1: User Can't See Documents in List View

```python
# Step 1: Check role permissions
from frappe.permissions import get_role_permissions
perms = get_role_permissions("Sales Order", user="user@example.com")
print(f"Role permissions: {perms}")

# Step 2: Check permission query conditions
from frappe.model.db_query import DatabaseQuery
query = DatabaseQuery("Sales Order", user="user@example.com")
conditions = query.get_permission_query_conditions()
print(f"Applied conditions: {conditions}")

# Step 3: Check user permissions
from frappe.permissions import get_user_permissions
user_perms = get_user_permissions("user@example.com")
print(f"User permissions: {user_perms}")

# Step 4: Test actual query
docs = frappe.get_all("Sales Order", filters={}, as_list=True)
print(f"Found {len(docs)} documents")
```

### Scenario 2: Can See in List but Can't Open Document

```python
# Check document permissions
doc = frappe.get_doc("Sales Order", "SO-0001")
perms = get_doc_permissions(doc, user="user@example.com", debug=True)
print(f"Document permissions: {perms}")

# Check has_permission with debug
result = frappe.has_permission("Sales Order", "read", doc,
                                user="user@example.com", debug=True)
print(f"Has permission: {result}")

# Check debug logs
logs = frappe.permissions._pop_debug_log()
for log in logs:
    print(log)
```

### Scenario 3: Permission Query Hook Not Working

```python
# Step 1: Verify hook registration
hooks = frappe.get_hooks("permission_query_conditions")
print(f"Registered hooks: {hooks}")

# Step 2: Test hook directly
from your_app.your_module.your_doctype import get_permission_query_conditions
condition = get_permission_query_conditions(user="user@example.com")
print(f"Returned condition: {condition}")

# Step 3: Clear cache
frappe.clear_cache()

# Step 4: Reload doctypes
frappe.reload_doctype("Your DocType")
```

### Scenario 4: Write Operations Fail Silently

```python
# Check write permission conditions
from frappe.permissions import check_write_permission_query_conditions

doc = frappe.get_doc("Sales Order", "SO-0001")
can_write = check_write_permission_query_conditions(doc, ptype="write",
                                                     user="user@example.com")
print(f"Can write: {can_write}")

# Enable SQL logging
frappe.db.set_debug_log()
# Perform operation
# Check SQL log
sql_log = frappe.db.get_debug_log()
```

## Logging and Monitoring

### Enable Permission Logging

```python
# Add to hooks.py
doc_events = {
    "*": {
        "on_update": "your_app.permissions.log_permission_check"
    }
}

# In your_app/permissions.py
def log_permission_check(doc, method):
    if frappe.session.user != "Administrator":
        frappe.log_error(
            f"User {frappe.session.user} updated {doc.doctype} {doc.name}",
            "Permission Check"
        )
```

### Monitor Permission Failures

```python
# Track failed permission checks
def track_permission_failure(doctype, ptype, doc, user):
    frappe.log_error(
        f"Permission denied: {user} tried {ptype} on {doctype} {doc}",
        "Permission Failure"
    )
```

## Bench Commands for Debugging

```bash
# Check user permissions
bench console
>>> frappe.get_user_permissions("user@example.com")

# Clear cache
bench clear-cache

# Rebuild
bench --site site_name rebuild

# Check installed apps and hooks
bench --site site_name list-hooks
```

## Browser Developer Tools

### Check Network Requests

1. Open Browser Developer Tools (F12)
2. Go to Network tab
3. Try to access the document
4. Look for failed API calls
5. Check response for permission errors

### Check Console Logs

```javascript
// In browser console
frappe.call({
    method: 'frappe.has_permission',
    args: {
        doctype: 'Sales Order',
        ptype: 'read',
        doc: 'SO-0001'
    },
    callback: function(r) {
        console.log('Has permission:', r.message);
    }
});
```

## Advanced Debugging

### SQL Query Debugging

```python
# Enable SQL debug
frappe.db.debug = 1

# Run operation
docs = frappe.get_all("Sales Order")

# Check executed queries
for query in frappe.db.sql_list:
    print(query)

# Disable debug
frappe.db.debug = 0
```

### Profile Permission Checks

```python
import cProfile
import pstats

# Profile permission check
profiler = cProfile.Profile()
profiler.enable()

frappe.has_permission("Sales Order", "read", doc)

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 time-consuming calls
```

## Debugging Checklist

- [ ] Debug mode enabled
- [ ] Checked role permissions
- [ ] Checked user permissions
- [ ] Checked permission query conditions
- [ ] Checked share permissions
- [ ] Verified hook registration
- [ ] Tested with different users
- [ ] Checked debug logs
- [ ] Cleared cache
- [ ] Checked for server scripts
- [ ] Verified SQL conditions
- [ ] Checked document status/workflow
- [ ] Tested in fresh browser session (no cache)

## Common Debug Outputs

### Successful Permission Check

```
Debug log:
- Allowed everything because user is Administrator
OR
- User has following roles: ['Sales User', 'Employee']
- User has following permissions using role permission system: {"read": 1, "write": 1}
- Document passes permission query conditions
```

### Failed Permission Check

```
Debug log:
- User has following roles: ['Sales User']
- User has following permissions using role permission system: {"read": 1, "write": 0}
- Permission check failed from role permission system
- User user@example.com does not have access to this document
```

## Tips

1. **Start broad, narrow down**: Check role permissions first, then user permissions, then query conditions
2. **Test as different users**: Switch between users to see different permission views
3. **Clear cache often**: Permissions are cached, clear after making changes
4. **Use debug=True**: Provides detailed logs of permission evaluation
5. **Check server scripts**: Often forgotten source of permission logic
6. **Verify hook paths**: Typos in hooks.py can break permissions silently
