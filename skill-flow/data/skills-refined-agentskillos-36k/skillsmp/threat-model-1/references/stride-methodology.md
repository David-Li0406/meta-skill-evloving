# STRIDE Threat Modeling Methodology

## STRIDE Categories

### Spoofing

**Definition:** Pretending to be someone or something else.

**Questions to Ask:**
- How does the system verify user identity?
- Can an attacker forge credentials?
- Are sessions properly validated?
- Can API keys/tokens be stolen or replicated?

**Common Threats:**
| Threat | Example | Mitigation |
|--------|---------|------------|
| Credential theft | Phishing, keyloggers | MFA, password managers |
| Session hijacking | Cookie theft, fixation | Secure cookies, regeneration |
| Token forgery | JWT manipulation | Signature verification, short expiry |
| IP spoofing | Source address forgery | Don't rely solely on IP |

**Mitigations:**
- Strong authentication (MFA)
- Cryptographic signing
- Certificate validation
- Session management best practices

---

### Tampering

**Definition:** Modifying data or code without authorization.

**Questions to Ask:**
- Can data be modified in transit?
- Are stored files/databases protected?
- Can configuration be changed?
- Are logs tamper-proof?

**Common Threats:**
| Threat | Example | Mitigation |
|--------|---------|------------|
| MITM attacks | SSL stripping | TLS everywhere, HSTS |
| Database tampering | SQL injection | Parameterized queries |
| File modification | Config changes | File integrity monitoring |
| Memory corruption | Buffer overflow | Memory-safe languages, ASLR |

**Mitigations:**
- TLS for data in transit
- Encryption at rest
- Digital signatures
- Input validation
- Integrity monitoring

---

### Repudiation

**Definition:** Denying an action without others being able to prove otherwise.

**Questions to Ask:**
- Are all actions logged?
- Can logs be tampered with?
- Is there proof of transactions?
- Can users deny actions they performed?

**Common Threats:**
| Threat | Example | Mitigation |
|--------|---------|------------|
| Log deletion | Attacker erases traces | Append-only, off-site logs |
| Action denial | User claims didn't place order | Digital signatures |
| Timestamp manipulation | Fake timestamps | NTP, trusted timestamping |
| No audit trail | Missing logs | Comprehensive logging |

**Mitigations:**
- Comprehensive audit logging
- Log integrity protection
- Digital signatures for transactions
- Non-repudiation protocols
- Third-party timestamping

---

### Information Disclosure

**Definition:** Exposing information to unauthorized parties.

**Questions to Ask:**
- What sensitive data exists?
- Who can access it and how?
- Is data encrypted at rest and in transit?
- Are error messages revealing?

**Common Threats:**
| Threat | Example | Mitigation |
|--------|---------|------------|
| Data breach | Database dump | Encryption, access controls |
| Verbose errors | Stack traces in response | Generic error messages |
| Path traversal | Access to /etc/passwd | Input validation |
| Side channels | Timing attacks | Constant-time operations |

**Mitigations:**
- Encryption (transit and rest)
- Access control lists
- Data classification
- Minimal error messages
- Secure defaults

---

### Denial of Service

**Definition:** Making a system unavailable or degraded.

**Questions to Ask:**
- What happens under high load?
- Are there resource limits?
- Can single requests consume excessive resources?
- What's the blast radius of failures?

**Common Threats:**
| Threat | Example | Mitigation |
|--------|---------|------------|
| Resource exhaustion | Memory/CPU floods | Rate limiting, quotas |
| Amplification | DNS amplification | Response limiting |
| Application DoS | Regex DoS (ReDoS) | Safe regex, timeouts |
| Account lockout | Locking legitimate users | CAPTCHA, progressive delay |

**Mitigations:**
- Rate limiting
- Resource quotas
- Auto-scaling
- DDoS protection (CDN, WAF)
- Graceful degradation

---

### Elevation of Privilege

**Definition:** Gaining capabilities beyond what's authorized.

