# Authentication Patterns

## JWT Flow

```
1. Login: POST /auth/login {email, password}
   → Validate credentials
   → Return: {access_token (15min), refresh_token (7d)}

2. API calls: Authorization: Bearer <access_token>
   → Validate signature + expiry
   → Extract user from payload

3. Refresh: POST /auth/refresh {refresh_token}
   → Validate refresh token
   → Return new access_token (rotate refresh optionally)

4. Logout: POST /auth/logout
   → Invalidate refresh token (store in blacklist or delete from DB)
```

### JWT Structure

```json
// Header
{"alg": "HS256", "typ": "JWT"}

// Payload (keep minimal!)
{
  "sub": "user-uuid",      // Subject (user ID)
  "iat": 1640000000,       // Issued at
  "exp": 1640000900,       // Expires (15 min)
  "role": "user"           // Optional claims
}

// Signature
HMACSHA256(base64(header) + "." + base64(payload), secret)
```

### Security Rules

- Access token: short-lived (5-15 min), stateless
- Refresh token: long-lived, stored in DB, rotated on use
- Store refresh token in httpOnly cookie (not localStorage)
- Use different secrets for access/refresh tokens

## OAuth 2.0 / OIDC

```
1. Redirect to provider:
   GET https://provider.com/authorize?
     client_id=XXX&
     redirect_uri=https://app.com/callback&
     response_type=code&
     scope=openid email profile&
     state=random-csrf-token

2. User authenticates, provider redirects:
   GET https://app.com/callback?code=AUTH_CODE&state=...

3. Exchange code for tokens:
   POST https://provider.com/token
   → {access_token, id_token, refresh_token}

4. Get user info from id_token or /userinfo endpoint
```

## Session-based Auth

```
1. Login: validate credentials → create session in DB/Redis
2. Set cookie: session_id=xxx; HttpOnly; Secure; SameSite=Lax
3. Each request: lookup session, attach user to request
4. Logout: delete session from store + clear cookie
```

### Session vs JWT

| Session | JWT |
|---------|-----|
| Stateful (DB/Redis lookup) | Stateless (no lookup) |
| Easy to invalidate | Hard to invalidate before expiry |
| Better for web apps | Better for APIs, mobile |
| CSRF protection needed | No CSRF (if not in cookie) |

## Magic Link

```
1. POST /auth/magic-link {email}
   → Generate token (random 32 bytes, hash stored in DB)
   → Email: https://app.com/auth/verify?token=XXX
   → Token expires in 15 min, single-use

2. GET /auth/verify?token=XXX
   → Hash token, lookup in DB
   → If valid: create session/JWT, delete token
   → If invalid/expired: error
```

## Password Hashing

```python
# Python (argon2)
from argon2 import PasswordHasher
ph = PasswordHasher()
hash = ph.hash(password)
ph.verify(hash, password)  # raises on mismatch

# Node (bcrypt)
import bcrypt from 'bcrypt';
const hash = await bcrypt.hash(password, 12);
await bcrypt.compare(password, hash);
```

**Never:**

- Use MD5, SHA1, SHA256 alone for passwords
- Store plaintext passwords
- Use cost factor < 10 for bcrypt
