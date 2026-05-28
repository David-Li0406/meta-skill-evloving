# API Quality Patterns

**Category**: code-quality/api
**Description**: API design, performance, observability, and rate limiting patterns
**CWE**: CWE-400 (Uncontrolled Resource Consumption), CWE-770 (Allocation of Resources Without Limits)

---

## API Design Patterns

### Non-RESTful Route Naming
**Type**: regex
**Severity**: info
**Pattern**: `\.(get|post)\s*\(\s*['"]/(get|fetch|retrieve|find)[A-Z]`
- Route uses verb in path (getUsers) instead of RESTful noun (users)
- Example: `app.get('/getUsers', handler)`
- Remediation: Use nouns for resources: GET /users instead of GET /getUsers

### POST for Read Operation
**Type**: regex
**Severity**: low
**Pattern**: `\.post\s*\(\s*['"][^'"]*/(get|fetch|retrieve|find|list|search)[^'"]*['"]`
- Using POST for a read operation that should be GET
- Example: `app.post('/fetchUsers', handler)`
- Remediation: Use GET for read operations, POST for creating resources

### GET with Request Body
**Type**: regex
**Severity**: medium
**Pattern**: `\.get\s*\([^)]+\)\s*(?:=>|{)[^}]*req\.body`
- GET request handler accesses request body, which is discouraged
- Example: `app.get('/users', (req, res) => { const data = req.body; })`
- Remediation: GET requests should use query parameters, not body

### Inconsistent Response Format
**Type**: regex
**Severity**: low
**Pattern**: `res\.json\s*\(\s*\{[^}]*\}\s*\)[^}]*res\.json\s*\(\s*[^\{]`
- Inconsistent response formats in same handler (object vs primitive)
- Example: Mixed `res.json({data})` and `res.json("ok")`
- Remediation: Use consistent response wrapper: { data: ..., error: null }

### Magic Status Code
**Type**: regex
**Severity**: info
**Pattern**: `\.status\s*\(\s*[0-9]+\s*\)`
- Using magic number for HTTP status code
- Example: `res.status(404).json({error: 'Not found'})`
- Remediation: Use named constants for better readability

---

## API Performance Patterns

### N+1 Query Pattern
**Type**: regex
**Severity**: high
**Pattern**: `(?:for|forEach|map)\s*\([^)]+\)\s*(?:=>|{)[^}]*(?:await|\.then)[^}]*(?:findOne|findById|get|fetch)`
- Potential N+1 query pattern: database call inside loop
- Example: `users.forEach(async u => await User.findById(u.id))`
- Remediation: Use batch queries or include/populate

### Missing Pagination
**Type**: regex
**Severity**: medium
**Pattern**: `\.find\s*\(\s*\{\s*\}\s*\)|\.find\s*\(\s*\)|\.(findAll|all)\s*\(`
- Unbounded query that returns all records without pagination
- Example: `User.find({})`
- Remediation: Add .limit() and .skip() or use pagination library

### Synchronous File Operation
**Type**: regex
**Severity**: medium
**Pattern**: `(?:readFileSync|writeFileSync|appendFileSync|existsSync)\s*\(`
- Synchronous file operation blocks the event loop
- Example: `fs.readFileSync('config.json')`
- Remediation: Use async versions with await

### Large Payload Without Streaming
**Type**: regex
**Severity**: info
**Pattern**: `JSON\.stringify\s*\([^)]*\)|res\.json\s*\(\s*(?:results|data|items|records)\s*\)`
- Large payload may benefit from streaming
- Example: `res.json(largeDataset)`
- Remediation: Consider streaming for large datasets

---

## API Observability Patterns

### Swallowed Exception
**Type**: regex
**Severity**: high
**Pattern**: `catch\s*\(\s*(?:err|error|e|_)\s*\)\s*\{\s*\}`
- Empty catch block swallows exception silently
- Example: `try { ... } catch (e) { }`
- Remediation: Log the error or re-throw if unhandled

