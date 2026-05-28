---
name: api-reviewer
description: Security review and analysis for Frappe API endpoints decorated with @frappe.whitelist(). Use when reviewing API security, checking for permission vulnerabilities, scanning for unprotected endpoints, validating role restrictions, or auditing API endpoints for security best practices. Helps identify missing frappe.only_for(), frappe.has_permission(), or frappe.get_list() usage.
---

# API Reviewer

Expert guidance for reviewing and securing Frappe API endpoints to prevent security vulnerabilities.

## Overview

Frappe makes it easy to expose API endpoints using the `@frappe.whitelist()` decorator. However, this convenience can lead to security holes if proper permission checks aren't implemented. This skill helps identify and fix common API security issues.

## Common Security Issues

The most common API security problems in Frappe applications:

1. **Missing role validation**: Endpoints accessible to any authenticated user
2. **Using frappe.get_all instead of frappe.get_list**: Bypassing permission checks
3. **No document permission checks**: Modifying records without validation
4. **SQL injection**: Unsafe query construction with user input
5. **Unrestricted data access**: Exposing sensitive information

See [references/security-best-practices.md](references/security-best-practices.md) for detailed explanations and examples of each issue.

## Security Review Workflow

### 1. Scan for API Endpoints

Use the included script to discover all `@frappe.whitelist()` decorated functions:

```bash
cd .github/skills/api-reviewer/scripts
python3 scan_api_endpoints.py --path /path/to/app
```

The script creates/updates `docs/api-review.yaml` (at the app root) with:
- Function name and location
- Function arguments
- Detected security checks
- Review status and notes

### 2. Review Security Checks

For each endpoint in the YAML file, verify:

**Role Restrictions**:
- Does the endpoint use `frappe.only_for("Role")`?
- Is the role appropriate for the operation?

**Permission Checks**:
- Does it use `frappe.has_permission()` before accessing documents?
- Are permission checks comprehensive?

**Safe Queries**:
- Does it use `frappe.get_list()` instead of `frappe.get_all()`?
- Are SQL queries parameterized (not concatenated)?

**Input Validation**:
- Is user input validated and sanitized?
- Are there checks for malicious input?

### 3. Document Findings

Update the YAML file with review results:

```yaml
endpoints:
- function: update_document
  file: custom/utils/documents.py
  line: 45
  reviewed: true
  notes: "ISSUE: No permission check before modifying document. Needs frappe.has_permission() call."
```

### 4. Fix Security Issues

Apply appropriate security measures based on the findings. Common fixes:

**Add role restriction**:
```python
@frappe.whitelist()
def admin_function():
    frappe.only_for("System Manager")
    # Implementation
```

**Add permission check**:
```python
@frappe.whitelist()
def update_record(doctype, name, data):
    if not frappe.has_permission(doctype, "write", name):
        frappe.throw("No permission")
    # Implementation
```

**Switch to frappe.get_list**:
```python
@frappe.whitelist()
def get_records(doctype):
    return frappe.get_list(doctype, fields=["name", "title"])  # Respects permissions
```

## Quick Security Checklist

When reviewing any API endpoint:

- [ ] Uses `frappe.only_for()` if admin/role-specific
- [ ] Uses `frappe.has_permission()` for document operations
- [ ] Uses `frappe.get_list()` instead of `frappe.get_all()`
- [ ] Parameterizes SQL queries (no string concatenation)
- [ ] Validates and sanitizes user inputs
- [ ] Doesn't expose sensitive data
- [ ] Implements pagination for expensive queries

## Automated Detection

The scan script automatically detects these security patterns:

- `has_frappe_only_for`: Presence of `frappe.only_for()`
- `has_frappe_get_list`: Usage of `frappe.get_list()`
- `has_frappe_has_permission`: Usage of `frappe.has_permission()`
- `has_permission_check`: Generic permission checking patterns

Review endpoints with `false` values for these checks more carefully.

## Resources

### scripts/scan_api_endpoints.py

Python script that scans Python files for `@frappe.whitelist()` decorators and extracts endpoint information into a YAML file.

**Features**:
- AST-based parsing for accurate detection
- Detects security patterns automatically
- Preserves review notes when re-scanning
- Generates summary statistics

### docs/api-review.yaml

YAML database of discovered API endpoints with security analysis. Located at the app root in the `docs/` directory. Updated by the scan script and manually annotated during review.

**Structure**:
- `scan_info`: Statistics (total, reviewed, unreviewed)
- `endpoints`: List of all discovered endpoints with metadata

### references/security-best-practices.md

Comprehensive guide to API security in Frappe, including:
- Detailed explanations of common security issues
- Bad vs. good code examples
- Security checklist
- Common security functions reference
- Review workflow guidance

## Usage Examples

**Example 1: Initial security audit**
```bash
# Scan the app
cd .github/skills/api-reviewer/scripts
python3 scan_api_endpoints.py --path tweaks

# Review generated YAML file
# Look for endpoints with all security_checks: false

# Fix identified issues and mark as reviewed
```

**Example 2: Regular security monitoring**
```bash
# Re-scan after adding new features
python3 scan_api_endpoints.py --path tweaks

# Check scan_info.unreviewed count
# Review only new/unreviewed endpoints
```

**Example 3: Reviewing specific endpoint**
```bash
# Find endpoint in docs/api-review.yaml
# Check security_checks flags
# Read the actual code at the file:line location
# Apply fixes based on security-best-practices.md
# Mark reviewed: true and add notes
```
