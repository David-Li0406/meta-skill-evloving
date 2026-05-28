# Field Properties Reference

Complete reference for all properties that can be set on DocType fields.

## Essential Properties

### fieldname
- **Type**: String
- **Required**: Yes
- **Description**: Unique identifier for the field (becomes database column name)
- **Format**: snake_case (lowercase with underscores)
- **Rules**: 
  - Must start with letter
  - Only alphanumeric and underscore
  - Cannot be a SQL keyword
  - Maximum 64 characters
- **Example**: `customer_name`, `total_amount`, `is_active`

### fieldtype
- **Type**: String
- **Required**: Yes
- **Description**: Type of field (determines storage and UI)
- **Options**: See field-types.md for complete list
- **Example**: `"Data"`, `"Link"`, `"Date"`, `"Int"`

### label
- **Type**: String
- **Required**: Recommended
- **Description**: User-friendly display name
- **Format**: Any text (spaces allowed)
- **Default**: Auto-generated from fieldname if not provided
- **Example**: `"Customer Name"`, `"Total Amount"`, `"Is Active"`

## Data Validation Properties

### reqd
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Make field mandatory
- **Note**: Not applicable to layout fields (Section Break, Column Break, etc.)
- **Example**: `"reqd": 1`

### unique
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Ensure unique values across all documents
- **Use Cases**: IDs, email addresses, serial numbers
- **Note**: Creates unique database index

### set_only_once
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Field can only be set once (cannot be changed after save)
- **Use Cases**: Serial numbers, initial dates, reference numbers

### no_copy
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Don't copy value when duplicating document
- **Use Cases**: Dates, amounts that shouldn't be copied

### length
- **Type**: Int
- **Description**: Maximum length for text fields
- **Applicable**: Data, Link, Dynamic Link, Password, Select, Read Only
- **Default**: 140 for Data fields
- **Example**: `"length": 200`

### precision
- **Type**: Int (0-9) or String
- **Description**: Number of decimal places
- **Applicable**: Float, Currency, Percent
- **Default**: System default (usually 2 for Currency)
- **Example**: `"precision": "3"`

### non_negative
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Restrict to non-negative numbers
- **Applicable**: Int, Float, Currency
- **Example**: `"non_negative": 1`

## Default Values and Fetching

### default
- **Type**: String
- **Description**: Default value for new documents
- **Special Values**:
  - `"Today"`: Current date
  - `"Now"`: Current datetime
  - `"user"`: Current user
  - `"user_fullname"`: Current user's full name
  - Python expression starting with `":"` (e.g., `":frappe.session.user"`)
- **Example**: `"default": "Draft"`, `"default": "Today"`

### fetch_from
- **Type**: String
- **Description**: Auto-fetch value from linked document
- **Format**: `linked_field.target_field`
- **Use Cases**: Auto-fill customer details, item properties
- **Example**: `"fetch_from": "customer.customer_name"`

```json
{
  "fieldname": "customer",
  "fieldtype": "Link",
  "options": "Customer"
},
{
  "fieldname": "customer_name",
  "fieldtype": "Data",
  "fetch_from": "customer.customer_name",
  "fetch_if_empty": 1
}
```

### fetch_if_empty
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Only fetch if field is empty (otherwise always re-fetch)
- **Use Cases**: Allow manual override of fetched values

## Display and Visibility Properties

### hidden
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Hide field from form
- **Use Cases**: Backend-only fields, computed values
- **Note**: Still accessible via API and database

### read_only
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Make field read-only
- **Use Cases**: Computed values, system-generated fields

### bold
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Display label in bold
- **Use Cases**: Important fields

### in_list_view
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Show field in list view and grid
- **Note**: Limited to ~5 fields for best UX
- **Use Cases**: Key fields for identification

### in_standard_filter
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Add field to standard list filters
- **Use Cases**: Common filter fields (status, date, type)

### in_global_search
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Include field in global search
- **Applicable**: Data, Select, Table, Text, Link, Small Text, Long Text, Read Only

