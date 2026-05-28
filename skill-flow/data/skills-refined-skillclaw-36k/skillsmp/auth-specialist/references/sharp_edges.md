# Auth Specialist - Sharp Edges

## Jwt Algorithm None Attack

### **Id**
jwt-algorithm-none-attack
### **Summary**
JWT libraries may accept 'alg:none' tokens, bypassing signature verification
### **Severity**
critical
### **Situation**
Using JWT libraries without explicit algorithm enforcement
### **Why**
  Early JWT specs allowed "none" as a valid algorithm (unsigned tokens).
  Many libraries still accept this if not explicitly blocked. An attacker
  changes the header to {"alg":"none"}, removes the signature, and the
  library accepts it as valid. Complete auth bypass with zero crypto knowledge.
  
### **Solution**
  Always specify allowed algorithms explicitly in verify():
  ```javascript
  jwt.verify(token, secret, { algorithms: ['HS256'] })  // Explicit
  // NOT: jwt.verify(token, secret)  // Trusts header
  ```
  Test your implementation by sending an alg:none token.
  
### **Detection Pattern**
jwt\.verify\([^,]+,\s*[^,]+\s*\)(?!.*algorithms)
### **References**
  - https://portswigger.net/web-security/jwt

## Jwt Algorithm Confusion

### **Id**
jwt-algorithm-confusion
### **Summary**
RS256 tokens accepted as HS256 using public key as secret
### **Severity**
critical
### **Situation**
Applications using RSA-signed JWTs (RS256, RS384, RS512)
### **Why**
  RS256 uses asymmetric crypto: sign with private key, verify with public.
  HS256 uses symmetric: same secret for both. If attacker knows your public
  key (often exposed), they craft a token with alg:HS256, signed using the
  public key as the HMAC secret. Library verifies with public key = valid token.
  
### **Solution**
  Explicit algorithm enforcement prevents this entirely:
  ```javascript
  // For RSA tokens, ONLY allow RSA
  jwt.verify(token, publicKey, { algorithms: ['RS256'] })
  // Never let the token header dictate the algorithm
  ```
  
### **Detection Pattern**
algorithms.*\[.*RS.*HS.*\]|algorithms.*\[.*HS.*RS.*\]
### **References**
  - https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/

## Oauth State Parameter Missing

### **Id**
oauth-state-parameter-missing
### **Summary**
OAuth without state parameter enables CSRF login attacks
### **Severity**
high
### **Situation**
Implementing OAuth authorization code flow
### **Why**
  Without state, attacker initiates OAuth flow, gets their authorization code,
  tricks victim into loading callback URL with attacker's code. Victim is now
  logged into attacker's account. Attacker sees everything victim does,
  including sensitive data they add to "their" account.
  
### **Solution**
  Generate cryptographically random state, store in session, validate on callback:
  ```javascript
  // Before redirect
  const state = crypto.randomUUID();
  session.oauthState = state;
  authUrl.searchParams.set('state', state);
  
  // On callback
  if (req.query.state !== session.oauthState) {
    throw new Error('State mismatch - possible CSRF');
  }
  delete session.oauthState;
  ```
  
### **Detection Pattern**
authorize\?(?!.*state=)

## Redirect Uri Open Redirect

### **Id**
redirect-uri-open-redirect
### **Summary**
OAuth redirect_uri not validated allows token theft
### **Severity**
critical
### **Situation**
Configuring OAuth applications and callback URLs
### **Why**
  If authorization server allows wildcard or partial redirect_uri matching,
  attacker registers https://evil.com/callback or finds open redirect on
  your domain. Authorization code or token ends up at attacker's server.
  Always require exact match on full URI including path and query.
  
### **Solution**
  - Register exact redirect URIs with no wildcards
  - Use exact string matching, not prefix/suffix
  - Check for open redirects on your domain
  - Different URIs for different environments (dev/staging/prod)
  ```javascript
  const ALLOWED_REDIRECTS = [
    'https://app.example.com/auth/callback',
    'http://localhost:3000/auth/callback',  // Dev only
  ];
  if (!ALLOWED_REDIRECTS.includes(redirect_uri)) {
    throw new Error('Invalid redirect_uri');
  }
  ```
  
