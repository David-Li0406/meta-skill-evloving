# Security Hardening - Validations

## Hardcoded Secret in Code

### **Id**
sec-hardcoded-secret
### **Severity**
error
### **Type**
regex
### **Pattern**
  - password\s*[=:]\s*['"][^$\{][^'"]{4,}['"]
  - api_key\s*[=:]\s*['"][^$\{][^'"]{8,}['"]
  - secret\s*[=:]\s*['"][^$\{][^'"]{8,}['"]
  - token\s*[=:]\s*['"][^$\{][^'"]{8,}['"]
  - AWS_SECRET_ACCESS_KEY\s*[=:]\s*["'][A-Za-z0-9/+=]{20,}
  - PRIVATE_KEY\s*[=:]\s*["'][A-Za-z0-9/+=]{20,}
### **Message**
Hardcoded secret detected. Will be visible in version control.
### **Fix Action**
Move to environment variable and use process.env
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.py
  - **/*.go

## SQL with Template Literal

### **Id**
sec-sql-template-literal
### **Severity**
error
### **Type**
regex
### **Pattern**
  - `SELECT.*\\$\\{
  - `INSERT.*\\$\\{
  - `UPDATE.*\\$\\{
  - `DELETE.*\\$\\{
  - "SELECT.*" \\+ 
  - "INSERT.*" \\+ 
  - "UPDATE.*" \\+ 
  - f"SELECT.*\\{
  - f'SELECT.*\{
### **Message**
SQL query using string interpolation. Potential SQL injection vulnerability.
### **Fix Action**
Use parameterized queries ($1, ?, etc.) instead of string interpolation
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.py

## Eval Function Usage

### **Id**
sec-eval-usage
### **Severity**
error
### **Type**
regex
### **Pattern**
  - eval\s*\(
  - new\s+Function\s*\(
  - setTimeout\s*\(\s*["']
  - setInterval\s*\(\s*["']
  - exec\s*\(\s*[`"'].*\\$
### **Message**
eval() or similar dynamic code execution detected. High risk of code injection.
### **Fix Action**
Replace with safe alternatives (JSON.parse, mathjs, explicit logic)
### **Applies To**
  - **/*.ts
  - **/*.js

## Dangerous HTML Insertion

### **Id**
sec-dangerous-html
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \\.innerHTML\\s*=
  - dangerouslySetInnerHTML
  - v-html\\s*=
  - \\.outerHTML\\s*=
  - document\\.write
### **Message**
Direct HTML insertion may cause XSS vulnerability.
### **Fix Action**
Use textContent, sanitize with DOMPurify, or use framework's safe methods
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx
  - **/*.vue

## Weak Password Hashing

### **Id**
sec-weak-password-hash
### **Severity**
error
### **Type**
regex
### **Pattern**
  - createHash\s*\(\s*['"]md5['"]\)
  - createHash\s*\(\s*['"]sha1['"]\)
  - createHash\s*\(\s*['"]sha256['"]\).*password
  - hashlib\\.md5\\(
  - hashlib\\.sha1\\(
  - hashlib\\.sha256\\(.*password
### **Message**
Using weak or fast hash for passwords. Use bcrypt or argon2 instead.
### **Fix Action**
Replace with bcrypt.hash() or argon2.hash() for password hashing
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.py

## CORS Wildcard with Credentials

### **Id**
sec-cors-wildcard
### **Severity**
error
### **Type**
regex
### **Pattern**
  - origin:\s*['"]\*['"].*credentials:\s*true
  - credentials:\s*true.*origin:\s*['"]\*['"]
  - Access-Control-Allow-Origin.*\*.*credentials
### **Message**
CORS wildcard with credentials allows any site to steal user data.
### **Fix Action**
Specify exact allowed origins instead of wildcard when using credentials
### **Applies To**
  - **/*.ts
  - **/*.js

## JWT with Weak Secret

### **Id**
sec-jwt-weak-secret
### **Severity**
error
### **Type**
regex
### **Pattern**
  - jwt\.sign.*['"][a-zA-Z0-9]{1,20}['"]
  - JWT_SECRET.*\|\|.*['"]
  - secret.*['"]password['"]
  - secret.*['"]secret['"]
### **Message**
JWT signed with weak or hardcoded secret.
### **Fix Action**
Use a strong (32+ char) secret from environment variable
### **Applies To**
  - **/*.ts
  - **/*.js

## Console Logging Sensitive Data

### **Id**
sec-console-sensitive
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - console\\.log.*password
  - console\\.log.*token
  - console\\.log.*secret
  - console\\.log.*apiKey
  - console\\.log.*credentials
  - print\\(.*password
### **Message**
Potentially logging sensitive data. Remove before production.
### **Fix Action**
Remove console.log with sensitive data or redact values
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.py

## Form Without CSRF Protection

### **Id**
sec-no-csrf-protection
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <form.*method=["']post["'](?![^>]*csrf)
  - <form.*method=["']POST["'](?![^>]*csrf)
### **Message**
Form POST without CSRF token. Vulnerable to cross-site request forgery.
### **Fix Action**
Add CSRF token to form or use SameSite cookies
### **Applies To**
  - **/*.html
  - **/*.jsx
  - **/*.tsx
  - **/*.vue

## HTTP URL in Security Context

### **Id**
sec-http-not-https
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - http://(?!localhost|127\\.0\\.0\\.1)
  - fetch\s*\(['"]http://
  - axios\s*\.[a-z]+\s*\(['"]http://
### **Message**
Using HTTP instead of HTTPS. Data transmitted in plain text.
### **Fix Action**
Use HTTPS for all external URLs
### **Applies To**
  - **/*.ts
  - **/*.js

## Mass Assignment Vulnerability

### **Id**
sec-mass-assignment
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - data:\\s*\\{\\s*\\.\\.\\.req\\.body
  - update\\(.*\\.\\.\\.req\\.body
  - create\\(.*\\.\\.\\.req\\.body
  - Object\\.assign.*req\\.body
### **Message**
Spreading request body directly into database operation. Mass assignment risk.
### **Fix Action**
Explicitly whitelist allowed fields or use Zod schema validation
### **Applies To**
  - **/*.ts
  - **/*.js

## Path Traversal Vulnerability

### **Id**
sec-path-traversal
### **Severity**
error
### **Type**
regex
### **Pattern**
  - readFile.*\\$\\{.*\\}
  - readFileSync.*\\$\\{.*\\}
  - path\\.join.*req\\.
  - fs\\..*\\(.*req\\.
  - open\\(.*req\\.
### **Message**
User input used in file path. Path traversal vulnerability risk.
### **Fix Action**
Validate and sanitize paths, use path.basename(), check for ..
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.py

## Command Injection

### **Id**
sec-command-injection
### **Severity**
error
### **Type**
regex
### **Pattern**
  - exec\\s*\\(.*\\$\\{.*\\}
  - execSync.*\\$\\{.*\\}
  - spawn.*\\$\\{.*\\}
  - child_process.*\\$\\{
  - subprocess\\..*\\(.*f"
  - os\\.system\\(
### **Message**
User input in shell command. Command injection vulnerability.
### **Fix Action**
Use spawn with array args, sanitize input, or avoid shell commands
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.py

## Insecure Cookie Settings

### **Id**
sec-insecure-cookie
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - cookie.*secure:\\s*false
  - cookie.*httpOnly:\\s*false
  - set-cookie(?!.*Secure)(?!.*HttpOnly)
### **Message**
Cookie missing secure flags. May be vulnerable to theft.
### **Fix Action**
Set secure: true, httpOnly: true, sameSite: 'strict'
### **Applies To**
  - **/*.ts
  - **/*.js

## Open Redirect Vulnerability

### **Id**
sec-open-redirect
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - redirect\\(.*req\\.
  - location\\s*=.*req\\.
  - window\\.location.*\\$\\{
  - res\\.redirect\\(.*query\\.
### **Message**
Redirect URL from user input. Open redirect vulnerability.
### **Fix Action**
Validate redirect URL against allowlist of domains
### **Applies To**
  - **/*.ts
  - **/*.js

## Debug Mode in Production Code

### **Id**
sec-debug-enabled
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - DEBUG\\s*=\\s*True
  - DEBUG\\s*=\\s*true
  - app\.debug\s*=\s*True
  - FLASK_DEBUG\s*=\s*1
### **Message**
Debug mode may be enabled. Exposes sensitive information.
### **Fix Action**
Ensure debug mode is disabled in production configuration
### **Applies To**
  - **/*.py
  - **/*.js
  - **/*.ts

## Authentication Without Rate Limiting

### **Id**
sec-no-rate-limit
### **Severity**
info
### **Type**
regex
### **Pattern**
  - login(?!.*rateLimit|Limit|throttle)
  - authenticate(?!.*rateLimit|Limit|throttle)
  - /auth/(?!.*rateLimit|Limit|throttle)
### **Message**
Authentication endpoint may lack rate limiting. Brute force risk.
### **Fix Action**
Add rate limiting middleware to authentication endpoints
### **Applies To**
  - **/*.ts
  - **/*.js

## Resource Access Without Authorization

### **Id**
sec-no-authorization-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - findUnique.*id.*params(?!.*userId|ownerId|user)
  - findFirst.*id.*params(?!.*userId|ownerId|user)
  - deleteOne.*id.*params(?!.*userId|ownerId|user)
### **Message**
Resource fetched by ID without ownership check. IDOR vulnerability risk.
### **Fix Action**
Add user ownership filter to query (where: { userId: req.user.id })
### **Applies To**
  - **/*.ts
  - **/*.js

## Weak Random Number Generation

### **Id**
sec-weak-random
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - Math\\.random\\(\\).*token
  - Math\\.random\\(\\).*secret
  - Math\\.random\\(\\).*password
  - Math\\.random\\(\\).*id
### **Message**
Math.random() is not cryptographically secure for tokens/secrets.
### **Fix Action**
Use crypto.randomBytes() or crypto.randomUUID()
### **Applies To**
  - **/*.ts
  - **/*.js

## Sensitive Data in URL Parameter

### **Id**
sec-sensitive-url-param
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \\?.*password=
  - \\?.*token=
  - \\?.*api_key=
  - \\?.*secret=
  - query\\.password
  - query\\.token
### **Message**
Sensitive data in URL query parameter. Visible in logs and history.
### **Fix Action**
Use POST body or headers for sensitive data instead of URL parameters
### **Applies To**
  - **/*.ts
  - **/*.js

## XML Parser Without Protection

### **Id**
sec-xxe-vulnerability
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - parseXML(?!.*disableEntities)
  - xml2js(?!.*explicitCharkey)
  - DOMParser.*parseFromString(?!.*text/html)
  - etree\\.parse\\(
### **Message**
XML parser may be vulnerable to XXE attacks.
### **Fix Action**
Disable external entities and DTD processing in XML parser
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.py