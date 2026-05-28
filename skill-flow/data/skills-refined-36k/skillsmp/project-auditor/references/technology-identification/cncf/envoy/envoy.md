# Envoy Proxy

**Category**: cncf
**Description**: Cloud-native high-performance edge/middle/service proxy
**Homepage**: https://envoyproxy.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Envoy Go extensions*

- `github.com/envoyproxy/go-control-plane` - Envoy control plane
- `github.com/envoyproxy/protoc-gen-validate` - Protobuf validation

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Envoy usage*

- `envoy.yaml` - Envoy configuration
- `envoy.json` - JSON configuration
- `envoy-config.yaml` - Alternative config name
- `bootstrap.yaml` - Bootstrap configuration
- `cds.yaml` - Cluster discovery
- `lds.yaml` - Listener discovery

### Code Patterns

**Pattern**: `envoyproxy\.io|envoy-proxy|envoy\.yaml`
- Envoy references
- Example: `envoyproxy.io/config`

**Pattern**: `admin:\s*\n\s*address:|static_resources:|dynamic_resources:`
- Envoy config sections
- Example: YAML configuration structure

**Pattern**: `ENVOY_|envoy_`
- Envoy environment variables
- Example: `ENVOY_ADMIN_PORT`

**Pattern**: `:9901|:15000|:15001`
- Envoy default ports
- Example: `localhost:9901/stats`

**Pattern**: `x-envoy-|envoy\.api\.v[0-9]`
- Envoy headers and API versions
- Example: `x-envoy-upstream-service-time`

**Pattern**: `type\.googleapis\.com/envoy`
- Envoy typed config
- Example: `type.googleapis.com/envoy.extensions.filters.http`

---

## Environment Variables

- `ENVOY_UID` - Envoy user ID
- `ENVOY_GID` - Envoy group ID
- `ENVOY_ADMIN_PORT` - Admin interface port
- `ENVOY_SERVICE_NAME` - Service name
- `ENVOY_CONFIG_PATH` - Config file path

## Detection Notes

- Admin interface on port 9901 by default
- xDS APIs for dynamic configuration
- Often used with Istio service mesh
- Sidecar proxy pattern common in Kubernetes

---

## Secrets Detection

### Credentials

#### Envoy TLS Private Key
**Pattern**: `private_key_file:\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: TLS private key file reference

#### Envoy JWT Token
**Pattern**: `token:\s*['"]?(eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*)['"]?`
**Severity**: critical
**Description**: JWT token in Envoy config

---

## TIER 3: Configuration Extraction

### Cluster Name Extraction

**Pattern**: `cluster:\s*\n\s*name:\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- Envoy cluster name
- Extracts: `cluster_name`
- Multiline: true

### Listener Port Extraction

**Pattern**: `socket_address:\s*\n\s*(?:address:[^\n]+\n\s*)?port_value:\s*['"]?([0-9]+)['"]?`
- Listener port value
- Extracts: `port`
- Multiline: true
