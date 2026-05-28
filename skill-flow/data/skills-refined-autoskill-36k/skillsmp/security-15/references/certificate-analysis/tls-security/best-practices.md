<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# TLS Security Best Practices

Reference for TLS configuration, security assessment, and best practices.

## TLS Version Overview

| Version | Status | Recommendation |
|---------|--------|----------------|
| SSL 2.0 | Deprecated | DISABLED - Insecure |
| SSL 3.0 | Deprecated | DISABLED - POODLE vulnerable |
| TLS 1.0 | Deprecated | DISABLED - PCI DSS non-compliant |
| TLS 1.1 | Deprecated | DISABLED - Weak ciphers |
| TLS 1.2 | Current | ENABLED - With secure ciphers |
| TLS 1.3 | Current | ENABLED - Preferred |

## TLS 1.3 Improvements

### Key Changes from TLS 1.2

1. **Simplified Handshake**: 1-RTT (or 0-RTT resumption)
2. **Removed Legacy Ciphers**: No RC4, DES, 3DES, MD5, SHA-1
3. **Forward Secrecy Required**: All cipher suites use ephemeral keys
4. **Encrypted Handshake**: More of the handshake is encrypted
5. **Removed Compression**: Eliminates CRIME/BREACH attacks
6. **Simplified Cipher Suites**: Only 5 cipher suites

### TLS 1.3 Cipher Suites

```
TLS_AES_256_GCM_SHA384        (0x13,0x02) - Recommended
TLS_AES_128_GCM_SHA256        (0x13,0x01) - Recommended
TLS_CHACHA20_POLY1305_SHA256  (0x13,0x03) - Recommended
TLS_AES_128_CCM_SHA256        (0x13,0x04) - Less common
TLS_AES_128_CCM_8_SHA256      (0x13,0x05) - IoT use
```

## Cipher Suite Selection

### Recommended TLS 1.2 Cipher Suites

**Priority Order**:
```
ECDHE-ECDSA-AES256-GCM-SHA384
ECDHE-RSA-AES256-GCM-SHA384
ECDHE-ECDSA-CHACHA20-POLY1305
ECDHE-RSA-CHACHA20-POLY1305
ECDHE-ECDSA-AES128-GCM-SHA256
ECDHE-RSA-AES128-GCM-SHA256
DHE-RSA-AES256-GCM-SHA384
DHE-RSA-AES128-GCM-SHA256
```

### Cipher Suite Components

| Component | Secure Options | Avoid |
|-----------|----------------|-------|
| Key Exchange | ECDHE, DHE | RSA, DH (static) |
| Authentication | ECDSA, RSA | DSS, anonymous |
| Bulk Encryption | AES-GCM, ChaCha20 | RC4, DES, 3DES, CBC mode |
| MAC | SHA-256, SHA-384, Poly1305 | MD5, SHA-1 |

### OpenSSL Cipher String

```bash
# Modern configuration (TLS 1.2+)
ECDHE+AESGCM:DHE+AESGCM:ECDHE+CHACHA20:DHE+CHACHA20:!aNULL:!MD5:!DSS

# Testing cipher configuration
openssl ciphers -v 'ECDHE+AESGCM:DHE+AESGCM'
```

## Server Configuration

### Nginx

```nginx
# TLS Configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
ssl_prefer_server_ciphers off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /path/to/chain.pem;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;

# Session Configuration
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;

# DH Parameters (if using DHE)
ssl_dhparam /path/to/dhparam.pem;

# Certificate
ssl_certificate /path/to/fullchain.pem;
ssl_certificate_key /path/to/privkey.pem;
```

### Apache

```apache
# TLS Configuration
SSLProtocol -all +TLSv1.2 +TLSv1.3
SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
SSLHonorCipherOrder off

# OCSP Stapling
SSLUseStapling On
SSLStaplingCache shmcb:/var/run/ocsp(128000)
SSLStaplingResponderTimeout 5
SSLStaplingReturnResponderErrors off

# Session Configuration
SSLSessionCache shmcb:/var/run/ssl_scache(512000)
SSLSessionCacheTimeout 300

# Certificate
SSLCertificateFile /path/to/cert.pem
SSLCertificateKeyFile /path/to/privkey.pem
SSLCertificateChainFile /path/to/chain.pem
```

