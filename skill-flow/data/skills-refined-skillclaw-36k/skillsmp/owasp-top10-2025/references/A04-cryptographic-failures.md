# A04 Cryptographic Failures

## Background

Cryptographic Failures has moved to **#4** in OWASP Top 10:2025. This vulnerability focuses on failures related to missing encryption, insufficiently strong encryption, cryptographic key leakage, and related errors.

### Statistics
| Item | Value |
|------|-------|
| Mapped CWEs | 32 |
| Max Incidence Rate | 13.77% |
| Avg Incidence Rate | 3.80% |
| Total Occurrences | 1,665,348 |
| Total CVEs | 2,185 |

### Key Related Vulnerabilities
- CWE-327: Broken or Risky Cryptographic Algorithm
- CWE-331: Insufficient Entropy
- CWE-1241: Predictable Algorithm in Random Number Generator
- CWE-338: Weak Pseudo-Random Number Generator

## Description

All data in transit must use transport layer encryption. Modern solutions with CPU acceleration (AES instructions) and streamlined certificate management (LetsEncrypt) address previous barriers.

Beyond transport security, organizations must encrypt:
- Sensitive data at rest
- Passwords, credit card numbers, health records
- Personal data subject to GDPR or PCI DSS

### Key Concerns

1. **Outdated or Weak Cryptographic Algorithms**
2. **Weak or Default Cryptographic Keys**
3. **Keys Checked Into Source Code**
4. **Missing Security Headers**
5. **Invalid Certificate Chain Verification**
6. **Improper Initialization Vectors**
7. **Using Password as Cryptographic Key**
8. **Weak Randomness Implementation**
9. **Deprecated Hash Functions (MD5, SHA1)**
10. **Exploitable Cryptographic Error Messages**
11. **Algorithm Downgrade Possibility**

## How to Prevent

### Minimum Protection Measures

1. **Data Classification**: Identify sensitive data according to privacy laws and business requirements
2. **Key Storage**: Use hardware or cloud HSM for critical keys
3. **Algorithm Selection**: Use trusted cryptographic implementations
4. **Data Minimization**: Discard unnecessary sensitive data or use PCI DSS tokenization
5. **Encryption Standards**: Enforce TLS 1.2+, forward secrecy ciphers, deprecate CBC, prepare for quantum-resistant algorithms
6. **Cache Control**: Disable caching for sensitive responses at CDN and application layers
7. **Protocol Security**: Do not use unencrypted protocols (FTP, unencrypted SMTP, STARTTLS)
8. **Password Hashing**: Use strong, salted functions — Argon2, yescrypt, scrypt or PBKDF2-HMAC-SHA-512
9. **Initialization Vectors**: Use cryptographically secure PRNG; never reuse IV with fixed key
10. **Authentication**: Always use authenticated encryption
11. **Key Generation**: Generate keys cryptographically randomly and store as byte arrays
12. **Randomness**: Ensure cryptographic randomness without predictable seeding
13. **Deprecated Functions**: Remove MD5, SHA1, CBC mode, PKCS 1 v1.5
14. **Post-Quantum Preparation**: Prepare for post-quantum cryptography by end of 2030

## Example Attack Scenarios

### Scenario #1 - Session Hijacking
```
Attacker monitors traffic over insecure wireless network,
downgrades HTTPS to HTTP, intercepts requests,
steals session cookies, hijacks authenticated sessions to
access or modify personal data or transaction details.
```

### Scenario #2 - Database Breach
```
Password database using unsalted or simple hashes is exposed
through file upload vulnerability.
Attackers use pre-computed rainbow tables or
GPU-accelerated cracking for salted hashes generated
with weak functions.
```

## References

