---
name: report-expert
description: Expert guidance on Frappe reports including report types, structure, creation workflow, and best practices. Use when creating standard script reports, query reports, understanding report structure, working with columns and filters, or troubleshooting report-related issues.
---

# Frappe Report Expert

This skill provides comprehensive guidance for working with Frappe reports, their structure, creation workflow, and best practices.

## Overview

Frappe provides a powerful reporting framework with multiple report types for different use cases:

- **Report Builder**: Visual report builder without code (uses DocType fields)
- **Query Report**: SQL-based reports with direct database queries
- **Script Report**: Python-based reports with full programmatic control (most flexible)
- **Custom Report**: Customized version of an existing report

This skill focuses primarily on **Script Reports** as they are the most commonly created programmatically and offer the most flexibility.

## Quick Reference

### Report Types Comparison

| Report Type | Code Required | Use Case | Flexibility |
|-------------|---------------|----------|-------------|
| Report Builder | None | Simple reports from DocType fields | Low |
| Query Report | SQL only | Database-driven reports, joins | Medium |
| Script Report | Python + JS | Complex logic, calculations, custom data | High |
| Custom Report | None | Saved customization of existing report | N/A |

### Standard Script Report Structure

Every Script Report consists of three files:

```
{module}/report/{report_name}/
├── __init__.py (empty)
├── {report_name}.json (metadata)
├── {report_name}.py (execute function)
└── {report_name}.js (filters and client-side logic)
```

## Core Concepts

### The Execute Function

The Python file must contain an `execute(filters=None)` function:

```python
def execute(filters=None):
    columns, data = [], []
    # Your logic here
    return columns, data
```

**Return value:**
- Returns a tuple: `(columns, data)` or extended `(columns, data, message, chart, report_summary, skip_total_row)`
- `columns`: List of column definitions
- `data`: List of rows (each row is a list or dict)

### Column Format

Columns can be defined as strings or dictionaries:

**String format:**
```python
columns = [
    "Name:Data:150",
    "Amount:Currency:120",
    "Customer:Link/Customer:200"
]
```

**Dictionary format:**
```python
columns = [
    {
        "label": "Name",
        "fieldname": "name",
        "fieldtype": "Data",
        "width": 150
    }
]
```

**Common fieldtypes:**
- **Text**: Data, Small Text, Text, Long Text, Text Editor, HTML Editor, Markdown Editor, Code
- **Numeric**: Int, Long Int, Float, Currency, Percent
- **Date/Time**: Date, Datetime, Time, Duration
- **Relationships**: Link (requires `options`), Dynamic Link
- **Boolean**: Check
- **Special**: Attach, Attach Image, Signature, Color, Barcode, Rating, Icon, Geolocation, Phone, Autocomplete, JSON, Password, Read Only

See [references/column-fieldtypes.md](references/column-fieldtypes.md) for complete field type reference.

### Data Format

Data rows can be lists or dictionaries:

**List format (matches column order):**
```python
data = [
    ["ID-001", 1000, "Customer A"],
    ["ID-002", 2000, "Customer B"],
]
```

**Dictionary format (uses fieldnames):**
```python
data = [
    {"name": "ID-001", "amount": 1000, "customer": "Customer A"},
    {"name": "ID-002", "amount": 2000, "customer": "Customer B"},
]
```

### Filters

Filters are defined in the JavaScript file:

```javascript
frappe.query_reports["Report Name"] = {
    filters: [
        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            reqd: 1
        },
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -1)
        }
    ]
};
```

See [references/filter-fieldtypes.md](references/filter-fieldtypes.md) for complete filter reference.

## Creating a Script Report

### Quick Start

1. **Create Report via Desk**: Navigate to Report DocType, create new with type "Script Report"
2. **Implement Execute Function**: Edit the generated `.py` file with your logic
3. **Define Filters**: Edit the generated `.js` file with filter definitions
4. **Test**: Run `bench migrate` and navigate to `/app/query-report/Your Report`

See [references/report-creation-workflow.md](references/report-creation-workflow.md) for detailed step-by-step guide.

## Common Use Cases

### Simple List Report

```python
def execute(filters=None):
    return get_columns(), frappe.get_list(
        "DocType",
        fields=["name", "status", "amount"],
        filters=filters
    )

def get_columns():
    return [
        "Name:Link/DocType:150",
        "Status:Data:100",
        "Amount:Currency:120"
    ]
```

### Report with Calculations

Add calculated fields in Python before returning data.

### Grouped/Hierarchical Reports

Use `indent` field and return tree structure flag.

See [references/script-report-examples.md](references/script-report-examples.md) for complete working examples.

## Advanced Features

- **Charts**: Return chart configuration as 4th element
- **Report Summary**: Return summary metrics as 5th element
- **Custom Buttons**: Add buttons in JavaScript `onload` function
- **Tree View**: Enable hierarchical display with indent levels
- **Permissions**: Use `frappe.only_for()` or `frappe.has_permission()`
- **Performance**: Cache results, use proper indexing, limit data

See [references/advanced-features.md](references/advanced-features.md) for detailed documentation.

## Reference Files

For detailed information on specific topics:

- **[report-creation-workflow.md](references/report-creation-workflow.md)** - Step-by-step guide to creating Script Reports
- **[script-report-examples.md](references/script-report-examples.md)** - Complete working examples of various report patterns
- **[column-fieldtypes.md](references/column-fieldtypes.md)** - All available column fieldtypes
- **[column-fieldproperties.md](references/column-fieldproperties.md)** - Column properties and formatting options
- **[filter-fieldtypes.md](references/filter-fieldtypes.md)** - All available filter types
- **[filter-fieldproperties.md](references/filter-fieldproperties.md)** - Filter properties and configuration options
- **[advanced-features.md](references/advanced-features.md)** - Charts, summaries, custom buttons, tree reports, and optimization

## Best Practices

**Code Organization:**
- Use helper functions: `get_columns()`, `get_data()`, `get_conditions()`
- Handle None filters: Check `filters.get(key)` not `filters[key]`

**Performance:**
- Filter early in SQL WHERE clause
- Use proper database indexes
- Add LIMIT for large datasets
- Cache expensive operations

**Security:**
- Validate permissions with `frappe.only_for()` or `frappe.has_permission()`
- Sanitize inputs in SQL queries
- Use parameterized queries

**User Experience:**
- Provide sensible default filter values
- Use appropriate column widths
- Add translations with `_()` or `__()`
- Sort data logically

## Troubleshooting

**Report not showing up:**
- Check if report is disabled
- Verify user has required role
- Run `bench migrate` to sync

**Data not displaying correctly:**
- Verify column count matches data row length
- Check fieldtype matches data type

**Filter not working:**
- Check fieldname matches in JS and Python
- Verify filter value is passed correctly

See documentation for common issues and solutions.
