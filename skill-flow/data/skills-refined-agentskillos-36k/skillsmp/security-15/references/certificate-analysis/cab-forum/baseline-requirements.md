<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# CA/Browser Forum Baseline Requirements

Comprehensive reference for CA/Browser Forum Baseline Requirements (BR) compliance.

## Overview

The CA/Browser Forum is an industry body that establishes standards for publicly trusted TLS/SSL certificates. The Baseline Requirements define the minimum standards that CAs must follow when issuing publicly trusted certificates.

**Current Version**: Baseline Requirements v2.0.x (2024)
**Official Source**: https://cabforum.org/baseline-requirements/

## Key Requirements

### 1. Certificate Validity Period

**Requirement**: Maximum 398 days (effective September 1, 2020)

| Issue Date | Maximum Validity |
|------------|-----------------|
| Before March 1, 2018 | 39 months (1185 days) |
| March 1, 2018 - Aug 31, 2020 | 825 days |
| After September 1, 2020 | 398 days |

**Future Changes**:
- Apple announced intent to reduce to 45 days by 2027
- Industry moving toward shorter validity periods

**Compliance Check**:
```bash
# Check validity period
openssl x509 -in cert.pem -noout -dates
# Calculate days between Not Before and Not After
```

### 2. Key Size Requirements

**RSA Keys**:
| Key Size | Status |
|----------|--------|
| 4096 bits | Recommended |
| 3072 bits | Strong |
| 2048 bits | Minimum required |
| < 2048 bits | PROHIBITED |

**ECDSA Keys**:
| Curve | Status |
|-------|--------|
| P-521 | Strong |
| P-384 | Strong |
| P-256 | Minimum required |
| < P-256 | PROHIBITED |

**Compliance Check**:
```bash
# Check key size
openssl x509 -in cert.pem -noout -text | grep "Public-Key"
```

### 3. Signature Algorithm Requirements

**Prohibited Algorithms**:
- MD2, MD4, MD5
- SHA-1 (since January 1, 2017)

**Allowed Algorithms**:
- SHA-256 (sha256WithRSAEncryption, ecdsa-with-SHA256)
- SHA-384 (sha384WithRSAEncryption, ecdsa-with-SHA384)
- SHA-512 (sha512WithRSAEncryption, ecdsa-with-SHA512)

**Compliance Check**:
```bash
# Check signature algorithm
openssl x509 -in cert.pem -noout -text | grep "Signature Algorithm"
```

### 4. Subject Alternative Name (SAN)

**Requirements**:
- SAN extension MUST be present
- All FQDN(s) MUST be in SAN
- CN is deprecated but may still appear
- Wildcard certificates allowed with restrictions

**Wildcard Restrictions**:
- Only in leftmost label: `*.example.com` (valid)
- Not multi-level: `*.*.example.com` (invalid)
- Not registry-controlled: `*.com` (invalid)

**Compliance Check**:
```bash
# Check SAN extension
openssl x509 -in cert.pem -noout -text | grep -A1 "Subject Alternative Name"
```

### 5. Basic Constraints

**For CA Certificates**:
- Basic Constraints MUST be present
- MUST be marked critical
- CA:TRUE MUST be set
- pathLenConstraint should be appropriate

**For End-Entity Certificates**:
- Basic Constraints SHOULD be present
- CA:FALSE or absent

**Compliance Check**:
```bash
# Check Basic Constraints
openssl x509 -in cert.pem -noout -text | grep -A2 "Basic Constraints"
```

### 6. Key Usage

**TLS Server Certificates**:
- digitalSignature MUST be present
- keyEncipherment (RSA) or keyAgreement (ECDSA)
- SHOULD be marked critical

**CA Certificates**:
- keyCertSign MUST be present
- cRLSign SHOULD be present
- MUST be marked critical

### 7. Extended Key Usage

**TLS Server Certificates**:
- id-kp-serverAuth (1.3.6.1.5.5.7.3.1) MUST be present
- id-kp-clientAuth (1.3.6.1.5.5.7.3.2) MAY be present
- MUST NOT contain anyExtendedKeyUsage

