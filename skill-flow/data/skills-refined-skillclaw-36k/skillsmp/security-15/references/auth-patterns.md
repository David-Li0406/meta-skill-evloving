# Authentication & Authorization Patterns

Best practices for implementing secure authentication and authorization.

## Authentication Methods Comparison

| Method | Use Case | Pros | Cons |
|--------|----------|------|------|
| Session cookies | Web apps, SSR | Simple, secure with httpOnly | Requires session storage |
| JWT | APIs, SPAs, mobile | Stateless, scalable | Token revocation complex |
| OAuth 2.0 | Third-party auth | Delegated access | Complex implementation |
| API keys | Service-to-service | Simple | No user context, hard to rotate |
| mTLS | Service mesh | Strong auth | Certificate management |

## JWT Best Practices

### Secure JWT Configuration

```javascript
// ✅ SECURE: Short-lived access tokens
const accessToken = jwt.sign(
  { sub: user.id, scope: ['read', 'write'] },
  ACCESS_SECRET,
  {
    algorithm: 'RS256',  // Use asymmetric
    expiresIn: '15m',    // Short expiry
    issuer: 'my-app',
    audience: 'my-api'
  }
);

// Refresh tokens (longer-lived, stored securely)
const refreshToken = jwt.sign(
  { sub: user.id, tokenId: uuid() },  // Track for revocation
  REFRESH_SECRET,
  { expiresIn: '7d' }
);
```

### JWT Anti-Patterns

```javascript
// ❌ BAD: Algorithm confusion attack
jwt.verify(token, secret);  // Accepts any algorithm!

// ✅ GOOD: Specify algorithm
jwt.verify(token, secret, { algorithms: ['RS256'] });

// ❌ BAD: Sensitive data in payload
jwt.sign({ password: user.password }, secret);

// ❌ BAD: Long expiry
jwt.sign(payload, secret, { expiresIn: '30d' });

// ❌ BAD: Storing in localStorage
localStorage.setItem('token', accessToken);  // XSS vulnerable

// ✅ GOOD: HttpOnly cookie
res.cookie('access_token', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
  maxAge: 15 * 60 * 1000  // 15 minutes
});
```

## Session Management

### Secure Session Configuration

```javascript
app.use(session({
  name: '__Host-session',  // Cookie prefix for extra security
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,
    secure: true,
    sameSite: 'strict',
    maxAge: 24 * 60 * 60 * 1000  // 24 hours
  },
  store: new RedisStore({ client: redisClient })
}));
```

### Session Security Checklist

- [ ] Regenerate session ID after login
- [ ] Invalidate session on logout
- [ ] Set absolute timeout (e.g., 24h)
- [ ] Set idle timeout (e.g., 30min)
- [ ] Bind to user agent/IP (optional, breaks mobile)
- [ ] Store minimal data in session

## Password Security

### Password Hashing

```python
# ✅ Argon2 (recommended)
from argon2 import PasswordHasher
ph = PasswordHasher(
    time_cost=3,        # Iterations
    memory_cost=65536,  # 64MB
    parallelism=4
)
hash = ph.hash(password)
ph.verify(hash, password)  # Raises on failure

# ✅ bcrypt (widely supported)
import bcrypt
hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))
bcrypt.checkpw(password.encode(), hash)
```

### Password Requirements

```javascript
function validatePassword(password) {
  const errors = [];

  if (password.length < 12) {
    errors.push('Minimum 12 characters');
  }
  if (password.length > 128) {
    errors.push('Maximum 128 characters');
  }
  // Check against breached passwords
  if (await isBreached(password)) {
    errors.push('Password found in data breach');
  }

  return errors;
}
```

## Multi-Factor Authentication

### TOTP Implementation

```javascript
import { authenticator } from 'otplib';

// Generate secret for user
const secret = authenticator.generateSecret();

// Generate QR code URI
const otpauth = authenticator.keyuri(user.email, 'MyApp', secret);

// Verify token
function verifyTOTP(token, secret) {
  return authenticator.verify({ token, secret });
}
```

### MFA Best Practices

- [ ] Require MFA for sensitive operations
- [ ] Provide backup codes (one-time use)
- [ ] Support multiple methods (TOTP, WebAuthn, SMS)
- [ ] Rate limit MFA attempts
- [ ] Allow recovery without disabling security

## OAuth 2.0 / OIDC

### Authorization Code Flow (Recommended)

```javascript
// Step 1: Redirect to authorization server
const authUrl = new URL('https://auth.example.com/authorize');
authUrl.searchParams.set('client_id', CLIENT_ID);
authUrl.searchParams.set('redirect_uri', REDIRECT_URI);
authUrl.searchParams.set('response_type', 'code');
authUrl.searchParams.set('scope', 'openid profile email');
authUrl.searchParams.set('state', generateState());
authUrl.searchParams.set('code_challenge', codeChallenge);  // PKCE
authUrl.searchParams.set('code_challenge_method', 'S256');

// Step 2: Exchange code for tokens (server-side)
const tokenResponse = await fetch('https://auth.example.com/token', {
  method: 'POST',
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    code: req.query.code,
    redirect_uri: REDIRECT_URI,
    client_id: CLIENT_ID,
    client_secret: CLIENT_SECRET,  // Server-side only!
    code_verifier: codeVerifier    // PKCE
  })
});
```

### OAuth Security Checklist

- [ ] Always use PKCE (even for confidential clients)
- [ ] Validate `state` parameter
- [ ] Use `response_type=code` (not `token`)
- [ ] Keep client_secret server-side only
- [ ] Validate ID token claims (iss, aud, exp, nonce)
- [ ] Use short-lived access tokens

## Authorization Patterns

### Role-Based Access Control (RBAC)

```javascript
const PERMISSIONS = {
  admin: ['read', 'write', 'delete', 'admin'],
  editor: ['read', 'write'],
  viewer: ['read']
};

function authorize(requiredPermission) {
  return (req, res, next) => {
    const userPermissions = PERMISSIONS[req.user.role] || [];
    if (!userPermissions.includes(requiredPermission)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}

app.delete('/api/posts/:id', authorize('delete'), deletePost);
```

### Attribute-Based Access Control (ABAC)

```javascript
function canAccess(user, resource, action) {
  const policies = [
    // Owner can do anything
    (u, r, a) => r.ownerId === u.id,

    // Admins can do anything
    (u, r, a) => u.role === 'admin',

    // Team members can read team resources
    (u, r, a) => a === 'read' && u.teamId === r.teamId,

    // Published content is public
    (u, r, a) => a === 'read' && r.status === 'published'
  ];

  return policies.some(policy => policy(user, resource, action));
}
```

## API Key Security

```javascript
// Generate secure API key
function generateApiKey() {
  const prefix = 'sk_live_';  // Identifiable prefix
  const key = crypto.randomBytes(32).toString('base64url');
  return prefix + key;
}

// Store hashed, not plain
async function createApiKey(userId) {
  const key = generateApiKey();
  const hash = crypto.createHash('sha256').update(key).digest('hex');

  await db.apiKeys.create({
    userId,
    keyHash: hash,
    prefix: key.slice(0, 12),  // For identification
    createdAt: new Date()
  });

  return key;  // Return once, never store plain
}

// Verify API key
async function verifyApiKey(key) {
  const hash = crypto.createHash('sha256').update(key).digest('hex');
  return db.apiKeys.findOne({ keyHash: hash });
}
```
