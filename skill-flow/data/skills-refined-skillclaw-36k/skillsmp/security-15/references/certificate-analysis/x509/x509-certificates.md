<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# X.509 Certificate Guide

Comprehensive reference for X.509 digital certificate structure, extensions, and validation.

## Overview

X.509 is an ITU-T standard defining the format of public key certificates. These certificates are used in TLS/SSL, code signing, email encryption (S/MIME), and many other security applications.

## Certificate Structure

An X.509 v3 certificate contains three main sections:

```
Certificate
├── tbsCertificate (To Be Signed)
│   ├── Version
│   ├── Serial Number
│   ├── Signature Algorithm
│   ├── Issuer
│   ├── Validity
│   │   ├── Not Before
│   │   └── Not After
│   ├── Subject
│   ├── Subject Public Key Info
│   │   ├── Algorithm
│   │   └── Public Key
│   └── Extensions
├── Signature Algorithm
└── Signature Value
```

### Version

- **v1 (0)**: Original version, no extensions
- **v2 (1)**: Added issuer/subject unique identifiers (rarely used)
- **v3 (2)**: Added extensions (current standard)

### Serial Number

- Unique identifier within a CA's domain
- Must be positive integer
- Maximum 20 octets
- Used for certificate revocation

### Issuer and Subject

Distinguished Names (DNs) identifying the certificate authority and certificate holder:

| Attribute | OID | Description |
|-----------|-----|-------------|
| CN | 2.5.4.3 | Common Name |
| O | 2.5.4.10 | Organization |
| OU | 2.5.4.11 | Organizational Unit |
| C | 2.5.4.6 | Country (2-letter code) |
| ST | 2.5.4.8 | State/Province |
| L | 2.5.4.7 | Locality |
| E | 1.2.840.113549.1.9.1 | Email Address |

Example DN:
```
CN=www.example.com, O=Example Inc., L=San Francisco, ST=California, C=US
```

### Validity Period

Two timestamps defining when the certificate is valid:

- **Not Before**: Certificate is not valid before this time
- **Not After**: Certificate expires after this time

Format: UTCTime or GeneralizedTime

### Public Key Information

Contains the public key and its algorithm:

**RSA Keys**:
- Modulus (n) and public exponent (e)
- Common sizes: 2048, 3072, 4096 bits
- Minimum for public trust: 2048 bits

**ECC Keys** (Elliptic Curve):
- Curve parameters and public point
- Common curves: P-256 (secp256r1), P-384, P-521
- Minimum for public trust: P-256

**EdDSA Keys**:
- Ed25519 or Ed448
- Modern alternative to ECDSA

## Certificate Extensions

Extensions provide additional information and constraints. Each extension has:

- **OID**: Unique identifier
- **Critical flag**: If true, certificate must be rejected if extension is not understood
- **Value**: Extension-specific data

### Subject Alternative Name (SAN)

**OID**: 2.5.29.17

Primary way to specify identities (domains, IPs, emails):

```
X509v3 Subject Alternative Name:
    DNS:www.example.com, DNS:example.com, DNS:*.example.com
    IP Address:192.168.1.1
    email:admin@example.com
```

**Types**:
- `dNSName`: Domain names
- `iPAddress`: IP addresses (v4 or v6)
- `rfc822Name`: Email addresses
- `uniformResourceIdentifier`: URIs

**Requirements**:
- MUST be present in publicly trusted certificates
- Should include all domain names the certificate covers
- Wildcards only valid in leftmost label

### Basic Constraints

**OID**: 2.5.29.19

Indicates if certificate is a CA and path length constraints:

```
X509v3 Basic Constraints: critical
    CA:TRUE, pathlen:0
```

- **CA**: TRUE for CA certificates, FALSE (or absent) for end-entity
- **pathlen**: Maximum number of intermediate CAs allowed below this CA
- **Critical**: MUST be critical for CA certificates

### Key Usage

**OID**: 2.5.29.15

Defines allowed cryptographic operations:

| Bit | Name | Purpose |
|-----|------|---------|
| 0 | digitalSignature | Signing (TLS, code signing) |
| 1 | nonRepudiation | Non-repudiation signatures |
| 2 | keyEncipherment | RSA key exchange |
| 3 | dataEncipherment | Encrypting data (rare) |
| 4 | keyAgreement | DH/ECDH key exchange |
| 5 | keyCertSign | Signing certificates (CA only) |
| 6 | cRLSign | Signing CRLs |
| 7 | encipherOnly | With keyAgreement |
| 8 | decipherOnly | With keyAgreement |

