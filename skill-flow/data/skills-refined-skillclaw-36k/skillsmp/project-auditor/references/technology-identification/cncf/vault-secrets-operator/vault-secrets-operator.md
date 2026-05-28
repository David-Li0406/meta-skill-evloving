# Vault Secrets Operator

**Category**: cncf
**Description**: HashiCorp Vault Secrets Operator for Kubernetes
**Homepage**: https://developer.hashicorp.com/vault/docs/platform/k8s/vso

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Vault Secrets Operator Go packages*

- `github.com/hashicorp/vault-secrets-operator` - VSO core
- `github.com/hashicorp/vault/api` - Vault API client
- `github.com/hashicorp/vault-client-go` - New Vault client

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Vault Secrets Operator usage*

- `vaultauth.yaml` - VaultAuth resource
- `vaultconnection.yaml` - VaultConnection resource
- `vaultstaticsecret.yaml` - VaultStaticSecret resource
- `vaultdynamicsecret.yaml` - VaultDynamicSecret resource
- `vaultpkisecret.yaml` - VaultPKISecret resource

### Code Patterns

**Pattern**: `secrets\.hashicorp\.com/`
- Vault Secrets Operator API group
- Example: `apiVersion: secrets.hashicorp.com/v1beta1`

**Pattern**: `kind:\s*(VaultAuth|VaultConnection|VaultStaticSecret|VaultDynamicSecret|VaultPKISecret)`
- VSO CRD kinds
- Example: `kind: VaultStaticSecret`

**Pattern**: `vaultAuthRef:|vaultConnectionRef:|mount:|path:`
- VSO spec fields
- Example: `vaultAuthRef: default`

**Pattern**: `method:\s*(kubernetes|jwt|appRole|aws|gcp|ldap|userpass)`
- Vault authentication methods
- Example: `method: kubernetes`

**Pattern**: `kubernetes:\s*\n\s*role:|jwt:\s*\n\s*role:|appRole:\s*\n\s*roleId:`
- Auth method configuration
- Example: `kubernetes:\n  role: my-role`

**Pattern**: `refreshAfter:|rolloutRestartTargets:|destination:`
- VSO sync configuration
- Example: `refreshAfter: 1m`

**Pattern**: `vault-secrets-operator|vso-`
- VSO component names
- Example: `vault-secrets-operator-controller-manager`

**Pattern**: `VAULT_ADDR|VAULT_TOKEN|VAULT_NAMESPACE`
- Vault environment variables
- Example: `VAULT_ADDR=https://vault.example.com`

---

## Environment Variables

- `VAULT_ADDR` - Vault server address
- `VAULT_NAMESPACE` - Vault namespace (Enterprise)
- `VAULT_TOKEN` - Vault token (for testing)
- `VAULT_CACERT` - CA certificate path
- `VAULT_SKIP_VERIFY` - Skip TLS verification

## Detection Notes

- VaultConnection defines how to connect to Vault
- VaultAuth defines authentication method
- VaultStaticSecret syncs KV secrets
- VaultDynamicSecret generates dynamic credentials
- VaultPKISecret for PKI certificate management
- Supports secret rotation and workload restarts

---

## Secrets Detection

### Credentials

#### Vault Token
**Pattern**: `VAULT_TOKEN\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Vault authentication token

#### AppRole Secret ID
**Pattern**: `secretId:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Vault AppRole secret ID

#### AppRole Role ID
**Pattern**: `roleId:\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: Vault AppRole role ID

---

## TIER 3: Configuration Extraction

### Vault Address

**Pattern**: `address:\s*['"]?(https?://[^\s'"]+)['"]?`
- Vault server address
- Extracts: `vault_address`
- Example: `address: https://vault.example.com:8200`

### Mount Path

**Pattern**: `mount:\s*['"]?([a-zA-Z0-9/_-]+)['"]?`
- Vault secrets engine mount path
- Extracts: `mount_path`
- Example: `mount: secret`

### Secret Path

**Pattern**: `path:\s*['"]?([a-zA-Z0-9/_-]+)['"]?`
- Secret path within the mount
- Extracts: `secret_path`
- Example: `path: data/my-app/config`

### Refresh Interval

**Pattern**: `refreshAfter:\s*['"]?([0-9]+[smh])['"]?`
- Secret refresh interval
- Extracts: `refresh_after`
- Example: `refreshAfter: 5m`

### Kubernetes Auth Role

**Pattern**: `kubernetes:\s*\n\s*role:\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- Kubernetes auth role
- Extracts: `k8s_auth_role`
- Example: `kubernetes:\n  role: my-app-role`
**Multiline**: true
