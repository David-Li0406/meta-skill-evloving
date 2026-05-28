# Report Creation Workflow

Complete step-by-step guide to creating Script Reports in Frappe.

## Creating a New Script Report

### Step 1: Create Report via Desk (Standard Reports)

For standard reports (shipped with apps):

1. Navigate to Report DocType list
2. Create new Report document
3. Set:
   - Report Name: "My Report"
   - Report Type: "Script Report"
   - Ref DocType: Select primary DocType
   - Module: Select module
   - Is Standard: "Yes"
4. Save

The framework automatically creates boilerplate files at:
```
{app}/{module}/report/{report_name}/
├── __init__.py
├── {report_name}.json
├── {report_name}.py
└── {report_name}.js
```

### Step 2: Implement the Execute Function

Edit `{report_name}.py`:

```python
# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        _("ID") + ":Link/DocType:120",
        _("Name") + ":Data:150",
        _("Amount") + ":Currency:120",
        _("Date") + ":Date:100",
    ]

def get_data(filters):
    # Your data fetching logic
    conditions = get_conditions(filters)
    
    data = frappe.db.sql("""
        SELECT 
            name,
            title,
            total_amount,
            posting_date
        FROM `tabDocType`
        WHERE docstatus = 1 {conditions}
        ORDER BY posting_date DESC
    """.format(conditions=conditions), filters, as_list=1)
    
    return data

def get_conditions(filters):
    conditions = ""
    
    if filters.get("company"):
        conditions += " AND company = %(company)s"
    
    if filters.get("from_date"):
        conditions += " AND posting_date >= %(from_date)s"
    
    if filters.get("to_date"):
        conditions += " AND posting_date <= %(to_date)s"
    
    return conditions
```

### Step 3: Define Filters

Edit `{report_name}.js`:

```javascript
// Copyright (c) 2024, Your Company and contributors
// For license information, please see license.txt

frappe.query_reports["My Report"] = {
    filters: [
        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            default: frappe.defaults.get_user_default("Company")
        },
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
};
```

### Step 4: Test the Report

1. Run `bench migrate` to sync changes
2. Navigate to the report: `/app/query-report/My Report`
3. Apply filters and verify data

## Report Metadata (.json file)

Required fields in the JSON file:

```json
{
  "report_name": "My Report",
  "ref_doctype": "DocType Name",
  "report_type": "Script Report",
  "is_standard": "Yes",
  "module": "Module Name",
  "disabled": 0,
  "add_total_row": 0,
  "roles": [
    {"role": "System Manager"}
  ]
}
```

**Key properties:**
- `report_name`: Display name of the report
- `ref_doctype`: The primary DocType this report relates to (required)
- `report_type`: One of "Report Builder", "Query Report", "Script Report", "Custom Report"
- `is_standard`: "Yes" for app-bundled reports, "No" for custom reports
- `module`: The module this report belongs to
- `add_total_row`: Set to 1 to automatically add a total row at the bottom
- `roles`: Array of roles that can access this report

## Boilerplate Generation

When you create a standard Script Report via the desk:

1. Report document is saved to database
2. On save, if `is_standard == "Yes"`:
   - Report JSON is exported to: `{app}/{module}/report/{report_name}/{report_name}.json`
   - Boilerplate files are created via `make_boilerplate()`:
     - `{report_name}.py` - From `frappe/core/doctype/report/boilerplate/controller.py`
     - `{report_name}.js` - From `frappe/core/doctype/report/boilerplate/controller.js`

**Boilerplate templates:**

Python template (`controller.py`):
```python
# Copyright (c) {year}, {app_publisher} and contributors
# For license information, please see license.txt

# import frappe

def execute(filters=None):
    columns, data = [], []
    return columns, data
```

JavaScript template (`controller.js`):
```javascript
// Copyright (c) {year}, {app_publisher} and contributors
// For license information, please see license.txt

frappe.query_reports["{name}"] = {
    "filters": []
};
```

The placeholders `{year}`, `{app_publisher}`, and `{name}` are replaced automatically.

## Quick Tips

### Permissions

Control access with role-based permissions:

```python
def execute(filters=None):
    # Restrict to specific role
    frappe.only_for("System Manager")
    
    # Or check permission
    if not frappe.has_permission("DocType", "read"):
        frappe.throw("Insufficient permissions")
    
    columns, data = get_columns(), get_data(filters)
    return columns, data
```

### Query Optimization

Best practices for performance:

1. **Use proper indexing**: Filter on indexed fields
2. **Limit data**: Add LIMIT clause for large datasets
3. **Avoid SELECT ***: Select only needed columns
4. **Use `frappe.get_list()`** for simple queries:
   ```python
   data = frappe.get_list(
       "DocType",
       fields=["name", "title", "amount"],
       filters={"status": "Active"},
       order_by="creation desc"
   )
   ```

5. **Cache expensive operations**:
   ```python
   @frappe.whitelist()
   def get_cached_data():
       return frappe.cache().get_value(
           "my_report_data",
           generator=lambda: fetch_data()
       )
   ```

## Common Patterns

### Simple List Report

```python
def execute(filters=None):
    return get_columns(), get_data(filters)

def get_columns():
    return [
        "Name:Link/DocType:150",
        "Status:Data:100",
        "Amount:Currency:120"
    ]

def get_data(filters):
    return frappe.get_list(
        "DocType",
        fields=["name", "status", "amount"],
        filters=filters
    )
```

### Report with Calculations

```python
def execute(filters=None):
    columns = get_columns()
    raw_data = fetch_raw_data(filters)
    data = process_data(raw_data)
    
    return columns, data

def process_data(raw_data):
    processed = []
    for row in raw_data:
        # Calculate additional fields
        total = row.qty * row.rate
        tax = total * 0.18
        grand_total = total + tax
        
        processed.append([
            row.name,
            row.qty,
            row.rate,
            total,
            tax,
            grand_total
        ])
    return processed
```

### Multi-Level Grouping

```python
def execute(filters=None):
    columns = get_columns()
    data = get_grouped_data(filters)
    
    return columns, data

def get_grouped_data(filters):
    from itertools import groupby
    
    raw_data = fetch_data(filters)
    data = []
    
    for company, company_rows in groupby(raw_data, key=lambda x: x.company):
        # Add company header
        data.append({
            "company": company,
            "indent": 0,
            "is_group": 1
        })
        
        # Add detail rows
        for row in company_rows:
            data.append({
                "item": row.item_name,
                "qty": row.qty,
                "amount": row.amount,
                "indent": 1
            })
    
    return data
```

### Dynamic Columns

```python
def execute(filters=None):
    columns = get_dynamic_columns(filters)
    data = get_data(filters)
    
    return columns, data

def get_dynamic_columns(filters):
    columns = ["Item:Link/Item:150"]
    
    # Add date columns dynamically
    date_list = get_date_range(filters.from_date, filters.to_date)
    for date in date_list:
        columns.append(f"{date}:Float:100")
    
    return columns
```

See [script-report-examples.md](script-report-examples.md) for more complete working examples.

## Troubleshooting

### Report not showing up
- Check if report is disabled
- Verify user has required role
- Check ref_doctype permissions
- Run `bench migrate` to sync

### Data not displaying correctly
- Verify column count matches data row length
- Check fieldtype matches data type
- Ensure fieldnames are correct (for dict format)

### Filter not working
- Check fieldname matches in JS and Python
- Verify filter value is being passed correctly
- Add debug prints: `frappe.log_error(str(filters))`

### Performance issues
- Add LIMIT clause
- Create database indexes
- Use `frappe.db.sql()` with proper WHERE clause
- Profile slow queries
