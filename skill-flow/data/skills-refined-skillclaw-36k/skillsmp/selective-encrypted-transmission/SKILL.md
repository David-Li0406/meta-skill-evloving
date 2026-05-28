---
name: selective-encrypted-transmission
description: Security pattern for encrypting specific data before transmission. Use when only certain data elements need encryption, implementing field-level encryption for transit, or when entities must actively manage encryption decisions. Addresses "Leak action request or data in transit" problem.
---

# Selective Encrypted Transmission Security Pattern

Entities actively encrypt specific sensitive data elements before transmitting them over uncontrolled channels. Entities directly interact with cryptographic libraries to encrypt only necessary parts.

## Problem Addressed

**Leak action request or data in transit**: Sensitive data exposed while being transmitted over a channel that may be observed by unauthorized parties.

## Core Components

| Role | Type | Responsibility |
|------|------|----------------|
| **Sender** | Entity | Encrypts and transmits data |
| **Receiver** | Entity | Receives and decrypts data |
| **CryptographerS** | Cryptographic Primitive | Encryption library for Sender |
| **CryptographerR** | Cryptographic Primitive | Decryption library for Receiver |

### Data Elements

- **d**: Plaintext data element
- **{d}_k**: Ciphertext (d encrypted with key k)
- **keyInfoS**: Key information for encryption
- **keyInfoR**: Key information for decryption
- **configS/configR**: Cipher configuration

## Pattern Flow

```
Sender → [encrypt(d, keyInfoS, configS)] → CryptographerS
CryptographerS → [{d}_k] → Sender
Sender → [{d}_k] → Receiver (over channel)
Receiver → [decrypt({d}_k, keyInfoR, configR)] → CryptographerR
CryptographerR → [d] → Receiver
```

1. Sender decides which data to encrypt
2. Sender requests encryption from CryptographerS
3. CryptographerS returns ciphertext
4. Sender transmits ciphertext
5. Receiver receives ciphertext
6. Receiver requests decryption from CryptographerR
7. CryptographerR returns plaintext

## Key Characteristics

### Selective Encryption
- Entities choose WHAT to encrypt
- Not all data needs encryption
- Application-level decision making

### Active Entity Participation
- Entities directly invoke cryptographic operations
- Entities manage when encryption occurs
- Different from channel-level encryption

## Cipher Negotiation

Sender and Receiver must agree on:
- Encryption algorithm
- Configuration (mode, block size)
- Cryptographic key(s)

### Negotiation Timing

| Stage | Approach |
|-------|----------|
| Design time | Hardcoded compatible algorithms |
| Deployment | Configured shared keys/certificates |
| Runtime | Dynamic negotiation protocol |

**Critical**: Use only standardized negotiation protocols from cryptographic libraries. Never implement custom negotiation.

## Security Considerations

### Use Existing Libraries
- Never implement custom cryptography
- Use well-known libraries (OpenSSL, libsodium, etc.)
- Follow library best practices

### Key Management
- Protect key confidentiality
- Protect key integrity
- Secure key exchange/distribution
- See: Cryptographic key management pattern

### Configuration Integrity
- Protect cipher configuration from tampering
- Attacker changing config could weaken encryption
- Protect during transmission and storage

### Public Key Infrastructure
For asymmetric encryption:
- Sender encrypts with Receiver's public key
- Protect public key integrity
- Receiver's private key must remain secret

### Symmetric Key Sharing
For symmetric encryption:
- Both parties need same secret key
- Secure distribution challenge
- Consider key exchange protocols

### Encryption Algorithm Selection
Follow Encryption pattern recommendations:
- Symmetric: AES-256, AES-128 minimum
- Asymmetric: RSA-3072+ or ECDH-256+
- Authenticated encryption preferred

## Comparison with Encrypted Tunnel

| Aspect | Selective Encryption | Encrypted Tunnel |
|--------|---------------------|------------------|
| Scope | Specific data elements | All communication |
| Control | Application decides | Infrastructure manages |
| Overhead | Lower (selective) | Higher (everything) |
| Complexity | Application manages | Delegated to endpoints |

Use selective encryption when:
- Only some data is sensitive
- Different data needs different keys
- Application needs encryption control

## Implementation Checklist

- [ ] Using established cryptographic library
- [ ] Strong algorithm selected (AES-256, RSA-3072+)
- [ ] Secure key management
- [ ] Configuration integrity protected
- [ ] Key exchange secured
- [ ] No custom cryptography implemented
- [ ] Sender/Receiver use compatible ciphers
- [ ] Public keys verified for authenticity

## Related Patterns

- Encryption (underlying cryptographic operations)
- Encrypted tunnel (alternative: encrypt all traffic)
- Cryptographic key management (key handling)
- Selective encrypted storage (encryption at rest)

## References

- Source: https://securitypatterns.distrinet-research.be/patterns/06_01_001__selective_encrypted_transmission/
- BSI TR-02102 Cryptographic Mechanisms
- NIST SP 800-175B Cryptographic Standards
