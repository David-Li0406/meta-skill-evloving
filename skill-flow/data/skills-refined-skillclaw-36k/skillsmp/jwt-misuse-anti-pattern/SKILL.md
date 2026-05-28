---
name: "jwt-misuse-anti-pattern"
description: "Security anti-pattern for JWT misuse vulnerabilities (CWE-287). Use when generating or reviewing code that creates, validates, or uses JSON Web Tokens. Detects 'none' algorithm attacks, weak secrets, sensitive data in payloads, and missing expiration."
---

# JWT Misuse Anti-Pattern

**Severity:** High

## Summary

JSON Web Tokens (JWTs) are frequently misused in AI-generated code, creating critical vulnerabilities. Common flaws include accepting the "none" algorithm, weak secrets, sensitive data in payloads, and missing expiration. These enable authentication bypass, token forgery, and sensitive data exposure.

## The Anti-Patterns and Solutions

### 1. Algorithm Confusion ("none" Algorithm Attack)

Critical vulnerability where library accepts any algorithm in token header. Attacker changes algorithm to "none" and removes signature, bypassing all cryptographic validation.

#### BAD Code Example

```python
# VULNERABLE: Accepts whatever algorithm is in the header
import jwt

def verify_jwt_vulnerable(token, secret_key):
    # If the token's header is {"alg": "none"}, the library may bypass signature verification entirely.
    try:
        decoded = jwt.decode(token, secret_key, algorithms=None) # algorithms=None or not specified
        return decoded
    except jwt.PyJWTError as e:
        print(f"JWT verification failed: {e}")
        return None
```

#### GOOD Code Example

```python
# SECURE: Explicitly specify allowed algorithms
import jwt

def verify_jwt_secure(token, secret_key):
    # CRITICAL: Always specify exact algorithm(s) expected
    # Library rejects tokens not using specified algorithms
    try:
        decoded = jwt.decode(token, secret_key, algorithms=["HS256", "RS256"])
        return decoded
    except jwt.PyJWTError as e:
        print(f"JWT verification failed: {e}")
        return None
```

### 2. Weak Secret

Weak, predictable, or hardcoded secrets for symmetric signing algorithms (HS256) enable attackers to brute-force secrets and forge valid tokens.

#### BAD Code Example

```python
# VULNERABLE: Weak or short secret key
import jwt

JWT_SECRET = "secret123"  # Easily brute-forced!

def create_jwt(user_id):
    payload = {"user_id": user_id}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")
```

#### GOOD Code Example

```python
# SECURE: Strong, centrally managed secret
import jwt
import os

# Load strong, randomly generated secret from environment or secret manager
JWT_SECRET = os.environ.get("JWT_SECRET")

def initialize():
    if not JWT_SECRET or len(JWT_SECRET) < 32:
        raise ValueError("JWT_SECRET must be at least 256 bits (32 chars) for HS256")

# For production, use asymmetric keys (RS256): private key kept secret,
# public key safely distributed for verification
def create_jwt_asymmetric(user_id, private_key):
    payload = {"sub": user_id}
    return jwt.encode(payload, private_key, algorithm="RS256")
```

### 3. Sensitive Data in Payload

JWT payload is Base64Url-encoded, not encrypted. Anyone intercepting the token can decode and read it. Storing PII, passwords, or internal data in payload creates major security risk.

#### BAD Code Example

```python
# VULNERABLE: Sensitive data in JWT payload
import jwt

def create_jwt_with_pii(user, secret_key):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "ssn": user.social_security_number,  # PII EXPOSED!
        "password_hash": user.password_hash # CRITICAL RISK!
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")
```

#### GOOD Code Example

```python
# SECURE: Minimal, non-sensitive claims
import jwt
import time

def create_jwt_secure(user, secret_key):
    payload = {
        "sub": user.id,          # Subject (user ID) - standard, non-sensitive
        "iat": int(time.time()), # Issued at - standard
        "exp": int(time.time()) + 3600, # Expiration (1 hour) - standard
        "role": user.role        # Non-sensitive custom claim
    }
    # Never include passwords, PII, payment info, or internal data
    # Server fetches data from secure database using user ID from token
    return jwt.encode(payload, secret_key, algorithm="HS256")
```

### Language-Specific Examples

**JavaScript/Node.js:**
```javascript
// VULNERABLE: Multiple JWT misuse patterns
const jwt = require('jsonwebtoken');

// Weak secret
const SECRET = 'mysecret';

// No algorithm specified - accepts "none"!
function verifyToken(token) {
    return jwt.verify(token, SECRET); // CRITICAL FLAW
}

// Sensitive data in payload, no expiration
function createToken(user) {
    return jwt.sign({
        id: user.id,
        email: user.email,
        password: user.passwordHash, // EXPOSED!
        ssn: user.ssn // EXPOSED!
        // No exp claim!
    }, SECRET);
}
```

