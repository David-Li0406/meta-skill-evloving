---
name: security-review
description: Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features. Provides a comprehensive security checklist and patterns.
---

# Security Review Skill

This skill ensures all code follows security best practices and identifies potential vulnerabilities.

## When to Activate

- Implementing authentication or authorization
- Handling user input or file uploads
- Creating new API endpoints
- Working with secrets or credentials
- Implementing payment features
- Storing or transmitting sensitive data
- Integrating third-party APIs

## Security Checklist

### 1. Secrets Management

#### ❌ NEVER Do This
```python
api_key = "sk-proj-xxxxx"  # Hardcoded secret
db_password = "password123"  # In source code
```

#### ✅ ALWAYS Do This
```python
import os

api_key = os.getenv('OPENAI_API_KEY')
db_url = os.getenv('DATABASE_URL')

# Verify secrets exist
if not api_key:
    raise ValueError('OPENAI_API_KEY not configured')
```

#### Verification Steps
- [ ] No hardcoded API keys, tokens, or passwords
- [ ] All secrets in environment variables
- [ ] `.env.local` in .gitignore
- [ ] No secrets in git history
- [ ] Production secrets in hosting platform (Vercel, Railway)

### 2. Input Validation

#### Always Validate User Input
```python
from pydantic import BaseModel, EmailStr, Field, ValidationError

class CreateUserSchema(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)

async def create_user(input_data: dict):
    try:
        validated = CreateUserSchema(**input_data)
        return await db.users.create(validated.model_dump())
    except ValidationError as e:
        return {'success': False, 'errors': e.errors()}
```

#### File Upload Validation
```python
from fastapi import UploadFile
import re

def validate_file_upload(file: UploadFile) -> bool:
    max_size = 5 * 1024 * 1024  # 5MB max
    if file.size > max_size:
        raise ValueError('File too large (max 5MB)')

    allowed_types = ['image/jpeg', 'image/png', 'image/gif']
    if file.content_type not in allowed_types:
        raise ValueError('Invalid file type')

    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    extension_match = re.search(r'\.[^.]+$', file.filename.lower())
    extension = extension_match.group(0) if extension_match else None

    if not extension or extension not in allowed_extensions:
        raise ValueError('Invalid file extension')

    return True
```

#### Verification Steps
- [ ] All user inputs validated with schemas
- [ ] File uploads restricted (size, type, extension)
- [ ] No direct use of user input in queries
- [ ] Whitelist validation (not blacklist)
- [ ] Error messages don't leak sensitive info

### 3. SQL Injection Prevention

#### ❌ NEVER Concatenate SQL
```python
query = f"SELECT * FROM users WHERE email = '{user_email}'"
db.execute(query)
```

#### ✅ ALWAYS Use Parameterized Queries
```python
from sqlalchemy import text

result = session.execute(
    text('SELECT * FROM users WHERE email = :email'),
    {'email': user_email}
)
```

#### Verification Steps
- [ ] All database queries use parameterized queries
- [ ] No string concatenation in SQL
- [ ] ORM/query builder used correctly

### 4. Authentication & Authorization

#### JWT Token Handling
```python
from fastapi import Response

response = Response()
response.set_cookie(
    key='token',
    value=token,
    httponly=True,
    secure=True,
    samesite='strict',
    max_age=3600
)
```

#### Authorization Checks
```python
from fastapi import HTTPException

async def delete_user(user_id: str, requester_id: str):
    requester = await db.users.get(id=requester_id)

    if requester.role != 'admin':
        raise HTTPException(
            status_code=403,
            detail='Unauthorized'
        )

    await db.users.delete(id=user_id)
```

#### Verification Steps
- [ ] Tokens stored in httpOnly cookies (not localStorage)
- [ ] Authorization checks before sensitive operations
- [ ] Role-based access control implemented

### 5. XSS Prevention

#### Sanitize HTML
```python
from bleach import clean

def render_user_content(html: str) -> str:
    allowed_tags = ['b', 'i', 'em', 'strong', 'p']
    cleaned = clean(
        html,
        tags=allowed_tags,
        attributes={},
        strip=True
    )
    return cleaned
```

#### Verification Steps
- [ ] User-provided HTML sanitized
- [ ] CSP headers configured
- [ ] No unvalidated dynamic content rendering

### 6. CSRF Protection

#### CSRF Tokens
```python
from fastapi import HTTPException, Header
import secrets

csrf_tokens = {}

def generate_csrf_token() -> str:
    token = secrets.token_urlsafe(32)
    csrf_tokens[token] = True
    return token

def verify_csrf_token(token: str) -> bool:
    return token in csrf_tokens

@app.post('/api/endpoint')
async def protected_endpoint(
    x_csrf_token: str = Header(..., alias='X-CSRF-Token')
):
    if not verify_csrf_token(x_csrf_token):
        raise HTTPException(
            status_code=403,
            detail='Invalid CSRF token'
        )
```

#### Verification Steps
- [ ] CSRF tokens on state-changing operations
- [ ] SameSite=Strict on all cookies

### 7. Rate Limiting

#### API Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get('/api/endpoint')
@limiter.limit('100/15minutes')
async def api_endpoint():
    pass
```

#### Verification Steps
- [ ] Rate limiting on all API endpoints

### 8. Sensitive Data Exposure

#### Logging
```python
import logging

logger = logging.getLogger(__name__)

logger.info(f'User login: email={email}, user_id={user_id}')
```

#### Verification Steps
- [ ] No passwords, tokens, or secrets in logs

### 9. Blockchain Security (Solana)

#### Wallet Verification
```python
async def verify_wallet_ownership(public_key: str, signature: str, message: str) -> bool:
    # Implement wallet verification logic
    return True
```

#### Verification Steps
- [ ] Wallet signatures verified

### 10. Dependency Security

#### Regular Updates
```bash
# Check for vulnerabilities
pip-audit

# Update dependencies
pip install --upgrade package
```

#### Verification Steps
- [ ] Dependencies up to date

## Security Testing

### Automated Security Tests
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_requires_authentication(client: AsyncClient):
    response = await client.get('/api/protected')
    assert response.status_code == 401
```

## Pre-Deployment Security Checklist

Before ANY production deployment:

- [ ] **Secrets**: No hardcoded secrets, all in env vars
- [ ] **Input Validation**: All user inputs validated
- [ ] **SQL Injection**: All queries parameterized
- [ ] **XSS**: User content sanitized
- [ ] **CSRF**: Protection enabled
- [ ] **Authentication**: Proper token handling
- [ ] **Authorization**: Role checks in place
- [ ] **Rate Limiting**: Enabled on all endpoints
- [ ] **HTTPS**: Enforced in production
- [ ] **Security Headers**: CSP configured
- [ ] **Error Handling**: No sensitive data in errors
- [ ] **Logging**: No sensitive data logged
- [ ] **Dependencies**: Up to date, no vulnerabilities

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Web Security Academy](https://portswigger.net/web-security)

---

**Remember**: Security is not optional. One vulnerability can compromise the entire platform. When in doubt, err on the side of caution.