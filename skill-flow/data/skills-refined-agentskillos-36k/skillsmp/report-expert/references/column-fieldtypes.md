# Column Fieldtypes Reference

Complete reference for all available column fieldtypes in Frappe reports.

## Overview

Columns in Frappe reports can use the same field types as DocType fields (excluding layout-only types like Section Break, Column Break, etc.). This document lists all data field types usable in report columns.

## String Format

Columns can be defined using a compact string format:

```
"Label:Fieldtype/Options:Width"
```

Examples:
```python
"Name:Data:150"
"Amount:Currency:120"
"Customer:Link/Customer:200"
"Is Active:Check:80"
```

## Dictionary Format

More detailed format with all options:

```python
{
    "label": "Display Label",
    "fieldname": "field_name",
    "fieldtype": "Data",
    "options": "Configuration",  # Usage varies by fieldtype - see below
    "width": 150,
    "precision": 2,  # For numeric types
    "convertible": "qty"  # For currency conversion
}
```

**The "options" property usage varies by field type:**
- **Link**: Target DocType name (e.g., `"Customer"`)
- **Dynamic Link**: Field name containing the DocType (e.g., `"reference_type"`)
- **Select**: Newline-separated choices (e.g., `"Draft\nSubmitted\nCancelled"`)
- **Currency**: Field name with Currency link (e.g., `"currency"`)
- **Code**: Language for syntax highlighting (e.g., `"Python"`, `"JavaScript"`)
- **Data**: Data type specification (e.g., `"Email"`, `"Phone"`, `"URL"`)

See [column-fieldproperties.md](column-fieldproperties.md) for detailed property documentation and examples.

## Available Fieldtypes

### Text Types

**Data**
- Single-line text
- Default width: 100-150px
- Example: `"Name:Data:150"`

**Text**
- Multi-line text (shows truncated in report)
- Default width: 200px
- Example: `"Description:Text:200"`

**Small Text**
- Medium-length text
- Default width: 150px
- Example: `"Notes:Small Text:150"`

**Long Text**
- Long text fields
- Similar to Text in reports
- Example: `"Content:Long Text:200"`

**Text Editor**
- Rich text/HTML content (displays as text in reports)
- Default width: 200px
- Example: `"Description:Text Editor:200"`

**HTML Editor**
- HTML formatted content (displays as text in reports)
- Default width: 200px
- Example: `"Content:HTML Editor:200"`

**Markdown Editor**
- Markdown formatted content (displays as text in reports)
- Default width: 200px
- Example: `"Notes:Markdown Editor:200"`

**Code**
- For code snippets or formatted text
- Displays in monospace font
- Example: `"Script:Code:200"`

**Password**
- Encrypted/masked text field
- Displays as masked in reports
- Example: `"API Key:Password:150"`

**Read Only**
- Display-only computed field
- Example: `"Status:Read Only:100"`

### Numeric Types

**Int**
- Integer numbers
- Right-aligned
- Example: `"Quantity:Int:80"`

**Long Int**
- Large integer numbers
- Right-aligned
- Example: `"Transaction ID:Long Int:100"`

**Float**
- Decimal numbers
- Right-aligned
- Supports precision
- Example: `"Rate:Float:100"`

**Currency**
- Monetary values
- Formatted with currency symbol
- Right-aligned
- Example: `"Amount:Currency:120"`

**Percent**
- Percentage values
- Displays with % symbol
- Example: `"Discount:Percent:80"`

### Date and Time Types

**Date**
- Date only (YYYY-MM-DD)
- Formatted based on user settings
- Example: `"Posting Date:Date:100"`

**Datetime**
- Date and time
- Formatted with time zone
- Example: `"Created On:Datetime:150"`

**Time**
- Time only (HH:MM:SS)
- Example: `"Start Time:Time:80"`

**Duration**
- Time duration (formatted as HH:MM:SS)
- Example: `"Duration:Duration:100"`

### Link Types

**Link**
- Reference to another DocType
- Clickable link to document
- Requires `options` parameter
- Example: `"Customer:Link/Customer:150"`

**Dynamic Link**
- Link determined by another field
- Example: `"Reference:Dynamic Link:150"`

### Boolean Type

