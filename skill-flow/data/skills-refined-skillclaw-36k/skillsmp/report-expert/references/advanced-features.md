# Advanced Features

Advanced features and techniques for Frappe reports.

## Charts

### Basic Chart Configuration

Return chart data as the 4th element of the execute function:

```python
def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    
    return columns, data, None, chart

def get_chart(data):
    return {
        "data": {
            "labels": ["Jan", "Feb", "Mar", "Apr"],
            "datasets": [
                {
                    "name": "Sales",
                    "values": [100, 150, 200, 180]
                }
            ]
        },
        "type": "line",  # Chart type
        "height": 300,   # Height in pixels
        "colors": ["#7cd6fd"]  # Optional: custom colors
    }
```

### Chart Types

**Line Chart**
```python
{
    "data": {
        "labels": ["Q1", "Q2", "Q3", "Q4"],
        "datasets": [{
            "name": "Revenue",
            "values": [10000, 15000, 12000, 18000]
        }]
    },
    "type": "line",
    "lineOptions": {
        "regionFill": 1,  # Fill area under line
        "hideDots": 0,    # Show/hide dots
        "heatline": 0,    # Gradient effect
        "dotSize": 4      # Size of dots
    }
}
```

**Bar Chart**
```python
{
    "data": {
        "labels": ["Product A", "Product B", "Product C"],
        "datasets": [{
            "name": "Sales",
            "values": [500, 800, 600]
        }]
    },
    "type": "bar",
    "barOptions": {
        "stacked": 0,     # Stack bars
        "spaceRatio": 0.5 # Space between bars
    }
}
```

**Pie Chart**
```python
{
    "data": {
        "labels": ["Category A", "Category B", "Category C"],
        "datasets": [{
            "name": "Distribution",
            "values": [30, 50, 20]
        }]
    },
    "type": "pie",
    "height": 300
}
```

**Percentage Chart**
```python
{
    "data": {
        "labels": ["Target", "Achieved"],
        "datasets": [{
            "name": "Progress",
            "values": [100, 75]
        }]
    },
    "type": "percentage"
}
```

### Multiple Datasets

Display multiple series in one chart:

```python
def get_chart(data):
    # Extract data for chart
    months = list(set(d["month"] for d in data))
    
    sales_data = []
    cost_data = []
    
    for month in months:
        month_data = [d for d in data if d["month"] == month]
        sales_data.append(sum(d["sales"] for d in month_data))
        cost_data.append(sum(d["cost"] for d in month_data))
    
    return {
        "data": {
            "labels": months,
            "datasets": [
                {
                    "name": "Sales",
                    "values": sales_data
                },
                {
                    "name": "Cost",
                    "values": cost_data
                }
            ]
        },
        "type": "line",
        "colors": ["#7cd6fd", "#ff6384"]
    }
```

### Dynamic Charts

Generate charts based on data:

```python
def get_chart_from_data(data):
    if not data:
        return None
    
    # Group by category
    from collections import defaultdict
    category_totals = defaultdict(float)
    
    for row in data:
        category_totals[row["category"]] += row["amount"]
    
    # Sort by value
    sorted_categories = sorted(
        category_totals.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]  # Top 10
    
    return {
        "data": {
            "labels": [cat for cat, _ in sorted_categories],
            "datasets": [{
                "name": "Amount",
                "values": [amt for _, amt in sorted_categories]
            }]
        },
        "type": "bar"
    }
```

## Report Summary

Show key metrics above the report table.

### Basic Summary

```python
def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    report_summary = get_summary(data)
    
    return columns, data, None, None, report_summary

def get_summary(data):
    total_orders = len(data)
    total_amount = sum(d["amount"] for d in data)
    avg_amount = total_amount / total_orders if total_orders > 0 else 0
    
    return [
        {
            "value": total_orders,
            "label": "Total Orders",
            "datatype": "Int",
            "indicator": "Blue"
        },
        {
            "value": total_amount,
            "label": "Total Amount",
            "datatype": "Currency",
            "currency": "USD"
        },
        {
            "value": avg_amount,
            "label": "Average Amount",
            "datatype": "Currency"
        }
    ]
```

### Summary with Indicators

```python
def get_summary(data):
    total = sum(d["amount"] for d in data)
    target = 100000
    achievement = (total / target * 100) if target > 0 else 0
    
    # Determine indicator color based on achievement
    if achievement >= 100:
        indicator = "Green"
    elif achievement >= 75:
        indicator = "Orange"
    else:
        indicator = "Red"
    
    return [
        {
            "value": total,
            "label": "Total Sales",
            "datatype": "Currency",
            "indicator": indicator
        },
        {
            "value": target,
            "label": "Target",
            "datatype": "Currency"
        },
        {
            "value": achievement,
            "label": "Achievement %",
            "datatype": "Percent",
            "indicator": indicator
        }
    ]
```

