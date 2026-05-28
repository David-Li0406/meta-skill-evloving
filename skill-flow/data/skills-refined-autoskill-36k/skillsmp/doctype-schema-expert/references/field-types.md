# Field Types Reference

Complete guide to all Frappe field types with descriptions, use cases, and examples.

## Data Storage Field Types

These fields store actual data in the database.

### Text Fields

#### Data
- **Type**: Short text input (up to 140 characters by default)
- **Use Cases**: Names, titles, short identifiers
- **Options**: Can specify type via `options` field ("Email", "Name", "Phone", "URL", "Barcode", "IBAN")
- **Example**: Customer name, email address, phone number

```json
{
  "fieldname": "customer_name",
  "fieldtype": "Data",
  "label": "Customer Name",
  "length": 200
}
```

#### Small Text
- **Type**: Multi-line text input (stored as VARCHAR/TEXT)
- **Use Cases**: Short descriptions, notes, addresses
- **Translatable**: Yes (if `translatable: 1`)
- **Example**: Shipping address, brief description

#### Text
- **Type**: Large text input (stored as TEXT)
- **Use Cases**: Long descriptions, comments, notes
- **Translatable**: Yes (if `translatable: 1`)
- **Example**: Product description, comments

#### Long Text
- **Type**: Very large text input (stored as LONGTEXT)
- **Use Cases**: Very long content, articles
- **Example**: Blog post content, detailed documentation

#### Code
- **Type**: Code editor with syntax highlighting
- **Options**: Specify language ("Python", "JavaScript", "HTML", "CSS", "JSON", etc.)
- **Use Cases**: Code snippets, scripts, JSON data
- **Example**: Custom script, API response

```json
{
  "fieldname": "custom_script",
  "fieldtype": "Code",
  "label": "Custom Script",
  "options": "Python"
}
```

#### Text Editor
- **Type**: Rich text editor (TinyMCE)
- **Use Cases**: Formatted content, HTML emails
- **Translatable**: Yes (if `translatable: 1`)
- **Example**: Email content, formatted descriptions

#### HTML Editor
- **Type**: Rich text editor with HTML source
- **Use Cases**: HTML content, formatted documents
- **Example**: Website content, newsletters

#### Markdown Editor
- **Type**: Markdown editor with preview
- **Use Cases**: Documentation, formatted text
- **Example**: README files, help documentation

#### Password
- **Type**: Encrypted password field
- **Use Cases**: Passwords, sensitive text
- **Security**: Automatically encrypted in database
- **Example**: User password, API key

### Numeric Fields

#### Int
- **Type**: Integer number
- **Range**: -2147483648 to 2147483647
- **Use Cases**: Quantities, counts, IDs
- **Properties**: `non_negative` to restrict to positive numbers
- **Example**: Quantity, age, count

```json
{
  "fieldname": "quantity",
  "fieldtype": "Int",
  "label": "Quantity",
  "non_negative": 1,
  "default": "1"
}
```

#### Long Int
- **Type**: Large integer number
- **Range**: -9223372036854775808 to 9223372036854775807
- **Use Cases**: Large IDs, big counts
- **Example**: Transaction ID, large quantity

#### Float
- **Type**: Decimal number
- **Precision**: Configurable (0-9 decimal places)
- **Use Cases**: Measurements, ratios, rates
- **Properties**: `precision`, `non_negative`
- **Example**: Weight, dimensions, temperature

```json
{
  "fieldname": "weight",
  "fieldtype": "Float",
  "label": "Weight (kg)",
  "precision": "3",
  "non_negative": 1
}
```

#### Currency
- **Type**: Monetary value
- **Display**: Formatted with currency symbol
- **Precision**: Configurable (default based on currency)
- **Options**: Should point to a field that links to a Currency DocType (e.g., `"currency"`)
- **Use Cases**: Prices, amounts, costs
- **Example**: Total amount, unit price

```json
{
  "fieldname": "currency",
  "fieldtype": "Link",
  "label": "Currency",
  "options": "Currency"
},
{
  "fieldname": "total_amount",
  "fieldtype": "Currency",
  "label": "Total Amount",
  "options": "currency"
}
```

#### Percent
- **Type**: Percentage value
- **Display**: Formatted with % symbol
- **Precision**: Configurable
- **Use Cases**: Discounts, rates, percentages
- **Example**: Tax rate, discount percentage

### Date and Time Fields