**TLS Server Certificate**:
```
Key Usage: critical
    Digital Signature, Key Encipherment
```

**CA Certificate**:
```
Key Usage: critical
    Certificate Sign, CRL Sign
```

### Extended Key Usage (EKU)

**OID**: 2.5.29.37

Specifies application purposes:

| OID | Name | Purpose |
|-----|------|---------|
| 1.3.6.1.5.5.7.3.1 | serverAuth | TLS server |
| 1.3.6.1.5.5.7.3.2 | clientAuth | TLS client |
| 1.3.6.1.5.5.7.3.3 | codeSigning | Code signing |
| 1.3.6.1.5.5.7.3.4 | emailProtection | S/MIME |
| 1.3.6.1.5.5.7.3.8 | timeStamping | Timestamping |
| 1.3.6.1.5.5.7.3.9 | OCSPSigning | OCSP responses |

```
Extended Key Usage:
    TLS Web Server Authentication, TLS Web Client Authentication
```

### Authority Key Identifier (AKI)

**OID**: 2.5.29.35

Identifies the issuing CA's public key:

```
X509v3 Authority Key Identifier:
    keyid:A8:4A:6A:63:04:7D:DD:BA:E6:D1:39:B7:A6:45:65:EF:F3:A8:EC:A1
```

Used to build certificate chains.

### Subject Key Identifier (SKI)

**OID**: 2.5.29.14

Hash of the certificate's public key:

```
X509v3 Subject Key Identifier:
    B3:2D:74:22:8C:D6:85:F4:87:A5:A3:CE:AA:48:85:3B:9C:11:FF:2B
```

Used to match certificates with their issuer.

### CRL Distribution Points

**OID**: 2.5.29.31

URLs where Certificate Revocation Lists can be found:

```
X509v3 CRL Distribution Points:
    Full Name:
        URI:http://crl.example.com/ca.crl
```

### Authority Information Access (AIA)

**OID**: 1.3.6.1.5.5.7.1.1

URLs for OCSP responders and CA certificate retrieval:

```
Authority Information Access:
    OCSP - URI:http://ocsp.example.com
    CA Issuers - URI:http://crt.example.com/intermediate.crt
```

### Certificate Policies

**OID**: 2.5.29.32

Identifies the certificate policy under which it was issued:

```
X509v3 Certificate Policies:
    Policy: 2.23.140.1.2.1 (DV)
    Policy: 2.23.140.1.2.2 (OV)
    Policy: 2.23.140.1.1 (EV)
```

**Common Policy OIDs**:
- 2.23.140.1.2.1: Domain Validated (DV)
- 2.23.140.1.2.2: Organization Validated (OV)
- 2.23.140.1.1: Extended Validation (EV)

### CT Precertificate SCTs

**OID**: 1.3.6.1.4.1.11129.2.4.2

Signed Certificate Timestamps for Certificate Transparency:

```
CT Precertificate SCTs:
    Signed Certificate Timestamp:
        Version: v1
        Log ID: CF:11:56:EE:D5:2E:7C:AF:F3:87:5B:D9:69:2E:9B:E9
        Timestamp: Nov 25 00:00:00.000 2024 UTC
        Signature Algorithm: sha256ECDSA
```

## Certificate Types

### Domain Validated (DV)

- Validates domain ownership only
- Fastest issuance (minutes)
- Lowest cost (often free)
- No organization information
- Example: Let's Encrypt

### Organization Validated (OV)

- Validates domain ownership AND organization identity
- Medium validation time (1-3 days)
- Organization name in certificate
- Moderate cost
- Shows "O=" field in subject

### Extended Validation (EV)

- Strictest validation
- Extensive organization verification
- Legal existence verification
- Longest validation time (1-2 weeks)
- Highest cost
- Distinguished by policy OID: 2.23.140.1.1

## Certificate Chains

Certificates form trust hierarchies:

```
Root CA (self-signed, trusted by OS/browser)
    └── Intermediate CA 1
            └── Intermediate CA 2
                    └── End-Entity Certificate (your server)
```

**Chain Validation**:
1. Start with end-entity certificate
2. Find issuer certificate (using AKI → SKI matching)
3. Verify signature on child certificate using parent's public key
4. Check validity, revocation, constraints
5. Continue until reaching trusted root

