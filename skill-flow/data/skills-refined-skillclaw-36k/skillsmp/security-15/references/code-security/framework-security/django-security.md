# Django Security Patterns

**Category**: code-security/framework-security/django
**Description**: Security vulnerabilities and secure coding patterns for Django applications
**CWE**: CWE-89, CWE-79, CWE-352, CWE-798, CWE-639, CWE-915, CWE-434

---

## Overview

Django has strong security defaults but misconfigurations and bypasses can introduce vulnerabilities.

---

## SQL Injection Patterns

### Raw SQL with f-string
**Pattern**: `\.raw\s*\(\s*f['"']`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Django raw SQL with f-string interpolation
- CWE-89: SQL Injection

### Raw SQL with format
**Pattern**: `\.raw\s*\([^)]*\.format\s*\(`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Django raw SQL with .format() interpolation
- CWE-89: SQL Injection

### Cursor Execute with f-string
**Pattern**: `cursor\.execute\s*\(\s*f['"']`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Direct cursor.execute with f-string
- CWE-89: SQL Injection

### Extra Where Clause
**Pattern**: `\.extra\s*\(\s*where\s*=\s*\[.*f['"']`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Django extra() with unparameterized where clause
- CWE-89: SQL Injection

---

## XSS Patterns

### Mark Safe on User Input
**Pattern**: `mark_safe\s*\(\s*(?:request\.|form\.|data\[)`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Marking user input as safe without sanitization
- CWE-79: Cross-site Scripting

### Safe Filter on User Content
**Pattern**: `\{\{\s*\w+\s*\|\s*safe\s*\}\}`
**Type**: regex
**Severity**: high
**Context**: django-templates
- Using |safe filter on potentially user-controlled content
- CWE-79: Cross-site Scripting

---

## CSRF Patterns

### CSRF Exempt Decorator
**Pattern**: `@csrf_exempt`
**Type**: regex
**Severity**: high
**Languages**: [python]
- CSRF protection disabled on view
- CWE-352: Cross-Site Request Forgery

### CSRF Trusted Origins Wildcard
**Pattern**: `CSRF_TRUSTED_ORIGINS\s*=\s*\[.*\*`
**Type**: regex
**Severity**: high
**Languages**: [python]
- Wildcard in CSRF trusted origins
- CWE-352: Cross-Site Request Forgery

---

## Authentication Patterns

### Hardcoded SECRET_KEY
**Pattern**: `SECRET_KEY\s*=\s*['"'][^'"]{20,}['"']`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Django SECRET_KEY hardcoded in settings
- CWE-798: Hardcoded Credentials

### Debug Mode Enabled
**Pattern**: `DEBUG\s*=\s*True`
**Type**: regex
**Severity**: high
**Languages**: [python]
- Debug mode should be disabled in production
- CWE-489: Active Debug Code

### Empty Password Validators
**Pattern**: `AUTH_PASSWORD_VALIDATORS\s*=\s*\[\s*\]`
**Type**: regex
**Severity**: high
**Languages**: [python]
- No password validation configured
- CWE-521: Weak Password Requirements

---

## IDOR/Authorization Patterns

### Get Without Owner Check
**Pattern**: `\.objects\.get\s*\(\s*(?:id|pk)\s*=`
**Type**: regex
**Severity**: medium
**Languages**: [python]
- Object retrieval without ownership verification
- CWE-639: Authorization Bypass

### Mass Assignment
**Pattern**: `setattr\s*\(\s*\w+\s*,\s*\w+\s*,\s*request\.`
**Type**: regex
**Severity**: high
**Languages**: [python]
- Setting object attributes directly from request
- CWE-915: Mass Assignment

---

## File Upload Patterns

### Open Without Path Validation
**Pattern**: `open\s*\(\s*(?:f['"']|request\.)`
**Type**: regex
**Severity**: high
**Languages**: [python]
- File operations without path validation
- CWE-22: Path Traversal

### File Save Without Validation
**Pattern**: `request\.FILES\[.*\]\.save\s*\(`
**Type**: regex
**Severity**: high
**Languages**: [python]
- File saved without type/size validation
- CWE-434: Unrestricted Upload

---

## Security Settings Patterns

### Missing HTTPS Settings
**Pattern**: `SECURE_SSL_REDIRECT\s*=\s*False`
**Type**: regex
**Severity**: medium
**Languages**: [python]
- HTTPS redirect disabled
- CWE-319: Cleartext Transmission

### Insecure Cookie Settings
**Pattern**: `SESSION_COOKIE_SECURE\s*=\s*False`
**Type**: regex
**Severity**: medium
**Languages**: [python]
- Session cookie not secure
- CWE-614: Sensitive Cookie in HTTPS Without Secure

### Missing HSTS
**Pattern**: `SECURE_HSTS_SECONDS\s*=\s*0`
**Type**: regex
**Severity**: medium
**Languages**: [python]
- HSTS disabled
- CWE-319: Cleartext Transmission

---

## Code Examples

### SQL Injection - Vulnerable vs Secure

```python
# VULNERABLE - String formatting in raw SQL
def get_user(request):
    user_id = request.GET.get('id')
    user = User.objects.raw(f"SELECT * FROM auth_user WHERE id = {user_id}")
    return user

# SECURE - Parameterized queries
def get_user(request):
    user_id = request.GET.get('id')
    user = User.objects.raw("SELECT * FROM auth_user WHERE id = %s", [user_id])
    return user

# BEST - Use ORM
def get_user(request):
    user_id = request.GET.get('id')
    user = User.objects.get(id=user_id)
    return user
```

### XSS - Vulnerable vs Secure

```python
# VULNERABLE - Marking content as safe without sanitization
from django.utils.safestring import mark_safe

def show_content(request):
    content = request.POST.get('content')
    return render(request, 'page.html', {'content': mark_safe(content)})

# SECURE - Let Django escape automatically
def show_content(request):
    content = request.POST.get('content')
    return render(request, 'page.html', {'content': content})
# Template: {{ content }}  # Auto-escaped

# If HTML needed, sanitize first
import bleach

def show_content(request):
    content = request.POST.get('content')
    clean_content = bleach.clean(content, tags=['p', 'b', 'i'])
    return render(request, 'page.html', {'content': mark_safe(clean_content)})
```

---

## Django Security Checklist

- [ ] SECRET_KEY from environment
- [ ] DEBUG = False in production
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enforced (SECURE_SSL_REDIRECT)
- [ ] Secure cookies enabled
- [ ] CSRF protection active
- [ ] Password validators configured
- [ ] User input properly escaped
- [ ] SQL queries parameterized
- [ ] File uploads validated
- [ ] Permissions checked on views
- [ ] Security middleware enabled

---

## References

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Django Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html)
