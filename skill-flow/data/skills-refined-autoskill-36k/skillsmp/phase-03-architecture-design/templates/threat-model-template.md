# Threat Model Document Template

**Document ID:** P3-THREAT-{XXX}  
  
**Status:** Draft | In Review | Approved  
**Author:** {Security Lead}  
**Classification:** Confidential  
**Traceability:** Links to P3-ARCH-{XXX}, P3-SEC-{XXX}

---

## 1. Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | {Date} | {Author} | Initial threat model |

---

## 2. Scope

### 2.1 System Overview
{Brief description of the system being threat modeled}

### 2.2 Scope Boundaries

| In Scope | Out of Scope |
|----------|--------------|
| {Component/Feature} | {Component/Feature} |

### 2.3 Assumptions
- {Assumption 1}
- {Assumption 2}

---

## 3. Data Flow Diagram

### 3.1 Level 0 (Context)

```
                    ┌─────────────────┐
     ┌─────────┐    │                 │    ┌─────────┐
     │  User   │───►│    SYSTEM       │───►│ External│
     │         │◄───│                 │◄───│ Service │
     └─────────┘    │                 │    └─────────┘
                    └─────────────────┘
```

### 3.2 Level 1 (System)

```
┌─────────────────────────────────────────────────────────────────┐
│                          SYSTEM                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  (1)─────►┌──────────┐(2)────►┌──────────┐(3)────►┌──────────┐ │
│   User    │   Web    │ API    │   App    │ Query  │ Database │ │
│   Input   │  Server  │────────│  Server  │────────│          │ │
│           └──────────┘        └──────────┘        └──────────┘ │
│                                    │                           │
│                                    │(4)                        │
│                                    ▼                           │
│                              ┌──────────┐                      │
│                              │ External │                      │
│                              │   API    │                      │
│                              └──────────┘                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 Trust Boundaries

| Boundary | Components | Trust Level |
|----------|------------|-------------|
| TB-1 | Internet ↔ Web Server | Untrusted → DMZ |
| TB-2 | Web Server ↔ App Server | DMZ → Internal |
| TB-3 | App Server ↔ Database | Internal → Data |
| TB-4 | App Server ↔ External API | Internal → External |

---

## 4. Asset Inventory

| Asset ID | Asset Name | Classification | Value | Location |
|----------|------------|----------------|-------|----------|
| A-001 | User Credentials | Restricted | Critical | Database |
| A-002 | Customer PII | Confidential | High | Database |
| A-003 | Payment Tokens | Restricted | Critical | Payment Service |
| A-004 | Session Tokens | Confidential | High | Memory |
| A-005 | API Keys | Restricted | Critical | Secrets Manager |
| A-006 | Application Code | Internal | Medium | Git Repository |
| A-007 | Audit Logs | Confidential | High | Log Storage |

---

## 5. Threat Identification (STRIDE)

### 5.1 Spoofing Threats

| ID | Threat | Component | Attack Vector | Likelihood | Impact |
|----|--------|-----------|---------------|------------|--------|
| S-001 | Credential theft | Auth System | Phishing, credential stuffing | High | Critical |
| S-002 | Session hijacking | Web App | XSS, token theft | Medium | High |
| S-003 | API key compromise | App Server | Code exposure, logs | Medium | Critical |

### 5.2 Tampering Threats

| ID | Threat | Component | Attack Vector | Likelihood | Impact |
|----|--------|-----------|---------------|------------|--------|
| T-001 | SQL injection | Database | User input fields | Medium | Critical |
| T-002 | Request tampering | API | Proxy interception | Low | Medium |
| T-003 | Log manipulation | Logging | Compromised server | Low | High |

### 5.3 Repudiation Threats

| ID | Threat | Component | Attack Vector | Likelihood | Impact |
|----|--------|-----------|---------------|------------|--------|
| R-001 | Denial of transactions | Payment | Missing audit logs | Low | High |
| R-002 | Admin action denial | Admin Panel | Insufficient logging | Medium | Medium |

### 5.4 Information Disclosure Threats

| ID | Threat | Component | Attack Vector | Likelihood | Impact |
|----|--------|-----------|---------------|------------|--------|
| I-001 | Data breach | Database | SQL injection, misconfiguration | Medium | Critical |
| I-002 | Error message leakage | API | Verbose error responses | High | Medium |
| I-003 | Memory dump exposure | App Server | Crash dump analysis | Low | High |

### 5.5 Denial of Service Threats

| ID | Threat | Component | Attack Vector | Likelihood | Impact |
|----|--------|-----------|---------------|------------|--------|
| D-001 | DDoS attack | Web Server | Volumetric attack | High | High |
| D-002 | Resource exhaustion | App Server | Algorithmic complexity | Medium | High |
| D-003 | Database lock | Database | Transaction flooding | Low | Critical |

### 5.6 Elevation of Privilege Threats

| ID | Threat | Component | Attack Vector | Likelihood | Impact |
|----|--------|-----------|---------------|------------|--------|
| E-001 | IDOR vulnerability | API | Parameter manipulation | Medium | High |
| E-002 | Role escalation | Auth System | Business logic flaw | Low | Critical |
| E-003 | Container escape | Infrastructure | Kernel vulnerability | Low | Critical |

---

## 6. Attack Trees

### 6.1 Attack Tree: Data Breach

```
                    ┌───────────────────┐
                    │   DATA BREACH     │
                    └─────────┬─────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ SQL Injection │   │  Credential   │   │  Insider      │
