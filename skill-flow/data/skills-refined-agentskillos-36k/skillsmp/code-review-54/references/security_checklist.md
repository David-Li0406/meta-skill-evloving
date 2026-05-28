# Security Checklist

Level 3 resource for code-review skill - load for security audits.

## OWASP Top 10 (2021)

### A01: Broken Access Control

**Check for:**

- [ ] Authorization checks on all endpoints
- [ ] RBAC/ABAC properly implemented
- [ ] No direct object references without validation
- [ ] Principle of least privilege

**Code patterns to flag:**

```go
// ❌ Bad: No authorization check
func GetUser(w http.ResponseWriter, r *http.Request) {
    userID := r.URL.Query().Get("id")
    user, _ := db.GetUser(userID)  // Anyone can access any user!
    json.NewEncoder(w).Encode(user)
}

// ✅ Good: Verify ownership
func GetUser(w http.ResponseWriter, r *http.Request) {
    requestingUserID := r.Context().Value("userID").(string)
    targetUserID := r.URL.Query().Get("id")

    if requestingUserID != targetUserID && !isAdmin(requestingUserID) {
        http.Error(w, "Forbidden", http.StatusForbidden)
        return
    }
    // ...
}
```

### A02: Cryptographic Failures

**Check for:**

- [ ] Strong encryption (AES-256-GCM, not DES/3DES)
- [ ] Proper key management
- [ ] TLS 1.2+ for transit
- [ ] No hardcoded secrets

**Code patterns to flag:**

```go
// ❌ Bad: Weak encryption
cipher, _ := des.NewCipher(key)  // DES is broken

// ✅ Good: Strong encryption
block, _ := aes.NewCipher(key)
gcm, _ := cipher.NewGCM(block)

// ❌ Bad: Hardcoded secret
const apiKey = "sk-1234567890"

// ✅ Good: Environment variable
apiKey := os.Getenv("API_KEY")
```

### A03: Injection

**Check for:**

- [ ] Parameterized queries (no string concatenation)
- [ ] Input validation
- [ ] Output encoding
- [ ] Command injection prevention

**Code patterns to flag:**

```go
// ❌ Bad: SQL injection
query := "SELECT * FROM users WHERE id = " + userID
db.Query(query)

// ✅ Good: Parameterized query
db.Query("SELECT * FROM users WHERE id = $1", userID)

// ❌ Bad: Command injection
exec.Command("sh", "-c", "ls " + userInput)

// ✅ Good: Pass arguments separately
exec.Command("ls", userInput)
```

### A04: Insecure Design

**Check for:**

- [ ] Threat modeling performed
- [ ] Security requirements defined
- [ ] Fail-secure defaults
- [ ] Defense in depth

### A05: Security Misconfiguration

**Check for:**

- [ ] No default credentials
- [ ] Unnecessary features disabled
- [ ] Error handling doesn't leak info
- [ ] Security headers present

```go
// ❌ Bad: Detailed error to client
http.Error(w, fmt.Sprintf("Database error: %v", err), 500)

// ✅ Good: Generic error, log details
log.Printf("Database error: %v", err)
http.Error(w, "Internal server error", 500)
```

### A06: Vulnerable Components

**Check for:**

- [ ] Dependencies up to date
- [ ] No known vulnerabilities
- [ ] Dependency scanning in CI

```bash
# Check Go vulnerabilities
go list -m -json all | nancy sleuth

# Check npm vulnerabilities
npm audit
```

### A07: Authentication Failures

**Check for:**

- [ ] Strong password requirements
- [ ] Rate limiting on login
- [ ] Secure session management
- [ ] MFA support

**Token handling (mcp-oauth-proxy specific):**

```go
// ✅ Good: Encrypt tokens at rest
encryptedToken, _ := encryptAESGCM(accessToken, key)
db.StoreToken(userID, encryptedToken)

// ✅ Good: Short-lived access tokens
accessToken := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
    "exp": time.Now().Add(15 * time.Minute).Unix(),  // 15 min expiry
    "sub": userID,
})
```

### A08: Software and Data Integrity

**Check for:**

- [ ] Signed dependencies
- [ ] CI/CD pipeline security
- [ ] Code signing

### A09: Security Logging

**Check for:**

- [ ] Authentication events logged
- [ ] Access control failures logged
- [ ] No sensitive data in logs

```go
// ❌ Bad: Logging sensitive data
log.Printf("User login: %s password: %s", username, password)

// ✅ Good: Sanitized logging
log.Printf("User login attempt: %s from IP: %s", username, clientIP)
```

### A10: Server-Side Request Forgery (SSRF)

**Check for:**

- [ ] URL validation
- [ ] Allowlist for external calls
- [ ] No user-controlled URLs without validation

```go
// ❌ Bad: SSRF vulnerability
url := r.FormValue("url")
resp, _ := http.Get(url)  // Can access internal services!

// ✅ Good: Validate URL
url := r.FormValue("url")
if !isAllowedDomain(url) {
    http.Error(w, "Invalid URL", 400)
    return
}
```

## Project-Specific Security

### mcp-oauth-proxy

- [ ] PKCE implemented for public clients
- [ ] Token encryption uses AES-256-GCM
- [ ] Refresh tokens rotated on use
- [ ] JWT validation includes all claims

### obot-entraid

- [ ] Session tokens httpOnly
- [ ] CSRF protection enabled
- [ ] Content Security Policy headers

### obot-tools

- [ ] Credential handling secure
- [ ] No secrets in tool definitions
- [ ] API calls use HTTPS

## Quick Reference

| Issue | Severity | CWE |
| :------- | :---------- | :----- |
| SQL Injection | Critical | CWE-89 |
| Command Injection | Critical | CWE-78 |
| Hardcoded Secret | Critical | CWE-798 |
| Missing Auth | High | CWE-306 |
| Weak Crypto | High | CWE-327 |
| SSRF | High | CWE-918 |
| XSS | Medium | CWE-79 |
| Info Disclosure | Medium | CWE-200 |
