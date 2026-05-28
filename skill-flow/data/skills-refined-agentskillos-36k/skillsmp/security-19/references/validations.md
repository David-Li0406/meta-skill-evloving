# Security - Validations

## SQL injection via template literal

### **Id**
sql-injection-template-literal
### **Severity**
critical
### **Type**
regex
### **Pattern**
(SELECT|INSERT|UPDATE|DELETE|FROM|WHERE).*\$\{
### **Message**
Potential SQL injection - use parameterized queries instead of template literals
### **Fix Action**
Use parameterized queries: db.query('SELECT * FROM x WHERE id = $1', [id])
### **Applies To**
  - **/*.ts
  - **/*.js

## dangerouslySetInnerHTML usage

### **Id**
dangerous-innerhtml
### **Severity**
critical
### **Type**
regex
### **Pattern**
dangerouslySetInnerHTML
### **Message**
dangerouslySetInnerHTML can lead to XSS - ensure input is sanitized with DOMPurify
### **Fix Action**
Use DOMPurify.sanitize() on the HTML content
### **Applies To**
  - **/*.tsx
  - **/*.jsx

## Eval function usage

### **Id**
eval-usage
### **Severity**
critical
### **Type**
regex
### **Pattern**
\beval\s*\(
### **Message**
eval() executes arbitrary code - this is almost always a security vulnerability
### **Fix Action**
Refactor to avoid eval - use JSON.parse for data, proper functions for logic
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Hardcoded API keys or secrets

### **Id**
hardcoded-secrets
### **Severity**
critical
### **Type**
regex
### **Pattern**
(api_key|apikey|secret|password|token|auth)\s*[=:]\s*['"][^'"]{16,}['"]
### **Message**
Potential hardcoded secret detected - use environment variables
### **Fix Action**
Move to process.env.SECRET_NAME
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Stripe keys in code

### **Id**
stripe-keys-hardcoded
### **Severity**
critical
### **Type**
regex
### **Pattern**
sk_live_[a-zA-Z0-9]+|sk_test_[a-zA-Z0-9]+
### **Message**
Stripe secret key in code - use environment variables
### **Fix Action**
Use process.env.STRIPE_SECRET_KEY
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Mass assignment vulnerability

### **Id**
mass-assignment
### **Severity**
error
### **Type**
regex
### **Pattern**
\.update\([^)]*data:\s*req\.body|\.create\([^)]*data:\s*req\.body
### **Message**
Mass assignment vulnerability - explicitly whitelist allowed fields
### **Fix Action**
Destructure only allowed fields: const { name, email } = req.body
### **Applies To**
  - **/*.ts
  - **/*.js

## Path traversal vulnerability

### **Id**
path-traversal
### **Severity**
critical
### **Type**
regex
### **Pattern**
path\.(join|resolve).*req\.(query|body|params)
### **Message**
Potential path traversal - use path.basename() to sanitize input
### **Fix Action**
Use path.basename() to strip directory traversal
### **Applies To**
  - **/*.ts
  - **/*.js

## JWT verification without algorithm

### **Id**
jwt-no-algorithm
### **Severity**
critical
### **Type**
regex
### **Pattern**
jwt\.verify\s*\([^)]+\)(?!.*algorithms)
### **Message**
JWT verification should specify allowed algorithms
### **Fix Action**
Add { algorithms: ['HS256'] } or appropriate algorithm
### **Applies To**
  - **/*.ts
  - **/*.js

## Cookie without HttpOnly

### **Id**
cookie-no-httponly
### **Severity**
error
### **Type**
regex
### **Pattern**
Set-Cookie.*(?!.*HttpOnly)
### **Message**
Session cookies should have HttpOnly flag
### **Fix Action**
Add HttpOnly to cookie flags
### **Applies To**
  - **/*.ts
  - **/*.js

## Console logging potentially sensitive data

### **Id**
console-log-sensitive
### **Severity**
warning
### **Type**
regex
### **Pattern**
console\.log\s*\([^)]*(?:password|token|secret|key|auth|bearer)[^)]*\)
### **Message**
Avoid logging sensitive data - it may appear in logs
### **Fix Action**
Remove sensitive data from console.log or redact it
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## CORS allowing all origins

### **Id**
cors-star
### **Severity**
warning
### **Type**
regex
### **Pattern**
origin:\s*['"]\*['"]|Access-Control-Allow-Origin.*\*
### **Message**
CORS * allows any origin - consider restricting to specific domains
### **Fix Action**
Specify allowed origins explicitly
### **Applies To**
  - **/*.ts
  - **/*.js

## Shell command execution

### **Id**
exec-child-process
### **Severity**
error
### **Type**
regex
### **Pattern**
exec\s*\(|execSync\s*\(|spawn\s*\(
### **Message**
Shell command execution detected - ensure input is sanitized
### **Fix Action**
Avoid user input in shell commands or use proper escaping
### **Applies To**
  - **/*.ts
  - **/*.js