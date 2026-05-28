# Open Policy Agent (OPA)

**Category**: cncf
**Description**: Policy engine for cloud-native environments
**Homepage**: https://www.openpolicyagent.org

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*OPA Go packages*

- `github.com/open-policy-agent/opa` - OPA core
- `github.com/open-policy-agent/opa/rego` - Rego language
- `github.com/open-policy-agent/opa/sdk` - OPA SDK
- `github.com/open-policy-agent/gatekeeper` - OPA Gatekeeper

#### PYPI
*OPA Python packages*

- `opa-python-client` - Python OPA client
- `regopy` - Rego Python bindings

#### NPM
*OPA Node.js packages*

- `@open-policy-agent/opa-wasm` - OPA WebAssembly
- `opa-wasm` - OPA WASM loader

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate OPA usage*

- `*.rego` - Rego policy files
- `policy.rego` - Policy definition
- `data.json` - Policy data
- `opa-config.yaml` - OPA configuration
- `.manifest` - OPA bundle manifest

### Code Patterns

**Pattern**: `package\s+[a-zA-Z0-9_.]+`
- Rego package declaration
- Example: `package authz`

**Pattern**: `import\s+data\.|import\s+future\.|import\s+input\.`
- Rego imports
- Example: `import data.kubernetes.pods`

**Pattern**: `default\s+\w+\s*=|allow\s*\{|deny\s*\{|violation\s*\[`
- Rego rule patterns
- Example: `default allow = false`

**Pattern**: `input\.[a-zA-Z_]+|data\.[a-zA-Z_]+`
- Rego input/data references
- Example: `input.request.user`

**Pattern**: `opa\s+(run|eval|test|build|check)`
- OPA CLI commands
- Example: `opa eval -d policy.rego "data.authz.allow"`

**Pattern**: `:8181/v1/data|:8181/v1/policies`
- OPA REST API endpoints
- Example: `POST /v1/data/authz/allow`

**Pattern**: `openpolicyagent\.org|opa-envoy|opa-istio`
- OPA ecosystem references
- Example: `openpolicyagent/opa:latest`

**Pattern**: `kind:\s*(ConstraintTemplate|K8sRequiredLabels)`
- Gatekeeper CRDs
- Example: `kind: ConstraintTemplate`

**Pattern**: `rego:\s*\|`
- Inline Rego in YAML
- Example: `rego: |`

---

## Environment Variables

- `OPA_LOG_LEVEL` - Log level
- `OPA_LOG_FORMAT` - Log format (json/text)
- `OPA_ADDR` - Listen address
- `OPA_CONFIG_FILE` - Configuration file path

## Detection Notes

- Rego is OPA's policy language
- Gatekeeper integrates OPA with Kubernetes
- Bundle API for policy distribution
- Decision logs for audit
- WASM compilation for edge deployment

---

## Secrets Detection

### Credentials

#### OPA Bearer Token
**Pattern**: `bearer_token:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Bearer token for OPA authentication

#### Bundle Service Credentials
**Pattern**: `credentials:\s*\n\s*bearer:\s*\n\s*token:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Bundle service authentication token
**Multiline**: true

---

## TIER 3: Configuration Extraction

### Package Name Extraction

**Pattern**: `package\s+([a-zA-Z0-9_.]+)`
- Rego package name
- Extracts: `package_name`
- Example: `package kubernetes.admission`

### Bundle URL Extraction

**Pattern**: `url:\s*['"]?(https?://[^\s'"]+)['"]?`
- Bundle service URL
- Extracts: `bundle_url`
- Example: `url: https://bundle-server.example.com`

### Decision Log Extraction

**Pattern**: `console:\s*(true|false)`
- Decision log console output
- Extracts: `decision_log_console`
- Example: `console: true`
