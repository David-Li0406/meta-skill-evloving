# Weak Cryptographic Ciphers

**Category**: cryptography/weak-ciphers
**Description**: Detection of weak, deprecated, or broken cryptographic algorithms
**CWE**: CWE-327, CWE-328

---

## Python Weak Ciphers

### Python DES Import
**Pattern**: `from Crypto\.Cipher import DES`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- DES cipher import (broken - 56-bit key)
- CWE-327: Use of a Broken or Risky Cryptographic Algorithm

### Python Blowfish Import
**Pattern**: `from Crypto\.Cipher import Blowfish`
**Type**: regex
**Severity**: high
**Languages**: [python]
- Blowfish cipher import (deprecated)

### Python RC4 Import
**Pattern**: `from Crypto\.Cipher import ARC4`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- RC4 cipher import (broken)

### Python MD5 Hash
**Pattern**: `hashlib\.md5\(`
**Type**: regex
**Severity**: high
**Languages**: [python]
- MD5 hash usage (broken for security)
- CWE-328: Use of Weak Hash

### Python SHA1 Hash
**Pattern**: `hashlib\.sha1\(`
**Type**: regex
**Severity**: medium
**Languages**: [python]
- SHA1 hash usage (deprecated for security)

### Python AES ECB Mode
**Pattern**: `AES\.MODE_ECB`
**Type**: regex
**Severity**: high
**Languages**: [python]
- ECB mode usage (insecure - no IV, patterns visible)

### Python DES3 ECB Mode
**Pattern**: `DES3\.MODE_ECB`
**Type**: regex
**Severity**: high
**Languages**: [python]
- Triple DES with ECB mode

---

## JavaScript Weak Ciphers

### Node.js DES Cipher
**Pattern**: `crypto\.createCipher\(['"]des`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- DES cipher in Node.js
- CWE-327: Use of a Broken or Risky Cryptographic Algorithm

### Node.js DES CipherIV
**Pattern**: `crypto\.createCipheriv\(['"]des`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- DES cipher with IV in Node.js

### Node.js MD5 Hash
**Pattern**: `crypto\.createHash\(['"]md5`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- MD5 hash in Node.js
- CWE-328: Use of Weak Hash

### Node.js SHA1 Hash
**Pattern**: `crypto\.createHash\(['"]sha1`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- SHA1 hash in Node.js

### CryptoJS DES
**Pattern**: `CryptoJS\.DES`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- DES in CryptoJS library

### CryptoJS RC4
**Pattern**: `CryptoJS\.RC4`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript]
- RC4 in CryptoJS (broken)

### CryptoJS TripleDES
**Pattern**: `CryptoJS\.TripleDES`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Triple DES (deprecated)

### CryptoJS MD5
**Pattern**: `CryptoJS\.MD5`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- MD5 in CryptoJS

### CryptoJS SHA1
**Pattern**: `CryptoJS\.SHA1`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript]
- SHA1 in CryptoJS

### CryptoJS ECB Mode
**Pattern**: `mode:\s*CryptoJS\.mode\.ECB`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- ECB mode in CryptoJS

---

## Java Weak Ciphers

### Java DES Cipher
**Pattern**: `Cipher\.getInstance\(["']DES`
**Type**: regex
**Severity**: critical
**Languages**: [java, kotlin]
- DES cipher in Java
- CWE-327: Use of a Broken or Risky Cryptographic Algorithm

### Java DESede Cipher
**Pattern**: `Cipher\.getInstance\(["']DESede`
**Type**: regex
**Severity**: high
**Languages**: [java, kotlin]
- Triple DES in Java (deprecated)

### Java ECB Mode
**Pattern**: `Cipher\.getInstance\(["'].*ECB`
**Type**: regex
**Severity**: high
**Languages**: [java, kotlin]
- ECB mode in Java

### Java RC4 Cipher
**Pattern**: `Cipher\.getInstance\(["']RC4`
**Type**: regex
**Severity**: critical
**Languages**: [java, kotlin]
- RC4 cipher in Java

