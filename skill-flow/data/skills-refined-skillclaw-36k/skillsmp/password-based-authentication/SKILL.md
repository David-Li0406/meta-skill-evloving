---
name: password-based-authentication
description: Security pattern for implementing password-based authentication. Use when designing login systems with username/password, implementing password storage, hashing, salting, peppering, password policies, or password reset flows. Specialization of the Authentication pattern.
---

# Password-Based Authentication Security Pattern

A subject proves identity by providing a correct identifier (username/email) and corresponding password. Relies on the assumption that only the actual owner knows the correct password.

## Core Components

| Role | Type | Responsibility |
|------|------|----------------|
| **Subject** | Entity | Provides identifier and password |
| **Enforcer** | Enforcement Point | Ensures authentication before action processing |
| **Verification Manager** | Entity | Collects inputs for password verification |
| **Comparator** | Decision Point | Compares hash values |
| **Hasher** | Cryptographic Primitive | Calculates hash values |
| **Password Store** | Storage | Keeps hash values for registered identities |
| **Registrar** | Entity | Handles subject registration |
| **Resetter** | Entity | Handles credential reset |
| **Password Policy** | Information Point | Rules passwords must satisfy |
| **SRNG** | Cryptographic Primitive | Secure random number generator |

### Data Elements

- **id**: Identifier (username, email)
- **pwd**: Password provided by Subject
- **hash(pwd)**: Hash value of password
- **salt**: Random value unique per Subject
- **pepper**: System-wide secret for additional protection

## Password Hashing

### Required Approach
1. Use modern password hashing algorithms: **Argon2**, **scrypt**, **bcrypt**, or **PBKDF2**
2. Never use general-purpose hash functions (MD5, SHA-1, SHA-256) alone
3. Always use salting (typically automatic with modern algorithms)

### Salting
- Add random string unique per Subject before hashing
- Ensures identical passwords produce different hashes
- Salt stored in plaintext alongside hash
- Modern algorithms handle salt automatically

### Peppering (Optional)
- System-wide secret added before hashing
- Stored separately from password store
- Provides additional protection if password store is compromised

## Registration Flow

Three approaches for credential determination:
1. Subject provides identifier and password
2. Subject provides identifier; Registrar selects password
3. Registrar selects both identifier and password

Upon completion:
- Password Store contains: identifier, hash(salted password), salt
- Subject possesses: identifier and password

## Password Policy

Enforce policies including:
- Minimum/maximum length
- Character requirements
- Common password blacklist
- Breach database checking

## Password Reset

1. Verify Subject identity through out-of-band channel
2. Generate time-limited reset token
3. Never reveal whether account exists
4. Invalidate existing sessions after reset
5. Force re-authentication

## Security Considerations

### Password Store Protection
- Encrypt at rest
- Restrict access
- Monitor for breaches
- Detect tampering

### Identifier Security
- Don't rely on identifier secrecy
- Prevent enumeration attacks
- Use consistent timing for valid/invalid identifiers

### Verification Timing
- Use constant-time comparison
- Prevent timing attacks

## Implementation Checklist

- [ ] Using Argon2/scrypt/bcrypt/PBKDF2
- [ ] Automatic salting enabled
- [ ] Password policy enforced
- [ ] Secure reset flow implemented
- [ ] Rate limiting on login attempts
- [ ] Constant-time hash comparison
- [ ] No credential logging

## References

- Source: https://securitypatterns.distrinet-research.be/patterns/01_01_002__authentication_pwd/
- OWASP Password Storage Cheat Sheet
