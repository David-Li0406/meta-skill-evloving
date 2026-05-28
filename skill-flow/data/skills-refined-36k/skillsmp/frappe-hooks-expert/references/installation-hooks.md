# Installation Hooks

Installation hooks allow you to run custom code during app installation, uninstallation, and migrations.

## Installation Lifecycle Hooks

### before_install

Runs before app is installed.

```python
before_install = "my_app.install.before_install"
```

**Use cases:**
- Check prerequisites
- Validate environment
- Display installation messages

```python
def before_install():
    import frappe
    
    # Check Python version
    import sys
    if sys.version_info < (3, 10):
        frappe.throw("Python 3.10+ required")
    
    # Check for required system packages
    try:
        import required_package
    except ImportError:
        frappe.throw("Please install required_package")
```

### after_install

Runs after app is installed.

```python
after_install = "my_app.install.after_install"
```

**Use cases:**
- Create default records
- Initialize settings
- Run setup wizard
- Create custom fields

```python
def after_install():
    import frappe
    
    # Create default records
    if not frappe.db.exists("Company", "Default Company"):
        frappe.get_doc({
            "doctype": "Company",
            "company_name": "Default Company",
        }).insert()
    
    # Initialize settings
    frappe.db.set_single_value("System Settings", "custom_field", "default_value")
    
    # Create custom fields
    from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
    create_custom_fields({
        "Customer": [
            {
                "fieldname": "custom_rating",
                "label": "Rating",
                "fieldtype": "Int",
            }
        ]
    })
```

## Uninstallation Hooks

### before_uninstall

Runs before app is uninstalled.

```python
before_uninstall = "my_app.uninstall.before_uninstall"
```

**Use cases:**
- Backup data
- Warn about data loss
- Check for dependencies

```python
def before_uninstall():
    import frappe
    
    # Check if other apps depend on this
    dependent_apps = get_dependent_apps()
    if dependent_apps:
        frappe.throw(f"Cannot uninstall: Required by {', '.join(dependent_apps)}")
    
    # Backup important data
    backup_custom_data()
```

### after_uninstall

Runs after app is uninstalled.

```python
after_uninstall = "my_app.uninstall.after_uninstall"
```

**Use cases:**
- Clean up files
- Remove custom fields
- Final cleanup

```python
def after_uninstall():
    import frappe
    
    # Remove custom fields
    frappe.db.delete("Custom Field", {"module": "My App"})
    
    # Clean up files
    import os
    file_path = frappe.get_site_path("public", "files", "my_app")
    if os.path.exists(file_path):
        import shutil
        shutil.rmtree(file_path)
```

## Inter-App Hooks

### before_app_install / after_app_install

Runs when another app is installed.

```python
before_app_install = "my_app.integrations.before_app_install"
after_app_install = "my_app.integrations.after_app_install"
```

**Function signature:**
```python
def after_app_install(app_name):
    """
    Args:
        app_name: Name of app being installed
    """
    if app_name == "erpnext":
        setup_erpnext_integration()
```

### before_app_uninstall / after_app_uninstall

Runs when another app is uninstalled.

```python
before_app_uninstall = "my_app.integrations.before_app_uninstall"
after_app_uninstall = "my_app.integrations.after_app_uninstall"
```

## Migration Hooks

### before_migrate

Runs before migrations execute.

```python
before_migrate = "my_app.patches.before_migrate"
```

**Use cases:**
- Backup data before migrations
- Prepare database
- Check migration prerequisites

```python
def before_migrate():
    import frappe
    
    # Backup critical data
    backup_critical_tables()
    
    # Check disk space
    if get_free_disk_space() < required_space:
        frappe.throw("Insufficient disk space")
```

### after_migrate

Runs after migrations complete.

```python
after_migrate = "my_app.patches.after_migrate"
```

**Use cases:**
- Rebuild indices
- Clear caches
- Run data migrations
- Update search index

