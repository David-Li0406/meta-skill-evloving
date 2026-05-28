# Filter Field Properties Reference

Complete guide to filter properties, configuration options, and advanced features in Frappe reports.

## Common Filter Properties

| Property | Description | Required | Type |
|----------|-------------|----------|------|
| `fieldname` | Internal name used in Python `filters` dict | Yes | String |
| `label` | Display label (use `__()` for translation) | Yes | String |
| `fieldtype` | Type of filter field | Yes | String |
| `options` | Configuration specific to field type (see below) | Conditional | String/Array/Function |
| `default` | Default value | No | Any |
| `reqd` | 1 for required, 0 for optional | No | Int (0 or 1) |
| `depends_on` | Show filter conditionally | No | String |
| `get_query` | Function to filter Link options | No | Function |
| `on_change` | Function called when value changes | No | Function |
| `get_data` | Function to fetch data for MultiSelect | No | Function |
| `get_options` | Function to get options for Dynamic Link | No | Function |

## The "options" Property

The `options` property is used differently depending on the field type:

**Link Fields:**
- Target DocType name
- Example: `options: "Customer"`

**Dynamic Link Fields:**
- Not directly set; use `get_options` function instead
- The function returns the DocType based on another filter's value

**Select Fields:**
- Array of choices OR newline-separated string
- Example: `options: ["", "Draft", "Submitted", "Cancelled"]`
- Or: `options: "\nDraft\nSubmitted\nCancelled"`

**MultiSelect/MultiSelectList Fields:**
- DocType name to select from
- Example: `options: "Warehouse"`

**Code Fields (rarely used in filters):**
- Programming language for syntax highlighting
- Example: `options: "Python"`

**Data Fields (rarely used in filters):**
- Data type specification
- Example: `options: "Email"` (for email validation)

### Options Property Examples

**Link Filter:**
```javascript
{
    fieldname: "customer",
    label: __("Customer"),
    fieldtype: "Link",
    options: "Customer"  // Target DocType
}
```

**Select Filter with Array:**
```javascript
{
    fieldname: "status",
    label: __("Status"),
    fieldtype: "Select",
    options: ["", "Draft", "Submitted", "Cancelled"],  // Array format
    default: ""
}
```

**Select Filter with String:**
```javascript
{
    fieldname: "priority",
    label: __("Priority"),
    fieldtype: "Select",
    options: "\nLow\nMedium\nHigh",  // Newline-separated string
    default: ""
}
```

**MultiSelect Filter:**
```javascript
{
    fieldname: "warehouses",
    label: __("Warehouses"),
    fieldtype: "MultiSelect",
    options: "Warehouse",  // DocType to select from
    get_data: function(txt) {
        return frappe.db.get_link_options("Warehouse", txt);
    }
}
```

**Dynamic Link Filter:**
```javascript
{
    fieldname: "party_type",
    label: __("Party Type"),
    fieldtype: "Link",
    options: "DocType"
},
{
    fieldname: "party",
    label: __("Party"),
    fieldtype: "Dynamic Link",
    // Use get_options instead of options
    get_options: function() {
        return frappe.query_report.get_filter_value("party_type");
    }
}
```

## Default Values

### Static Defaults

Simple static values:

```javascript
{
    fieldname: "company",
    label: __("Company"),
    fieldtype: "Link",
    options: "Company",
    default: "My Company"  // Static default
}
```

### Dynamic Defaults

Calculate defaults using Frappe utilities:

**Date defaults:**
```javascript
{
    fieldname: "from_date",
    label: __("From Date"),
    fieldtype: "Date",
    default: frappe.datetime.add_months(frappe.datetime.get_today(), -1)  // Last month
}

{
    fieldname: "to_date",
    label: __("To Date"),
    fieldtype: "Date",
    default: frappe.datetime.get_today()  // Today
}
```

**User defaults:**
```javascript
{
    fieldname: "company",
    label: __("Company"),
    fieldtype: "Link",
    options: "Company",
    default: frappe.defaults.get_user_default("Company")  // User's default company
}
```

**System defaults:**
```javascript
{
    fieldname: "fiscal_year",
    label: __("Fiscal Year"),
    fieldtype: "Link",
    options: "Fiscal Year",
    default: frappe.sys_defaults.fiscal_year  // System's fiscal year
}
```

## Dependent Filters

Show filters conditionally based on other filters:

