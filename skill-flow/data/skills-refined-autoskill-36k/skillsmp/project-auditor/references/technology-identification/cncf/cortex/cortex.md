# Cortex

**Category**: cncf
**Description**: Horizontally scalable, multi-tenant Prometheus
**Homepage**: https://cortexmetrics.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Cortex Go packages*

- `github.com/cortexproject/cortex` - Cortex core
- `github.com/cortexproject/cortex/pkg` - Cortex packages

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Cortex usage*

- `cortex.yaml` - Cortex configuration
- `cortex-config.yaml` - Cortex config
- `runtime-config.yaml` - Runtime configuration

### Code Patterns

**Pattern**: `cortexproject|cortexmetrics`
- Cortex references
- Example: `quay.io/cortexproject/cortex`

**Pattern**: `cortex\s+(-config\.file|-target)`
- Cortex CLI usage
- Example: `cortex -config.file=/etc/cortex/cortex.yaml`

**Pattern**: `target:\s*(all|distributor|ingester|querier|query-frontend|ruler|alertmanager|compactor|store-gateway)`
- Cortex components
- Example: `target: all`

**Pattern**: `:9009|:9095|:3100`
- Cortex default ports
- Example: `http://localhost:9009/api/prom/push`

**Pattern**: `X-Scope-OrgID|tenant_id`
- Cortex multi-tenancy
- Example: `X-Scope-OrgID: my-tenant`

**Pattern**: `ingester:|distributor:|querier:|store_gateway:`
- Cortex config sections
- Example: `ingester:\n  lifecycler:`

**Pattern**: `blocks_storage:|s3:|gcs:|azure:|filesystem:`
- Cortex storage backends
- Example: `blocks_storage:\n  backend: s3`

**Pattern**: `ring:|memberlist:|consul:|etcd:`
- Cortex clustering
- Example: `ring:\n  kvstore:\n    store: memberlist`

---

## Environment Variables

- `CORTEX_CONFIG_FILE` - Configuration file path
- `CORTEX_TARGET` - Component to run

## Detection Notes

- Multi-tenant by design
- Compatible with Prometheus remote write
- Supports blocks or chunks storage
- Can run as microservices or monolith
- Similar to Grafana Mimir (fork)

---

## Secrets Detection

### Credentials

#### S3 Credentials
**Pattern**: `s3:.*secret_access_key:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: S3 secret access key
**Multiline**: true

#### GCS Credentials
**Pattern**: `gcs:.*service_account:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: GCS service account path
**Multiline**: true

---

## TIER 3: Configuration Extraction

### Target Extraction

**Pattern**: `target:\s*['"]?([a-z-]+)['"]?`
- Cortex target component
- Extracts: `target`
- Example: `target: all`

### Storage Backend Extraction

**Pattern**: `backend:\s*['"]?(s3|gcs|azure|filesystem)['"]?`
- Storage backend type
- Extracts: `storage_backend`
- Example: `backend: s3`

### Tenant ID Extraction

**Pattern**: `X-Scope-OrgID:\s*['"]?([^\s'"]+)['"]?`
- Tenant identifier
- Extracts: `tenant_id`
- Example: `X-Scope-OrgID: my-tenant`
