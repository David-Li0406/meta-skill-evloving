# CoreDNS

**Category**: cncf
**Description**: DNS and Service Discovery
**Homepage**: https://coredns.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*CoreDNS Go packages*

- `github.com/coredns/coredns` - CoreDNS core
- `github.com/coredns/caddy` - Caddy server fork
- `github.com/coredns/corefile-migration` - Corefile migration tools

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate CoreDNS usage*

- `Corefile` - CoreDNS configuration
- `coredns.yaml` - Kubernetes deployment
- `coredns-config.yaml` - ConfigMap

### Code Patterns

**Pattern**: `coredns|CoreDNS`
- CoreDNS references
- Example: `image: coredns/coredns:1.11.1`

**Pattern**: `^\.\s*\{|^[a-z]+\.[a-z]+\s*\{`
- Corefile zone blocks
- Example: `.:53 {`

**Pattern**: `kubernetes\s+cluster\.local|forward\s+\.|cache\s+[0-9]+|errors|health|ready`
- CoreDNS plugins
- Example: `kubernetes cluster.local in-addr.arpa ip6.arpa`

**Pattern**: `loadbalance|loop|reload|log|prometheus`
- Common CoreDNS plugins
- Example: `prometheus :9153`

**Pattern**: `hosts\s*\{|file\s+|auto\s*\{`
- CoreDNS file plugins
- Example: `hosts /etc/coredns/hosts`

**Pattern**: `:53\s*\{|:5353\s*\{`
- DNS port configuration
- Example: `.:53 {`

**Pattern**: `kube-dns|coredns-`
- Kubernetes CoreDNS components
- Example: `kube-dns.kube-system.svc`

---

## Environment Variables

- `COREDNS_CONFIG` - Configuration file path
- `COREDNS_LOG` - Log level

## Detection Notes

- Default DNS server in Kubernetes
- Corefile is the main configuration
- Plugin-based architecture
- Replaces kube-dns in modern K8s
- Prometheus metrics on :9153

---

## Secrets Detection

### Credentials

#### DNS Zone Transfer Key
**Pattern**: `transfer\s+to\s+.*key\s+["']?([^\s"']+)["']?`
**Severity**: high
**Description**: TSIG key for DNS zone transfers

---

## TIER 3: Configuration Extraction

### Zone Extraction

**Pattern**: `^([a-zA-Z0-9._-]+)\s*:\s*[0-9]+\s*\{`
- DNS zone configuration
- Extracts: `dns_zone`
- Example: `example.com:53 {`

### Upstream DNS Extraction

**Pattern**: `forward\s+\.\s+([0-9./\s]+)`
- Upstream DNS servers
- Extracts: `upstream_dns`
- Example: `forward . 8.8.8.8 8.8.4.4`

### Cache TTL Extraction

**Pattern**: `cache\s+([0-9]+)`
- Cache TTL in seconds
- Extracts: `cache_ttl`
- Example: `cache 30`
