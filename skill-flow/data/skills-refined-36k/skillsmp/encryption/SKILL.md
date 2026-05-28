---
name: encryption
description: Security pattern for implementing encryption and decryption operations. Use when encrypting data for confidentiality, selecting encryption algorithms (AES, RSA), configuring cipher modes (GCM, CBC), choosing key lengths, or implementing symmetric/asymmetric encryption. Specialization of Cryptographic action pattern addressing confidentiality requirements.
---

# Encryption Security Pattern

Encrypt a message (data elements and/or action requests) to ensure its confidentiality with respect to entities that do not possess the correct decryption key.

## Core Components

| Role | Type | Responsibility |
|------|------|----------------|
| **EntityA** | Entity | Wants to encrypt one or more data elements and/or action requests |
| **EntityB** | Entity | Wants to decrypt received ciphertext (may be same as EntityA) |
| **Encrypter** | Cryptographic Primitive | Library providing encryption action |
| **Decrypter** | Cryptographic Primitive | Library providing decryption action |

**Note**: Encrypter and Decrypter roles can be performed by a single library instance. Similarly, EntityA and EntityB can be the same entity.

### Data Elements

- **plaintext**: Original data to be encrypted
- **ciphertext**: Encrypted data {plaintext}_k
- **keyInfo**: Information on cryptographic key (identifier or key material)
- **config**: Cipher configuration (algorithm, mode, parameters) - optional

### Actions

- **encrypt**: Request to encrypt plaintext using identified key and configuration
- **decrypt**: Request to decrypt ciphertext using identified key and configuration

## Pattern Flow

### Encryption
```
EntityA → [encrypt(plaintext, keyInfo, config)] → Encrypter
Encrypter → [ciphertext] → EntityA
```

### Decryption
```
EntityB → [decrypt(ciphertext, keyInfo, config)] → Decrypter
Decrypter → [plaintext] → EntityB
```

## Symmetric vs. Asymmetric Encryption

### Symmetric Ciphers
- Same secret key for encryption and decryption
- Fast performance
- Use for bulk data encryption
- Key distribution challenge

### Asymmetric Ciphers
- Public key encrypts, private key decrypts
- Slower performance (significantly slower decryption)
- Use only for small amounts of data
- Better for key negotiation, digital signatures

**Recommendation**: Use symmetric ciphers for encrypting data. Use asymmetric ciphers only where appropriate (key exchange, small data).

## Algorithm Recommendations

### Symmetric Ciphers

| Algorithm | Key Length | Status |
|-----------|------------|--------|
| **AES** | 128 bits | Minimum recommended |
| **AES** | 256 bits | Recommended for long-term (30-50 years) |
| DES | 56 bits | **Deprecated - never use** |
| 3DES/TDEA | 168 bits | **Deprecated - decrypt legacy only** |
| Salsa/ChaCha | Variable | Use with caution (less studied than AES) |

**Preferred**: AES with minimum 128-bit key length. Use AES-256 for long-term protection.

### Cipher Modes (for AES)

| Mode | Status | Notes |
|------|--------|-------|
| **GCM** | Recommended | Authenticated encryption |
| **CCM** | Recommended | Authenticated encryption |
| CBC | Acceptable | Requires separate MAC |
| CTR | Acceptable | Stream mode, needs MAC |
| **ECB** | **Never use** | Reveals patterns in plaintext |

**Critical**: Always use authenticated encryption modes (GCM, CCM) when possible. They provide both confidentiality AND integrity.

### Asymmetric Ciphers

| Algorithm | Key Length | Status |
|-----------|------------|--------|
| **RSA** | 3072 bits | Recommended (≈ AES-128 security) |
| RSA | 2048 bits | Minimum acceptable |
| RSA-PKCS#1 v1.5 | Any | **Avoid** (padding oracle attacks) |

**Note**: RSA-3072 provides security strength comparable to AES-128.

## Security Considerations

### Reuse Existing Libraries

Specialization of Cryptographic action.Reuse existing libraries:
- Use well-known cryptographic libraries
- Verify library supports recommended ciphers
- Avoid libraries supporting only deprecated ciphers
- Consult library documentation

### Use Keys for Single Purpose

Specialization of Cryptographic action.Use keys for single purpose:
- **Never use encryption keys for other purposes** (e.g., signing)
- Use different keys for different data types
- Symmetric key: one kind of plaintext only
- Asymmetric: public key for one kind of plaintext, private key for corresponding ciphertexts

### Design for Change

Specialization of Cryptographic action.Design for change:
- Algorithms may become deprecated
- Key lengths may need to increase
- Design for easy cipher/library transitions

### Authenticated Encryption

**General consensus**: Use authenticated encryption modes for symmetric ciphers.

Benefits:
- Provides integrity guarantees in addition to confidentiality
- Detects if ciphertext was modified after encryption (e.g., by attacker during transmission)
- Most libraries provide authenticated encryption modes for AES

### Random Value Generation (Nonces/IVs)

If Entity must provide random values (nonces, initialization vectors):
- **Always use cryptographically-secure generator**
- OWASP provides overview of secure generators by language
- Never reuse nonce/IV with same key

### Plaintext Leakage

Since plaintext needed encryption, it is likely sensitive:
- Analyze entire plaintext flow for potential leaks
- Check for caching before encryption
- Ensure plaintext doesn't leak through logs, errors, or side channels

## Implementation Checklist

- [ ] Using AES with minimum 128-bit keys
- [ ] Using authenticated encryption mode (GCM/CCM)
- [ ] **No ECB mode**
- [ ] **No deprecated ciphers** (DES, 3DES for new data)
- [ ] RSA minimum 2048 bits (prefer 3072)
- [ ] **No RSA-PKCS#1 v1.5**
- [ ] Keys used for single purpose only
- [ ] Nonces/IVs from cryptographically-secure generator
- [ ] Plaintext flow analyzed for leaks
- [ ] Library supports recommended ciphers
- [ ] Designed for algorithm/key transitions

## Related Patterns

- **Cryptographic action** (parent pattern)
- **Cryptographic key management** (key handling)
- **Selective encrypted transmission** (encryption in transit)
- **Encrypted tunnel** (channel-level encryption)
- **Selective encrypted storage** (encryption at rest)
- **Transparent encrypted storage** (storage-level encryption)

## References

- Source: https://securitypatterns.distrinet-research.be/patterns/99_01_002__encryption/
- Bundesamt für Sicherheit in der Informationstechnik, 'Cryptographic Mechanisms: Recommendations and Key Lengths', BSI TR-02102-1, Mar. 2020
- N. P. Smart et al., 'Algorithms, Key size and parameters report', ENISA, Nov. 2014
- E. Barker, 'Recommendation for Key Management: Part 1 – General', NIST SP 800-57 Part 1, May 2020
- E. Barker, 'Guideline for Using Cryptographic Standards in the Federal Government: Cryptographic Mechanisms', NIST SP 800-175B, Mar. 2020
- E. Barker and A. Roginsky, 'Transitioning the Use of Cryptographic Algorithms and Key Lengths', NIST SP 800-131A rev 2, Mar. 2019
- W. Breyha et al., 'Applied Crypto Hardening', bettercrypto.org, Dec. 2018
- P. C. van Oorschot, Computer Security and the Internet - Tools and Jewels, 2020
- awesome-cryptography: https://github.com/sobolevn/awesome-cryptography
