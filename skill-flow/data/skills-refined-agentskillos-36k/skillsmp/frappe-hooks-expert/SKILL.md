---
name: frappe-hooks-expert
description: Expert guidance on Frappe hooks system including application hooks, document events (doc_events), permission hooks, scheduler hooks, UI hooks, jinja filters, installation hooks, and other extension points. Use when implementing custom hooks, understanding hook execution order, registering hooks in hooks.py, troubleshooting hook issues, or extending Frappe framework functionality.
---

# Frappe Hooks Expert

This skill provides comprehensive guidance for understanding and working with Frappe's hooks system.

## Overview

Frappe's hooks system allows apps to extend and customize framework behavior without modifying core code. Hooks are registered in an app's `hooks.py` file and are called by the framework at specific points during execution.

**Core Concept**: Hooks are extension points that allow your app to:
- React to document lifecycle events
- Extend permissions logic
- Schedule background tasks
- Customize UI behavior
- Add custom validations
- Integrate with external systems

## Hook Categories

### 1. Application Hooks
Basic app metadata and configuration:
- `app_name`, `app_title`, `app_publisher`, `app_description`, `app_email`, `app_license`
- `required_apps` - List of dependencies
- `add_to_apps_screen` - App configuration for apps page

**When to read:** See [references/application-hooks.md](references/application-hooks.md) for app metadata and configuration details.

### 2. Installation Hooks
Execute code during app lifecycle:
- `before_install` / `after_install` - Run during app installation
- `before_uninstall` / `after_uninstall` - Run during app removal
- `before_app_install` / `after_app_install` - When other apps install
- `before_app_uninstall` / `after_app_uninstall` - When other apps uninstall
- `before_migrate` / `after_migrate` - Run during migrations
- `before_tests` - Setup before running tests

**When to read:** See [references/installation-hooks.md](references/installation-hooks.md) for installation and migration hooks.

### 3. Document Hooks (doc_events)
React to document lifecycle events:
- `before_insert`, `after_insert` - Document creation
- `before_save`, `after_save` - Document save
- `before_submit`, `after_submit` - Document submission
- `before_cancel`, `after_cancel` - Document cancellation
- `before_update_after_submit`, `after_update_after_submit` - Submitted doc edits
- `on_update`, `on_cancel`, `on_trash` - Common events
- `on_change` - When any field changes
- `before_rename`, `after_rename` - Document renaming
- `before_print`, `after_print` - Print events

**When to read:** See [references/document-hooks.md](references/document-hooks.md) for complete document event hooks with 20+ examples.

### 4. Permission Hooks
Extend permission logic:
- `permission_query_conditions` - Filter documents in list views
- `has_permission` - Custom document-level permissions
- `write_permission_query_conditions` - Validate writes before commit
- `has_website_permission` - Portal/website access control
- `filter_workflow_transitions` - Customize workflow transitions
- `has_workflow_action_permission` - Control workflow action visibility
- `workflow_safe_eval_globals` - Extend available globals in workflow transition conditions

**When to read:** See [references/permission-hooks.md](references/permission-hooks.md) for permission extension hooks.

### 5. Scheduler Hooks
Schedule background tasks:
- `scheduler_events` - Cron-based task scheduling
  - `all` - Every event (every few minutes)
  - `cron` - Custom cron expressions
  - `hourly`, `hourly_maintenance` - Hourly tasks
  - `daily`, `daily_long`, `daily_maintenance` - Daily tasks
  - `weekly`, `weekly_long` - Weekly tasks
  - `monthly`, `monthly_long` - Monthly tasks

**When to read:** See [references/scheduler-hooks.md](references/scheduler-hooks.md) for scheduled task configuration.

### 6. UI and Frontend Hooks
Customize user interface:
- `app_include_js` / `app_include_css` - Desk assets
- `web_include_js` / `web_include_css` - Website assets
- `doctype_js` / `doctype_list_js` / `doctype_tree_js` / `doctype_calendar_js` - DocType UI
- `page_js` - Page customization
- `webform_include_js` / `webform_include_css` - Web form assets
- `app_include_icons` - SVG icon bundles
- `standard_navbar_items` - Navbar menu items
- `standard_help_items` - Help menu items

**When to read:** See [references/ui-hooks.md](references/ui-hooks.md) for frontend customization hooks.

### 7. Jinja Hooks
Extend template rendering:
- `jinja` - Add methods and filters to Jinja environment
  - `methods` - Custom functions in templates
  - `filters` - Custom Jinja filters

