# API Reviewer Skill - Quick Reference

## What is this?

The API Reviewer skill helps identify and fix security vulnerabilities in Frappe API endpoints that use the `@frappe.whitelist()` decorator.

## Quick Start

### 1. Scan for API Endpoints

```bash
cd .github/skills/api-reviewer/scripts
python3 scan_api_endpoints.py --path /path/to/your/app
```

This creates/updates `docs/api-review.yaml` (at the app root) with all discovered endpoints.

### 2. Review the YAML File

Open `docs/api-review.yaml` and look for endpoints with security issues:

- `has_frappe_only_for: false` - No role restriction
- `has_frappe_has_permission: false` - No permission check
- `has_frappe_get_list: false` - Might be using `frappe.get_all()`

### 3. Fix Security Issues

Common fixes:

**Add role restriction:**
```python
@frappe.whitelist()
def admin_function():
    frappe.only_for("System Manager")
    # ...
```

**Add permission check:**
```python
@frappe.whitelist()
def update_record(doctype, name, data):
    if not frappe.has_permission(doctype, "write", name):
        frappe.throw("No permission")
    # ...
```

**Use frappe.get_list instead of frappe.get_all:**
```python
@frappe.whitelist()
def get_records(doctype):
    return frappe.get_list(doctype, fields=["name", "title"])
```

### 4. Mark as Reviewed

Update the endpoint in `docs/api-review.yaml`:

```yaml
- function: my_function
  reviewed: true
  notes: "Fixed: Added frappe.only_for check"
```

## Security Checklist

For each API endpoint, verify:

- [ ] Uses `frappe.only_for()` if admin/role-specific
- [ ] Uses `frappe.has_permission()` for document operations
- [ ] Uses `frappe.get_list()` instead of `frappe.get_all()`
- [ ] SQL queries are parameterized (no string concatenation)
- [ ] User inputs are validated
- [ ] Sensitive data is not exposed

## Files

- `SKILL.md` - Complete skill documentation
- `scripts/scan_api_endpoints.py` - Scanner script
- `scripts/test_scanner.py` - Test suite for the scanner
- `../../docs/api-review.yaml` - Generated endpoint database (at app root)
- `references/security-best-practices.md` - Detailed security guide

## Running Tests

```bash
cd .github/skills/api-reviewer/scripts
python3 test_scanner.py
```

## Documentation

See [SKILL.md](SKILL.md) for complete documentation and [references/security-best-practices.md](references/security-best-practices.md) for detailed security guidelines.
