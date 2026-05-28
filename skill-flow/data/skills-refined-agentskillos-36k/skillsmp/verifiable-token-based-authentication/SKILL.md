---
name: verifiable-token-based-authentication
description: Security pattern for self-contained token authentication (e.g., JWT). Use when implementing stateless authentication, designing tokens with embedded claims, or building systems where tokens contain principal information and can be verified without server-side storage. Specialization of Authentication pattern.
---

# Verifiable Token-Based Authentication Security Pattern

A subject is authenticated using a token that itself contains the necessary information to determine the principal. The system verifies the token is valid (not tampered, not expired) without needing to look up stored evidence.

## Core Components

| Role | Type | Responsibility |
|------|------|----------------|
| **Subject** | Entity | Provides token with action requests |
| **Enforcer** | Enforcement Point | Ensures token verification before processing |
| **Verifier** | Decision Point | Manages token validity verification |
| **Cryptographer** | Cryptographic Primitive | Verifies token integrity |
| **Key Manager** | Entity | Manages cryptographic keys |
| **Registrar** | Entity | Issues tokens after initial authentication |

### Data Elements

- **token**: Self-contained credential with principal and metadata
- **principal**: Identity extracted from valid token
- **expiration**: Token validity period
- **signature/MAC**: Cryptographic integrity protection

## Token Structure

A verifiable token must contain:
1. **Principal identifier** (username, user ID, email)
2. **Expiration date/time**
3. **Cryptographic signature or MAC**
4. **Optional**: Additional claims (roles, permissions, metadata)

## Token Integrity Verification

Two approaches:

### Digital Signature (Asymmetric)
- Token signed with private key
- Verified with public key
- Enables verification without sharing signing key
- Use RSA (min 2048 bits) or ECDSA (min 256 bits)

### MAC (Symmetric)
- Token authenticated with shared secret
- Same key for creation and verification
- Use HMAC with min 128-bit keys

**Recommendation**: Use cryptographic keys with at least 128 bits of entropy.

## Verification Flow

```
Subject → [action + token] → Enforcer
Enforcer → [token] → Verifier
Verifier → [get key] → Key Manager
Key Manager → [key] → Verifier
Verifier → [verify integrity] → Cryptographer
Cryptographer → [result] → Verifier
Verifier → [check expiration, extract principal] → Verifier
Verifier → [principal or error] → Enforcer
```

Verification steps:
1. Verify integrity (signature/MAC)
2. Check expiration date
3. Check revocation status (if implemented)
4. Extract and return principal

## Token Registration (Issuance)

1. Subject authenticates via other means (e.g., password)
2. Registrar generates token with:
   - Principal identifier
   - Expiration date
   - Additional claims
   - Cryptographic signature/MAC
3. Token returned to Subject

## Security Considerations

### Token Lifetime
- Shorter = more secure, less convenient
- Include absolute expiration
- Consider refresh token pattern for long sessions

### Token Revocation
- Stateless tokens cannot be directly revoked
- Options: short lifetimes, revocation lists, token versioning

### Token Storage (Client-Side)
- Web: HttpOnly, Secure cookies or secure storage
- Mobile: Secure enclave/keychain
- Never store in localStorage for sensitive apps

### Token Transmission
- Always use HTTPS
- Consider token binding

### No Token Reset
- Tokens should never be reset on request
- Subject must re-authenticate for new token

### Integrity is Paramount
- Never accept tampered tokens
- Verify signature before trusting any claims

## Common Implementation: JWT

JSON Web Tokens follow this pattern:
- Header: algorithm, type
- Payload: claims (principal, exp, iat, etc.)
- Signature: cryptographic verification

**Warning**: Always verify signature; never use "none" algorithm.

## Implementation Checklist

- [ ] Strong signing algorithm (RS256, ES256, HS256)
- [ ] Expiration claim enforced
- [ ] Signature verified before trusting claims
- [ ] Keys managed securely
- [ ] Transmission over HTTPS only
- [ ] Appropriate token lifetime
- [ ] Revocation strategy defined

## References

- Source: https://securitypatterns.distrinet-research.be/patterns/01_01_003__verifiable_token_based_authentication/
- RFC 7519 (JWT)
- OWASP JWT Cheat Sheet
