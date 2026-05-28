# Naming Conventions

Standard naming conventions for Frappe DocTypes and fields.

## DocType Names

### Format
- **Convention**: PascalCase with spaces allowed
- **Examples**: 
  - Good: `"Sales Order"`, `"Customer"`, `"Item Price"`
  - Avoid: `"sales_order"`, `"salesOrder"`, `"SALES ORDER"`

### Rules
- Start with capital letter
- Use meaningful, descriptive names
- Singular nouns for standard doctypes (e.g., "Customer", not "Customers")
- Plural only for collection doctypes (e.g., "Sales Taxes and Charges")
- Keep names concise but clear
- Avoid abbreviations unless widely understood

### Module-Specific Naming
- Prefix with module name for module-specific doctypes
- Example: `"Selling Settings"`, `"Buying Settings"`

### Child Table Names
- Typically named `"Parent DocType Child"` or `"Parent DocType Item"`
- Examples: `"Sales Order Item"`, `"Purchase Receipt Item"`

## Field Names (fieldname)

### Format
- **Convention**: snake_case (lowercase with underscores)
- **Examples**:
  - Good: `"customer_name"`, `"total_amount"`, `"is_active"`
  - Bad: `"CustomerName"`, `"totalAmount"`, `"TOTAL_AMOUNT"`

### Rules
1. **Start with letter**: Never start with number or underscore
2. **Lowercase only**: All characters must be lowercase
3. **Use underscores**: Separate words with underscores
4. **No special characters**: Only letters, numbers, and underscores
5. **Maximum 64 characters**: Database column name limit
6. **Avoid SQL keywords**: Don't use `select`, `from`, `where`, `order`, etc.
7. **Meaningful names**: Describe what the field contains

### Common Patterns

**Status fields:**
- `status`, `workflow_state`, `approval_status`

**Date fields:**
- `posting_date`, `transaction_date`, `start_date`, `end_date`, `modified_date`

**Boolean flags:**
- Prefix with `is_`: `is_active`, `is_company`, `is_group`
- Prefix with `has_`: `has_discount`, `has_variants`
- Prefix with `allow_`: `allow_negative_stock`, `allow_editing`

**Amounts and totals:**
- Prefix with `total_`: `total_amount`, `total_qty`, `total_tax`
- Suffix with `_amount`: `base_amount`, `net_amount`
- Suffix with `_rate`: `conversion_rate`, `tax_rate`

**References:**
- Reference field + `_name`: `customer` and `customer_name`
- Parent reference: `parent_customer`, `parent_item`

**Counts and indexes:**
- Suffix with `_count`: `item_count`, `row_count`
- Use `idx` for ordering/indexing

### Reserved Field Names

Never use these as custom field names (added automatically by framework):

- `name`: Document unique identifier
- `owner`: Creator user
- `creation`: Creation timestamp
- `modified`: Last modified timestamp
- `modified_by`: Last modifier user
- `docstatus`: Document status
- `idx`: Row index
- `parent`: Parent document (child tables)
- `parenttype`: Parent DocType (child tables)
- `parentfield`: Parent field (child tables)
- `_user_tags`: User tags
- `_comments`: Comments
- `_assign`: Assignments
- `_liked_by`: Likes
- `_seen`: View tracking

### Naming by Purpose

**Identifiers:**
```
customer_id
serial_no
reference_no
```

**Names and titles:**
```
customer_name
item_name
project_title
```

**Descriptions:**
```
description
notes
remarks
comments
```

**Amounts and quantities:**
```
quantity
qty
amount
rate
price
cost
```

**Dates:**
```
posting_date
due_date
expiry_date
start_date
end_date
```

**Contact information:**
```
email_id
phone
mobile_no
address_line_1
```

**Relationships:**
```
customer
item_code
project
department
```

## Field Labels

### Format
- **Convention**: Title Case with spaces
- **Examples**: 
  - Good: `"Customer Name"`, `"Total Amount"`, `"Is Active"`
  - Avoid: `"customer name"`, `"CUSTOMER NAME"`, `"Customer_Name"`

### Rules
1. Use proper title case
2. Use spaces, not underscores
3. Clear and descriptive
4. Shorter is better (but not cryptic)
5. Avoid redundant words

### Label Patterns

**Auto-generated labels:**
If no label specified, framework converts fieldname:
- `customer_name` → `"Customer Name"`
- `total_amount` → `"Total Amount"`
- `is_active` → `"Is Active"`

**Concise labels:**
```json
"fieldname": "customer",        "label": "Customer"
"fieldname": "qty",             "label": "Qty"
"fieldname": "amount",          "label": "Amount"
```

