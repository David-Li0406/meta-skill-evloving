# Column Field Properties Reference

Complete guide to column properties, formatting options, and advanced features in Frappe reports.

## Dictionary Format Properties

When defining columns in dictionary format, you can specify these properties:

```python
{
    "label": "Display Label",          # Required: Column header text
    "fieldname": "field_name",         # Required: Internal field identifier
    "fieldtype": "Data",               # Required: Field type
    "options": "DocType",              # Configuration specific to field type (see below)
    "width": 150,                      # Column width in pixels
    "precision": 2,                    # Decimal places for numeric types
    "convertible": "qty",              # For currency conversion
    "no_total": 1                      # Exclude from totals row
}
```

### The "options" Property

The `options` property is used differently depending on the field type:

**Link Fields:**
- Target DocType name
- Example: `"options": "Customer"`

**Dynamic Link Fields:**
- Field name containing the DocType name
- Example: `"options": "reference_type"` (where reference_type field contains "Customer", "Supplier", etc.)

**Select Fields:**
- Newline-separated string of choices
- Example: `"options": "Draft\nSubmitted\nCancelled"`

**Currency Fields:**
- Field name containing the Currency link field
- Example: `"options": "currency"` (references a "currency" field that links to Currency DocType)

**Code Fields:**
- Programming language for syntax highlighting
- Example: `"options": "Python"` or `"JavaScript"`, `"HTML"`, `"CSS"`, `"JSON"`

**Data Fields:**
- Data type specification (rarely used in reports)
- Example: `"options": "Email"` or `"Phone"`, `"URL"`, `"Barcode"`, `"IBAN"`

## Column Width Guidelines

Recommended widths for different content types:

| Content Type | Width (px) | Use For |
|--------------|------------|---------|
| ID/Code | 80-120 | Document names, codes, short identifiers |
| Short Text | 100-150 | Status, type, category, flags |
| Medium Text | 150-200 | Names, titles, labels |
| Long Text | 200-300 | Descriptions, addresses, notes |
| Date | 80-100 | Dates without time |
| Datetime | 140-160 | Dates with time |
| Time | 80-100 | Time values |
| Duration | 80-100 | Time durations |
| Currency | 100-120 | Monetary values |
| Quantity | 60-80 | Numbers, counts |
| Percentage | 60-80 | Percentages |
| Check | 40-60 | Checkboxes |
| Link | Same as text | Depends on content length |
| Attach/Files | 150-200 | File links |
| Image | 80-120 | Image thumbnails |
| Phone | 120-150 | Phone numbers |
| Barcode | 100-120 | Barcode values |
| Rating | 100-120 | Star ratings |
| Color | 60-80 | Color indicators |
| Icon | 40-60 | Icons |

## Formatting Options

### Options Property Examples

**Link Field with Options:**
```python
{
    "label": "Customer",
    "fieldname": "customer",
    "fieldtype": "Link",
    "options": "Customer",  # Target DocType
    "width": 150
}
```

**Dynamic Link with Options:**
```python
# First, a field specifying the DocType
{
    "label": "Reference Type",
    "fieldname": "reference_type",
    "fieldtype": "Link",
    "options": "DocType",
    "width": 120
},
# Then the dynamic link referencing it
{
    "label": "Reference Name",
    "fieldname": "reference_name",
    "fieldtype": "Dynamic Link",
    "options": "reference_type",  # Field containing the DocType
    "width": 150
}
```

**Select Field with Options:**
```python
{
    "label": "Status",
    "fieldname": "status",
    "fieldtype": "Select",
    "options": "Draft\nSubmitted\nCancelled",  # Newline-separated
    "width": 100
}
```

**Currency Field with Currency Reference:**
```python
# Currency reference field
{
    "label": "Currency",
    "fieldname": "currency",
    "fieldtype": "Link",
    "options": "Currency",
    "width": 80
},
# Currency amount using the reference
{
    "label": "Amount",
    "fieldname": "amount",
    "fieldtype": "Currency",
    "options": "currency",  # References the currency field
    "width": 120
}
```

