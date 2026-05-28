# Other Hooks

Additional hooks for various extension points.

## Override Hooks

### override_whitelisted_methods

Override or redirect API methods.

```python
override_whitelisted_methods = {
    "frappe.desk.form.save.savedocs": "my_app.overrides.custom_save",
    "frappe.client.get": "my_app.api.custom_get"
}
```

**Example:**
```python
@frappe.whitelist()
def custom_save(doc, action):
    # Custom save logic
    doc = frappe.get_doc(json.loads(doc))
    
    # Add validation
    validate_document(doc)
    
    # Call original or custom save
    doc.save()
    return doc
```

### override_doctype_class

Replace DocType controller class.

```python
override_doctype_class = {
    "ToDo": "my_app.overrides.CustomToDo"
}
```

**Example:**
```python
# my_app/overrides.py
from frappe.desk.doctype.todo.todo import ToDo

class CustomToDo(ToDo):
    def validate(self):
        super().validate()
        # Custom validation
        if not self.priority:
            self.priority = "Medium"
```

### override_doctype_dashboards

Customize DocType dashboards.

```python
override_doctype_dashboards = {
    "Customer": "my_app.dashboard.get_customer_dashboard"
}
```

**Example:**
```python
def get_customer_dashboard(data):
    # Add custom dashboard data
    data['transactions'].append({
        'label': 'Custom Transactions',
        'items': ['Custom DocType']
    })
    return data
```

## Session Hooks

### on_session_creation

Runs when user session is created.

```python
on_session_creation = [
    "my_app.auth.on_session_creation"
]
```

**Example:**
```python
def on_session_creation(login_manager):
    import frappe
    
    # Log login
    frappe.get_doc({
        "doctype": "Login Log",
        "user": frappe.session.user,
        "timestamp": frappe.utils.now()
    }).insert(ignore_permissions=True)
```

### on_login

Runs after successful login.

```python
on_login = "my_app.auth.on_login"
```

**Example:**
```python
def on_login(login_manager):
    import frappe
    
    # Update last login
    frappe.db.set_value("User", frappe.session.user, 
        "last_login", frappe.utils.now())
    
    # Show welcome message
    frappe.msgprint(f"Welcome, {frappe.session.user}!")
```

### on_logout

Runs when user logs out.

```python
on_logout = "my_app.auth.on_logout"
```

**Example:**
```python
def on_logout(login_manager):
    import frappe
    
    # Cleanup user session data
    cleanup_session_files(frappe.session.user)
```

### auth_hooks

Custom authentication validation.

```python
auth_hooks = [
    "my_app.auth.validate_auth"
]
```

**Example:**
```python
def validate_auth(user, password):
    # Custom authentication logic
    if not is_valid_password_format(password):
        frappe.throw("Password format invalid")
```

## Safe Execution Hooks

Frappe uses RestrictedPython for safe code execution in Server Scripts, custom reports, and other contexts. These hooks allow apps to extend the available globals in safe execution environments.

### safe_exec_globals

Extend available globals in `frappe.safe_exec()` contexts.

```python
safe_exec_globals = [
    "my_app.safe_exec.get_safe_exec_globals"
]
```

**Function signature:**
```python
def get_safe_exec_globals(current_globals):
    """
    Add custom functions or data for safe execution contexts.
    
    Args:
        current_globals: Dict of currently available globals
    
    Returns:
        dict: Additional globals to make available
    """
```

**Context:** `frappe.safe_exec()` is used in:
- Server Scripts (DocType, API, Scheduler, Permission Query)
- Custom Report scripts
- Notification conditions
- Assignment Rule conditions
- Custom Print Format scripts
- Webhooks

**Available by default in safe_exec:**
- `frappe` module with core functions (db, utils, etc.)
- Common Python builtins (len, range, enumerate, etc.)
- Safe versions of imports (json, math, etc.)

**Use cases:**
- Add app-specific helper functions
- Expose custom APIs for server scripts
- Provide utility functions for report scripts
- Add domain-specific calculations

**Example 1: Add utility functions:**
```python
def get_safe_exec_globals(current_globals):
    """Add custom utility functions."""
    
    def calculate_tax(amount, rate):
        """Calculate tax with proper rounding."""
        return round(amount * rate / 100, 2)
    
    def format_currency(amount, currency="USD"):
        """Format amount as currency."""
        import frappe.utils
        return frappe.utils.fmt_money(amount, currency=currency)
    
    def get_exchange_rate(from_currency, to_currency):
        """Get latest exchange rate."""
        return frappe.db.get_value(
            "Currency Exchange",
            {"from_currency": from_currency, "to_currency": to_currency},
            "exchange_rate"
        )
    
    return {
        "calculate_tax": calculate_tax,
        "format_currency": format_currency,
        "get_exchange_rate": get_exchange_rate,
    }

# Usage in Server Script:
# total = calculate_tax(base_amount, tax_rate)
# display = format_currency(total, "EUR")
```

