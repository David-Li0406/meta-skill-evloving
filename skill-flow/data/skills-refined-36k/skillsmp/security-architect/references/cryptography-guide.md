# Cryptography Guide for Security Architects

Pragmatic guidance on cryptographic algorithm selection, key management, and implementation patterns.

## Core Principle

**Use well-established, peer-reviewed cryptography. Never roll your own crypto.**

## Cryptographic Primitives

### Symmetric Encryption

**Current Standard: AES-256-GCM**
- **Use Case**: Encrypting data at rest and in transit
- **Key Size**: 256-bit minimum
- **Mode**: GCM (Galois/Counter Mode) for authenticated encryption
- **Why**: NIST-approved, hardware-accelerated on modern CPUs, provides both confidentiality and integrity

**Legacy (Avoid for New Systems)**: AES-CBC, 3DES, RC4

### Asymmetric Encryption

**Current Standards:**
- **RSA**: 3072-bit minimum (4096-bit for long-term security)
- **Elliptic Curve**: Ed25519 (signing), X25519 (key exchange), P-256 (NIST curves)

**Use Cases:**
- **Digital Signatures**: Ed25519, RSA-PSS
- **Key Exchange**: ECDH (X25519), RSA-OAEP
- **TLS/SSL**: ECDHE for forward secrecy

**Why Ed25519**: Faster than RSA, smaller keys (32 bytes), immune to timing attacks, no complex parameters

**Legacy (Avoid)**: RSA < 2048-bit, DSA

### Hashing

**Current Standards:**
- **SHA-256/SHA-384/SHA-512**: General-purpose cryptographic hashing
- **SHA-3**: Alternative to SHA-2, newer standard
- **BLAKE3**: High-performance, parallelizable (for non-compliance scenarios)

**Use Cases:**
- **Integrity Verification**: SHA-256
- **Digital Signatures**: SHA-256 or SHA-384
- **File Checksums**: SHA-256

**Legacy (Avoid)**: MD5, SHA-1 (both cryptographically broken)

### Password Hashing

**Current Standards:**
- **Argon2id**: Winner of Password Hashing Competition, best overall choice
- **scrypt**: Good alternative, widely supported
- **bcrypt**: Acceptable, proven track record (use cost factor ≥ 12)

**Parameters (Argon2id):**
- **Memory**: 64 MB minimum (adjust based on threat model)
- **Iterations**: 3-4
- **Parallelism**: 2-4

**Never Use**: Plain hashing (SHA-256, MD5), unsalted hashes

### Message Authentication Codes (MAC)

**Current Standards:**
- **HMAC-SHA256**: Most common, well-supported
- **HMAC-SHA384/512**: For higher security requirements
- **Poly1305**: Used with ChaCha20 in modern protocols

**Use Case**: Verify integrity and authenticity of messages

## Key Management

### Key Generation

**Principles:**
- Use cryptographically secure random number generators (CSPRNG)
- Never derive keys from passwords without proper KDF
- Generate keys of appropriate length for algorithm

**CSPRNGs:**
- **Linux**: `/dev/urandom` (not `/dev/random`)
- **Python**: `secrets` module
- **Node.js**: `crypto.randomBytes()`
- **Go**: `crypto/rand`

### Key Storage

**Hierarchy:**
1. **Hardware Security Modules (HSM)**: Highest security for root keys (FIPS 140-2 Level 3+)
2. **Key Management Services**: AWS KMS, Azure Key Vault, GCP KMS - for production workloads
3. **Secrets Management**: HashiCorp Vault, Doppler - for application secrets
4. **Encrypted Configuration**: SOPS, git-crypt - for development secrets
5. **Environment Variables**: Acceptable for non-production with proper access controls

**Never Store:**
- Keys in source code
- Keys in container images
- Keys in version control (even private repos)
- Unencrypted keys on disk

### Key Rotation

**Frequency:**
- **Data Encryption Keys (DEK)**: Monthly to quarterly
- **Key Encryption Keys (KEK)**: Annually
- **Root Keys**: Every 2-3 years or after security incidents
- **TLS Certificates**: 90 days (modern best practice)

**Pattern**: Envelope encryption (encrypt data with DEK, encrypt DEK with KEK)

### Key Lifecycle

1. **Generation**: Use CSPRNG with sufficient entropy
2. **Distribution**: Use secure channels (TLS 1.3, out-of-band verification)
3. **Storage**: Encrypted at rest, access-controlled
4. **Usage**: Principle of least privilege, audit all usage
5. **Rotation**: Regular schedule, triggered by incidents
6. **Destruction**: Cryptographic erasure (overwrite with random data), hardware destruction for physical media

## TLS/SSL Configuration

