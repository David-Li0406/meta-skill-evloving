# OWASP Top 10 (2021) Reference

## Overview

The OWASP Top 10 represents the most critical security risks to web applications. This guide explains each vulnerability with examples and prevention strategies.

---

## A01: Broken Access Control

**Risk:** Users can access resources or perform actions they shouldn't be authorized for.

### Common Vulnerabilities

- Bypassing access control by modifying URLs or parameters
- Viewing/editing someone else's account by changing the user ID
- Privilege escalation (acting as admin without being one)
- CORS misconfiguration allowing unauthorized API access
- Missing access control on API endpoints

### Examples

```python
# ❌ Insecure Direct Object Reference (IDOR)
@app.route('/api/user/<user_id>')
def get_user(user_id):
    # No check if current user can access this user_id!
    return User.query.get(user_id).to_dict()

# ✅ Secure - Verify authorization
@app.route('/api/user/<user_id>')
@login_required
def get_user(user_id):
    if current_user.id != user_id and not current_user.is_admin:
        abort(403)  # Forbidden
    return User.query.get(user_id).to_dict()
```

### Prevention

1. Deny by default - require explicit permission grants
2. Check authorization on every request
3. Use UUIDs instead of sequential IDs
4. Log access control failures
5. Rate limit failed access attempts

---

## A02: Cryptographic Failures

**Risk:** Sensitive data exposed due to weak or missing cryptography.

### Common Vulnerabilities

- Transmitting data in clear text (HTTP instead of HTTPS)
- Using weak algorithms (MD5, SHA1, DES)
- Hardcoded encryption keys
- Missing encryption for sensitive data at rest
- Improper key management

### Examples

```python
# ❌ Weak password hashing
password_hash = hashlib.md5(password.encode()).hexdigest()

# ✅ Strong password hashing
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))

# ❌ Weak encryption
from Crypto.Cipher import DES  # Deprecated!

# ✅ Strong encryption
from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher = Fernet(key)
encrypted = cipher.encrypt(data.encode())
```

### Prevention

1. Classify data - know what's sensitive
2. Encrypt sensitive data at rest and in transit
3. Use strong algorithms: AES-256, RSA-2048+, bcrypt/Argon2
4. Manage keys securely (KMS, HSM, Vault)
5. Disable caching for sensitive responses

---

## A03: Injection

**Risk:** Untrusted data sent to an interpreter as part of a command or query.

### Types of Injection

| Type | Target | Example |
|------|--------|---------|
| SQL Injection | Database | `'; DROP TABLE users; --` |
| NoSQL Injection | MongoDB, etc. | `{"$gt": ""}` |
| Command Injection | OS shell | `; rm -rf /` |
| LDAP Injection | Directory services | `*)(uid=*))(|(uid=*` |
| XPath Injection | XML queries | `' or '1'='1` |

### Examples

```python
# ❌ SQL Injection vulnerable
query = f"SELECT * FROM users WHERE email = '{email}'"
cursor.execute(query)

# ✅ Parameterized query
cursor.execute("SELECT * FROM users WHERE email = ?", (email,))

# ❌ Command Injection vulnerable
os.system(f"ping {host}")

# ✅ Safe - no shell, argument array
subprocess.run(["ping", "-c", "1", host], shell=False)
```

### Prevention

1. Use parameterized queries (prepared statements)
2. Use ORMs with proper parameter binding
3. Validate and sanitize all input
4. Use allowlists for permitted values
5. Escape special characters when parameterization isn't possible

---

## A04: Insecure Design

**Risk:** Design flaws that can't be fixed by perfect implementation.

### Common Issues

- Missing threat modeling
- No security requirements in design
- Insufficient business logic validation
- Missing rate limiting on sensitive operations
- No defense in depth

### Examples

```python
# ❌ Insecure design - no rate limiting on password reset
@app.route('/api/password-reset', methods=['POST'])
def reset_password():
    email = request.json['email']
    send_reset_email(email)  # Can be spammed!
    return {"status": "sent"}

# ✅ Secure design - rate limited, no info leak
@app.route('/api/password-reset', methods=['POST'])
@rate_limit("3/hour")
def reset_password():
    email = request.json['email']
    if User.exists(email):  # Don't reveal if email exists
        send_reset_email(email)
    # Always return same response
    return {"status": "If account exists, email sent"}
```

### Prevention

1. Threat model during design phase
2. Define security requirements upfront
3. Use secure design patterns
4. Implement defense in depth
5. Limit resource consumption (rate limiting, quotas)

---

## A05: Security Misconfiguration

**Risk:** Missing security hardening or improper configuration.

### Common Issues

- Default credentials left unchanged
- Unnecessary features enabled
- Overly permissive permissions
- Verbose error messages
- Missing security headers
- Outdated software

### Examples

```python
# ❌ Debug mode in production
app.run(debug=True)  # Exposes debugger!

# ✅ Production configuration
app.run(debug=False)

# ❌ Verbose errors
@app.errorhandler(500)
def handle_error(e):
    return {"error": str(e), "trace": traceback.format_exc()}

# ✅ Generic errors
@app.errorhandler(500)
def handle_error(e):
    app.logger.error(f"Error: {e}", exc_info=True)
    return {"error": "Internal server error"}, 500
```

### Security Headers

```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

### Prevention

1. Hardened, repeatable deployment process
2. Remove unnecessary features/frameworks
3. Review and update configurations regularly
4. Use security headers
5. Automated configuration verification

---

## A06: Vulnerable and Outdated Components

**Risk:** Using components with known vulnerabilities.

### Common Issues

- Not knowing all component versions
- Using unsupported or outdated software
- Not scanning for vulnerabilities regularly
- Not updating in timely manner
- Not testing component compatibility

### Tools for Detection

```bash
# Python
pip-audit
safety check