#### Date
- **Type**: Date only (no time)
- **Format**: YYYY-MM-DD
- **Use Cases**: Dates, deadlines
- **Example**: Birth date, due date, posting date

#### Datetime
- **Type**: Date and time
- **Format**: YYYY-MM-DD HH:MM:SS
- **Use Cases**: Timestamps, schedules
- **Example**: Event time, transaction timestamp

#### Time
- **Type**: Time only (no date)
- **Format**: HH:MM:SS
- **Use Cases**: Time of day, duration
- **Example**: Start time, closing time

#### Duration
- **Type**: Time duration
- **Format**: HH:MM:SS or configurable
- **Properties**: `hide_days`, `hide_seconds`
- **Use Cases**: Task duration, elapsed time
- **Example**: Work hours, video length

### Relationship Fields

#### Link
- **Type**: Foreign key reference to another DocType
- **Options**: Target DocType name (required)
- **Use Cases**: References to other documents
- **Properties**: `ignore_user_permissions`, `remember_last_selected_value`
- **Example**: Customer, Item, Project reference

```json
{
  "fieldname": "customer",
  "fieldtype": "Link",
  "label": "Customer",
  "options": "Customer",
  "reqd": 1
}
```

#### Dynamic Link
- **Type**: Foreign key where target DocType is dynamic
- **Options**: Field name containing the DocType name
- **Use Cases**: Generic references, polymorphic relationships
- **Example**: Reference that can point to Customer OR Supplier

```json
{
  "fieldname": "party_type",
  "fieldtype": "Link",
  "label": "Party Type",
  "options": "DocType"
},
{
  "fieldname": "party",
  "fieldtype": "Dynamic Link",
  "label": "Party",
  "options": "party_type"
}
```

#### Table
- **Type**: One-to-many relationship (child table)
- **Options**: Child DocType name (must have `istable: 1`)
- **Use Cases**: Line items, multiple values
- **Example**: Invoice items, contact details

```json
{
  "fieldname": "items",
  "fieldtype": "Table",
  "label": "Items",
  "options": "Sales Order Item"
}
```

#### Table MultiSelect
- **Type**: Multiple selection from child table
- **Options**: Child DocType name
- **Use Cases**: Multiple selections with display
- **Example**: Selected items, categories

### Selection and Boolean Fields

#### Select
- **Type**: Dropdown/Select field
- **Options**: Newline-separated list of options
- **Use Cases**: Status, categories, predefined choices
- **Properties**: `sort_options` to sort alphabetically
- **Example**: Status, priority, category

```json
{
  "fieldname": "status",
  "fieldtype": "Select",
  "label": "Status",
  "options": "Draft\nOpen\nPending\nCompleted\nCancelled",
  "default": "Draft"
}
```

#### Check
- **Type**: Boolean checkbox
- **Values**: 0 or 1
- **Use Cases**: Yes/No, enabled/disabled flags
- **Example**: Is active, allow discount

```json
{
  "fieldname": "is_active",
  "fieldtype": "Check",
  "label": "Is Active",
  "default": "1"
}
```

#### Autocomplete
- **Type**: Text input with autocomplete suggestions
- **Options**: Newline-separated list of suggestions
- **Use Cases**: Text with common values
- **Example**: City, occupation

### Special Purpose Fields

#### Attach
- **Type**: File upload
- **Storage**: Stores file path
- **Use Cases**: Document attachments
- **Properties**: `make_attachment_public`
- **Example**: Invoice PDF, image file

#### Attach Image
- **Type**: Image upload with preview
- **Storage**: Stores image path
- **Use Cases**: Product images, user photos
- **Example**: Product image, profile picture

#### Signature
- **Type**: Digital signature capture
- **Storage**: Stores signature as image
- **Use Cases**: Approvals, signatures
- **Example**: Customer signature, approval signature

#### Color
- **Type**: Color picker
- **Storage**: Stores hex color code
- **Use Cases**: Theme colors, category colors
- **Example**: Status color, category color

#### Barcode
- **Type**: Barcode input/scanner
- **Storage**: Stores barcode value
- **Use Cases**: Product barcodes, asset tracking
- **Example**: Product barcode, serial number

#### Rating
- **Type**: Star rating input
- **Range**: 0-5 stars
- **Use Cases**: Ratings, reviews
- **Example**: Product rating, service rating

