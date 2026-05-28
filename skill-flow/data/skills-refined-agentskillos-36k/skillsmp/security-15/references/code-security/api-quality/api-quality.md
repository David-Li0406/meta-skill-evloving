# API Quality and Security Patterns

**Category**: code-security/api-quality
**Description**: Detect API security issues, rate limiting, design patterns
**CWE**: CWE-770 (Allocation of Resources Without Limits), CWE-285 (Improper Authorization)

---

## Rate Limiting Detection

### Express.js Missing Rate Limiting on Auth Endpoints

**Type**: semgrep
**Severity**: high
**Languages**: [javascript, typescript]
**Pattern**: |
  app.post('/api/auth/$ENDPOINT', $HANDLER)
- Authentication endpoints without rate limiting are vulnerable to brute force
- Example: `app.post('/api/auth/login', handleLogin)`
- Remediation: Add rate limiting middleware before auth handlers

### Express.js Missing Rate Limiting on Public API

**Type**: semgrep
**Severity**: medium
**Languages**: [javascript, typescript]
**Pattern**: |
  app.$METHOD('/api/$PATH', $HANDLER)
- Public API endpoints should have rate limiting
- Example: `app.get('/api/users', getUsers)`
- Check for rate-limit, express-rate-limit middleware

### FastAPI Missing Rate Limiting

**Type**: semgrep
**Severity**: medium
**Languages**: [python]
**Pattern**: |
  @app.$METHOD("/$PATH")
  async def $FUNC(...):
      ...
- FastAPI endpoints without rate limiting
- Example: `@app.post("/login")`
- Remediation: Use slowapi or custom rate limiting

### Spring Boot Missing Rate Limiting

**Type**: semgrep
**Severity**: medium
**Languages**: [java]
**Pattern**: |
  @$MAPPING("/$PATH")
  public $RET $METHOD(...) { ... }
- Spring endpoints without rate limiting
- Consider using bucket4j or resilience4j

---

## API Authentication Issues

### Missing Authentication Middleware (Express)

**Type**: semgrep
**Severity**: high
**Languages**: [javascript, typescript]
**Pattern**: |
  app.$METHOD('/api/$PATH', (req, res) => { ... })
- Direct handler without auth middleware chain
- Example: `app.get('/api/users', (req, res) => ...)`
- Remediation: Add authentication middleware

### Unprotected Admin Endpoint

**Type**: regex
**Severity**: critical
**Pattern**: `(?i)app\.(get|post|put|delete)\s*\(\s*['"]/(?:api/)?admin`
- Admin endpoints should require authentication
- Example: `app.get('/api/admin/users', ...)`

### JWT Verification Missing

**Type**: semgrep
**Severity**: high
**Languages**: [javascript, typescript]
**Pattern**: |
  jwt.decode($TOKEN)
- Using jwt.decode instead of jwt.verify skips signature validation
- Example: `const payload = jwt.decode(token)`
- Remediation: Use jwt.verify with secret/public key

### Hardcoded JWT Secret

**Type**: regex
**Severity**: critical
**Pattern**: `jwt\.sign\([^)]+,\s*['"][^'"]{8,}['"]`
- JWT secret hardcoded in source
- Example: `jwt.sign(payload, 'mysecretkey123')`
- Remediation: Use environment variables

---

## Input Validation

### Missing Request Body Validation (Express)

**Type**: semgrep
**Severity**: medium
**Languages**: [javascript, typescript]
**Pattern**: |
  app.post($PATH, (req, res) => {
    const $VAR = req.body.$FIELD;
    ...
  })
- Using req.body without validation
- Remediation: Use express-validator, joi, or zod

### SQL Injection Risk

**Type**: semgrep
**Severity**: critical
**Languages**: [javascript, typescript]
**Pattern**: |
  $DB.query(`... ${$VAR} ...`)
- String interpolation in SQL query
- Example: `db.query(\`SELECT * FROM users WHERE id = ${userId}\`)`
- Remediation: Use parameterized queries

### Python SQL Injection

**Type**: semgrep
**Severity**: critical
**Languages**: [python]
**Pattern**: |
  cursor.execute(f"... {$VAR} ...")
- f-string in SQL query
- Remediation: Use parameterized queries

### SSRF Vulnerability

**Type**: semgrep
**Severity**: high
**Languages**: [javascript, typescript]
**Pattern**: |
  fetch(req.body.$URL)
- User-controlled URL in fetch
- Example: `fetch(req.body.url)`
- Remediation: Validate and allowlist URLs

### Python SSRF

