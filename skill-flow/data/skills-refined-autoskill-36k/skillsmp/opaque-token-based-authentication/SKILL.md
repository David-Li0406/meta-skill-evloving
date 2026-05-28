---
name: opaque-token-based-authentication
description: Security pattern for server-side token authentication (e.g., session IDs). Use when implementing session management, designing stateful authentication where server maintains token-to-principal mapping, or building systems requiring immediate token revocation. Specialization of Authentication pattern.
---

# Opaque Token-Based Authentication Security Pattern

A subject is authenticated based on a unique, opaque token provided with action requests. The system maintains a mapping of valid tokens to principals. Token secrecy is crucial as it's the sole proof of identity.

## Core Components

| Role | Type | Responsibility |
|------|------|----------------|
| **Subject** | Entity | Provides token with action requests |
| **Enforcer** | Enforcement Point | Ensures token verification before processing |
| **Verifier** | Decision Point | Validates token and retrieves principal |
| **Principal Provider** | Entity | Maintains token-to-principal mapping |
| **Registrar** | Entity | Issues tokens after initial authentication |
| **Token Generator** | Cryptographic Primitive | Generates secure random tokens |

### Data Elements

- **token**: Opaque identifier (no embedded meaning)
- **principal**: Identity associated with token
- **credential factor**: "Something you have"

## Token Characteristics

Opaque tokens:
- Contain no meaningful information themselves
- Require server-side lookup to determine principal
- Must be cryptographically random
- Should be unique across all active sessions

## Token Generation Requirements

### Entropy
- Minimum **64 bits of entropy** to prevent guessing
- Generate tokens of at least **128 bits** using CSPRNG
- Use cryptographically secure pseudo-random number generator

### Secure Generators by Language
- Java: `java.security.SecureRandom`
- Python: `secrets` module
- Node.js: `crypto.randomBytes()`
- .NET: `RNGCryptoServiceProvider`

## Authentication Flow

```
Subject → [action + token] → Enforcer
Enforcer → [token] → Verifier
Verifier → [get_principal(token)] → Principal Provider
Principal Provider → [principal or error] → Verifier
Verifier → [principal or error] → Enforcer
Enforcer → [action + principal] → System (if valid)
```

## Token Registration (Issuance)

1. Subject authenticates via primary method (password, etc.)
2. Registrar requests new token from Principal Provider
3. Token Generator creates secure random token
4. Principal Provider stores token→principal mapping
5. Token returned to Subject

**Important**: Check for duplicate tokens before issuing; regenerate if collision detected.

## Token Lifecycle Management

### Timeout Policies
- **Idle timeout**: Invalidate after period of inactivity
- **Absolute timeout**: Maximum lifetime regardless of activity
- Recommended: Both idle AND absolute timeouts

### Token Invalidation
- On logout: Remove from Principal Provider
- On re-authentication: Invalidate old tokens before issuing new
- On credential change: Invalidate all tokens for that principal

### Lost Tokens
- Cannot be "reset" - Subject must re-authenticate
- No recovery mechanism should exist

## Security Considerations

### Token Secrecy
- Transmit only over HTTPS
- Store securely (HttpOnly, Secure cookies)
- Never log tokens
- Never expose in URLs

### Guessing Prevention
- Sufficient entropy (128+ bits)
- Rate limit token verification attempts
- Monitor for brute-force patterns

### Session Fixation Prevention
- Always issue new token after authentication
- Never accept client-provided tokens as session identifiers

### Token Binding
- Consider binding to client characteristics (IP, user-agent)
- Balance security vs. usability (mobile networks change IPs)

## Common Implementation: Session IDs

Web session identifiers follow this pattern:
- Generated on successful login
- Stored in secure cookie
- Server maintains session store
- Invalidated on logout

## Comparison with Verifiable Tokens

| Aspect | Opaque Token | Verifiable Token |
|--------|--------------|------------------|
| Principal storage | Server-side | In token |
| Revocation | Immediate | Requires strategy |
| Scalability | Requires shared storage | Stateless |
| Token size | Small | Larger |

## Implementation Checklist

- [ ] Using CSPRNG for generation
- [ ] Minimum 128-bit tokens
- [ ] Secure storage (HttpOnly, Secure cookies)
- [ ] HTTPS-only transmission
- [ ] Idle and absolute timeouts
- [ ] New token on authentication
- [ ] Proper invalidation on logout
- [ ] No token logging

## References

- Source: https://securitypatterns.distrinet-research.be/patterns/01_01_004__opaque_token_based_authentication/
- OWASP Session Management Cheat Sheet