**When to read:** See [references/jinja-hooks.md](references/jinja-hooks.md) for template customization.

### 8. Request and Job Hooks
Intercept HTTP requests and background jobs:
- `before_request` / `after_request` - HTTP request lifecycle
- `before_job` / `after_job` - Background job lifecycle
- `extend_bootinfo` - Add data to initial page load

**When to read:** See [references/request-job-hooks.md](references/request-job-hooks.md) for request and job lifecycle hooks.

### 9. Safe Execution Hooks
Extend safe code execution environments:
- `safe_exec_globals` - Add globals for Server Scripts, reports, and custom code execution
- `safe_eval_globals` - Add globals for formula fields and simple expressions

**When to read:** See [references/other-hooks.md](references/other-hooks.md) for safe execution hooks, differences, and best practices.

### 10. Other Hooks
Additional extension points:
- `override_whitelisted_methods` - Override API methods
- `override_doctype_class` - Replace DocType controllers
- `override_doctype_dashboards` - Customize dashboards
- `fixtures` - Export/import data during migrations
- `on_session_creation` / `on_login` / `on_logout` - Session events
- `auth_hooks` - Custom authentication logic
- `notification_config` - Notification configuration
- `standard_queries` - Custom search queries
- `global_search_doctypes` - Configure global search
- `user_data_fields` - GDPR data protection
- `ignore_links_on_delete` - Skip link validation
- `auto_cancel_exempted_doctypes` - Exempt from auto-cancel
- `website_generators` - Create website pages from docs
- `website_route_rules` - Custom URL routing
- `website_redirects` - URL redirects
- `update_website_context` - Modify website context
- `default_log_clearing_doctypes` - Auto-cleanup logs

**When to read:** See [references/other-hooks.md](references/other-hooks.md) for additional hooks and extension points.

## Quick Reference

### Hook Registration Format

Hooks are registered in `{app_name}/hooks.py`:

```python
# Single function
hook_name = "app_name.module.function_name"

# Multiple functions (executed in order)
hook_name = [
    "app_name.module.function1",
    "app_name.module.function2",
]

# Dictionary mapping (doctype/key specific)
hook_name = {
    "DocType Name": "app_name.module.function",
    "Another DocType": "app_name.module.another_function",
}

# Nested structure (doc_events)
doc_events = {
    "*": {  # All doctypes
        "on_update": "app_name.utils.on_any_update",
    },
    "Specific DocType": {
        "before_save": "app_name.doctype_utils.validate",
        "after_insert": [
            "app_name.utils.notify",
            "app_name.utils.log_creation",
        ],
    },
}
```

### Function Signatures

**Document hooks:**
```python
def hook_function(doc, method=None):
    """
    Args:
        doc: Document instance being processed
        method: Event name (e.g., "on_update")
    """
    pass
```

**Permission hooks:**
```python
def has_permission(doc, ptype=None, user=None, debug=False):
    """Return True/False/None"""
    pass

def get_permission_query_conditions(user=None, doctype=None):
    """Return SQL WHERE clause string"""
    pass
```

**Scheduler hooks:**
```python
def scheduled_task():
    """No arguments for scheduled tasks"""
    pass
```

## Hook Execution Order

### Document Lifecycle

1. **Insert**:
   - `validate()` controller method
   - `before_insert` hook
   - Database INSERT
   - `after_insert` hook
   - `on_update` hook

2. **Update**:
   - `validate()` controller method
   - `before_save` hook
   - Database UPDATE
   - `after_save` hook
   - `on_update` hook
   - `on_change` hook (if fields changed)

3. **Submit**:
   - `before_submit` hook
   - Set docstatus = 1
   - Database UPDATE
   - `after_submit` hook
   - `on_update` hook

4. **Cancel**:
   - `before_cancel` hook
   - Set docstatus = 2
   - Database UPDATE
   - `after_cancel` hook
   - `on_cancel` hook

5. **Delete**:
   - `before_trash` hook (controller method)
   - `on_trash` hook
   - Database DELETE

### Permission Evaluation

1. Administrator check (bypass all)
2. Role-based permissions
3. `has_permission` hook
4. `permission_query_conditions` hook (for read/select)
5. User permissions
6. Share permissions

**When to read:** See [references/execution-order.md](references/execution-order.md) for complete hook execution sequences.

## Best Practices

### Hook Implementation