## Security Headers

### HSTS (HTTP Strict Transport Security)

Forces HTTPS connections and prevents downgrade attacks.

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

**Components**:
- `max-age`: Seconds to remember HTTPS-only (31536000 = 1 year)
- `includeSubDomains`: Apply to all subdomains
- `preload`: Submit to browser preload list

**Nginx**:
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

**Apache**:
```apache
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
```

### Certificate Transparency Expect-CT

```
Expect-CT: max-age=86400, enforce, report-uri="https://example.com/ct-report"
```

**Note**: Being deprecated as CT is now mandatory.

## StartTLS Protocols

### Protocol Support Matrix

| Protocol | Port | StartTLS Command |
|----------|------|------------------|
| SMTP | 25, 587 | `STARTTLS` |
| IMAP | 143 | `STARTTLS` |
| POP3 | 110 | `STLS` |
| LDAP | 389 | StartTLS extension |
| FTP | 21 | `AUTH TLS` |
| XMPP | 5222 | `<starttls>` |
| MySQL | 3306 | `mysql` |
| PostgreSQL | 5432 | `postgres` |

### OpenSSL StartTLS Commands

```bash
# SMTP
openssl s_client -connect mail.example.com:587 -starttls smtp

# IMAP
openssl s_client -connect mail.example.com:143 -starttls imap

# POP3
openssl s_client -connect mail.example.com:110 -starttls pop3

# LDAP
openssl s_client -connect ldap.example.com:389 -starttls ldap

# FTP
openssl s_client -connect ftp.example.com:21 -starttls ftp

# MySQL
openssl s_client -connect db.example.com:3306 -starttls mysql

# PostgreSQL
openssl s_client -connect db.example.com:5432 -starttls postgres
```

## Common Vulnerabilities

### BEAST (Browser Exploit Against SSL/TLS)

- **Affected**: TLS 1.0 CBC ciphers
- **Mitigation**: Use TLS 1.2+ or GCM ciphers
- **Status**: Mitigated in modern browsers

### POODLE (Padding Oracle On Downgraded Legacy Encryption)

- **Affected**: SSL 3.0, TLS 1.0-1.2 CBC ciphers
- **Mitigation**: Disable SSL 3.0, use GCM ciphers
- **Status**: Critical vulnerability

### CRIME/BREACH

- **Affected**: TLS compression, HTTP compression with secrets
- **Mitigation**: Disable TLS compression
- **Status**: TLS compression disabled by default

### Heartbleed

- **Affected**: OpenSSL 1.0.1 - 1.0.1f
- **Mitigation**: Update OpenSSL
- **Status**: Patched in OpenSSL 1.0.1g+

### ROBOT (Return Of Bleichenbacher's Oracle Threat)

- **Affected**: RSA key exchange
- **Mitigation**: Disable RSA key exchange, use ECDHE
- **Status**: Use forward secrecy

### DROWN (Decrypting RSA with Obsolete and Weakened eNcryption)

- **Affected**: Servers supporting SSLv2
- **Mitigation**: Disable SSLv2 completely
- **Status**: SSLv2 should never be enabled

## Testing Tools

### OpenSSL Commands

```bash
# Test TLS connection
openssl s_client -connect example.com:443 -servername example.com

# Test specific TLS version
openssl s_client -connect example.com:443 -tls1_2
openssl s_client -connect example.com:443 -tls1_3

# List supported ciphers
openssl s_client -connect example.com:443 -cipher 'ALL' 2>/dev/null | grep Cipher

# Check certificate chain
openssl s_client -connect example.com:443 -showcerts

# Check OCSP stapling
openssl s_client -connect example.com:443 -status

# Test session resumption
openssl s_client -connect example.com:443 -reconnect
```

### Testing Services

