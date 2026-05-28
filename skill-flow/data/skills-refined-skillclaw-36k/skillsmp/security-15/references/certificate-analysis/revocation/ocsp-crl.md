<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# Certificate Revocation: OCSP and CRL

Reference for certificate revocation checking mechanisms.

## Overview

Certificate revocation is the process of invalidating a certificate before its natural expiration. Two primary mechanisms exist:

| Mechanism | Type | Update Frequency | Scalability |
|-----------|------|------------------|-------------|
| CRL | Pull | Periodic (hours/days) | Limited |
| OCSP | Push/Pull | Real-time | Better |
| OCSP Stapling | Push | Real-time | Best |

## Certificate Revocation List (CRL)

### How CRLs Work

1. CA maintains list of revoked certificate serial numbers
2. CRL is signed by CA and published at CRL Distribution Point
3. Clients download CRL and check if certificate is listed
4. CRLs have validity period and must be refreshed

### CRL Structure

```
CRL
├── Version
├── Signature Algorithm
├── Issuer
├── This Update (issue date)
├── Next Update (expiry)
├── Revoked Certificates
│   ├── Serial Number
│   ├── Revocation Date
│   └── CRL Entry Extensions
│       └── Reason Code (optional)
└── CRL Extensions
    ├── CRL Number
    ├── Delta CRL Indicator
    └── Authority Key Identifier
```

### Revocation Reasons

| Code | Reason | Description |
|------|--------|-------------|
| 0 | unspecified | No reason given |
| 1 | keyCompromise | Private key compromised |
| 2 | cACompromise | CA's key compromised |
| 3 | affiliationChanged | Subject's affiliation changed |
| 4 | superseded | Replaced by new certificate |
| 5 | cessationOfOperation | No longer in use |
| 6 | certificateHold | Temporarily suspended |
| 8 | removeFromCRL | Removed from hold |
| 9 | privilegeWithdrawn | Privilege withdrawn |
| 10 | aACompromise | AA compromised |

### CRL Distribution Points

Found in certificate's CRL Distribution Points extension:

```
X509v3 CRL Distribution Points:
    Full Name:
        URI:http://crl.example.com/ca.crl
```

### OpenSSL CRL Commands

```bash
# Download CRL
curl -o ca.crl http://crl.example.com/ca.crl

# View CRL (PEM format)
openssl crl -in ca.crl -text -noout

# View CRL (DER format)
openssl crl -in ca.crl -inform DER -text -noout

# Convert CRL DER to PEM
openssl crl -in ca.crl -inform DER -outform PEM -out ca.pem

# Verify CRL signature
openssl crl -in ca.crl -CAfile ca-cert.pem -verify

# Check if certificate is revoked
openssl verify -crl_check -CAfile ca-cert.pem -CRLfile ca.crl cert.pem
```

### CRL Limitations

- **Size**: CRLs grow with revocations
- **Latency**: Not real-time (hours to days delay)
- **Bandwidth**: Full CRL download required
- **Privacy**: CRL download reveals which sites visited

### Delta CRLs

Incremental updates containing only recent changes:

- Base CRL: Full list, published less frequently
- Delta CRL: Changes since base, published frequently
- Reduces bandwidth but adds complexity

## Online Certificate Status Protocol (OCSP)

### How OCSP Works

1. Client extracts OCSP responder URL from certificate
2. Client sends OCSP request with certificate serial number
3. OCSP responder returns signed response with status
4. Client validates response signature and checks status

### OCSP Request

```
OCSPRequest
├── TBSRequest
│   ├── Version
│   ├── Requestor Name (optional)
│   └── Request List
│       └── CertID
│           ├── Hash Algorithm
│           ├── Issuer Name Hash
│           ├── Issuer Key Hash
│           └── Serial Number
└── Signature (optional)
```

### OCSP Response

```
OCSPResponse
├── Response Status
│   ├── successful (0)
│   ├── malformedRequest (1)
│   ├── internalError (2)
│   ├── tryLater (3)
│   ├── sigRequired (5)
│   └── unauthorized (6)
└── Response Bytes
    └── BasicOCSPResponse
        ├── TBS Response Data
        │   ├── Version
        │   ├── Responder ID
        │   ├── Produced At
        │   └── Responses
        │       └── Single Response
        │           ├── CertID
        │           ├── Cert Status (good/revoked/unknown)
        │           ├── This Update
        │           ├── Next Update
        │           └── Extensions
        ├── Signature Algorithm
        └── Signature
```

### Certificate Status Values

| Status | Meaning |
|--------|---------|
| good | Certificate is valid (not revoked) |
| revoked | Certificate has been revoked |
| unknown | Responder doesn't know about certificate |

### Authority Information Access (AIA)

OCSP responder URL found in certificate:

```
Authority Information Access:
    OCSP - URI:http://ocsp.example.com
    CA Issuers - URI:http://crt.example.com/intermediate.crt
```

### OpenSSL OCSP Commands

