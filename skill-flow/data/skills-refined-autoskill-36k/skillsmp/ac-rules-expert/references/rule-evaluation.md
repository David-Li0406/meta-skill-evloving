# Rule Evaluation and SQL Generation

This document explains how AC Rules are evaluated and how SQL queries are generated for filtering.

## Rule Map Generation

**Function**: `get_rule_map()` in `ac_rule_utils.py`

The rule map is a hierarchical structure that organizes rules by resource and action:

```python
rule_map = {
    "doctype": {
        "Customer": {
            "": {  # fieldname (empty string = whole doctype)
                "read": [rule1, rule2, ...],
                "write": [rule1, rule2, ...],
                "delete": [...]
            }
        }
    },
    "report": {
        "Sales Report": {
            "": {
                "read": [rule1, rule2, ...]
            }
        }
    }
}
```

**Process**:
1. Load all enabled AC Resources
2. For each resource, create slots for managed actions
3. Load all valid, enabled AC Rules (within date range)
4. For each rule, resolve principals and resources
5. Add rule to appropriate slots in the map

## Permission Evaluation Flow

### Step 1: Get Resource Rules

**Function**: `get_resource_rules()` in `ac_rule_utils.py`

1. **Get Rule Map**: Load the complete rule map (cached)
2. **Find Applicable Rules**: Look up rules for the specific resource/action
3. **Filter by User** (Principal Resolution):
   - For each rule, convert principal filters to SQL
   - Handle User, User Group, and Role reference doctypes specially
   - Execute SQL to check if current user matches any principals
   - Exclude exception principals
4. **Return Matching Rules**: Only rules where the user matches principals

### Step 2: Build Resource Filter Query

**Function**: `get_resource_filter_query()` in `ac_rule_utils.py`

1. **Get User's Rules**: Call `get_resource_rules()` to get rules for user
2. **Build Resource Filter** (Resource Resolution):
   - For each rule, convert resource filters to SQL
   - Combine allowed and denied filters with AND/OR logic
   - Separate Permit and Forbid rules
3. **Combine Rules**:
   ```sql
   -- Final query structure
   (Permit1 OR Permit2 OR ...) AND NOT (Forbid1 OR Forbid2 OR ...)
   ```
4. **Return Query**: SQL WHERE clause that filters records

**Access Levels**:
- `total`: User has access to all records (query = "1=1")
- `none`: User has no access (query = "1=0")
- `partial`: User has conditional access (complex query)
- `unmanaged`: Resource not managed by AC Rules (full Frappe permissions apply)

## Principal Filter SQL Generation

**Function**: `get_principal_filter_sql(filter)` in `ac_rule_utils.py`

Special handling for different reference doctypes:

### User Filter (reference_doctype = "User")

```python
# Direct SQL from filter
return filter.get_sql()
```

### User Group Filter (reference_doctype = "User Group")

```python
# Get matching user groups
user_groups = frappe.db.sql(f"SELECT name FROM `tabUser Group` WHERE {sql}")

# Get users in those groups
sql = frappe.get_all("User Group Member", 
                    filters={"parent": ["in", user_groups]}, 
                    fields=["user"], run=0)

return f"`tabUser`.`name` in ({sql})"
```

### Role Filter (reference_doctype = "Role")

```python
# Get matching roles
roles = frappe.db.sql(f"SELECT name FROM `tabRole` WHERE {sql}")

# Handle "All" role specially
if "All" in roles:
    sql = frappe.get_all("User", run=0)
else:
    sql = frappe.get_all("Has Role", 
                       filters={"role": ["in", roles]}, 
                       fields=["parent"], run=0)

return f"`tabUser`.`name` in ({sql})"
```

## Resource Filter SQL Generation

**Function**: `get_resource_filter_sql(filter)` in `ac_rule_utils.py`

```python
if filter.get("all"):
    return "1=1"  # Match all records

if filter.get("name"):
    filter = frappe.get_cached_doc("Query Filter", filter.get("name"))
    return filter.get_sql()

return "1=0"  # Match nothing
```

## Permit vs Forbid Logic

User will have access if:
- At least ONE Permit rule matches
- AND ZERO Forbid rules match

**Example**:
```python
# These rules work together:
Permit Rule 1: All records (filter returns "1=1")
Forbid Rule 2: Archived records (filter returns "status = 'Archived'")

# Final query: (1=1) AND NOT (status = 'Archived')
# Result: User can access all records except archived ones
```

**Common mistake**:
```python
# This is redundant:
Permit Rule 1: Active records (filter returns "status = 'Active'")
# No Forbid rule needed - just use the Permit filter

# Better approach:
Permit Rule 1: Active records
# User can ONLY access active records
```

## Performance Optimization

### 1. Request Caching

Query Filter's `get_sql()` uses `@frappe.request_cache` to cache SQL generation within a single request.

```python
@frappe.request_cache
def get_sql(query_filter: str | QueryFilter | dict):
    # Cached per request
    pass
```

### 2. Rule Map Caching

The rule map should be cached for performance:

```python
@frappe.cache()  # Site-level cache
def get_rule_map():
    # Expensive operation - cache this
    pass
```

**Cache Invalidation**: Clear cache when:
- AC Rule is created/updated/deleted
- AC Resource is created/updated/deleted
- Query Filter is created/updated/deleted

### 3. SQL Query Optimization

- Ensure proper indexes on filtered fields
- Avoid complex Python filters when SQL/JSON will work
- Test generated SQL with EXPLAIN to check performance
- Consider materialized views for complex filters

### 4. Limit Rule Complexity

- Too many rules per resource/action slows evaluation
- Too many filters per rule increases SQL complexity
- Combine similar rules when possible
- Use exceptions sparingly

## Checking Access Programmatically

### Check if user has any access

```python
from tweaks.tweaks.doctype.ac_rule.ac_rule_utils import has_resource_access

result = has_resource_access(
    doctype="Customer",
    action="write",
    user=frappe.session.user
)

if result.get("access"):
    # User has write access to some customers
    pass
else:
    frappe.throw("You don't have write access to customers")
```

### Get filter query for listing

```python
from tweaks.tweaks.doctype.ac_rule.ac_rule_utils import get_resource_filter_query

result = get_resource_filter_query(
    doctype="Customer",
    action="read"
)

if result.get("access") == "total":
    # User can see all customers
    customers = frappe.get_all("Customer")
elif result.get("access") == "partial":
    # Apply filter query
    query = result.get("query")
    customers = frappe.db.sql(f"""
        SELECT * FROM `tabCustomer`
        WHERE {query}
    """, as_dict=True)
else:
    # No access
    customers = []
```

## Security Considerations

### SQL Injection Prevention

**Always use proper escaping**:

```python
# GOOD - Using frappe.db.escape()
user = frappe.session.user
conditions = f"`tabCustomer`.`owner` = {frappe.db.escape(user)}"

# BAD - Direct interpolation
conditions = f"`tabCustomer`.`owner` = '{user}'"  # Vulnerable!
```

### Python Filter Safety

Python filters use `safe_exec()` which provides a restricted environment:

```python
from frappe.utils.safe_exec import safe_exec

loc = {"resource": query_filter, "conditions": ""}
safe_exec(
    filters,
    None,
    loc,
    script_filename=f"Query Filter {query_filter.get('name')}"
)
```

**Restrictions**:
- No import statements
- Limited built-in functions
- Sandboxed environment

### Permission Bypass Prevention

**Never allow**:
- Direct SQL execution without validation
- User-provided SQL in filters
- Disabling AC Rules without authorization

**Always**:
- Validate filter references match resource types
- Check user permissions before executing
- Log access attempts for audit trail
