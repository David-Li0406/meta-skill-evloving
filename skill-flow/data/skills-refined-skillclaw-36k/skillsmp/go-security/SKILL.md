---
name: go-security
description: >
  Go security patterns and vulnerability prevention. Load when handling user
  input, authentication, API endpoints, database queries, file operations,
  or external integrations. Triggers: SQL queries, exec.Command, file paths,
  HTTP clients, secrets, passwords, TLS, or security audits.
license: MIT
compatibility: opencode
---

# Go Security Patterns

Security best practices for Go applications - preventing common vulnerabilities and secure coding patterns.

## When This Skill MUST Be Used

**ALWAYS invoke this skill when the user's request involves ANY of these:**

- Handling user input (forms, query params, headers)
- Database queries (SQL, NoSQL)
- Executing shell commands
- File path operations
- HTTP client requests
- Authentication or authorization
- Password handling
- Secret management
- TLS configuration
- Security audits or reviews

**If you're about to handle untrusted input, STOP and use this skill first.**

## Critical Safety Rules

**NEVER:**
- Hardcode secrets, API keys, or passwords
- Use `fmt.Sprintf` for SQL queries
- Use `exec.Command("sh", "-c", userInput)`
- Trust user input in file paths without validation
- Use `http.DefaultClient` (no timeout)
- Ignore TLS errors
- Store passwords in plaintext
- Log sensitive data (passwords, tokens, PII)

**ALWAYS:**
- Use parameterized queries for SQL
- Validate and sanitize all user input
- Set timeouts on HTTP clients
- Use bcrypt for password hashing
- Load secrets from environment variables
- Run `gosec` and `govulncheck` before deployment

## Quick Reference

| Task | Command |
|------|---------|
| Static analysis | `gosec ./...` |
| Dependency vulnerabilities | `govulncheck ./...` |
| Secret scanning | `gitleaks detect` |
| Fuzz testing | `go test -fuzz=FuzzMyFunction` |

---

# Secret Management

```go
// NEVER: Hardcoded secrets
apiKey := "sk-proj-xxxxx"

// ALWAYS: Environment variables
apiKey := os.Getenv("API_KEY")
if apiKey == "" {
    return errors.New("API_KEY not configured")
}
```

---

# SQL Injection Prevention

```go
// BAD: String concatenation
query := fmt.Sprintf("SELECT * FROM users WHERE id = %s", userID)

// GOOD: Parameterized queries
query := "SELECT * FROM users WHERE id = ?"
db.Query(query, userID)

// GOOD: Using sqlx named queries
query := "SELECT * FROM users WHERE id = :id"
db.NamedQuery(query, map[string]interface{}{"id": userID})
```

---

# Command Injection Prevention

```go
// BAD: User input in shell command
cmd := exec.Command("sh", "-c", "ping " + userInput)

// GOOD: Separate arguments, no shell
cmd := exec.Command("ping", "-c", "1", userInput)

// BETTER: Validate input first
if !isValidHostname(userInput) {
    return errors.New("invalid hostname")
}
```

---

# Path Traversal Prevention

```go
// BAD: Direct user input in file path
path := filepath.Join("/uploads", userInput)

// GOOD: Clean and validate
cleanPath := filepath.Clean(userInput)
if strings.Contains(cleanPath, "..") {
    return errors.New("invalid path")
}
fullPath := filepath.Join("/uploads", filepath.Base(cleanPath))
```

---

# Race Condition Prevention

```go
// BAD: Check-then-act without lock
if balance >= amount {
    withdraw(amount)  // Race condition!
}

// GOOD: Database transaction with row lock
tx, _ := db.BeginTx(ctx, nil)
defer tx.Rollback()

var balance int
tx.QueryRow("SELECT balance FROM accounts WHERE id = ? FOR UPDATE", id).Scan(&balance)
if balance < amount {
    return ErrInsufficientFunds
}
tx.Exec("UPDATE accounts SET balance = balance - ? WHERE id = ?", amount, id)
tx.Commit()
```

---

# Context Timeouts

```go
// GOOD: Always set timeouts for external calls
ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
defer cancel()

resp, err := client.Do(req.WithContext(ctx))
```

---

# HTTP Client Security