**CA Certificates**:
- Should not contain EKU (or should be restricted)

### 8. Certificate Transparency

**Requirements** (as of April 2018):
- All publicly trusted certificates MUST have SCTs
- At least 2 SCTs from different CT logs required
- SCTs can be embedded, delivered via TLS extension, or OCSP stapling

**CT Log Requirements**:
- Logs must be qualified by browser programs
- Different logs operated by different organizations

**Compliance Check**:
```bash
# Check for SCT extension (OID: 1.3.6.1.4.1.11129.2.4.2)
openssl x509 -in cert.pem -noout -text | grep -i "1.3.6.1.4.1.11129"
```

### 9. OCSP and CRL

**OCSP Requirements**:
- OCSP responder URL MUST be included in AIA
- OCSP responses MUST be signed
- Response validity: max 10 days

**CRL Requirements**:
- CRL Distribution Point SHOULD be present
- CRL validity: max 10 days for end-entity, 12 months for CA

**OCSP Stapling**:
- Servers SHOULD support OCSP stapling
- OCSP Must-Staple extension available

### 10. Certificate Policies

**Required Policy OIDs**:
| Type | OID | Description |
|------|-----|-------------|
| DV | 2.23.140.1.2.1 | Domain Validated |
| OV | 2.23.140.1.2.2 | Organization Validated |
| EV | 2.23.140.1.1 | Extended Validation |
| IV | 2.23.140.1.2.3 | Individual Validated |

## Validation Types

### Domain Validation (DV)

**What's Validated**:
- Domain ownership/control only

**Methods**:
1. Email to domain contacts
2. DNS TXT record
3. HTTP file validation
4. TLS using ALPN

**Certificate Contents**:
- No organization information
- Subject contains only CN/SAN

### Organization Validation (OV)

**What's Validated**:
- Domain ownership/control
- Organization legal existence
- Organization identity

**Certificate Contents**:
- Organization name (O)
- Location (L, ST, C)
- Subject DN includes organization info

### Extended Validation (EV)

**What's Validated**:
- Domain ownership/control
- Organization legal existence
- Organization identity
- Physical address
- Operational existence
- Business registration

**Additional Requirements**:
- Face-to-face or equivalent verification
- More stringent identity checks
- Annual verification required

## Compliance Checklist

### For End-Entity TLS Certificates

- [ ] Validity period ≤ 398 days
- [ ] RSA key ≥ 2048 bits OR ECC key ≥ P-256
- [ ] Signature uses SHA-256 or stronger
- [ ] SAN extension present with all domains
- [ ] No SHA-1 or weaker signatures
- [ ] No prohibited key usages
- [ ] Certificate Transparency SCTs present
- [ ] OCSP responder URL in AIA
- [ ] Certificate Policy OID present


### For Intermediate CA Certificates

- [ ] Basic Constraints: CA:TRUE, critical
- [ ] Key Usage: keyCertSign, cRLSign, critical
- [ ] Validity within root CA validity
- [ ] pathLenConstraint appropriate
- [ ] Name constraints if applicable
- [ ] CRL Distribution Point present

## Policy Timeline

| Date | Change |
|------|--------|
| 2016-06-01 | SHA-1 prohibited for new certs |
| 2017-01-01 | SHA-1 completely prohibited |
| 2018-03-01 | 825-day max validity |
| 2018-04-30 | CT required for all certs |
| 2020-09-01 | 398-day max validity |
| 2024+ | Shorter validity expected |

## References

- CA/Browser Forum Baseline Requirements: https://cabforum.org/baseline-requirements/
- Mozilla Root Store Policy: https://www.mozilla.org/en-US/about/governance/policies/security-group/certs/policy/
- Apple Root Certificate Program: https://www.apple.com/certificateauthority/ca_program.html
- Microsoft Trusted Root Program: https://docs.microsoft.com/en-us/security/trusted-root/program-requirements
- Chrome Certificate Transparency Policy: https://googlechrome.github.io/CertificateTransparency/