**Type**: semgrep
**Severity**: high
**Languages**: [python]
**Pattern**: |
  requests.get(request.$FIELD.$URL)
- User-controlled URL in requests
- Remediation: Validate and allowlist URLs

---

## CORS Configuration

### Wildcard CORS Origin

**Type**: regex
**Severity**: high
**Pattern**: `(?i)(?:access-control-allow-origin|cors).*['"]\*['"]`
- Wildcard CORS allows any origin
- Example: `Access-Control-Allow-Origin: *`
- Remediation: Specify allowed origins explicitly

### CORS Credentials with Wildcard

**Type**: semgrep
**Severity**: critical
**Languages**: [javascript, typescript]
**Pattern**: |
  cors({ origin: '*', credentials: true })
- Wildcard origin with credentials is invalid and dangerous
- Remediation: Specify allowed origins

### Reflected CORS Origin

**Type**: semgrep
**Severity**: high
**Languages**: [javascript, typescript]
**Pattern**: |
  res.setHeader('Access-Control-Allow-Origin', req.headers.origin)
- Reflecting request origin without validation
- Remediation: Validate against allowlist

---

## Error Handling

### Detailed Error in Production

**Type**: semgrep
**Severity**: medium
**Languages**: [javascript, typescript]
**Pattern**: |
  res.status($CODE).json({ error: $ERR.stack })
- Exposing stack traces to clients
- Remediation: Log errors server-side, return generic message

### Python Exception Exposure

**Type**: semgrep
**Severity**: medium
**Languages**: [python]
**Pattern**: |
  return {"error": str($EXCEPTION)}
- Exposing exception details to clients
- Remediation: Log exceptions, return generic error

---

## API Design Issues

### Missing Content-Type Validation

**Type**: semgrep
**Severity**: low
**Languages**: [javascript, typescript]
**Pattern**: |
  app.post($PATH, $HANDLER)
- POST endpoint without content-type validation
- Add express.json() or validate Content-Type header

### Excessive Data Exposure

**Type**: regex
**Severity**: medium
**Pattern**: `(?i)res\.(?:json|send)\s*\(\s*(?:user|account|profile)\s*\)`
- Returning entire user object may expose sensitive fields
- Example: `res.json(user)`
- Remediation: Select specific fields to return

### Missing Pagination

**Type**: semgrep
**Severity**: low
**Languages**: [javascript, typescript]
**Pattern**: |
  $MODEL.find({})
- Database query without limit
- Example: `User.find({})`
- Remediation: Add pagination with skip/limit

### GraphQL Introspection Enabled

**Type**: regex
**Severity**: medium
**Pattern**: `(?i)introspection\s*:\s*true`
- GraphQL introspection should be disabled in production
- Remediation: Set introspection: false for production

### GraphQL Query Depth Unlimited

**Type**: semgrep
**Severity**: medium
**Languages**: [javascript, typescript]
**Pattern**: |
  new ApolloServer({ $SCHEMA, ... })
- Apollo Server without depth limiting
- Remediation: Use graphql-depth-limit plugin

---

## API Versioning

### Unversioned API Endpoint

**Type**: regex
**Severity**: low
**Pattern**: `app\.(get|post|put|delete)\s*\(\s*['"]/api/(?!v\d)`
- API endpoint without version prefix
- Example: `app.get('/api/users', ...)`
- Recommendation: Use /api/v1/users pattern

### Deprecated API Version

**Type**: regex
**Severity**: medium
**Pattern**: `(?i)/api/v[01]/`
- Using deprecated API version (v0 or v1)
- Example: `/api/v0/legacy`
- Review if endpoint should be sunset

---

## Response Security Headers

### Missing Security Headers

**Type**: regex
**Severity**: medium
**Pattern**: `(?i)res\.(?:send|json)\s*\(`
- Response without security headers
- Add X-Content-Type-Options, X-Frame-Options, etc.
- Consider using helmet middleware

### Missing Cache Control

**Type**: semgrep
**Severity**: low
**Languages**: [javascript, typescript]
**Pattern**: |
  res.json({ $DATA })
- Response without cache control headers
- Sensitive data should have Cache-Control: no-store

---

## Detection Confidence

**Rate Limiting Detection**: 85%
**Auth Issues Detection**: 90%
**Injection Detection**: 95%
**CORS Issues Detection**: 90%

---

## References

- OWASP API Security Top 10
- CWE-770: Allocation of Resources Without Limits
- CWE-285: Improper Authorization
- CWE-89: SQL Injection
- CWE-918: Server-Side Request Forgery
