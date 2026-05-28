# Common DocType Patterns

Frequently used patterns and configurations for common scenarios.

## Master-Detail Pattern

### Parent with Child Table

**Parent DocType (Sales Order):**
```json
{
  "name": "Sales Order",
  "module": "Selling",
  "is_submittable": 1,
  "autoname": "SO-.YYYY.-.#####",
  "fields": [
    {
      "fieldname": "customer",
      "fieldtype": "Link",
      "label": "Customer",
      "options": "Customer",
      "reqd": 1
    },
    {
      "fieldname": "transaction_date",
      "fieldtype": "Date",
      "label": "Date",
      "default": "Today",
      "reqd": 1
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
      "label": "Total Quantity",
      "read_only": 1
    },
    {
      "fieldname": "grand_total",
      "fieldtype": "Currency",
      "label": "Grand Total",
      "read_only": 1
    }
  ]
}
```

**Child DocType (Sales Order Item):**
```json
{
  "name": "Sales Order Item",
  "module": "Selling",
  "istable": 1,
  "editable_grid": 1,
  "fields": [
    {
      "fieldname": "item_code",
      "fieldtype": "Link",
      "label": "Item Code",
      "options": "Item",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "item_name",
      "fieldtype": "Data",
      "label": "Item Name",
      "fetch_from": "item_code.item_name",
      "in_list_view": 1,
      "read_only": 1
    },
    {
      "fieldname": "qty",
      "fieldtype": "Float",
      "label": "Quantity",
      "reqd": 1,
      "in_list_view": 1,
      "non_negative": 1
    },
    {
      "fieldname": "rate",
      "fieldtype": "Currency",
      "label": "Rate",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "amount",
      "fieldtype": "Currency",
      "label": "Amount",
      "read_only": 1,
      "in_list_view": 1
    }
  ]
}
```

## Status Workflow Pattern

### DocType with Status Field and Workflow

```json
{
  "name": "Leave Application",
  "is_submittable": 1,
  "fields": [
    {
      "fieldname": "employee",
      "fieldtype": "Link",
      "label": "Employee",
      "options": "Employee",
      "reqd": 1
    },
    {
      "fieldname": "from_date",
      "fieldtype": "Date",
      "label": "From Date",
      "reqd": 1
    },
    {
      "fieldname": "to_date",
      "fieldtype": "Date",
      "label": "To Date",
      "reqd": 1
    },
    {
      "fieldname": "leave_type",
      "fieldtype": "Link",
      "label": "Leave Type",
      "options": "Leave Type",
      "reqd": 1
    },
    {
      "fieldname": "status",
      "fieldtype": "Select",
      "label": "Status",
      "options": "Open\nApproved\nRejected",
      "default": "Open",
      "in_list_view": 1,
      "in_standard_filter": 1
    },
    {
      "fieldname": "approved_by",
      "fieldtype": "Link",
      "label": "Approved By",
      "options": "User",
      "read_only": 1,
      "depends_on": "eval:doc.status=='Approved'"
    }
  ]
}
```

## Settings Pattern

### Single DocType for Module Settings

```json
{
  "name": "Sales Settings",
  "issingle": 1,
  "module": "Selling",
  "fields": [
    {
      "fieldname": "defaults_section",
      "fieldtype": "Section Break",
      "label": "Defaults"
    },
    {
      "fieldname": "default_customer_group",
      "fieldtype": "Link",
      "label": "Default Customer Group",
      "options": "Customer Group"
    },
    {
      "fieldname": "default_territory",
      "fieldtype": "Link",
      "label": "Default Territory",
      "options": "Territory"
    },
    {
      "fieldname": "column_break_1",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "default_price_list",
      "fieldtype": "Link",
      "label": "Default Price List",
      "options": "Price List"
    },
    {
      "fieldname": "features_section",
      "fieldtype": "Section Break",
      "label": "Features"
    },
    {
      "fieldname": "allow_multiple_items",
      "fieldtype": "Check",
      "label": "Allow Multiple Items"
    },
    {
      "fieldname": "show_discount_percentage",
      "fieldtype": "Check",
      "label": "Show Discount Percentage"
    }
  ]
}
```

## Tree Structure Pattern

### Hierarchical DocType