```bash
# Extract OCSP URL from certificate
openssl x509 -in cert.pem -noout -ocsp_uri

# Send OCSP request
openssl ocsp -issuer issuer.pem -cert cert.pem \
    -url http://ocsp.example.com -resp_text

# Save OCSP response
openssl ocsp -issuer issuer.pem -cert cert.pem \
    -url http://ocsp.example.com -respout response.der

# Verify saved response
openssl ocsp -issuer issuer.pem -cert cert.pem \
    -respin response.der -text

# Check OCSP for remote server
openssl s_client -connect example.com:443 -status 2>/dev/null | \
    grep -A 20 "OCSP Response"
```

### OCSP Limitations

- **Privacy**: OCSP server sees which certs are checked
- **Availability**: Depends on OCSP server uptime
- **Performance**: Adds latency to TLS handshake
- **Soft-fail**: Many clients ignore OCSP failures

## OCSP Stapling

### How Stapling Works

1. Server periodically fetches OCSP response from CA
2. Server caches the signed response
3. Server sends response during TLS handshake
4. Client validates response (signed by CA)

### Benefits

- **Privacy**: No OCSP query visible to third parties
- **Performance**: No additional round-trip
- **Reliability**: Not dependent on OCSP server availability
- **Freshness**: Server keeps response current

### TLS Extension

OCSP stapling uses TLS `status_request` extension:

```
Client Hello:
    Extension: status_request (5)

Server Hello:
    Extension: status_request (5)

Certificate Status:
    OCSP Response
```

### Server Configuration

**Nginx**:
```nginx
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /path/to/chain.pem;
resolver 8.8.8.8;
```

**Apache**:
```apache
SSLUseStapling On
SSLStaplingCache shmcb:/tmp/stapling_cache(128000)
```

### Checking Stapling Support

```bash
# Check if server supports OCSP stapling
echo | openssl s_client -connect example.com:443 -status 2>/dev/null | \
    grep -i "OCSP Response"

# Verbose stapling check
openssl s_client -connect example.com:443 -status -servername example.com
```

### Response Output

**Stapling supported**:
```
OCSP Response Status: successful (0x0)
Response Type: Basic OCSP Response
...
Cert Status: good
```

**Stapling not supported**:
```
OCSP response: no response sent
```

## OCSP Must-Staple

### Purpose

Certificate extension requiring server to provide stapled OCSP response.

### Extension OID

```
1.3.6.1.5.5.7.1.24 (id-pe-tlsfeature)
```

### Certificate Entry

```
X509v3 TLS Feature:
    status_request
```

### Behavior

- Server MUST provide stapled OCSP response
- Client SHOULD reject if staple missing/invalid
- Hard-fail revocation checking

### Checking Must-Staple

```bash
# Check for Must-Staple extension
openssl x509 -in cert.pem -noout -text | grep -i "1.3.6.1.5.5.7.1.24"

# Or look for TLS Feature
openssl x509 -in cert.pem -noout -text | grep -A1 "TLS Feature"
```

## Comparison

| Feature | CRL | OCSP | OCSP Stapling |
|---------|-----|------|---------------|
| Latency | High | Medium | Low |
| Privacy | Low | Low | High |
| Bandwidth | High | Low | Low |
| Availability | Good | Medium | Good |
| Real-time | No | Yes | Yes |
| Client Complexity | Low | Medium | Low |
| Server Complexity | N/A | N/A | Low |

## Best Practices

### For CAs

1. Publish CRLs frequently (at least daily)
2. Use delta CRLs for large CRLs
3. Ensure OCSP responder high availability
4. Sign OCSP responses with dedicated key
5. Cache OCSP responses appropriately

### For Server Operators

1. Enable OCSP stapling
2. Monitor stapling status
3. Keep intermediate certificates current
4. Test revocation checking
5. Consider Must-Staple for high-security

### For Developers

1. Implement both CRL and OCSP checking
2. Handle soft-fail gracefully
3. Cache revocation responses
4. Respect cache headers
5. Log revocation check failures

## Troubleshooting

### OCSP Responder Unreachable

```bash
# Test connectivity
curl -v http://ocsp.example.com

# Check DNS
dig ocsp.example.com

# Try with timeout
timeout 5 openssl ocsp -issuer issuer.pem -cert cert.pem -url http://ocsp.example.com
```

### Stapling Not Working

1. Check resolver configuration
2. Verify trusted certificate chain
3. Check OCSP responder URL in certificate
4. Review server error logs
5. Test with `openssl s_client -status`

### Certificate Shows Revoked

1. Verify serial number matches
2. Check revocation date
3. Review revocation reason
4. Confirm with CA
5. Issue new certificate if necessary

## References

- RFC 5280: Internet X.509 PKI Certificate and CRL Profile
- RFC 6960: X.509 Internet PKI OCSP
- RFC 7633: X.509v3 TLS Feature Extension (Must-Staple)
- RFC 6961: TLS Multiple Certificate Status Extension
