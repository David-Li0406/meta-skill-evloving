# Sigstore - Technical Reference for Supply Chain Security

## Overview

**Sigstore** is a free and open service for signing and verifying software artifacts, providing a transparent and auditable way to establish provenance.

**Website**: https://sigstore.dev
**Status**: Linux Foundation project
**Purpose**: Keyless signing and verification for software supply chain

## Core Components

### 1. Cosign
**Purpose**: Sign and verify container images and artifacts

**Key Features**:
- Container image signing
- Keyless signing with OIDC
- Attestation support (SLSA, in-toto)
- Policy enforcement

**Common Commands**:
```bash
# Sign container image
cosign sign docker.io/myimage:latest

# Verify image
cosign verify docker.io/myimage:latest

# Sign with attestation
cosign attest --predicate slsa.json \
  --type slsaprovenance \
  docker.io/myimage:latest

# Verify attestation
cosign verify-attestation \
  --type slsaprovenance \
  docker.io/myimage:latest
```

### 2. Rekor
**Purpose**: Transparency log for signatures and attestations

**Key Features**:
- Append-only ledger
- Publicly verifiable
- Timestamp authority
- Entry immutability

**Common Operations**:
```bash
# Search by artifact hash
rekor-cli search --artifact-hash sha256:abc123

# Get log entry
rekor-cli get --log-index 12345

# Verify inclusion
rekor-cli verify --artifact artifact.tar.gz
```

### 3. Fulcio
**Purpose**: Certificate authority for code signing

**Key Features**:
- Short-lived certificates (10 minutes)
- OIDC-based identity
- No long-term key management
- Automatic certificate issuance

**Identity Verification**:
```
# Example certificate subject
CN=user@example.com
Issuer=https://accounts.google.com
San=email:user@example.com
```

## Keyless Signing Workflow

### Traditional vs Keyless

**Traditional Signing**:
1. Generate long-lived private key
2. Store key securely
3. Sign artifacts with key
4. Distribute public key
5. Verify with public key

**Keyless Signing (Sigstore)**:
1. Authenticate with OIDC (GitHub, Google, etc.)
2. Get short-lived certificate from Fulcio
3. Sign artifact
4. Record in Rekor transparency log
5. Verify using OIDC identity + Rekor entry

### Benefits
- No key management burden
- Certificates expire quickly (reduced risk)
- Identity tied to OIDC provider
- Publicly auditable (Rekor)
- Cannot forge retroactively

## Verification Process

### Container Image Verification

```bash
# Verify with expected identity
cosign verify \
  --certificate-identity user@example.com \
  --certificate-oidc-issuer https://github.com/login/oauth \
  docker.io/myimage:latest

# Verify with regex
cosign verify \
  --certificate-identity-regexp '.*@myorg\.com' \
  --certificate-oidc-issuer https://accounts.google.com \
  docker.io/myimage:latest
```

### Attestation Verification

```bash
# Verify SLSA provenance
cosign verify-attestation \
  --type slsaprovenance \
  --certificate-identity https://github.com/actions/runner \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  docker.io/myimage:latest

# Extract and inspect
cosign verify-attestation \
  --type slsaprovenance \
  docker.io/myimage:latest | \
  jq '.payload | @base64d | fromjson'
```

## Trusted OIDC Providers

### GitHub Actions
- **Issuer**: `https://token.actions.githubusercontent.com`
- **Identity**: Repository slug (e.g., `octo-org/octo-repo`)
- **Use Case**: Automated builds and releases

### Google Cloud Build
- **Issuer**: `https://accounts.google.com`
- **Identity**: Service account email
- **Use Case**: GCP-based builds

### GitLab
- **Issuer**: `https://gitlab.com`
- **Identity**: Project path
- **Use Case**: GitLab CI/CD

## Rekor Transparency Log

### Log Structure

Each Rekor entry contains:
```json
{
  "logIndex": 12345678,
  "body": {
    "intotoObj": {
      "content": {
        "payloadHash": "sha256:abc123..."
      }
    }
  },
  "verification": {
    "signedEntryTimestamp": "base64..."
  },
  "integratedTime": 1700000000
}
```

### Querying Rekor

```bash
# By artifact hash
rekor-cli search --sha sha256:abc123

# By email
rekor-cli search --email user@example.com

# By public key
rekor-cli search --public-key pubkey.pem

# Get specific entry
rekor-cli get --uuid <entry-uuid>
```

## Policy Enforcement

### Kubernetes Admission Control