### Console.log in Production
**Type**: regex
**Severity**: low
**Pattern**: `console\.(log|info|warn|error)\s*\(`
- Using console.log instead of structured logging
- Example: `console.log('User logged in:', userId)`
- Remediation: Use structured logger (winston, pino, bunyan)

### Generic Error Response
**Type**: regex
**Severity**: low
**Pattern**: `res\.status\s*\(\s*500\s*\)\.(?:json|send)\s*\(\s*['"](?:error|Error|Something went wrong)['"]`
- Generic error message provides no debugging context
- Example: `res.status(500).json('Error')`
- Remediation: Include error code and message

---

## API Rate Limiting Patterns

### Auth Endpoint Without Rate Limiting
**Type**: regex
**Severity**: high
**Pattern**: `\.(get|post|put|delete)\s*\(\s*['"]/(api|v[0-9]+)/(?:auth|login|register|signup|password|reset|verify|token)[^'"]*['"]`
- Authentication endpoint detected without apparent rate limiting
- Example: `app.post('/api/auth/login', handler)`
- Remediation: Add rate limiting middleware

### File Upload Without Rate Limiting
**Type**: regex
**Severity**: medium
**Pattern**: `(?:multer|upload|formidable|busboy)\s*\(`
- File upload detected - verify rate limiting and size limits
- Example: `multer({ dest: 'uploads/' })`
- Remediation: Add rate limiting and maxFileSize limits

### Search Endpoint
**Type**: regex
**Severity**: medium
**Pattern**: `\.(get|post)\s*\(\s*['"]/(api/)?(?:search|query|find|lookup)[^'"]*['"]`
- Search endpoint detected - verify rate limiting
- Example: `app.get('/api/search', handler)`
- Remediation: Add rate limiting to prevent scraping

### Webhook Endpoint
**Type**: regex
**Severity**: medium
**Pattern**: `\.(post)\s*\(\s*['"]/(api/)?(?:webhook|hook|callback|notify)[^'"]*['"]`
- Webhook endpoint - verify rate limiting and signature validation
- Example: `app.post('/webhook', handler)`
- Remediation: Rate limit and verify request signatures

### Email Sending
**Type**: regex
**Severity**: high
**Pattern**: `(?:sendMail|sendEmail|nodemailer|sendgrid|mailgun|ses\.send)`
- Email sending detected - verify rate limiting
- Example: `transporter.sendMail(mailOptions)`
- Remediation: Add strict rate limiting for email endpoints

### Rate Limit Middleware Detected
**Type**: regex
**Severity**: info
**Pattern**: `(?:rateLimit|RateLimiter|express-rate-limit|rate-limiter-flexible)\s*\(`
- Rate limiting middleware detected - good practice
- Example: `app.use(rateLimit({ windowMs: 15*60*1000, max: 100 }))`
- Remediation: Verify rate limits are appropriate

---

## Language-Specific: Go

### Go Rate Limiter
**Type**: regex
**Severity**: info
**Pattern**: `(?:rate\.NewLimiter|limiter\.New|tollbooth|throttle)\s*\(`
- Rate limiting detected in Go code
- Example: `limiter := rate.NewLimiter(1, 3)`
- Remediation: Verify rate limits are appropriate

---

## Language-Specific: Python

### Python Rate Limiter
**Type**: regex
**Severity**: info
**Pattern**: `(?:flask_limiter|Limiter|ratelimit|slowapi|RateLimitMiddleware)`
- Rate limiting detected in Python code
- Example: `limiter = Limiter(app, key_func=get_remote_address)`
- Remediation: Verify rate limits are appropriate

---

## Detection Confidence

**Regex Detection**: 85%
**Rate Limiting Detection**: 80%

---

## References

- OWASP API Security Top 10
- REST API Best Practices
- Node.js Security Checklist