```json
{
  "name": "Department",
  "module": "HR",
  "is_tree": 1,
  "nsm_parent_field": "parent_department",
  "autoname": "field:department_name",
  "fields": [
    {
      "fieldname": "department_name",
      "fieldtype": "Data",
      "label": "Department Name",
      "reqd": 1,
      "unique": 1
    },
    {
      "fieldname": "parent_department",
      "fieldtype": "Link",
      "label": "Parent Department",
      "options": "Department"
    },
    {
      "fieldname": "is_group",
      "fieldtype": "Check",
      "label": "Is Group"
    },
    {
      "fieldname": "company",
      "fieldtype": "Link",
      "label": "Company",
      "options": "Company"
    }
  ]
}
```

## Multi-Currency Pattern

### DocType with Base and Foreign Currency

```json
{
  "name": "Purchase Order",
  "fields": [
    {
      "fieldname": "currency_section",
      "fieldtype": "Section Break",
      "label": "Currency"
    },
    {
      "fieldname": "currency",
      "fieldtype": "Link",
      "label": "Currency",
      "options": "Currency",
      "default": "USD"
    },
    {
      "fieldname": "conversion_rate",
      "fieldtype": "Float",
      "label": "Exchange Rate",
      "precision": "9",
      "reqd": 1
    },
    {
      "fieldname": "column_break_2",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "company_currency",
      "fieldtype": "Link",
      "label": "Company Currency",
      "options": "Currency",
      "read_only": 1
    },
    {
      "fieldname": "totals_section",
      "fieldtype": "Section Break",
      "label": "Totals"
    },
    {
      "fieldname": "total",
      "fieldtype": "Currency",
      "label": "Total",
      "options": "currency",
      "read_only": 1
    },
    {
      "fieldname": "base_total",
      "fieldtype": "Currency",
      "label": "Total (Company Currency)",
      "options": "company_currency",
      "read_only": 1
    }
  ]
}
```

## Address and Contact Pattern

### Dynamic Link Pattern

```json
{
  "name": "Address",
  "fields": [
    {
      "fieldname": "address_type",
      "fieldtype": "Select",
      "label": "Address Type",
      "options": "Billing\nShipping\nOffice\nPersonal"
    },
    {
      "fieldname": "address_line1",
      "fieldtype": "Data",
      "label": "Address Line 1",
      "reqd": 1
    },
    {
      "fieldname": "address_line2",
      "fieldtype": "Data",
      "label": "Address Line 2"
    },
    {
      "fieldname": "city",
      "fieldtype": "Data",
      "label": "City",
      "reqd": 1
    },
    {
      "fieldname": "state",
      "fieldtype": "Data",
      "label": "State"
    },
    {
      "fieldname": "pincode",
      "fieldtype": "Data",
      "label": "Postal Code"
    },
    {
      "fieldname": "country",
      "fieldtype": "Link",
      "label": "Country",
      "options": "Country",
      "reqd": 1
    },
    {
      "fieldname": "links_section",
      "fieldtype": "Section Break",
      "label": "Links"
    },
    {
      "fieldname": "links",
      "fieldtype": "Table",
      "label": "Links",
      "options": "Dynamic Link"
    }
  ]
}
```

**Dynamic Link Child Table:**
```json
{
  "name": "Dynamic Link",
  "istable": 1,
  "fields": [
    {
      "fieldname": "link_doctype",
      "fieldtype": "Link",
      "label": "Link DocType",
      "options": "DocType",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "link_name",
      "fieldtype": "Dynamic Link",
      "label": "Link Name",
      "options": "link_doctype",
      "reqd": 1,
      "in_list_view": 1
    }
  ]
}
```

## Versioning Pattern

### Track Changes to a Document

```json
{
  "name": "Contract",
  "track_changes": 1,
  "fields": [
    {
      "fieldname": "contract_name",
      "fieldtype": "Data",
      "label": "Contract Name",
      "reqd": 1
    },
    {
      "fieldname": "version",
      "fieldtype": "Int",
      "label": "Version",
      "read_only": 1,
      "default": "1"
    },
    {
      "fieldname": "previous_version",
      "fieldtype": "Link",
      "label": "Previous Version",
      "options": "Contract",
      "read_only": 1
    },
    {
      "fieldname": "effective_date",
      "fieldtype": "Date",
      "label": "Effective Date",
      "reqd": 1
    },
    {
      "fieldname": "expiry_date",
      "fieldtype": "Date",
      "label": "Expiry Date"
    },
    {
      "fieldname": "terms",
      "fieldtype": "Text Editor",
      "label": "Terms and Conditions"
    }
  ]
}
```