**With context:**
```json
"fieldname": "base_amount",     "label": "Amount (Company Currency)"
"fieldname": "net_total",       "label": "Net Total (After Discount)"
```

**For booleans:**
```json
"fieldname": "is_active",       "label": "Active"
"fieldname": "is_company",      "label": "Is a Company"
"fieldname": "allow_discount",  "label": "Allow Discount"
```

## Module Names

### Format
- **Convention**: Title Case with spaces
- **Examples**: `"Selling"`, `"Stock"`, `"Accounts"`, `"HR"`

### Rules
- Short and descriptive
- Typically single word or two words
- Represents functional area
- No version numbers

## File and Directory Names

### DocType directory:
```
module_name/doctype/doctype_name/
```

Example:
```
selling/doctype/sales_order/
```

### Files in DocType directory:
```
doctype_name.json          # Schema
doctype_name.py            # Controller
doctype_name.js            # Client script
test_doctype_name.py       # Tests
doctype_name_list.js       # List view customization
```

Example:
```
sales_order.json
sales_order.py
sales_order.js
test_sales_order.py
sales_order_list.js
```

### Naming rules:
- All lowercase
- Use underscores (snake_case)
- Exact match to DocType name (converted to snake_case)

## Autoname Patterns

### Common patterns for the `autoname` property:

**Prompt user:**
```json
"autoname": "Prompt"
```
User enters the ID when creating document.

**Field value:**
```json
"autoname": "field:customer_name"
```
Use value from specified field as document name.

**Series with year:**
```json
"autoname": "PROJ-.YY.-.####"
"autoname": "INV-.YYYY.-.#####"
```
Format: `PROJ-24-0001`, `INV-2024-00001`

**Series with naming series:**
```json
"autoname": "naming_series:"
```
User selects from predefined series (requires "naming_series" field).

**Hash:**
```json
"autoname": "hash"
```
Generate random hash as ID (for child tables).

**Format expression:**
```json
"autoname": "format:{customer}-{posting_date}"
```
Combine multiple field values.

### Series naming conventions:
- Uppercase letters for series prefix
- Dots to separate components
- Hashes (#) for sequential numbers
- `YY` for 2-digit year, `YYYY` for 4-digit year
- Example formats:
  - `SO-.YYYY.-.#####` → `SO-2024-00001`
  - `CUST-.####` → `CUST-0001`
  - `PO-.YY.MM.-.####` → `PO-24.01-0001`

## Best Practices

### DocType Naming
✅ **Do:**
- Use clear, descriptive names
- Follow existing naming patterns in the module
- Use singular nouns
- Keep names concise

❌ **Don't:**
- Use abbreviations unless standard (e.g., BOM, UOM are OK)
- Include version numbers
- Use technical jargon
- Make names too long (>50 characters)

### Field Naming
✅ **Do:**
- Use descriptive, self-explanatory names
- Follow snake_case convention
- Be consistent with similar fields across doctypes
- Use common prefixes/suffixes

❌ **Don't:**
- Use single letters (except standard like `x`, `y` for coordinates)
- Mix naming conventions
- Use reserved words
- Create names longer than needed

### Label Naming
✅ **Do:**
- Keep labels short but clear
- Use proper capitalization
- Match user's vocabulary
- Be consistent across similar fields

❌ **Don't:**
- Use technical field names
- Make labels too long
- Use all caps or no caps
- Include field type in label

## Examples of Good Naming

### Sales Order DocType
```json
{
  "name": "Sales Order",
  "module": "Selling",
  "autoname": "SO-.YY.-.#####",
  "fields": [
    {
      "fieldname": "customer",
      "fieldtype": "Link",
      "label": "Customer",
      "options": "Customer"
    },
    {
      "fieldname": "customer_name",
      "fieldtype": "Data",
      "label": "Customer Name",
      "fetch_from": "customer.customer_name"
    },
    {
      "fieldname": "transaction_date",
      "fieldtype": "Date",
      "label": "Date"
    },
    {
      "fieldname": "delivery_date",
      "fieldtype": "Date",
      "label": "Delivery Date"
    },
    {
      "fieldname": "items",
      "fieldtype": "Table",
      "label": "Items",
      "options": "Sales Order Item"
    },
    {
      "fieldname": "total_qty",
      "fieldtype": "Float",
      "label": "Total Quantity"
    },
    {
      "fieldname": "total",
      "fieldtype": "Currency",
      "label": "Total"
    },
    {
      "fieldname": "grand_total",
      "fieldtype": "Currency",
      "label": "Grand Total"
    }
  ]
}
```

This example shows:
- Clear DocType name with space
- Descriptive module name
- Standard autoname pattern
- snake_case fieldnames
- Clear, concise labels
- Consistent naming patterns
