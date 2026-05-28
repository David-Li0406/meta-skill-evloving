# API Server-Side Request Forgery (SSRF)

**Category**: api-security/ssrf
**Description**: Detection patterns for SSRF vulnerabilities in API endpoints
**CWE**: CWE-918, CWE-611

---

## OWASP API Security Top 10

- **API7:2023** - Server Side Request Forgery

---

## Direct URL from Request

### Fetch With User URL
**Pattern**: `(fetch|axios|got|request|http\.get|https\.get)\s*\(\s*req\.(body|params|query)\.(url|uri|href|link|target|redirect)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Fetch/axios with user-provided URL
- CWE-918: SSRF

### Python Requests With User URL
**Pattern**: `requests\.(get|post|put|delete|head|patch)\s*\(\s*request\.(args|form|json)\.(url|uri|href|link|target)`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Python requests with user URL
- CWE-918: SSRF

---

## URL Construction from User Input

### URL Concatenation
**Pattern**: `(http|https):\/\/.*(\+|\$\{).*req\.(body|params|query)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- URL concatenation with user input
- CWE-918: SSRF

### Template Literal URL
**Pattern**: `(http|https):\/\/.*\$\{.*req\.(body|params|query)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Template literal URL with user input
- CWE-918: SSRF

### Python f-string URL
**Pattern**: `f['"](http|https):\/\/.*\{.*request\.(args|form|json)`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Python f-string URL construction
- CWE-918: SSRF

---

## Image/File URL Fetch

### Image URL From Request
**Pattern**: `(imageUrl|image_url|avatarUrl|avatar_url|fileUrl|file_url|pictureUrl)\s*=\s*req\.(body|params|query)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript, python]
- Image download from user URL
- CWE-918: SSRF

### File Download From Request
**Pattern**: `(download|fetch|get).*\(\s*req\.(body|params|query)\.(url|path|file|image)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Fetch for file download from user input
- CWE-918: SSRF

---

## Webhook URL

### Webhook From User Input
**Pattern**: `(webhook|callback|notify|endpoint).*=\s*req\.(body|params|query)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript, python]
- Webhook endpoint from user input
- CWE-918: SSRF

---

## XML External Entity (XXE)

### XML Parsing Without Protection
**Pattern**: `(DOMParser|xml2js|xmldom|libxmljs|etree\.parse|lxml\.etree)(?!.*resolveExternals\s*[=:]\s*false|noent\s*[=:]\s*false)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript, python]
- XML parsing without disabling external entities
- CWE-611: XXE

### Dangerous XML Parser Options
**Pattern**: `(parseXML|parse).*\{[^}]*(resolveExternals|expandEntities|loadExternalDTD)\s*[=:]\s*true`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Dangerous XML parser options enabled
- CWE-611: XXE

---

## PDF/HTML Generation SSRF

### PDF From User URL
**Pattern**: `(puppeteer|playwright|pdf|wkhtmltopdf|phantom).*(goto|navigate|url|create)\s*\([^)]*req\.(body|params|query)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- PDF generation from user-controlled URL
- CWE-918: SSRF

### Browser Automation With User URL
**Pattern**: `(page\.goto|page\.navigate|browser\.newPage).*req\.(body|params|query)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Browser automation with user URL
- CWE-918: SSRF

---

## Cloud Metadata Access

### AWS Metadata Endpoint
**Pattern**: `169\.254\.169\.254`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript, python, java, go]
- AWS metadata endpoint access pattern
- CWE-918: SSRF to Cloud Metadata

### GCP Metadata Endpoint
**Pattern**: `metadata\.google\.internal`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript, python, java, go]
- GCP metadata endpoint access
- CWE-918: SSRF to Cloud Metadata

### Azure Metadata Endpoint
**Pattern**: `169\.254\.169\.254.*metadata`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript, python, java, go]
- Azure metadata endpoint access
- CWE-918: SSRF to Cloud Metadata

---

## Internal Network Access

### Localhost/Internal IP
**Pattern**: `(127\.|10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.|localhost|0\.0\.0\.0)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript, python]
- Localhost or internal IP patterns
- CWE-918: SSRF

---

## Redirect Following

### Following Redirects
**Pattern**: `(followRedirects?|maxRedirects|redirect)\s*[=:]\s*(true|[1-9])`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- Following redirects without validation
- CWE-918: SSRF via Redirect

---

## Dynamic Import SSRF

### Dynamic Import From Request
**Pattern**: `import\s*\(\s*req\.(body|params|query)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Dynamic import from user URL
- CWE-918: SSRF

### Require From Request
**Pattern**: `require\s*\(\s*req\.(body|params|query)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- Require from user input
- CWE-918: SSRF

---

## Protocol Handler SSRF

### File Protocol
**Pattern**: `file:\/\/`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript, python]
- File protocol in URL
- CWE-918: SSRF

### Gopher Protocol
**Pattern**: `gopher:\/\/`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript, python]
- Gopher protocol in URL
- CWE-918: SSRF

### Dict Protocol
**Pattern**: `dict:\/\/`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript, python]
- Dict protocol in URL
- CWE-918: SSRF

---

## Detection Confidence

**Regex Detection**: 90%
**Security Pattern Detection**: 85%

---

## References

- [OWASP API7:2023 - Server Side Request Forgery](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/)
- [CWE-918: Server-Side Request Forgery](https://cwe.mitre.org/data/definitions/918.html)
- [PortSwigger SSRF](https://portswigger.net/web-security/ssrf)
