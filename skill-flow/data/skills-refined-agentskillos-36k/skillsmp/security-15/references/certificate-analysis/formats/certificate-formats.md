<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# Certificate Formats Guide

Reference for X.509 certificate encoding formats and conversion between them.

## Format Overview

| Format | Encoding | Extensions | Contains | Usage |
|--------|----------|------------|----------|-------|
| PEM | Base64 | .pem, .crt, .cer, .key | Certs, keys | Most common, text-based |
| DER | Binary | .der, .cer | Single cert | Java, Windows |
| PKCS#7 | Both | .p7b, .p7c | Cert chain | Certificate bundles |
| PKCS#12 | Binary | .p12, .pfx | Cert + key | Key exchange, Windows |
| JKS | Binary | .jks | Cert + key | Java applications |

## PEM Format

**Privacy Enhanced Mail** - Base64 encoded with header/footer markers.

### Structure

```
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAJC1HiIAZAiUMA0Gcz93FGQDFGFDFGdfkjsdlfk
...base64 encoded DER data...
dfKJdlfjeiDFSDFSDfsldkfjKLJDFLKJ==
-----END CERTIFICATE-----
```

### Common Headers

| Type | Header |
|------|--------|
| Certificate | `-----BEGIN CERTIFICATE-----` |
| Private Key (PKCS#8) | `-----BEGIN PRIVATE KEY-----` |
| RSA Private Key | `-----BEGIN RSA PRIVATE KEY-----` |
| EC Private Key | `-----BEGIN EC PRIVATE KEY-----` |
| Encrypted Key | `-----BEGIN ENCRYPTED PRIVATE KEY-----` |
| CSR | `-----BEGIN CERTIFICATE REQUEST-----` |
| Public Key | `-----BEGIN PUBLIC KEY-----` |

### Multiple Certificates

PEM files can contain multiple certificates (chain):

```
-----BEGIN CERTIFICATE-----
(end-entity certificate)
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
(intermediate certificate)
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
(root certificate - optional)
-----END CERTIFICATE-----
```

### OpenSSL Commands

```bash
# View PEM certificate
openssl x509 -in cert.pem -text -noout

# Convert PEM to DER
openssl x509 -in cert.pem -outform DER -out cert.der

# Extract certificate from PEM with key
openssl x509 -in combined.pem -out cert.pem

# Extract key from PEM with certificate
openssl pkey -in combined.pem -out key.pem
```

## DER Format

**Distinguished Encoding Rules** - Binary ASN.1 encoding.

### Characteristics

- Binary format (not human-readable)
- Single certificate per file
- Compact size
- No headers/footers
- Starts with byte 0x30 (SEQUENCE tag)

### Magic Bytes

```
30 82 xx xx  (SEQUENCE, length > 127 bytes)
30 xx        (SEQUENCE, length ≤ 127 bytes)
```

### OpenSSL Commands

```bash
# View DER certificate
openssl x509 -in cert.der -inform DER -text -noout

# Convert DER to PEM
openssl x509 -in cert.der -inform DER -outform PEM -out cert.pem

# Check if file is DER
xxd -l 4 cert.der
# Should show: 30 82 xx xx
```

## PKCS#7 / P7B Format

**Cryptographic Message Syntax** - Certificate bundles without private keys.

### Characteristics

- Contains certificate chain (no private keys)
- Can be PEM or DER encoded
- Used for certificate distribution
- Common in Windows/IIS environments

### Structure (PEM encoded)

```
-----BEGIN PKCS7-----
MIIGfQYJKoZIhvcNAQcCoIIGbjCCBmoCAQExADALBgkqhkiG9w0BBwGgggZSMIID
...base64 encoded data...
-----END PKCS7-----
```

### OpenSSL Commands

```bash
# View PKCS7 certificates
openssl pkcs7 -in bundle.p7b -print_certs -noout

# Extract certificates from PKCS7
openssl pkcs7 -in bundle.p7b -print_certs -out certs.pem

# Convert PEM chain to PKCS7
openssl crl2pkcs7 -nocrl -certfile chain.pem -out bundle.p7b

# View DER-encoded PKCS7
openssl pkcs7 -in bundle.p7b -inform DER -print_certs
```

## PKCS#12 / PFX Format

**Personal Information Exchange** - Certificate with private key.

### Characteristics

- Contains certificate AND private key
- Password protected
- Binary format only
- Common for certificate backup/transfer
- Windows "Personal Information Exchange"

### Contents

- End-entity certificate
- Private key (encrypted)
- Certificate chain (optional)
- Friendly names/aliases

### OpenSSL Commands

```bash
# View PKCS12 contents
openssl pkcs12 -in keystore.p12 -info -noout

# Extract certificate
openssl pkcs12 -in keystore.p12 -clcerts -nokeys -out cert.pem

# Extract private key
openssl pkcs12 -in keystore.p12 -nocerts -out key.pem

# Extract all (cert + key)
openssl pkcs12 -in keystore.p12 -out all.pem

# Create PKCS12 from PEM
openssl pkcs12 -export -in cert.pem -inkey key.pem -out keystore.p12

# Create PKCS12 with chain
openssl pkcs12 -export -in cert.pem -inkey key.pem -certfile chain.pem -out keystore.p12

# Create PKCS12 with friendly name
openssl pkcs12 -export -in cert.pem -inkey key.pem -name "my-cert" -out keystore.p12
```

## Java KeyStore (JKS)

**Java-specific format** - Deprecated in favor of PKCS#12.

### Characteristics

- Java-proprietary format
- Password protected
- Contains certificates and/or keys
- Being replaced by PKCS#12 (JDK 9+)

### keytool Commands

```bash
# List keystore contents
keytool -list -keystore keystore.jks

# View certificate details
keytool -list -v -keystore keystore.jks -alias mycert

# Import certificate
keytool -import -alias mycert -file cert.pem -keystore keystore.jks

# Export certificate
keytool -export -alias mycert -file cert.der -keystore keystore.jks

# Convert JKS to PKCS12
keytool -importkeystore -srckeystore keystore.jks -destkeystore keystore.p12 -deststoretype PKCS12

# Convert PKCS12 to JKS
keytool -importkeystore -srckeystore keystore.p12 -srcstoretype PKCS12 -destkeystore keystore.jks
```

## Format Detection

### By File Extension

| Extension | Likely Format |
|-----------|--------------|
| .pem | PEM |
| .crt, .cer | PEM or DER |
| .der | DER |
| .p7b, .p7c | PKCS#7 |
| .p12, .pfx | PKCS#12 |
| .jks | Java KeyStore |
| .key | PEM (private key) |

### By Content

```bash
# Check if text (PEM) or binary (DER/PKCS12)
file cert.unknown

# Check first bytes
xxd -l 10 cert.unknown

# Try to parse as different formats
openssl x509 -in cert.unknown -text -noout 2>/dev/null && echo "PEM cert"
openssl x509 -in cert.unknown -inform DER -text -noout 2>/dev/null && echo "DER cert"
openssl pkcs7 -in cert.unknown -print_certs 2>/dev/null && echo "PKCS7"
openssl pkcs12 -in cert.unknown -info -noout 2>/dev/null && echo "PKCS12"
```

### Programmatic Detection

```bash
# Check for PEM headers
grep -q "BEGIN CERTIFICATE" file && echo "PEM format"

# Check for PKCS7 header
grep -q "BEGIN PKCS7" file && echo "PKCS7 PEM format"

# Check DER magic bytes (0x30 = SEQUENCE)
[[ $(xxd -p -l 1 file) == "30" ]] && echo "Likely DER or binary format"
```

## Format Conversion Matrix

### From PEM

| To | Command |
|----|---------|
| DER | `openssl x509 -in cert.pem -outform DER -out cert.der` |
| PKCS#7 | `openssl crl2pkcs7 -nocrl -certfile cert.pem -out cert.p7b` |
| PKCS#12 | `openssl pkcs12 -export -in cert.pem -inkey key.pem -out cert.p12` |

### From DER

| To | Command |
|----|---------|
| PEM | `openssl x509 -in cert.der -inform DER -outform PEM -out cert.pem` |
| PKCS#7 | Convert to PEM first, then to PKCS#7 |
| PKCS#12 | Convert to PEM first, then to PKCS#12 |

### From PKCS#7

| To | Command |
|----|---------|
| PEM | `openssl pkcs7 -in cert.p7b -print_certs -out cert.pem` |
| DER | Extract to PEM, then convert to DER |

### From PKCS#12

| To | Command |
|----|---------|
| PEM (cert) | `openssl pkcs12 -in cert.p12 -clcerts -nokeys -out cert.pem` |
| PEM (key) | `openssl pkcs12 -in cert.p12 -nocerts -out key.pem` |
| PEM (all) | `openssl pkcs12 -in cert.p12 -out all.pem` |

## Best Practices

1. **Use PEM for servers**: Most compatible, easy to manage
2. **Use PKCS#12 for transfer**: Contains both cert and key
3. **Avoid JKS for new projects**: Use PKCS#12 instead
4. **Secure private keys**: Encrypt when storing/transferring
5. **Include full chain**: Include intermediates in bundles
6. **Validate after conversion**: Verify certificate works after converting

## Common Issues

### Wrong Format Error

```
unable to load certificate
```
**Solution**: Try different `-inform` option (PEM vs DER)

### Password Required

```
Mac verify error: invalid password?
```
**Solution**: Provide correct password with `-passin`

### Missing Private Key

```
No private key found
```
**Solution**: PEM file doesn't contain key; need separate key file

### Chain Incomplete

**Solution**: Include intermediate certificates in PKCS#7/PKCS#12