```javascript
{
    fieldname: "report_type",
    label: __("Report Type"),
    fieldtype: "Select",
    options: ["Summary", "Detailed"]
},
{
    fieldname: "group_by",
    label: __("Group By"),
    fieldtype: "Select",
    options: ["Customer", "Item", "Territory"],
    depends_on: "eval:doc.report_type=='Summary'"  // Only show if report_type is Summary
}
```

## Conditional Options (get_query)

Filter Link field options based on other filters:

```javascript
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
        let company = frappe.query_report.get_filter_value("company");
        return {
            filters: {
                "company": company,
                "is_group": 0
            }
        };
    }
}
```

**Custom server-side query:**
```javascript
{
    fieldname: "customer",
    label: __("Customer"),
    fieldtype: "Link",
    options: "Customer",
    get_query: function() {
        return {
            query: "your_app.queries.get_active_customers",
            filters: {
                "status": "Active"
            }
        };
    }
}
```

Server-side query function:
```python
# In your_app/queries.py
import frappe

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_active_customers(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
        SELECT name, customer_name
        FROM `tabCustomer`
        WHERE status = 'Active'
            AND ({key} LIKE %(txt)s OR customer_name LIKE %(txt)s)
        ORDER BY
            CASE WHEN name LIKE %(txt)s THEN 0 ELSE 1 END,
            name
        LIMIT %(start)s, %(page_len)s
    """.format(key=searchfield), {
        "txt": "%" + txt + "%",
        "start": start,
        "page_len": page_len
    })
```

## On Change Events

Execute code when filter value changes:

```javascript
{
    fieldname: "company",
    label: __("Company"),
    fieldtype: "Link",
    options: "Company",
    on_change: function() {
        // Reset dependent filters
        frappe.query_report.set_filter_value("cost_center", "");
        frappe.query_report.set_filter_value("warehouse", "");
        
        // Optionally refresh report
        // frappe.query_report.refresh();
    }
}
```

## MultiSelect Configuration

For MultiSelect and MultiSelectList fields:

```javascript
{
    fieldname: "warehouses",
    label: __("Warehouses"),
    fieldtype: "MultiSelect",
    options: "Warehouse",
    get_data: function(txt) {
        // Fetch matching options
        return frappe.db.get_link_options("Warehouse", txt, {
            "is_group": 0
        });
    }
}
```

## Dynamic Link Configuration

For Dynamic Link fields:

```javascript
{
    fieldname: "party_type",
    label: __("Party Type"),
    fieldtype: "Link",
    options: "DocType",
    get_query: function() {
        return {
            filters: {
                "name": ["in", ["Customer", "Supplier"]]
            }
        };
    }
},
{
    fieldname: "party",
    label: __("Party"),
    fieldtype: "Dynamic Link",
    get_options: function() {
        let party_type = frappe.query_report.get_filter_value("party_type");
        if (!party_type) {
            frappe.throw(__("Please select Party Type first"));
        }
        return party_type;
    }
}
```

## Accessing Filter Values

### In JavaScript

```javascript
frappe.query_reports["My Report"] = {
    filters: [...],
    
    onload: function(report) {
        // Get single filter value
        let company = frappe.query_report.get_filter_value("company");
        
        // Set filter value
        frappe.query_report.set_filter_value("status", "Active");
        
        // Get all filter values
        let all_filters = report.get_filter_values();
        console.log(all_filters);
    }
};
```

### In Python

Filters are passed as a dictionary to the execute function:

```python
def execute(filters=None):
    # Access filter values
    company = filters.get("company")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    
    # Check if filter is set
    if filters.get("customer"):
        # Customer filter was provided
        pass
    
    # Use in SQL with parameterized query
    data = frappe.db.sql("""
        SELECT *
        FROM `tabSales Order`
        WHERE company = %(company)s
            AND transaction_date BETWEEN %(from_date)s AND %(to_date)s
    """, filters, as_dict=1)
    
    return columns, data
```

## Filter Validation

### Client-Side Validation

```javascript
{
    fieldname: "from_date",
    label: __("From Date"),
    fieldtype: "Date",
    reqd: 1,
    on_change: function() {
        let from_date = frappe.query_report.get_filter_value("from_date");
        let to_date = frappe.query_report.get_filter_value("to_date");
        
        if (from_date && to_date && from_date > to_date) {
            frappe.throw(__("From Date cannot be greater than To Date"));
        }
    }
}
```

### Server-Side Validation