### in_preview
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Show in preview popup
- **Use Cases**: Key fields for quick preview

### in_filter
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Make field available for filtering
- **Use Cases**: Fields users might filter by

### show_on_timeline
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Show field changes in timeline
- **Depends on**: Field must be hidden
- **Use Cases**: Track important hidden fields

## Conditional Display

### depends_on
- **Type**: String (JavaScript expression)
- **Description**: Show field only when condition is true
- **Format**: `eval:expression` or just `fieldname`
- **Examples**:
  - `"depends_on": "eval:doc.status=='Active'"`
  - `"depends_on": "is_company"`
  - `"depends_on": "eval:doc.type=='Sales' && doc.status=='Open'"`

### mandatory_depends_on
- **Type**: String (JavaScript expression)
- **Description**: Make field mandatory when condition is true
- **Format**: Same as depends_on
- **Example**: `"mandatory_depends_on": "eval:doc.type=='Company'"`

### read_only_depends_on
- **Type**: String (JavaScript expression)
- **Description**: Make field read-only when condition is true
- **Format**: Same as depends_on
- **Example**: `"read_only_depends_on": "eval:doc.docstatus==1"`

## Search and Indexing

### search_index
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Create database index for faster searches
- **Use Cases**: Fields used in WHERE clauses, frequently filtered fields
- **Note**: Improves query performance but increases write time

## Link Field Properties

### options
- **Type**: String
- **Description**: Configuration specific to field type
- **Usage by Field Type**:
  - **Link**: Target DocType name (e.g., `"Customer"`)
  - **Dynamic Link**: Field containing DocType name
  - **Select**: Newline-separated options
  - **Code**: Programming language (e.g., `"Python"`, `"JavaScript"`)
  - **Data**: Data type (e.g., `"Email"`, `"Phone"`, `"URL"`)
  - **Table**: Child DocType name
  - **Currency**: Field name containing the Currency link field (e.g., `"currency"`)

```json
// Link field
{
  "fieldname": "customer",
  "fieldtype": "Link",
  "options": "Customer"
}

// Currency field with currency reference
{
  "fieldname": "currency",
  "fieldtype": "Link",
  "label": "Currency",
  "options": "Currency"
},
{
  "fieldname": "total",
  "fieldtype": "Currency",
  "label": "Total",
  "options": "currency"
}

// Select field
{
  "fieldname": "status",
  "fieldtype": "Select",
  "options": "Draft\nOpen\nClosed"
}

// Code field
{
  "fieldname": "script",
  "fieldtype": "Code",
  "options": "Python"
}
```

### ignore_user_permissions
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Bypass user permission restrictions on link field
- **Applicable**: Link fields
- **Use Cases**: System-level references, administrative fields

### remember_last_selected_value
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Remember last selected value for new documents
- **Applicable**: Link fields
- **Use Cases**: Frequently used selections

### link_filters
- **Type**: JSON String
- **Description**: Filter options in link field dropdown
- **Format**: JSON object with filter conditions
- **Example**: 
```json
{
  "fieldname": "customer",
  "fieldtype": "Link",
  "options": "Customer",
  "link_filters": "[[\"Customer\",\"customer_type\",\"=\",\"Company\"]]"
}
```

### sort_options
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Sort select options alphabetically
- **Applicable**: Select fields

## Print and Report Properties

### print_hide
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Hide field in print view
- **Use Cases**: Internal fields not needed in print

### print_hide_if_no_value
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Hide field in print if value is empty
- **Applicable**: Int, Float, Currency, Percent

### print_width
- **Type**: String
- **Description**: Width in print view (e.g., "50px", "10%")

### report_hide
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Hide field in report builder

## Grid and Table Properties

### columns
- **Type**: Int
- **Description**: Number of columns in list/grid view
- **Range**: 1-11 (total columns should be ≤ 11)
- **Use Cases**: Control column width in grid

