---
name: security-review
description: Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features. Provides comprehensive security checklist and patterns.
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

# Define validation schema
class CreateUserSchema(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)

# Validate before processing
async def create_user(input_data: dict):
    try:
        validated = CreateUserSchema(**input_data)
        return await db.users.create(validated.model_dump())
    except ValidationError as e:
        return {'success': False, 'errors': e.errors()}
    except Exception as e:
        raise
```

#### File Upload Validation
```python
from fastapi import UploadFile
import re

def validate_file_upload(file: UploadFile) -> bool:
    # Size check (5MB max)
    max_size = 5 * 1024 * 1024
    if file.size > max_size:
        raise ValueError('File too large (max 5MB)')

    # Type check
    allowed_types = ['image/jpeg', 'image/png', 'image/gif']
    if file.content_type not in allowed_types:
        raise ValueError('Invalid file type')

    # Extension check
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
# DANGEROUS - SQL Injection vulnerability
query = f"SELECT * FROM users WHERE email = '{user_email}'"
db.execute(query)
```

#### ✅ ALWAYS Use Parameterized Queries
```python
# Safe - parameterized query (SQLAlchemy)
from sqlalchemy import text

result = session.execute(
    text('SELECT * FROM users WHERE email = :email'),
    {'email': user_email}
)

# Safe - ORM query (Django)
users = User.objects.filter(email=user_email)

# Safe - parameterized query (psycopg2)
cursor.execute(
    'SELECT * FROM users WHERE email = %s',
    (user_email,)
)
```

#### Verification Steps
- [ ] All database queries use parameterized queries
- [ ] No string concatenation in SQL
- [ ] ORM/query builder used correctly
- [ ] Supabase queries properly sanitized

### 4. Authentication & Authorization

#### JWT Token Handling
```python
# ❌ WRONG: Client-side storage (vulnerable to XSS)
# Don't store tokens in localStorage or sessionStorage

# ✅ CORRECT: httpOnly cookies (FastAPI)
from fastapi import Response
from datetime import timedelta

response = Response()
response.set_cookie(
    key='token',
    value=token,
    httponly=True,
    secure=True,
    samesite='strict',
    max_age=3600
)

# ✅ CORRECT: httpOnly cookies (Django)
from django.http import HttpResponse

response = HttpResponse()
response.set_cookie(
    'token',
    token,
    httponly=True,
    secure=True,
    samesite='Strict',
    max_age=3600
)
```

#### Authorization Checks
```python
from fastapi import HTTPException

async def delete_user(user_id: str, requester_id: str):
    # ALWAYS verify authorization first
    requester = await db.users.get(id=requester_id)

    if requester.role != 'admin':
        raise HTTPException(
            status_code=403,
            detail='Unauthorized'
        )

    # Proceed with deletion
    await db.users.delete(id=user_id)
```

#### Row Level Security (Supabase)
```sql
-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Users can only view their own data
CREATE POLICY "Users view own data"
  ON users FOR SELECT
  USING (auth.uid() = id);

-- Users can only update their own data
CREATE POLICY "Users update own data"
  ON users FOR UPDATE
  USING (auth.uid() = id);
```

#### Verification Steps
- [ ] Tokens stored in httpOnly cookies (not localStorage)
- [ ] Authorization checks before sensitive operations
- [ ] Row Level Security enabled in Supabase
- [ ] Role-based access control implemented
- [ ] Session management secure

### 5. XSS Prevention

#### Sanitize HTML
```python
from bleach import clean

# ALWAYS sanitize user-provided HTML
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

#### Content Security Policy
```python
# FastAPI middleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-eval' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self' https://api.example.com;"
        )
        return response
```

#### Verification Steps
- [ ] User-provided HTML sanitized
- [ ] CSP headers configured
- [ ] No unvalidated dynamic content rendering
- [ ] React's built-in XSS protection used

### 6. CSRF Protection

#### CSRF Tokens
```python
from fastapi import HTTPException, Header
import secrets

# Generate and verify CSRF tokens
csrf_tokens = {}

def generate_csrf_token() -> str:
    token = secrets.token_urlsafe(32)
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

    # Process request
    pass
```

#### SameSite Cookies
```python
from fastapi import Response

response = Response()
response.set_cookie(
    'session',
    session_id,
    httponly=True,
    secure=True,
    samesite='strict'
)
```

#### Verification Steps
- [ ] CSRF tokens on state-changing operations
- [ ] SameSite=Strict on all cookies
- [ ] Double-submit cookie pattern implemented

### 7. Rate Limiting

#### API Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get('/api/endpoint')
@limiter.limit('100/15minutes')
async def api_endpoint(request: Request):
    # 100 requests per 15 minutes
    pass
```

#### Expensive Operations
```python
# Aggressive rate limiting for searches
@app.get('/api/search')
@limiter.limit('10/minute')
async def search_endpoint(request: Request):
    # 10 requests per minute
    pass
```

#### Verification Steps
- [ ] Rate limiting on all API endpoints
- [ ] Stricter limits on expensive operations
- [ ] IP-based rate limiting
- [ ] User-based rate limiting (authenticated)

### 8. Sensitive Data Exposure

#### Logging
```python
import logging

