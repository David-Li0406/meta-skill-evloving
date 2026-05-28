# Best Practices for DocType Schema Design

Guidelines and recommendations for creating well-designed DocType schemas.

## General Principles

### 1. Start Simple
- Begin with essential fields only
- Add complexity as needed
- Easier to add fields than remove them
- Test with minimal schema first

### 2. Think About Users
- Use clear, non-technical labels
- Group related fields logically
- Provide helpful descriptions
- Make forms intuitive

### 3. Plan for Scale
- Consider performance with large datasets
- Add indexes on frequently queried fields
- Keep field count reasonable (<50 for good UX)
- Use child tables for repeating data

### 4. Maintain Data Integrity
- Use appropriate field types
- Add validation through field properties
- Use `reqd` for mandatory fields
- Use `unique` for unique identifiers
- Use `non_negative` for quantities/amounts

## Field Design

### Choose Appropriate Field Types

**Use Currency for money:**
```json
{
  "fieldname": "total_amount",
  "fieldtype": "Currency",
  "label": "Total Amount",
  "precision": "2"
}
```

**Use Link for references:**
```json
{
  "fieldname": "customer",
  "fieldtype": "Link",
  "label": "Customer",
  "options": "Customer",
  "reqd": 1
}
```

**Use Select for predefined options:**
```json
{
  "fieldname": "status",
  "fieldtype": "Select",
  "label": "Status",
  "options": "Draft\nOpen\nCompleted\nCancelled",
  "default": "Draft"
}
```

**Use Check for boolean flags:**
```json
{
  "fieldname": "is_active",
  "fieldtype": "Check",
  "label": "Active",
  "default": "1"
}
```

### Field Ordering Best Practices

1. **Most important fields first**: ID, name, primary identifiers
2. **Logical grouping**: Related fields together
3. **Required before optional**: Mandatory fields at top
4. **Details before items**: Header info before line items
5. **Totals at bottom**: Summary fields at end

### Use Layout Fields Effectively

**Section Breaks for logical groups:**
```json
{
  "fieldname": "customer_details_section",
  "fieldtype": "Section Break",
  "label": "Customer Details"
}
```

**Column Breaks for side-by-side fields:**
```json
{
  "fieldname": "column_break_1",
  "fieldtype": "Column Break"
}
```

**Collapsible sections for advanced options:**
```json
{
  "fieldname": "advanced_settings",
  "fieldtype": "Section Break",
  "label": "Advanced Settings",
  "collapsible": 1
}
```

**Tabs for complex forms:**
```json
{
  "fieldname": "details_tab",
  "fieldtype": "Tab Break",
  "label": "Details"
}
```

## Performance Optimization

### Add Indexes Strategically

Add `search_index: 1` to fields that are:
- Frequently used in filters
- Used in WHERE clauses
- Foreign keys (Link fields)
- Used for sorting

```json
{
  "fieldname": "customer",
  "fieldtype": "Link",
  "label": "Customer",
  "options": "Customer",
  "search_index": 1
}
```

**Don't over-index**: Too many indexes slow down writes.

### List View Configuration

**Limit in_list_view fields to ~5:**
```json
{
  "fieldname": "customer_name",
  "fieldtype": "Data",
  "label": "Customer Name",
  "in_list_view": 1
}
```

**Add standard filters for common searches:**
```json
{
  "fieldname": "status",
  "fieldtype": "Select",
  "label": "Status",
  "options": "Open\nClosed",
  "in_standard_filter": 1
}
```

**Configure search fields:**
```json
{
  "search_fields": "customer_name,customer_group,territory"
}
```

### Child Tables

**Keep child tables focused:**
- One child table per logical entity (items, taxes, addresses)
- Don't mix different types of data
- Keep field count reasonable

**Example - Sales Order Items:**
```json
{
  "fieldname": "items",
  "fieldtype": "Table",
  "label": "Items",
  "options": "Sales Order Item"
}
```

Child DocType should have:
- `istable: 1`
- Essential fields only
- Clear in_list_view fields

## Data Validation

### Use Field Properties for Validation

