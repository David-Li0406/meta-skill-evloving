# API Authentication & Authorization

**Category**: api-security/auth
**Description**: Detection patterns for API authentication and authorization vulnerabilities
**CWE**: CWE-306, CWE-639, CWE-287, CWE-798, CWE-384, CWE-942, CWE-285, CWE-598

---

## OWASP API Security Top 10

- **API1:2023** - Broken Object Level Authorization (BOLA)
- **API2:2023** - Broken Authentication
- **API5:2023** - Broken Function Level Authorization

---

## Missing Authentication Middleware

### Express Routes Without Auth
**Pattern**: `app\.(get|post|put|delete|patch)\s*\(\s*['"][^'"]+['"]\s*,\s*(?!.*(?:auth|authenticate|isAuthenticated|requireAuth|verifyToken|passport|jwt|session)).*\(\s*req\s*,\s*res`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Express.js routes without authentication middleware
- CWE-306: Missing Authentication

### FastAPI Without Dependencies
**Pattern**: `@app\.(get|post|put|delete|patch)\s*\([^)]*\)\s*\n(?:async\s+)?def\s+\w+\s*\([^)]*\)(?!.*Depends)`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- FastAPI endpoints without security dependencies
- CWE-306: Missing Authentication

### Flask Without Login Required
**Pattern**: `@app\.route\s*\([^)]+\)\s*\ndef\s+\w+\s*\((?!.*login_required|auth_required)`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Flask routes without login_required decorator
- CWE-306: Missing Authentication

---

## Broken Object Level Authorization (BOLA)

### Direct Object Reference
**Pattern**: `\.(findById|findOne|findByPk|get)\s*\(\s*(req\.params\.|req\.query\.|request\.args)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript, python]
- Direct object reference without ownership check
- CWE-639: IDOR / BOLA

### User ID From Request
**Pattern**: `(user_id|userId|user\.id)\s*=\s*(req\.params|req\.query|request\.args|request\.form)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript, python]
- User ID from request used directly in query
- CWE-639: IDOR / BOLA

---

## JWT Validation Issues

### JWT Decode Without Verify
**Pattern**: `jwt\.decode\s*\([^)]*verify\s*=\s*False`
**Type**: regex
**Severity**: high
**Languages**: [python]
- JWT decode without verification
- CWE-287: Improper Authentication

### JWT Without Algorithm
**Pattern**: `jwt\.(sign|verify)\s*\([^)]*\)(?!.*algorithm)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- JWT without algorithm specification
- CWE-287: Improper Authentication

### JWT None Algorithm
**Pattern**: `algorithms?\s*[=:]\s*\[.*['"]none['"]`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript, python]
- Accepting 'none' algorithm
- CWE-287: Improper Authentication

---

## Hardcoded Secrets

### Hardcoded JWT Secret
**Pattern**: `(jwt_secret|JWT_SECRET|secret_key|SECRET_KEY)\s*[=:]\s*['"][^'"]{8,}['"]`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript, python]
- JWT secret hardcoded in source code
- CWE-798: Hardcoded Credentials

---

## Session Security

### Session Not Regenerated
**Pattern**: `(login|authenticate|signin).*\{[^}]*(?!regenerate|destroy|create).*session`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Session not regenerated after login
- CWE-384: Session Fixation

---

## CORS Issues

### CORS Credentials With Wildcard
**Pattern**: `(credentials|withCredentials)\s*[=:]\s*true.*origin\s*[=:]\s*['"]\*['"]`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript, python]
- CORS with credentials but wildcard origin
- CWE-942: Overly Permissive Cross-domain Whitelist

---

## Function Level Authorization

### Admin Endpoints Without Role Check
**Pattern**: `(\/admin|\/manage|\/internal|\/system).*(?!role|permission|isAdmin|authorize)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript, python]
- Admin endpoints without role check
- CWE-285: Improper Authorization

---

## API Key Security

### API Key In Query String
**Pattern**: `(api_key|apikey|api-key|access_token)\s*=\s*(req\.query|request\.args|params\[)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript, python]
- API key passed in query string (logged in URLs)
- CWE-598: Use of GET Request Method With Sensitive Query Strings

---

## Detection Confidence

**Regex Detection**: 90%
**Security Pattern Detection**: 85%

---

## References

- [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [CWE-306: Missing Authentication](https://cwe.mitre.org/data/definitions/306.html)
- [CWE-639: Insecure Direct Object Reference](https://cwe.mitre.org/data/definitions/639.html)