logger = logging.getLogger(__name__)

# ❌ WRONG: Logging sensitive data
logger.info(f'User login: {email}, {password}')
logger.info(f'Payment: {card_number}, {cvv}')

# ✅ CORRECT: Redact sensitive data
logger.info(f'User login: email={email}, user_id={user_id}')
logger.info(f'Payment: last4={card.last4}, user_id={user_id}')
```

#### Error Messages
```python
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

# ❌ WRONG: Exposing internal details
try:
    # Some operation
    pass
except Exception as error:
    raise HTTPException(
        status_code=500,
        detail={'error': str(error), 'stack': traceback.format_exc()}
    )

# ✅ CORRECT: Generic error messages
try:
    # Some operation
    pass
except Exception as error:
    logger.error('Internal error:', exc_info=True)
    raise HTTPException(
        status_code=500,
        detail='An error occurred. Please try again.'
    )
```

#### Verification Steps
- [ ] No passwords, tokens, or secrets in logs
- [ ] Error messages generic for users
- [ ] Detailed errors only in server logs
- [ ] No stack traces exposed to users

### 9. Blockchain Security (Solana)

#### Wallet Verification
```python
from solders.keypair import Keypair
from solders.signature import Signature
import base64

async def verify_wallet_ownership(
    public_key: str,
    signature: str,
    message: str
) -> bool:
    try:
        message_bytes = message.encode('utf-8')
        signature_bytes = base64.b64decode(signature)
        public_key_bytes = base64.b64decode(public_key)

        # Use appropriate Solana library for verification
        # This is a simplified example
        from solders.pubkey import Pubkey
        pubkey = Pubkey.from_bytes(public_key_bytes)
        sig = Signature.from_bytes(signature_bytes)

        # Verify signature (implementation depends on Solana library)
        return True  # Placeholder - implement actual verification
    except Exception:
        return False
```

#### Transaction Verification
```python
from dataclasses import dataclass

@dataclass
class Transaction:
    to: str
    amount: float
    from_address: str

async def verify_transaction(transaction: Transaction) -> bool:
    # Verify recipient
    if transaction.to != expected_recipient:
        raise ValueError('Invalid recipient')

    # Verify amount
    if transaction.amount > max_amount:
        raise ValueError('Amount exceeds limit')

    # Verify user has sufficient balance
    balance = await get_balance(transaction.from_address)
    if balance < transaction.amount:
        raise ValueError('Insufficient balance')

    return True
```

#### Verification Steps
- [ ] Wallet signatures verified
- [ ] Transaction details validated
- [ ] Balance checks before transactions
- [ ] No blind transaction signing

### 10. Dependency Security

#### Regular Updates
```bash
# Check for vulnerabilities (pip)
uv run pip-audit

# Update dependencies (poetry)
uv add <dependency>==<version>
```

#### Lock Files
```bash
# ALWAYS commit lock files
git add requirements.txt  # or uv.lock

# Use in CI/CD for reproducible builds
pip install -r requirements.txt  # Instead of pip install package_name
```

#### Verification Steps
- [ ] Dependencies up to date
- [ ] No known vulnerabilities (pip-audit or poetry audit clean)
- [ ] Lock files committed
- [ ] Dependabot enabled on GitHub
- [ ] Regular security updates

## Security Testing

### Automated Security Tests
```python
import pytest
from httpx import AsyncClient

# Test authentication
@pytest.mark.asyncio
async def test_requires_authentication(client: AsyncClient):
    response = await client.get('/api/protected')
    assert response.status_code == 401

# Test authorization
@pytest.mark.asyncio
async def test_requires_admin_role(client: AsyncClient, user_token: str):
    response = await client.get(
        '/api/admin',
        headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403

# Test input validation
@pytest.mark.asyncio
async def test_rejects_invalid_input(client: AsyncClient):
    response = await client.post(
        '/api/users',
        json={'email': 'not-an-email'}
    )
    assert response.status_code == 400

# Test rate limiting
@pytest.mark.asyncio
async def test_enforces_rate_limits(client: AsyncClient):
    requests = [client.get('/api/endpoint') for _ in range(101)]
    responses = await asyncio.gather(*requests)
    too_many_requests = [r for r in responses if r.status_code == 429]
    assert len(too_many_requests) > 0
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
- [ ] **Security Headers**: CSP, X-Frame-Options configured
- [ ] **Error Handling**: No sensitive data in errors
- [ ] **Logging**: No sensitive data logged
- [ ] **Dependencies**: Up to date, no vulnerabilities
- [ ] **Row Level Security**: Enabled in Supabase
- [ ] **CORS**: Properly configured
- [ ] **File Uploads**: Validated (size, type)
- [ ] **Wallet Signatures**: Verified (if blockchain)

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Web Security Academy](https://portswigger.net/web-security)
- [All Security Topics]https://portswigger.net/web-security/all-topics

---

**Remember**: Security is not optional. One vulnerability can compromise the entire platform. When in doubt, err on the side of caution.
