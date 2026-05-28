# Application Hooks

Application hooks define basic metadata and configuration for your Frappe app.

## Required Hooks

### App Identity

```python
app_name = "my_app"  # Slug (snake_case)
app_title = "My App"  # Display name
app_publisher = "Your Company"
app_description = "Description of your app"
app_email = "contact@example.com"
app_license = "MIT"  # or "GPL", "AGPL", etc.
```

## Optional Configuration Hooks

### App Dependencies

**required_apps** - List apps that must be installed first

```python
required_apps = ["frappe", "erpnext"]
```

### Apps Screen Configuration

**add_to_apps_screen** - Show app on apps page

```python
add_to_apps_screen = [
    {
        "name": "my_app",
        "logo": "/assets/my_app/logo.png",
        "title": "My App",
        "route": "/my_app",
        "has_permission": "my_app.api.has_app_permission"
    }
]
```

### Home Page Configuration

**home_page** - Override default home page

```python
home_page = "custom-home"
```

**role_home_page** - Role-based home pages

```python
role_home_page = {
    "Sales User": "sales-dashboard",
    "Purchase User": "purchase-dashboard",
}
```

### Website Generators

**website_generators** - Auto-create pages for doctypes

```python
website_generators = ["Blog Post", "Product"]
```

Creates `/blog-post/[name]` and `/product/[name]` routes.

### URL Routing

**website_route_rules** - Custom URL patterns

```python
website_route_rules = [
    {"from_route": "/shop/<category>", "to_route": "Product"},
    {"from_route": "/articles/<name>", "to_route": "Blog Post"},
]
```

**website_redirects** - URL redirects

```python
website_redirects = [
    {"source": "/old-page", "target": "/new-page"},
    {"source": r"/blog/(.*)", "target": r"/articles/\1"},  # Regex
]
```

### Export Configuration

**export_python_type_annotations** - Enable type annotations

```python
export_python_type_annotations = True
```

Generates type stubs for IDE support.

### Default Data

**fixtures** - Export/import data during migrations

```python
fixtures = [
    "Custom Field",
    {
        "doctype": "Role",
        "filters": [["name", "in", ["Custom Role 1", "Custom Role 2"]]]
    },
]
```

Data is exported to `fixtures/` directory.

## Examples

### Minimal App

```python
app_name = "simple_app"
app_title = "Simple App"
app_publisher = "Your Name"
app_description = "A simple Frappe app"
app_email = "you@example.com"
app_license = "MIT"
```

### App with Dependencies

```python
app_name = "custom_erp"
app_title = "Custom ERP"
app_publisher = "Your Company"
app_description = "ERP customizations"
app_email = "contact@company.com"
app_license = "MIT"

required_apps = ["erpnext"]

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [["module", "=", "Custom ERP"]]
    },
]
```

### App with Custom Routing

```python
app_name = "portal_app"
app_title = "Portal App"
# ... other metadata ...

website_generators = ["Article", "Course"]

website_route_rules = [
    {"from_route": "/articles/<category>", "to_route": "Article"},
    {"from_route": "/courses/<name>", "to_route": "Course"},
]

website_redirects = [
    {"source": "/blog", "target": "/articles"},
]

home_page = "portal-home"

role_home_page = {
    "Student": "my-courses",
    "Teacher": "course-management",
}
```

## Best Practices

1. **App Name**: Use snake_case, no spaces or special characters
2. **Dependencies**: Only list direct dependencies
3. **Fixtures**: Export only necessary data, use filters
4. **Versioning**: Update `app_version` for releases
5. **License**: Choose appropriate open source license

## Notes

- Changes to most application hooks require app reinstall or bench restart
- App name must match directory name
- Fixtures are imported during `bench migrate`
- Website generators create routes automatically