## Approval Pattern

### Multi-Level Approval Workflow

```json
{
  "name": "Purchase Order",
  "is_submittable": 1,
  "fields": [
    {
      "fieldname": "approval_section",
      "fieldtype": "Section Break",
      "label": "Approval",
      "collapsible": 1
    },
    {
      "fieldname": "approval_status",
      "fieldtype": "Select",
      "label": "Approval Status",
      "options": "Pending\nApproved\nRejected",
      "default": "Pending",
      "read_only": 1
    },
    {
      "fieldname": "approved_by",
      "fieldtype": "Link",
      "label": "Approved By",
      "options": "User",
      "read_only": 1
    },
    {
      "fieldname": "approved_on",
      "fieldtype": "Datetime",
      "label": "Approved On",
      "read_only": 1
    },
    {
      "fieldname": "rejection_reason",
      "fieldtype": "Small Text",
      "label": "Rejection Reason",
      "depends_on": "eval:doc.approval_status=='Rejected'"
    }
  ]
}
```

## Serial/Batch Number Pattern

### Item with Serial Numbers

```json
{
  "name": "Item",
  "fields": [
    {
      "fieldname": "item_code",
      "fieldtype": "Data",
      "label": "Item Code",
      "reqd": 1,
      "unique": 1
    },
    {
      "fieldname": "item_name",
      "fieldtype": "Data",
      "label": "Item Name",
      "reqd": 1
    },
    {
      "fieldname": "inventory_section",
      "fieldtype": "Section Break",
      "label": "Inventory"
    },
    {
      "fieldname": "has_serial_no",
      "fieldtype": "Check",
      "label": "Has Serial No"
    },
    {
      "fieldname": "serial_no_series",
      "fieldtype": "Data",
      "label": "Serial Number Series",
      "depends_on": "has_serial_no"
    },
    {
      "fieldname": "has_batch_no",
      "fieldtype": "Check",
      "label": "Has Batch No"
    },
    {
      "fieldname": "create_new_batch",
      "fieldtype": "Check",
      "label": "Create New Batch",
      "depends_on": "has_batch_no"
    }
  ]
}
```

## Price List Pattern

### Item Price with Multiple Price Lists

```json
{
  "name": "Item Price",
  "autoname": "hash",
  "fields": [
    {
      "fieldname": "item_code",
      "fieldtype": "Link",
      "label": "Item Code",
      "options": "Item",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "price_list",
      "fieldtype": "Link",
      "label": "Price List",
      "options": "Price List",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "price_list_rate",
      "fieldtype": "Currency",
      "label": "Rate",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "valid_from",
      "fieldtype": "Date",
      "label": "Valid From"
    },
    {
      "fieldname": "valid_upto",
      "fieldtype": "Date",
      "label": "Valid Upto"
    }
  ]
}
```

## Calendar/Scheduling Pattern

### Event with Date/Time

```json
{
  "name": "Event",
  "fields": [
    {
      "fieldname": "subject",
      "fieldtype": "Data",
      "label": "Subject",
      "reqd": 1
    },
    {
      "fieldname": "event_type",
      "fieldtype": "Select",
      "label": "Event Type",
      "options": "Private\nPublic\nMeeting\nCall",
      "default": "Public"
    },
    {
      "fieldname": "starts_on",
      "fieldtype": "Datetime",
      "label": "Starts On",
      "reqd": 1
    },
    {
      "fieldname": "ends_on",
      "fieldtype": "Datetime",
      "label": "Ends On",
      "reqd": 1
    },
    {
      "fieldname": "all_day",
      "fieldtype": "Check",
      "label": "All Day"
    },
    {
      "fieldname": "repeat_this_event",
      "fieldtype": "Check",
      "label": "Repeat This Event"
    },
    {
      "fieldname": "repeat_on",
      "fieldtype": "Select",
      "label": "Repeat On",
      "options": "Daily\nWeekly\nMonthly\nYearly",
      "depends_on": "repeat_this_event"
    }
  ]
}
```

