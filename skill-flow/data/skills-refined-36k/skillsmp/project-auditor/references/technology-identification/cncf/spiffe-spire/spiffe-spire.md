# SPIFFE/SPIRE

**Category**: cncf
**Description**: Secure identity framework for production workloads
**Homepage**: https://spiffe.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*SPIFFE/SPIRE Go packages*

- `github.com/spiffe/spire` - SPIRE core
- `github.com/spiffe/go-spiffe/v2` - Go SPIFFE library
- `github.com/spiffe/spiffe-csi` - CSI driver
- `github.com/spiffe/spire-controller-manager` - K8s controller

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate SPIFFE/SPIRE usage*

- `server.conf` - SPIRE server config
- `agent.conf` - SPIRE agent config
- `spire-server.yaml` - K8s server deployment
- `spire-agent.yaml` - K8s agent deployment

### Code Patterns

**Pattern**: `spiffe://|spiffe\.io`
- SPIFFE ID format
- Example: `spiffe://example.org/service/web`

**Pattern**: `spire-server|spire-agent`
- SPIRE components
- Example: `spire-server run -config /run/spire/config/server.conf`

**Pattern**: `kind:\s*(ClusterSPIFFEID|ClusterFederatedTrustDomain)`
- SPIRE Controller Manager CRDs
- Example: `kind: ClusterSPIFFEID`

**Pattern**: `trust_domain:|node_attestors:|workload_attestors:`
- SPIRE config sections
- Example: `trust_domain = "example.org"`

**Pattern**: `x509-svid|jwt-svid|bundle`
- SVID types
- Example: `spire-agent api fetch x509`

**Pattern**: `workloadapi\.NewX509Source|workloadapi\.FetchX509SVID`
- Go SPIFFE API
- Example: `x509Source, err := workloadapi.NewX509Source(ctx)`

**Pattern**: `/run/spire/sockets/|spire-agent\.sock`
- SPIRE socket paths
- Example: `/run/spire/sockets/agent.sock`

**Pattern**: `SPIFFE_ENDPOINT_SOCKET|SPIRE_`
- SPIFFE environment variables
- Example: `SPIFFE_ENDPOINT_SOCKET=/run/spire/sockets/agent.sock`

---

## Environment Variables

- `SPIFFE_ENDPOINT_SOCKET` - Workload API socket
- `SPIRE_SERVER_ADDRESS` - Server address
- `SPIRE_TRUST_DOMAIN` - Trust domain

## Detection Notes

- SPIFFE defines identity standard
- SPIRE implements SPIFFE
- SVIDs are workload identities
- Trust domains scope identities
- Workload API for fetching SVIDs

---

## Secrets Detection

### Credentials

#### SPIRE Join Token
**Pattern**: `join_token\s*=\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: SPIRE agent join token

#### Trust Bundle
**Pattern**: `bundle_endpoint\s*=|ca_bundle\s*=`
**Severity**: high
**Description**: Trust bundle configuration

---

## TIER 3: Configuration Extraction

### Trust Domain Extraction

**Pattern**: `trust_domain\s*=\s*['"]?([a-zA-Z0-9.-]+)['"]?`
- SPIFFE trust domain
- Extracts: `trust_domain`
- Example: `trust_domain = "example.org"`

### Server Address Extraction

**Pattern**: `server_address\s*=\s*['"]?([^\s'"]+)['"]?`
- SPIRE server address
- Extracts: `server_address`
- Example: `server_address = "spire-server:8081"`

### Socket Path Extraction

**Pattern**: `socket_path\s*=\s*['"]?([^\s'"]+)['"]?`
- Workload API socket path
- Extracts: `socket_path`
- Example: `socket_path = "/run/spire/sockets/agent.sock"`