```python
def execute(filters=None):
    # Validate required filters
    if not filters.get("company"):
        frappe.throw(_("Company is required"))
    
    # Validate date range
    if filters.get("from_date") and filters.get("to_date"):
        from frappe.utils import getdate
        if getdate(filters.from_date) > getdate(filters.to_date):
            frappe.throw(_("From Date cannot be greater than To Date"))
    
    # Validate permissions
    if filters.get("customer"):
        if not frappe.has_permission("Customer", "read", filters.get("customer")):
            frappe.throw(_("You don't have permission to access this customer"))
    
    columns, data = get_columns(), get_data(filters)
    return columns, data
```

## Best Practices

### Filter Order

1. Place most important filters first (e.g., company, date range)
2. Group related filters together
3. Put optional filters after required ones
4. Place dependent filters after their parent filters

### Default Values

1. Provide sensible defaults for better UX
2. Use user preferences where applicable
3. Default date ranges to common periods (last month, current month)
4. Clear dependent filters when parent changes

### Validation

1. Validate on both client and server side
2. Provide clear error messages
3. Prevent invalid filter combinations
4. Check permissions for sensitive filters

### Performance

1. Limit options in Select fields
2. Use `get_query` to reduce Link field options
3. Don't fetch too much data in `get_data` for MultiSelect
4. Cache expensive default calculations

### User Experience

1. Mark required filters with `reqd: 1`
2. Use meaningful labels
3. Provide helpful defaults
4. Show/hide filters based on context
5. Reset dependent filters when parent changes

## Translation

Always wrap filter labels for translation support:

```javascript
{
    fieldname: "customer",
    label: __("Customer"),  // Translated
    fieldtype: "Link",
    options: "Customer"
}
```

For dynamic text:
```javascript
frappe.throw(__("Please select {0} first", [__("Company")]));
```

## Advanced Patterns

### Cascading Filters

```javascript
filters: [
    {
        fieldname: "country",
        label: __("Country"),
        fieldtype: "Link",
        options: "Country",
        on_change: function() {
            frappe.query_report.set_filter_value("state", "");
            frappe.query_report.set_filter_value("city", "");
        }
    },
    {
        fieldname: "state",
        label: __("State"),
        fieldtype: "Link",
        options: "State",
        get_query: function() {
            return {
                filters: {
                    "country": frappe.query_report.get_filter_value("country")
                }
            };
        },
        on_change: function() {
            frappe.query_report.set_filter_value("city", "");
        }
    },
    {
        fieldname: "city",
        label: __("City"),
        fieldtype: "Link",
        options: "City",
        get_query: function() {
            return {
                filters: {
                    "state": frappe.query_report.get_filter_value("state")
                }
            };
        }
    }
]
```

### Dynamic Filter Options

```javascript
{
    fieldname: "document_type",
    label: __("Document Type"),
    fieldtype: "Select",
    options: [],  // Populated dynamically
    onload: function(report) {
        // Fetch options from server
        frappe.call({
            method: "your_app.api.get_document_types",
            callback: function(r) {
                if (r.message) {
                    let filter = frappe.query_report.get_filter("document_type");
                    filter.df.options = r.message;
                    filter.refresh();
                }
            }
        });
    }
}
```

### Conditional Required

```javascript
{
    fieldname: "customer",
    label: __("Customer"),
    fieldtype: "Link",
    options: "Customer",
    mandatory_depends_on: "eval:doc.report_type=='Customer-wise'"
}
```

## Debugging

### Check Filter Values

```javascript
onload: function(report) {
    console.log("All filters:", report.get_filter_values());
    console.log("Company:", frappe.query_report.get_filter_value("company"));
}
```

### Python Debugging

```python
def execute(filters=None):
    # Log filter values
    frappe.log_error("Report Filters", frappe.as_json(filters))
    
    # Check filter existence
    if not filters:
        filters = {}
    
    # Debug print
    print(f"Filters: {filters}")
    
    columns, data = get_columns(), get_data(filters)
    return columns, data
```

## Common Issues

### Filter not passing to Python

- Check fieldname spelling matches
- Verify filter has a value (not empty)
- Check JavaScript console for errors

### Get_query not working

- Ensure function returns proper filter object
- Check parent filter has value
- Verify DocType exists and has required fields

### Default not setting

- Check default expression syntax
- Verify Frappe utilities are available
- Test in browser console first

## Related Documentation

- [filter-fieldtypes.md](filter-fieldtypes.md) - All available filter field types
- [column-fieldproperties.md](column-fieldproperties.md) - Column properties reference
- [script-report-examples.md](script-report-examples.md) - Complete working examples