**Required fields:**
```json
{
  "fieldname": "customer",
  "fieldtype": "Link",
  "label": "Customer",
  "options": "Customer",
  "reqd": 1
}
```

**Unique values:**
```json
{
  "fieldname": "email",
  "fieldtype": "Data",
  "label": "Email",
  "options": "Email",
  "unique": 1
}
```

**Non-negative numbers:**
```json
{
  "fieldname": "quantity",
  "fieldtype": "Int",
  "label": "Quantity",
  "non_negative": 1
}
```

**Set once only:**
```json
{
  "fieldname": "transaction_date",
  "fieldtype": "Date",
  "label": "Date",
  "set_only_once": 1
}
```

**Length limits:**
```json
{
  "fieldname": "short_name",
  "fieldtype": "Data",
  "label": "Short Name",
  "length": 50
}
```

### Conditional Validation

**Conditional mandatory:**
```json
{
  "fieldname": "company_registration",
  "fieldtype": "Data",
  "label": "Company Registration",
  "mandatory_depends_on": "eval:doc.customer_type=='Company'"
}
```

**Conditional display:**
```json
{
  "fieldname": "tax_id",
  "fieldtype": "Data",
  "label": "Tax ID",
  "depends_on": "eval:doc.is_company==1"
}
```

## User Experience

### Provide Context and Help

**Use descriptions:**
```json
{
  "fieldname": "credit_limit",
  "fieldtype": "Currency",
  "label": "Credit Limit",
  "description": "Maximum credit amount allowed for this customer"
}
```

**Use placeholders:**
```json
{
  "fieldname": "email",
  "fieldtype": "Data",
  "label": "Email",
  "options": "Email",
  "placeholder": "user@example.com"
}
```

**Link to documentation:**
```json
{
  "fieldname": "custom_script",
  "fieldtype": "Code",
  "label": "Custom Script",
  "options": "Python",
  "documentation_url": "https://docs.example.com/custom-scripts"
}
```

### Smart Defaults

**Today for date fields:**
```json
{
  "fieldname": "posting_date",
  "fieldtype": "Date",
  "label": "Posting Date",
  "default": "Today"
}
```

**Current user for owner fields:**
```json
{
  "fieldname": "assigned_to",
  "fieldtype": "Link",
  "label": "Assigned To",
  "options": "User",
  "default": "user"
}
```

**Status defaults:**
```json
{
  "fieldname": "status",
  "fieldtype": "Select",
  "label": "Status",
  "options": "Draft\nSubmitted\nCancelled",
  "default": "Draft"
}
```

### Auto-fetch Related Data

**Fetch customer details:**
```json
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
  "fetch_from": "customer.customer_name",
  "read_only": 1
},
{
  "fieldname": "customer_group",
  "fieldtype": "Link",
  "label": "Customer Group",
  "options": "Customer Group",
  "fetch_from": "customer.customer_group",
  "fetch_if_empty": 1
}
```

## Security Considerations

### Sensitive Data

**Use Password field type:**
```json
{
  "fieldname": "api_secret",
  "fieldtype": "Password",
  "label": "API Secret"
}
```

**Use permission levels:**
```json
{
  "fieldname": "internal_notes",
  "fieldtype": "Text",
  "label": "Internal Notes",
  "permlevel": 1
}
```

**Hide sensitive fields:**
```json
{
  "fieldname": "profit_margin",
  "fieldtype": "Percent",
  "label": "Profit Margin",
  "hidden": 1
}
```

### XSS Protection

**Don't disable XSS filter unless necessary:**
```json
// Only when HTML content is intentional and from trusted source
{
  "fieldname": "custom_html",
  "fieldtype": "Text Editor",
  "label": "Custom HTML",
  "ignore_xss_filter": 1  // Use with caution!
}
```

## Submittable DocTypes

### Design Considerations

When `is_submittable: 1`:

1. **Plan the workflow**:
   - Draft → Submit → Cancel/Amend
   - What can be edited after submit?
   - What triggers submission?

2. **Allow editing specific fields:**
```json
{
  "fieldname": "delivery_status",
  "fieldtype": "Select",
  "label": "Delivery Status",
  "options": "Pending\nPartially Delivered\nDelivered",
  "allow_on_submit": 1
}
```

