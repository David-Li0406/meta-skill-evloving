# Jinja Hooks

Jinja hooks extend template rendering with custom methods and filters.

## Jinja Configuration

```python
jinja = {
    "methods": "my_app.utils.jinja_methods",
    "filters": [
        "my_app.utils.jinja_filters.custom_filter",
        "my_app.utils.jinja_filters.another_filter"
    ]
}
```

## Methods

Add functions callable in Jinja templates.

**hooks.py:**
```python
jinja = {
    "methods": "my_app.utils.jinja_methods"
}
```

**utils.py:**
```python
# my_app/utils.py
def get_user_fullname(email):
    import frappe
    return frappe.db.get_value("User", email, "full_name")

def get_company_address(company):
    import frappe
    address = frappe.db.get_value("Address", 
        {"company": company, "is_primary_address": 1}, 
        "address_line1"
    )
    return address or ""

def format_currency_words(amount, currency="INR"):
    from frappe.utils import money_in_words
    return money_in_words(amount, currency)
```

**Usage in templates:**
```jinja
<!-- In print format or web template -->
<p>User: {{ get_user_fullname("user@example.com") }}</p>
<p>Address: {{ get_company_address(doc.company) }}</p>
<p>Amount in words: {{ format_currency_words(doc.total) }}</p>
```

## Filters

Add custom Jinja filters for data transformation.

**hooks.py:**
```python
jinja = {
    "filters": [
        "my_app.utils.jinja_filters"
    ]
}
```

**utils.py:**
```python
# my_app/utils.py
def format_phone(value):
    """Format phone number"""
    if not value:
        return ""
    # Format as (XXX) XXX-XXXX
    value = str(value).replace("-", "").replace(" ", "")
    if len(value) == 10:
        return f"({value[:3]}) {value[3:6]}-{value[6:]}"
    return value

def titlecase(value):
    """Convert to title case"""
    return value.title() if value else ""

def highlight_keywords(text, keywords):
    """Highlight keywords in text"""
    if not text or not keywords:
        return text
    for keyword in keywords:
        text = text.replace(keyword, f"<mark>{keyword}</mark>")
    return text
```

**Usage in templates:**
```jinja
<!-- In templates -->
<p>Phone: {{ doc.phone | format_phone }}</p>
<p>Name: {{ doc.name | titlecase }}</p>
<div>{{ doc.description | highlight_keywords(["important", "urgent"]) }}</div>
```

## Built-in Jinja Filters

Frappe provides several built-in filters:

```jinja
<!-- Date formatting -->
{{ doc.date | frappe.utils.global_date_format }}

<!-- Markdown to HTML -->
{{ doc.description | markdown }}

<!-- Absolute URL -->
{{ "/assets/image.png" | abs_url }}
```

## Examples

### Custom Date Formatting

```python
def format_date_range(start, end):
    from frappe.utils import formatdate
    if not start or not end:
        return ""
    return f"{formatdate(start)} to {formatdate(end)}"
```

```jinja
<p>Period: {{ format_date_range(doc.start_date, doc.end_date) }}</p>
```

### Conditional Formatting

```python
def status_badge(status):
    colors = {
        "Active": "success",
        "Inactive": "secondary",
        "Pending": "warning",
        "Rejected": "danger"
    }
    color = colors.get(status, "info")
    return f'<span class="badge badge-{color}">{status}</span>'
```

```jinja
{{ doc.status | status_badge | safe }}
```

### Data Aggregation

```python
def get_total_items(order_name):
    import frappe
    return frappe.db.count("Order Item", {"parent": order_name})

def get_order_summary(order_name):
    import frappe
    items = frappe.get_all("Order Item",
        filters={"parent": order_name},
        fields=["sum(amount) as total", "count(*) as count"]
    )
    if items:
        return f"{items[0].count} items, Total: {items[0].total}"
    return "No items"
```

```jinja
<p>Total Items: {{ get_total_items(doc.name) }}</p>
<p>Summary: {{ get_order_summary(doc.name) }}</p>
```

### QR Code Generation

```python
def generate_qr_code(data):
    import frappe
    from frappe.utils.qrcode import get_qr_code_svg
    return get_qr_code_svg(data)
```

```jinja
<div>{{ generate_qr_code(doc.name) | safe }}</div>
```

### HTML Sanitization

```python
def safe_html(html_content):
    import frappe
    from frappe.utils.html_utils import clean_html
    return clean_html(html_content)
```

```jinja
<div>{{ doc.description | safe_html | safe }}</div>
```

## Context Functions

Jinja methods can access request context:

```python
def get_current_user_role():
    import frappe
    roles = frappe.get_roles(frappe.session.user)
    return ", ".join(roles)

def has_role(role_name):
    import frappe
    return role_name in frappe.get_roles(frappe.session.user)

def get_website_settings(key):
    import frappe
    return frappe.db.get_single_value("Website Settings", key)
```

```jinja
{% if has_role("Manager") %}
    <div>Manager-only content</div>
{% endif %}

<p>Current User Roles: {{ get_current_user_role() }}</p>
```

## Best Practices

1. **Keep Functions Simple**: Complex logic belongs in controllers
2. **Cache Results**: Cache expensive operations
3. **Error Handling**: Return safe defaults on errors
4. **Security**: Sanitize HTML output, validate inputs
5. **Performance**: Avoid database queries in loops
6. **Use `| safe`**: Mark HTML output as safe when needed

### Cached Method

```python
def get_company_logo(company):
    import frappe
    from frappe.utils import cstr
    
    cache_key = f"company_logo:{company}"
    logo = frappe.cache().get_value(cache_key)
    
    if not logo:
        logo = frappe.db.get_value("Company", company, "logo")
        frappe.cache().set_value(cache_key, logo)
    
    return cstr(logo)
```

### Error-Safe Function

```python
def safe_get_value(doctype, name, fieldname):
    import frappe
    try:
        return frappe.db.get_value(doctype, name, fieldname) or ""
    except Exception:
        return ""
```

## Template Locations

Jinja functions work in:
- Print Formats
- Web Pages
- Web Templates
- Email Templates
- Report Templates

## Notes

- Methods are available as functions: `{{ my_function() }}`
- Filters are applied with pipe: `{{ value | my_filter }}`
- Use `| safe` to output HTML without escaping
- Methods run on each template render; optimize for performance
- Changes require bench restart
