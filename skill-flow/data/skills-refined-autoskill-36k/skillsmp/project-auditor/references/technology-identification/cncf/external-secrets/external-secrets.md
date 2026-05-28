# External Secrets Operator

**Category**: cncf
**Description**: Kubernetes operator to synchronize secrets from external secret stores
**Homepage**: https://external-secrets.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*External Secrets Go packages*

- `github.com/external-secrets/external-secrets` - External Secrets Operator
- `github.com/external-secrets/external-secrets/apis` - API types

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate External Secrets usage*

- `externalsecret.yaml` - ExternalSecret resource
- `secretstore.yaml` - SecretStore configuration
- `clustersecretstore.yaml` - ClusterSecretStore configuration
- `external-secrets.yaml` - Installation manifest

### Code Patterns

**Pattern**: `external-secrets\.io/`
- External Secrets API group
- Example: `apiVersion: external-secrets.io/v1beta1`

**Pattern**: `kind:\s*(ExternalSecret|SecretStore|ClusterSecretStore|ClusterExternalSecret|PushSecret)`
- External Secrets CRD kinds
- Example: `kind: ExternalSecret`

**Pattern**: `secretStoreRef:|provider:|data:|dataFrom:`
- External Secret spec fields
- Example: `secretStoreRef:\n  name: aws-secretsmanager`

**Pattern**: `aws:\s*\n\s*service:\s*(SecretsManager|ParameterStore)`
- AWS provider configuration
- Example: `aws:\n  service: SecretsManager\n  region: us-east-1`

**Pattern**: `vault:\s*\n\s*server:|azurekv:|gcpsm:|doppler:|onepassword:`
- Secret store provider types
- Example: `vault:\n  server: https://vault.example.com`

**Pattern**: `refreshInterval:|target:\s*\n\s*name:`
- External Secret configuration
- Example: `refreshInterval: 1h`

**Pattern**: `remoteRef:\s*\n\s*key:`
- Remote secret reference
- Example: `remoteRef:\n  key: /my-app/database-password`

**Pattern**: `external-secrets-|es-controller|eso-`
- External Secrets component names
- Example: `external-secrets-cert-controller`

---

## Environment Variables

- `ESO_NAMESPACE` - External Secrets namespace
- `ESO_LOG_LEVEL` - Log level

## Detection Notes

- SecretStore/ClusterSecretStore define provider connections
- ExternalSecret syncs external secrets to K8s Secrets
- Supports AWS, Azure, GCP, HashiCorp Vault, and more
- PushSecret enables pushing K8s Secrets to external stores
- ClusterExternalSecret for multi-namespace secrets

---

## Secrets Detection

### Credentials

#### SecretStore Auth Secret
**Pattern**: `auth:\s*\n\s*secretRef:\s*\n\s*accessKeyIDSecretRef:`
**Severity**: critical
**Description**: AWS access key reference in SecretStore
**Multiline**: true

#### Vault Token Reference
**Pattern**: `tokenSecretRef:\s*\n\s*name:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Vault token secret reference
**Multiline**: true

#### Azure Client Secret
**Pattern**: `clientSecret:\s*\n\s*name:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Azure client secret reference
**Multiline**: true

---

## TIER 3: Configuration Extraction

### Secret Store Name

**Pattern**: `secretStoreRef:\s*\n\s*name:\s*['"]?([a-zA-Z0-9-]+)['"]?`
- Referenced secret store
- Extracts: `secret_store_name`
- Example: `secretStoreRef:\n  name: aws-secretsmanager`
**Multiline**: true

### Target Secret Name

**Pattern**: `target:\s*\n\s*name:\s*['"]?([a-zA-Z0-9-]+)['"]?`
- Target Kubernetes secret name
- Extracts: `target_secret`
- Example: `target:\n  name: my-app-secrets`
**Multiline**: true

### Refresh Interval

**Pattern**: `refreshInterval:\s*['"]?([0-9]+[smh])['"]?`
- Secret refresh interval
- Extracts: `refresh_interval`
- Example: `refreshInterval: 1h`

### Provider Region

**Pattern**: `region:\s*['"]?([a-z0-9-]+)['"]?`
- Cloud provider region
- Extracts: `provider_region`
- Example: `region: us-east-1`
