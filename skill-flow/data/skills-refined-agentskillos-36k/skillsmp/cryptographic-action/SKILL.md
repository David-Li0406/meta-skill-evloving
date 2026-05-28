---
name: cryptographic-action
description: Base security pattern for integrating cryptographic primitives into software systems. Use when implementing encryption, digital signatures, MACs, or any cryptographic operations. Provides guidance on library selection, key usage, configuration protection, and designing for cryptographic agility. Foundation pattern for Encryption, Digital signature, and MAC patterns.
---

# Cryptographic Action Security Pattern

This pattern encapsulates the common considerations for integrating cryptographic primitives into a system. It acts as a foundation for specific patterns like Encryption, Digital Signature, and Message Authentication Code (MAC).

## Purpose

This pattern does not directly address a specific security problem but provides essential guidance for correctly applying cryptographic solutions. Proper implementation of cryptographic actions is crucial—incorrect usage can nullify all security guarantees.

## Core Components

| Role | Type | Responsibility |
|------|------|----------------|
| **Entity** | Entity | Wants to perform one or more cryptographic actions |
| **Cryptographer** | Cryptographic Primitive | Library that provides cryptographic actions |

### Data Elements

- **input**: The plaintext data on which the cryptographic action is performed
- **output**: The result of the cryptographic action (e.g., ciphertext, digital signature)
- **keyInfo**: Information on the cryptographic key to use (identifier or key material itself, depending on key management approach)
- **config**: Configuration for the Cryptographer (e.g., cipher mode) - optional

## Pattern Flow

```
Entity → [crypto_action(input, keyInfo, config)] → Cryptographer
Cryptographer → [output] → Entity
```

1. Entity requests a cryptographic action (e.g., encrypt, sign)
2. Entity provides input data, key information, and optional configuration
3. Cryptographer performs the requested action
4. Cryptographer returns the result to Entity

## Critical Considerations

### Reuse Existing Libraries

**One should always use existing, well-known libraries when integrating cryptography into a system.**

**Never attempt to:**
- Define new, custom cryptographic ciphers
- Implement existing ciphers yourself
- Create custom cryptographic protocols

Before selecting a library:
- Consult library documentation
- Verify assumptions and dependencies are compatible with your system
- Avoid libraries no longer actively maintained
- Avoid libraries that deviate from best practices

### Use Keys for a Single Purpose

**A cryptographic key should never be used for multiple purposes.**

Examples of violations:
- Using the same key for encryption AND signing
- Using the same key for different types of data

Why this matters:
- May negatively impact security properties of operations
- Increases damage if key is compromised
- Different operations may have different security requirements

### Design for Change

Over time, vulnerabilities in ciphers or implementations will be discovered, and processing power will increase. Software should be designed to allow:
- Configuration changes (e.g., longer keys)
- Cipher replacement
- Library replacement

**Recommended approach**: Provide an API abstraction layer around the cryptography library. This abstraction:
- Isolates cryptographic operations
- Makes transitions easier
- Centralizes cryptographic policy

### Configuration Integrity

If Entity provides configuration to Cryptographer:
- **Protect against tampering** during transmission and storage
- An attacker might change configuration to use insecure, deprecated ciphers
- Detect any unauthorized changes

### Configuration Confidentiality

In some cases, configuration may reveal information about:
- Keys that will be used
- System capabilities
- Attack surface

Consider additional measures to keep configuration confidential when warranted.

## Implementations

This pattern is specialized by:
- **Encryption**: Encrypting and decrypting data
- **Digital Signature**: Signing and verifying messages
- **Message Authentication Code (MAC)**: Generating and verifying MACs

Each implementation provides specific considerations for that cryptographic action.

## Related Patterns

- **Cryptographic key management**: Addresses proper key handling
- **Cryptography as a service**: Delegates crypto to external service (e.g., KMS)
- **Self-managed cryptography**: Application manages its own keys

## Library Resources

Pointers to cryptographic libraries can be found in:
- Implementing patterns (Encryption, Digital signature, MAC)
- Cryptographic key management pattern and its implementations
- [awesome-cryptography](https://github.com/sobolevn/awesome-cryptography) - comprehensive list by language

## Implementation Checklist

- [ ] Using established, well-known cryptographic library
- [ ] No custom cryptographic implementations
- [ ] Each key used for single purpose only
- [ ] API abstraction layer for cryptographic operations
- [ ] Configuration protected from tampering
- [ ] Configuration confidentiality addressed if needed
- [ ] Library actively maintained
- [ ] Library follows current best practices
- [ ] Designed for cipher/key length transitions

## References

- Source: https://securitypatterns.distrinet-research.be/patterns/99_01_001__cryptographic_action/
- I. Arce et al., 'Avoiding the Top 10 Software Security Design Flaws', IEEE, 2014
- Bundesamt für Sicherheit in der Informationstechnik, 'Cryptographic Mechanisms: Recommendations and Key Lengths', BSI TR-02102-1, Mar. 2020
- E. Barker, 'Recommendation for Key Management: Part 1 – General', NIST SP 800-57 Part 1, May 2020
- P. C. van Oorschot, Computer Security and the Internet - Tools and Jewels, 2020