## Permission Level Pattern

### Field-Level Permissions

```json
{
  "name": "Sales Order",
  "fields": [
    {
      "fieldname": "customer",
      "fieldtype": "Link",
      "label": "Customer",
      "options": "Customer",
      "permlevel": 0
    },
    {
      "fieldname": "discount_percentage",
      "fieldtype": "Percent",
      "label": "Discount %",
      "permlevel": 1
    },
    {
      "fieldname": "profit_margin",
      "fieldtype": "Percent",
      "label": "Profit Margin",
      "permlevel": 2,
      "hidden": 1
    }
  ],
  "permissions": [
    {
      "role": "Sales User",
      "permlevel": 0,
      "read": 1,
      "write": 1
    },
    {
      "role": "Sales Manager",
      "permlevel": 1,
      "read": 1,
      "write": 1
    },
    {
      "role": "Accounts Manager",
      "permlevel": 2,
      "read": 1,
      "write": 1
    }
  ]
}
```

## Fetch and Compute Pattern

### Auto-Calculate Based on Other Fields

```json
{
  "name": "Sales Order Item",
  "istable": 1,
  "fields": [
    {
      "fieldname": "item_code",
      "fieldtype": "Link",
      "label": "Item",
      "options": "Item",
      "reqd": 1
    },
    {
      "fieldname": "item_name",
      "fieldtype": "Data",
      "label": "Item Name",
      "fetch_from": "item_code.item_name",
      "read_only": 1
    },
    {
      "fieldname": "uom",
      "fieldtype": "Link",
      "label": "UOM",
      "options": "UOM",
      "fetch_from": "item_code.stock_uom",
      "fetch_if_empty": 1
    },
    {
      "fieldname": "qty",
      "fieldtype": "Float",
      "label": "Qty",
      "reqd": 1,
      "non_negative": 1
    },
    {
      "fieldname": "rate",
      "fieldtype": "Currency",
      "label": "Rate",
      "reqd": 1
    },
    {
      "fieldname": "amount",
      "fieldtype": "Currency",
      "label": "Amount",
      "read_only": 1
    }
  ]
}
```

## Quick Entry Pattern

### Minimal Fields for Quick Creation

```json
{
  "name": "Customer",
  "quick_entry": 1,
  "fields": [
    {
      "fieldname": "customer_name",
      "fieldtype": "Data",
      "label": "Customer Name",
      "reqd": 1,
      "allow_in_quick_entry": 1
    },
    {
      "fieldname": "customer_type",
      "fieldtype": "Select",
      "label": "Customer Type",
      "options": "Company\nIndividual",
      "default": "Company",
      "allow_in_quick_entry": 1
    },
    {
      "fieldname": "customer_group",
      "fieldtype": "Link",
      "label": "Customer Group",
      "options": "Customer Group",
      "allow_in_quick_entry": 1
    },
    {
      "fieldname": "territory",
      "fieldtype": "Link",
      "label": "Territory",
      "options": "Territory",
      "allow_in_quick_entry": 1
    },
    {
      "fieldname": "more_info_section",
      "fieldtype": "Section Break",
      "label": "More Information"
    },
    {
      "fieldname": "email",
      "fieldtype": "Data",
      "label": "Email",
      "options": "Email"
    }
  ]
}
```

## Web Portal Pattern

### DocType with Portal Access

```json
{
  "name": "Project",
  "has_web_view": 1,
  "allow_guest_to_view": 0,
  "fields": [
    {
      "fieldname": "project_name",
      "fieldtype": "Data",
      "label": "Project Name",
      "reqd": 1
    },
    {
      "fieldname": "status",
      "fieldtype": "Select",
      "label": "Status",
      "options": "Open\nCompleted\nCancelled"
    },
    {
      "fieldname": "is_published",
      "fieldtype": "Check",
      "label": "Published",
      "default": "0"
    },
    {
      "fieldname": "route",
      "fieldtype": "Data",
      "label": "Route",
      "read_only": 1
    }
  ]
}
```
