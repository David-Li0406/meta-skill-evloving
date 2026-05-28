# STRIDE Analysis Examples

## STRIDE Overview

| Threat | Violates | Question |
|--------|----------|----------|
| **S**poofing | Authentication | Can someone pretend to be someone else? |
| **T**ampering | Integrity | Can data be modified without detection? |
| **R**epudiation | Non-repudiation | Can someone deny doing something? |
| **I**nformation Disclosure | Confidentiality | Can sensitive data leak? |
| **D**enial of Service | Availability | Can the system be made unavailable? |
| **E**levation of Privilege | Authorization | Can someone gain unauthorized access? |

## Example 1: Web Login Flow

### System Description

```
User → Browser → Load Balancer → Web Server → Auth Service → Database
                      ↓
                 Session Store
```

### STRIDE Analysis

#### Spoofing

| Component | Threat | Mitigation |
|-----------|--------|------------|
| User → Browser | Attacker creates phishing page | HTTPS, HSTS, user education |
| Browser → Server | MITM intercepts credentials | TLS, certificate pinning |
| Server → Auth Service | Service impersonation | Mutual TLS, service mesh |

**Specific Threats:**
- Attacker steals session cookie and impersonates user
- Attacker brute-forces login credentials
- Attacker uses stolen credentials from data breach

**Mitigations:**
- HttpOnly, Secure, SameSite cookies
- Rate limiting on login attempts
- Password breach checking (HaveIBeenPwned API)
- Multi-factor authentication

#### Tampering

| Component | Threat | Mitigation |
|-----------|--------|------------|
| Browser storage | XSS modifies stored data | CSP, input sanitization |
| Request data | Man-in-the-middle modifies | TLS encryption |
| Session data | Session fixation | Regenerate session on login |

**Specific Threats:**
- Attacker modifies form data to change user ID
- Attacker tampers with JWT token payload
- Attacker modifies cookie values

**Mitigations:**
- Server-side validation of all inputs
- Signed JWTs with strong algorithm (RS256)
- HMAC on sensitive cookie values

#### Repudiation

| Component | Threat | Mitigation |
|-----------|--------|------------|
| User actions | User denies login attempt | Audit logging |
| Admin actions | Admin denies deleting account | Immutable audit log |

**Specific Threats:**
- User denies making fraudulent purchase
- Admin denies accessing sensitive data

**Mitigations:**
- Comprehensive audit logging
- Tamper-evident logs (append-only, signed)
- Login notifications to user email

#### Information Disclosure

| Component | Threat | Mitigation |
|-----------|--------|------------|
| Error messages | Stack traces reveal internals | Generic error messages |
| Timing | Login timing reveals valid users | Constant-time comparison |
| Logs | Passwords logged in plaintext | Never log credentials |

**Specific Threats:**
- Password visible in browser autocomplete
- Session token visible in URL
- Database dump exposes password hashes

**Mitigations:**
- autocomplete="off" for password fields
- Session tokens only in cookies/headers
- Strong password hashing (bcrypt, Argon2)

#### Denial of Service

| Component | Threat | Mitigation |
|-----------|--------|------------|
| Login endpoint | Brute force attempts | Rate limiting, CAPTCHA |
| Auth service | Resource exhaustion | Timeouts, circuit breakers |
| Session store | Session flooding | Session limits per user |

**Specific Threats:**
- Attacker floods login with requests
- Attacker creates many accounts rapidly
- Attacker locks out legitimate users

**Mitigations:**
- Rate limiting per IP and per account
- CAPTCHA after failed attempts
- Account lockout with admin notification

#### Elevation of Privilege

| Component | Threat | Mitigation |
|-----------|--------|------------|
| Session | User accesses admin functions | Role-based access control |
| URL | User guesses admin URLs | Authorization checks on all endpoints |
| API | User modifies role in request | Server-side role enforcement |

**Specific Threats:**
- User changes "isAdmin=false" to "isAdmin=true"
- User accesses /admin without authorization
- SQL injection elevates privileges

**Mitigations:**
- Never trust client-side role data
- Authorization middleware on all endpoints
- Parameterized queries, ORM

## Example 2: File Upload Feature

### System Description

```
User → Browser → API Server → File Service → Object Storage
                     ↓
                Virus Scanner
```

### STRIDE Analysis

| Threat | Example | Mitigation |
|--------|---------|------------|
| **Spoofing** | Upload file as another user | Verify user owns target |
| **Tampering** | Modify file content in transit | TLS, checksums |
| **Repudiation** | Deny uploading malicious file | Audit log with user ID |
| **Info Disclosure** | Access other users' files | Authorization on download |
| **DoS** | Upload huge files | Size limits, quotas |
| **EoP** | Upload executable to run on server | Content-type validation, sandboxing |

### Detailed Threats

**File Type Attacks:**
```
Threat: User uploads .exe disguised as .jpg
Attack: Rename malware.exe to malware.jpg
Impact: Other users download and execute

Mitigation:
- Validate file content, not just extension
- Use magic bytes to verify file type
- Store files in non-executable location
- Serve with Content-Disposition: attachment
```

**Path Traversal:**
```
Threat: User uploads to arbitrary path
Attack: filename="../../../etc/passwd"
Impact: Overwrite system files

Mitigation:
- Sanitize filename (strip path components)
- Use UUID for stored filename
- Validate final path is within allowed directory
```

**Malware Upload:**
```
Threat: User uploads infected file
Attack: Upload document with macro virus
Impact: Infects other users who download

Mitigation:
- Virus scanning before storage
- Quarantine pending scan results
- Block executable content types
```

## Example 3: API Authentication

### System Description

```
Mobile App → API Gateway → Microservices
               ↓
           Auth Server (OAuth2)
```

### STRIDE for OAuth2 Flow

| Threat | Target | Attack | Mitigation |
|--------|--------|--------|------------|
| Spoofing | Client | Fake client gets token | Client secret, redirect URI validation |
| Spoofing | User | Stolen auth code | PKCE, short-lived codes |
| Tampering | Token | Modified JWT claims | Signature verification |
| Repudiation | API calls | User denies action | Include user ID in audit |
| Info Disclosure | Token | Token in logs | Never log tokens |
| DoS | Auth server | Token endpoint flood | Rate limit per client |
| EoP | Scope | Request excessive scopes | Scope validation, consent screen |

### Token Security

```
Threat: Access token stolen from mobile device
Attack: Malware extracts token from storage
Impact: Attacker has full API access

Mitigations:
- Short token expiry (15 minutes)
- Refresh tokens with rotation
- Token binding to device
- Detect anomalous usage patterns
```

## Threat Model Template

```markdown
## Component: [Name]

### Description
[What this component does]

### Data Flow
[How data enters and leaves]

### Trust Boundaries
[What is trusted vs untrusted]

### STRIDE Analysis

#### Spoofing
- **Threat:** [Description]
- **Likelihood:** [Low/Medium/High]
- **Impact:** [Low/Medium/High]
- **Mitigation:** [How to prevent]

[Repeat for T, R, I, D, E]

### Residual Risk
[Risks that remain after mitigations]

### Action Items
- [ ] Implement [mitigation]
- [ ] Test [threat scenario]
```
