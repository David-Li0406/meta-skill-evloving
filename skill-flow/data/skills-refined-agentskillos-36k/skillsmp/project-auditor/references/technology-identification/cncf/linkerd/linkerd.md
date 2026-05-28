# Linkerd

**Category**: cncf
**Description**: Ultralight service mesh for Kubernetes
**Homepage**: https://linkerd.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Linkerd Go packages*

- `github.com/linkerd/linkerd2` - Linkerd v2 core
- `github.com/linkerd/linkerd2-proxy-api` - Proxy API
- `github.com/linkerd/linkerd2/controller` - Controller
- `github.com/linkerd/linkerd2/pkg` - Shared packages

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Linkerd usage*

- `linkerd.yaml` - Linkerd configuration
- `linkerd-config.yaml` - Linkerd config
- `linkerd-install.yaml` - Installation manifest

### Code Patterns

**Pattern**: `linkerd\s+inject|linkerd\s+install|linkerd\s+check`
- Linkerd CLI commands
- Example: `linkerd inject deployment.yaml`

**Pattern**: `linkerd\.io/inject:\s*['"]?enabled['"]?`
- Linkerd injection annotation
- Example: `linkerd.io/inject: enabled`

**Pattern**: `linkerd\.io/proxy-|config\.linkerd\.io/`
- Linkerd annotations
- Example: `config.linkerd.io/proxy-cpu-request: 100m`

**Pattern**: `linkerd-proxy|linkerd-init`
- Linkerd sidecar containers
- Example: `name: linkerd-proxy`

**Pattern**: `viz\.linkerd\.io|buoyant\.io`
- Linkerd-related domains
- Example: `viz.linkerd.io`

**Pattern**: `ServiceProfile|TrafficSplit`
- Linkerd custom resources
- Example: `kind: ServiceProfile`

**Pattern**: `:4140|:4143|:4191|:9990`
- Linkerd default ports
- Example: `localhost:4191/metrics`

**Pattern**: `emojivoto|linkerd-viz|linkerd-jaeger`
- Linkerd examples and extensions
- Example: `linkerd-viz install`

---

## Environment Variables

- `LINKERD2_PROXY_LOG` - Proxy log level
- `LINKERD2_PROXY_DESTINATION_CONTEXT` - Destination context
- `LINKERD2_PROXY_IDENTITY_DIR` - Identity certificates directory
- `LINKERD_AWAIT_DISABLED` - Disable linkerd-await
- `LINKERD_DISABLED` - Disable proxy

## Detection Notes

- Look for linkerd.io annotations in Kubernetes manifests
- linkerd-proxy sidecar indicates mesh membership
- ServiceProfile CRDs for traffic management
- SMI (Service Mesh Interface) compatible
- Default admin port is 4191

---

## Secrets Detection

### Credentials

#### Linkerd Trust Anchor
**Pattern**: `trust-anchor\.crt|ca\.crt`
**Severity**: high
**Description**: Linkerd trust anchor certificate file

#### Linkerd Identity Key
**Pattern**: `issuer\.key|identity\.key`
**Severity**: critical
**Description**: Linkerd identity issuer private key

---

## TIER 3: Configuration Extraction

### Proxy Version Extraction

**Pattern**: `linkerd\.io/proxy-version:\s*['"]?([a-zA-Z0-9._-]+)['"]?`
- Linkerd proxy version
- Extracts: `proxy_version`
- Example: `linkerd.io/proxy-version: stable-2.14.0`

### Namespace Extraction

**Pattern**: `linkerd-viz|linkerd-jaeger|linkerd-multicluster`
- Linkerd extension namespaces
- Extracts: `extension_namespace`
- Example: `namespace: linkerd-viz`
