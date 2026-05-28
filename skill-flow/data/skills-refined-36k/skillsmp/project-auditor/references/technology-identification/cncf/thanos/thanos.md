# Thanos

**Category**: cncf
**Description**: Highly available Prometheus setup with long-term storage
**Homepage**: https://thanos.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Thanos Go packages*

- `github.com/thanos-io/thanos` - Thanos core
- `github.com/thanos-io/objstore` - Object storage client

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Thanos usage*

- `thanos.yaml` - Thanos configuration
- `bucket.yaml` - Object storage config
- `objstore.yaml` - Object store config

### Code Patterns

**Pattern**: `thanos\.io|thanos-`
- Thanos references
- Example: `image: quay.io/thanos/thanos:v0.32.0`

**Pattern**: `thanos\s+(sidecar|query|store|compact|receive|rule|query-frontend)`
- Thanos components
- Example: `thanos sidecar --prometheus.url=http://localhost:9090`

**Pattern**: `:10901|:10902|:10903|:10904`
- Thanos default ports
- Example: `--grpc-address=0.0.0.0:10901`

**Pattern**: `--objstore\.config|--objstore\.config-file`
- Object store configuration
- Example: `--objstore.config-file=/etc/thanos/bucket.yaml`

**Pattern**: `type:\s*(S3|GCS|AZURE|SWIFT|COS|ALIYUNOSS|FILESYSTEM)`
- Thanos bucket types
- Example: `type: S3`

**Pattern**: `--query\.replica-label|--store\.grpc`
- Thanos query flags
- Example: `--query.replica-label=prometheus_replica`

**Pattern**: `dedup|downsample|retention`
- Thanos features
- Example: `--retention.resolution-raw=30d`

---

## Environment Variables

- `THANOS_OBJSTORE_CONFIG` - Object store config
- `THANOS_QUERY_ENDPOINTS` - Query endpoints

## Detection Notes

- Extends Prometheus for HA and long-term storage
- Sidecar attaches to Prometheus
- Store Gateway serves historical data
- Compactor handles downsampling
- PromQL compatible via Query component

---

## Secrets Detection

### Credentials

#### S3 Access Key
**Pattern**: `access_key:\s*['"]?([A-Z0-9]+)['"]?`
**Severity**: critical
**Description**: S3 access key in bucket config

#### S3 Secret Key
**Pattern**: `secret_key:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: S3 secret key in bucket config

#### GCS Service Account
**Pattern**: `service_account:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: GCS service account key path

---

## TIER 3: Configuration Extraction

### Bucket Type Extraction

**Pattern**: `type:\s*['"]?([A-Z]+)['"]?`
- Object storage type
- Extracts: `bucket_type`
- Example: `type: S3`

### Bucket Name Extraction

**Pattern**: `bucket:\s*['"]?([a-zA-Z0-9._-]+)['"]?`
- Bucket name
- Extracts: `bucket_name`
- Example: `bucket: thanos-data`

### Retention Extraction

**Pattern**: `retention.*resolution-raw:\s*['"]?([0-9]+[dhw])['"]?`
- Raw data retention period
- Extracts: `retention_raw`
- Example: `--retention.resolution-raw=30d`
