# Istio

**Category**: cncf
**Description**: Service mesh for Kubernetes
**Homepage**: https://istio.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Istio Go packages*

- `istio.io/client-go` - Istio client library
- `istio.io/api` - Istio API definitions
- `istio.io/istio` - Istio core

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Istio usage*

- `istio-operator.yaml` - Istio operator config
- `istioctl` - Istio CLI
- `mesh.yaml` - Mesh configuration
- `istio-config.yaml` - Istio configuration

### Kubernetes Resources (YAML files)

**Pattern**: `kind:\s*(?:VirtualService|DestinationRule|Gateway|ServiceEntry|Sidecar|PeerAuthentication|AuthorizationPolicy|EnvoyFilter)`
- Istio CRD kinds
- Example: `kind: VirtualService`

**Pattern**: `apiVersion:\s*(?:networking\.istio\.io|security\.istio\.io|telemetry\.istio\.io)/v[0-9]+`
- Istio API groups
- Example: `apiVersion: networking.istio.io/v1beta1`

### Code Patterns

**Pattern**: `istio\.io|istiod|istio-ingressgateway`
- Istio references
- Example: `istio.io/rev`

**Pattern**: `ISTIO_|istio-system|istio-proxy`
- Istio environment and namespaces
- Example: `ISTIO_META_WORKLOAD_NAME`

**Pattern**: `sidecar\.istio\.io/inject|istio-injection=enabled`
- Istio injection annotations
- Example: `sidecar.istio.io/inject: "true"`

**Pattern**: `:15014|:15010|:15012|:15021`
- Istio default ports
- Example: `istiod:15012`

**Pattern**: `istioctl\s+|istioctl\.io`
- Istio CLI usage
- Example: `istioctl analyze`

---

## Environment Variables

- `ISTIO_META_WORKLOAD_NAME` - Workload name
- `ISTIO_META_NAMESPACE` - Namespace
- `ISTIO_META_CLUSTER_ID` - Cluster ID
- `ISTIO_META_MESH_ID` - Mesh ID
- `ISTIO_PILOT_PORT` - Pilot port
- `ISTIO_PROXY_IMAGE` - Proxy image
- `ISTIO_VERSION` - Istio version

## Detection Notes

- Service mesh with sidecar injection
- VirtualService for traffic routing
- DestinationRule for traffic policies
- Gateway for ingress/egress traffic
- Uses Envoy proxy as data plane

---

## Secrets Detection

### Credentials

#### Istio CA Certificate
**Pattern**: `ca-cert\.pem|ca-key\.pem|cert-chain\.pem`
**Severity**: high
**Description**: Istio CA certificate files

#### Istio mTLS Configuration
**Pattern**: `mode:\s*(?:STRICT|PERMISSIVE|DISABLE)`
**Severity**: medium
**Description**: mTLS mode configuration
**Context Required**: Near PeerAuthentication

---

## TIER 3: Configuration Extraction

### Gateway Host Extraction

**Pattern**: `hosts:\s*\n\s*-\s*['"]?([a-zA-Z0-9.*-]+)['"]?`
- Gateway hostname
- Extracts: `hostname`
- Multiline: true

### Virtual Service Destination Extraction

**Pattern**: `host:\s*['"]?([a-zA-Z0-9.-]+)['"]?`
- Service hostname
- Extracts: `service_host`
- Context Required: In VirtualService spec