### **Detection Pattern**
redirect.*\*|redirect.*startsWith|redirect.*includes

## Refresh Token No Rotation

### **Id**
refresh-token-no-rotation
### **Summary**
Static refresh tokens provide permanent access if compromised
### **Severity**
high
### **Situation**
Implementing refresh token mechanism
### **Why**
  Non-rotating refresh tokens are valid until explicitly revoked. If stolen
  (XSS, malware, log exposure), attacker maintains access indefinitely even
  after user changes password. You may never know it was compromised.
  
### **Solution**
  Rotate on every use, detect reuse (indicates theft):
  ```javascript
  async function refresh(oldToken) {
    const family = await db.findTokenFamily(oldToken);
    if (family.currentToken !== oldToken) {
      // Token already used = compromised
      await db.invalidateFamily(family.id);
      throw new SecurityError('Token reuse detected');
    }
    const newRefresh = generateToken();
    await db.updateFamily(family.id, newRefresh);
    return { access: newAccessToken(), refresh: newRefresh };
  }
  ```
  
### **Detection Pattern**
refresh.*token(?!.*rotat|.*new|.*generat)

## Bcrypt 72 Byte Limit

### **Id**
bcrypt-72-byte-limit
### **Summary**
bcrypt silently truncates passwords over 72 bytes
### **Severity**
medium
### **Situation**
Using bcrypt for password hashing with potentially long passwords
### **Why**
  bcrypt has a 72-byte input limit. Longer passwords are silently truncated.
  Two passwords sharing the same first 72 bytes hash identically. Passphrases
  and concatenated passwords may exceed this. Users think they're secure with
  a 100-character password but only 72 bytes are checked.
  
### **Solution**
  Use Argon2id (no limit) or pre-hash with SHA-256:
  ```javascript
  // Pre-hash for bcrypt (preserves entropy)
  const preHashed = crypto
    .createHash('sha256')
    .update(password)
    .digest('base64');
  const hash = await bcrypt.hash(preHashed, 12);
  
  // Better: just use Argon2id
  const hash = await argon2.hash(password);  // No limit
  ```
  
