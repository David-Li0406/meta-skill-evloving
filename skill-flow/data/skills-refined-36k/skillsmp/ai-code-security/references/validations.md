# Ai Code Security - Validations

## SQL Injection in AI-Generated Code

### **Id**
ai-sql-injection
### **Severity**
critical
### **Type**
regex
### **Pattern**
(?:SELECT|INSERT|UPDATE|DELETE|WHERE)[^;]*(?:\+\s*(?:req|params|body|user|input)|\$\{[^}]*(?:req|params|body|user|input))
### **Message**
Potential SQL injection in AI-generated code. User input concatenated in query.
### **Fix Action**
Use parameterized queries: db.query('SELECT * FROM users WHERE id = $1', [userId])
### **Applies To**
  - *.ts
  - *.js
  - *.py

## XSS via innerHTML in AI Code

### **Id**
ai-xss-innerhtml
### **Severity**
high
### **Type**
regex
### **Pattern**
\.innerHTML\s*=\s*(?!.*(?:DOMPurify|sanitize|escape))[^;]+
### **Message**
Unsanitized innerHTML assignment. XSS vulnerability.
### **Fix Action**
Use textContent for text, or DOMPurify.sanitize() for HTML
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## dangerouslySetInnerHTML Without Sanitization

### **Id**
ai-dangerous-react
### **Severity**
high
### **Type**
regex
### **Pattern**
dangerouslySetInnerHTML\s*=\s*\{\s*\{\s*__html:\s*(?!.*DOMPurify)[^}]+
### **Message**
dangerouslySetInnerHTML without DOMPurify sanitization.
### **Fix Action**
Use DOMPurify.sanitize(): dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(content) }}
### **Applies To**
  - *.tsx
  - *.jsx

## eval() in AI-Generated Code

### **Id**
ai-eval-usage
### **Severity**
critical
### **Type**
regex
### **Pattern**
\beval\s*\([^)]+\)|new\s+Function\s*\(
### **Message**
eval() or Function() constructor detected. Never execute AI-generated code directly.
### **Fix Action**
Use a sandboxed execution environment like vm2 or WebContainers
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Hardcoded Secrets in AI Output

### **Id**
ai-hardcoded-secrets
### **Severity**
critical
### **Type**
regex
### **Pattern**
(?:api[_-]?key|secret|password|token)\s*[:=]\s*["'][A-Za-z0-9+/=_-]{20,}["']
### **Message**
Potential hardcoded secret in AI-generated code.
### **Fix Action**
Use environment variables: process.env.API_KEY
### **Applies To**
  - *.ts
  - *.js
  - *.py
  - *.yaml
  - *.json

## Command Injection in AI Code

### **Id**
ai-command-injection
### **Severity**
critical
### **Type**
regex
### **Pattern**
(?:exec|spawn|execSync|spawnSync)\s*\([^)]*(?:\+|`\$\{)[^)]*(?:req|params|body|user|input)
### **Message**
Command injection vulnerability. User input in shell command.
### **Fix Action**
Use spawn with array arguments, never concatenate user input
### **Applies To**
  - *.ts
  - *.js

## Path Traversal in AI Code

### **Id**
ai-path-traversal
### **Severity**
high
### **Type**
regex
### **Pattern**
(?:readFile|writeFile|unlink|readdir)\s*\([^)]*(?:\+|`\$\{)[^)]*(?:req|params|body|user|input)
### **Message**
Path traversal vulnerability. User input in file path.
### **Fix Action**
Use path.resolve() and validate path is within allowed directory
### **Applies To**
  - *.ts
  - *.js

## Insecure Random in Security Context

### **Id**
ai-insecure-random
### **Severity**
medium
### **Type**
regex
### **Pattern**
Math\.random\s*\(\)[^;]*(?:token|key|secret|password|session|auth)
### **Message**
Math.random() used in security context. Not cryptographically secure.
### **Fix Action**
Use crypto.randomBytes() or crypto.randomUUID()
### **Applies To**
  - *.ts
  - *.js

## Missing Input Validation

### **Id**
ai-no-input-validation
### **Severity**
medium
### **Type**
regex
### **Pattern**
req\.(?:body|params|query)\.[a-zA-Z]+(?!\s*\?\.|\.?(?:validate|parse|safeParse|check))
### **Negative Pattern**
zod|yup|joi|validator|sanitize
### **Message**
Request input used without apparent validation.
### **Fix Action**
Validate input with Zod, Yup, or similar before use
### **Applies To**
  - *.ts
  - *.js

## Broad File System Access

### **Id**
ai-excessive-permissions
### **Severity**
medium
### **Type**
regex
### **Pattern**
readdir\s*\(['"]\/['"]|glob\s*\(['"]\/\*\*
### **Message**
Reading from root directory or recursive glob. Potential excessive access.
### **Fix Action**
Restrict file operations to specific allowed directories
### **Applies To**
  - *.ts
  - *.js

## Unsafe Deserialization

### **Id**
ai-unsafe-deserialization
### **Severity**
high
### **Type**
regex
### **Pattern**
JSON\.parse\s*\([^)]*(?:req|body|input|user)
### **Negative Pattern**
try\s*\{|catch|safeParse|schema\.parse
### **Message**
JSON.parse without error handling or schema validation.
### **Fix Action**
Wrap in try-catch and validate against schema
### **Applies To**
  - *.ts
  - *.js

## CORS Wildcard Origin

### **Id**
ai-cors-wildcard
### **Severity**
medium
### **Type**
regex
### **Pattern**
cors\s*\(\s*\{[^}]*origin:\s*['"]?\*['"]?
### **Message**
CORS configured with wildcard origin. May expose API to any domain.
### **Fix Action**
Specify allowed origins explicitly: origin: ['https://yourdomain.com']
### **Applies To**
  - *.ts
  - *.js

## Missing Authentication Check

### **Id**
ai-missing-auth-check
### **Severity**
high
### **Type**
regex
### **Pattern**
app\.(?:get|post|put|delete|patch)\s*\([^,]+,\s*(?:async\s*)?\([^)]*\)\s*=>
### **Negative Pattern**
auth|authenticate|isAuthenticated|requireAuth|protect|verify
### **Message**
Route handler without apparent authentication middleware.
### **Fix Action**
Add authentication middleware: app.get('/api/data', authMiddleware, handler)
### **Applies To**
  - *.ts
  - *.js