# Script Report Examples

Complete working examples of various script report patterns.

## Example 1: Basic List Report

Simple report listing documents with filters.

**File: todo_report.py**
```python
# Copyright (c) 2024, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        _("ID") + ":Link/ToDo:90",
        _("Priority") + "::60",
        _("Date") + ":Date:80",
        _("Description") + "::150",
        _("Assigned To") + ":Data:120",
        _("Status") + "::80",
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    
    data = frappe.db.sql("""
        SELECT 
            name,
            priority,
            date,
            description,
            owner,
            status
        FROM `tabToDo`
        WHERE 1=1 {conditions}
        ORDER BY priority DESC, date ASC
    """.format(conditions=conditions), filters, as_list=1)
    
    return data

def get_conditions(filters):
    conditions = ""
    
    if filters.get("status"):
        conditions += " AND status = %(status)s"
    
    if filters.get("priority"):
        conditions += " AND priority = %(priority)s"
    
    if filters.get("assigned_to"):
        conditions += " AND owner = %(assigned_to)s"
    
    if filters.get("from_date"):
        conditions += " AND date >= %(from_date)s"
    
    if filters.get("to_date"):
        conditions += " AND date <= %(to_date)s"
    
    return conditions
```

**File: todo_report.js**
```javascript
// Copyright (c) 2024, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.query_reports["ToDo Report"] = {
    filters: [
        {
            fieldname: "status",
            label: __("Status"),
            fieldtype: "Select",
            options: ["", "Open", "Closed", "Cancelled"],
            default: "Open"
        },
        {
            fieldname: "priority",
            label: __("Priority"),
            fieldtype: "Select",
            options: ["", "Low", "Medium", "High"]
        },
        {
            fieldname: "assigned_to",
            label: __("Assigned To"),
            fieldtype: "Link",
            options: "User"
        },
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date"
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today()
        }
    ]
};
```

## Example 2: Report with Calculations

Report that performs calculations on fetched data.

**File: sales_analysis.py**
```python
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    report_summary = get_summary(data)
    
    return columns, data, None, chart, report_summary

def get_columns():
    return [
        {
            "label": _("Item"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        },
        {
            "label": _("Qty"),
            "fieldname": "qty",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("Rate"),
            "fieldname": "rate",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Amount"),
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Tax (18%)"),
            "fieldname": "tax",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Total"),
            "fieldname": "total",
            "fieldtype": "Currency",
            "width": 120
        }
    ]

def get_data(filters):
    # Fetch raw data
    raw_data = frappe.db.sql("""
        SELECT 
            soi.item_code,
            SUM(soi.qty) as qty,
            AVG(soi.rate) as rate,
            SUM(soi.amount) as amount
        FROM `tabSales Order Item` soi
        INNER JOIN `tabSales Order` so ON soi.parent = so.name
        WHERE so.docstatus = 1
            AND so.transaction_date BETWEEN %(from_date)s AND %(to_date)s
        GROUP BY soi.item_code
        ORDER BY amount DESC
    """, filters, as_dict=1)
    
    # Calculate additional fields
    data = []
    for row in raw_data:
        tax = row.amount * 0.18  # 18% tax
        total = row.amount + tax
        
        data.append({
            "item_code": row.item_code,
            "qty": row.qty,
            "rate": row.rate,
            "amount": row.amount,
            "tax": tax,
            "total": total
        })
    
    return data

def get_chart(data):
    if not data:
        return None
    
    # Get top 10 items for chart
    top_items = data[:10]
    
    return {
        "data": {
            "labels": [d["item_code"] for d in top_items],
            "datasets": [
                {
                    "name": "Sales Amount",
                    "values": [d["amount"] for d in top_items]
                }
            ]
        },
        "type": "bar",
        "height": 300
    }

def get_summary(data):
    if not data:
        return []
    
    total_qty = sum(d["qty"] for d in data)
    total_amount = sum(d["amount"] for d in data)
    total_tax = sum(d["tax"] for d in data)
    grand_total = sum(d["total"] for d in data)
    
    return [
        {
            "value": len(data),
            "label": "Total Items",
            "datatype": "Int"
        },
        {
            "value": total_qty,
            "label": "Total Quantity",
            "datatype": "Float"
        },
        {
            "value": total_amount,
            "label": "Total Amount",
            "datatype": "Currency"
        },
        {
            "value": total_tax,
            "label": "Total Tax",
            "datatype": "Currency"
        },
        {
            "value": grand_total,
            "label": "Grand Total",
            "datatype": "Currency"
        }
    ]
```

**File: sales_analysis.js**
```javascript
frappe.query_reports["Sales Analysis"] = {
    filters: [
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

## Example 3: Grouped/Hierarchical Report

Report with grouped data and indentation.

**File: company_wise_sales.py**
```python
import frappe
from frappe import _
from itertools import groupby

