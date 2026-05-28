# Hardcoded Cryptographic Keys

**Category**: cryptography/hardcoded-keys
**Description**: Detection of cryptographic keys embedded in source code
**CWE**: CWE-321, CWE-798

---

## Private Key Detection

### RSA Private Key
**Pattern**: `-----BEGIN RSA PRIVATE KEY-----`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- RSA private key embedded in source code
- CWE-321: Use of Hard-coded Cryptographic Key

### RSA Private Key (Encrypted)
**Pattern**: `-----BEGIN ENCRYPTED PRIVATE KEY-----`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Encrypted private key in source (password may be nearby)

### EC Private Key
**Pattern**: `-----BEGIN EC PRIVATE KEY-----`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Elliptic curve private key in source code

### Generic Private Key (PKCS#8)
**Pattern**: `-----BEGIN PRIVATE KEY-----`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- PKCS#8 private key in source code

### DSA Private Key
**Pattern**: `-----BEGIN DSA PRIVATE KEY-----`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- DSA private key in source code

### OpenSSH Private Key
**Pattern**: `-----BEGIN OPENSSH PRIVATE KEY-----`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- OpenSSH format private key in source code

### PGP Private Key
**Pattern**: `-----BEGIN PGP PRIVATE KEY BLOCK-----`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- PGP private key block in source code

---

## Symmetric Key Detection

### Hardcoded AES Key (Hex 128-bit)
**Pattern**: `(?:aes|AES|encryption).*key\s*[=:]\s*['"]([0-9a-fA-F]{32})['"]`
**Type**: regex
**Severity**: critical
**Languages**: [python, javascript, typescript, java, go]
- AES-128 key hardcoded as hex string

### Hardcoded AES Key (Hex 256-bit)
**Pattern**: `(?:aes|AES|encryption).*key\s*[=:]\s*['"]([0-9a-fA-F]{64})['"]`
**Type**: regex
**Severity**: critical
**Languages**: [python, javascript, typescript, java, go]
- AES-256 key hardcoded as hex string

### Hardcoded AES Key (Base64)
**Pattern**: `(?:aes|AES|encryption).*key\s*[=:]\s*['"]([A-Za-z0-9+/]{22,44}={0,2})['"]`
**Type**: regex
**Severity**: critical
**Languages**: [python, javascript, typescript, java, go]
- AES key hardcoded as base64 string

### Symmetric Key Bytes
**Pattern**: `key\s*=\s*b['"][^'"]{16,}['"]`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Hardcoded symmetric key as byte string

---

## IV and Salt Detection

### Hardcoded IV (Hex)
**Pattern**: `(?:iv|IV|nonce|NONCE)\s*[=:]\s*['"]([0-9a-fA-F]{16,32})['"]`
**Type**: regex
**Severity**: high
**Languages**: [python, javascript, typescript, java, go]
- Hardcoded initialization vector (should be random per encryption)

### Hardcoded IV (Bytes)
**Pattern**: `(?:iv|IV|nonce)\s*[=:]\s*b['"]`
**Type**: regex
**Severity**: high
**Languages**: [python]
- Hardcoded byte string IV

### Password Salt (Hardcoded)
**Pattern**: `(?:salt|SALT)\s*[=:]\s*['"]([^'"]{8,})['"]`
**Type**: regex
**Severity**: high
**Languages**: [python, javascript, typescript, java, go, ruby, php]
- Hardcoded salt value (should be random per user)

---

## JWT and HMAC Keys

### JWT Secret Key
**Pattern**: `(?:jwt|JWT).*(?:secret|SECRET|key|KEY)\s*[=:]\s*['"]([^'"]{16,})['"]`
**Type**: regex
**Severity**: critical
**Languages**: [python, javascript, typescript, java, go]
- Hardcoded JWT signing secret

### HMAC Secret Key
**Pattern**: `(?:hmac|HMAC).*(?:secret|SECRET|key|KEY)\s*[=:]\s*['"]([^'"]{16,})['"]`
**Type**: regex
**Severity**: critical
**Languages**: [python, javascript, typescript, java, go]
- Hardcoded HMAC secret key

### Generic Encryption Key Variable
**Pattern**: `(?:ENCRYPTION|CRYPTO|SECRET|SIGNING)_KEY\s*[=:]\s*['"]([^'"]{16,})['"]`
**Type**: regex
**Severity**: critical
**Languages**: [python, javascript, typescript, java, go, ruby, php]
- Generic encryption key in environment/config style

---

## Weak Key Generation

### Python Weak RSA Key
**Pattern**: `RSA\.generate\((512|1024)\)`
**Type**: regex
**Severity**: high
**Languages**: [python]
- Weak RSA key generation (should be >= 2048)

### Python Cryptography Weak RSA
**Pattern**: `rsa\.generate_private_key\(.*key_size=(512|1024)`
**Type**: regex
**Severity**: high
**Languages**: [python]
- Weak RSA in cryptography library

### Java Weak RSA
**Pattern**: `keyGenerator\.init\((512|1024)\)`
**Type**: regex
**Severity**: high
**Languages**: [java]
- Weak RSA key size in Java KeyGenerator

### Go Weak RSA
**Pattern**: `rsa\.GenerateKey\(.*,(512|1024)\)`
**Type**: regex
**Severity**: high
**Languages**: [go]
- Weak RSA key in Go

### JavaScript Weak RSA
**Pattern**: `modulusLength:\s*(512|1024)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Weak RSA modulus length in Web Crypto API

### Ruby Weak RSA
**Pattern**: `OpenSSL::PKey::RSA\.(new|generate)\((512|1024)\)`
**Type**: regex
**Severity**: high
**Languages**: [ruby]
- Weak RSA key in Ruby

---

## Best Practices

### Key Management
- Store keys in environment variables or secrets managers
- Use key derivation functions (KDF) when deriving keys from passwords
- Rotate keys regularly
- Use hardware security modules (HSM) for sensitive keys

### Key Size Requirements
| Algorithm | Minimum Size | Recommended Size |
|-----------|--------------|------------------|
| RSA | 2048 bits | 4096 bits |
| DSA | 2048 bits | 3072 bits |
| ECDSA | 256 bits (P-256) | 384 bits (P-384) |
| AES | 128 bits | 256 bits |

---

## References

- [CWE-321: Use of Hard-coded Cryptographic Key](https://cwe.mitre.org/data/definitions/321.html)
- [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
- [NIST Key Management Guidelines](https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final)
