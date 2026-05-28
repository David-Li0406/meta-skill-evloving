<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# Certificate Analysis Knowledge Base

Comprehensive reference documentation for X.509 certificate analysis, TLS/SSL security assessment, and CA/Browser Forum compliance verification.

## Contents

### [X.509 Certificate Guide](x509-certificates.md)
Deep dive into X.509 certificate structure, extensions, and validation.

**Topics Covered**:
- Certificate structure and fields
- Certificate extensions (SAN, Basic Constraints, Key Usage)
- Certificate types (DV, OV, EV)
- Public key algorithms (RSA, ECC, EdDSA)
- Signature algorithms (SHA-256, SHA-384, SHA-512)
- Certificate chains and trust hierarchies
- Self-signed vs CA-signed certificates

**Use Cases**:
- Understanding certificate contents
- Debugging certificate issues
- Certificate creation and management
- PKI architecture planning

### [CA/Browser Forum Compliance](cab-forum-compliance.md)
CA/Browser Forum Baseline Requirements and compliance validation.

**Topics Covered**:
- Baseline Requirements overview
- Validity period limits (398 days)
- Key size requirements (RSA 2048+, ECC P-256+)
- Signature algorithm requirements
- Subject Alternative Name (SAN) requirements
- Certificate Transparency (CT) requirements
- OCSP and CRL requirements
- Compliance timeline and policy changes

**Use Cases**:
- Validating public trust certificates
- Ensuring CA/B Forum compliance
- Audit preparation
- Certificate policy development

### [TLS Security Best Practices](tls-security.md)
TLS configuration, security assessment, and best practices.

**Topics Covered**:
- TLS versions (1.2, 1.3)
- Cipher suite selection
- Certificate chain validation
- OCSP stapling
- HSTS and certificate pinning
- StartTLS protocols (SMTP, IMAP, LDAP, etc.)
- Common vulnerabilities and mitigations
- Security headers

**Use Cases**:
- Server TLS configuration
- Security assessments
- Vulnerability remediation
- Compliance audits

### [Certificate Formats](certificate-formats.md)
Certificate encoding formats and conversion between them.

**Topics Covered**:
- PEM format (Base64 encoded)
- DER format (Binary ASN.1)
- PKCS#7/P7B (Certificate bundles)
- PKCS#12/PFX (Keystores with private keys)
- JKS (Java KeyStore)
- Format detection and conversion
- OpenSSL commands for each format

**Use Cases**:
- Format identification
- Certificate conversion
- Platform compatibility
- Key management

### [Claude AI Integration](claude-ai-integration.md)
AI-enhanced certificate analysis with Claude for intelligent recommendations.

**Topics Covered**:
- Claude AI architecture for cert analysis
- RAG-enhanced security assessment
- Automated risk prioritization
- Remediation recommendations
- Cost optimization
- Performance benchmarks

**Use Cases**:
- Comprehensive security audits
- Complex compliance questions
- Intelligent remediation guidance
- Executive reporting

## Quick Start

### For Security Engineers

1. **Understand certificate basics**
   - Read: [X.509 Certificate Guide](x509-certificates.md)
   - Focus on: Certificate structure, extensions, chains

2. **Learn compliance requirements**
   - Read: [CA/Browser Forum Compliance](cab-forum-compliance.md)
   - Focus on: Key requirements, validity periods

3. **Configure secure TLS**
   - Read: [TLS Security Best Practices](tls-security.md)
   - Implement: Recommended cipher suites, HSTS

### For DevOps Engineers

1. **Certificate format handling**
   - Read: [Certificate Formats](certificate-formats.md)
   - Learn: Format conversion, keystores

2. **Automation**
   - Use: cert-analyser.sh for automated checks
   - Integrate: CI/CD pipeline validation

3. **Monitoring**
   - Set up: Expiry alerts
   - Implement: CT log monitoring

### For Compliance Officers

1. **Understand requirements**
   - Read: [CA/Browser Forum Compliance](cab-forum-compliance.md)
   - Focus on: Policy requirements, audit criteria

2. **Generate reports**
   - Use: `--compliance` flag for detailed reports
   - Review: JSON output for audit documentation

## Common Scenarios

### Scenario 1: Certificate Expiry Check

**Question**: When does this certificate expire and is the renewal urgent?

**Process**:
1. Run `./cert-analyser.sh example.com`
2. Check "Days until expiration" in summary
3. Review expiry date in report
4. Plan renewal based on urgency

**Command**:
```bash
./cert-analyser.sh example.com
```

### Scenario 2: Compliance Audit

**Question**: Does this certificate meet CA/B Forum requirements?

**Process**:
1. Run compliance check
2. Review all 7 compliance areas
3. Document failures and remediation