**Sigstore Policy Controller**:
```yaml
apiVersion: policy.sigstore.dev/v1beta1
kind: ClusterImagePolicy
metadata:
  name: signed-images
spec:
  images:
  - glob: "**/*"
  authorities:
  - keyless:
      url: https://fulcio.sigstore.dev
      identities:
      - issuer: https://token.actions.githubusercontent.com
        subject: "https://github.com/myorg/*"
```

### CI/CD Policy

```bash
#!/bin/bash
# Verify before deployment

EXPECTED_IDENTITY="https://github.com/myorg/myrepo"
EXPECTED_ISSUER="https://token.actions.githubusercontent.com"

if cosign verify \
  --certificate-identity "$EXPECTED_IDENTITY" \
  --certificate-oidc-issuer "$EXPECTED_ISSUER" \
  "$IMAGE"; then
  echo "✓ Signature verified"
  kubectl apply -f deployment.yaml
else
  echo "✗ Signature verification failed"
  exit 1
fi
```

## npm Provenance

### How it Works

1. **Build**: GitHub Actions builds package
2. **Sign**: OIDC token → Fulcio certificate
3. **Attest**: SLSA provenance created
4. **Record**: Logged in Rekor
5. **Publish**: npm stores provenance with package

### Verification

```bash
# Automatic verification
npm audit signatures

# Manual verification
npm view express dist.attestations

# Cosign verification
cosign verify-attestation \
  --type slsaprovenance \
  --certificate-identity https://github.com/expressjs/express \
  registry.npmjs.org/express@4.18.2
```

## Best Practices

### For Producers

1. **Use Keyless Signing**
   - Eliminate key management
   - Leverage existing OIDC identity
   - Automatic Rekor transparency

2. **Sign Everything**
   - Container images
   - Release artifacts
   - SBOMs
   - Attestations

3. **Provide Attestations**
   - SLSA provenance
   - SBOM attestations
   - Test results
   - Vulnerability scans

### For Consumers

1. **Verify Signatures**
   - Always verify before use
   - Check identity matches expectation
   - Verify transparency log entry

2. **Trust Model**
   - Define allowed OIDC issuers
   - Allowlist identities
   - Check certificate validity

3. **Automate Verification**
   - CI/CD gates
   - Admission controllers
   - Dependency scanning

## Ecosystem Integration

### Container Registries
- **Docker Hub**: Cosign-compatible
- **GHCR**: Native support
- **GCR**: Integrated with GCP
- **ECR**: AWS support

### Package Managers
- **npm**: Native provenance
- **PyPI**: Trusted publishers
- **Maven**: PGP + Sigstore
- **RubyGems**: Sigstore integration planned

### Build Platforms
- **GitHub Actions**: OIDC built-in
- **Google Cloud Build**: Native integration
- **GitLab CI**: OIDC support
- **Jenkins**: Plugin available

## Troubleshooting

### Common Issues

**Certificate Expired**:
```
Error: certificate expired
```
Solution: Certificates are short-lived. Verify immediately after signing or check Rekor for historical verification.

**Identity Mismatch**:
```
Error: certificate identity doesn't match
```
Solution: Verify expected identity matches certificate subject. Check OIDC issuer.

**Rekor Entry Not Found**:
```
Error: entry not found in transparency log
```
Solution: Signature may not have been uploaded to Rekor. Re-sign with Rekor upload enabled.

## Tools and Libraries

### CLI Tools
- **cosign**: Primary signing/verification tool
- **rekor-cli**: Transparency log interaction
- **gitsign**: Git commit signing

### Libraries
- **sigstore-python**: Python implementation
- **sigstore-js**: JavaScript/TypeScript
- **sigstore-java**: Java integration
- **sigstore-go**: Go library

### Integrations
- **policy-controller**: Kubernetes admission
- **k8s-manifest-sigstore**: Manifest verification
- **sigstore-gradle-plugin**: Gradle integration

## Public Infrastructure

### Hosted Services
- **Fulcio**: `https://fulcio.sigstore.dev`
- **Rekor**: `https://rekor.sigstore.dev`
- **OIDC Issuer**: `https://oauth2.sigstore.dev`

### SLA and Availability
- Public instance maintained by Linux Foundation
- Production-ready and enterprise-supported
- Backup and disaster recovery in place
- Status: https://status.sigstore.dev

## References

- **Documentation**: https://docs.sigstore.dev
- **GitHub**: https://github.com/sigstore
- **Cosign**: https://github.com/sigstore/cosign
- **Rekor**: https://github.com/sigstore/rekor
- **Fulcio**: https://github.com/sigstore/fulcio
- **Blog**: https://blog.sigstore.dev