def execute(filters=None):
    columns = get_columns()
    data = get_grouped_data(filters)
    
    return columns, data

def get_columns():
    return [
        {
            "label": _("Company/Customer"),
            "fieldname": "name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Sales Order"),
            "fieldname": "order_id",
            "fieldtype": "Link",
            "options": "Sales Order",
            "width": 150
        },
        {
            "label": _("Date"),
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Amount"),
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 120
        }
    ]

def get_grouped_data(filters):
    # Fetch raw data
    raw_data = frappe.db.sql("""
        SELECT 
            company,
            customer,
            name as order_id,
            transaction_date as date,
            grand_total as amount
        FROM `tabSales Order`
        WHERE docstatus = 1
            AND transaction_date BETWEEN %(from_date)s AND %(to_date)s
        ORDER BY company, customer, transaction_date
    """, filters, as_dict=1)
    
    # Group data
    data = []
    
    # Group by company
    for company, company_rows in groupby(raw_data, key=lambda x: x.company):
        company_rows = list(company_rows)
        company_total = sum(row.amount for row in company_rows)
        
        # Add company header
        data.append({
            "name": f"<b>{company}</b>",
            "order_id": "",
            "date": "",
            "amount": company_total,
            "indent": 0
        })
        
        # Group by customer within company
        for customer, customer_rows in groupby(company_rows, key=lambda x: x.customer):
            customer_rows = list(customer_rows)
            customer_total = sum(row.amount for row in customer_rows)
            
            # Add customer header
            data.append({
                "name": customer,
                "order_id": "",
                "date": "",
                "amount": customer_total,
                "indent": 1
            })
            
            # Add order details
            for row in customer_rows:
                data.append({
                    "name": "",
                    "order_id": row.order_id,
                    "date": row.date,
                    "amount": row.amount,
                    "indent": 2
                })
    
    return data
```

## Example 4: Report with Dynamic Columns

Report where columns are generated based on filters.

**File: monthly_sales.py**
```python
import frappe
from frappe import _
from frappe.utils import getdate, add_months, get_last_day

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters, columns)
    
    return columns, data

def get_columns(filters):
    columns = [
        {
            "label": _("Item"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        }
    ]
    
    # Add month columns dynamically
    date_list = get_month_list(filters.from_date, filters.to_date)
    
    for date in date_list:
        columns.append({
            "label": date.strftime("%b %Y"),
            "fieldname": date.strftime("%Y-%m"),
            "fieldtype": "Currency",
            "width": 100
        })
    
    # Add total column
    columns.append({
        "label": _("Total"),
        "fieldname": "total",
        "fieldtype": "Currency",
        "width": 120
    })
    
    return columns

def get_month_list(from_date, to_date):
    from_date = getdate(from_date)
    to_date = getdate(to_date)
    
    months = []
    current = from_date
    
    while current <= to_date:
        months.append(current)
        current = add_months(current, 1)
    
    return months

def get_data(filters, columns):
    # Get all items
    items = frappe.db.sql("""
        SELECT DISTINCT item_code
        FROM `tabSales Order Item`
    """, as_dict=1)
    
    # Prepare data structure
    data = []
    
    for item in items:
        row = {"item_code": item.item_code}
        row_total = 0
        
        # Get sales for each month
        for col in columns[1:-1]:  # Skip first (item) and last (total) columns
            month_str = col["fieldname"]
            
            # Calculate sales for this month
            sales = frappe.db.sql("""
                SELECT SUM(soi.amount) as amount
                FROM `tabSales Order Item` soi
                INNER JOIN `tabSales Order` so ON soi.parent = so.name
                WHERE soi.item_code = %(item_code)s
                    AND so.docstatus = 1
                    AND DATE_FORMAT(so.transaction_date, '%%Y-%%m') = %(month)s
            """, {"item_code": item.item_code, "month": month_str}, as_dict=1)
            
            amount = sales[0].amount if sales and sales[0].amount else 0
            row[month_str] = amount
            row_total += amount
        
        row["total"] = row_total
        data.append(row)
    
    return data
```

## Example 5: Report with Custom Actions

Report with custom buttons and server-side methods.

**File: pending_invoices.py**
```python
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    
    return columns, data

def get_columns():
    return [
        _("Invoice") + ":Link/Sales Invoice:150",
        _("Customer") + ":Link/Customer:150",
        _("Date") + ":Date:100",
        _("Due Date") + ":Date:100",
        _("Amount") + ":Currency:120",
        _("Outstanding") + ":Currency:120",
        _("Overdue Days") + ":Int:100"
    ]

def get_data(filters):
    data = frappe.db.sql("""
        SELECT 
            name,
            customer,
            posting_date,
            due_date,
            grand_total,
            outstanding_amount,
            DATEDIFF(CURDATE(), due_date) as overdue_days
        FROM `tabSales Invoice`
        WHERE docstatus = 1
            AND outstanding_amount > 0
            AND due_date < CURDATE()
        ORDER BY overdue_days DESC
    """, as_dict=0)
    
    return data

@frappe.whitelist()
def send_reminder(invoice_name):
    """Server-side method to send payment reminder"""
    frappe.only_for("Accounts User")
    
    invoice = frappe.get_doc("Sales Invoice", invoice_name)
    
    # Send email
    frappe.sendmail(
        recipients=invoice.contact_email,
        subject=f"Payment Reminder: {invoice.name}",
        message=f"""
            Dear {invoice.customer_name},
            
            This is a reminder that invoice {invoice.name} 
            dated {invoice.posting_date} is overdue.
            
            Outstanding amount: {invoice.outstanding_amount}
            
            Please arrange payment at the earliest.
        """
    )
    
    frappe.msgprint(f"Reminder sent for {invoice.name}")
```

**File: pending_invoices.js**
```javascript
frappe.query_reports["Pending Invoices"] = {
    filters: [],
    
    onload: function(report) {
        // Add custom button
        report.page.add_inner_button(__("Send Reminders"), function() {
            let selected_invoices = report.get_checked_items();
            
            if (!selected_invoices.length) {
                frappe.msgprint(__("Please select invoices"));
                return;
            }
            
            frappe.confirm(
                __("Send payment reminders for {0} invoices?", [selected_invoices.length]),
                function() {
                    selected_invoices.forEach(function(invoice) {
                        frappe.call({
                            method: "your_app.reports.pending_invoices.send_reminder",
                            args: {
                                invoice_name: invoice.name
                            },
                            callback: function(r) {
                                report.refresh();
                            }
                        });
                    });
                }
            );
        }, __("Actions"));
        
        // Add export button
        report.page.add_inner_button(__("Export to Excel"), function() {
            let filters = report.get_filter_values();
            
            frappe.call({
                method: "your_app.reports.pending_invoices.export_to_excel",
                args: {
                    filters: filters
                },
                callback: function(r) {
                    if (r.message) {
                        window.open(r.message);
                    }
                }
            });
        }, __("Export"));
    },
    
    formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        
        // Highlight overdue by more than 30 days in red
        if (column.fieldname == "overdue_days" && data && data[6] > 30) {
            value = `<span style="color: red; font-weight: bold;">${value}</span>`;
        }
        
        return value;
    }
};
```

## Example 6: Permission-Based Report

Report that respects user permissions.

**File: user_documents.py**
```python
import frappe
from frappe import _
import frappe.permissions