```go
// BAD: Default client has no timeout
resp, _ := http.Get(url)

// GOOD: Custom client with timeout
client := &http.Client{
    Timeout: 10 * time.Second,
    CheckRedirect: func(req *http.Request, via []*http.Request) error {
        return http.ErrUseLastResponse
    },
}
```

---

# TLS Configuration

```go
tlsConfig := &tls.Config{
    MinVersion: tls.VersionTLS12,
    CipherSuites: []uint16{
        tls.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
        tls.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
    },
}
```

---

# Password Hashing

```go
// BAD: Weak hash
hash := md5.Sum([]byte(password))

// GOOD: Use bcrypt
hash, _ := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)

// Verify
err := bcrypt.CompareHashAndPassword(hash, []byte(password))
```

---

# Input Validation

```go
// Validate before use
func processID(input string) (UserID, error) {
    id, err := strconv.ParseInt(input, 10, 64)
    if err != nil {
        return 0, fmt.Errorf("invalid ID format: %w", err)
    }
    
    if id <= 0 {
        return 0, errors.New("ID must be positive")
    }
    
    return UserID(id), nil
}
```

---

# CSRF Protection

```go
// Generate token
token := make([]byte, 32)
rand.Read(token)
csrfToken := base64.URLEncoding.EncodeToString(token)

// Store in session, verify on POST requests
func verifyCSRF(r *http.Request, sessionToken string) bool {
    formToken := r.FormValue("csrf_token")
    return subtle.ConstantTimeCompare([]byte(formToken), []byte(sessionToken)) == 1
}
```

---

# Secure Headers

```go
func securityHeaders(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("X-Content-Type-Options", "nosniff")
        w.Header().Set("X-Frame-Options", "DENY")
        w.Header().Set("X-XSS-Protection", "1; mode=block")
        w.Header().Set("Content-Security-Policy", "default-src 'self'")
        w.Header().Set("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        next.ServeHTTP(w, r)
    })
}
```

---

# Rate Limiting

```go
import "golang.org/x/time/rate"

type RateLimiter struct {
    limiters map[string]*rate.Limiter
    mu       sync.Mutex
}

func (rl *RateLimiter) Allow(ip string) bool {
    rl.mu.Lock()
    defer rl.mu.Unlock()
    
    limiter, exists := rl.limiters[ip]
    if !exists {
        limiter = rate.NewLimiter(rate.Limit(10), 20) // 10 req/sec, burst 20
        rl.limiters[ip] = limiter
    }
    
    return limiter.Allow()
}
```

---

# Security Tools

```bash
# Static analysis
gosec ./...

# Dependency vulnerabilities
govulncheck ./...

# Secret scanning
gitleaks detect

# Fuzz testing
go test -fuzz=FuzzMyFunction
```

---

# Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| SQL injection detected | String concatenation | Use parameterized queries |
| Command injection | Shell execution | Use separate args, validate input |
| Path traversal | Unvalidated path | Use filepath.Base, check for `..` |
| Timeout not working | Using DefaultClient | Create custom http.Client |
| Password breach | Weak hashing | Use bcrypt |
| Secret in logs | Logging request bodies | Redact sensitive fields |

---

# Anti-Patterns

| Pattern | Risk | Fix |
|---------|------|-----|
| `fmt.Sprintf` in SQL | SQL injection | Parameterized queries |
| `exec.Command("sh", "-c", ...)` | Command injection | Separate arguments |
| User input in file paths | Path traversal | Validate, use filepath.Base |
| `http.DefaultClient` | No timeout, DoS | Custom client with timeout |
| Plaintext password comparison | Auth bypass | bcrypt |
| Logging request bodies | PII exposure | Redact sensitive data |
| Ignoring TLS errors | MITM attacks | Proper cert validation |
| Hardcoded secrets | Secret exposure | Environment variables |

---

# Example Requests

| User Request | Action |
|--------------|--------|
| "Add database query" | Use parameterized queries, validate input |
| "Execute shell command" | Avoid shell, use separate args, validate |
| "Handle file upload" | Validate filename, use filepath.Base |
| "Add HTTP client call" | Set timeout, validate response |
| "Store user password" | Use bcrypt, never store plaintext |
| "Add API key" | Load from env var, never hardcode |
| "Security audit" | Run gosec, govulncheck, gitleaks |
| "Add authentication" | Use bcrypt, secure sessions, CSRF tokens |