# JavaScript
npm audit
yarn audit

# General
snyk test
dependabot (GitHub)
```

### Prevention

1. Inventory all components and versions
2. Monitor for vulnerabilities (CVE databases)
3. Update regularly with testing
4. Remove unused dependencies
5. Use lockfiles for reproducible builds

---

## A07: Identification and Authentication Failures

**Risk:** Broken authentication allowing attackers to compromise accounts.

### Common Issues

- Permits brute force attacks
- Weak password requirements
- Insecure password recovery
- Session IDs in URL
- Missing/ineffective MFA
- Session fixation

### Examples

```python
# ❌ No brute force protection
@app.route('/login', methods=['POST'])
def login():
    user = User.verify(email, password)
    if user:
        return create_session(user)
    return {"error": "Invalid credentials"}, 401

# ✅ With rate limiting and lockout
@app.route('/login', methods=['POST'])
@rate_limit("5/minute")
def login():
    if is_locked_out(email):
        return {"error": "Account locked. Try again later."}, 429

    user = User.verify(email, password)
    if not user:
        record_failed_attempt(email)
        return {"error": "Invalid credentials"}, 401

    clear_failed_attempts(email)
    return create_session(user)
```

### Prevention

1. Implement MFA where possible
2. Prevent brute force (rate limiting, CAPTCHA, lockouts)
3. Strong password requirements
4. Secure session management
5. Secure password recovery process

---

## A08: Software and Data Integrity Failures

**Risk:** Code or data modified without detection.

### Common Issues

- Insecure CI/CD pipelines
- Auto-update without verification
- Untrusted deserialization
- Missing integrity checks on data
- Compromised dependencies (supply chain attacks)

### Examples

```python
# ❌ Insecure deserialization
import pickle
data = pickle.loads(untrusted_data)  # Can execute arbitrary code!

# ✅ Safe serialization
import json
data = json.loads(untrusted_data)  # Only parses data

# ❌ No integrity verification
def update_software():
    download_and_install(update_url)

# ✅ Verify signature
def update_software():
    package = download(update_url)
    signature = download(signature_url)
    if not verify_signature(package, signature, public_key):
        raise SecurityError("Invalid signature")
    install(package)
```

### Prevention

1. Use digital signatures for code and data
2. Verify integrity of dependencies
3. Secure CI/CD pipeline
4. Avoid insecure deserialization (pickle, yaml.load)
5. Use Subresource Integrity (SRI) for CDN resources

---

## A09: Security Logging and Monitoring Failures

**Risk:** Unable to detect, escalate, or respond to attacks.

### Common Issues

- Not logging security events
- Logs not monitored
- Missing alerting
- Insufficient log detail
- Logs accessible to attackers

### What to Log

```python
SECURITY_EVENTS = {
    "authentication": ["login_success", "login_failure", "logout", "mfa_failure"],
    "authorization": ["access_denied", "privilege_escalation_attempt"],
    "data": ["sensitive_data_access", "bulk_export", "data_modification"],
    "system": ["config_change", "admin_action", "error_rate_spike"],
}

def log_security_event(category, event, user_id, details):
    logger.warning("SECURITY", extra={
        "category": category,
        "event": event,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "ip": get_client_ip(),
        "details": sanitize(details),
    })
```

### Prevention

1. Log all authentication and access control events
2. Monitor logs for suspicious patterns
3. Set up alerting for anomalies
4. Protect log integrity
5. Have an incident response plan

---

## A10: Server-Side Request Forgery (SSRF)

**Risk:** Server makes requests to attacker-controlled destinations.

### Common Issues

- Fetching URLs provided by users
- Accessing internal services via user input
- No URL validation
- Following redirects blindly

### Examples

```python
# ❌ SSRF vulnerable
@app.route('/fetch')
def fetch_url():
    url = request.args.get('url')
    response = requests.get(url)  # Can access internal services!
    return response.content

# ✅ Protected - allowlist domains
ALLOWED_DOMAINS = {'api.example.com', 'cdn.example.com'}

@app.route('/fetch')
def fetch_url():
    url = request.args.get('url')
    parsed = urlparse(url)

    if parsed.netloc not in ALLOWED_DOMAINS:
        abort(400, "Domain not allowed")

    if parsed.scheme not in ('http', 'https'):
        abort(400, "Invalid scheme")

    # Also block internal IPs
    if is_internal_ip(parsed.netloc):
        abort(400, "Internal addresses not allowed")

    response = requests.get(url, allow_redirects=False)
    return response.content
```

### Prevention

1. Allowlist permitted domains/IPs
2. Block requests to internal networks (10.x, 192.168.x, 127.x)
3. Disable redirects or validate redirect targets
4. Don't return raw responses to users
5. Use a dedicated service for URL fetching

---

## Quick Reference

| Vulnerability | One-Line Prevention |
|---------------|---------------------|
| A01 Broken Access Control | Check authorization on every request |
| A02 Cryptographic Failures | Use strong algorithms, encrypt sensitive data |
| A03 Injection | Parameterized queries, never concat input |
| A04 Insecure Design | Threat model, defense in depth |
| A05 Misconfiguration | Secure defaults, remove unused features |
| A06 Vulnerable Components | Update regularly, audit dependencies |
| A07 Auth Failures | MFA, rate limiting, secure sessions |
| A08 Integrity Failures | Sign code, verify dependencies |
| A09 Logging Failures | Log security events, monitor and alert |
| A10 SSRF | Allowlist URLs, block internal addresses |