def execute(filters=None):
    frappe.only_for("System Manager")
    
    columns = get_columns()
    data = get_data(filters)
    
    return columns, data

def get_columns():
    return [
        _("Document") + ":Link/DocType:150",
        _("ID") + ":Data:120",
        _("Modified") + ":Datetime:150",
        _("Modified By") + ":Link/User:150"
    ]

def get_data(filters):
    user = filters.get("user") or frappe.session.user
    doctype = filters.get("doctype")
    
    if not doctype:
        return []
    
    # Check if user has permission
    if not frappe.has_permission(doctype, "read", user=user):
        frappe.throw(_("User {0} does not have permission to {1}").format(user, doctype))
    
    # Fetch documents that user has access to
    data = frappe.get_list(
        doctype,
        fields=["name", "modified", "modified_by"],
        user=user,  # This applies user permissions
        order_by="modified desc",
        limit=1000
    )
    
    # Format for display
    result = []
    for doc in data:
        result.append([
            doctype,
            doc.name,
            doc.modified,
            doc.modified_by
        ])
    
    return result
```

## Example 7: Report with Caching

Report that uses caching for expensive operations.

**File: database_stats.py**
```python
import frappe
from frappe import _
from frappe.utils import cint

def execute(filters=None):
    frappe.only_for("System Manager")
    
    columns = get_columns()
    data = get_data_cached()
    
    return columns, data

def get_columns():
    return [
        _("Table") + ":Data:200",
        _("Rows") + ":Int:100",
        _("Size (MB)") + ":Float:100",
        _("Index Size (MB)") + ":Float:100"
    ]

def get_data_cached():
    """Get data with 5 minute cache"""
    cache_key = "database_stats"
    cache_expires = 300  # 5 minutes
    
    data = frappe.cache().get_value(
        cache_key,
        generator=fetch_database_stats,
        expires_in_sec=cache_expires
    )
    
    return data

def fetch_database_stats():
    """Expensive database operation"""
    return frappe.db.sql("""
        SELECT 
            table_name,
            table_rows,
            ROUND(data_length / 1024 / 1024, 2) as data_mb,
            ROUND(index_length / 1024 / 1024, 2) as index_mb
        FROM information_schema.TABLES
        WHERE table_schema = DATABASE()
        ORDER BY (data_length + index_length) DESC
    """, as_list=1)
```

These examples demonstrate various patterns and features available in Frappe Script Reports. Use them as templates for your own reports.