**Example 2: Add business logic helpers:**
```python
def get_safe_exec_globals(current_globals):
    """Add business-specific functions."""
    
    def get_customer_credit_limit(customer):
        """Get effective credit limit for customer."""
        return frappe.db.get_value("Customer", customer, "credit_limit") or 0
    
    def is_holiday(date):
        """Check if date is a holiday."""
        return frappe.db.exists("Holiday", {"holiday_date": date})
    
    def get_working_days(start_date, end_date):
        """Calculate working days between dates."""
        from frappe.utils import date_diff, get_datetime
        days = date_diff(end_date, start_date)
        # Subtract weekends and holidays
        # (simplified example)
        return max(0, days - (days // 7 * 2))
    
    return {
        "get_customer_credit_limit": get_customer_credit_limit,
        "is_holiday": is_holiday,
        "get_working_days": get_working_days,
    }

# Usage in Assignment Rule condition:
# doc.total_amount <= get_customer_credit_limit(doc.customer)
```

**Example 3: Add custom API access:**
```python
def get_safe_exec_globals(current_globals):
    """Expose custom app APIs."""
    
    class CustomAPI:
        @staticmethod
        def get_inventory_status(item_code):
            """Get real-time inventory status."""
            # Call custom inventory system
            return frappe.call("my_app.inventory.get_status", item=item_code)
        
        @staticmethod
        def check_compliance(doc_type, doc_name):
            """Check document compliance status."""
            return frappe.call("my_app.compliance.check", 
                             doctype=doc_type, name=doc_name)
    
    return {
        "CustomAPI": CustomAPI,
    }

# Usage in Server Script:
# status = CustomAPI.get_inventory_status("ITEM-001")
```

**Security considerations:**
- Functions run in RestrictedPython sandbox
- Avoid exposing functions that bypass security
- Validate inputs in your functions
- Don't provide direct file system or system access
- Use frappe's permission system within functions

### safe_eval_globals

Extend available globals in `frappe.safe_eval()` contexts.

```python
safe_eval_globals = [
    "my_app.safe_eval.get_safe_eval_globals"
]
```

**Function signature:**
```python
def get_safe_eval_globals(current_globals):
    """
    Add custom functions or data for safe evaluation contexts.
    
    Args:
        current_globals: Dict of currently available globals
    
    Returns:
        dict: Additional globals to make available
    """
```

**Context:** `frappe.safe_eval()` is used in:
- Formula fields (e.g., calculated field expressions)
- Assignment Rule conditions (simple expressions)
- Notification conditions (simple expressions)
- Custom validation expressions
- Dynamic defaults evaluation

**Available by default in safe_eval:**
- Limited set of safe functions (much more restricted than safe_exec)
- Basic arithmetic and comparison operators
- Common Python builtins (max, min, abs, round, etc.)

**Use cases:**
- Add helper functions for formula fields
- Provide constants for calculations
- Add custom comparison functions

**Example 1: Add mathematical functions:**
```python
def get_safe_eval_globals(current_globals):
    """Add math helpers for formula fields."""
    import math
    
    def percentage(value, total):
        """Calculate percentage."""
        return (value / total * 100) if total else 0
    
    def clamp(value, min_val, max_val):
        """Clamp value between min and max."""
        return max(min_val, min(value, max_val))
    
    return {
        "percentage": percentage,
        "clamp": clamp,
        "pi": math.pi,
        "sqrt": math.sqrt,
    }

# Usage in formula field:
# percentage(completed_qty, total_qty)
# clamp(discount, 0, 50)
```

**Example 2: Add business constants:**
```python
def get_safe_eval_globals(current_globals):
    """Add business configuration as constants."""
    
    # Load from configuration
    config = frappe.get_single("Business Settings")
    
    return {
        "MIN_ORDER_AMOUNT": config.min_order_amount,
        "MAX_DISCOUNT_PERCENT": config.max_discount_percent,
        "STANDARD_TAX_RATE": config.standard_tax_rate,
        "FREE_SHIPPING_THRESHOLD": config.free_shipping_threshold,
    }

# Usage in formula field:
# total_amount >= FREE_SHIPPING_THRESHOLD
# discount_percent <= MAX_DISCOUNT_PERCENT
```

**Example 3: Add conditional helpers:**
```python
def get_safe_eval_globals(current_globals):
    """Add helper functions for conditions."""
    
    def in_range(value, min_val, max_val):
        """Check if value is in range."""
        return min_val <= value <= max_val
    
    def any_of(value, *options):
        """Check if value matches any option."""
        return value in options
    
    def all_positive(*values):
        """Check if all values are positive."""
        return all(v > 0 for v in values)
    
    return {
        "in_range": in_range,
        "any_of": any_of,
        "all_positive": all_positive,
    }

# Usage in condition:
# in_range(doc.amount, 100, 1000)
# any_of(doc.status, "Approved", "Completed")
```

