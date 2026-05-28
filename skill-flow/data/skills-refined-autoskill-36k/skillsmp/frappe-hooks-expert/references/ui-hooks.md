# UI and Frontend Hooks

UI hooks customize the Frappe desk and website interface.

## Desk Assets

### app_include_js / app_include_css

Include JS/CSS in all desk pages.

```python
app_include_js = [
    "/assets/my_app/js/custom.js",
    "/assets/my_app/js/utils.js"
]

app_include_css = [
    "/assets/my_app/css/custom.css"
]
```

### app_include_icons

Include SVG icon bundle.

```python
app_include_icons = "my_app/public/icons.svg"
```

## DocType UI Customization

### doctype_js

Add custom JS to doctype forms.

```python
doctype_js = {
    "Sales Order": "public/js/sales_order.js",
    "Customer": "public/js/customer.js"
}
```

**Example JS file:**
```javascript
// public/js/sales_order.js
frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        // Add custom button
        frm.add_custom_button('Custom Action', () => {
            // Your logic
        });
    },
    
    customer: function(frm) {
        // On field change
        if (frm.doc.customer) {
            // Fetch and set values
        }
    }
});
```

### doctype_list_js

Customize list view behavior.

```python
doctype_list_js = {
    "Task": "public/js/task_list.js"
}
```

**Example:**
```javascript
// public/js/task_list.js
frappe.listview_settings['Task'] = {
    add_fields: ["status", "priority"],
    
    onload: function(listview) {
        // Add custom filter button
    },
    
    get_indicator: function(doc) {
        // Custom list indicators
        if (doc.status === "Completed") {
            return [__("Completed"), "green", "status,=,Completed"];
        }
    }
};
```

### doctype_tree_js

Customize tree view.

```python
doctype_tree_js = {
    "Account": "public/js/account_tree.js"
}
```

### doctype_calendar_js

Customize calendar view.

```python
doctype_calendar_js = {
    "Event": "public/js/event_calendar.js"
}
```

## Page Customization

### page_js

Add JS to specific pages.

```python
page_js = {
    "my-page": "public/js/my_page.js"
}
```

## Website Assets

### web_include_js / web_include_css

Include assets on website pages.

```python
web_include_js = [
    "/assets/my_app/js/web.js"
]

web_include_css = [
    "/assets/my_app/css/web.css"
]
```

### website_theme_scss

Custom SCSS for website themes.

```python
website_theme_scss = "my_app/public/scss/website"
```

## Web Form Assets

### webform_include_js / webform_include_css

Add assets to web forms.

```python
webform_include_js = {
    "contact-us": "public/js/contact_form.js"
}

webform_include_css = {
    "contact-us": "public/css/contact_form.css"
}
```

## Navbar and Help Menu

### standard_navbar_items

Add items to navbar dropdown.

```python
standard_navbar_items = [
    {
        "item_label": "My Custom Link",
        "item_type": "Route",
        "route": "/app/my-page",
        "is_standard": 0,
    },
    {
        "item_label": "Custom Action",
        "item_type": "Action",
        "action": "my_app.show_dialog()",
        "is_standard": 0,
    }
]
```

### standard_help_items

Add items to help menu.

```python
standard_help_items = [
    {
        "item_label": "Documentation",
        "item_type": "Route",
        "route": "https://docs.example.com",
        "is_standard": 0,
    }
]
```

## Examples

### Custom Form Behavior

```javascript
frappe.ui.form.on('Sales Order', {
    setup: function(frm) {
        // Setup custom queries
        frm.set_query('item_code', 'items', function() {
            return {
                filters: {
                    'item_group': 'Products'
                }
            };
        });
    },
    
    onload: function(frm) {
        // On form load
        frm.set_df_property('field_name', 'read_only', 1);
    },
    
    refresh: function(frm) {
        if (frm.doc.docstatus == 1) {
            frm.add_custom_button(__('Create Delivery'), function() {
                frappe.call({
                    method: 'my_app.api.create_delivery',
                    args: {
                        'sales_order': frm.doc.name
                    },
                    callback: function(r) {
                        frappe.msgprint(__('Delivery Note created'));
                    }
                });
            });
        }
    }
});
```

### List View Bulk Actions

```javascript
frappe.listview_settings['Task'] = {
    onload: function(listview) {
        listview.page.add_action_item(__('Bulk Complete'), function() {
            let selected = listview.get_checked_items();
            frappe.call({
                method: 'my_app.api.bulk_complete',
                args: {
                    'tasks': selected
                }
            });
        });
    }
};
```

### Dynamic Field Dependencies

```javascript
frappe.ui.form.on('Sales Order', {
    customer: function(frm) {
        if (frm.doc.customer) {
            frappe.db.get_value('Customer', frm.doc.customer, 'territory')
                .then(r => {
                    if (r.message) {
                        frm.set_value('territory', r.message.territory);
                    }
                });
        }
    }
});
```

## Best Practices

1. **Load Order**: UI scripts load after core Frappe JS
2. **Translations**: Use `__()` for translatable strings
3. **Performance**: Minimize custom JS, use frappe.call sparingly
4. **Clean Up**: Remove event listeners when appropriate
5. **Asset Building**: Run `bench build` after JS/CSS changes

## Notes

- Changes to JS/CSS require `bench build`
- Use `bench watch` for automatic rebuilding in development
- Custom scripts can access `frappe`, `$`, and other globals
- DocType JS runs when form loads
- List/Tree JS runs when respective view loads
