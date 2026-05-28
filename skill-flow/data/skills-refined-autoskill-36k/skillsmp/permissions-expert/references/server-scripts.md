# Server Scripts - Permission Query

## Purpose

Define permission query conditions using Server Scripts (Python code in the UI) for rapid prototyping and testing before moving to code.

## Location

Created through Frappe UI at `/app/server-script`

## Script Type

"Permission Query"

## Available Variables

- `user`: The user being checked
- `doctype`: The DocType being queried

## Return Value

Must return a string with SQL WHERE condition (without the "WHERE" keyword)

## Example Server Script

```python
# Server Script Name: Your DocType Permission Query
# Script Type: Permission Query
# DocType: Your DocType

# The script should return a SQL WHERE condition
conditions = []

# Show documents from user's department
user_dept = frappe.db.get_value("User", user, "department")
if user_dept:
    conditions.append(f"`tabYour DocType`.`department` = {frappe.db.escape(user_dept)}")

# Managers see all departments
if "Manager" in frappe.get_roles(user):
    return ""  # Empty condition = show all

# Return combined conditions
return " AND ".join(conditions) if conditions else "1=0"
```

## Notes

- Available variables: `user`, `doctype`
- Must return a string with SQL WHERE condition
- Automatically integrated with permission query flow
- Useful for rapid prototyping before moving to code
- Server scripts have performance overhead compared to code-based hooks

## Best Practices

1. **Use for prototyping**: Test permission logic quickly before coding
2. **Move to code for production**: Code-based hooks are faster and more maintainable
3. **Always escape input**: Use `frappe.db.escape()` for dynamic values
4. **Test thoroughly**: Server scripts can be harder to debug than Python files
5. **Document the logic**: Add comments explaining the permission rules

## Example Use Cases

### Example 1: Department-based filtering

```python
# Only show documents from user's department
user_dept = frappe.db.get_value("User", user, "department")
if not user_dept:
    return "1=0"

return f"`tabYour DocType`.`department` = {frappe.db.escape(user_dept)}"
```

### Example 2: Role-based access

```python
# Different access based on role
roles = frappe.get_roles(user)

if "Manager" in roles:
    return ""  # See everything

if "Team Lead" in roles:
    team = frappe.db.get_value("User", user, "team")
    return f"`tabYour DocType`.`team` = {frappe.db.escape(team)}"

# Default: see only own documents
return f"`tabYour DocType`.`owner` = {frappe.db.escape(user)}"
```

### Example 3: Status-based filtering

```python
# Show only approved documents to regular users
roles = frappe.get_roles(user)

if "Approver" in roles:
    return ""  # Approvers see all

# Regular users see only approved documents
return "`tabYour DocType`.`status` = 'Approved'"
```

## Integration with Permission Query Flow

Server scripts are automatically integrated into the permission query flow:

1. System checks for registered Server Scripts of type "Permission Query"
2. If found for the doctype, executes the script with `user` and `doctype` variables
3. Returns the SQL condition to be combined with other permission conditions
4. Combined with code-based `permission_query_conditions` hooks using AND logic

## Debugging

Enable debug mode to see server script execution:

```python
frappe.has_permission("Your DocType", "read", doc, debug=True)
```

Check logs to see if server script was executed and what condition it returned.
