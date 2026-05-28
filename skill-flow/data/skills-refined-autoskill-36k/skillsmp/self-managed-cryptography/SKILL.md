---
name: self-managed-cryptography
description: Security pattern for systems that manage cryptographic keys themselves rather than delegating to an external service. Use when the application must store, retrieve, and manage cryptographic keys directly. Implementation of Cryptographic Key Management pattern. Covers key storage security, key derivation from passwords, limiting key exposure, and protecting key confidentiality and integrity throughout the lifecycle.
---

# Self-Managed Cryptography Security Pattern

In this pattern, the system itself manages the cryptographic keys, including storage and retrieval when necessary. The system is responsible for ensuring the confidentiality and integrity of cryptographic keys throughout their lifetime.

## Key Responsibilities

When using self-managed cryptography, the system must handle:
- **Key storage** - Secure persistent storage of keys
- **Key retrieval** - Secure access to stored keys when needed
- **Key distribution** - Secure transmission of keys when required
- **Key revocation** - Proper invalidation and destruction of keys

## Core Components

| Role | Type | Responsibility |
|------|------|----------------|
| **Application** | Entity | Interacts with cryptographic library and manages keys |
| **Cryptographer** | Cryptographic Primitive | Library performing cryptographic operations |
| **Key Storage** | Storage | Persistently stores cryptographic key material |

**Note:** The Application inherits the Entity role from the parent Cryptographic Key Management pattern.

### Data Elements

- **keyConf**: Configuration for key generation (e.g., key length) - optional
- **key**: The actual cryptographic key material used by the Cryptographer
- **id**: Identifier used to store and retrieve keys from Key Storage
- **input**: Data on which cryptographic operation should be performed
- **output**: Result of the cryptographic operation
- **config**: Configuration for the cryptographic operation - optional

### Actions

- **generate_key**: Generate new cryptographic key according to configuration
- **store_key**: Store the cryptographic key under given identifier in Key Storage
- **get_key**: Retrieve key information from Key Storage
- **crypto_action**: Perform cryptographic operation (encrypt, sign, etc.)

## Pattern Flow

### Key Generation and Storage
```
Application → [generate_key(keyConf)] → Cryptographer
Cryptographer → [key] → Application
Application → [store_key(id, key)] → Key Storage
```

The Application requests key generation from the Cryptographer, then stores the returned key in Key Storage with a chosen identifier.

### Key Retrieval and Use
```
Application → [get_key(id)] → Key Storage
Key Storage → [key] → Application
Application → [crypto_action(input, key, config)] → Cryptographer
Cryptographer → [output] → Application
```

To use a stored key, the Application retrieves it from Key Storage, then provides it to the Cryptographer along with the input data.

## Key Difference from Cryptography as a Service

| Aspect | Self-Managed Cryptography | Cryptography as a Service |
|--------|---------------------------|---------------------------|
| Key possession | Application holds actual key material | System holds only key identifiers |
| Key storage | Managed by application | Managed by external service |
| Key exposure risk | Higher (keys in application memory) | Lower (keys never exposed) |
| Control | Full control over keys | Dependent on service provider |
| Responsibility | Full responsibility for key security | Shared with service provider |

## Critical Security Considerations

### Key Generation

**Never implement custom key generation algorithms.**

Generating good (random and unpredictable) cryptographic keys is complex. Always use the appropriate functions offered by the cryptographic library.

### Key Derivation from Passwords

When deriving keys from user-provided passwords:
- **Always use a suitable key derivation function (KDF)**
- Use functions from the chosen cryptographic library
- **Never devise custom key derivation algorithms**

**Recommended KDFs:**
| Function | Notes |
|----------|-------|
| **Argon2** | Modern, recommended for new applications |
| **scrypt** | Memory-hard, good alternative |
| **PBKDF2** | Use if FIPS-140 compliance is required |

Verify that your cryptographic library uses up-to-date key derivation functions.

### Key Storage Security

The Key Storage must protect cryptographic keys throughout their lifecycle:

**Platform Security Features (Preferred):**
- Take advantage of OS and hardware security features when possible
- Store keys in cryptographic modules (HSM, TPM) when available

**When Platform Features Unavailable:**
- Limit physical access to storage medium (protected area)
- Implement logical access controls (authentication, authorization)

**Key Integrity Verification:**
- Use MACs or digital signatures computed from the key
- Periodically verify integrity of all stored keys

**Key Recovery:**
- Maintain key copies in physically separate locations
- Enables restoration after unauthorized modifications

### Key Confidentiality and Integrity in Transit

Both integrity and confidentiality of keys must be protected:
- During transmission between entities
- At rest in Key Storage

**Exception:** Confidentiality can be relaxed for public keys only (e.g., when verifying digital signatures).

### Key Identifier (id) Protection

The identifier determines which key is used for cryptographic actions.

**Risk:** An attacker who can tamper with the id (e.g., change it to match a known key) can negate all security guarantees.

**Required Protections:**
- Protect id from tampering during transmission over uncontrolled channels
- Protect id from tampering when stored by Application

### Limiting Key Exposure

Since the Application processes actual cryptographic keys, minimize exposure:

| Practice | Description |
|----------|-------------|
| **Minimize time in memory** | Load keys only when needed, clear immediately after |
| **Zeroize memory** | Overwrite key material before freeing memory |
| **Avoid logging** | Never log key material |
| **Limit copies** | Minimize the number of key copies in memory |
| **Secure memory** | Use secure memory allocation when available |

## Implementation Checklist

- [ ] Key generation uses cryptographic library functions (no custom algorithms)
- [ ] Password-derived keys use proper KDF (Argon2, scrypt, or PBKDF2)
- [ ] Key Storage protects confidentiality and integrity
- [ ] Platform security features utilized where available
- [ ] Physical and logical access to storage restricted
- [ ] Key integrity verified periodically (MACs/signatures)
- [ ] Key backups maintained in separate locations
- [ ] Keys protected during transmission
- [ ] Key identifiers protected from tampering
- [ ] Key exposure minimized (memory cleared after use)
- [ ] Public key exception applied only where appropriate

## When to Choose Self-Managed vs. As-a-Service

**Choose Self-Managed Cryptography when:**
- Full control over keys is required
- Offline operation is necessary
- Regulatory requirements mandate key custody
- Integration with external KMS is not feasible

**Choose Cryptography as a Service when:**
- Reducing key exposure risk is priority
- External expertise in key management is desired
- Cloud-native deployment is standard
- Audit and compliance features are needed out-of-box

## Related Patterns

- **Cryptographic Key Management** (parent pattern)
- **Cryptography as a Service** (alternative implementation)
- **Cryptographic Action** (uses keys managed by this pattern)
- **Encryption** (specific cryptographic action)
- **Digital Signature** (specific cryptographic action)
- **Message Authentication Code** (specific cryptographic action)

## References

- Source: https://securitypatterns.distrinet-research.be/patterns/99_02_003__crypto_self_managed/
- E. Barker, 'Recommendation for Key Management: Part 1 – General', NIST SP 800-57 Part 1, May 2020
- OWASP, 'OWASP Top 10:2021 - A02: Cryptographic Failures'
- P. C. van Oorschot, Computer Security and the Internet - Tools and Jewels, 2020
- NIST SP 800-130, 'A Framework for Designing Cryptographic Key Management Systems'