- [OWASP Proactive Controls: C2 (Cryptography for Data Protection)](https://owasp.org/www-project-proactive-controls/)
- [OWASP ASVS: V11, V12, V14](https://owasp.org/www-project-application-security-verification-standard/)
- [Transport Layer Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)
- [User Privacy Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html)
- [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [HSTS Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html)
- [OWASP Testing Guide: Testing for Weak Cryptography](https://owasp.org/www-project-web-security-testing-guide/)
- [ENISA: Post-Quantum Cryptography Implementation Roadmap](https://www.enisa.europa.eu/)
- [NIST: Post-Quantum Cryptography Standards (2024)](https://csrc.nist.gov/Projects/Post-Quantum-Cryptography)

## List of Mapped CWEs

| CWE ID | Description |
|--------|-------------|
| [CWE-261](https://cwe.mitre.org/data/definitions/261.html) | Weak Encoding for Password |
| [CWE-296](https://cwe.mitre.org/data/definitions/296.html) | Improper Following of Certificate Trust Chain |
| [CWE-319](https://cwe.mitre.org/data/definitions/319.html) | Cleartext Transmission of Sensitive Information |
| [CWE-320](https://cwe.mitre.org/data/definitions/320.html) | Key Management Errors |
| [CWE-321](https://cwe.mitre.org/data/definitions/321.html) | Hardcoded Cryptographic Key |
| [CWE-322](https://cwe.mitre.org/data/definitions/322.html) | Key Exchange Without Entity Authentication |
| [CWE-323](https://cwe.mitre.org/data/definitions/323.html) | Reusing Nonce/Key Pair in Encryption |
| [CWE-324](https://cwe.mitre.org/data/definitions/324.html) | Use of Key Past Expiration |
| [CWE-325](https://cwe.mitre.org/data/definitions/325.html) | Missing Cryptographic Step |
| [CWE-326](https://cwe.mitre.org/data/definitions/326.html) | Inadequate Encryption Strength |
| [CWE-327](https://cwe.mitre.org/data/definitions/327.html) | Broken or Risky Cryptographic Algorithm |
| [CWE-328](https://cwe.mitre.org/data/definitions/328.html) | Reversible One-Way Hash |
| [CWE-329](https://cwe.mitre.org/data/definitions/329.html) | Non-Random IV in CBC Mode |
| [CWE-330](https://cwe.mitre.org/data/definitions/330.html) | Insufficiently Random Values |
| [CWE-331](https://cwe.mitre.org/data/definitions/331.html) | Insufficient Entropy |
| [CWE-332](https://cwe.mitre.org/data/definitions/332.html) | Insufficient Entropy in PRNG |
| [CWE-334](https://cwe.mitre.org/data/definitions/334.html) | Small Space of Random Values |
| [CWE-335](https://cwe.mitre.org/data/definitions/335.html) | Incorrect Usage of Seeds in PRNG |
| [CWE-336](https://cwe.mitre.org/data/definitions/336.html) | Same Seed in PRNG |
| [CWE-337](https://cwe.mitre.org/data/definitions/337.html) | Predictable Seed in PRNG |
| [CWE-338](https://cwe.mitre.org/data/definitions/338.html) | Weak Pseudo-Random Number Generator |
| [CWE-340](https://cwe.mitre.org/data/definitions/340.html) | Predictable Number/Identifier Generation |
| [CWE-342](https://cwe.mitre.org/data/definitions/342.html) | Predictable Value from Previous Value |
| [CWE-347](https://cwe.mitre.org/data/definitions/347.html) | Improper Verification of Cryptographic Signature |
| [CWE-523](https://cwe.mitre.org/data/definitions/523.html) | Unprotected Transport of Credentials |
| [CWE-757](https://cwe.mitre.org/data/definitions/757.html) | Selection of Less-Secure Algorithm During Negotiation |
| [CWE-759](https://cwe.mitre.org/data/definitions/759.html) | One-Way Hash Without Salt |
| [CWE-760](https://cwe.mitre.org/data/definitions/760.html) | One-Way Hash with Predictable Salt |
| [CWE-780](https://cwe.mitre.org/data/definitions/780.html) | RSA Algorithm without OAEP |
| [CWE-916](https://cwe.mitre.org/data/definitions/916.html) | Insufficient Computational Effort in Password Hashing |
| [CWE-1240](https://cwe.mitre.org/data/definitions/1240.html) | Cryptographic Primitives with Risky Implementation |
| [CWE-1241](https://cwe.mitre.org/data/definitions/1241.html) | Predictable Algorithm in Random Number Generator |
