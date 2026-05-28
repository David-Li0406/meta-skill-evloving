# Filter Fieldtypes Reference

Complete guide to all filter field types available in Frappe reports.

## Overview

Filters are defined in the JavaScript (`.js`) file of a report and allow users to control what data is displayed. Filters can use most of the same field types as DocType fields.

## Basic Filter Structure

```javascript
frappe.query_reports["Report Name"] = {
    filters: [
        {
            fieldname: "filter_name",
            label: __("Display Label"),
            fieldtype: "FieldType",
            options: "Configuration",  // Usage varies by fieldtype - see below
            default: "default_value",
            reqd: 1  // 1 for required, 0 for optional
        }
    ]
};
```

**The "options" property usage varies by field type:**
- **Link**: Target DocType name (e.g., `"Customer"`)
- **Select**: Array or newline-separated string (e.g., `["Draft", "Submitted"]` or `"\nDraft\nSubmitted"`)
- **MultiSelect**: DocType to select from (e.g., `"Warehouse"`)
- **Dynamic Link**: Use `get_options` function instead of `options` property
- **Code**: Language for syntax highlighting (e.g., `"Python"`)
- **Data**: Data type specification (e.g., `"Email"`)

See [filter-fieldproperties.md](filter-fieldproperties.md) for detailed property documentation and examples.

## Available Filter Fieldtypes

### Text Filters

**Data**
- Single-line text input
- Use for: Search terms, names, codes
```javascript
{
    fieldname: "search",
    label: __("Search"),
    fieldtype: "Data"
}
```

**Text**
- Multi-line text input
- Use for: Long descriptions, notes
```javascript
{
    fieldname: "description",
    label: __("Description"),
    fieldtype: "Text"
}
```

### Numeric Filters

**Int**
- Integer number input
- Use for: Quantities, counts, IDs
```javascript
{
    fieldname: "quantity",
    label: __("Minimum Quantity"),
    fieldtype: "Int",
    default: 0
}
```

**Float**
- Decimal number input
- Use for: Rates, measurements
```javascript
{
    fieldname: "rate",
    label: __("Minimum Rate"),
    fieldtype: "Float"
}
```

**Currency**
- Currency input with formatting
- Use for: Monetary amounts
```javascript
{
    fieldname: "amount",
    label: __("Minimum Amount"),
    fieldtype: "Currency"
}
```

### Date Filters

**Date**
- Date picker
- Use for: Single date selection
```javascript
{
    fieldname: "from_date",
    label: __("From Date"),
    fieldtype: "Date",
    default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
    reqd: 1
}
```

**Datetime**
- Date and time picker
- Use for: Timestamp selection
```javascript
{
    fieldname: "created_on",
    label: __("Created On"),
    fieldtype: "Datetime",
    default: frappe.datetime.now_datetime()
}
```

**Time**
- Time picker
- Use for: Time of day selection
```javascript
{
    fieldname: "start_time",
    label: __("Start Time"),
    fieldtype: "Time"
}
```

### Selection Filters

**Select**
- Dropdown with predefined options
- Use for: Status, categories, predefined choices
```javascript
{
    fieldname: "status",
    label: __("Status"),
    fieldtype: "Select",
    options: ["", "Draft", "Submitted", "Cancelled"],
    default: ""
}
```

With newline-separated string options:
```javascript
{
    fieldname: "priority",
    label: __("Priority"),
    fieldtype: "Select",
    options: "\nLow\nMedium\nHigh",
    default: ""
}
```

### Link Filters

**Link**
- Dropdown linked to a DocType
- Use for: References to documents
```javascript
{
    fieldname: "customer",
    label: __("Customer"),
    fieldtype: "Link",
    options: "Customer",
    default: frappe.defaults.get_user_default("Customer")
}
```

With filtered options:
```javascript
{
    fieldname: "warehouse",
    label: __("Warehouse"),
    fieldtype: "Link",
    options: "Warehouse",
    get_query: function() {
        return {
            filters: {
                "is_group": 0,
                "company": frappe.query_report.get_filter_value("company")
            }
        };
    }
}
```

**Dynamic Link**
- Link field where options depend on another field
- Use for: Polymorphic references
```javascript
{
    fieldname: "reference_type",
    label: __("Reference Type"),
    fieldtype: "Link",
    options: "DocType"
},
{
    fieldname: "reference_name",
    label: __("Reference Name"),
    fieldtype: "Dynamic Link",
    get_options: function() {
        let reference_type = frappe.query_report.get_filter_value("reference_type");
        if (!reference_type) {
            frappe.throw(__("Please select Reference Type first"));
        }
        return reference_type;
    }
}
```

### Boolean Filter

**Check**
- Checkbox filter
- Use for: Yes/No, enabled/disabled flags
```javascript
{
    fieldname: "include_cancelled",
    label: __("Include Cancelled"),
    fieldtype: "Check",
    default: 0
}
```

### Multi-Select Filters

**MultiSelect**
- Select multiple values from a list
- Use for: Multiple document selection
```javascript
{
    fieldname: "warehouses",
    label: __("Warehouses"),
    fieldtype: "MultiSelect",
    options: "Warehouse",
    get_data: function(txt) {
        return frappe.db.get_link_options("Warehouse", txt);
    }
}
```

