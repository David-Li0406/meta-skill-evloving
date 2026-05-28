# Webhook Troubleshooting

cert-manager webhook validates and mutates Certificate resources. Webhook failures block all cert-manager operations.

## Connection Refused

**Error:** `dial tcp 10.96.20.99:443: connect: connection refused`

**Cause:** No service listening on webhook port.

**Debug:**
```bash
# Check endpoints
kubectl get endpoints -n cert-manager cert-manager-webhook

# Check pod status
kubectl get pod -n cert-manager -l app.kubernetes.io/name=webhook

# Test port-forward
kubectl port-forward -n cert-manager deploy/cert-manager-webhook 10250
curl -k https://localhost:10250/healthz
```

## I/O Timeout

**Error:** `dial tcp 10.0.0.69:443: i/o timeout`

**Cause:** Network policy or firewall blocking API server → webhook traffic.

| Environment | Fix |
|-------------|-----|
| GKE Private | Set `webhook.securePort=10250` or `443` |
| EKS Custom CNI | Set `webhook.hostNetwork=true`, `webhook.securePort=10260` |
| Calico | Allow TCP 10250 from API server |
| EKS Security Groups | Allow TCP 10250 between control plane and workers |

## TLS Certificate Errors

**Error:** `x509: certificate signed by unknown authority`

**Cause:** CA bundle not injected into webhook configuration.

**Debug:**
```bash
# Check cainjector logs
kubectl logs -n cert-manager deploy/cert-manager-cainjector

# Verify CA secret exists
kubectl get secret -n cert-manager cert-manager-webhook-ca

# Check webhook config CA bundle
kubectl get validatingwebhookconfiguration cert-manager-webhook -o yaml | grep caBundle
```

## EKS Fargate Certificate Mismatch

**Error:** `x509: certificate is valid for ip-192-168-xxx-xxx.xxx.compute.internal`

**Fix:** Change webhook port to avoid kubelet port conflict:
```bash
helm upgrade cert-manager jetstack/cert-manager --set webhook.securePort=10260
```

## Context Deadline Exceeded

**Error:** `context deadline exceeded`

**Debug:**
```bash
# Increase timeout and test manually
kubectl port-forward -n cert-manager deploy/cert-manager-webhook 10250
curl -k --connect-timeout 30 https://localhost:10250/healthz
```

If curl succeeds: webhook-side issue (check logs)
If curl fails: network/connectivity issue

## GKE Autopilot

**Error:** Leader election fails in kube-system.

**Fix:**
```bash
helm upgrade cert-manager jetstack/cert-manager \
  --set global.leaderElection.namespace=cert-manager
```

## Quick Checks

```bash
# All cert-manager pods healthy
kubectl get pods -n cert-manager

# Webhook logs
kubectl logs -n cert-manager deploy/cert-manager-webhook

# cainjector logs
kubectl logs -n cert-manager deploy/cert-manager-cainjector

# Test webhook endpoint
kubectl run curl --rm -it --image=curlimages/curl -- \
  curl -k https://cert-manager-webhook.cert-manager.svc:443/healthz
```
