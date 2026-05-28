# Contour

**Category**: cncf
**Description**: Kubernetes ingress controller using Envoy proxy
**Homepage**: https://projectcontour.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Contour Go packages*

- `github.com/projectcontour/contour` - Contour core
- `github.com/projectcontour/contour/apis` - API types

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Contour usage*

- `contour.yaml` - Contour configuration
- `contour-config.yaml` - Contour config

### Code Patterns

**Pattern**: `projectcontour\.io/|contour-`
- Contour annotations and naming
- Example: `projectcontour.io/ingress.class: contour`

**Pattern**: `kind:\s*(HTTPProxy|TLSCertificateDelegation|ExtensionService)`
- Contour CRD kinds
- Example: `kind: HTTPProxy`

**Pattern**: `apiVersion:\s*projectcontour\.io/v[0-9]+`
- Contour API version
- Example: `apiVersion: projectcontour.io/v1`

**Pattern**: `virtualhost:|routes:|services:|tcpproxy:`
- HTTPProxy spec fields
- Example: `virtualhost:\n  fqdn: www.example.com`

**Pattern**: `contour\s+(serve|certgen|envoy)`
- Contour CLI commands
- Example: `contour serve --incluster`

**Pattern**: `contour-envoy|envoy-service`
- Contour Envoy components
- Example: `name: contour-envoy`

**Pattern**: `ingressClassName:\s*['"]?contour['"]?`
- Contour ingress class
- Example: `ingressClassName: contour`

**Pattern**: `rateLimitService:|requestHeadersPolicy:|responseHeadersPolicy:`
- HTTPProxy features
- Example: `rateLimitService:\n  extensionRef:`

---

## Environment Variables

- `CONTOUR_NAMESPACE` - Contour namespace
- `CONTOUR_CONFIG` - Configuration file path

## Detection Notes

- Uses Envoy as data plane
- HTTPProxy extends Ingress capabilities
- Supports multi-team delegation
- Rate limiting via extension service
- Gateway API support

---

## Secrets Detection

### Credentials

#### TLS Secret Reference
**Pattern**: `secretName:\s*['"]?([a-zA-Z0-9-]+)['"]?`
**Severity**: high
**Description**: TLS secret reference in HTTPProxy

---

## TIER 3: Configuration Extraction

### FQDN Extraction

**Pattern**: `fqdn:\s*['"]?([a-zA-Z0-9.-]+)['"]?`
- Virtual host FQDN
- Extracts: `fqdn`
- Example: `fqdn: www.example.com`

### Service Name Extraction

**Pattern**: `name:\s*['"]?([a-zA-Z0-9-]+)['"]?\s*\n\s*port:`
- Backend service name
- Extracts: `service_name`
- Example: `name: my-service\n  port: 80`
**Multiline**: true

### Ingress Class Extraction

**Pattern**: `ingressClassName:\s*['"]?([a-zA-Z0-9-]+)['"]?`
- Ingress class name
- Extracts: `ingress_class`
- Example: `ingressClassName: contour`
