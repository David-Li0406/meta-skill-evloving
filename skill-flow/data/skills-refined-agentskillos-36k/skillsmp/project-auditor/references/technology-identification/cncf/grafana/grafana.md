# Grafana

**Category**: cncf
**Description**: Observability platform for metrics, logs, and traces
**Homepage**: https://grafana.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Grafana packages*

- `@grafana/toolkit` - Grafana plugin development
- `@grafana/data` - Grafana data utilities
- `@grafana/ui` - Grafana UI components
- `@grafana/runtime` - Grafana runtime
- `@grafana/e2e` - E2E testing framework

#### GO
*Grafana Go packages*

- `github.com/grafana/grafana-plugin-sdk-go` - Plugin SDK

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Grafana usage*

- `grafana.ini` - Grafana configuration
- `defaults.ini` - Default configuration
- `provisioning/dashboards/*.yml` - Dashboard provisioning
- `provisioning/datasources/*.yml` - Datasource provisioning
- `plugin.json` - Plugin manifest
- `dashboards/*.json` - Dashboard JSON files

### Configuration Directories
*Known directories that indicate Grafana usage*

- `provisioning/` - Provisioning config
- `dashboards/` - Dashboard files
- `plugins/` - Plugin directory

### Code Patterns

**Pattern**: `grafana\.com|grafana-server|grafana\.ini`
- Grafana URLs and config
- Example: `https://grafana.example.com`

**Pattern**: `GRAFANA_|GF_`
- Grafana environment variables
- Example: `GF_SECURITY_ADMIN_PASSWORD`

**Pattern**: `:3000/d/|/api/dashboards/|grafana/api`
- Grafana API endpoints
- Example: `http://localhost:3000/d/abc123`

**Pattern**: `"type":\s*"dashboard"|"panels":\s*\[`
- Grafana dashboard JSON
- Example: Dashboard JSON structure

**Pattern**: `__expr__|__name__|__auto`
- Grafana query expressions
- Example: `__name__="up"`

---

## Environment Variables

- `GF_SECURITY_ADMIN_USER` - Admin username
- `GF_SECURITY_ADMIN_PASSWORD` - Admin password
- `GF_SERVER_ROOT_URL` - Root URL
- `GF_SERVER_HTTP_PORT` - HTTP port
- `GF_DATABASE_TYPE` - Database type
- `GF_DATABASE_HOST` - Database host
- `GF_DATABASE_NAME` - Database name
- `GF_DATABASE_USER` - Database user
- `GF_DATABASE_PASSWORD` - Database password
- `GF_AUTH_ANONYMOUS_ENABLED` - Anonymous access
- `GF_INSTALL_PLUGINS` - Plugins to install
- `GRAFANA_API_KEY` - API key for automation

## Detection Notes

- Default port is 3000
- GF_ prefix for all environment variables
- Provisioning for config as code
- Dashboard UIDs in URLs (/d/{uid})
- Plugin development uses @grafana packages

---

## Secrets Detection

### Credentials

#### Grafana Admin Password
**Pattern**: `GF_SECURITY_ADMIN_PASSWORD\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Grafana admin password
**Example**: `GF_SECURITY_ADMIN_PASSWORD=secret`

#### Grafana API Key
**Pattern**: `(?:grafana|GRAFANA).*(?:api[_-]?key|API[_-]?KEY)\s*[=:]\s*['"]?(eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*)['"]?`
**Severity**: critical
**Description**: Grafana API key (JWT format)
**Example**: `GRAFANA_API_KEY=eyJrIjoiYWJjMTIzLi4u`

#### Grafana Service Account Token
**Pattern**: `glsa_[A-Za-z0-9_]{32}_[A-Fa-f0-9]{8}`
**Severity**: critical
**Description**: Grafana service account token
**Example**: `glsa_abc123def456..._12345678`

#### Grafana Database Password
**Pattern**: `GF_DATABASE_PASSWORD\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Grafana database password
**Example**: `GF_DATABASE_PASSWORD=dbpass`

### Validation

#### API Documentation
- **HTTP API**: https://grafana.com/docs/grafana/latest/developers/http_api/

#### Validation Endpoint
**API**: Current User
**Endpoint**: `{grafana_url}/api/user`
**Method**: GET
**Headers**: `Authorization: Bearer {api_key}`
**Purpose**: Validates API key

---

## TIER 3: Configuration Extraction

### Root URL Extraction

**Pattern**: `(?:root_url|GF_SERVER_ROOT_URL)\s*[=:]\s*['"]?(https?://[^\s'"]+)['"]?`
- Grafana root URL
- Extracts: `root_url`
- Example: `GF_SERVER_ROOT_URL=https://grafana.example.com`

### Port Extraction

**Pattern**: `(?:http_port|GF_SERVER_HTTP_PORT)\s*[=:]\s*['"]?([0-9]+)['"]?`
- Grafana HTTP port
- Extracts: `http_port`
- Example: `GF_SERVER_HTTP_PORT=3000`
