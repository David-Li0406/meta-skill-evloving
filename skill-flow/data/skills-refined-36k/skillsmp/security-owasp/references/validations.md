# Security Owasp - Validations

## SQL string concatenation

### **Id**
sql-concatenation
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - query\s*\(\s*[`'"]*.*\$\{
  - query\s*\(\s*[`'"].*\+\s*
  - WHERE.*=.*['"]\s*\+\s*
  - exec\\s*\\(.*\\+.*\\)
### **Message**
Potential SQL injection - use parameterized queries
### **Fix Action**
Use prepared statements or ORM with parameter binding
### **Applies To**
  - *.js
  - *.ts

## Command injection risk

### **Id**
command-injection
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - exec\\s*\\(.*\\$\\{
  - execSync\\s*\\(.*\\$\\{
  - spawn\\s*\\([^,]+\\+|spawn\\s*\\([^,]+\\$\\{
  - eval\\s*\\(
### **Message**
Potential command injection - avoid user input in commands
### **Fix Action**
Use execFile with array args, or validate/escape input strictly
### **Applies To**
  - *.js
  - *.ts

## Hardcoded secret or API key

### **Id**
hardcoded-secret
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - api[_-]?key\s*[=:]\s*['"][a-zA-Z0-9]{20,}
  - secret\s*[=:]\s*['"][a-zA-Z0-9]{20,}
  - password\s*[=:]\s*['"][^'"]{8,}
  - sk_live_[a-zA-Z0-9]+
  - ghp_[a-zA-Z0-9]+
  - AKIA[A-Z0-9]{16}
### **Message**
Hardcoded secret detected
### **Fix Action**
Use environment variables or secrets manager
### **Applies To**
  - *.js
  - *.ts
  - *.jsx
  - *.tsx
  - *.py

## JWT verify without algorithm check

### **Id**
jwt-no-algorithm
### **Severity**
high
### **Type**
regex
### **Pattern**
  - jwt\\.verify\\s*\\([^,]+,\\s*[^,]+\\s*\\)(?!.*algorithms)
  - verify\\s*\\([^)]*\\)(?!.*algorithm)
### **Message**
JWT verification should specify allowed algorithms
### **Fix Action**
Add algorithms option: { algorithms: ['HS256'] }
### **Applies To**
  - *.js
  - *.ts

## Weak password hashing

### **Id**
weak-password-hash
### **Severity**
high
### **Type**
regex
### **Pattern**
  - createHash\s*\(['"]md5['"]\)
  - createHash\s*\(['"]sha1['"]\)
  - hashSync\\s*\\([^,]+,\\s*[0-5]\\s*\\)
### **Message**
Use strong password hashing (Argon2 or bcrypt with high rounds)
### **Fix Action**
Use Argon2id or bcrypt with cost factor >= 10
### **Applies To**
  - *.js
  - *.ts

## Dangerous HTML insertion

### **Id**
dangerous-html
### **Severity**
high
### **Type**
regex
### **Pattern**
  - dangerouslySetInnerHTML.*\\{\\s*__html:(?!.*sanitize|.*DOMPurify)
  - \\.innerHTML\\s*=
  - document\\.write\\s*\\(
### **Message**
Direct HTML insertion can cause XSS
### **Fix Action**
Use DOMPurify.sanitize() or avoid innerHTML
### **Applies To**
  - *.js
  - *.ts
  - *.jsx
  - *.tsx

## State-changing endpoint without CSRF protection

### **Id**
missing-csrf
### **Severity**
medium
### **Type**
regex
### **Pattern**
  - app\\.(post|put|patch|delete)\\s*\\([^)]+(?!csrf|token)
### **Message**
Consider CSRF protection for state-changing endpoints
### **Fix Action**
Use SameSite cookies or CSRF tokens
### **Applies To**
  - *.js
  - *.ts

## Cookie without security flags

### **Id**
insecure-cookie
### **Severity**
medium
### **Type**
regex
### **Pattern**
  - cookie\\s*\\([^)]+(?!httpOnly|secure|sameSite)
  - setCookie\\s*\\([^)]+(?!httpOnly)
### **Message**
Cookies should have security flags
### **Fix Action**
Add httpOnly, secure, and sameSite flags
### **Applies To**
  - *.js
  - *.ts

## User input in file path

### **Id**
path-traversal
### **Severity**
high
### **Type**
regex
### **Pattern**
  - readFile.*req\\.(params|query|body)
  - readFileSync.*req\\.
  - path\\.join.*req\\.
  - sendFile.*req\\.(params|query)
### **Message**
User input in file paths can lead to path traversal
### **Fix Action**
Use path.basename() and verify resolved path is in allowed directory
### **Applies To**
  - *.js
  - *.ts

## Spreading request body into database

### **Id**
mass-assignment
### **Severity**
high
### **Type**
regex
### **Pattern**
  - \\.create\\s*\\(\\s*\\{[^}]*\\.\\.\\.req\\.body
  - \\.update\\s*\\(\\s*\\{[^}]*\\.\\.\\.req\\.body
  - data:\\s*req\\.body(?!\\[)
### **Message**
Mass assignment vulnerability - explicitly pick allowed fields
### **Fix Action**
Destructure only allowed fields or use validation schema
### **Applies To**
  - *.js
  - *.ts

## Non-constant-time secret comparison

### **Id**
timing-attack
### **Severity**
medium
### **Type**
regex
### **Pattern**
  - (password|secret|token|key|hash)\\s*===\\s*(password|secret|token|key|hash|req\\.|input|user)
### **Message**
Use timing-safe comparison for secrets
### **Fix Action**
Use crypto.timingSafeEqual() or library comparison functions
### **Applies To**
  - *.js
  - *.ts