# Input Validation Reference

## Overview

Input validation is the first line of defense against attacks. All user input must be validated before processing.

---

## Validation Strategy

### The Three Steps

```
1. VALIDATE → Check input meets requirements
2. SANITIZE → Remove/escape dangerous characters
3. ENCODE   → Encode for output context (HTML, URL, SQL)
```

### Validation Types

| Type | Purpose | Example |
|------|---------|---------|
| **Allowlist** | Only permit known-good values | File extensions: `.jpg`, `.png`, `.pdf` |
| **Blocklist** | Block known-bad values | Block `<script>`, `DROP TABLE` |
| **Format** | Check structure/pattern | Email, phone, date formats |
| **Range** | Check numeric bounds | Age: 0-150, Price: 0-999999 |
| **Length** | Check string length | Username: 3-30 characters |
| **Type** | Check data type | Expect integer, got string |

**Rule:** Prefer allowlists over blocklists. It's safer to define what's allowed than try to block everything dangerous.

---

## Common Input Types

### Email Validation

```python
import re

def validate_email(email: str) -> bool:
    """
    Validate email format.
    - Max 254 characters (RFC 5321)
    - Has @ symbol with local and domain parts
    - Domain has at least one dot
    """
    if not email or len(email) > 254:
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# Usage
assert validate_email("user@example.com") == True
assert validate_email("invalid") == False
assert validate_email("a" * 255 + "@x.com") == False
```

### Username Validation

```python
import re

def validate_username(username: str) -> tuple[bool, str]:
    """
    Validate username.
    - 3-30 characters
    - Alphanumeric plus underscore
    - Must start with letter
    """
    if not username:
        return False, "Username required"

    if len(username) < 3:
        return False, "Username must be at least 3 characters"

    if len(username) > 30:
        return False, "Username must be at most 30 characters"

    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
        return False, "Username must start with letter, contain only letters, numbers, underscores"

    return True, ""
```

### Password Validation

```python
def validate_password(password: str) -> tuple[bool, list[str]]:
    """
    Validate password strength.
    Returns (is_valid, list_of_issues)
    """
    issues = []

    if len(password) < 12:
        issues.append("Password must be at least 12 characters")

    if len(password) > 128:
        issues.append("Password must be at most 128 characters")

    # Check against common passwords
    if password.lower() in COMMON_PASSWORDS:
        issues.append("Password is too common")

    # Optional complexity requirements
    # (NIST recommends length over complexity)

    return len(issues) == 0, issues

# Common passwords list (top entries)
COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123",
    "password1", "password123", "admin", "letmein", "welcome",
    # ... load from file for complete list
}
```

### Phone Number Validation

```python
import re

def validate_phone(phone: str, country: str = "US") -> bool:
    """Validate phone number format."""
    # Remove common formatting characters
    digits = re.sub(r'[\s\-\(\)\.]', '', phone)

    patterns = {
        "US": r'^(\+1)?[2-9]\d{9}$',      # +1 + 10 digits
        "UK": r'^(\+44)?[0-9]{10,11}$',   # +44 + 10-11 digits
        "INTL": r'^\+[1-9]\d{6,14}$',     # E.164 format
    }

    pattern = patterns.get(country, patterns["INTL"])
    return bool(re.match(pattern, digits))
```

### URL Validation

```python
from urllib.parse import urlparse

def validate_url(url: str, allowed_schemes: set = None, allowed_domains: set = None) -> tuple[bool, str]:
    """
    Validate URL with optional restrictions.
    """
    if allowed_schemes is None:
        allowed_schemes = {'http', 'https'}

    try:
        parsed = urlparse(url)
    except Exception:
        return False, "Invalid URL format"

    # Check scheme
    if parsed.scheme not in allowed_schemes:
        return False, f"Scheme must be one of: {allowed_schemes}"

    # Check domain if allowlist provided
    if allowed_domains and parsed.netloc not in allowed_domains:
        return False, f"Domain not allowed"

    # Block internal addresses (SSRF prevention)
    if is_internal_address(parsed.netloc):
        return False, "Internal addresses not allowed"

    return True, ""

def is_internal_address(host: str) -> bool:
    """Check if host resolves to internal IP."""
    import socket
    try:
        ip = socket.gethostbyname(host)
        return (
            ip.startswith('10.') or
            ip.startswith('192.168.') or
            ip.startswith('172.16.') or
            ip.startswith('172.17.') or
            ip.startswith('127.') or
            ip == 'localhost'
        )
    except socket.gaierror:
        return False
```

