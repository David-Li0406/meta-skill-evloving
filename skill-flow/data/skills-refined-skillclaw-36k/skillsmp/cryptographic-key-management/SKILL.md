---
name: cryptographic-key-management
description: Security pattern for managing cryptographic keys throughout their lifecycle. Use when integrating cryptography requiring key generation, storage, distribution, or usage. Provides guidance on key confidentiality, integrity, configuration protection, and key information handling. Foundation for Cryptography as a service and Self-managed cryptography patterns.
---

# Cryptographic Key Management Security Pattern

When integrating cryptographic primitives into a system, correctly managing cryptographic keys is a crucial aspect. This pattern encapsulates common issues when applying solutions involving cryptography.

## Importance

**Proper key management is one of the most crucial aspects when applying cryptography.**

Any security guarantees provided by a cryptosystem can be nullified if an attacker can obtain or tamper with the used cryptographic key(s).

**Example**: An attacker that obtains a supposedly secret session key will be able to decrypt all messages encrypted with that key.

## Key Security Requirements

In most circumstances, cryptographic keys should be:
1. **Kept confidential** throughout their lifecycle
2. **Have their integrity protected** throughout their lifecycle

**Exception**: For some types of keys, such as the **public key** in an asymmetric key pair, the confidentiality requirement can be relaxed (but integrity must still be protected).

## Core Components

| Role | Type | Responsibility |
|------|------|----------------|
| **Entity** | Entity | Wants to generate and use cryptographic keys |
| **Cryptographer** | Cryptographic Primitive | Library generating keys and performing cryptographic actions |

### Data Elements

- **keyConf**: Configuration for key generation (e.g., symmetric/asymmetric, key length) - optional
- **keyInfo**: Information on the key to use (identifier or key material itself, depending on implementation)
- **input**: Plaintext input for cryptographic action
- **output**: Result of cryptographic action (e.g., ciphertext, signature)
- **config**: Configuration for Cryptographer (e.g., cipher mode) - optional

### Actions

- **generate_key**: Generate new cryptographic key according to configuration
- **crypto_action**: Perform cryptographic action (e.g., encrypt, sign) using identified key

## Pattern Flow

### Key Generation
```
Entity → [generate_key(keyConf)] → Cryptographer
Cryptographer → [keyInfo] → Entity
```

The Entity requests key generation with optional configuration. The Cryptographer generates the key and returns information needed to use it in future requests.

### Cryptographic Action
```
Entity → [crypto_action(input, keyInfo, config)] → Cryptographer
Cryptographer → [output] → Entity
```

To use a previously generated key, Entity provides keyInfo received during generation along with input data and optional configuration.

## Security Considerations

### Key Configuration Protection (keyConf)

If key configuration is provided, it should be **protected from undetected tampering**:
- During transmission over uncontrolled channels
- During persistent storage by Entity

**Risk Example**: An attacker may change key configuration to generate a shorter key than advised, making ciphertexts easier to break.

### Key Information Protection (keyInfo)

After generating a key, Entity receives keyInfo which it will process and use in further interactions.

- **Protect against unauthorized tampering** during transmission and storage
- An attacker that can influence keyInfo might change the key used to one under their control
- **Example**: Attacker tampers with keyInfo so encryption uses a key the attacker knows, allowing decryption

The exact information and necessary security measures depend on the chosen implementation pattern.

### Configuration Protection (config)

If Entity provides action configuration to Cryptographer:
- Protect against undetected tampering during transmission and storage
- Attacker might change config to use insecure, deprecated ciphers

## Implementation Patterns

This pattern has two main implementations:

### 1. Cryptography as a Service
- Delegate key management to external service (e.g., KMS, HSM)
- System never possesses cryptographic keys directly
- Only stores key identifiers
- Reduces risk of key leakage
- Examples: AWS KMS, Azure Key Vault, Google Cloud KMS, Android Keystore

### 2. Self-Managed Cryptography
- Application manages keys itself
- Application responsible for key storage, distribution, revocation
- Requires careful attention to key confidentiality and integrity
- More control but more responsibility

## Key Lifecycle Considerations

Throughout a key's lifecycle, ensure:

| Phase | Confidentiality | Integrity |
|-------|----------------|-----------|
| Generation | Protect output | Protect configuration |
| Storage | Encrypt at rest | Detect tampering |
| Distribution | Secure channel | Verify authenticity |
| Usage | Limit exposure | Validate before use |
| Rotation | Secure transition | Complete replacement |
| Destruction | Secure deletion | Confirm destruction |

## Symmetric vs. Asymmetric Keys

| Key Type | Confidentiality | Integrity |
|----------|----------------|-----------|
| Symmetric key | **Required** | Required |
| Asymmetric private key | **Required** | Required |
| Asymmetric public key | Can be relaxed | **Required** |

**Note**: Even public keys require integrity protection—an attacker substituting a public key can compromise the entire system.

## Implementation Checklist

- [ ] Key confidentiality protected (storage and transmission)
- [ ] Key integrity protected (storage and transmission)
- [ ] Key configuration protected from tampering
- [ ] KeyInfo protected from tampering
- [ ] Action configuration protected from tampering
- [ ] Key lifecycle managed (generation through destruction)
- [ ] Appropriate implementation chosen (as-a-service vs. self-managed)
- [ ] Public key integrity verified even if confidentiality relaxed

## Related Patterns

- **Cryptographic action** (uses keys managed by this pattern)
- **Encryption** (specific cryptographic action)
- **Digital signature** (specific cryptographic action)
- **Message authentication code** (specific cryptographic action)
- **Cryptography as a service** (implementation pattern)
- **Self-managed cryptography** (implementation pattern)

## References

- Source: https://securitypatterns.distrinet-research.be/patterns/99_02_001__crypto_key_management/
- E. Barker, 'Recommendation for Key Management: Part 1 – General', NIST SP 800-57 Part 1, May 2020
- NIST SP 800-130, 'A Framework for Designing Cryptographic Key Management Systems'
- OWASP Key Management Cheat Sheet