### **Detection Pattern**
bcrypt\.hash\((?!.*sha|.*argon)

## Timing Attack String Comparison

### **Id**
timing-attack-string-comparison
### **Summary**
Direct string comparison for tokens leaks validity via timing
### **Severity**
medium
### **Situation**
Comparing secrets, tokens, or API keys in authentication checks
### **Why**
  String === exits on first mismatch. Token "abc123" vs "xyz789" fails faster
  than "abc123" vs "abc124". Attackers measure response times to deduce correct
  bytes one at a time. Not theoretical - demonstrated in practice.
  
### **Solution**
  Use constant-time comparison:
  ```javascript
  import crypto from 'crypto';
  
  function secureCompare(a: string, b: string): boolean {
    if (a.length !== b.length) {
      // Lengths differ, but still do comparison to maintain timing
      crypto.timingSafeEqual(
        Buffer.from(a.padEnd(Math.max(a.length, b.length))),
        Buffer.from(b.padEnd(Math.max(a.length, b.length)))
      );
      return false;
    }
    return crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b));
  }
  ```
  
### **Detection Pattern**
token\s*===\s*|secret\s*===\s*|apiKey\s*===\s*

## Nextauth Missing Secret

### **Id**
nextauth-missing-secret
### **Summary**
NextAuth without NEXTAUTH_SECRET uses predictable encryption
### **Severity**
critical
### **Situation**
Deploying NextAuth.js to production
### **Why**
  Without NEXTAUTH_SECRET, the library generates a key from your source code.
  This is predictable and shared across all instances. Session cookies can be
  forged. Anyone with your source code (open source, leaked, guessed) can
  create valid admin sessions.
  
### **Solution**
  Set strong secret in environment:
  ```bash
  # Generate: openssl rand -base64 32
  NEXTAUTH_SECRET="K7gNU3sdo+Owv0iMJTH5UvYrzyKl4hMn+..."
  ```
  NextAuth v5 (Auth.js) requires this - fails without it.
  
### **Detection Pattern**
NextAuth\((?!.*secret)

## Cookie Samesite None Without Secure

### **Id**
cookie-samesite-none-without-secure
### **Summary**
SameSite=None without Secure flag exposes cookies on HTTP
### **Severity**
high
### **Situation**
Configuring cookies for cross-site scenarios
### **Why**
  Browsers require Secure flag when SameSite=None. Without it, cookie is
  either rejected entirely (modern browsers) or sent over HTTP (older
  browsers), exposing it to network attackers. Cross-site auth flows break
  in production.
  
### **Solution**
  Always pair SameSite=None with Secure=true:
  ```javascript
  res.cookie('session', value, {
    sameSite: 'none',
    secure: true,  // Required for SameSite=None
    httpOnly: true,
  });
  
  // For same-site apps, prefer 'lax' or 'strict' instead
  ```
  
### **Detection Pattern**
sameSite.*none(?!.*secure.*true)

## Session Fixation No Regeneration

### **Id**
session-fixation-no-regeneration
### **Summary**
Session ID not regenerated after login enables session fixation
### **Severity**
high
### **Situation**
Implementing session-based authentication
### **Why**
  Attacker gets a valid session ID (their own), tricks victim into using it
  (via URL parameter or cookie injection). Victim logs in, session now has
  their auth. Attacker uses same session ID = logged in as victim.
  
### **Solution**
  Regenerate session ID after authentication state changes:
  ```javascript
  async function login(req, user) {
    // Regenerate BEFORE setting user
    await new Promise((resolve, reject) => {
      req.session.regenerate((err) => {
        if (err) reject(err);
        else resolve(null);
      });
    });
  
    // Now set authenticated user
    req.session.userId = user.id;
    await req.session.save();
  }
  ```
  
### **Detection Pattern**
session\.user\s*=(?!.*regenerate)

## Password In Logs Or Errors

### **Id**
password-in-logs-or-errors
### **Summary**
Passwords appearing in logs, error messages, or stack traces
### **Severity**
critical
### **Situation**
Implementing login endpoints with logging
### **Why**
  Logging request bodies or error details may include plaintext passwords.
  Log aggregators store indefinitely. Anyone with log access sees credentials.
  Password appears in: req.body, error.message, JSON.stringify(req).
  
### **Solution**
  Sanitize before logging:
  ```javascript
  function sanitizeRequest(req) {
    const sanitized = { ...req.body };
    if (sanitized.password) sanitized.password = '[REDACTED]';
    if (sanitized.token) sanitized.token = '[REDACTED]';
    return sanitized;
  }
  
  // Never log raw request body
  logger.info('Login attempt', { user: req.body.email });
  // NOT: logger.info('Login', req.body);
  ```
  
### **Detection Pattern**
console\.log.*password|logger\.(info|error|debug).*req\.body

## Oidc Nonce Not Validated

### **Id**
oidc-nonce-not-validated
### **Summary**
OIDC ID token accepted without nonce validation enables replay
### **Severity**
high
### **Situation**
Implementing OpenID Connect authentication
### **Why**
  The nonce parameter binds the ID token to the session. Without validation,
  attacker captures an ID token and replays it in their session = logged in
  as victim. CVE-2024-10318 in NGINX OIDC was exactly this bug.
  
### **Solution**
  Generate nonce, include in auth request, validate in ID token:
  ```javascript
  // Before auth redirect
  const nonce = crypto.randomUUID();
  session.oidcNonce = nonce;
  authUrl.searchParams.set('nonce', nonce);
  
  // After receiving ID token
  const idToken = jwt.decode(tokens.id_token);
  if (idToken.nonce !== session.oidcNonce) {
    throw new Error('Nonce mismatch - possible replay');
  }
  delete session.oidcNonce;
  ```
  
### **Detection Pattern**
id_token(?!.*nonce)