```javascript
// SECURE: Proper JWT implementation
const jwt = require('jsonwebtoken');

const SECRET = process.env.JWT_SECRET; // Strong, env-based secret
if (!SECRET || SECRET.length < 32) {
    throw new Error('JWT_SECRET must be at least 256 bits');
}

function verifyToken(token) {
    // CRITICAL: Explicitly specify allowed algorithms
    return jwt.verify(token, SECRET, {
        algorithms: ['HS256'],
        maxAge: '1h' // Also enforce expiration
    });
}

function createToken(user) {
    const now = Math.floor(Date.now() / 1000);
    return jwt.sign({
        sub: user.id,          // Standard claim
        iat: now,              // Issued at
        exp: now + 3600,       // Expires in 1 hour
        role: user.role        // Non-sensitive only
    }, SECRET, {
        algorithm: 'HS256'
    });
}
```

**Java:**
```java
// VULNERABLE: Weak secret and no algorithm enforcement
import io.jsonwebtoken.*;

public class JwtService {
    private static final String SECRET = "secret123"; // Weak!

    public Claims verifyToken(String token) {
        // No algorithm specified - vulnerable to none attack
        return Jwts.parser()
            .setSigningKey(SECRET)
            .parseClaimsJws(token)
            .getBody();
    }

    public String createToken(User user) {
        // No expiration, sensitive data included
        return Jwts.builder()
            .setSubject(user.getId())
            .claim("email", user.getEmail())
            .claim("ssn", user.getSsn()) // EXPOSED!
            .signWith(SignatureAlgorithm.HS256, SECRET)
            .compact();
    }
}
```

```java
// SECURE: Proper JWT implementation
import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import java.security.Key;
import java.util.Date;

public class SecureJwtService {
    // Load from environment or secret manager
    private static final String SECRET_KEY = System.getenv("JWT_SECRET");
    private static final Key KEY = Keys.hmacShaKeyFor(SECRET_KEY.getBytes());

    public Claims verifyToken(String token) {
        // Explicitly require HS256 algorithm
        return Jwts.parserBuilder()
            .setSigningKey(KEY)
            .requireAlgorithm("HS256")
            .build()
            .parseClaimsJws(token)
            .getBody();
    }

    public String createToken(User user) {
        long nowMillis = System.currentTimeMillis();
        Date now = new Date(nowMillis);
        Date expiry = new Date(nowMillis + 3600000); // 1 hour

        return Jwts.builder()
            .setSubject(user.getId())
            .setIssuedAt(now)
            .setExpiration(expiry) // REQUIRED
            .claim("role", user.getRole()) // Non-sensitive only
            .signWith(KEY, SignatureAlgorithm.HS256)
            .compact();
    }
}
```

## Detection

- **Find algorithm confusion vulnerabilities:** Grep for unsafe jwt.decode calls:
  - `rg 'jwt\.decode.*algorithms\s*=\s*(None|null|\[\])'`
  - `rg 'jwt\.decode' | rg -v 'algorithms='` (missing explicit algorithm)
  - `rg 'verify.*false|verify:\s*false' --type js` (disabled verification)
- **Identify weak secrets:** Search for hardcoded JWT keys:
  - `rg 'JWT_SECRET.*=.*["\'][^"\']{1,16}["\']'` (short secrets < 32 chars)
  - `rg 'secret.*password|password.*jwt' -i`
  - Use gitleaks/trufflehog to scan for leaked secrets
- **Find sensitive data in payloads:** Audit JWT creation:
  - `rg 'jwt\.encode|jwt\.sign' -A 5`
  - Check for PII: `ssn`, `password`, `credit_card`, `email`, `phone`
- **Detect missing expiration:** Find tokens without exp claim:
  - `rg 'jwt\.encode' -A 5 | rg -v 'exp|expir'`
  - Verify all tokens include expiration timestamps

## Prevention

- [ ] **Always specify allowed algorithms:** Explicitly declare during token verification
- [ ] **Use strong secrets:** At least 256 bits for HS256. Prefer asymmetric algorithms (RS256/ES256) for production
- [ ] **Never store sensitive data:** JWT payload readable by anyone
- [ ] **Always include `exp` claim:** Reasonably short lifetime for access tokens
- [ ] **Implement token refresh:** For sessions longer than access token lifetime
- [ ] **Consider token revocation list:** Invalidate tokens for compromised accounts

## Related Security Patterns & Anti-Patterns

- [Hardcoded Secrets Anti-Pattern](../hardcoded-secrets/): JWT secrets commonly hardcoded
- [Session Fixation Anti-Pattern](../session-fixation/): Alternative session management strategies
- [Insufficient Randomness Anti-Pattern](../insufficient-randomness/): Relevant for generating unique token identifiers (`jti`)

## References

- [OWASP Top 10 A07:2025 - Authentication Failures](https://owasp.org/Top10/2025/A07_2025-Authentication_Failures/)
- [OWASP GenAI LLM06:2025 - Excessive Agency](https://genai.owasp.org/llmrisk/llm06-excessive-agency/)
- [OWASP API Security API2:2023 - Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [CWE-287: Improper Authentication](https://cwe.mitre.org/data/definitions/287.html)
- [CAPEC-220: Client-Server Protocol Manipulation](https://capec.mitre.org/data/definitions/220.html)
- [PortSwigger: Jwt](https://portswigger.net/web-security/jwt)
- [BlueKrypt - Cryptographic Key Length Recommendation](https://www.keylength.com/)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
