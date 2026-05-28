# Private CA Issuers

Self-hosted certificate issuers for internal PKI without external CA dependencies.

## SelfSigned Issuer

Signs certificates with their own private key. Use for bootstrapping CA hierarchy or testing.

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned-issuer
spec:
  selfSigned: {}
```

### Bootstrap CA Pattern

Create root CA using SelfSigned, then use CA issuer for leaf certs:

```yaml
# 1. SelfSigned issuer for root
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned-issuer
spec:
  selfSigned: {}
---
# 2. Root CA certificate
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: root-ca
  namespace: cert-manager
spec:
  isCA: true
  commonName: root-ca
  secretName: root-ca-secret
  privateKey:
    algorithm: ECDSA
    size: 256
  issuerRef:
    name: selfsigned-issuer
    kind: ClusterIssuer
---
# 3. CA issuer using root
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: ca-issuer
spec:
  ca:
    secretName: root-ca-secret
```

### SelfSigned Limitations

- Clients cannot trust certs without pre-distributed CA
- Must set `spec.subject` on Certificate to avoid empty Issuer DN
- Use `trust-manager` to distribute CA across namespaces

## CA Issuer

Signs certificates using CA credentials stored in Kubernetes Secret.

### Secret Format

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ca-key-pair
  namespace: cert-manager
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded-certificate>
  tls.key: <base64-encoded-private-key>
```

For intermediate CAs, include full chain in `tls.crt`: issuer → intermediate(s) → root.

### CA Issuer Spec

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: ca-issuer
spec:
  ca:
    secretName: ca-key-pair
```

### CA Issuer Caveats

- No automatic CA rotation - monitor expiry manually
- Updating CA secret doesn't renew existing certs (use `cmctl renew`)
- No validation that CA has proper extensions (`isCA: true`, key usage)

## Vault Issuer

Signs certificates using HashiCorp Vault PKI secrets engine.

### Prerequisites

- Vault PKI secrets engine enabled
- PKI role configured with allowed domains
- Authentication method configured (AppRole, Kubernetes, Token, JWT)

### Vault Issuer Spec

```yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: vault-issuer
  namespace: sandbox
spec:
  vault:
    server: https://vault.example.com
    path: pki_int/sign/example-role  # Must use 'sign' endpoint
    caBundle: <base64-encoded-ca-bundle>
    auth:
      kubernetes:
        role: cert-manager
        mountPath: /v1/auth/kubernetes
        serviceAccountRef:
          name: cert-manager
```

### Vault Auth Methods

| Method | Use Case |
|--------|----------|
| `kubernetes` | Vault inside cluster or can reach K8s API |
| `appRole` | RoleID/SecretID stored in K8s Secret |
| `tokenSecretRef` | Pre-generated token (requires external refresh) |
| `jwt` | OIDC discovery reachable from Vault |

### Vault Debugging

```bash
# Verify issuer readiness
kubectl get issuer vault-issuer -n sandbox -o wide

# Check Vault connectivity (issuer tests v1/sys/health)
kubectl describe issuer vault-issuer -n sandbox
```

Common errors:
- `permission denied` - Vault policy doesn't allow cert signing
- `unknown role` - PKI role name incorrect in path
- `token expired` - Refresh token or use Kubernetes auth
