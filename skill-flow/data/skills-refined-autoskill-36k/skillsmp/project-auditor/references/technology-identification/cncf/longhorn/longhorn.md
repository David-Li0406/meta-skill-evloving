# Longhorn

**Category**: cncf
**Description**: Cloud-native distributed storage for Kubernetes
**Homepage**: https://longhorn.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Longhorn Go packages*

- `github.com/longhorn/longhorn-manager` - Longhorn manager
- `github.com/longhorn/longhorn-engine` - Storage engine
- `github.com/longhorn/backing-image-manager` - Backing image manager

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Longhorn usage*

- `longhorn.yaml` - Longhorn deployment
- `longhorn-values.yaml` - Helm values

### Code Patterns

**Pattern**: `longhorn\.io/|longhorn-`
- Longhorn annotations and naming
- Example: `longhorn.io/volume-size`

**Pattern**: `kind:\s*(Volume|Engine|Replica|BackingImage|RecurringJob)`
- Longhorn CRD kinds
- Example: `kind: Volume`

**Pattern**: `apiVersion:\s*longhorn\.io/v[0-9]+`
- Longhorn API version
- Example: `apiVersion: longhorn.io/v1beta2`

**Pattern**: `storageClassName:\s*['"]?longhorn['"]?`
- Longhorn storage class
- Example: `storageClassName: longhorn`

**Pattern**: `longhorn-manager|longhorn-driver|longhorn-ui`
- Longhorn components
- Example: `name: longhorn-manager`

**Pattern**: `numberOfReplicas:|dataLocality:|diskSelector:`
- Longhorn volume settings
- Example: `numberOfReplicas: 3`

**Pattern**: `backup:|snapshot:|recurring-job`
- Longhorn data protection
- Example: `backup:\n  target: s3://bucket`

---

## Environment Variables

- `LONGHORN_NAMESPACE` - Longhorn namespace
- `LONGHORN_MANAGER_IP` - Manager IP address

## Detection Notes

- Distributed block storage for K8s
- Incremental snapshots and backups
- DR via cross-cluster replication
- CSI driver for dynamic provisioning
- UI for management

---

## Secrets Detection

### Credentials

#### Backup Target Credential
**Pattern**: `backup-target-credential-secret:\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: Backup target credential secret reference

#### S3 Endpoint Secret
**Pattern**: `AWS_SECRET_ACCESS_KEY`
**Severity**: critical
**Description**: AWS secret key for S3 backups

---

## TIER 3: Configuration Extraction

### Replica Count Extraction

**Pattern**: `numberOfReplicas:\s*([0-9]+)`
- Volume replica count
- Extracts: `replica_count`
- Example: `numberOfReplicas: 3`

### Storage Class Extraction

**Pattern**: `storageClassName:\s*['"]?([a-zA-Z0-9-]+)['"]?`
- Storage class name
- Extracts: `storage_class`
- Example: `storageClassName: longhorn`

### Backup Target Extraction

**Pattern**: `backup-target:\s*['"]?(s3://[^\s'"]+)['"]?`
- S3 backup target URL
- Extracts: `backup_target`
- Example: `backup-target: s3://my-bucket@us-east-1/`