**Indicator colors:**
- `"Blue"` - Information
- `"Green"` - Success
- `"Orange"` - Warning
- `"Red"` - Danger
- `"Gray"` - Neutral

## Custom Buttons and Actions

Add custom buttons to report interface.

### Basic Custom Button

```javascript
frappe.query_reports["My Report"] = {
    filters: [...],
    
    onload: function(report) {
        report.page.add_inner_button(__("Export to Excel"), function() {
            // Custom export logic
            export_to_excel(report);
        });
    }
};

function export_to_excel(report) {
    let filters = report.get_filter_values();
    
    frappe.call({
        method: "your_app.reports.my_report.export_to_excel",
        args: {
            filters: filters
        },
        callback: function(r) {
            if (r.message) {
                window.open(r.message);  // Download URL
            }
        }
    });
}
```

### Button with Dialog

```javascript
onload: function(report) {
    report.page.add_inner_button(__("Send Email"), function() {
        let d = new frappe.ui.Dialog({
            title: __("Send Report"),
            fields: [
                {
                    label: __("Recipients"),
                    fieldname: "recipients",
                    fieldtype: "Small Text",
                    reqd: 1,
                    description: __("Comma separated email addresses")
                },
                {
                    label: __("Subject"),
                    fieldname: "subject",
                    fieldtype: "Data",
                    default: "Report: " + report.report_name
                }
            ],
            primary_action_label: __("Send"),
            primary_action: function(values) {
                send_report_email(report, values);
                d.hide();
            }
        });
        d.show();
    }, __("Actions"));
}
```

### Bulk Actions

```javascript
onload: function(report) {
    report.page.add_inner_button(__("Process Selected"), function() {
        let selected = report.get_checked_items();
        
        if (!selected || selected.length === 0) {
            frappe.msgprint(__("Please select at least one item"));
            return;
        }
        
        frappe.confirm(
            __("Process {0} selected items?", [selected.length]),
            function() {
                frappe.call({
                    method: "your_app.reports.my_report.process_items",
                    args: {
                        items: selected.map(s => s.name)
                    },
                    callback: function(r) {
                        frappe.show_alert({
                            message: __("Processed successfully"),
                            indicator: "green"
                        });
                        report.refresh();
                    }
                });
            }
        );
    }, __("Actions"));
}
```

### Dynamic Buttons

Show/hide buttons based on conditions:

```javascript
onload: function(report) {
    // Add button conditionally
    frappe.call({
        method: "frappe.client.get_value",
        args: {
            doctype: "User",
            filters: {name: frappe.session.user},
            fieldname: "role_profile_name"
        },
        callback: function(r) {
            if (r.message && r.message.role_profile_name === "Administrator") {
                report.page.add_inner_button(__("Admin Action"), function() {
                    // Admin-only action
                });
            }
        }
    });
}
```

## Cell Formatting

Custom formatting for table cells.

### Basic Formatter

```javascript
frappe.query_reports["My Report"] = {
    filters: [...],
    
    formatter: function(value, row, column, data, default_formatter) {
        // Use default formatter first
        value = default_formatter(value, row, column, data);
        
        // Custom formatting
        if (column.fieldname === "status") {
            if (value === "Active") {
                value = `<span class="indicator-pill green">${value}</span>`;
            } else if (value === "Inactive") {
                value = `<span class="indicator-pill red">${value}</span>`;
            }
        }
        
        return value;
    }
};
```

### Conditional Styling

```javascript
formatter: function(value, row, column, data, default_formatter) {
    value = default_formatter(value, row, column, data);
    
    // Highlight negative values in red
    if (column.fieldname === "profit" && data && data.profit < 0) {
        value = `<span style="color: red; font-weight: bold;">${value}</span>`;
    }
    
    // Highlight high amounts
    if (column.fieldname === "amount" && data && data.amount > 10000) {
        value = `<span style="background-color: #fffacd; padding: 2px 5px;">${value}</span>`;
    }
    
    return value;
}
```

### Progress Bars

```javascript
formatter: function(value, row, column, data, default_formatter) {
    if (column.fieldname === "completion") {
        // Show progress bar
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

### Custom Links

```javascript
formatter: function(value, row, column, data, default_formatter) {
    if (column.fieldname === "reference_name" && data.reference_type) {
        // Custom link format
        return `<a href="/app/${frappe.router.slug(data.reference_type)}/${value}">${value}</a>`;
    }
    
    return default_formatter(value, row, column, data);
}
```

## Tree Reports

Hierarchical reports with parent-child relationships.

### Enable Tree View

Return an additional parameter to enable tree structure:

```python
def execute(filters=None):
    columns = get_columns()
    data = get_tree_data(filters)
    
    # Return with tree flag
    return columns, data, None, None, None, None, True