1. **Keep Hooks Focused**: Each hook should do one thing well
2. **Avoid Side Effects**: Be careful with database commits in hooks
3. **Handle Errors**: Use try-except to prevent hook failures from breaking operations
4. **Performance**: Hooks run synchronously; optimize for speed
5. **Idempotency**: Design hooks to be safely re-runnable

### Common Patterns

**Conditional execution:**
```python
def on_update(doc, method=None):
    # Only process specific doctypes
    if doc.doctype != "Target DocType":
        return
    
    # Only process when field changes
    if not doc.has_value_changed("status"):
        return
    
    # Your logic here
```

**Error handling:**
```python
def after_insert(doc, method=None):
    try:
        # Your logic
        external_api_call(doc)
    except Exception as e:
        frappe.log_error(f"Hook failed: {str(e)}")
        # Decide: raise or continue?
```

**Wildcard hooks:**
```python
doc_events = {
    "*": {  # Applies to all doctypes
        "on_update": "app.utils.log_all_updates",
    }
}
```

### Security Considerations

1. **Validate Input**: Don't trust data in hooks
2. **Check Permissions**: Hooks may run with elevated privileges
3. **Sanitize SQL**: Use parameterized queries in permission hooks
4. **Avoid Recursion**: Be careful with hooks that modify documents
5. **Rate Limiting**: Consider impact on high-volume operations

**When to read:** See [references/best-practices.md](references/best-practices.md) for comprehensive guidelines.

## Debugging Hooks

### Enable Debug Logging

```python
# In hook function
import frappe
frappe.logger().debug(f"Hook called: {doc.doctype} - {method}")
```

### Test Hooks

```python
# In test file
def test_my_hook():
    doc = frappe.get_doc({
        "doctype": "Test DocType",
        "field": "value"
    })
    doc.insert()  # Triggers hooks
    
    # Verify hook effects
    assert some_condition
```

### Common Issues

1. **Hook Not Firing**: Check hooks.py syntax, restart bench
2. **Hook Order**: Multiple hooks execute in registration order
3. **Infinite Loops**: Hook modifies doc, triggering itself
4. **Performance**: Slow hooks delay all operations

**When to read:** See [references/debugging-hooks.md](references/debugging-hooks.md) for troubleshooting guide.

## Reference Files

For detailed information on specific hook categories:

- **[application-hooks.md](references/application-hooks.md)** - App metadata and configuration
- **[installation-hooks.md](references/installation-hooks.md)** - Install, uninstall, and migration hooks
- **[document-hooks.md](references/document-hooks.md)** - Complete doc_events reference with examples
- **[permission-hooks.md](references/permission-hooks.md)** - Permission extension hooks
- **[scheduler-hooks.md](references/scheduler-hooks.md)** - Scheduled task configuration
- **[ui-hooks.md](references/ui-hooks.md)** - Frontend customization hooks
- **[jinja-hooks.md](references/jinja-hooks.md)** - Template rendering hooks
- **[request-job-hooks.md](references/request-job-hooks.md)** - Request and job lifecycle hooks
- **[other-hooks.md](references/other-hooks.md)** - Additional hooks and extension points
- **[execution-order.md](references/execution-order.md)** - Hook execution sequences
- **[best-practices.md](references/best-practices.md)** - Patterns and guidelines
- **[debugging-hooks.md](references/debugging-hooks.md)** - Troubleshooting and testing

## Core Implementation Files

Key files in Frappe codebase:
- `/frappe/__init__.py` - Hook loading and execution (`get_hooks`, `get_doc_hooks`, `call_hook`)
- `/frappe/model/document.py` - Document lifecycle and hook calls
- `/frappe/utils/boilerplate.py` - Hooks template for new apps
- Individual hook implementations throughout the codebase

## Usage

When working with hooks:

1. **Identify the requirement**: What behavior needs customization?
2. **Choose appropriate hook**: Select based on event type and timing
3. **Register in hooks.py**: Follow correct syntax for hook type
4. **Implement function**: Create function with proper signature
5. **Test thoroughly**: Verify hook fires and produces expected results
6. **Monitor performance**: Ensure hooks don't slow down operations

## Important Notes

- Hooks run synchronously in the main thread (except scheduler hooks)
- Multiple apps can register hooks for the same event (all execute in order)
- Hook execution order: by app installation order in `apps.txt`
- Changes to `hooks.py` require bench restart (`bench restart`)
- Wildcard `*` in `doc_events` applies to all doctypes
- Controller methods (like `validate()`) run before hooks
- Hooks should be idempotent and handle errors gracefully