**Command**:
```bash
./cert-analyser.sh --compliance example.com
```

### Scenario 3: Certificate Chain Validation

**Question**: Is the certificate chain valid and complete?

**Process**:
1. Run chain validation
2. Check chain order
3. Verify against trust store
4. Review intermediate certificates

**Command**:
```bash
./cert-analyser.sh --verify-chain example.com
```

### Scenario 4: StartTLS Analysis

**Question**: Is my mail server's TLS configuration secure?

**Process**:
1. Connect via StartTLS
2. Analyze certificate
3. Check OCSP and chain
4. Review compliance

**Command**:
```bash
./cert-analyser.sh --starttls smtp --port 587 --all-checks mail.example.com
```

### Scenario 5: Certificate Comparison

**Question**: Is the deployed certificate the same as our backup?

**Process**:
1. Extract both certificates
2. Compare fingerprints and properties
3. Verify identity match

**Command**:
```bash
./cert-analyser.sh --compare cert1.pem cert2.pem
```

## Integration with Gibson Powers

### Using with Certificate Analyser

```bash
# Basic domain analysis
./utils/certificate-analyser/cert-analyser.sh example.com

# Full compliance check
./utils/certificate-analyser/cert-analyser.sh --all-checks example.com

# CA/B Forum compliance only
./utils/certificate-analyser/cert-analyser.sh --compliance example.com

# Analyze local certificate file
./utils/certificate-analyser/cert-analyser.sh --file certificate.pem

# PKCS12 keystore analysis
./utils/certificate-analyser/cert-analyser.sh --file keystore.p12 --password secret

# StartTLS SMTP analysis
./utils/certificate-analyser/cert-analyser.sh --starttls smtp mail.example.com

# With Claude AI enhanced analysis
export ANTHROPIC_API_KEY='your-key'
./utils/certificate-analyser/cert-analyser.sh --claude example.com
```

### Using with Skills

The certificate-analysis skill provides Claude AI access to this knowledge base:

```bash
# In Claude Code
@cert-analysis analyze certificate for example.com
@cert-analysis check compliance of my certificate
@cert-analysis explain this certificate chain issue
```

### Using with Prompts

Pre-configured prompts in `prompts/certificate-analysis/`:
- `security-audit.md` - Comprehensive security audit
- `compliance-check.md` - CA/B Forum compliance
- `expiry-report.md` - Certificate expiry monitoring
- `chain-analysis.md` - Chain validation and troubleshooting

## Supported Certificate Formats

| Format | Extensions | Description |
|--------|------------|-------------|
| PEM | .pem, .crt, .cer | Base64 encoded, most common |
| DER | .der, .cer | Binary ASN.1 encoding |
| PKCS#7 | .p7b, .p7c | Certificate bundles |
| PKCS#12 | .p12, .pfx | Keystores with private keys |

## Validation Checks

| Check | Flag | Description |
|-------|------|-------------|
| Chain Validation | `--verify-chain` | Validates certificate chain |
| OCSP | `--check-ocsp` | Checks OCSP status and stapling |
| CT | `--check-ct` | Certificate Transparency SCTs |
| Compliance | `--compliance` | CA/B Forum requirements |
| All | `--all-checks` | All validations |

## Best Practices

### 1. Continuous Monitoring
- Set up expiry alerts (30, 14, 7 days)
- Monitor CT logs for unauthorized certs
- Regular compliance scans

### 2. Key Management
- Use strong key sizes (RSA 2048+, ECC P-256+)
- Protect private keys
- Rotate keys periodically

### 3. Certificate Lifecycle
- Automate renewal (ACME/Let's Encrypt)
- Test before deployment
- Maintain backup certificates

### 4. Compliance
- Follow CA/B Forum requirements
- Keep validity under 398 days
- Use SHA-256 or stronger signatures

### 5. Security
- Enable HSTS
- Implement OCSP stapling
- Use TLS 1.2+ only
- Configure secure cipher suites

## Additional Resources

### Standards & Specifications
- **RFC 5280**: X.509 PKI Certificate Profile
- **RFC 6960**: OCSP Protocol
- **RFC 6962**: Certificate Transparency
- **CA/B Forum BR**: https://cabforum.org/baseline-requirements/

### Tools & Projects
- **OpenSSL**: https://www.openssl.org/
- **certigo**: https://github.com/square/certigo
- **crt.sh**: https://crt.sh/

### Learning Resources
- **SSL Labs**: https://www.ssllabs.com/
- **BadSSL**: https://badssl.com/

## Contributing

To improve this knowledge base:

1. Submit corrections via pull request
2. Suggest additional topics
3. Share real-world scenarios
4. Update tool references

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for guidelines.

## License

This documentation is licensed under GPL-3.0. See [LICENSE](../../../LICENSE) for details.