**Code Field with Language:**
```python
{
    "label": "Script",
    "fieldname": "script",
    "fieldtype": "Code",
    "options": "Python",  # Syntax highlighting language
    "width": 300
}
```

**Data Field with Type (rarely used in reports):**
```python
{
    "label": "Email",
    "fieldname": "email",
    "fieldtype": "Data",
    "options": "Email",  # Validates email format
    "width": 150
}
```

### Precision for Numeric Fields

Control decimal places for Float, Currency, Percent:

```python
{
    "label": "Rate",
    "fieldname": "rate",
    "fieldtype": "Float",
    "precision": 3  # Shows 3 decimal places
}
```

**Default precision:**
- Float: 2 decimal places
- Currency: Based on currency (usually 2)
- Percent: 2 decimal places

### Currency Conversion

Enable multi-currency conversion:

```python
{
    "label": "Amount",
    "fieldname": "amount",
    "fieldtype": "Currency",
    "options": "currency",  # Field containing currency code
    "convertible": "qty"  # Field to use for conversion
}
```

This allows reports to display amounts in different currencies and convert them to a base currency.

### Column Alignment

**Automatic alignment:**

Right-aligned (numeric types):
- Int, Long Int, Float, Currency, Percent
- Date, Time, Datetime

Left-aligned (text types):
- Data, Text, Small Text, Long Text
- Code, Password, Read Only
- Link, Dynamic Link, Select
- Attach, Attach Image, Phone
- All other text-based types

### Totals Row

For numeric columns, totals are automatically calculated if `add_total_row: 1` is set in the report JSON.

**Exclude specific columns from totals:**

```python
{
    "label": "ID",
    "fieldname": "id",
    "fieldtype": "Int",
    "width": 80,
    "no_total": 1  # Exclude from totals
}
```

**Applies to:**
- Int, Long Int, Float, Currency, Percent
- Any column where summing values makes sense

## Advanced Column Features

### Conditional Formatting

Use formatter in JavaScript file to apply custom styling:

```javascript
frappe.query_reports["My Report"] = {
    filters: [...],
    
    formatter: function(value, row, column, data, default_formatter) {
        // Apply default formatting first
        value = default_formatter(value, row, column, data);
        
        // Custom formatting based on conditions
        if (column.fieldname == "status") {
            if (value == "Completed") {
                value = `<span style="color: green;">${value}</span>`;
            } else if (value == "Cancelled") {
                value = `<span style="color: red;">${value}</span>`;
            }
        }
        
        // Highlight high amounts
        if (column.fieldname == "amount" && data && data.amount > 10000) {
            value = `<span style="background-color: #fffacd; padding: 2px 5px;">${value}</span>`;
        }
        
        return value;
    }
};
```

### Custom Cell Rendering

Create custom HTML for specific columns:

```javascript
formatter: function(value, row, column, data, default_formatter) {
    if (column.fieldname == "custom_column") {
        // Custom HTML
        return `<button onclick="myFunction('${data.name}')">Click</button>`;
    }
    
    // Progress bar example
    if (column.fieldname == "completion") {
        let percent = parseFloat(value) || 0;
        let color = percent >= 75 ? "green" : percent >= 50 ? "orange" : "red";
        
        return `
            <div style="display: flex; align-items: center;">
                <div style="flex: 1; height: 20px; background-color: #f0f0f0; border-radius: 3px; overflow: hidden;">
                    <div style="width: ${percent}%; height: 100%; background-color: ${color};"></div>
                </div>
                <span style="margin-left: 10px; font-weight: bold;">${percent}%</span>
            </div>
        `;
    }
    
    return default_formatter(value, row, column, data);
}
```

### Dynamic Column Width

Columns can adjust width based on content, but it's better to specify explicit widths for consistency:

```python
# Variable width based on content
"Name:Data"  # No width specified, uses auto-sizing

# Fixed width for consistency
"Name:Data:150"  # Better for report readability
```

## Common Patterns

### Standard Report Columns

```python
# Basic document info
"ID:Link/DocType:120",
"Name:Data:150",
"Status:Data:100",
"Created:Datetime:150",
"Modified:Datetime:150",
"Owner:Link/User:150"
```

