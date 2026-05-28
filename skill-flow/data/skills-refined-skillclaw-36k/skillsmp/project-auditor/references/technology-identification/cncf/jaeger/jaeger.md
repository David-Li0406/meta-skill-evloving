# Jaeger

**Category**: cncf
**Description**: Distributed tracing platform
**Homepage**: https://jaegertracing.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Jaeger JavaScript packages*

- `jaeger-client` - Jaeger Node.js client

#### PYPI
*Jaeger Python packages*

- `jaeger-client` - Jaeger Python client

#### GO
*Jaeger Go packages*

- `github.com/jaegertracing/jaeger` - Jaeger core
- `github.com/uber/jaeger-client-go` - Jaeger Go client
- `github.com/jaegertracing/jaeger-client-go` - Official Go client

#### MAVEN
*Jaeger Java packages*

- `io.jaegertracing:jaeger-client` - Java client
- `io.jaegertracing:jaeger-core` - Core library
- `io.jaegertracing:jaeger-thrift` - Thrift transport

#### RUBYGEMS
*Jaeger Ruby packages*

- `jaeger-client` - Ruby client

---

## TIER 2: Deep Detection (File-based)

### Import Patterns

#### Go
Extensions: `.go`

**Pattern**: `"github\.com/uber/jaeger-client-go"`
- Jaeger Go client import
- Example: `import "github.com/uber/jaeger-client-go"`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+jaeger_client\s+import`
- Jaeger Python import
- Example: `from jaeger_client import Config`

#### Java
Extensions: `.java`

**Pattern**: `import\s+io\.jaegertracing\.`
- Jaeger Java import
- Example: `import io.jaegertracing.Configuration;`

### Code Patterns

**Pattern**: `jaegertracing\.io|jaeger-agent|jaeger-collector`
- Jaeger references
- Example: `jaeger-agent:6831`

**Pattern**: `JAEGER_|jaeger_`
- Jaeger environment variables
- Example: `JAEGER_AGENT_HOST`

**Pattern**: `:16686|:6831|:6832|:14268`
- Jaeger default ports
- Example: `localhost:16686`

**Pattern**: `sampler_type|sampler_param|reporter_`
- Jaeger configuration
- Example: `sampler_type: const`

---

## Environment Variables

- `JAEGER_AGENT_HOST` - Agent hostname
- `JAEGER_AGENT_PORT` - Agent port
- `JAEGER_ENDPOINT` - Collector endpoint
- `JAEGER_SAMPLER_TYPE` - Sampler type
- `JAEGER_SAMPLER_PARAM` - Sampler parameter
- `JAEGER_SERVICE_NAME` - Service name
- `JAEGER_TAGS` - Default tags
- `JAEGER_DISABLED` - Disable tracing
- `JAEGER_REPORTER_LOG_SPANS` - Log spans

## Detection Notes

- Default UI port is 16686
- Agent port 6831 for UDP spans
- Collector port 14268 for HTTP spans
- OpenTelemetry is successor but Jaeger still widely used

---

## Secrets Detection

### Credentials

#### Jaeger Auth Token
**Pattern**: `(?:jaeger|JAEGER).*(?:token|TOKEN|auth|AUTH)\s*[=:]\s*['"]?([a-zA-Z0-9._-]+)['"]?`
**Severity**: high
**Description**: Jaeger authentication token

---

## TIER 3: Configuration Extraction

### Agent Host Extraction

**Pattern**: `(?:JAEGER_AGENT_HOST|agent[_-]?host)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
- Jaeger agent host
- Extracts: `agent_host`
- Example: `JAEGER_AGENT_HOST=jaeger-agent`

### Service Name Extraction

**Pattern**: `(?:JAEGER_SERVICE_NAME|service[_-]?name)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
- Service name for tracing
- Extracts: `service_name`
- Example: `JAEGER_SERVICE_NAME=my-service`
