# Apache Pulsar

**Category**: apache
**Description**: Cloud-native distributed messaging and streaming platform
**Homepage**: https://pulsar.apache.org

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Pulsar Node.js client*

- `pulsar-client` - Official Node.js client

#### PYPI
*Pulsar Python client*

- `pulsar-client` - Official Python client

#### GO
*Pulsar Go client*

- `github.com/apache/pulsar-client-go` - Official Go client

#### MAVEN
*Pulsar Java client*

- `org.apache.pulsar:pulsar-client` - Java client
- `org.apache.pulsar:pulsar-client-admin` - Admin client
- `org.apache.pulsar:pulsar-functions-api` - Functions API

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Pulsar usage*

- `broker.conf` - Pulsar broker configuration
- `standalone.conf` - Standalone configuration
- `client.conf` - Client configuration
- `functions_worker.yml` - Functions worker config

### Import Patterns

#### Python
Extensions: `.py`

**Pattern**: `^import\s+pulsar`
- Pulsar Python import
- Example: `import pulsar`

**Pattern**: `^from\s+pulsar\s+import`
- Pulsar Python import
- Example: `from pulsar import Client`

#### Java
Extensions: `.java`

**Pattern**: `import\s+org\.apache\.pulsar\.`
- Pulsar Java import
- Example: `import org.apache.pulsar.client.api.PulsarClient;`

#### Go
Extensions: `.go`

**Pattern**: `"github\.com/apache/pulsar-client-go/pulsar"`
- Pulsar Go import
- Example: `import "github.com/apache/pulsar-client-go/pulsar"`

### Code Patterns

**Pattern**: `pulsar://|pulsar\+ssl://`
- Pulsar URL schemes
- Example: `pulsar://localhost:6650`

**Pattern**: `PULSAR_|pulsar\.`
- Pulsar configuration
- Example: `PULSAR_BROKER_URL`

**Pattern**: `:6650|:6651|:8080/admin`
- Pulsar default ports
- Example: `localhost:6650`

**Pattern**: `PulsarClient\.builder\(|Client\(`
- Pulsar client creation
- Example: `PulsarClient.builder().serviceUrl("pulsar://...").build()`

---

## Environment Variables

- `PULSAR_BROKER_URL` - Pulsar broker URL
- `PULSAR_SERVICE_URL` - Service URL
- `PULSAR_AUTH_PLUGIN` - Authentication plugin
- `PULSAR_AUTH_PARAMS` - Authentication parameters
- `PULSAR_TLS_CERT` - TLS certificate
- `PULSAR_TOKEN` - JWT token

## Detection Notes

- Default broker port is 6650
- Admin API on port 8080
- Multi-tenancy with tenant/namespace/topic hierarchy
- Functions are serverless compute on Pulsar

---

## Secrets Detection

### Credentials

#### Pulsar JWT Token
**Pattern**: `(?:pulsar|PULSAR).*(?:token|TOKEN)\s*[=:]\s*['"]?(eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*)['"]?`
**Severity**: critical
**Description**: Pulsar JWT authentication token
**Example**: `PULSAR_TOKEN=eyJhbGciOiJIUzI1NiJ9...`

#### Pulsar Auth Params
**Pattern**: `(?:authParams|auth[_-]?params)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: Pulsar authentication parameters
**Context Required**: Near pulsar configuration

---

## TIER 3: Configuration Extraction

### Service URL Extraction

**Pattern**: `(?:serviceUrl|service[_-]?url|PULSAR_BROKER_URL)\s*[=:]\s*['"]?(pulsar(?:\+ssl)?://[^\s'"]+)['"]?`
- Pulsar service URL
- Extracts: `service_url`
- Example: `serviceUrl=pulsar://localhost:6650`