**MultiSelectList**
- Enhanced multi-select with checkboxes
- Use for: Multiple selections with better UX
```javascript
{
    fieldname: "companies",
    label: __("Companies"),
    fieldtype: "MultiSelectList",
    get_data: function(txt) {
        return frappe.db.get_link_options("Company", txt, {
            "enabled": 1
        });
    }
}
```

## Filter Field Types by Category

**Text Input:**
Data, Text

**Numeric Input:**
Int, Float, Currency

**Date/Time Input:**
Date, Datetime, Time

**Selection:**
Select, Check

**References:**
Link, Dynamic Link

**Multi-Selection:**
MultiSelect, MultiSelectList

## Quick Reference Table

| Fieldtype | Input Type | Use For | Default Widget |
|-----------|------------|---------|----------------|
| Data | Text | Short text, search | Input box |
| Text | Textarea | Long text | Text area |
| Int | Number | Whole numbers | Number input |
| Float | Number | Decimals | Number input |
| Currency | Number | Money | Currency input |
| Date | Date picker | Dates | Date picker |
| Datetime | Datetime picker | Date+time | Datetime picker |
| Time | Time picker | Time only | Time picker |
| Select | Dropdown | Predefined options | Dropdown |
| Check | Checkbox | Boolean | Checkbox |
| Link | Autocomplete | DocType reference | Link search |
| Dynamic Link | Autocomplete | Dynamic reference | Link search |
| MultiSelect | Multi-select | Multiple values | Tag input |
| MultiSelectList | Checkbox list | Multiple selections | Checkbox list |

## Common Filter Patterns

### Date Range Filters

```javascript
filters: [
    {
        fieldname: "from_date",
        label: __("From Date"),
        fieldtype: "Date",
        default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
        reqd: 1
    },
    {
        fieldname: "to_date",
        label: __("To Date"),
        fieldtype: "Date",
        default: frappe.datetime.get_today(),
        reqd: 1
    }
]
```

### Company-Based Filters

```javascript
filters: [
    {
        fieldname: "company",
        label: __("Company"),
        fieldtype: "Link",
        options: "Company",
        default: frappe.defaults.get_user_default("Company"),
        reqd: 1
    },
    {
        fieldname: "fiscal_year",
        label: __("Fiscal Year"),
        fieldtype: "Link",
        options: "Fiscal Year",
        default: frappe.sys_defaults.fiscal_year
    }
]
```

### Status Filters

```javascript
filters: [
    {
        fieldname: "status",
        label: __("Status"),
        fieldtype: "Select",
        options: [
            "",
            "Draft",
            "Submitted",
            "Completed",
            "Cancelled"
        ],
        default: ""
    }
]
```

### Hierarchical Filters

```javascript
filters: [
    {
        fieldname: "company",
        label: __("Company"),
        fieldtype: "Link",
        options: "Company",
        reqd: 1
    },
    {
        fieldname: "cost_center",
        label: __("Cost Center"),
        fieldtype: "Link",
        options: "Cost Center",
        get_query: function() {
            return {
                filters: {
                    "company": frappe.query_report.get_filter_value("company")
                }
            };
        }
    }
]
```

## Examples by Report Type

### Financial Report Filters
```javascript
filters: [
    {
        fieldname: "company",
        label: __("Company"),
        fieldtype: "Link",
        options: "Company",
        reqd: 1
    },
    {
        fieldname: "fiscal_year",
        label: __("Fiscal Year"),
        fieldtype: "Link",
        options: "Fiscal Year",
        reqd: 1
    },
    {
        fieldname: "from_date",
        label: __("From Date"),
        fieldtype: "Date",
        reqd: 1
    },
    {
        fieldname: "to_date",
        label: __("To Date"),
        fieldtype: "Date",
        reqd: 1
    }
]
```

### Inventory Report Filters
```javascript
filters: [
    {
        fieldname: "company",
        label: __("Company"),
        fieldtype: "Link",
        options: "Company",
        default: frappe.defaults.get_user_default("Company")
    },
    {
        fieldname: "warehouse",
        label: __("Warehouse"),
        fieldtype: "Link",
        options: "Warehouse"
    },
    {
        fieldname: "item_group",
        label: __("Item Group"),
        fieldtype: "Link",
        options: "Item Group"
    },
    {
        fieldname: "include_zero_stock",
        label: __("Include Zero Stock"),
        fieldtype: "Check",
        default: 0
    }
]
```

### Sales Report Filters
```javascript
filters: [
    {
        fieldname: "from_date",
        label: __("From Date"),
        fieldtype: "Date",
        default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
        reqd: 1
    },
    {
        fieldname: "to_date",
        label: __("To Date"),
        fieldtype: "Date",
        default: frappe.datetime.get_today(),
        reqd: 1
    },
    {
        fieldname: "customer",
        label: __("Customer"),
        fieldtype: "Link",
        options: "Customer"
    },
    {
        fieldname: "territory",
        label: __("Territory"),
        fieldtype: "Link",
        options: "Territory"
    }
]
```

## Related Documentation

- [filter-fieldproperties.md](filter-fieldproperties.md) - Filter properties, defaults, validation, and advanced features
- [column-fieldtypes.md](column-fieldtypes.md) - Field types for report columns
- [script-report-examples.md](script-report-examples.md) - Complete working examples