```python
def after_migrate():
    import frappe
    
    # Clear all caches
    frappe.clear_cache()
    
    # Rebuild search index
    from frappe.utils.global_search import rebuild_for_doctype
    rebuild_for_doctype("Custom DocType")
    
    # Run post-migration tasks
    update_calculated_fields()
```

## Testing Hooks

### before_tests

Runs before test suite executes.

```python
before_tests = "my_app.testing.before_tests"
```

**Use cases:**
- Create test data
- Initialize test environment
- Mock external services

```python
def before_tests():
    import frappe
    
    # Create test user
    if not frappe.db.exists("User", "test@example.com"):
        frappe.get_doc({
            "doctype": "User",
            "email": "test@example.com",
            "first_name": "Test",
        }).insert()
    
    # Create test data
    create_test_fixtures()
    
    # Mock external API
    mock_external_services()
```

## Examples

### Complete Installation Flow

```python
# hooks.py
before_install = "my_app.install.before_install"
after_install = "my_app.install.after_install"
before_migrate = "my_app.install.before_migrate"
after_migrate = "my_app.install.after_migrate"

# install.py
def before_install():
    """Check prerequisites"""
    check_system_requirements()
    check_dependencies()

def after_install():
    """Setup app"""
    create_default_records()
    setup_custom_fields()
    initialize_settings()
    run_initial_sync()

def before_migrate():
    """Prepare for migration"""
    frappe.db.commit()  # Commit any pending changes
    backup_data()

def after_migrate():
    """Post-migration tasks"""
    frappe.clear_cache()
    rebuild_search_index()
    notify_admins("Migration completed")
```

### Conditional Setup

```python
def after_install():
    import frappe
    
    # Only create demo data in development
    if frappe.conf.developer_mode:
        create_demo_data()
    
    # Setup integration if other app exists
    if "erpnext" in frappe.get_installed_apps():
        setup_erpnext_integration()
```

### App Integration

```python
def after_app_install(app_name):
    """Setup integration with newly installed app"""
    
    integrations = {
        "erpnext": setup_erpnext_integration,
        "hrms": setup_hrms_integration,
    }
    
    if app_name in integrations:
        integrations[app_name]()

def setup_erpnext_integration():
    """Configure ERPNext-specific features"""
    # Add custom fields to ERPNext doctypes
    # Setup item synchronization
    # Configure accounting integration
```

## Best Practices

1. **Idempotency**: Make installation hooks re-runnable
2. **Error Handling**: Use try-except to handle failures gracefully
3. **Logging**: Log important steps for debugging
4. **Transactions**: Commit database changes explicitly
5. **Validation**: Check prerequisites before proceeding
6. **Cleanup**: Remove temporary data and files
7. **Testing**: Test install/uninstall in development

## Common Patterns

### Check if Already Setup

```python
def after_install():
    if frappe.db.get_single_value("My App Settings", "setup_complete"):
        return  # Already setup
    
    # Run setup
    setup_app()
    
    frappe.db.set_single_value("My App Settings", "setup_complete", 1)
```

### Conditional Installation

```python
def after_install():
    # Ask user for setup options
    if frappe.flags.in_install:
        # Full setup
        full_setup()
    else:
        # Minimal setup
        minimal_setup()
```

### Safe Cleanup

```python
def after_uninstall():
    try:
        # Remove custom fields
        remove_custom_fields()
    except Exception as e:
        frappe.log_error(f"Cleanup failed: {str(e)}")
    
    try:
        # Delete files
        delete_app_files()
    except Exception as e:
        frappe.log_error(f"File deletion failed: {str(e)}")
```

## Notes

- Installation hooks run once during `bench install-app`
- Migration hooks run during `bench migrate`
- Use `frappe.flags.in_install` to detect installation context
- Hooks don't have access to HTTP request context
- Database changes should be committed explicitly
- Errors in hooks will stop installation/migration