│               │   │    Theft      │   │   Threat      │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
   ┌────┴────┐         ┌────┴────┐         ┌────┴────┐
   │         │         │         │         │         │
   ▼         ▼         ▼         ▼         ▼         ▼
┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
│Input│  │Blind│  │Phish│  │Brute│  │Data │  │Priv │
│Field│  │SQLi │  │ ing │  │Force│  │Copy │  │Abuse│
└─────┘  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘
```

---

## 7. Risk Assessment

### 7.1 Risk Matrix

|              | **Minimal** | **Minor** | **Moderate** | **Significant** | **Severe** |
|--------------|-------------|-----------|--------------|-----------------|------------|
| **Almost Certain** | Medium | High | High | Critical | Critical |
| **Likely** | Low | Medium | High | High | Critical |
| **Possible** | Low | Medium | Medium | High | High |
| **Unlikely** | Low | Low | Medium | Medium | High |
| **Rare** | Low | Low | Low | Medium | Medium |

### 7.2 Threat Risk Ratings

| Threat ID | Threat | Likelihood | Impact | Risk Level | Priority |
|-----------|--------|------------|--------|------------|----------|
| S-001 | Credential theft | Likely | Severe | Critical | 1 |
| I-001 | Data breach | Possible | Severe | High | 2 |
| D-001 | DDoS attack | Likely | Significant | High | 3 |
| T-001 | SQL injection | Possible | Severe | High | 4 |
| E-001 | IDOR vulnerability | Possible | Significant | High | 5 |

---

## 8. Mitigations

### 8.1 Mitigation Strategies

| Threat ID | Mitigation | Control Type | Status | Owner |
|-----------|------------|--------------|--------|-------|
| S-001 | MFA implementation | Preventive | Planned | Security |
| S-001 | Credential monitoring | Detective | Implemented | Security |
| I-001 | Encryption at rest | Preventive | Implemented | Data |
| I-001 | WAF deployment | Preventive | Implemented | Ops |
| D-001 | DDoS protection | Preventive | Implemented | Ops |
| D-001 | Rate limiting | Preventive | Implemented | Dev |
| T-001 | Parameterized queries | Preventive | Implemented | Dev |
| T-001 | Input validation | Preventive | In Progress | Dev |
| E-001 | Authorization checks | Preventive | In Progress | Dev |

### 8.2 Mitigation Details

#### M-001: MFA Implementation

**Threat Addressed:** S-001 (Credential theft)

**Description:** Implement multi-factor authentication for all user accounts

**Implementation:**
- TOTP-based authenticator apps
- WebAuthn/FIDO2 for passwordless
- SMS as fallback only

**Residual Risk:** Low (phishing-resistant MFA reduces risk significantly)

---

## 9. Security Requirements

| Req ID | Requirement | Source Threat | Priority |
|--------|-------------|---------------|----------|
| SEC-001 | All user authentication must support MFA | S-001 | Must |
| SEC-002 | All database queries must use parameterized statements | T-001 | Must |
| SEC-003 | API rate limiting: 100 requests/minute per user | D-001 | Must |
| SEC-004 | All PII must be encrypted at rest using AES-256 | I-001 | Must |
| SEC-005 | Session tokens expire after 15 minutes of inactivity | S-002 | Must |

---

## 10. Review and Sign-off

| Role | Name | Sign-off Date | Notes |
|------|------|---------------|-------|
| Security Architect | | | |
| Technical Lead | | | |
| Product Owner | | | |
| Risk Manager | | | |

---

## 11. Appendices

### Appendix A: Threat Modeling Methodology

This threat model uses the STRIDE methodology:
- **S**poofing
- **T**ampering
- **R**epudiation
- **I**nformation Disclosure
- **D**enial of Service
- **E**levation of Privilege

### Appendix B: References

- OWASP Threat Modeling: https://owasp.org/www-community/Threat_Modeling
- Microsoft STRIDE: https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats
- NIST SP 800-30: Risk Assessment Guide

---

**Document End**

---

**Version 1.0.0 | OCTALUME Enterprise Lifecycle Framework**