3. **Use docstatus for queries:**
   - 0 = Draft
   - 1 = Submitted
   - 2 = Cancelled

4. **Consider dependencies:**
   - Which documents link to this?
   - What happens on cancel?

## Single DocTypes

### Design Considerations

When `issingle: 1`:

1. **Use for settings and configurations**
2. **No name field needed** (uses DocType name)
3. **Cannot be copied or renamed**
4. **One instance only**
5. **Data stored in tabSingles**

**Example:**
```json
{
  "doctype": "DocType",
  "name": "System Settings",
  "issingle": 1,
  "module": "Core",
  "fields": [
    {
      "fieldname": "site_name",
      "fieldtype": "Data",
      "label": "Site Name"
    },
    {
      "fieldname": "timezone",
      "fieldtype": "Select",
      "label": "Time Zone"
    }
  ]
}
```

## Tree DocTypes

### Design Considerations

When `is_tree: 1`:

1. **Set nsm_parent_field:**
```json
{
  "is_tree": 1,
  "nsm_parent_field": "parent_department"
}
```

2. **Add parent field:**
```json
{
  "fieldname": "parent_department",
  "fieldtype": "Link",
  "label": "Parent Department",
  "options": "Department"
}
```

3. **Consider:**
   - How deep can the tree go?
   - Can nodes be moved?
   - What happens to children when parent is deleted?

## Migration and Maintenance

### Plan for Changes

1. **Don't change field types** of existing fields with data
2. **Don't rename fields** directly (use migration)
3. **Test schema changes** in development first
4. **Backup before migrations**
5. **Use `no_copy: 1`** for fields that shouldn't be copied

### Backward Compatibility

When adding new required fields:
```json
{
  "fieldname": "new_required_field",
  "fieldtype": "Data",
  "label": "New Required Field",
  "reqd": 1,
  "default": "Default Value"  // Important for existing docs
}
```

### Deprecating Fields

Instead of deleting:
```json
{
  "fieldname": "old_field",
  "fieldtype": "Data",
  "label": "Old Field (Deprecated)",
  "hidden": 1,
  "read_only": 1
}
```

## Common Patterns

### Master DocType Pattern

**Characteristics:**
- Relatively static data
- Referenced by many transactions
- Examples: Customer, Item, Employee

**Structure:**
```json
{
  "name": "Customer",
  "autoname": "CUST-.####",
  "title_field": "customer_name",
  "search_fields": "customer_name,customer_group,territory",
  "fields": [
    // Basic identification
    // Contact details
    // Business details
    // Settings/preferences
  ]
}
```

### Transaction DocType Pattern

**Characteristics:**
- Time-sensitive data
- Links to master data
- Usually submittable
- Examples: Sales Order, Purchase Invoice

**Structure:**
```json
{
  "name": "Sales Order",
  "is_submittable": 1,
  "autoname": "SO-.YY.-.#####",
  "title_field": "customer_name",
  "fields": [
    // Header: date, customer, reference
    // Items: child table
    // Totals: calculated fields
    // Additional details
  ]
}
```

### Settings DocType Pattern

**Characteristics:**
- Single DocType
- Module configuration
- Examples: Selling Settings, System Settings

**Structure:**
```json
{
  "name": "Selling Settings",
  "issingle": 1,
  "module": "Selling",
  "fields": [
    // Organized in sections
    // Defaults and preferences
    // Feature flags
  ]
}
```

## Checklist for New DocType

- [ ] Choose appropriate naming (singular/plural, PascalCase)
- [ ] Set correct module
- [ ] Define type (table/single/tree/submittable)
- [ ] Design naming rule (autoname)
- [ ] Add essential fields only
- [ ] Use appropriate field types
- [ ] Add required/unique constraints
- [ ] Organize with section/column breaks
- [ ] Configure list view (in_list_view, search_fields)
- [ ] Add standard filters
- [ ] Set title_field
- [ ] Add indexes on key fields
- [ ] Define permissions
- [ ] Add field descriptions where helpful
- [ ] Test with sample data
- [ ] Document special behaviors