**Security considerations:**
- Even more restricted than safe_exec
- Keep functions pure (no side effects)
- Avoid database calls in safe_eval contexts (use cached data)
- Don't expose functions that could be exploited in expressions
- safe_eval is for simple expressions, not complex logic

### Differences: safe_exec vs safe_eval

| Aspect | safe_exec | safe_eval |
|--------|-----------|-----------|
| **Purpose** | Execute multi-line scripts | Evaluate single expressions |
| **Context** | Server Scripts, Reports | Formula fields, conditions |
| **Complexity** | Full Python code | Simple expressions only |
| **Default Globals** | Many (frappe, db, utils) | Very few (basic functions) |
| **Database Access** | Yes (via frappe.db) | Limited (via frappe.db in globals) |
| **Performance** | Slower (full execution) | Fast (simple evaluation) |
| **Use Cases** | Complex logic, workflows | Calculations, validations |

**Best practices:**
1. **Use safe_eval_globals for:** Simple functions, constants, calculations
2. **Use safe_exec_globals for:** Complex logic, database operations, integrations
3. **Cache expensive operations:** Load configuration once, not per evaluation
4. **Test thoroughly:** Test functions with various inputs
5. **Document well:** Add clear docstrings for functions
6. **Keep it simple:** Don't overcomplicate the execution environment

## Notification Hook

### notification_config

Configuration for notifications.

```python
notification_config = "my_app.notifications.get_notification_config"
```

**Example:**
```python
def get_notification_config():
    return {
        "for_doctype": {
            "Task": {"status": "Open"},
            "Issue": {"status": "Open"}
        }
    }
```

## Search Hooks

### standard_queries

Custom search queries for link fields.

```python
standard_queries = {
    "Customer": "my_app.queries.customer_query"
}
```

**Example:**
```python
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def customer_query(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
        SELECT name, customer_name, territory
        FROM `tabCustomer`
        WHERE customer_name LIKE %(txt)s
        ORDER BY name
        LIMIT %(start)s, %(page_len)s
    """, {
        'txt': f"%{txt}%",
        'start': start,
        'page_len': page_len
    })
```

### global_search_doctypes

Configure which doctypes appear in global search.

```python
global_search_doctypes = {
    "Sales": [
        {"doctype": "Sales Order"},
        {"doctype": "Customer"}
    ],
    "HR": [
        {"doctype": "Employee"},
        {"doctype": "Leave Application"}
    ]
}
```

## Data Management Hooks

### user_data_fields

Configure GDPR data protection.

```python
user_data_fields = [
    {
        "doctype": "Comment",
        "filter_by": "owner",
        "redact_fields": ["content"]
    },
    {
        "doctype": "Customer",
        "filter_by": "email_id",
        "redact_fields": ["customer_name", "phone"],
        "rename": True
    }
]
```

### ignore_links_on_delete

Skip link validation when deleting.

```python
ignore_links_on_delete = [
    "Comment",
    "Activity Log",
    "Version"
]
```

### auto_cancel_exempted_doctypes

Exempt from automatic cancellation.

```python
auto_cancel_exempted_doctypes = [
    "Auto Repeat",
    "Scheduled Job"
]
```

## Website Hooks

### update_website_context

Add data to website page context.

```python
update_website_context = [
    "my_app.website.update_context"
]
```

**Example:**
```python
def update_context(context):
    # Add custom data to all website pages
    context['custom_footer'] = get_custom_footer()
    context['social_links'] = get_social_links()
```

## Log Management

### default_log_clearing_doctypes

Auto-cleanup old logs.

```python
default_log_clearing_doctypes = {
    "Custom Log": 30,  # Delete after 30 days
    "API Log": 7       # Delete after 7 days
}
```

## PDF Hooks

### pdf_header_html / pdf_footer_html / pdf_body_html

Customize PDF generation.

```python
pdf_header_html = "my_app.utils.pdf.get_header"
pdf_footer_html = "my_app.utils.pdf.get_footer"
```

**Example:**
```python
def get_header(html, kwargs):
    return f"<div class='header'>{kwargs.get('company', '')}</div>"

def get_footer(html, kwargs):
    return f"<div class='footer'>Page {kwargs.get('page', '')}</div>"
```

## Fixture Hook

### fixtures

Export/import data during migrations.

```python
fixtures = [
    "Custom Field",
    "Role",
    {
        "doctype": "Custom Field",
        "filters": [["module", "=", "My App"]]
    }
]
```

Data exported to `fixtures/` directory during `bench export-fixtures`.

## Telemetry Hook

### get_changelog_feed

Provide changelog feed.

```python
get_changelog_feed = "my_app.utils.get_changelog"
```

## Notes

- Most hooks require bench restart
- Override hooks can break core functionality
- Test overrides thoroughly
- Document custom hooks well
- Use sparingly to maintain compatibility
