# API Authentication

**ID:** api-authentication

## Problem

APIs need secure, scalable authentication. Different use cases need different auth methods.

## Framework

**Auth Method Comparison:**

| Method | Use Case | Pros | Cons |
|--------|----------|------|------|
| **API Keys** | Server-to-server | Simple, no expiry | Revocation hard |
| **JWT** | User sessions | Stateless, claims | Token size, revocation |
| **OAuth 2.0** | Third-party access | Scoped, standard | Complex implementation |
| **mTLS** | High-security | Very secure | Certificate management |

## API Keys

```http
GET /api/users HTTP/1.1
Authorization: Api-Key sk_live_abc123xyz
```

**Implementation:**

```python
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    key = await db.api_keys.find(hashed=hash(x_api_key))
    if not key or key.revoked:
        raise HTTPException(401, "Invalid API key")
    if key.rate_limit_exceeded():
        raise HTTPException(429, "Rate limit exceeded")
    return key

@app.get("/users")
async def get_users(api_key: APIKey = Depends(verify_api_key)):
    # Authenticated request
    pass
```

**Best Practices:**
- Hash keys before storage (like passwords)
- Use prefix for identification: `sk_live_`, `sk_test_`
- Implement key rotation without downtime
- Log key usage for security audits

## JWT (JSON Web Tokens)

**Token Structure:**

```
Header.Payload.Signature

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4ifQ.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

**Payload Claims:**

```json
{
  "sub": "user-123",
  "iss": "https://api.example.com",
  "aud": "https://api.example.com",
  "exp": 1735689600,
  "iat": 1735603200,
  "jti": "unique-token-id",
  "scope": "read:users write:users",
  "role": "admin"
}
```

**Implementation:**

```python
from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(401, "Invalid token")
```

## OAuth 2.0 Flows

**Authorization Code (Web Apps):**

```
1. User clicks "Login with Google"
2. Redirect to: https://auth.example.com/authorize?
     client_id=abc&
     redirect_uri=https://app.com/callback&
     response_type=code&
     scope=read:profile&
     state=random123

3. User authenticates, grants permission
4. Redirect to: https://app.com/callback?code=AUTH_CODE&state=random123

5. Exchange code for tokens:
   POST https://auth.example.com/token
   grant_type=authorization_code&
   code=AUTH_CODE&
   client_id=abc&
   client_secret=xyz&
   redirect_uri=https://app.com/callback

6. Receive:
   {
     "access_token": "...",
     "refresh_token": "...",
     "expires_in": 3600,
     "token_type": "Bearer"
   }
```

**Client Credentials (Server-to-Server):**

```bash
curl -X POST https://auth.example.com/token \
  -d "grant_type=client_credentials" \
  -d "client_id=abc" \
  -d "client_secret=xyz" \
  -d "scope=read:users"
```

## Scope Management

```python
SCOPES = {
    "read:users": "Read user profiles",
    "write:users": "Create and update users",
    "delete:users": "Delete users",
    "admin": "Full administrative access"
}

def require_scope(required: str):
    def checker(token: dict = Depends(verify_token)):
        scopes = token.get("scope", "").split()
        if required not in scopes and "admin" not in scopes:
            raise HTTPException(403, f"Scope '{required}' required")
        return token
    return checker

@app.delete("/users/{id}")
async def delete_user(id: str, _: dict = Depends(require_scope("delete:users"))):
    pass
```

## Best Practices

- Use short-lived access tokens (15-60 min)
- Implement refresh token rotation
- Store secrets in environment variables
- Use HTTPS everywhere
- Implement token revocation
- Log authentication events
- Use asymmetric keys (RS256) for distributed systems

## Agent

faion-api-agent
