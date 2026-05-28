# Common Issues and Solutions

## Table of Contents

- [Issue 1: User Can't See Documents in List View](#issue-1-user-cant-see-documents-in-list-view)
- [Issue 2: Can See Document in List but Can't Open](#issue-2-can-see-document-in-list-but-cant-open)
- [Issue 3: Permission Query Hook Not Working](#issue-3-permission-query-hook-not-working)
- [Issue 4: Write Operations Fail Silently](#issue-4-write-operations-fail-silently)
- [Issue 5: Virtual DocType Permission Issues](#issue-5-virtual-doctype-permission-issues)
- [Issue 6: Share Permissions Not Working](#issue-6-share-permissions-not-working)
- [Issue 7: Administrator Not Seeing All Documents](#issue-7-administrator-not-seeing-all-documents)
- [Issue 8: User Sees Too Many Documents](#issue-8-user-sees-too-many-documents)
- [Issue 9: Permission Changes Don't Take Effect](#issue-9-permission-changes-dont-take-effect)
- [Issue 10: Child Table Fields Not Visible](#issue-10-child-table-fields-not-visible)
- [Issue 11: Slow List Views](#issue-11-slow-list-views)
- [Issue 12: PermissionError in API Calls](#issue-12-frappeexceptionspermissionerror-in-api-calls)
- [Troubleshooting Workflow](#troubleshooting-workflow)

## Issue 1: User Can't See Documents in List View

**Symptoms:** User has role permission but list view is empty or missing documents

**Possible Causes:**
1. Permission query conditions are too restrictive
2. User permissions are blocking access
3. Share-only access (user can only see explicitly shared documents)

**Solutions:**

```python
# Debug: Check what conditions are being applied
from frappe.model.db_query import DatabaseQuery
query = DatabaseQuery("Your DocType", user="user@example.com")
conditions = query.get_permission_query_conditions()
print(f"Applied conditions: {conditions}")

# Debug: Check user permissions
from frappe.permissions import get_user_permissions
user_perms = get_user_permissions("user@example.com")
print(f"User permissions: {user_perms}")

# Fix: Review and adjust permission_query_conditions hook
# Fix: Clear unnecessary user permissions
from frappe.permissions import clear_user_permissions_for_doctype
clear_user_permissions_for_doctype("Your DocType", "user@example.com")
```

## Issue 2: Can See Document in List but Can't Open

**Symptoms:** Document appears in list view but "You don't have permission" error when opening

**Possible Causes:**
1. Has "select" permission but not "read"
2. `has_permission` hook is denying access
3. Permission query conditions don't match when checking individual document

**Solutions:**

```python
# Debug: Check document permissions
doc = frappe.get_doc("Your DocType", "DOC-001")
perms = frappe.permissions.get_doc_permissions(doc, user="user@example.com")
print(f"Document permissions: {perms}")

# Debug: Enable detailed permission logging
result = frappe.has_permission("Your DocType", "read", doc,
                                user="user@example.com", debug=True)
# Check logs for details

# Fix: Ensure role has "read" permission, not just "select"
# Fix: Review has_permission hook logic
```

## Issue 3: Permission Query Hook Not Working

**Symptoms:** Hook is registered but documents are still not filtered correctly

**Possible Causes:**
1. Hook not properly registered in hooks.py
2. Syntax error in SQL condition
3. Cache not cleared after hook changes
4. Hook returning None instead of empty string

**Solutions:**

```python
# Verify hook registration
hooks = frappe.get_hooks("permission_query_conditions")
print(f"Registered hooks: {hooks}")

# Test hook directly
from your_app.your_module.your_doctype import get_permission_query_conditions
condition = get_permission_query_conditions(user="user@example.com")
print(f"Returned condition: {condition}")

# Clear cache
frappe.clear_cache()

# Correct hook return value
def get_permission_query_conditions(user):
    # WRONG: returns None
    if some_condition:
        return None

    # CORRECT: returns empty string for no restrictions
    if some_condition:
        return ""

    return "your_condition"
```

## Issue 4: Write Operations Fail Silently

**Symptoms:** Document saves without error but changes aren't persisted

**Possible Causes:**
1. `write_permission_query_conditions` is failing validation
2. Transaction rollback due to permission check
3. `before_save` hook blocking changes

**Solutions:**

```python
# Debug: Check write permission conditions
from frappe.permissions import check_write_permission_query_conditions
can_write = check_write_permission_query_conditions(doc, ptype="write")
print(f"Can write: {can_write}")

# Enable transaction debugging
frappe.db.rollback()  # Check if this is called unexpectedly

# Fix: Review write_permission_query_conditions hook
# Fix: Ensure conditions match the current state of document
# Note: write_permission_query_conditions is automatically called
# during has_permission() for write operations
```

## Issue 5: Virtual DocType Permission Issues

**Symptoms:** Permission errors or incorrect filtering on virtual doctypes

**Possible Causes:**
1. Trying to use permission_query_conditions on virtual doctype
2. Custom get_list not implementing permission checks

**Solutions:**

```python
# Virtual doctypes need custom permission handling
class YourVirtualDocType(Document):
    @staticmethod
    def get_list(args):
        # Manually check permissions
        user = frappe.session.user
        if user == "Administrator":
            # Return all documents
            pass
        else:
            # Filter based on custom logic
            pass

        return filtered_list

    def has_permission(self, ptype="read", user=None):
        # Implement custom permission check
        return True  # or custom logic
```

## Issue 6: Share Permissions Not Working

**Symptoms:** Shared documents not accessible to users

**Possible Causes:**
1. Document sharing disabled in System Settings
2. Wrong permission type specified when sharing
3. User doesn't have System User role

**Solutions:**

```python
# Check if sharing is enabled
sharing_enabled = not frappe.get_system_settings("disable_document_sharing")
print(f"Sharing enabled: {sharing_enabled}")

# Verify share exists
shares = frappe.get_all("DocShare", filters={
    "share_doctype": "Your DocType",
    "share_name": "DOC-001",
    "user": "user@example.com"
})
print(f"Shares: {shares}")

# Check user has System User role
is_system_user = frappe.permissions.is_system_user("user@example.com")
print(f"Is system user: {is_system_user}")
```

## Issue 7: Administrator Not Seeing All Documents

**Symptoms:** Even Administrator can't see certain documents

**Possible Causes:**
1. Filters or conditions applied regardless of user
2. Virtual doctype with custom filtering
3. Data permission errors (documents don't exist)

**Solutions:**

```python
# Verify Administrator check is first in hook
def has_permission(doc, ptype, user):
    # ALWAYS check Administrator first
    if user == "Administrator":
        return True

    # Your custom logic
    pass

# Check if documents actually exist
exists = frappe.db.exists("Your DocType", "DOC-001")
print(f"Document exists: {exists}")
```

## Issue 8: User Sees Too Many Documents

**Symptoms:** User sees documents they shouldn't have access to

**Possible Causes:**
1. Permission query conditions too permissive
2. No permission query conditions defined
3. Role permissions too broad
4. User has multiple User Permissions creating OR logic

**Solutions:**

```python
# Check permission query conditions
from frappe.model.db_query import DatabaseQuery
query = DatabaseQuery("Your DocType", user="user@example.com")
conditions = query.get_permission_query_conditions()
print(f"Applied conditions: {conditions}")

# If empty or "1=1", add proper filtering
def get_permission_query_conditions(user):
    if user == "Administrator":
        return ""

    # Add your filtering logic
    user_company = frappe.db.get_value("User", user, "company")
    return f"`tabYour DocType`.`company` = {frappe.db.escape(user_company)}"
```

## Issue 9: Permission Changes Don't Take Effect

**Symptoms:** Changes to permission hooks or role permissions not reflecting

**Possible Causes:**
1. Cache not cleared
2. Server not restarted
3. Hook path incorrect in hooks.py
4. Syntax error in hook code

**Solutions:**

```bash
# Clear cache
bench --site your-site clear-cache

# Restart server
bench restart

# Rebuild
bench --site your-site rebuild
```

```python
# Verify hook registration in Python console
import frappe
hooks = frappe.get_hooks("permission_query_conditions")
print(hooks)

# Clear cache programmatically
frappe.clear_cache()
```

## Issue 10: Child Table Fields Not Visible

**Symptoms:** User can see parent document but not specific child table or fields

**Possible Causes:**
1. Child table field has permlevel > 0
2. User doesn't have permission for that permlevel
3. Parent document permission restricting child access

**Solutions:**

```python
# Check permlevel of child table field
meta = frappe.get_meta("Parent DocType")
child_field = meta.get_field("child_table_fieldname")
print(f"Child table permlevel: {child_field.permlevel}")

# Check user's accessible permlevels
accessible_permlevels = meta.get_permlevel_access("read", user="user@example.com")
print(f"User can access permlevels: {accessible_permlevels}")

# Fix: Grant user permission for required permlevel in Role Permission Manager
```

## Issue 11: Slow List Views

**Symptoms:** List views taking long time to load

**Possible Causes:**
1. Expensive permission query conditions
2. Too many User Permissions
3. Complex SQL conditions without indexes
4. Multiple permission hooks

**Solutions:**

```python
# Optimize permission query conditions
def get_permission_query_conditions(user):
    # SLOW - functions on indexed columns
    return "DATE(`tabDoc`.`creation`) = CURDATE()"

    # FAST - direct indexed column comparison
    return f"`tabDoc`.`company` = {frappe.db.escape(user_company)}"

# Cache user data
user_company = frappe.cache.hget("user_companies", user,
    lambda: frappe.db.get_value("User", user, "company"))

# Add database indexes on filtered columns
frappe.db.add_index("Your DocType", ["company"])
```

## Issue 12: "frappe.exceptions.PermissionError" in API Calls

**Symptoms:** API calls failing with permission errors

**Possible Causes:**
1. API key user doesn't have permissions
2. Guest user trying to access restricted resource
3. Cross-site restrictions

**Solutions:**

```python
# Check API key user permissions
api_key = "your_api_key"
api_secret = "your_api_secret"

# Get user for this API key
user = frappe.get_all("User", filters={"api_key": api_key}, limit=1)
if user:
    # Check permissions for this user
    perms = frappe.has_permission("Your DocType", user=user[0].name)
    print(f"Has permission: {perms}")

# In API code, use ignore_permissions with caution
doc = frappe.get_doc("Your DocType", "DOC-001", ignore_permissions=True)
```

## Troubleshooting Workflow

1. **Enable debug mode**: `debug=True` in has_permission
2. **Check role permissions**: Verify user has necessary roles
3. **Check user permissions**: Look for restrictive User Permissions
4. **Check query conditions**: Verify permission_query_conditions
5. **Test as user**: Switch to user's session and test
6. **Clear cache**: After any permission changes
7. **Check logs**: Look for errors in error log
8. **Test incrementally**: Add/remove permissions one at a time