### Current Best Practices

**TLS Version**: 1.3 preferred, 1.2 acceptable minimum (disable 1.0, 1.1, SSLv3)

**Cipher Suites (Recommended Order):**
```
TLS 1.3:
- TLS_AES_128_GCM_SHA256
- TLS_AES_256_GCM_SHA384
- TLS_CHACHA20_POLY1305_SHA256

TLS 1.2 (if needed):
- ECDHE-RSA-AES128-GCM-SHA256
- ECDHE-RSA-AES256-GCM-SHA384
- ECDHE-RSA-CHACHA20-POLY1305
```

**Certificate Requirements:**
- RSA: 3072-bit minimum
- ECC: P-256 or P-384
- Validity: 90 days (Let's Encrypt automated renewal)
- Certificate Transparency: Required
- OCSP Stapling: Enabled

**Additional Protections:**
- Perfect Forward Secrecy (PFS): ECDHE key exchange
- HTTP Strict Transport Security (HSTS): `max-age=31536000; includeSubDomains; preload`
- Certificate Pinning: For mobile apps, high-security scenarios

## Modern Cryptography Patterns

### Authenticated Encryption with Associated Data (AEAD)

**Why**: Provides confidentiality, integrity, and authenticity in single operation

**Algorithms:**
- AES-GCM: Fast, hardware-accelerated
- ChaCha20-Poly1305: Pure software performance, constant-time

**Use Case**: Encrypting application data, network protocols

### Zero-Knowledge Proofs (ZKP)

**Use Case**: Prove knowledge of information without revealing it
**Applications**: Privacy-preserving authentication, blockchain, confidential voting
**Caution**: Complex to implement correctly, use established libraries

### Post-Quantum Cryptography (PQC)

**Timeline**: NIST standards finalized in 2024, gradual adoption beginning
**Algorithms (Standardized):**
- **Key Exchange**: CRYSTALS-Kyber
- **Signatures**: CRYSTALS-Dilithium, FALCON, SPHINCS+

**Migration Strategy:**
- Hybrid approach: Classical + PQC algorithms
- Monitor NIST standardization process
- Plan transition for long-term secrets (10+ year data retention)

## Common Pitfalls to Avoid

1. **ECB Mode**: Leaks patterns in encrypted data (use GCM, CTR, or CBC with IV)
2. **Weak Random Numbers**: Using predictable random number generators
3. **Key Reuse**: Using same key for encryption and authentication
4. **Insufficient Key Length**: 128-bit keys for symmetric, 3072-bit RSA minimum
5. **Hardcoded Keys**: Keys in source code or configuration
6. **Ignoring Crypto Agility**: No ability to switch algorithms when vulnerabilities discovered
7. **Timing Attacks**: Non-constant-time comparisons (use constant-time compare functions)
8. **Padding Oracle Attacks**: Improper error handling with CBC mode

## Implementation Checklist

When implementing cryptography:

- [ ] Use established, well-maintained libraries (OpenSSL, libsodium, Bouncy Castle)
- [ ] Never implement cryptographic algorithms from scratch
- [ ] Use AEAD modes (GCM) instead of unauthenticated encryption
- [ ] Generate keys with CSPRNG
- [ ] Store keys securely (HSM, KMS, secrets manager)
- [ ] Implement key rotation
- [ ] Use TLS 1.3 for data in transit
- [ ] Hash passwords with Argon2id, scrypt, or bcrypt
- [ ] Enable Perfect Forward Secrecy
- [ ] Implement proper error handling (don't leak crypto details)
- [ ] Log crypto operations (key usage, rotation, failures)
- [ ] Plan for crypto agility (ability to change algorithms)
- [ ] Conduct cryptographic review with experts
- [ ] Test with known test vectors
- [ ] Monitor for vulnerability disclosures

## Reference Implementations

**Python:**
```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# AES-GCM encryption
key = AESGCM.generate_key(bit_length=256)
aesgcm = AESGCM(key)
nonce = os.urandom(12)  # 96-bit nonce
ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
```

**Key Derivation:**
```python
from argon2 import PasswordHasher

ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)
hash = ph.hash("user_password")
ph.verify(hash, "user_password")  # Raises exception if invalid
```

## Resources

- **NIST Cryptographic Standards**: https://csrc.nist.gov/
- **OWASP Cryptographic Storage Cheat Sheet**: https://cheatsheetseries.owasp.org/
- **SSL Labs**: https://www.ssllabs.com/ (TLS configuration testing)
- **Crypto.SE**: https://crypto.stackexchange.com/ (cryptography Q&A)

---

**Remember**: Cryptography is a tool, not a solution. Proper key management, secure implementation, and defense-in-depth are equally critical to security architecture.