### Date Validation

```python
from datetime import datetime, date

def validate_date(date_str: str, format: str = "%Y-%m-%d") -> tuple[bool, date | None]:
    """
    Validate date string and return date object.
    """
    try:
        parsed = datetime.strptime(date_str, format).date()
        return True, parsed
    except ValueError:
        return False, None

def validate_date_range(date_obj: date, min_date: date = None, max_date: date = None) -> tuple[bool, str]:
    """
    Validate date is within acceptable range.
    """
    if min_date and date_obj < min_date:
        return False, f"Date must be after {min_date}"

    if max_date and date_obj > max_date:
        return False, f"Date must be before {max_date}"

    return True, ""
```

---

## Numeric Validation

### Integer Validation

```python
def validate_int(value: str, min_val: int = None, max_val: int = None) -> tuple[bool, int | None, str]:
    """
    Validate and parse integer with optional range.
    Returns (is_valid, parsed_value, error_message)
    """
    try:
        parsed = int(value)
    except (ValueError, TypeError):
        return False, None, "Must be a whole number"

    if min_val is not None and parsed < min_val:
        return False, None, f"Must be at least {min_val}"

    if max_val is not None and parsed > max_val:
        return False, None, f"Must be at most {max_val}"

    return True, parsed, ""

# Usage
valid, age, error = validate_int(request.form['age'], min_val=0, max_val=150)
if not valid:
    return {"error": error}, 400
```

### Decimal/Currency Validation

```python
from decimal import Decimal, InvalidOperation

def validate_currency(value: str, max_amount: Decimal = Decimal("999999.99")) -> tuple[bool, Decimal | None, str]:
    """
    Validate currency amount.
    """
    try:
        amount = Decimal(value)
    except InvalidOperation:
        return False, None, "Invalid amount format"

    if amount < 0:
        return False, None, "Amount cannot be negative"

    if amount > max_amount:
        return False, None, f"Amount cannot exceed {max_amount}"

    # Check decimal places (max 2 for currency)
    if amount.as_tuple().exponent < -2:
        return False, None, "Maximum 2 decimal places"

    return True, amount, ""
```

---

## File Upload Validation

### Complete File Validator

```python
from pathlib import Path
import magic  # python-magic library

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

MIME_TYPES = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.pdf': 'application/pdf',
    '.doc': 'application/msword',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
}

def validate_file_upload(file) -> tuple[bool, str]:
    """
    Comprehensive file upload validation.
    """
    # 1. Check if file exists
    if not file or not file.filename:
        return False, "No file provided"

    # 2. Check file size
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)     # Reset position

    if size > MAX_FILE_SIZE:
        return False, f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)} MB"

    if size == 0:
        return False, "File is empty"

    # 3. Check extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"File type not allowed. Allowed: {ALLOWED_EXTENSIONS}"

    # 4. Verify content type matches extension (magic bytes)
    mime = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)

    expected_mime = MIME_TYPES.get(ext)
    if mime != expected_mime:
        return False, f"File content doesn't match extension"

    # 5. Check filename for path traversal
    if '..' in file.filename or '/' in file.filename or '\\' in file.filename:
        return False, "Invalid filename"

    return True, ""

def generate_safe_filename(original: str) -> str:
    """Generate safe random filename preserving extension."""
    import uuid
    ext = Path(original).suffix.lower()
    return f"{uuid.uuid4()}{ext}"
```