#### Geolocation
- **Type**: Latitude/longitude coordinates
- **Storage**: Stores JSON with coordinates
- **Use Cases**: Location tracking, maps
- **Example**: Store location, delivery address

#### JSON
- **Type**: JSON data field
- **Storage**: Stores JSON object
- **Use Cases**: Structured data, API responses
- **Example**: API response, configuration object

#### Read Only
- **Type**: Computed/display-only field
- **Use Cases**: Calculated values, fetched data
- **Example**: Total amount, computed status

#### Phone
- **Type**: Phone number field with validation
- **Storage**: Stores phone number
- **Use Cases**: Contact numbers
- **Example**: Mobile number, office phone

#### Icon
- **Type**: Icon picker
- **Storage**: Stores icon name
- **Use Cases**: Visual indicators
- **Example**: DocType icon, status icon

## Layout Field Types

These fields control form layout and don't store data.

### Section Break
- **Purpose**: Start new section in form
- **Properties**: `label`, `collapsible`, `collapsible_depends_on`, `hide_border`
- **Use Cases**: Group related fields
- **Example**: "Contact Details" section

```json
{
  "fieldname": "contact_section",
  "fieldtype": "Section Break",
  "label": "Contact Details",
  "collapsible": 1
}
```

### Column Break
- **Purpose**: Start new column in current section
- **Use Cases**: Multi-column layouts
- **Example**: Split form into two columns

### Tab Break
- **Purpose**: Create tabbed interface
- **Properties**: `label`, `show_dashboard`
- **Use Cases**: Organize complex forms
- **Example**: "Details" tab, "Settings" tab

```json
{
  "fieldname": "settings_tab",
  "fieldtype": "Tab Break",
  "label": "Settings"
}
```

### HTML
- **Purpose**: Display custom HTML content
- **Options**: HTML content to display
- **Use Cases**: Instructions, messages, custom UI
- **Example**: Help text, warnings

```json
{
  "fieldname": "html_help",
  "fieldtype": "HTML",
  "options": "<p>Fill in all required fields</p>"
}
```

### Button
- **Purpose**: Custom action button
- **Options**: JavaScript function to call
- **Use Cases**: Custom actions
- **Example**: Calculate total, fetch data

### Image
- **Purpose**: Display static image
- **Options**: Image URL or path
- **Use Cases**: Logos, illustrations
- **Example**: Company logo, help image

### Fold
- **Purpose**: Collapsible section
- **Use Cases**: Hide advanced options
- **Example**: Advanced settings

### Heading
- **Purpose**: Section heading
- **Use Cases**: Visual organization
- **Example**: "Basic Information" heading

## Field Type Selection Guide

| Use Case | Recommended Field Type |
|----------|----------------------|
| Short text (name, title) | Data |
| Email address | Data with options: "Email" |
| Phone number | Phone or Data with options: "Phone" |
| URL | Data with options: "URL" |
| Multi-line text | Small Text or Text |
| Rich formatted text | Text Editor or HTML Editor |
| Code/JSON | Code with appropriate options |
| Whole number | Int (with non_negative if needed) |
| Decimal number | Float with precision |
| Money amount | Currency |
| Percentage | Percent |
| Date | Date |
| Date and time | Datetime |
| Duration | Duration |
| Yes/No flag | Check |
| Predefined options | Select |
| Reference to another doc | Link |
| Multiple selections | Table MultiSelect |
| Child records | Table |
| File attachment | Attach or Attach Image |
| Color selection | Color |
| Star rating | Rating |
| Location | Geolocation |
| Signature | Signature |
| Password | Password |

## Properties Available by Field Type

| Property | Applicable Field Types |
|----------|----------------------|
| `length` | Data, Link, Dynamic Link, Password, Select, Read Only |
| `precision` | Float, Currency, Percent |
| `non_negative` | Int, Float, Currency |
| `unique` | Most data fields |
| `options` | Link, Dynamic Link, Select, Code, Data |
| `default` | All data fields |
| `reqd` | All data fields |
| `read_only` | All data fields |
| `hidden` | All fields |
| `depends_on` | All fields |
| `mandatory_depends_on` | All data fields |
| `read_only_depends_on` | All data fields |
| `fetch_from` | Data fields (when linked to another doc) |
| `in_list_view` | All data fields |
| `in_standard_filter` | All data fields |
| `in_global_search` | Text, Data, Select, Link fields |
| `search_index` | Most data fields |
