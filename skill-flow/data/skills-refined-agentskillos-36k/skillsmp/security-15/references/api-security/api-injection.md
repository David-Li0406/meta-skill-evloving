# API Injection Vulnerabilities

**Category**: api-security/injection
**Description**: Detection patterns for injection vulnerabilities in API endpoints
**CWE**: CWE-89, CWE-78, CWE-90, CWE-643, CWE-113, CWE-117, CWE-1336, CWE-943

---

## OWASP API Security Top 10

- **API8:2023** - Security Misconfiguration (includes injection via misconfigured parsers)
- **API10:2023** - Unsafe Consumption of APIs

---

## SQL Injection in APIs

### SQL String Concatenation
**Pattern**: `(execute|query|raw)\s*\([^)]*(\+|\.format\(|%s|%d|\$\{).*req\.(body|params|query)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript, python]
- String concatenation in SQL with request params
- CWE-89: SQL Injection

### SQL Template Literals
**Pattern**: `(execute|query|raw)\s*\([^)]*\$\{.*req\.(body|params|query)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Template literals in SQL queries
- CWE-89: SQL Injection

### Python f-string SQL
**Pattern**: `(execute|cursor\.execute)\s*\(\s*f['"][^'"]*\{.*request\.(args|form|json)`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Python f-string in SQL queries
- CWE-89: SQL Injection

---

## NoSQL Injection

### MongoDB Query Injection
**Pattern**: `\.(find|findOne|findOneAndUpdate|updateOne|deleteOne)\s*\(\s*\{[^}]*req\.(body|params|query)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- MongoDB query with unsanitized input
- CWE-943: NoSQL Injection

### MongoDB $where Injection
**Pattern**: `\$where\s*[=:]\s*.*req\.(body|params|query)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- MongoDB $where with user input
- CWE-943: NoSQL Injection

### PyMongo Injection
**Pattern**: `(find|find_one|update_one|delete_one)\s*\(\s*\{.*request\.(args|form|json)`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- PyMongo with unsanitized user input
- CWE-943: NoSQL Injection

---

## Command Injection in APIs

### Shell Execution with Request Data
**Pattern**: `(exec|spawn|execSync|execFile|system|popen|subprocess)\s*\([^)]*req\.(body|params|query)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript, python]
- Shell execution with request data
- CWE-78: OS Command Injection

### Template Command Injection
**Pattern**: `\$\{.*req\.(body|params|query).*\}`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Template with user input in command
- CWE-78: OS Command Injection

---

## LDAP Injection

### LDAP Filter Injection
**Pattern**: `(search|bind)\s*\([^)]*(\+|\.format\(|%s|\$\{).*req\.(body|params|query)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript, python]
- LDAP filter with user input
- CWE-90: LDAP Injection

---

## XPath Injection

### XPath Query Injection
**Pattern**: `(xpath|evaluate|selectNodes)\s*\([^)]*(\+|\.format\(|\$\{).*req\.(body|params|query)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript, python]
- XPath query with concatenation
- CWE-643: XPath Injection

---

## Header Injection

### Response Header Injection
**Pattern**: `(setHeader|set|header)\s*\([^,]+,\s*req\.(body|params|query)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Response header with user input
- CWE-113: HTTP Response Splitting

---

## Log Injection

### Unsanitized Log Input
**Pattern**: `(logger\.|console\.|log\.)(info|warn|error|debug)\s*\([^)]*req\.(body|params|query)\.[^)]*\)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript, python]
- Unsanitized user input in logs
- CWE-117: Log Injection

---

## Template Injection (SSTI)

### Server-Side Template Injection
**Pattern**: `(render_template_string|Template|render_string)\s*\([^)]*req\.(body|params|query)`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Server-side template with user input
- CWE-1336: Server-Side Template Injection

### Jinja2 Autoescape Disabled
**Pattern**: `Environment\s*\([^)]*autoescape\s*=\s*False`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Jinja2 with autoescape disabled
- CWE-1336: Server-Side Template Injection

---

## GraphQL Injection

### GraphQL String Concatenation
**Pattern**: `(graphql|query)\s*[=:]\s*['\"].*\$\{.*req\.(body|params|query)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- GraphQL query string concatenation
- CWE-89: Injection

---

## ORM Injection

### Sequelize Literal Injection
**Pattern**: `Sequelize\.literal\s*\([^)]*req\.(body|params|query)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Sequelize literal with user input
- CWE-89: SQL Injection via ORM

### SQLAlchemy Text Injection
**Pattern**: `(text|literal_column)\s*\([^)]*request\.(args|form|json)`
**Type**: regex
**Severity**: high
**Languages**: [python]
- SQLAlchemy text with user input
- CWE-89: SQL Injection via ORM

---

## Detection Confidence

**Regex Detection**: 90%
**Security Pattern Detection**: 85%

---

## References

- [OWASP Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)
- [CWE-78: OS Command Injection](https://cwe.mitre.org/data/definitions/78.html)