### Java ARCFOUR Cipher
**Pattern**: `Cipher\.getInstance\(["']ARCFOUR`
**Type**: regex
**Severity**: critical
**Languages**: [java, kotlin]
- ARCFOUR (RC4) in Java

### Java Blowfish Cipher
**Pattern**: `Cipher\.getInstance\(["']Blowfish`
**Type**: regex
**Severity**: high
**Languages**: [java, kotlin]
- Blowfish in Java

### Java MD5 Hash
**Pattern**: `MessageDigest\.getInstance\(["']MD5`
**Type**: regex
**Severity**: high
**Languages**: [java, kotlin]
- MD5 in Java
- CWE-328: Use of Weak Hash

### Java SHA-1 Hash
**Pattern**: `MessageDigest\.getInstance\(["']SHA-1`
**Type**: regex
**Severity**: medium
**Languages**: [java, kotlin]
- SHA1 in Java

### Java SHA1 Hash Alt
**Pattern**: `MessageDigest\.getInstance\(["']SHA1`
**Type**: regex
**Severity**: medium
**Languages**: [java, kotlin]
- SHA1 in Java (alternate form)

---

## Go Weak Ciphers

### Go DES Cipher
**Pattern**: `des\.NewCipher`
**Type**: regex
**Severity**: critical
**Languages**: [go]
- DES cipher in Go
- CWE-327: Use of a Broken or Risky Cryptographic Algorithm

### Go Triple DES Cipher
**Pattern**: `des\.NewTripleDESCipher`
**Type**: regex
**Severity**: high
**Languages**: [go]
- Triple DES in Go

### Go MD5 New
**Pattern**: `md5\.New\(\)`
**Type**: regex
**Severity**: high
**Languages**: [go]
- MD5 in Go
- CWE-328: Use of Weak Hash

### Go MD5 Sum
**Pattern**: `md5\.Sum\(`
**Type**: regex
**Severity**: high
**Languages**: [go]
- MD5 sum in Go

### Go SHA1 New
**Pattern**: `sha1\.New\(\)`
**Type**: regex
**Severity**: medium
**Languages**: [go]
- SHA1 in Go

### Go SHA1 Sum
**Pattern**: `sha1\.Sum\(`
**Type**: regex
**Severity**: medium
**Languages**: [go]
- SHA1 sum in Go

### Go RC4 Cipher
**Pattern**: `rc4\.NewCipher`
**Type**: regex
**Severity**: critical
**Languages**: [go]
- RC4 in Go (broken)

### Go DES with CBC
**Pattern**: `cipher\.NewCBCEncrypter.*des`
**Type**: regex
**Severity**: critical
**Languages**: [go]
- DES with CBC in Go

---

## Ruby Weak Ciphers

### Ruby DES Cipher
**Pattern**: `OpenSSL::Cipher\.new\(['"]des`
**Type**: regex
**Severity**: critical
**Languages**: [ruby]
- DES cipher in Ruby
- CWE-327: Use of a Broken or Risky Cryptographic Algorithm

### Ruby RC4 Cipher
**Pattern**: `OpenSSL::Cipher\.new\(['"]rc4`
**Type**: regex
**Severity**: critical
**Languages**: [ruby]
- RC4 cipher in Ruby

### Ruby MD5 Hash
**Pattern**: `Digest::MD5`
**Type**: regex
**Severity**: high
**Languages**: [ruby]
- MD5 in Ruby
- CWE-328: Use of Weak Hash

### Ruby SHA1 Hash
**Pattern**: `Digest::SHA1`
**Type**: regex
**Severity**: medium
**Languages**: [ruby]
- SHA1 in Ruby

---

## PHP Weak Ciphers

### PHP mcrypt DES
**Pattern**: `mcrypt_encrypt\(.*MCRYPT_DES`
**Type**: regex
**Severity**: critical
**Languages**: [php]
- DES in PHP mcrypt (deprecated API)
- CWE-327: Use of a Broken or Risky Cryptographic Algorithm

### PHP OpenSSL DES
**Pattern**: `openssl_encrypt\(.*['"]des`
**Type**: regex
**Severity**: critical
**Languages**: [php]
- DES in PHP OpenSSL