**Questions to Ask:**
- How are permissions enforced?
- Can users modify their own roles?
- Are there privilege boundaries?
- What happens if a component is compromised?

**Common Threats:**
| Threat | Example | Mitigation |
|--------|---------|------------|
| Vertical escalation | User → Admin | Proper authorization |
| Horizontal escalation | Access other users' data | Object-level auth |
| Container escape | Break out of container | Security contexts |
| Injection | Command injection | Input sanitization |

**Mitigations:**
- Principle of least privilege
- Separation of duties
- Sandboxing/isolation
- Input validation
- Regular privilege audits

## Threat Modeling Process

### 1. Define Scope

```
System: [Name]
Components: [List major components]
Data Flows: [Key data movements]
Trust Boundaries: [Where trust changes]
```

### 2. Create Data Flow Diagram

```
[External Entity] --> [Process] --> [Data Store]
       |                  |
       v                  v
   [Process]         [Process]
```

**Elements:**
- **External Entities:** Users, external systems (rectangles)
- **Processes:** Code that transforms data (circles)
- **Data Stores:** Databases, files, caches (parallel lines)
- **Data Flows:** Movement of data (arrows)
- **Trust Boundaries:** Where privilege changes (dashed lines)

### 3. Identify Threats per Element

| Element | Type | STRIDE Applicable |
|---------|------|-------------------|
| External Entity | User, system | S |
| Process | Code | S, T, R, I, D, E |
| Data Store | Database | T, R, I, D |
| Data Flow | Network | T, I, D |

### 4. Document Threats

```markdown
## Threat: [ID] - [Name]

**Category:** [STRIDE category]
**Component:** [Affected component]
**Description:** [What could happen]
**Attack Vector:** [How it could be exploited]
**Impact:** [High/Medium/Low] - [Description]
**Likelihood:** [High/Medium/Low] - [Reasoning]
**Risk Score:** [Impact × Likelihood]

**Mitigations:**
1. [Mitigation 1]
2. [Mitigation 2]

**Status:** [Open/Mitigated/Accepted]
```

### 5. Prioritize and Mitigate

**Risk Matrix:**

|              | Low Impact | Medium Impact | High Impact |
|--------------|------------|---------------|-------------|
| High Likelihood | Medium | High | Critical |
| Medium Likelihood | Low | Medium | High |
| Low Likelihood | Low | Low | Medium |

## Quick Reference Card

```
┌────────────────────────────────────────────────────┐
│ STRIDE Quick Reference                              │
├──────────┬─────────────────────────────────────────┤
│ S        │ Can someone pretend to be someone else? │
│ T        │ Can data be modified without detection? │
│ R        │ Can users deny actions they performed?  │
│ I        │ Can sensitive data be exposed?          │
│ D        │ Can the system be made unavailable?     │
│ E        │ Can someone gain unauthorized access?   │
└──────────┴─────────────────────────────────────────┘
```

## Threat Library Examples

### Authentication

| ID | Threat | STRIDE | Mitigation |
|----|--------|--------|------------|
| AUTH-01 | Brute force password | S | Account lockout, rate limiting |
| AUTH-02 | Credential stuffing | S | Breach detection, MFA |
| AUTH-03 | Session fixation | S | Regenerate session on login |
| AUTH-04 | Token replay | S | Short expiry, one-time tokens |

### API

| ID | Threat | STRIDE | Mitigation |
|----|--------|--------|------------|
| API-01 | Missing authentication | S, E | Require auth on all endpoints |
| API-02 | BOLA/IDOR | E | Object-level authorization |
| API-03 | Mass assignment | T | Explicit allowlists |
| API-04 | Excessive data exposure | I | Response filtering |

### Data

| ID | Threat | STRIDE | Mitigation |
|----|--------|--------|------------|
| DATA-01 | SQL injection | T, I, E | Parameterized queries |
| DATA-02 | Unencrypted storage | I | Encryption at rest |
| DATA-03 | Backup exposure | I | Encrypted backups |
| DATA-04 | Log injection | R, T | Log sanitization |
