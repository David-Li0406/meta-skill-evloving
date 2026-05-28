# Cilium

**Category**: cncf
**Description**: eBPF-based networking, observability, and security
**Homepage**: https://cilium.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Cilium Go packages*

- `github.com/cilium/cilium` - Cilium core
- `github.com/cilium/ebpf` - eBPF library
- `github.com/cilium/cilium/pkg` - Cilium packages
- `github.com/cilium/cilium/api` - Cilium API
- `github.com/cilium/hubble` - Hubble observability
- `github.com/cilium/tetragon` - Security observability

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Cilium usage*

- `cilium-config.yaml` - Cilium configuration
- `cilium.yaml` - Cilium deployment
- `hubble-relay.yaml` - Hubble relay config
- `cilium-values.yaml` - Helm values

### Code Patterns

**Pattern**: `cilium\.io/|cilium-`
- Cilium annotations and naming
- Example: `io.cilium.proxy-visibility`

**Pattern**: `kind:\s*(CiliumNetworkPolicy|CiliumClusterwideNetworkPolicy|CiliumEndpoint)`
- Cilium CRD kinds
- Example: `kind: CiliumNetworkPolicy`

**Pattern**: `apiVersion:\s*cilium\.io/v[0-9]+`
- Cilium API versions
- Example: `apiVersion: cilium.io/v2`

**Pattern**: `cilium\s+(status|connectivity|hubble|install)`
- Cilium CLI commands
- Example: `cilium status`

**Pattern**: `hubble\s+(observe|status|relay)`
- Hubble CLI commands
- Example: `hubble observe --pod my-pod`

**Pattern**: `bpf|eBPF|BPF_|XDP`
- eBPF references
- Example: `eBPF-based networking`

**Pattern**: `kube-proxy-replacement|tunnel:\s*(disabled|vxlan|geneve)`
- Cilium features
- Example: `kube-proxy-replacement: strict`

**Pattern**: `endpointSelector:|fromEndpoints:|toEndpoints:`
- CiliumNetworkPolicy selectors
- Example: `endpointSelector:\n  matchLabels:`

**Pattern**: `:4240|:4244|:9962|:9963`
- Cilium default ports
- Example: `localhost:4240/healthz`

---

## Environment Variables

- `CILIUM_K8S_NAMESPACE` - Cilium namespace
- `CILIUM_CNI_CHAINING_MODE` - CNI chaining mode
- `CILIUM_IDENTITY_ALLOCATION_MODE` - Identity allocation
- `HUBBLE_LISTEN_ADDRESS` - Hubble listen address

## Detection Notes

- Uses eBPF for networking and security
- Can replace kube-proxy
- Hubble provides observability
- CiliumNetworkPolicy extends K8s NetworkPolicy
- Supports WireGuard encryption

---

## Secrets Detection

### Credentials

#### Cilium Etcd Config
**Pattern**: `etcd-config:\s*["']?([^\s"']+)["']?`
**Severity**: high
**Description**: Cilium etcd configuration with potential credentials

#### Hubble TLS
**Pattern**: `hubble.*tls.*cert|hubble.*tls.*key`
**Severity**: high
**Description**: Hubble TLS certificate configuration

---

## TIER 3: Configuration Extraction

### Cluster Name Extraction

**Pattern**: `cluster-name:\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- Cilium cluster name
- Extracts: `cluster_name`
- Example: `cluster-name: my-cluster`

### Tunnel Mode Extraction

**Pattern**: `tunnel:\s*['"]?(disabled|vxlan|geneve)['"]?`
- Tunnel encapsulation mode
- Extracts: `tunnel_mode`
- Example: `tunnel: vxlan`

### IPAM Mode Extraction

**Pattern**: `ipam:\s*['"]?(kubernetes|cluster-pool|azure|eni)['"]?`
- IP address management mode
- Extracts: `ipam_mode`
- Example: `ipam: cluster-pool`
