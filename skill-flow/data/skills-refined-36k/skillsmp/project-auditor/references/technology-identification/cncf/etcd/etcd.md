# etcd

**Category**: cncf
**Description**: Distributed reliable key-value store
**Homepage**: https://etcd.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*etcd Go packages*

- `go.etcd.io/etcd/client/v3` - etcd v3 client
- `go.etcd.io/etcd/client/v2` - etcd v2 client
- `go.etcd.io/etcd/server/v3` - etcd server
- `go.etcd.io/etcd/api/v3` - etcd API
- `go.etcd.io/etcd/raft/v3` - Raft implementation
- `github.com/etcd-io/etcd` - Legacy import path

#### PYPI
*etcd Python packages*

- `etcd3` - Python etcd v3 client
- `python-etcd` - Python etcd v2 client
- `aioetcd3` - Async etcd client

#### NPM
*etcd Node.js packages*

- `etcd3` - Node.js etcd v3 client

#### MAVEN
*etcd Java packages*

- `io.etcd:jetcd-core` - Java etcd client

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate etcd usage*

- `etcd.conf.yaml` - etcd configuration
- `etcd.conf.yml` - Alternative config
- `etcd.yaml` - etcd config
- `etcd.env` - Environment file

### Code Patterns

**Pattern**: `etcd\.io|etcdctl`
- etcd references
- Example: `etcdctl get /my/key`

**Pattern**: `--advertise-client-urls|--listen-peer-urls|--initial-cluster`
- etcd CLI flags
- Example: `--advertise-client-urls=http://localhost:2379`

**Pattern**: `:2379|:2380`
- etcd default ports
- Example: `http://localhost:2379`

**Pattern**: `etcd\.New|clientv3\.New|clientv3\.Config`
- etcd Go client
- Example: `cli, err := clientv3.New(clientv3.Config{...})`

**Pattern**: `ETCD_|etcd-`
- etcd environment and naming
- Example: `ETCD_INITIAL_CLUSTER`

**Pattern**: `/v3/kv/|/v2/keys/`
- etcd API paths
- Example: `POST /v3/kv/put`

**Pattern**: `member\s+list|endpoint\s+status|snapshot\s+save`
- etcdctl commands
- Example: `etcdctl member list`

---

## Environment Variables

- `ETCD_INITIAL_CLUSTER` - Initial cluster configuration
- `ETCD_INITIAL_CLUSTER_STATE` - Cluster state (new/existing)
- `ETCD_NAME` - Member name
- `ETCD_DATA_DIR` - Data directory
- `ETCD_LISTEN_CLIENT_URLS` - Client listen URLs
- `ETCD_ADVERTISE_CLIENT_URLS` - Advertised client URLs
- `ETCD_LISTEN_PEER_URLS` - Peer listen URLs
- `ETCDCTL_ENDPOINTS` - etcdctl endpoints
- `ETCDCTL_CACERT` - CA certificate
- `ETCDCTL_CERT` - Client certificate
- `ETCDCTL_KEY` - Client key

## Detection Notes

- Used as Kubernetes backing store
- Default client port 2379, peer port 2380
- Raft consensus algorithm
- Supports TLS authentication
- Snapshot for backup/restore

---

## Secrets Detection

### Credentials

#### etcd Client Certificate
**Pattern**: `--cert-file\s*[=\s]*["']?([^\s"']+)["']?`
**Severity**: high
**Description**: etcd TLS client certificate path

#### etcd Client Key
**Pattern**: `--key-file\s*[=\s]*["']?([^\s"']+)["']?`
**Severity**: critical
**Description**: etcd TLS client private key path

#### etcd Password
**Pattern**: `--password\s*[=\s]*["']?([^\s"']+)["']?`
**Severity**: critical
**Description**: etcd authentication password

---

## TIER 3: Configuration Extraction

### Cluster Name Extraction

**Pattern**: `name:\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- etcd member name
- Extracts: `member_name`
- Example: `name: etcd-0`

### Data Directory Extraction

**Pattern**: `data-dir:\s*['"]?([^\s'"]+)['"]?`
- etcd data directory
- Extracts: `data_dir`
- Example: `data-dir: /var/lib/etcd`

### Initial Cluster Extraction

**Pattern**: `initial-cluster:\s*['"]?([^\s'"]+)['"]?`
- Initial cluster members
- Extracts: `initial_cluster`
- Example: `initial-cluster: etcd-0=http://etcd-0:2380`
