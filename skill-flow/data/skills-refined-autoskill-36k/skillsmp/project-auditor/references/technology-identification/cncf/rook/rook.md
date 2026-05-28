# Rook

**Category**: cncf
**Description**: Cloud-native storage orchestrator for Kubernetes
**Homepage**: https://rook.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Rook Go packages*

- `github.com/rook/rook` - Rook core
- `github.com/rook/rook/pkg/operator/ceph` - Ceph operator
- `github.com/rook/rook/pkg/operator/nfs` - NFS operator

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Rook usage*

- `cluster.yaml` - Rook cluster definition
- `storageclass.yaml` - Storage class
- `rook-ceph-cluster.yaml` - Ceph cluster
- `cephblockpool.yaml` - Ceph block pool
- `cephfilesystem.yaml` - Ceph filesystem

### Code Patterns

**Pattern**: `rook\.io/|rook-ceph`
- Rook annotations and naming
- Example: `rook.io/ceph-cluster-name`

**Pattern**: `kind:\s*(CephCluster|CephBlockPool|CephFilesystem|CephObjectStore|CephNFS)`
- Rook Ceph CRD kinds
- Example: `kind: CephCluster`

**Pattern**: `apiVersion:\s*ceph\.rook\.io/v[0-9]+`
- Rook Ceph API version
- Example: `apiVersion: ceph.rook.io/v1`

**Pattern**: `mon:|mgr:|osd:|mds:|rgw:`
- Ceph daemon configurations
- Example: `mon:\n  count: 3`

**Pattern**: `rook-ceph-operator|rook-ceph-mon|rook-ceph-osd`
- Rook Ceph component names
- Example: `rook-ceph-operator`

**Pattern**: `ceph\.com|ceph-volume|ceph-mon`
- Ceph references
- Example: `ceph-volume lvm`

**Pattern**: `useAllNodes:|useAllDevices:|deviceFilter:`
- Rook storage configuration
- Example: `useAllNodes: true`

**Pattern**: `storageClassName:\s*['"]?rook-ceph`
- Rook storage class reference
- Example: `storageClassName: rook-ceph-block`

---

## Environment Variables

- `ROOK_CEPH_USERNAME` - Ceph admin username
- `ROOK_CEPH_SECRET` - Ceph admin secret
- `ROOK_CURRENT_NAMESPACE_ONLY` - Single namespace mode
- `ROOK_LOG_LEVEL` - Log level

## Detection Notes

- Orchestrates Ceph storage on Kubernetes
- CephCluster is main resource
- Supports block, file, and object storage
- CSI driver for dynamic provisioning
- Toolbox pod for Ceph CLI access

---

## Secrets Detection

### Credentials

#### Ceph Admin Secret
**Pattern**: `admin-secret:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Ceph admin authentication secret

#### Ceph User Secret
**Pattern**: `userSecretName:\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: Ceph user secret reference

---

## TIER 3: Configuration Extraction

### Mon Count Extraction

**Pattern**: `mon:\s*\n\s*count:\s*([0-9]+)`
- Number of Ceph monitors
- Extracts: `mon_count`
- Example: `mon:\n  count: 3`
**Multiline**: true

### Storage Class Extraction

**Pattern**: `storageClassName:\s*['"]?([a-zA-Z0-9-]+)['"]?`
- Storage class name
- Extracts: `storage_class`
- Example: `storageClassName: rook-ceph-block`

### Pool Name Extraction

**Pattern**: `name:\s*['"]?([a-zA-Z0-9-]+)['"]?`
- Ceph pool name
- Extracts: `pool_name`
- Example: `name: replicapool`