### PHP OpenSSL RC4
**Pattern**: `openssl_encrypt\(.*['"]rc4`
**Type**: regex
**Severity**: critical
**Languages**: [php]
- RC4 in PHP

### PHP MD5 Function
**Pattern**: `\bmd5\(`
**Type**: regex
**Severity**: high
**Languages**: [php]
- MD5 function in PHP
- CWE-328: Use of Weak Hash

### PHP SHA1 Function
**Pattern**: `\bsha1\(`
**Type**: regex
**Severity**: medium
**Languages**: [php]
- SHA1 function in PHP

### PHP ECB Mode
**Pattern**: `MCRYPT_MODE_ECB`
**Type**: regex
**Severity**: high
**Languages**: [php]
- ECB mode in PHP

---

## C/C++ Weak Ciphers

### OpenSSL DES Set Key
**Pattern**: `DES_set_key`
**Type**: regex
**Severity**: critical
**Languages**: [c, cpp]
- DES in OpenSSL C API
- CWE-327: Use of a Broken or Risky Cryptographic Algorithm

### OpenSSL DES ECB
**Pattern**: `DES_ecb_encrypt`
**Type**: regex
**Severity**: critical
**Languages**: [c, cpp]
- DES ECB in OpenSSL

### OpenSSL MD5 Init
**Pattern**: `MD5_Init`
**Type**: regex
**Severity**: high
**Languages**: [c, cpp]
- MD5 in OpenSSL C API
- CWE-328: Use of Weak Hash

### OpenSSL SHA1 Init
**Pattern**: `SHA1_Init`
**Type**: regex
**Severity**: medium
**Languages**: [c, cpp]
- SHA1 in OpenSSL C API

### OpenSSL EVP DES
**Pattern**: `EVP_des_`
**Type**: regex
**Severity**: critical
**Languages**: [c, cpp]
- DES EVP functions

### OpenSSL EVP RC4
**Pattern**: `EVP_rc4`
**Type**: regex
**Severity**: critical
**Languages**: [c, cpp]
- RC4 EVP function

### OpenSSL EVP MD5
**Pattern**: `EVP_md5`
**Type**: regex
**Severity**: high
**Languages**: [c, cpp]
- MD5 EVP function

### OpenSSL EVP SHA1
**Pattern**: `EVP_sha1`
**Type**: regex
**Severity**: medium
**Languages**: [c, cpp]
- SHA1 EVP function

---

## Rust Weak Ciphers

### Rust DES Cipher
**Pattern**: `des::Des::new`
**Type**: regex
**Severity**: critical
**Languages**: [rust]
- DES cipher in Rust (des crate)
- CWE-327: Use of a Broken or Risky Cryptographic Algorithm

### Rust Triple DES
**Pattern**: `des::TdesEde[23]::new`
**Type**: regex
**Severity**: high
**Languages**: [rust]
- Triple DES in Rust

### Rust MD5 Crate
**Pattern**: `md5::compute`
**Type**: regex
**Severity**: high
**Languages**: [rust]
- MD5 in Rust (md5 crate)
- CWE-328: Use of Weak Hash

### Rust MD5 Digest
**Pattern**: `Md5::new\(\)`
**Type**: regex
**Severity**: high
**Languages**: [rust]
- MD5 in Rust (md-5/digest crate)

### Rust SHA1 Digest
**Pattern**: `Sha1::new\(\)`
**Type**: regex
**Severity**: medium
**Languages**: [rust]
- SHA1 in Rust (sha-1/digest crate)

### Rust RC4 Cipher
**Pattern**: `rc4::Rc4::new`
**Type**: regex
**Severity**: critical
**Languages**: [rust]
- RC4 in Rust

### Rust Blowfish
**Pattern**: `blowfish::Blowfish::new`
**Type**: regex
**Severity**: high
**Languages**: [rust]
- Blowfish in Rust