**Check**
- Checkbox (0 or 1)
- Shows checkmark icon
- Example: `"Is Active:Check:80"`

### Selection Type

**Select**
- Dropdown selection
- Shows selected value
- Example: `"Status:Select:100"`

### Special Types

**Attach**
- File attachment field
- Shows file link in report
- Example: `"Document:Attach:150"`

**Attach Image**
- Image attachment with thumbnail
- Shows image preview in report
- Example: `"Photo:Attach Image:100"`

**Signature**
- Digital signature field
- Shows signature image in report
- Example: `"Signature:Signature:120"`

**Barcode**
- Barcode value field
- Example: `"Product Code:Barcode:120"`

**Phone**
- Phone number field with formatting
- Example: `"Contact:Phone:120"`

**Geolocation**
- Latitude/longitude coordinates
- Example: `"Location:Geolocation:150"`

**JSON**
- JSON data field
- Displays as formatted JSON in report
- Example: `"Metadata:JSON:200"`

**Autocomplete**
- Text field with autocomplete suggestions
- Example: `"City:Autocomplete:120"`

**Icon**
- Display icon
- Example: `"Icon:Icon:50"`

**Color**
- Color picker value
- Shows color block
- Example: `"Color:Color:80"`

**Rating**
- Star rating display
- Example: `"Rating:Rating:100"`

**Image**
- Display image thumbnail
- Shows image from URL or field
- Example: `"Photo:Image:100"`

**Button**
- Custom button in cell
- Requires client-side handler
- Example: `"Actions:Button:80"`
- Note: Primarily for custom interactive reports

**HTML**
- Raw HTML content for display
- Use with caution (XSS risk)
- Note: Different from HTML Editor fieldtype
- Example: `"Content:HTML:200"`

## Field Type Categories

**Text Fields:**
Data, Text, Small Text, Long Text, Text Editor, HTML Editor, Markdown Editor, Code, Password, Read Only

**Numeric Fields:**
Int, Long Int, Float, Currency, Percent

**Date/Time Fields:**
Date, Datetime, Time, Duration

**Relationship Fields:**
Link, Dynamic Link

**Boolean/Selection:**
Check, Select

**Attachment Fields:**
Attach, Attach Image, Signature

**Special Purpose:**
Barcode, Phone, Geolocation, JSON, Autocomplete, Icon, Color, Rating, Image, Button, HTML

## Quick Reference Table

| Fieldtype | Use For | Width Range |
|-----------|---------|-------------|
| Data | Short text, names | 100-150 |
| Text | Long text, descriptions | 200-300 |
| Int | Whole numbers | 60-80 |
| Float | Decimal numbers | 80-120 |
| Currency | Money amounts | 100-120 |
| Percent | Percentages | 60-80 |
| Date | Dates | 80-100 |
| Datetime | Date with time | 140-160 |
| Link | Reference to document | 150-200 |
| Check | Boolean yes/no | 40-60 |
| Select | Dropdown values | 100-150 |
| Attach | File links | 150-200 |
| Phone | Phone numbers | 120-150 |
| Rating | Star ratings | 100-120 |

## Common Examples

### Basic Report
```python
columns = [
    "Name:Data:150",
    "Status:Select:100",
    "Amount:Currency:120",
    "Date:Date:100"
]
```

### Financial Report
```python
columns = [
    "Account:Link/Account:200",
    "Debit:Currency:120",
    "Credit:Currency:120",
    "Balance:Currency:120"
]
```

### Inventory Report
```python
columns = [
    "Item:Link/Item:200",
    "Warehouse:Link/Warehouse:150",
    "Quantity:Float:100",
    "Value:Currency:120",
    "Last Updated:Datetime:150"
]
```

### Contact Report
```python
columns = [
    "Name:Data:150",
    "Phone:Phone:120",
    "Email:Data:150",
    "Rating:Rating:100",
    "Active:Check:60"
]
```

## Related Documentation

- [column-fieldproperties.md](column-fieldproperties.md) - Column properties, widths, formatting, and advanced features
- [filter-fieldtypes.md](filter-fieldtypes.md) - Field types for report filters
- [script-report-examples.md](script-report-examples.md) - Complete working examples
