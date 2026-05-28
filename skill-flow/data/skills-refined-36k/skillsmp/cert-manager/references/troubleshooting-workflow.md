# cert-manager Troubleshooting Workflow

`kubectl describe` is the primary diagnostic tool. Avoid logs unless initial steps fail.

## Resource Chain Debugging

Certificate issues cascade through resources. Debug in this order:

```
Certificate → CertificateRequest → Issuer/ClusterIssuer → (Order → Challenge for ACME only)
```

### 1. Certificate

```bash
kubectl get certificate -n <namespace>
kubectl describe certificate <name> -n <namespace>
```

- `Ready: False` indicates issuance problems
- Check `Conditions` and `Events` sections
- Look for issuer reference errors, secret creation failures

### 2. CertificateRequest

```bash
kubectl get certificaterequest -n <namespace>
kubectl describe certificaterequest <name> -n <namespace>
```

- Created automatically when Certificate needs issuance
- Shows CSR validation status
- Check for issuer connectivity issues

### 3. Issuer/ClusterIssuer

```bash
kubectl describe issuer <name> -n <namespace>
kubectl describe clusterissuer <name>
```

- Verify `Ready: True` status
- Check authentication/connectivity to CA backend
- For Vault: verify token validity, path correctness

## Common Symptoms

| Symptom | Check |
|---------|-------|
| Certificate stuck `Pending` | CertificateRequest status, issuer readiness |
| Secret not created | Certificate events, issuer type matches spec |
| Certificate expired | Check `spec.renewBefore`, issuer availability |
| Wrong certificate content | Verify `dnsNames`, `commonName`, issuer chain |

## Useful Commands

```bash
# All cert-manager resources in namespace
kubectl get cert,cr,issuer,secret -n <namespace>

# Watch certificate status
kubectl get certificate -n <namespace> -w

# Force renewal (requires cmctl)
cmctl renew <certificate-name> -n <namespace>

# Check cert-manager controller logs
kubectl logs -n cert-manager deploy/cert-manager -f

# Decode certificate from secret
kubectl get secret <secret-name> -n <namespace> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout
```

## Events to Watch For

- `Issuing` - Certificate issuance started
- `Issued` - Certificate successfully issued
- `IssuerNotFound` - Referenced issuer doesn't exist
- `IssuerNotReady` - Issuer exists but not ready
- `PrivateKeyError` - Problem with private key generation
