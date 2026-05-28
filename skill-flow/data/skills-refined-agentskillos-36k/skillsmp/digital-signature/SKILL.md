---
name: digital-signature
description: Security pattern for implementing digital signatures. Use when implementing document signing, code signing, certificate signing, non-repudiation, or verifying authenticity and integrity of messages using asymmetric cryptography (RSA, ECDSA, Ed25519).
---

# Digital Signature Security Pattern

Create and verify digital signatures to ensure data integrity, authenticity, and non-repudiation using asymmetric cryptography.

## Properties Provided

1. **Data Integrity**: Message not modified since signing
2. **Authentication**: Message originated from key holder
3. **Non-repudiation**: Signer cannot deny having signed

## Core Components

| Role | Type | Responsibility |
|------|------|----------------|
| **EntityA** | Entity | Creates digital signatures |
| **EntityB** | Entity | Verifies digital signatures |
| **Signature Generator** | Cryptographic Primitive | Creates signatures |
| **Signature Verifier** | Cryptographic Primitive | Verifies signatures |

### Data Elements

- **message**: Data to be signed
- **signature**: Digital signature of message
- **private_key**: Signing key (secret)
- **public_key**: Verification key (can be distributed)

## Signature Flow

### Signing
```
EntityA → [sign(message, private_key)] → Signature Generator
Signature Generator → [signature] → EntityA
EntityA → [message + signature] → EntityB
```

### Verification
```
EntityB → [verify(message, signature, public_key)] → Signature Verifier
Signature Verifier → [valid/invalid] → EntityB
```

## Comparison with MAC

| Aspect | Digital Signature | MAC |
|--------|------------------|-----|
| Key type | Asymmetric (public/private) | Symmetric (shared) |
| Non-repudiation | Yes | No |
| Verification key | Public (distributable) | Secret (shared) |
| Performance | Slower | Faster |
| Use case | External parties, legal | Internal, performance |

**Use digital signatures** when non-repudiation required or verifiers shouldn't be able to create signatures.

## Algorithm Recommendations

### RSA Signatures

| Variant | Status | Notes |
|---------|--------|-------|
| **RSA-PSS** | Recommended | Probabilistic padding |
| RSA-PKCS#1 v1.5 | Acceptable | Deterministic, widely supported |

Key sizes:
- **3072 bits**: Recommended for long-term
- **2048 bits**: Minimum acceptable
- **4096 bits**: High security requirements
- **15360 bits**: 30+ year protection (if needed)

### Elliptic Curve Signatures

| Algorithm | Curve | Status |
|-----------|-------|--------|
| **Ed25519** | Curve25519 | Recommended (modern) |
| **ECDSA** | P-256 | Recommended |
| ECDSA | P-384 | High security |
| ECDSA | P-521 | Highest security |

Key sizes:
- **256 bits**: Standard security (≈RSA 3072)
- **384 bits**: High security
- **512 bits**: Long-term protection

### Hash Functions for Signing
- **SHA-256**: Standard
- **SHA-384/SHA-512**: Higher security
- **SHA-3**: Alternative

**Never**: MD5, SHA-1

## Security Considerations

### Private Key Protection
**Critical**: Private key security = signature trustworthiness

- Store in HSM for high-value keys
- Use secure key storage APIs
- Never expose in logs or errors
- Implement access controls
- Consider key ceremonies for critical keys

### Public Key Authenticity
Verifier must trust public key belongs to signer:
- Certificate from trusted CA
- Out-of-band verification
- Web of trust
- Key pinning

### Algorithm Selection
- Use current recommendations
- Plan for algorithm transitions
- Avoid deprecated algorithms

### Timestamp Considerations
- Include timestamp in signed data
- Consider timestamping service
- Prevents backdating

### Message Hashing
Typically, signature is over hash of message:
1. Hash the message (SHA-256)
2. Sign the hash

Library usually handles this—verify behavior.

### Signature Malleability
Some signature schemes are malleable (valid signature can be modified to create another valid signature). Use signature schemes that prevent malleability or handle at application layer.

## Common Use Cases

### Code Signing
- Sign software/updates
- Verify before installation
- Protect against tampering

### Document Signing
- Legal documents
- Contracts
- Non-repudiation

### Certificate Signing
- X.509 certificates
- CA hierarchy
- TLS/HTTPS

### JWT Signing
- Token integrity
- RS256 (RSA), ES256 (ECDSA)
- Verify before trusting claims

### API Request Signing
- Request authenticity
- Webhook verification
- Prevents tampering

## Implementation Checklist

- [ ] Using RSA-PSS, Ed25519, or ECDSA
- [ ] Key size ≥ 3072 bits (RSA) or ≥ 256 bits (ECC)
- [ ] Private key stored securely
- [ ] Public key authenticity established
- [ ] SHA-256+ for hashing
- [ ] No MD5 or SHA-1
- [ ] Verification before trusting signed data
- [ ] Algorithm agility for future changes

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Weak key size | Forgery possible | Use recommended sizes |
| MD5/SHA-1 | Collision attacks | Use SHA-256+ |
| Private key exposure | Full compromise | Secure storage (HSM) |
| Skipping verification | Accept forged data | Always verify |
| Trusting unverified public key | Accept attacker's signature | Establish key authenticity |

## Related Patterns

- Cryptographic action (parent pattern)
- Message authentication code (symmetric alternative)
- Cryptographic key management (key handling)
- Verifiable token-based authentication (JWT use case)

## References

- Source: https://securitypatterns.distrinet-research.be/patterns/99_01_003__digital_signature/
- NIST FIPS 186-5 Digital Signature Standard
- RFC 8017 (PKCS#1 RSA)