| Service | URL | Description |
|---------|-----|-------------|
| SSL Labs | https://www.ssllabs.com/ssltest/ | Comprehensive TLS testing |
| testssl.sh | https://testssl.sh/ | Command-line testing tool |
| Hardenize | https://www.hardenize.com/ | Security assessment |
| SSL Checker | https://www.sslshopper.com/ssl-checker.html | Quick certificate check |
| Observatory | https://observatory.mozilla.org/ | Mozilla security scan |

## Certificate Chain Validation

### Chain Order

Correct chain order (leaf first):
```
1. End-entity certificate (your certificate)
2. Intermediate CA certificate(s)
3. Root CA certificate (optional, usually in trust store)
```

### Validation Steps

1. **Signature Verification**: Each certificate signed by issuer
2. **Validity Period**: All certificates within validity
3. **Name Chaining**: Subject matches issuer of next cert
4. **Trust Anchor**: Chain terminates at trusted root
5. **Revocation Check**: OCSP/CRL verification

### OpenSSL Chain Verification

```bash
# Verify certificate chain
openssl verify -CAfile ca-bundle.crt -untrusted intermediate.crt server.crt

# Check chain from server
openssl s_client -connect example.com:443 -showcerts 2>/dev/null | \
    openssl x509 -noout -issuer -subject

# Verify against system trust store
openssl verify -CApath /etc/ssl/certs server.crt
```

## Key Management

### Private Key Security

1. **Generate Strong Keys**:
   ```bash
   # RSA 4096-bit
   openssl genrsa -out key.pem 4096

   # ECDSA P-384
   openssl ecparam -genkey -name secp384r1 -out key.pem
   ```

2. **Protect Private Keys**:
   - Store in secure location with restricted permissions
   - Use HSM for high-security environments
   - Encrypt keys at rest

3. **Key Rotation**:
   - Rotate keys with each certificate renewal
   - Plan for emergency key rotation

### DH Parameters

Generate strong DH parameters for DHE cipher suites:

```bash
# Generate 4096-bit DH parameters (slow but secure)
openssl dhparam -out dhparam.pem 4096

# Generate 2048-bit DH parameters (minimum)
openssl dhparam -out dhparam.pem 2048
```

## Monitoring and Alerting

### Certificate Expiry

- Alert at 30 days before expiry
- Warning at 14 days
- Critical at 7 days

### CT Log Monitoring

Monitor Certificate Transparency logs for unauthorized certificates:

- crt.sh: https://crt.sh/
- Google CT Search: https://transparencyreport.google.com/https/certificates
- Facebook CT Monitor: https://developers.facebook.com/tools/ct/

### OCSP Failures

Monitor OCSP responder availability and response times.

## Compliance Requirements

### PCI DSS

- TLS 1.2 minimum (TLS 1.0/1.1 deprecated)
- Strong cipher suites
- Regular vulnerability scanning

### HIPAA

- Encryption in transit required
- Strong key management
- Audit logging

### NIST Guidelines

- SP 800-52 Rev. 2: TLS Guidelines
- TLS 1.2 minimum, TLS 1.3 preferred
- Approved cipher suites only

## Best Practices Summary

### Do

- Enable TLS 1.2 and TLS 1.3 only
- Use ECDHE key exchange for forward secrecy
- Use AES-GCM or ChaCha20-Poly1305 encryption
- Enable OCSP stapling
- Implement HSTS with long max-age
- Monitor certificate expiry
- Use strong keys (RSA 2048+, ECDSA P-256+)
- Validate certificate chains completely

### Don't

- Enable SSL 2.0, SSL 3.0, TLS 1.0, TLS 1.1
- Use RSA key exchange (no forward secrecy)
- Use CBC mode ciphers (prefer GCM)
- Use MD5 or SHA-1 for signatures
- Ignore certificate warnings
- Use self-signed certificates in production
- Expose private keys
- Use weak DH parameters

## References

- RFC 8446: TLS 1.3
- RFC 5246: TLS 1.2
- RFC 7525: TLS Best Current Practices
- NIST SP 800-52 Rev. 2: TLS Guidelines
- Mozilla SSL Configuration Generator: https://ssl-config.mozilla.org/
- SSL Labs Best Practices: https://github.com/ssllabs/research/wiki/SSL-and-TLS-Deployment-Best-Practices