```

### Tree Data Structure

Data should include `indent` field for hierarchy:

```python
def get_tree_data(filters):
    data = []
    
    # Parent level
    data.append({
        "account": "Assets",
        "balance": 100000,
        "indent": 0,
        "has_children": 1  # Indicates this row has children
    })
    
    # Child level 1
    data.append({
        "account": "Current Assets",
        "balance": 60000,
        "indent": 1,
        "has_children": 1
    })
    
    # Child level 2
    data.append({
        "account": "Cash",
        "balance": 30000,
        "indent": 2,
        "has_children": 0
    })
    
    data.append({
        "account": "Bank Accounts",
        "balance": 30000,
        "indent": 2,
        "has_children": 0
    })
    
    # Child level 1
    data.append({
        "account": "Fixed Assets",
        "balance": 40000,
        "indent": 1,
        "has_children": 0
    })
    
    return data
```

### Expandable Tree Nodes

```python
def get_tree_data(filters):
    # Query to get hierarchy
    accounts = frappe.db.sql("""
        SELECT 
            name,
            parent_account,
            is_group,
            balance
        FROM `tabAccount`
        WHERE company = %(company)s
        ORDER BY lft
    """, filters, as_dict=1)
    
    data = []
    indent_map = {}
    
    for acc in accounts:
        # Calculate indent level
        if acc.parent_account:
            indent = indent_map.get(acc.parent_account, 0) + 1
        else:
            indent = 0
        
        indent_map[acc.name] = indent
        
        data.append({
            "account": acc.name,
            "balance": acc.balance,
            "indent": indent,
            "has_children": acc.is_group
        })
    
    return data
```

## Prepared Reports

For large reports that take time to generate, use prepared reports.

### Enable Prepared Reports

In report JSON:
```json
{
    "prepared_report": 1,
    "timeout": 300
}
```

### Background Generation

```python
def execute(filters=None):
    # This runs in background for prepared reports
    columns = get_columns()
    data = get_large_dataset(filters)  # Can take several minutes
    
    return columns, data
```

The report will:
1. Queue for background generation
2. Show progress to user
3. Allow user to continue working
4. Notify when ready
5. Cache results for quick viewing

## Report Messages

Show informational messages above the report.

```python
def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    
    # Message to display
    message = """
        <div class="alert alert-info">
            This report shows data as of {date}.
            <a href="/app/help">Learn more</a>
        </div>
    """.format(date=frappe.utils.today())
    
    return columns, data, message
```

## Skip Total Row

Control whether total row is added:

```python
def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    
    # Skip total row
    skip_total_row = True
    
    return columns, data, None, None, None, skip_total_row
```

## Performance Optimization

### Database Query Optimization

```python
def get_data(filters):
    # Use proper indexes
    # Filter early in WHERE clause
    # Use JOINs instead of multiple queries
    
    data = frappe.db.sql("""
        SELECT 
            so.name,
            so.customer,
            so.grand_total,
            c.customer_group
        FROM `tabSales Order` so
        INNER JOIN `tabCustomer` c ON so.customer = c.name
        WHERE so.docstatus = 1
            AND so.company = %(company)s
            AND so.transaction_date BETWEEN %(from_date)s AND %(to_date)s
        ORDER BY so.transaction_date DESC
        LIMIT 1000
    """, filters, as_dict=1)
    
    return data
```

### Caching

```python
def get_cached_reference_data():
    """Cache static reference data"""
    return frappe.cache().get_value(
        "my_report_reference_data",
        generator=lambda: fetch_reference_data(),
        expires_in_sec=3600  # 1 hour
    )
```

### Pagination

```python
def execute(filters=None):
    # Get page info from filters
    page = filters.get("page", 1)
    page_size = filters.get("page_size", 100)
    
    columns = get_columns()
    data = get_paginated_data(filters, page, page_size)
    
    return columns, data

def get_paginated_data(filters, page, page_size):
    offset = (page - 1) * page_size
    
    return frappe.db.sql("""
        SELECT *
        FROM `tabDocType`
        WHERE status = %(status)s
        LIMIT %(page_size)s OFFSET %(offset)s
    """, {
        "status": filters.get("status"),
        "page_size": page_size,
        "offset": offset
    }, as_dict=1)
```

## Error Handling

```python
def execute(filters=None):
    try:
        columns = get_columns()
        data = get_data(filters)
        return columns, data
    except Exception as e:
        frappe.log_error("Report Error", str(e))
        
        # Return empty with message
        message = f"<div class='alert alert-danger'>Error: {str(e)}</div>"
        return [], [], message
```

## Debugging

```python
def execute(filters=None):
    # Enable SQL debugging
    frappe.flags.in_test = True
    
    # Log filter values
    frappe.log_error("Report Filters", frappe.as_json(filters))
    
    columns = get_columns()
    data = get_data(filters)
    
    # Log data structure
    if data:
        frappe.log_error("Report Data Sample", frappe.as_json(data[0]))
    
    return columns, data
```

Use `frappe.throw()` for user-facing errors and `frappe.log_error()` for debugging.
