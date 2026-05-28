# Authentication Oauth - Validations

## JWT Token in localStorage

### **Id**
auth-jwt-localstorage
### **Severity**
error
### **Type**
regex
### **Pattern**
  - localStorage\.setItem\([^)]*token
  - localStorage\.setItem\([^)]*jwt
  - localStorage\.setItem\([^)]*accessToken
  - localStorage\[.*(token|jwt)
### **Message**
JWT stored in localStorage is vulnerable to XSS. Use HttpOnly cookies or memory.
### **Fix Action**
Store access tokens in memory, refresh tokens in HttpOnly cookies
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Token in URL Query Parameter

### **Id**
auth-token-in-url
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \?.*token=
  - \?.*access_token=
  - \?.*jwt=
  - searchParams.*token
### **Message**
Token in URL can leak via referrer, logs, and browser history.
### **Fix Action**
Pass tokens in headers or request body instead
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Plaintext Password Storage

### **Id**
auth-plaintext-password
### **Severity**
error
### **Type**
regex
### **Pattern**
  - password:\s*req\.body\.password
  - password:\s*password\b
  - user\.password\s*=\s*password
### **Message**
Possible plaintext password storage. Always hash passwords.
### **Fix Action**
Use bcrypt.hash(password, 12) before storing
### **Applies To**
  - **/*.ts
  - **/*.js

## Weak Password Hashing

### **Id**
auth-weak-hash
### **Severity**
error
### **Type**
regex
### **Pattern**
  - md5\([^)]*password
  - sha1\([^)]*password
  - sha256\([^)]*password
  - createHash\(['"](?:md5|sha1|sha256)['"]\).*password
### **Message**
MD5/SHA1/SHA256 are too fast for password hashing. Use bcrypt or Argon2.
### **Fix Action**
Replace with bcrypt.hash(password, 12) or argon2.hash(password)
### **Applies To**
  - **/*.ts
  - **/*.js

## Hardcoded JWT Secret

### **Id**
auth-hardcoded-secret
### **Severity**
error
### **Type**
regex
### **Pattern**
  - jwt\.sign\([^)]+['"][a-zA-Z0-9]{1,30}['"]\s*\)
  - secret.*=.*['"][a-zA-Z0-9]{1,30}['"]
  - JWT_SECRET.*=.*['"][a-zA-Z0-9]{1,30}['"]
### **Message**
Hardcoded or weak JWT secret. Use environment variable with strong random value.
### **Fix Action**
Use process.env.JWT_SECRET with 256+ bit random value
### **Applies To**
  - **/*.ts
  - **/*.js

## OAuth Without State Parameter

### **Id**
auth-no-oauth-state
### **Severity**
error
### **Type**
regex
### **Pattern**
  - oauth.*callback(?![\s\S]{0,200}state)
  - /callback.*code(?![\s\S]{0,100}state)
  - authorization_code(?![\s\S]{0,200}state)
### **Message**
OAuth callback without state validation. Vulnerable to CSRF.
### **Fix Action**
Generate random state on auth start, validate on callback
### **Applies To**
  - **/*.ts
  - **/*.js

## OAuth Without PKCE

### **Id**
auth-no-pkce
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - response_type.*code(?![\s\S]{0,300}code_challenge)
  - authorization_code(?![\s\S]{0,300}code_verifier)
### **Message**
OAuth without PKCE. Consider adding for extra security on public clients.
### **Fix Action**
Add code_challenge and code_verifier for PKCE flow
### **Applies To**
  - **/*.ts
  - **/*.js

## Login Without Session Regeneration

### **Id**
auth-no-session-regenerate
### **Severity**
error
### **Type**
regex
### **Pattern**
  - session\.userId\s*=(?![\s\S]{0,50}regenerate)
  - session\.user\s*=(?![\s\S]{0,50}regenerate)
  - req\.session\..*=.*user(?![\s\S]{0,100}regenerate)
### **Message**
Setting session user without regenerating session ID. Vulnerable to session fixation.
### **Fix Action**
Call session.regenerate() before storing user in session
### **Applies To**
  - **/*.ts
  - **/*.js

## Insecure Session Cookie

### **Id**
auth-insecure-cookie
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - cookie.*httpOnly.*false
  - cookie.*secure.*false
  - cookie(?![\s\S]{0,100}httpOnly)
  - session\(\{(?![\s\S]{0,200}httpOnly)
### **Message**
Session cookie may be insecure. Set httpOnly, secure, and sameSite.
### **Fix Action**
Add cookie options: { httpOnly: true, secure: true, sameSite: 'lax' }
### **Applies To**
  - **/*.ts
  - **/*.js

## Session Without Expiry

### **Id**
auth-no-session-expiry
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - session\(\{(?![\s\S]{0,300}maxAge|expires)
### **Message**
Session without expiry. Sessions should have maximum lifetime.
### **Fix Action**
Add maxAge to session config: maxAge: 24 * 60 * 60 * 1000
### **Applies To**
  - **/*.ts
  - **/*.js

## Long-Lived Access Token

### **Id**
auth-long-access-token
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - expiresIn.*['"][0-9]+d
  - expiresIn.*['"][0-9]+h(?!.*1[0-5]?h)
  - expiresIn.*3600000
### **Message**
Access token expiry seems too long. Keep access tokens short (5-15 minutes).
### **Fix Action**
Use expiresIn: '15m' for access tokens, use refresh tokens for longer sessions
### **Applies To**
  - **/*.ts
  - **/*.js

## Refresh Token Without Rotation

### **Id**
auth-no-refresh-rotation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - refreshToken(?![\s\S]{0,500}rotate|revoke|delete|update)
### **Message**
Refresh tokens should be rotated on use. One-time use prevents theft.
### **Fix Action**
Invalidate old refresh token and issue new one on each refresh
### **Applies To**
  - **/*.ts
  - **/*.js

## Weak Password Requirements

### **Id**
auth-weak-password-policy
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - password\.length.*[<>=]+.*[1-7]\b
  - minLength.*[1-7]\b
  - min.*password.*[1-7]
### **Message**
Password minimum length too short. Require at least 12 characters.
### **Fix Action**
Increase minimum password length to 12+ characters
### **Applies To**
  - **/*.ts
  - **/*.js

## No Password Strength Validation

### **Id**
auth-password-no-strength-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - password.*length(?![\s\S]{0,200}strength|zxcvbn|complexity)
### **Message**
Password validation checks only length. Consider using zxcvbn for strength.
### **Fix Action**
Add password strength check: const result = zxcvbn(password)
### **Applies To**
  - **/*.ts
  - **/*.js

## Possible Timing Attack

### **Id**
auth-timing-attack
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - if.*!user.*return|throw
  - user.*null.*throw
  - user not found
### **Message**
Early return when user not found may leak user existence via timing.
### **Fix Action**
Always perform password hash comparison even when user not found
### **Applies To**
  - **/*.ts
  - **/*.js

## Specific Authentication Error Message

### **Id**
auth-specific-error
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ['"]user.*not.*found['"]
  - ['"]invalid.*password['"]
  - ['"]wrong.*password['"]
  - ['"]email.*not.*registered['"]
### **Message**
Specific auth errors leak information. Use generic 'Invalid credentials'.
### **Fix Action**
Return generic error: 'Invalid email or password'
### **Applies To**
  - **/*.ts
  - **/*.js

## No Multi-Factor Authentication

### **Id**
auth-no-mfa
### **Severity**
info
### **Type**
regex
### **Pattern**
  - login(?![\s\S]{0,500}mfa|totp|2fa|twoFactor)
### **Message**
No MFA implementation detected. Consider adding TOTP for sensitive apps.
### **Fix Action**
Implement TOTP-based MFA using otplib
### **Applies To**
  - **/auth/**/*.ts
  - **/auth/**/*.js

## No Auth Event Logging

### **Id**
auth-no-audit-log
### **Severity**
info
### **Type**
regex
### **Pattern**
  - login(?![\s\S]{0,200}log|audit|track)
### **Message**
Authentication events not logged. Consider audit logging for security.
### **Fix Action**
Log login attempts, failures, password changes, and MFA events
### **Applies To**
  - **/auth/**/*.ts
  - **/auth/**/*.js

## Password in Log Statement

### **Id**
auth-password-in-log
### **Severity**
error
### **Type**
regex
### **Pattern**
  - console\.log.*password
  - logger\..*password
  - log\(.*password
### **Message**
Password may be logged. Never log passwords or credentials.
### **Fix Action**
Remove password from log statement
### **Applies To**
  - **/*.ts
  - **/*.js