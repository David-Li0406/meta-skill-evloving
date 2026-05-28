# User Permissions

## Overview

User Permissions restrict access to specific document values for link fields. They provide document-level access control based on user assignments.

## How User Permissions Work

1. Checked after role permissions but before share permissions
2. Applied to the document itself if doctype matches
3. Applied to all link fields pointing to restricted doctypes
4. If `apply_strict_user_permissions` is enabled, even empty link fields are checked
5. "if_owner" permissions take precedence when user is the document owner

## Creating User Permissions Programmatically

```python
from frappe.permissions import add_user_permission

add_user_permission(
    doctype="Company",           # DocType to restrict
    name="Company A",            # Specific document
    user="user@example.com",     # User to apply restriction to
    applicable_for="Sales Order", # Optional: Apply only to this doctype
    is_default=1,                # Optional: Make this the default value
    hide_descendants=0,          # Optional: For tree doctypes
    ignore_permissions=True      # Optional: Bypass permission checks
)
```

## Creating User Permissions via UI

1. Go to User Permission List
2. Click "New"
3. Select:
   - User
   - Allow (DocType to restrict, e.g., "Company")
   - For Value (Specific document, e.g., "Company A")
   - Applicable For (Optional: specific DocType)
4. Save

## Parameters Explained

### doctype (Allow)

The DocType you want to restrict access to (e.g., "Company", "Territory", "Cost Center")

### name (For Value)

The specific document the user can access (e.g., "Company A", "North Territory")

### applicable_for

Optional. If specified, the restriction only applies when this value is used in link fields of this DocType.

Example:
- Allow: Company
- For Value: Company A
- Applicable For: Sales Order

This means the user can only see Company A in Sales Order link fields, but might see other companies elsewhere.

### is_default

If checked, this value becomes the default for new documents.

### hide_descendants

For tree doctypes. If checked, user cannot access child nodes of the permitted document.

## Example Use Cases

### Use Case 1: Multi-Company Access Control

Restrict users to specific companies:

```python
# User can only access Company A
add_user_permission("Company", "Company A", "user@example.com")

# Now user can only:
# - View documents where company = Company A
# - Create documents with company = Company A
# - See "Company A" in company link fields
```

### Use Case 2: Territory-Based Sales Access

```python
# Sales user restricted to North territory
add_user_permission("Territory", "North", "sales@example.com")

# Sales manager can access all territories (no user permission)
```

### Use Case 3: Department-Based Access

```python
# HR user can only access HR department documents
add_user_permission("Department", "HR", "hr@example.com")

# With applicable_for
add_user_permission(
    doctype="Department",
    name="HR", 
    user="hr@example.com",
    applicable_for="Employee"  # Only applies to Employee doctype
)
```

### Use Case 4: Warehouse Access Control

```python
# Warehouse keeper restricted to specific warehouse
add_user_permission("Warehouse", "Mumbai Warehouse", "keeper@example.com")
```

### Use Case 5: Branch-Based Banking

```python
# Bank teller can only access their branch
add_user_permission("Branch", "Mumbai Branch", "teller@example.com")

# Branch manager can access all branches (no user permission)
```

## Checking User Permissions

```python
from frappe.core.doctype.user_permission.user_permission import get_user_permissions

# Get all user permissions for a user
user_perms = get_user_permissions("user@example.com")

# Result structure:
# {
#     "Company": [
#         {
#             "doc": "Company A",
#             "applicable_for": None,
#             "is_default": 1,
#             "hide_descendants": 0
#         }
#     ]
# }
```

## Clearing User Permissions

```python
from frappe.permissions import clear_user_permissions_for_doctype

# Clear all user permissions for a specific doctype
clear_user_permissions_for_doctype("Company", "user@example.com")

# Clear all user permissions for a user
frappe.db.delete("User Permission", {"user": "user@example.com"})
```

## Interaction with Role Permissions

User Permissions are **more restrictive** than role permissions:

1. User must have role permission to read/write a doctype
2. User Permission further restricts which specific documents they can access
3. Even if user has role to read all Sales Orders, User Permission can limit them to specific companies

## Owner Permissions

If a user is the owner of a document, "if_owner" permissions take precedence over User Permissions:

```python
# User has User Permission for Company A only
# But user created a document with Company B
# If role has "if_owner" permission, user can still access it
```

## Strict User Permissions

Enable via System Settings: "Apply Strict User Permissions"

When enabled:
- Empty link fields are also validated
- Users cannot create documents without selecting a permitted value
- More restrictive but ensures data integrity

## Best Practices

1. **Start with roles**: Define role permissions first, then add User Permissions
2. **Use applicable_for**: More flexible and allows exceptions
3. **Document the structure**: Keep track of who has access to what
4. **Test thoroughly**: User Permissions can be confusing, test edge cases
5. **Use for data separation**: Ideal for multi-company, multi-branch setups
6. **Set defaults**: Use is_default to improve UX
7. **Monitor performance**: Many User Permissions can slow down queries

## Common Patterns

### Pattern 1: Multi-company setup

```python
# Assign each user to their company
for user in company_a_users:
    add_user_permission("Company", "Company A", user)

for user in company_b_users:
    add_user_permission("Company", "Company B", user)
```

### Pattern 2: Hierarchical territory access

```python
# Regional manager gets parent territory
add_user_permission("Territory", "North Region", "regional.manager@example.com")

# Sales users get specific territories
add_user_permission("Territory", "Delhi", "delhi.sales@example.com")
add_user_permission("Territory", "Mumbai", "mumbai.sales@example.com")
```

### Pattern 3: Conditional access

```python
# User can access Company A for Sales Orders only
add_user_permission(
    doctype="Company",
    name="Company A",
    user="user@example.com",
    applicable_for="Sales Order"
)

# But can access Company B for Purchase Orders
add_user_permission(
    doctype="Company",
    name="Company B",
    user="user@example.com",
    applicable_for="Purchase Order"
)
```

## Debugging User Permissions

```python
# Check if user has permission considering User Permissions
from frappe.permissions import has_user_permission

result = has_user_permission(doc, user="user@example.com", debug=True)

# Enable debug in has_permission
frappe.has_permission("Sales Order", "read", doc, user="user@example.com", debug=True)
```

## Limitations

1. **Performance**: Many User Permissions can slow down list queries
2. **Complexity**: Can be confusing when combined with role permissions
3. **No OR logic**: User cannot have "Company A OR Company B" except by creating multiple User Permissions
4. **Cache**: Permissions are cached, may need cache clear after changes
