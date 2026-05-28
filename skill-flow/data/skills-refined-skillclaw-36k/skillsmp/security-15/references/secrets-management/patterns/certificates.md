# Private Keys and Certificates

**Category**: devops/secrets/certificates
**Description**: Detection patterns for private keys, certificates, and keystores
**CWE**: CWE-798, CWE-321, CWE-312

---

## Private Keys

### RSA Private Key
**Pattern**: `-----BEGIN RSA PRIVATE KEY-----`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Traditional RSA private key format (PKCS#1)
- CWE-321: Use of Hard-coded Cryptographic Key

### Generic Private Key (PKCS#8)
**Pattern**: `-----BEGIN PRIVATE KEY-----`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- PKCS#8 format (can contain RSA, EC, or other key types)

### EC Private Key
**Pattern**: `-----BEGIN EC PRIVATE KEY-----`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Elliptic Curve private keys

### DSA Private Key
**Pattern**: `-----BEGIN DSA PRIVATE KEY-----`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- DSA private keys

### OpenSSH Private Key
**Pattern**: `-----BEGIN OPENSSH PRIVATE KEY-----`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Modern OpenSSH format (since OpenSSH 7.8)

### Encrypted Private Key
**Pattern**: `-----BEGIN ENCRYPTED PRIVATE KEY-----`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Password-protected private keys (still sensitive)

### PuTTY Private Key
**Pattern**: `PuTTY-User-Key-File-[0-9]+:`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- PuTTY PPK format private keys

---

## PGP/GPG Keys

### PGP Private Key Block
**Pattern**: `-----BEGIN PGP PRIVATE KEY BLOCK-----`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- PGP private key blocks

### PGP Secret Key Block
**Pattern**: `-----BEGIN PGP SECRET KEY BLOCK-----`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Older PGP format name for private keys

---

## Certificates (Lower Severity)

### X.509 Certificate
**Pattern**: `-----BEGIN CERTIFICATE-----`
**Type**: regex
**Severity**: informational
**Languages**: [all]
- Public certificates are not secrets
- May indicate private key nearby

### Certificate Request
**Pattern**: `-----BEGIN CERTIFICATE REQUEST-----`
**Type**: regex
**Severity**: informational
**Languages**: [all]
- Certificate signing requests are not secrets

---

## PKCS#12 / PFX Files

### P12/PFX File Extension
**Pattern**: `\.p12$|\.pfx$`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Binary format containing private key and certificate chain
- Often password-protected with weak passwords

---

## SSH Keys

### SSH Private Key Files
**Pattern**: `id_rsa|id_dsa|id_ecdsa|id_ed25519`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Common SSH private key filenames

### SSH Public Key
**Pattern**: `ssh-(rsa|dsa|ecdsa|ed25519) AAAA[A-Za-z0-9+/]+`
**Type**: regex
**Severity**: informational
**Languages**: [all]
- Public keys are not secrets but may indicate private key presence

---

## SSL/TLS Related

### Key File Extension
**Pattern**: `\.key$`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Files often containing private keys
- Investigate content

### PEM File Extension
**Pattern**: `\.pem$`
**Type**: regex
**Severity**: high
**Languages**: [all]
- May contain private key and certificate
- Investigate content

### JKS Keystore Extension
**Pattern**: `\.jks$`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Java KeyStore files (password-protected)

### Keystore Password
**Pattern**: `storepass[=:]["']?[^\s"']+`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Java keystore password in command or config

### Key Password
**Pattern**: `keypass[=:]["']?[^\s"']+`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Java key password in command or config

---

## Code Signing

### Apple P12 Certificate
**Pattern**: `\.p12$`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- iOS/macOS code signing certificates
- Context: Apple development

### Mobile Provisioning Profile
**Pattern**: `\.mobileprovision$`
**Type**: regex
**Severity**: high
**Languages**: [all]
- iOS provisioning profiles

### Android Keystore
**Pattern**: `\.keystore$`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Android app signing keystores

### Android Key Password Env
**Pattern**: `ANDROID_KEY_PASSWORD|KEYSTORE_PASSWORD`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Android signing key passwords in CI/CD

---

## Cloud Certificates

### AWS ACM Certificate ARN
**Pattern**: `arn:aws:acm:[a-z0-9-]+:[0-9]+:certificate/[a-f0-9-]+`
**Type**: regex
**Severity**: informational
**Languages**: [all]
- Reference to ACM certificate, not the cert itself

### Let's Encrypt Private Key Path
**Pattern**: `/etc/letsencrypt/live/[^/]+/privkey\.pem`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Path to Let's Encrypt private keys

---

## Detection Notes

### Critical Files to Flag
- Any file containing `BEGIN.*PRIVATE KEY`
- `.pem` files in non-standard locations
- `.p12`, `.pfx`, `.key` files in repositories
- `id_rsa`, `id_ecdsa` without `.pub` extension

### Common Locations (should not be in repo)
- `~/.ssh/`
- `/etc/ssl/private/`
- `/etc/letsencrypt/`
- `./certs/`, `./keys/`, `./ssl/`

### False Positives
- Documentation about key formats
- Test certificates in test fixtures
- Public certificates (BEGIN CERTIFICATE)
- Empty placeholder files

### Immediate Actions Required
1. **Revoke/rotate** any exposed private key immediately
2. **Check git history** - key may be in old commits
3. **Update certificates** that used exposed keys
4. **Add to .gitignore** to prevent future commits

---

## References

- [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
- [CWE-321: Use of Hard-coded Cryptographic Key](https://cwe.mitre.org/data/definitions/321.html)
- [CWE-312: Cleartext Storage of Sensitive Information](https://cwe.mitre.org/data/definitions/312.html)
