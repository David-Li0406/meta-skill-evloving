---
name: ac-rules-expert
description: Expert guidance for creating, implementing, and troubleshooting AC (Access Control) Rules in Frappe Tweaks - an advanced rule-based permission system. Use when working with AC Rules, Query Filters, AC Resources, AC Actions, implementing fine-grained access control, debugging permission issues, creating principal/resource filters, integrating with DocTypes or Reports, or understanding rule evaluation and SQL generation.
---

# AC Rules Expert

Expert guidance for the Frappe Tweaks AC Rule system - an advanced access control framework that extends Frappe's built-in permissions with fine-grained, rule-based access control.

## Overview

The AC Rule system provides:
- **Fine-grained access control**: Control access at the record level, not just doctype level
- **Dynamic filtering**: Use SQL, Python, or JSON filters to determine access
- **Rule-based logic**: Define complex access rules with Permit/Forbid semantics
- **Principal-based**: Define who has access (users, roles, user groups, or custom logic)
- **Resource-based**: Define what is being accessed (doctypes, reports, or custom resources)
- **Action-based**: Control specific actions (read, write, delete, etc.)

## Implementation Status

**Current State**:
- ✅ **DocTypes**: Fully implemented - Automatic permission enforcement via Frappe hooks
- ✅ **Reports**: Fully functional - Manual integration required (call API and inject SQL)
- ✅ **Workflows**: Fully implemented - Automatic transition filtering and permission enforcement
- 🔄 **Migration**: Deprecated systems (Event Scripts, Server Script Permission Policy) being phased out

## Quick Start

### Creating AC Rules

1. **Create Query Filter**: Define who (principals) or what (resources) the rule applies to
2. **Create AC Resource**: Define the DocType or Report being controlled
3. **Create AC Rule**: Tie together principals, resources, and actions

### DocType Integration (Automatic)

No code needed - AC Rules are automatically enforced for DocTypes through Frappe permission hooks.

### Workflow Integration (Automatic)

No code needed - AC Rules automatically filter workflow transitions and enforce action permissions through Frappe workflow hooks.

### Report Integration (Manual)

```python
from tweaks.tweaks.doctype.ac_rule.ac_rule_utils import get_resource_filter_query

def execute(filters=None):
    result = get_resource_filter_query(report="Your Report", action="read")
    
    if result.get("access") == "none":
        return [], []
    
    ac_filter = result.get("query", "1=1")
    
    data = frappe.db.sql(f"""
        SELECT * FROM `tabDocType`
        WHERE {ac_filter}
    """, as_dict=True)
    
    return columns, data
```

## Core Components

The system consists of four main DocTypes:

1. **AC Rule**: Central component that defines access control rules (Permit/Forbid)
2. **Query Filter**: Reusable filter definitions (JSON, SQL, or Python)
3. **AC Resource**: Defines what is being accessed (DocType or Report)
4. **AC Action**: Defines controllable actions (read, write, delete, etc.)

See [references/core-components.md](references/core-components.md) for detailed documentation.

## Rule Evaluation

Rules are evaluated through:
1. **Rule Map Generation**: Organize rules by resource and action
2. **Principal Resolution**: Determine which users match the rule
3. **Resource Resolution**: Determine which records match the rule
4. **SQL Generation**: Convert filters to SQL WHERE clauses

**Final Logic**: `(Permit1 OR Permit2 OR ...) AND NOT (Forbid1 OR Forbid2 OR ...)`

See [references/rule-evaluation.md](references/rule-evaluation.md) for evaluation flow and SQL generation.

## Integration

### DocTypes (Automatic)

Implemented via Frappe permission hooks - no manual integration needed:
- Read operations: Filtered automatically in list views and queries
- Write operations: Filtered automatically for create, write, delete, submit, cancel

### Reports (Manual)

Must explicitly call `get_resource_filter_query()` and inject SQL into report queries.

See [references/integration.md](references/integration.md) for complete integration guide and API documentation.

## Usage Examples

Common patterns and complete examples:

1. **Sales Team Access Control**: Restrict report to user's managed customers
2. **Restrict Archived Records**: Prevent access to archived data
3. **Tenant-Based Multi-Tenancy**: Isolate data by tenant
4. **Department-Based Access**: Access based on user's department with exceptions
5. **Complex SQL Filters**: Subqueries and multi-table joins
6. **Multiple Permit Rules**: Combine rules for managers and team leaders

See [references/examples.md](references/examples.md) for complete code examples.

## Debugging and Auditing

**Available Reports** (System Manager role required):

1. **AC Permissions** - System-wide access audit (who has access to what)
2. **Query Filters** - Debug filter SQL generation with user impersonation
3. **AC Principal Query Filters** - See which users match each principal filter

**Common Workflows**:
- Why does User X have access? → AC Permissions Report
- Test a Query Filter → Query Filters Report with impersonation
- Who matches a Principal Filter? → AC Principal Query Filters Report

See [references/debugging-reports.md](references/debugging-reports.md) for detailed documentation and workflows.

## Troubleshooting

Common issues:
- **Rules Not Applying**: Check enabled status, date range, principal/resource matches
- **Incorrect Filtering**: Verify SQL generation, reference doctypes, exception flags
- **Performance Problems**: Analyze query complexity, consolidate rules, add indexes
- **Access Denied**: Check Forbid rules, verify user/record matches, test with Administrator

See [references/troubleshooting.md](references/troubleshooting.md) for debugging techniques and solutions.

## Best Practices

1. Use Standard Mode for simple mappings, Bypass for complex operations
2. Validate source/target before syncing
3. Handle missing targets gracefully
4. Use context for runtime parameters
5. Set appropriate timeouts for operation complexity
6. Use specific queues for heavy operations
7. Test with different user roles and edge cases
8. Always escape user input in SQL filters
9. Monitor performance with complex rule sets
10. Document rule logic and purpose

## Source Code Locations

- `tweaks/tweaks/doctype/ac_rule/` - AC Rule DocType
- `tweaks/tweaks/doctype/query_filter/` - Query Filter DocType
- `tweaks/tweaks/doctype/ac_resource/` - AC Resource DocType
- `tweaks/tweaks/doctype/ac_action/` - AC Action DocType
- `tweaks/tweaks/doctype/ac_rule/ac_rule_utils.py` - Core utilities and API

## Reference Files

For detailed information:
- **[core-components.md](references/core-components.md)**: Detailed documentation on AC Rule, Query Filter, AC Resource, AC Action
- **[rule-evaluation.md](references/rule-evaluation.md)**: Rule map generation, permission evaluation, SQL generation
- **[integration.md](references/integration.md)**: DocType and Report integration, API endpoints
- **[examples.md](references/examples.md)**: Complete usage examples and code patterns
- **[debugging-reports.md](references/debugging-reports.md)**: Reports for debugging and auditing permissions
- **[troubleshooting.md](references/troubleshooting.md)**: Common issues, debugging techniques, solutions
