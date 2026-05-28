# Permission Levels

## Overview

Permission levels provide field-level access control within a document. Different fields can require different permission levels, allowing you to hide sensitive information from certain users.

## How Permission Levels Work

1. Each field can have a permlevel (0, 1, 2, etc.)
2. Users must have role permission with that permlevel to see/edit the field
3. Permlevel 0 is default and always checked
4. Higher permlevels are for sensitive fields (e.g., pricing, margins, internal notes)

## Setting Permission Levels

### In DocType JSON

```json
{
  "fieldname": "discount_percentage",
  "fieldtype": "Percent",
  "label": "Discount %",
  "permlevel": 1
}
```

### In DocType Form (UI)

1. Open DocType
2. Edit field
3. Set "Perm Level" (0, 1, 2, etc.)
4. Save

## Configuring Role Permissions for Levels

In Permission Manager:

1. Go to Role Permission Manager
2. Select DocType
3. For each role, you can grant permissions at different levels
4. Check "Perm Level" column and grant read/write for each level

Example:
- Sales User: Permlevel 0 (read/write)
- Sales Manager: Permlevel 0 and 1 (read/write)
- Director: Permlevel 0, 1, and 2 (read/write)

## Example Use Cases

### Use Case 1: Hide pricing from warehouse staff

```json
// In Sales Order Item (child table)
{
  "fields": [
    {"fieldname": "item_code", "permlevel": 0},
    {"fieldname": "qty", "permlevel": 0},
    {"fieldname": "rate", "permlevel": 1},        // Only managers
    {"fieldname": "discount", "permlevel": 1},    // Only managers
    {"fieldname": "margin", "permlevel": 2}       // Only directors
  ]
}
```

Role permissions:
- Warehouse Staff: Permlevel 0 only
- Sales Manager: Permlevel 0 and 1
- Director: Permlevel 0, 1, and 2

### Use Case 2: Hide internal notes from customers on portal

```json
{
  "fields": [
    {"fieldname": "description", "permlevel": 0},
    {"fieldname": "internal_notes", "permlevel": 1}
  ]
}
```

### Use Case 3: Restrict cost fields to finance team

```json
{
  "fields": [
    {"fieldname": "selling_price", "permlevel": 0},
    {"fieldname": "cost_price", "permlevel": 1},
    {"fieldname": "profit_margin", "permlevel": 1}
  ]
}
```

## Checking Permission Level Access

```python
# Get which permlevels a user can access
meta = frappe.get_meta("Sales Order")
accessible_permlevels = meta.get_permlevel_access("read", user="user@example.com")
# Returns: [0, 1]  (user can access permlevel 0 and 1, but not 2)
```

## In has_permission Hook

```python
def has_permission(doc, ptype=None, user=None, debug=False):
    """Restrict edit access to sensitive fields based on role."""
    if ptype in ("write", "submit"):
        # Check if user has access to permlevel 1 (pricing fields)
        meta = frappe.get_meta(doc.doctype)
        accessible_permlevels = meta.get_permlevel_access(ptype, user=user)
        
        # If pricing fields were modified, check access
        if doc.has_value_changed("discount_percentage"):
            if 1 not in accessible_permlevels:
                frappe.throw("You don't have permission to modify pricing")
    
    return None
```

## Child Table Permission Levels

Permission levels in child tables (Table fields):

1. Set permlevel on the Table field itself in parent DocType
2. This controls access to the entire child table
3. Can also set permlevel on individual fields within child table

Example:

```json
// In parent Sales Order
{
  "fieldname": "cost_breakdown",
  "fieldtype": "Table",
  "options": "Cost Breakdown Item",
  "permlevel": 1  // Only managers can see this child table
}

// In child Cost Breakdown Item
{
  "fields": [
    {"fieldname": "component", "permlevel": 0},
    {"fieldname": "cost", "permlevel": 0}
  ]
}
```

## Standard Fields with Permission Levels

Some standard fields can also have permission levels:

- Naming series
- Status fields
- Workflow state fields

## Best Practices

1. **Start with permlevel 0**: Most fields should be at permlevel 0
2. **Group related fields**: Put related sensitive fields at the same level
3. **Document the levels**: Add comments explaining what each level protects
4. **Test thoroughly**: Verify users see/hide correct fields
5. **Use sparingly**: Too many levels can confuse users
6. **Consider UI layout**: Fields with different permlevels may break layout

## Limitations

1. **Cannot hide standard fields**: Some standard fields like name, owner cannot have permlevel
2. **All or nothing**: User either sees the field or doesn't, no read-only for higher permlevel
3. **Complexity**: Multiple permlevels can be hard to manage
4. **Child tables**: Entire child table hidden if user lacks access to permlevel

## Common Patterns

### Pattern 1: Three-tier access

```python
# Permlevel 0: Everyone
# Permlevel 1: Managers
# Permlevel 2: Directors

# Fields:
# - Basic info: permlevel 0
# - Pricing: permlevel 1
# - Cost/Margin: permlevel 2
```

### Pattern 2: Internal vs external

```python
# Permlevel 0: Customer-facing fields
# Permlevel 1: Internal fields (notes, analysis)
```

### Pattern 3: Financial data protection

```python
# Permlevel 0: Quantity, description
# Permlevel 1: Pricing, discounts
# Permlevel 2: Cost, margin, profit
```

## UI Behavior

When user lacks access to a permlevel:
- Fields are completely hidden
- No placeholder or indication they exist
- Form layout may look different for different users

## Debugging

```python
# Check user's accessible permlevels
from frappe.permissions import get_role_permissions

meta = frappe.get_meta("Sales Order")
perms = get_role_permissions(meta, user="user@example.com")

# Get accessible permlevels
accessible = meta.get_permlevel_access("read", user="user@example.com")
print(f"User can access permlevels: {accessible}")
```

## Example: Sales Order with Permission Levels

```json
{
  "doctype": "Sales Order",
  "fields": [
    // Permlevel 0 - Everyone
    {"fieldname": "customer", "permlevel": 0},
    {"fieldname": "delivery_date", "permlevel": 0},
    {"fieldname": "items", "permlevel": 0},
    
    // Permlevel 1 - Sales Managers
    {"fieldname": "discount_percentage", "permlevel": 1},
    {"fieldname": "pricing_rule", "permlevel": 1},
    
    // Permlevel 2 - Directors
    {"fieldname": "internal_notes", "permlevel": 2},
    {"fieldname": "cost_breakdown", "permlevel": 2}
  ]
}
```

Role permissions:
```python
# Sales User
Permlevel 0: Read, Write

# Sales Manager  
Permlevel 0: Read, Write
Permlevel 1: Read, Write

# Director
Permlevel 0: Read, Write
Permlevel 1: Read, Write
Permlevel 2: Read, Write
```