---

## SQL Injection Prevention

### Always Use Parameterized Queries

```python
# ❌ NEVER - String concatenation
def get_user_bad(email):
    query = f"SELECT * FROM users WHERE email = '{email}'"
    cursor.execute(query)
    return cursor.fetchone()

# ✅ ALWAYS - Parameterized query (SQLite/psycopg2 style)
def get_user_good(email):
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    return cursor.fetchone()

# ✅ ALWAYS - Named parameters
def get_user_named(email):
    cursor.execute(
        "SELECT * FROM users WHERE email = :email",
        {"email": email}
    )
    return cursor.fetchone()

# ✅ ALWAYS - ORM (SQLAlchemy)
def get_user_orm(email):
    return User.query.filter_by(email=email).first()

# ✅ ALWAYS - ORM (Django)
def get_user_django(email):
    return User.objects.get(email=email)
```

### Dynamic Column/Table Names

When you must use dynamic names (can't be parameterized):

```python
# ❌ NEVER - Direct injection
def sort_by(column):
    query = f"SELECT * FROM users ORDER BY {column}"

# ✅ ALWAYS - Allowlist approach
ALLOWED_SORT_COLUMNS = {'name', 'email', 'created_at'}

def sort_by(column):
    if column not in ALLOWED_SORT_COLUMNS:
        raise ValueError(f"Invalid sort column: {column}")
    query = f"SELECT * FROM users ORDER BY {column}"  # Safe - validated
```

---

## XSS Prevention

### Output Encoding

```python
import html

def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return html.escape(text)

# Usage in templates
# Most template engines auto-escape. Verify yours does!

# Jinja2 (Flask) - auto-escapes by default
# {{ user_input }}  ← Safe, auto-escaped

# ❌ DANGER - Marking as safe disables escaping
# {{ user_input | safe }}  ← Only use for trusted HTML!
```

### Content Security Policy

```python
# Add CSP header to prevent inline scripts
CSP_POLICY = (
    "default-src 'self'; "
    "script-src 'self'; "       # Only scripts from same origin
    "style-src 'self' 'unsafe-inline'; "  # Allow inline styles
    "img-src 'self' data: https:; "
    "font-src 'self'; "
    "connect-src 'self' https://api.example.com; "
    "frame-ancestors 'none'; "  # Prevent framing (clickjacking)
)

@app.after_request
def add_csp_header(response):
    response.headers['Content-Security-Policy'] = CSP_POLICY
    return response
```

---

## JSON Validation

### Schema Validation

```python
from jsonschema import validate, ValidationError

USER_SCHEMA = {
    "type": "object",
    "required": ["email", "name"],
    "properties": {
        "email": {"type": "string", "format": "email", "maxLength": 254},
        "name": {"type": "string", "minLength": 1, "maxLength": 100},
        "age": {"type": "integer", "minimum": 0, "maximum": 150},
    },
    "additionalProperties": False  # Reject unknown fields
}

def validate_user_input(data: dict) -> tuple[bool, str]:
    """Validate user input against schema."""
    try:
        validate(instance=data, schema=USER_SCHEMA)
        return True, ""
    except ValidationError as e:
        return False, e.message
```

### Pydantic Validation

```python
from pydantic import BaseModel, EmailStr, Field, validator

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(None, ge=0, le=150)

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be blank')
        return v.strip()

# Usage
try:
    user = UserCreate(**request.json)
except ValidationError as e:
    return {"errors": e.errors()}, 400
```

---

## Validation Checklist

Before processing any input:

- [ ] Is the input required? Handle missing values
- [ ] Is there a maximum length? Prevent DoS
- [ ] Is there a valid format? Regex/schema validation
- [ ] Is there a valid range? Min/max values
- [ ] Is it in an allowlist? For fixed options
- [ ] Is it properly typed? String vs int vs bool
- [ ] Is it properly encoded? For output context
- [ ] Is it sanitized? Remove dangerous characters if needed
