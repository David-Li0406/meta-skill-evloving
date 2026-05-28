# Dapr

**Category**: cncf
**Description**: Distributed Application Runtime for microservices
**Homepage**: https://dapr.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Dapr Go packages*

- `github.com/dapr/dapr` - Dapr core
- `github.com/dapr/go-sdk` - Go SDK
- `github.com/dapr/components-contrib` - Components

#### NPM
*Dapr Node.js packages*

- `@dapr/dapr` - Node.js SDK
- `dapr-client` - Legacy client

#### PYPI
*Dapr Python packages*

- `dapr` - Python SDK
- `dapr-ext-grpc` - gRPC extension
- `dapr-ext-fastapi` - FastAPI integration

#### MAVEN
*Dapr Java packages*

- `io.dapr:dapr-sdk` - Java SDK
- `io.dapr:dapr-sdk-springboot` - Spring Boot integration

#### NUGET
*Dapr .NET packages*

- `Dapr.Client` - .NET SDK
- `Dapr.AspNetCore` - ASP.NET Core integration
- `Dapr.Actors` - Actor SDK

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Dapr usage*

- `dapr.yaml` - Dapr configuration
- `components/*.yaml` - Component configurations
- `config.yaml` - Dapr config
- `subscription.yaml` - Pub/sub subscription

### Configuration Directories
*Known directories that indicate Dapr usage*

- `.dapr/` - Dapr local config
- `components/` - Dapr components

### Code Patterns

**Pattern**: `dapr\.io/|dapr-`
- Dapr annotations and naming
- Example: `dapr.io/enabled: "true"`

**Pattern**: `kind:\s*(Component|Configuration|Subscription|Resiliency)`
- Dapr CRD kinds
- Example: `kind: Component`

**Pattern**: `apiVersion:\s*dapr\.io/v[0-9]+`
- Dapr API version
- Example: `apiVersion: dapr.io/v1alpha1`

**Pattern**: `dapr\s+(run|init|components|dashboard)`
- Dapr CLI commands
- Example: `dapr run --app-id myapp`

**Pattern**: `state\.|pubsub\.|bindings\.|secrets\.|actors\.`
- Dapr building blocks
- Example: `state.redis`

**Pattern**: `:3500/v1\.0/(state|invoke|publish|bindings|secrets)`
- Dapr HTTP API
- Example: `http://localhost:3500/v1.0/state/statestore`

**Pattern**: `daprd|dapr-sidecar-injector|dapr-placement`
- Dapr components
- Example: `daprd --app-id myapp`

**Pattern**: `@dapr|DaprClient|DaprServer`
- Dapr SDK references
- Example: `const { DaprClient } = require('@dapr/dapr')`

---

## Environment Variables

- `DAPR_HTTP_PORT` - Dapr HTTP port (default 3500)
- `DAPR_GRPC_PORT` - Dapr gRPC port (default 50001)
- `APP_PORT` - Application port
- `DAPR_API_TOKEN` - API token
- `NAMESPACE` - Kubernetes namespace

## Detection Notes

- Sidecar architecture pattern
- Building blocks: state, pub/sub, bindings, actors
- Component model for pluggable infrastructure
- Multi-runtime support via SDKs
- Default HTTP port 3500, gRPC 50001

---

## Secrets Detection

### Credentials

#### Dapr API Token
**Pattern**: `DAPR_API_TOKEN\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Dapr API authentication token

#### Component Secret
**Pattern**: `secretKeyRef:\s*\n\s*name:\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: Kubernetes secret reference in component
**Multiline**: true

---

## TIER 3: Configuration Extraction

### Component Type Extraction

**Pattern**: `type:\s*['"]?([a-z]+\.[a-z0-9]+)['"]?`
- Dapr component type
- Extracts: `component_type`
- Example: `type: state.redis`

### App ID Extraction

**Pattern**: `dapr\.io/app-id:\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- Dapr application ID
- Extracts: `app_id`
- Example: `dapr.io/app-id: myapp`

### App Port Extraction

**Pattern**: `dapr\.io/app-port:\s*['"]?([0-9]+)['"]?`
- Application listening port
- Extracts: `app_port`
- Example: `dapr.io/app-port: "3000"`