### Financial Report Columns

```python
columns = [
    "Account:Link/Account:200",
    "Debit:Currency:120",
    "Credit:Currency:120",
    "Balance:Currency:120"
]
```

### Multi-Currency Report

```python
columns = [
    "Invoice:Link/Sales Invoice:150",
    {
        "label": "Currency",
        "fieldname": "currency",
        "fieldtype": "Link",
        "options": "Currency",
        "width": 80
    },
    {
        "label": "Amount",
        "fieldname": "amount",
        "fieldtype": "Currency",
        "options": "currency",  # Link to currency field
        "width": 120
    },
    {
        "label": "Amount (Base)",
        "fieldname": "base_amount",
        "fieldtype": "Currency",
        "width": 120
    }
]
```

### Time-Based Report

```python
columns = [
    "Task:Link/Task:150",
    "Start:Datetime:150",
    "End:Datetime:150",
    "Duration:Duration:100",
    "Completed:Check:80"
]
```

### Status with Color Coding

Use formatter to add color indicators:

```javascript
formatter: function(value, row, column, data, default_formatter) {
    value = default_formatter(value, row, column, data);
    
    if (column.fieldname === "status") {
        let color_map = {
            "Open": "blue",
            "In Progress": "orange",
            "Completed": "green",
            "Cancelled": "red"
        };
        
        let color = color_map[value] || "gray";
        return `<span class="indicator-pill ${color}">${value}</span>`;
    }
    
    return value;
}
```

## Best Practices

### Width Selection

1. **Be consistent**: Use similar widths for similar content types across reports
2. **Consider content**: Allow enough space for typical values plus some padding
3. **Mobile-friendly**: Wider columns may not fit on mobile screens
4. **Essential first**: Put most important columns on the left with appropriate width

### Precision Settings

1. **Match business needs**: Use 2 decimals for currency, 3-4 for technical measurements
2. **Be consistent**: Use same precision for similar fields across reports
3. **Performance**: Higher precision doesn't impact performance, it's display-only

### Formatting

1. **Use default formatter**: Always call `default_formatter` first for consistent base formatting
2. **Progressive enhancement**: Add custom formatting on top of defaults
3. **Accessibility**: Ensure color coding is not the only indicator (use icons, text)
4. **Performance**: Keep formatter function lightweight for large datasets

### Alignment

1. **Respect defaults**: Don't override natural alignment unless necessary
2. **Numeric right**: Keep numeric data right-aligned for easy comparison
3. **Text left**: Keep text left-aligned for readability

## Translation Support

Always wrap column labels in translation function:

```python
from frappe import _

columns = [
    _("Name") + ":Data:150",
    _("Amount") + ":Currency:120"
]

# Or for dict format
columns = [
    {
        "label": _("Name"),
        "fieldname": "name",
        "fieldtype": "Data",
        "width": 150
    }
]
```

**For JavaScript:**
```javascript
{
    fieldname: "status",
    label: __("Status"),  // Translated
    fieldtype: "Data",
    width: 100
}
```

## Performance Considerations

### Large Datasets

For reports with thousands of rows:

1. **Limit columns**: Only include necessary columns
2. **Simplify formatters**: Keep formatter logic minimal
3. **Avoid inline HTML**: Minimize HTML generation in formatters
4. **Use pagination**: Implement server-side pagination for very large datasets

### Column Count

- **Optimal**: 5-10 columns for best readability
- **Maximum**: 15-20 columns before horizontal scrolling becomes problematic
- **Mobile**: Limit to 3-5 columns for mobile views

## Debugging Column Issues

### Column not displaying

- Check fieldname spelling in data
- Verify fieldtype is valid
- Ensure data matches column order (for list format)

### Wrong formatting

- Check fieldtype matches data type
- Verify precision is set correctly for numeric types
- Check for conflicting custom formatters

### Alignment issues

- Verify fieldtype is correct (numeric vs text)
- Check for custom CSS that might override defaults
- Ensure no extra spaces in fieldname or data
