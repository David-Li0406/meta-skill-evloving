# Security Review Checklist

## OWASP Top 10 Checks

### 1. Injection (SQL, Command, etc.)

```
□ Parameterized queries used (no string concatenation)
□ ORM used correctly (no raw SQL with user input)
□ Command injection prevented (no shell=True with user input)
□ LDAP injection prevented
□ XML injection prevented
```

**Detection Patterns:**

```python
# BAD: SQL Injection
query = f"SELECT * FROM users WHERE id = {user_id}"  # Vulnerable!
cursor.execute(f"DELETE FROM users WHERE id = '{id}'")  # Vulnerable!

# GOOD: Parameterized
stmt = select(User).where(User.id == user_id)
cursor.execute("DELETE FROM users WHERE id = %s", (id,))

# BAD: Command Injection
os.system(f"convert {filename}")  # Vulnerable!
subprocess.run(f"echo {user_input}", shell=True)  # Vulnerable!

# GOOD: Safe command execution
subprocess.run(["convert", filename])  # List form, no shell
```

### 2. Broken Authentication

```
□ Passwords hashed with bcrypt/argon2 (not MD5/SHA1)
□ Password complexity enforced
□ Account lockout after failed attempts
□ Session tokens are random and long enough
□ Session invalidation on logout
□ Secure cookie flags set (HttpOnly, Secure, SameSite)
```

**Detection Patterns:**

```python
# BAD: Weak hashing
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()  # Weak!

# GOOD: Strong hashing
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# BAD: Predictable session
session_id = str(user_id)  # Predictable!

# GOOD: Random session
session_id = secrets.token_urlsafe(32)
```

### 3. Sensitive Data Exposure

```
□ Secrets not hardcoded in code
□ Secrets loaded from environment/vault
□ Sensitive data not logged
□ PII properly handled
□ HTTPS enforced
□ Sensitive fields excluded from API responses
```

**Detection Patterns:**

```python
# BAD: Hardcoded secrets
API_KEY = "sk-1234567890abcdef"  # Hardcoded!
DATABASE_URL = "postgresql://user:password@localhost/db"  # Hardcoded!

# GOOD: Environment variables
API_KEY = os.environ["API_KEY"]
DATABASE_URL = settings.database_url  # From secure config

# BAD: Logging sensitive data
logger.info(f"User login: {username}, password: {password}")  # Leaking!
logger.debug(f"Request: {request.json()}")  # May contain secrets!

# GOOD: Redact sensitive data
logger.info(f"User login: {username}")
logger.debug(f"Request: {redact_sensitive(request.json())}")
```

### 4. XML External Entities (XXE)

```
□ XML parsing disabled external entities
□ DTD processing disabled
□ Using defusedxml library
```

**Detection Patterns:**

```python
# BAD: Vulnerable XML parsing
import xml.etree.ElementTree as ET
tree = ET.parse(user_file)  # XXE vulnerable!

# GOOD: Safe XML parsing
import defusedxml.ElementTree as ET
tree = ET.parse(user_file)  # Safe
```

### 5. Broken Access Control

```
□ Authorization checks on every endpoint
□ Resource ownership verified
□ Role-based access control implemented
□ No direct object references without auth check
□ Admin functions protected
```

**Detection Patterns:**

```python
# BAD: No authorization check
@router.get("/users/{user_id}")
async def get_user(user_id: UUID):
    return await user_repo.get(user_id)  # Anyone can access any user!

# GOOD: Authorization check
@router.get("/users/{user_id}")
async def get_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(403, "Not authorized")
    return await user_repo.get(user_id)
```

### 6. Security Misconfiguration

```
□ Debug mode disabled in production
□ Default credentials changed
□ Error messages don't leak stack traces
□ CORS configured correctly
□ Security headers set (CSP, X-Frame-Options, etc.)
```

**Detection Patterns:**

```python
# BAD: Debug in production
app = FastAPI(debug=True)  # Should be False in prod!

# BAD: Verbose errors
@app.exception_handler(Exception)
async def handle_error(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "traceback": traceback.format_exc()}  # Leaking!
    )

# GOOD: Generic errors
@app.exception_handler(Exception)
async def handle_error(request, exc):
    logger.exception("Unhandled error")  # Log internally
    return JSONResponse(status_code=500, content={"error": "Internal server error"})
```

### 7. Cross-Site Scripting (XSS)

```
□ Output encoding applied
□ Content-Type headers set correctly
□ User input sanitized before rendering
□ CSP headers configured
```

### 8. Insecure Deserialization

```
□ No pickle.loads on untrusted data
□ No yaml.load (use yaml.safe_load)
□ JSON schema validation before processing
```

**Detection Patterns:**

```python
# BAD: Unsafe deserialization
import pickle
data = pickle.loads(user_data)  # Remote code execution!

import yaml
config = yaml.load(user_file)  # Unsafe!

# GOOD: Safe deserialization
import json
data = json.loads(user_data)  # Safe for untrusted data

import yaml
config = yaml.safe_load(user_file)  # Safe
```

### 9. Using Components with Known Vulnerabilities

```
□ Dependencies up to date
□ No known CVEs in dependencies
□ Security advisories monitored
```

**Check Command:**
```bash
# Check for vulnerabilities
pip-audit
safety check
```

### 10. Insufficient Logging & Monitoring

```
□ Authentication events logged
□ Authorization failures logged
□ Input validation failures logged
□ Logs don't contain sensitive data
□ Log injection prevented
```

---

## Python-Specific Security

### Input Validation

```python
# GOOD: Pydantic validation
class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    age: int = Field(ge=0, le=150)

# GOOD: Custom validation
@validator('password')
def password_complexity(cls, v):
    if not re.search(r'[A-Z]', v):
        raise ValueError('Must contain uppercase')
    if not re.search(r'[0-9]', v):
        raise ValueError('Must contain number')
    return v
```

### Path Traversal

```python
# BAD: Path traversal
file_path = f"/uploads/{user_filename}"  # ../../../etc/passwd possible!

# GOOD: Sanitize path
import os
safe_name = os.path.basename(user_filename)
file_path = os.path.join("/uploads", safe_name)

# Or use pathlib
from pathlib import Path
base = Path("/uploads")
file_path = base / user_filename
if not file_path.resolve().is_relative_to(base.resolve()):
    raise ValueError("Invalid path")
```

### Rate Limiting

```python
# GOOD: Rate limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, ...):
    ...
```

---

## Security Review Summary Template

```markdown
## Security Review: [Module/PR Name]

### Critical Findings :x:
- [ ] None found / [List issues]

### High Risk :warning:
- [ ] None found / [List issues]

### Medium Risk :bulb:
- [ ] None found / [List issues]

### Checklist Results
| Category | Status | Notes |
|----------|--------|-------|
| Injection Prevention | :white_check_mark: / :x: | |
| Authentication | :white_check_mark: / :x: | |
| Authorization | :white_check_mark: / :x: | |
| Data Protection | :white_check_mark: / :x: | |
| Input Validation | :white_check_mark: / :x: | |
| Error Handling | :white_check_mark: / :x: | |
| Logging | :white_check_mark: / :x: | |

### Recommendations
1. ...
```