### Rust ECB Mode
**Pattern**: `ecb::Encryptor|ecb::Decryptor`
**Type**: regex
**Severity**: high
**Languages**: [rust]
- ECB mode in Rust (block-modes crate)

---

## C# Weak Ciphers

### C# DES Provider
**Pattern**: `DESCryptoServiceProvider`
**Type**: regex
**Severity**: critical
**Languages**: [csharp]
- DES in C#
- CWE-327: Use of a Broken or Risky Cryptographic Algorithm

### C# DES Create
**Pattern**: `DES\.Create\(\)`
**Type**: regex
**Severity**: critical
**Languages**: [csharp]
- DES.Create() in C#

### C# Triple DES
**Pattern**: `TripleDESCryptoServiceProvider`
**Type**: regex
**Severity**: high
**Languages**: [csharp]
- Triple DES in C#

### C# Triple DES Create
**Pattern**: `TripleDES\.Create\(\)`
**Type**: regex
**Severity**: high
**Languages**: [csharp]
- TripleDES.Create() in C#

### C# RC2 Provider
**Pattern**: `RC2CryptoServiceProvider`
**Type**: regex
**Severity**: critical
**Languages**: [csharp]
- RC2 in C#

### C# MD5 Provider
**Pattern**: `MD5CryptoServiceProvider`
**Type**: regex
**Severity**: high
**Languages**: [csharp]
- MD5 in C#
- CWE-328: Use of Weak Hash

### C# MD5 Create
**Pattern**: `MD5\.Create\(\)`
**Type**: regex
**Severity**: high
**Languages**: [csharp]
- MD5.Create() in C#

### C# SHA1 Provider
**Pattern**: `SHA1CryptoServiceProvider`
**Type**: regex
**Severity**: medium
**Languages**: [csharp]
- SHA1 in C#

### C# SHA1 Create
**Pattern**: `SHA1\.Create\(\)`
**Type**: regex
**Severity**: medium
**Languages**: [csharp]
- SHA1.Create() in C#

### C# SHA1 Managed
**Pattern**: `SHA1Managed`
**Type**: regex
**Severity**: medium
**Languages**: [csharp]
- SHA1Managed in C#

### C# ECB Mode
**Pattern**: `CipherMode\.ECB`
**Type**: regex
**Severity**: high
**Languages**: [csharp]
- ECB mode in C#

---

## Hardcoded Keys Detection

### Hardcoded DES Key
**Pattern**: `DES\.new\(['"bx][0-9a-fA-F]{16}['"]`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Hardcoded DES key in source code

### Hardcoded RC4 Key
**Pattern**: `[Rr][Cc]4.*key\s*[=:]\s*['"][^'"]{8,}['"]`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Hardcoded RC4 key in source code

### Hardcoded 3DES Key
**Pattern**: `DES3\.new\(['"bx][0-9a-fA-F]{32,48}['"]`
**Type**: regex
**Severity**: critical
**Languages**: [python]
- Hardcoded Triple DES key in source code

---

## Algorithm Recommendations

### Encryption Algorithms
| Weak/Deprecated | Recommended |
|-----------------|-------------|
| DES | AES-256 |
| 3DES/DESede | AES-256 |
| RC4 | AES-GCM, ChaCha20-Poly1305 |
| Blowfish | AES-256 |
| RC2 | AES-256 |

### Hash Algorithms
| Weak/Deprecated | Recommended |
|-----------------|-------------|
| MD5 | SHA-256, SHA-3, BLAKE2 |
| SHA1 | SHA-256, SHA-3, BLAKE2 |
| MD4 | SHA-256, SHA-3 |

### Block Cipher Modes
| Weak | Recommended |
|------|-------------|
| ECB | GCM, CTR, CBC with HMAC |

---

## References

- [CWE-327: Use of a Broken or Risky Cryptographic Algorithm](https://cwe.mitre.org/data/definitions/327.html)
- [CWE-328: Use of Weak Hash](https://cwe.mitre.org/data/definitions/328.html)
- [NIST SP 800-131A: Transitioning Cryptographic Algorithms](https://csrc.nist.gov/publications/detail/sp/800-131a/rev-2/final)