**Common Issues**:
- Missing intermediate certificates
- Expired certificates in chain
- Wrong certificate order
- Untrusted root

## Signature Algorithms

### RSA Signatures

| Algorithm | OID | Status |
|-----------|-----|--------|
| sha256WithRSAEncryption | 1.2.840.113549.1.1.11 | Recommended |
| sha384WithRSAEncryption | 1.2.840.113549.1.1.12 | Strong |
| sha512WithRSAEncryption | 1.2.840.113549.1.1.13 | Strong |
| sha1WithRSAEncryption | 1.2.840.113549.1.1.5 | **DEPRECATED** |
| md5WithRSAEncryption | 1.2.840.113549.1.1.4 | **PROHIBITED** |

### ECDSA Signatures

| Algorithm | OID | Status |
|-----------|-----|--------|
| ecdsa-with-SHA256 | 1.2.840.10045.4.3.2 | Recommended |
| ecdsa-with-SHA384 | 1.2.840.10045.4.3.3 | Strong |
| ecdsa-with-SHA512 | 1.2.840.10045.4.3.4 | Strong |

### EdDSA Signatures

| Algorithm | OID | Status |
|-----------|-----|--------|
| Ed25519 | 1.3.101.112 | Modern |
| Ed448 | 1.3.101.113 | Modern |

## OpenSSL Commands

### View Certificate

```bash
# View PEM certificate
openssl x509 -in cert.pem -text -noout

# View DER certificate
openssl x509 -in cert.der -inform DER -text -noout

# View remote certificate
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -text -noout
```

### Extract Information

```bash
# Subject
openssl x509 -in cert.pem -noout -subject

# Issuer
openssl x509 -in cert.pem -noout -issuer

# Dates
openssl x509 -in cert.pem -noout -dates

# Serial
openssl x509 -in cert.pem -noout -serial

# Fingerprint
openssl x509 -in cert.pem -noout -fingerprint -sha256

# Public key
openssl x509 -in cert.pem -noout -pubkey
```

### Verify Certificate

```bash
# Verify against CA bundle
openssl verify -CAfile ca-bundle.pem cert.pem

# Verify with intermediate
openssl verify -CAfile ca-bundle.pem -untrusted intermediate.pem cert.pem

# Check certificate chain
openssl verify -show_chain -CAfile ca-bundle.pem cert.pem
```

## Common Issues and Solutions

### Issue: Certificate Not Trusted

**Symptoms**: Browser shows security warning

**Causes**:
1. Self-signed certificate
2. Missing intermediate certificates
3. Expired root CA
4. Root CA not in trust store

**Solutions**:
1. Use publicly trusted CA
2. Include full certificate chain
3. Update trust store
4. Add custom CA to trust store

### Issue: Name Mismatch

**Symptoms**: "Certificate does not match domain"

**Causes**:
1. Wrong domain in certificate
2. Missing SAN entry
3. Wildcard doesn't match subdomain depth

**Solutions**:
1. Issue certificate with correct domain(s)
2. Include all domains in SAN
3. Use separate certificate for multi-level subdomains

### Issue: Certificate Expired

**Symptoms**: "Certificate has expired"

**Causes**:
1. Not renewed before expiry
2. Time sync issues on server

**Solutions**:
1. Renew certificate
2. Implement automated renewal
3. Fix server time synchronization

### Issue: Weak Key

**Symptoms**: Security scan shows weak key

**Causes**:
1. RSA key < 2048 bits
2. Using deprecated algorithms

**Solutions**:
1. Generate new key with >= 2048 bits
2. Use modern algorithms (SHA-256+)

## Best Practices

1. **Use strong keys**: RSA 2048+ or ECC P-256+
2. **Use SHA-256 or stronger**: Never SHA-1 for new certificates
3. **Short validity**: 90-398 days maximum
4. **Include SANs**: Always use SAN, CN alone is deprecated
5. **Protect private keys**: Secure storage, limited access
6. **Automate renewal**: Use ACME/Let's Encrypt
7. **Monitor expiry**: Set up alerts well in advance
8. **Complete chains**: Always include intermediate certificates

## References

- RFC 5280: Internet X.509 PKI Certificate and CRL Profile
- RFC 6818: Updates to the Internet X.509 PKI Certificate Profile
- RFC 8398: Internationalized Email Addresses in X.509 Certificates
- CA/Browser Forum Baseline Requirements
