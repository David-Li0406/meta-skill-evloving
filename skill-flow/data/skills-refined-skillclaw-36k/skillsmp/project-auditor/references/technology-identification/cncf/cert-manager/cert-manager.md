# cert-manager

**Category**: cncf
**Description**: X.509 certificate management for Kubernetes
**Homepage**: https://cert-manager.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*cert-manager Go packages*

- `github.com/cert-manager/cert-manager` - cert-manager core
- `github.com/cert-manager/cert-manager/pkg/apis` - API types
- `github.com/cert-manager/cert-manager/pkg/client` - Go client

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate cert-manager usage*

- `certificate.yaml` - Certificate resource
- `issuer.yaml` - Issuer configuration
- `clusterissuer.yaml` - ClusterIssuer configuration
- `cert-manager.yaml` - Installation manifest

### Code Patterns

**Pattern**: `cert-manager\.io/|certmanager\.k8s\.io/`
- cert-manager annotations and API groups
- Example: `cert-manager.io/cluster-issuer: letsencrypt-prod`

**Pattern**: `kind:\s*(Certificate|Issuer|ClusterIssuer|CertificateRequest|Order|Challenge)`
- cert-manager CRD kinds
- Example: `kind: Certificate`

**Pattern**: `apiVersion:\s*cert-manager\.io/v[0-9]+`
- cert-manager API version
- Example: `apiVersion: cert-manager.io/v1`

**Pattern**: `acme:|selfSigned:|ca:|vault:|venafi:`
- Issuer types
- Example: `acme:\n  server: https://acme-v02.api.letsencrypt.org/directory`

**Pattern**: `letsencrypt|acme-v02\.api\.letsencrypt\.org`
- Let's Encrypt ACME server
- Example: `server: https://acme-v02.api.letsencrypt.org/directory`

**Pattern**: `secretName:|dnsNames:|issuerRef:`
- Certificate spec fields
- Example: `secretName: tls-secret`

**Pattern**: `http01:|dns01:`
- ACME challenge solvers
- Example: `http01:\n  ingress:\n    class: nginx`

**Pattern**: `cmctl|kubectl\s+cert-manager`
- cert-manager CLI
- Example: `cmctl status certificate`

---

## Environment Variables

- `CERT_MANAGER_NAMESPACE` - Installation namespace
- `CERT_MANAGER_CLUSTER_RESOURCE_NAMESPACE` - Cluster-scoped resources namespace
- `CERT_MANAGER_LEADER_ELECTION_NAMESPACE` - Leader election namespace

## Detection Notes

- Certificate CRDs manage TLS certificates
- Issuer/ClusterIssuer define certificate authorities
- Commonly used with Let's Encrypt for free TLS
- Supports ACME HTTP01 and DNS01 challenges
- Integration with Ingress and Gateway API

---

## Secrets Detection

### Credentials

#### ACME Account Key
**Pattern**: `privateKeySecretRef:\s*\n\s*name:\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: ACME account private key secret reference
**Multiline**: true

#### CA Private Key
**Pattern**: `ca:\s*\n\s*secretName:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: CA private key secret reference
**Multiline**: true

#### Vault Token
**Pattern**: `vault:.*tokenSecretRef`
**Severity**: critical
**Description**: Vault authentication token for cert-manager
**Multiline**: true

---

## TIER 3: Configuration Extraction

### Certificate DNS Names

**Pattern**: `dnsNames:\s*\n(?:\s*-\s*['"]?([a-zA-Z0-9.*-]+)['"]?\n?)+`
- Certificate DNS names
- Extracts: `dns_names`
- Example: `dnsNames:\n  - example.com\n  - www.example.com`
**Multiline**: true

### Certificate Duration

**Pattern**: `duration:\s*['"]?([0-9]+h)['"]?`
- Certificate validity duration
- Extracts: `duration`
- Example: `duration: 2160h`

### Issuer Reference

**Pattern**: `issuerRef:\s*\n\s*name:\s*['"]?([a-zA-Z0-9-]+)['"]?`
- Referenced issuer name
- Extracts: `issuer_name`
- Example: `issuerRef:\n  name: letsencrypt-prod`
**Multiline**: true
