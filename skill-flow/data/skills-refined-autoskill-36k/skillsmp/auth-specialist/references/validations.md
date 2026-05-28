# Auth Specialist - Validations

## JWT Verify Without Explicit Algorithm

### **Id**
jwt-verify-no-algorithm
### **Severity**
error
### **Type**
regex
### **Pattern**
  - jwt\.verify\(\s*\w+\s*,\s*\w+\s*\)(?!\s*,|\s*{)
  - verify\(\s*token\s*,\s*secret\s*\)(?!.*algorithms)
  - \.verify\([^)]+\)(?!.*algorithms.*\[)
### **Message**
JWT verification without explicit algorithm. Vulnerable to algorithm confusion attacks.
### **Fix Action**
Add { algorithms: ['HS256'] } or ['RS256'] as third parameter to verify()
### **Applies To**
  - *.ts
  - *.js
  - *.mjs

## Using jwt.decode() for Authentication

### **Id**
jwt-decode-for-auth
### **Severity**
error
### **Type**
regex
### **Pattern**
  - jwt\.decode\(.*\).*(?:user|auth|session|role|admin)
  - (?:if|when).*decode\(.*token
  - decode\(.*\)\.(?:userId|sub|role)
### **Message**
Using decode() for authentication. decode() does NOT verify signatures.
### **Fix Action**
Use jwt.verify() with secret/public key and explicit algorithm
### **Applies To**
  - *.ts
  - *.js

## Direct String Comparison for Secrets

### **Id**
password-direct-comparison
### **Severity**
error
### **Type**
regex
### **Pattern**
  - password\s*===\s*
  - token\s*===\s*(?!.*length)
  - apiKey\s*===\s*
  - secret\s*===\s*
### **Message**
Direct string comparison for secrets enables timing attacks.
### **Fix Action**
Use crypto.timingSafeEqual() for constant-time comparison
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Weak Hash Algorithm for Passwords

### **Id**
md5-sha1-password-hash
### **Severity**
error
### **Type**
regex
### **Pattern**
  - createHash\(['"]md5['"]\).*password
  - createHash\(['"]sha1['"]\).*password
  - hashlib\.(md5|sha1).*password
  - MD5\.hashStr.*password
### **Message**
MD5/SHA1 for password hashing. These are cryptographically broken for passwords.
### **Fix Action**
Use argon2id (preferred) or bcrypt with cost factor 12+
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Hardcoded JWT Secret

### **Id**
hardcoded-jwt-secret
### **Severity**
error
### **Type**
regex
### **Pattern**
  - jwt\.sign\([^,]+,\s*['"][^'"]{8,}['"]
  - jwt\.verify\([^,]+,\s*['"][^'"]{8,}['"]
  - secret\s*[:=]\s*['"][^'"]{8,}['"].*jwt
### **Message**
Hardcoded JWT secret in code. Will be exposed in version control.
### **Fix Action**
Use environment variable: process.env.JWT_SECRET
### **Applies To**
  - *.ts
  - *.js

## OAuth Request Without State Parameter

### **Id**
oauth-no-state
### **Severity**
error
### **Type**
regex
### **Pattern**
  - authorize\?(?!.*state=)
  - /oauth/authorize(?!.*state)
  - authorizationUrl(?!.*state)
### **Message**
OAuth authorization without state parameter. Vulnerable to CSRF attacks.
### **Fix Action**
Generate random state, store in session, validate on callback
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Cookie Without Security Flags

### **Id**
cookie-missing-security-flags
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - cookie\([^)]+\)(?!.*httpOnly)
  - setCookie\([^)]+\)(?!.*httpOnly)
  - cookies\.set\([^)]+\)(?!.*httpOnly)
### **Message**
Cookie set without httpOnly flag. Accessible to JavaScript (XSS vulnerable).
### **Fix Action**
Add httpOnly: true, secure: true, sameSite: 'lax' to cookie options
### **Applies To**
  - *.ts
  - *.js

## Session Not Regenerated After Login

### **Id**
session-no-regeneration
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - session\.user\s*=(?!.*regenerate)
  - req\.session\.userId\s*=(?!.*regenerate)
  - setUser\(.*\)(?!.*regenerate)
### **Message**
Session ID not regenerated after login. Vulnerable to session fixation.
### **Fix Action**
Call session.regenerate() before setting user data
### **Applies To**
  - *.ts
  - *.js

## Password May Be Logged

### **Id**
password-in-log
### **Severity**
error
### **Type**
regex
### **Pattern**
  - console\.(log|error|info|debug).*password
  - logger\.\w+.*req\.body(?!.*sanitize|redact)
  - JSON\.stringify\(.*req\.body
### **Message**
Password or request body may be logged. Sensitive data in logs.
### **Fix Action**
Sanitize request body before logging, redact password fields
### **Applies To**
  - *.ts
  - *.js

## Access Token With Long Expiry

### **Id**
access-token-long-expiry
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - expiresIn.*['"]\d+d['"]
  - expiresIn.*['"][3-9]h['"]
  - expiresIn.*86400|expiresIn.*3600\d
  - maxAge.*86400000
### **Message**
Access token with long expiry (>1 hour). Should be 15-60 minutes max.
### **Fix Action**
Use 15-30 minute access tokens with refresh token rotation
### **Applies To**
  - *.ts
  - *.js

## Bcrypt With Low Cost Factor

### **Id**
bcrypt-low-cost
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - bcrypt\.hash\([^,]+,\s*[1-9]\)
  - bcrypt\.hash\([^,]+,\s*1[01]\)
  - genSalt\(\s*[1-9]\s*\)
### **Message**
Bcrypt cost factor below 12. Increases brute force speed significantly.
### **Fix Action**
Use cost factor 12 or higher (balance with login latency)
### **Applies To**
  - *.ts
  - *.js

## NextAuth Without Secret Configuration

### **Id**
nextauth-no-secret
### **Severity**
error
### **Type**
regex
### **Pattern**
  - NextAuth\(\s*\{(?![\s\S]*secret)[\s\S]*\}\s*\)
  - authOptions\s*=\s*\{(?![\s\S]*secret)
### **Message**
NextAuth configuration without explicit secret. Uses predictable encryption.
### **Fix Action**
Add secret: process.env.NEXTAUTH_SECRET to NextAuth options
### **Applies To**
  - *.ts
  - *.js
  - **/auth.ts
  - **/[...nextauth].ts

## JWT Stored in localStorage

### **Id**
localstorage-token
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - localStorage\.setItem\([^,]*token
  - localStorage\.setItem\([^,]*jwt
  - localStorage\.setItem\([^,]*access
  - localStorage\[['"].*token
### **Message**
Storing token in localStorage. Accessible to any JavaScript (XSS vulnerable).
### **Fix Action**
Store tokens in HttpOnly cookies, or keep in memory with refresh via cookie
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## OAuth Without PKCE

### **Id**
pkce-missing
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - response_type.*code(?!.*code_challenge)
  - grant_type.*authorization_code(?!.*code_verifier)
  - /authorize\?(?!.*code_challenge)
### **Message**
OAuth authorization code flow without PKCE. Required by OAuth 2.1.
### **Fix Action**
Add code_challenge to authorize request, code_verifier to token exchange
### **Applies To**
  - *.ts
  - *.js