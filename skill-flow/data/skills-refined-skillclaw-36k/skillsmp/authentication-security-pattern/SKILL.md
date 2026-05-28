---
name: authentication-security-pattern
description: Security pattern for implementing authentication in software systems. Use when designing or reviewing authentication mechanisms, implementing login systems, verifying user identity, protecting system access, or addressing OWASP authentication flaws. Provides guidance on enforcers, verifiers, evidence providers, subject registration, credential management, and security considerations.
---

# Authentication Security Pattern

Authentication verifies that a subject (user, service, device) is who they claim to be before allowing system access. This pattern is a prerequisite for authorization and auditing.

## Core Components

### Roles

| Role | Type | Responsibility |
|------|------|----------------|
| **Subject** | Entity | Requests actions from the system |
| **Enforcer** | Enforcement Point | Intercepts requests; ensures authentication before processing. Must be incorporated into the system |
| **Verifier** | Decision Point | Validates credentials against evidence to determine authentication success |
| **Evidence Provider** | Entity | Stores/provides evidence for credential verification (internal or external) |

### Data Elements

- **credential**: Proof of identity provided by Subject
- **evidence**: Data used by Verifier to validate credentials
- **principal**: Authenticated identity established after successful verification
- **action**: The operation Subject wants to perform

## Authentication Flow

```
Subject → [action + credential] → Enforcer
Enforcer → [credential] → Verifier
Verifier → [request evidence] → Evidence Provider
Evidence Provider → [evidence] → Verifier
Verifier → [principal or error] → Enforcer
Enforcer → [action + principal] → System (if authenticated)
         → [error] → Subject (if failed)
```

1. Subject requests action with credential
2. Enforcer intercepts and forwards credential to Verifier
3. Verifier requests evidence from Evidence Provider
4. Verifier compares credential against evidence
5. On success: Enforcer forwards action + principal to System
6. On failure: Subject receives authentication error

## Subject Registration

Registration establishes the credential/evidence pair. Three approaches:

1. **Subject-provided**: Subject chooses both identifier and credential
2. **Hybrid**: Subject provides identifier; system generates credential
3. **System-assigned**: System generates both identifier and credential

Key requirements:
- Verify Subject actually owns the claimed identity (e.g., email verification)
- Protect credential transmission during registration
- Consider secure channels for initial credential delivery

## Credential and Evidence Selection

Credential factors:
- **Something you know**: passwords, PINs
- **Something you have**: tokens, keys, devices
- **Something you are**: biometrics

Evidence guidelines:
- Never store credentials directly; use derived evidence (e.g., hashed passwords)
- Evidence leakage should not directly reveal credentials
- Protect evidence integrity to prevent tampering

## Security Considerations

### Enforcer Placement
- Must be impossible to bypass
- Place at system boundary where all requests enter
- Consider defense in depth with multiple enforcement points

### Evidence Protection
- Encrypt evidence at rest
- Implement integrity checks to detect tampering
- Limit access to Evidence Provider

### Rate Limiting
Prevent brute-force attacks:
- Limit authentication attempts per time window
- Implement exponential backoff
- Consider account lockout policies
- Protect against DoS on authentication endpoints

### Credential Change
- Require current credential verification before changes
- Force re-authentication after credential updates
- Invalidate active sessions on credential change

### Credential Reset
- Use out-of-band verification (email, SMS)
- Time-limit reset tokens
- Never expose whether an account exists

### Logging
- Log authentication attempts (success and failure)
- Never log credentials
- Include timestamps and source identifiers

## Related Patterns

- **Password-based authentication**: Uses identifier + password as credential
- **Opaque token-based authentication**: Uses system-issued tokens (e.g., session IDs)
- **Verifiable token-based authentication**: Uses self-contained tokens (e.g., JWTs)
- **Multi-factor authentication**: Combines multiple credential factors
- **Session-based access control**: Combines opaque tokens with authorization

## Common Vulnerabilities (OWASP/IEEE Top 10)

- Broken authentication mechanisms
- Credential stuffing susceptibility
- Weak credential policies
- Missing rate limiting
- Insecure credential storage
- Session fixation
- Bypassing authentication checks

## Implementation Checklist

- [ ] Enforcer intercepts ALL entry points
- [ ] Credentials never stored in plaintext
- [ ] Evidence protected at rest and in transit
- [ ] Rate limiting implemented
- [ ] Failed attempts logged (without credentials)
- [ ] Secure credential reset flow
- [ ] Session invalidation on credential change
- [ ] Identity verification during registration

## References

- Source: [Security Pattern Catalogue - DistriNet Research](https://securitypatterns.distrinet-research.be/patterns/01_01_001__authentication/)
- OWASP Authentication Cheat Sheet
- IEEE Top 10 Security Flaws
