# Threat Model Template

## Overview

Threat modeling helps identify security risks early in the design process. Complete this template for new features, systems, or significant changes.

---

## Project Information

| Field | Value |
|-------|-------|
| **Project/Feature Name** | _[Name]_ |
| **Author** | _[Your name]_ |
| **Date** | _[Date]_ |
| **Version** | _[1.0]_ |
| **Status** | _[Draft / In Review / Approved]_ |

---

## System Description

### Purpose

_What does this system/feature do? What problem does it solve?_

```
[Describe the system's purpose in 2-3 sentences]
```

### Architecture Overview

_High-level diagram of components and data flow_

```
[ASCII diagram or reference to architecture doc]

Example:
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Client  │────▶│   API    │────▶│ Database │
│  (Web)   │◀────│  Server  │◀────│          │
└──────────┘     └──────────┘     └──────────┘
                      │
                      ▼
                ┌──────────┐
                │ External │
                │   API    │
                └──────────┘
```

### Components

| Component | Description | Technology |
|-----------|-------------|------------|
| _[Name]_ | _[What it does]_ | _[Tech stack]_ |
| | | |
| | | |

### Data Classification

| Data Type | Classification | Storage Location | Encryption |
|-----------|---------------|------------------|------------|
| User passwords | Confidential | Database | Hashed (bcrypt) |
| Email addresses | PII | Database | At rest (AES-256) |
| Session tokens | Confidential | Redis | N/A |
| _[Add more]_ | | | |

---

## Trust Boundaries

_Where does trusted meet untrusted?_

### Boundaries Identified

| Boundary | Trust Level Change |
|----------|-------------------|
| Browser → API | Untrusted → Authenticated |
| API → Database | Authenticated → Trusted |
| API → External Service | Authenticated → Untrusted |
| _[Add more]_ | |

---

## Assets

_What are we protecting?_

| Asset | Value | Impact if Compromised |
|-------|-------|----------------------|
| User credentials | High | Account takeover, data breach |
| User PII | High | Privacy violation, regulatory fines |
| Business data | Medium | Competitive disadvantage |
| System availability | Medium | Revenue loss, reputation damage |
| _[Add more]_ | | |

---

## Threat Identification (STRIDE)

Use STRIDE to systematically identify threats:

### S - Spoofing (Identity)

_Can someone pretend to be someone else?_

| Threat | Target | Likelihood | Impact | Mitigation |
|--------|--------|------------|--------|------------|
| Credential stuffing | Login endpoint | High | High | Rate limiting, MFA |
| Session hijacking | User sessions | Medium | High | Secure cookies, HTTPS |
| _[Add more]_ | | | | |

### T - Tampering (Integrity)

_Can someone modify data maliciously?_

| Threat | Target | Likelihood | Impact | Mitigation |
|--------|--------|------------|--------|------------|
| SQL injection | Database | Medium | Critical | Parameterized queries |
| Parameter tampering | API requests | High | Medium | Server-side validation |
| _[Add more]_ | | | | |

### R - Repudiation (Non-repudiation)

_Can someone deny they performed an action?_

| Threat | Target | Likelihood | Impact | Mitigation |
|--------|--------|------------|--------|------------|
| Deleted audit logs | Logging system | Low | High | Append-only logs, backup |
| Forged timestamps | Activity logs | Low | Medium | Server-side timestamps |
| _[Add more]_ | | | | |

### I - Information Disclosure (Confidentiality)

_Can sensitive information be exposed?_

| Threat | Target | Likelihood | Impact | Mitigation |
|--------|--------|------------|--------|------------|
| Error message leakage | API responses | Medium | Low | Generic error messages |
| Log file exposure | Application logs | Low | High | Secure log storage |
| IDOR | User data | Medium | High | Authorization checks |
| _[Add more]_ | | | | |

### D - Denial of Service (Availability)

_Can the system be made unavailable?_

| Threat | Target | Likelihood | Impact | Mitigation |
|--------|--------|------------|--------|------------|
| API flooding | Public endpoints | High | Medium | Rate limiting |
| Resource exhaustion | File uploads | Medium | Medium | Size limits, quotas |
| _[Add more]_ | | | | |

### E - Elevation of Privilege (Authorization)

_Can someone gain unauthorized access?_

| Threat | Target | Likelihood | Impact | Mitigation |
|--------|--------|------------|--------|------------|
| Admin access bypass | Admin functions | Low | Critical | Role-based access |
| Horizontal escalation | Other users' data | Medium | High | Owner checks on all resources |
| _[Add more]_ | | | | |

---

## Attack Trees

_For critical assets, map possible attack paths_

### Example: Unauthorized Data Access

```
Goal: Access user's private data
├── Compromise user credentials
│   ├── Phishing attack
│   ├── Credential stuffing
│   └── Password reset flaw
├── Exploit application vulnerability
│   ├── SQL injection
│   ├── IDOR vulnerability
│   └── XSS to steal session
├── Compromise backend systems
│   ├── Exploit unpatched software
│   └── Social engineering employee
└── Physical access
    └── Stolen laptop with saved credentials
```

---

## Risk Assessment

### Risk Matrix

| | **Low Impact** | **Medium Impact** | **High Impact** | **Critical Impact** |
|---|----------------|-------------------|-----------------|---------------------|
| **High Likelihood** | Medium | High | Critical | Critical |
| **Medium Likelihood** | Low | Medium | High | Critical |
| **Low Likelihood** | Low | Low | Medium | High |

### Prioritized Risks

| Risk | Likelihood | Impact | Risk Level | Priority |
|------|------------|--------|------------|----------|
| _[From STRIDE analysis]_ | | | | |
| | | | | |
| | | | | |

---

## Security Requirements

Based on threats identified, these security requirements must be implemented:

### Authentication & Authorization

- [ ] _[Requirement 1]_
- [ ] _[Requirement 2]_

### Input Validation

- [ ] _[Requirement 1]_
- [ ] _[Requirement 2]_

### Data Protection

- [ ] _[Requirement 1]_
- [ ] _[Requirement 2]_

### Logging & Monitoring

- [ ] _[Requirement 1]_
- [ ] _[Requirement 2]_

---

## Mitigations Summary

| Threat | Mitigation | Owner | Status |
|--------|------------|-------|--------|
| _[Threat]_ | _[How to address]_ | _[Who]_ | _[Done/In Progress/Planned]_ |
| | | | |
| | | | |

---

## Residual Risks

_Risks that remain after mitigations. Must be accepted or addressed later._

| Risk | Reason | Accepted By | Date |
|------|--------|-------------|------|
| _[Remaining risk]_ | _[Why not fully mitigated]_ | _[Name]_ | _[Date]_ |
| | | | |

---

## Review & Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Author | | | |
| Security Reviewer | | | |
| Tech Lead | | | |
| Product Owner | | | |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | | | Initial version |
| | | | |
