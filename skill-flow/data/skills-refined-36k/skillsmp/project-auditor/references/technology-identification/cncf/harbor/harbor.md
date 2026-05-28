# Harbor

**Category**: cncf
**Description**: Cloud-native container registry with security features
**Homepage**: https://goharbor.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Harbor Go packages*

- `github.com/goharbor/harbor` - Harbor core

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Harbor usage*

- `harbor.yml` - Harbor configuration
- `harbor.cfg` - Legacy configuration
- `docker-compose.yml` - Harbor compose file

### Code Patterns

**Pattern**: `goharbor\.io|harbor-core|harbor-portal`
- Harbor references
- Example: `harbor.example.com`

**Pattern**: `HARBOR_|harbor-`
- Harbor environment variables
- Example: `HARBOR_ADMIN_PASSWORD`

**Pattern**: `\.harbor\.|harbor\.yml|/harbor/`
- Harbor configuration references
- Example: `harbor.example.com/library/nginx`

**Pattern**: `:443/v2/|/api/v2\.0/|/chartrepo/`
- Harbor API endpoints
- Example: `https://harbor.example.com/api/v2.0/projects`

**Pattern**: `harbor\s+login|harbor\s+push`
- Harbor CLI commands
- Example: `harbor login harbor.example.com`

---

## Environment Variables

- `HARBOR_ADMIN_PASSWORD` - Admin password
- `HARBOR_DB_PASSWORD` - Database password
- `HARBOR_URL` - Harbor URL
- `HARBOR_USERNAME` - Harbor username
- `HARBOR_PASSWORD` - Harbor password
- `HARBOR_INSECURE` - Skip TLS verification
- `REGISTRY_STORAGE_S3_ACCESSKEY` - S3 access key
- `REGISTRY_STORAGE_S3_SECRETKEY` - S3 secret key

## Detection Notes

- Container registry with vulnerability scanning
- Supports Helm charts via ChartMuseum
- Robot accounts for CI/CD
- Replication for multi-site deployments

---

## Secrets Detection

### Credentials

#### Harbor Admin Password
**Pattern**: `(?:harbor|HARBOR).*(?:admin[_-]?password|ADMIN[_-]?PASSWORD)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Harbor admin password
**Example**: `HARBOR_ADMIN_PASSWORD=secret`

#### Harbor Robot Token
**Pattern**: `(?:harbor|HARBOR).*(?:robot[_-]?token|ROBOT[_-]?TOKEN)\s*[=:]\s*['"]?([a-zA-Z0-9._-]+)['"]?`
**Severity**: critical
**Description**: Harbor robot account token

#### Harbor Database Password
**Pattern**: `(?:harbor|HARBOR).*(?:db[_-]?password|DB[_-]?PASSWORD)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Harbor database password

### Validation

#### API Documentation
- **API Reference**: https://goharbor.io/docs/2.0.0/build-customize-contribute/configure-swagger/

---

## TIER 3: Configuration Extraction

### Harbor URL Extraction

**Pattern**: `(?:hostname|external_url|HARBOR_URL)\s*[=:]\s*['"]?(https?://[^\s'"]+)['"]?`
- Harbor instance URL
- Extracts: `harbor_url`
- Example: `hostname: harbor.example.com`

### Project Name Extraction

**Pattern**: `harbor\.example\.com/([a-z0-9_-]+)/`
- Project name from image reference
- Extracts: `project_name`
- Example: `harbor.example.com/myproject/nginx:latest`