### allow_bulk_edit
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Allow bulk editing in child table
- **Applicable**: Table fields

### allow_in_quick_entry
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Include field in quick entry dialog

## Permission Properties

### permlevel
- **Type**: Int
- **Default**: 0
- **Description**: Permission level (0-9)
- **Use Cases**: Restrict access to sensitive fields
- **Note**: User needs role permission for that permlevel

### allow_on_submit
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Allow editing after document submission
- **Applicable**: When parent DocType is submittable
- **Use Cases**: Status updates, comments on submitted docs

### ignore_xss_filter
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Disable XSS filtering for field
- **Security**: Use with extreme caution!
- **Use Cases**: Intentional HTML content, trusted sources only

## Display Format Properties

### width
- **Type**: String
- **Description**: Width in form view (e.g., "50%", "200px")

### max_height
- **Type**: String
- **Description**: Maximum height for text fields (e.g., "3rem")
- **Use Cases**: Limit height of text editors

### placeholder
- **Type**: String
- **Description**: Placeholder text in empty field
- **Example**: `"placeholder": "Enter customer name"`

### description
- **Type**: String
- **Description**: Help text shown below field
- **Format**: Plain text or markdown
- **Example**: `"description": "Select the customer for this order"`

### documentation_url
- **Type**: String
- **Description**: URL to documentation
- **Display**: Help icon next to field
- **Example**: `"documentation_url": "https://docs.example.com/fields/customer"`

## Translatable Content

### translatable
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Mark field content as translatable
- **Applicable**: Data, Select, Text, Small Text, Text Editor
- **Use Cases**: Multi-language support

## Special Properties

### is_virtual
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Virtual field (not stored in database)
- **Use Cases**: Computed fields, display-only fields

### show_dashboard
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Show dashboard in tab
- **Applicable**: Tab Break

### hide_days
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Hide days in duration display
- **Applicable**: Duration fields

### hide_seconds
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Hide seconds in duration display
- **Applicable**: Duration fields

### hide_border
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Hide section break border
- **Applicable**: Section Break

### collapsible
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Make section collapsible
- **Applicable**: Section Break

### collapsible_depends_on
- **Type**: String (JavaScript expression)
- **Description**: Condition for section to be collapsible
- **Applicable**: Section Break with collapsible=1

### make_attachment_public
- **Type**: Int (0 or 1)
- **Default**: 0
- **Description**: Make uploaded files publicly accessible
- **Applicable**: Attach, Attach Image

## Legacy Properties

### oldfieldname
- **Type**: String
- **Description**: Previous field name (for migration tracking)

### oldfieldtype
- **Type**: String
- **Description**: Previous field type (for migration tracking)

## Property Combinations

### Common Patterns

**Required field with default:**
```json
{
  "fieldname": "status",
  "fieldtype": "Select",
  "label": "Status",
  "options": "Open\nClosed",
  "default": "Open",
  "reqd": 1
}
```

**Linked field with auto-fetch:**
```json
{
  "fieldname": "customer",
  "fieldtype": "Link",
  "label": "Customer",
  "options": "Customer",
  "reqd": 1
},
{
  "fieldname": "customer_name",
  "fieldtype": "Data",
  "label": "Customer Name",
  "fetch_from": "customer.customer_name",
  "read_only": 1
}
```

**Conditional mandatory field:**
```json
{
  "fieldname": "company_registration",
  "fieldtype": "Data",
  "label": "Company Registration",
  "mandatory_depends_on": "eval:doc.customer_type=='Company'"
}
```

**Hidden indexed field:**
```json
{
  "fieldname": "search_key",
  "fieldtype": "Data",
  "label": "Search Key",
  "hidden": 1,
  "search_index": 1
}
```

**List view field with filter:**
```json
{
  "fieldname": "status",
  "fieldtype": "Select",
  "label": "Status",
  "options": "Active\nInactive",
  "in_list_view": 1,
  "in_standard_filter": 1,
  "in_filter": 1
}
```
