# API Rate Limiting & Resource Exhaustion

**Category**: api-security/rate-limiting
**Description**: Detection patterns for missing rate limiting and resource exhaustion vulnerabilities
**CWE**: CWE-770, CWE-400, CWE-1333

---

## OWASP API Security Top 10

- **API4:2023** - Unrestricted Resource Consumption

---

## Missing Rate Limiting

### Express Without Rate Limiter
**Pattern**: `const\s+app\s*=\s*express\s*\(\)(?![\s\S]*rate-limit|rateLimit|rateLimiter)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Express app without rate limiter
- CWE-770: Allocation Without Limits

### Login Without Rate Limit
**Pattern**: `(\/login|\/signin|\/auth|\/authenticate).*app\.(post|get)(?!.*rateLimit|rateLimiter)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Login endpoint without rate limiting
- CWE-770: Allocation Without Limits

### Password Reset Without Rate Limit
**Pattern**: `(\/reset-password|\/forgot-password|\/password-reset).*app\.(post|get)(?!.*rateLimit)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Password reset without rate limiting
- CWE-770: Allocation Without Limits

---

## Missing Request Size Limits

### Body Parser Without Limit
**Pattern**: `(bodyParser|express)\.(json|urlencoded)\s*\(\s*\)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Body parser without size limit
- CWE-770: Allocation Without Limits

### Multer Without Size Limit
**Pattern**: `multer\s*\(\s*\{(?!.*limits)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Multer without file size limit
- CWE-770: Allocation Without Limits

---

## Missing Pagination

### Find All Without Limit
**Pattern**: `\.(find|findAll|findMany)\s*\(\s*\{(?!.*limit|take|first)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Find all without limit
- CWE-770: Allocation Without Limits

### Query Without Pagination
**Pattern**: `(SELECT|select)(?!.*LIMIT|limit).*FROM.*res\.(json|send)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript, python]
- Database query without pagination
- CWE-770: Allocation Without Limits

---

## GraphQL Complexity Limits

### GraphQL Without Depth Limit
**Pattern**: `(ApolloServer|GraphQLServer)\s*\(\s*\{(?!.*depthLimit|queryComplexity|maxDepth)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- GraphQL without depth limiting
- CWE-770: Allocation Without Limits

### GraphQL Without Complexity
**Pattern**: `(ApolloServer|GraphQLServer)\s*\(\s*\{(?!.*complexity|costAnalysis)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- GraphQL without query complexity
- CWE-770: Allocation Without Limits

---

## Unrestricted File Upload

### Upload Without Size Limit
**Pattern**: `(upload|multer|formidable|busboy)(?!.*fileSize|maxFileSize|limits)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- File upload without size validation
- CWE-400: Uncontrolled Resource Consumption

### No File Count Limit
**Pattern**: `(\.array|\.fields)\s*\([^)]*\)(?!.*maxCount|limits)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- No file count limit
- CWE-400: Uncontrolled Resource Consumption

---

## Regex DoS (ReDoS)

### Dynamic Regex
**Pattern**: `new\s+RegExp\s*\(\s*req\.(body|params|query)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Dangerous regex patterns from user input
- CWE-1333: ReDoS

### Nested Quantifiers
**Pattern**: `\/\([^)]*[\*\+]\)[^\/]*[\*\+]\/`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Nested quantifiers (potential ReDoS)
- CWE-1333: ReDoS

---

## Missing Timeout

### HTTP Request Without Timeout
**Pattern**: `(axios|fetch|request|got)\s*\(\s*[^)]*\)(?!.*timeout)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- HTTP request without timeout
- CWE-400: Uncontrolled Resource Consumption

### Query Without Timeout
**Pattern**: `(query|execute)\s*\(\s*[^)]*\)(?!.*timeout|maxTimeMS)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript, python]
- Database query without timeout
- CWE-400: Uncontrolled Resource Consumption

---

## Memory Exhaustion

### Unbounded Array Growth
**Pattern**: `\[\s*\]\.push\s*\([^)]*req\.(body|params|query)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Unbounded array growth
- CWE-400: Uncontrolled Resource Consumption

### Read File From Request
**Pattern**: `(readFileSync|readFile)\s*\([^)]*req\.(body|params|query)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Reading entire file into memory from user input
- CWE-400: Uncontrolled Resource Consumption

---

## Connection Pool Exhaustion

### DB Without Pooling
**Pattern**: `(createConnection|connect)\s*\([^)]*\)(?!.*pool|poolSize|connectionLimit)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Database connection without pooling
- CWE-400: Uncontrolled Resource Consumption

---

## Batch Operation Limits

### Bulk Ops Without Limit
**Pattern**: `(bulkCreate|insertMany|bulkWrite)\s*\(\s*req\.body(?!.*limit)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Bulk operations without limits
- CWE-770: Allocation Without Limits

---

## CPU-Intensive Operations

### Sync Crypto In Handler
**Pattern**: `(pbkdf2Sync|scryptSync|hashSync)\s*\([^)]*req\.(body|params|query)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Synchronous crypto in request handler
- CWE-400: Uncontrolled Resource Consumption

### JSON Parse From Request
**Pattern**: `JSON\.parse\s*\(\s*req\.(body|params|query)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- JSON parsing of large input
- CWE-400: Uncontrolled Resource Consumption

---

## Detection Confidence

**Regex Detection**: 75%
**Security Pattern Detection**: 70%

---

## References

- [OWASP API4:2023 - Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)
- [CWE-770: Allocation of Resources Without Limits](https://cwe.mitre.org/data/definitions/770.html)
- [CWE-400: Uncontrolled Resource Consumption](https://cwe.mitre.org/data/definitions/400.html)
