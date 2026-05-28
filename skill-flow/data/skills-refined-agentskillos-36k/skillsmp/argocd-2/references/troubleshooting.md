# ArgoCD Troubleshooting

## Application Sync Issues

### OutOfSync After Successful Sync

**Cause:** Field differences between desired and live state.

**Solutions:**
1. Check diff: `argocd app diff myapp`
2. Add to ignoreDifferences:
```yaml
spec:
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
        - /metadata/annotations/kubectl.kubernetes.io~1last-applied-configuration
```

### Stuck in Progressing

**Common causes:**
- Ingress controller not updating status
- StatefulSet waiting for PVCs
- Pods failing to start

**Debug:**
```bash
argocd app get myapp
kubectl describe deployment -n myapp myapp
kubectl get events -n myapp
```

### Sync Failed

**Check logs:**
```bash
argocd app sync myapp --dry-run
kubectl logs -n argocd deployment/argocd-repo-server
kubectl logs -n argocd deployment/argocd-application-controller
```

## Authentication Issues

### Forgot Admin Password

**ArgoCD 1.9+:**
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

**Reset password:**
```bash
# Generate bcrypt hash
argocd account bcrypt --password 'newpassword'

# Update secret
kubectl -n argocd patch secret argocd-secret \
  -p '{"stringData": {"admin.password": "$2a$10$...", "admin.passwordMtime": "'$(date +%FT%T%Z)'"}}'
```

### Disable Admin Account

```yaml
# argocd-cm ConfigMap
data:
  admin.enabled: "false"
```

### OIDC/SSO Issues

Check argocd-server logs:
```bash
kubectl logs -n argocd deployment/argocd-server | grep -i oidc
```

## Repository Connection Issues

### Permission Denied (SSH)

1. Verify SSH key: `ssh -T git@github.com`
2. Check key permissions: `chmod 600 ~/.ssh/id_rsa`
3. Add known hosts: `ssh-keyscan github.com | argocd cert add-ssh --batch`

### Certificate Errors (HTTPS)

1. Add CA certificate: `argocd cert add-tls git.example.com --from ca.pem`
2. Or skip verification (testing only): `--insecure-skip-server-verification`

### GitLab 301 Redirect

Add `.git` suffix to URL:
```bash
argocd repo add https://gitlab.example.com/org/repo.git
```

## CLI Issues

### "transport is closing" Error

**Cause:** Proxy incompatible with HTTP/2

**Solution:** Use gRPC-web:
```bash
argocd app list --grpc-web
# Or set default
export ARGOCD_OPTS='--grpc-web'
```

### Certificate Validation Error

```bash
argocd login myargocd.example.com --insecure
```

## Cluster Connectivity

### Test from ArgoCD Pod

```bash
kubectl exec -n argocd deployment/argocd-application-controller -- \
  argocd admin cluster kubeconfig https://kubernetes.default.svc

# Then test kubectl
kubectl exec -n argocd deployment/argocd-application-controller -- \
  kubectl --kubeconfig=/tmp/kubeconfig get nodes
```

### Network Policy Issues

Ensure argocd-application-controller can reach target cluster API servers.

## Resource Issues

### "Field not declared in schema"

**Cause:** Using fields not in ArgoCD's bundled schemas.

**Solutions:**
1. Use server-side apply: `ServerSideApply=true`
2. Skip validation: `Validate=false`

### Cached Manifest Error

**Clear cache:**
```bash
# Restart repo-server
kubectl rollout restart -n argocd deployment/argocd-repo-server
```

### Out of Memory

Increase limits:
```yaml
# argocd-repo-server deployment
resources:
  limits:
    memory: 2Gi
```

## Redis Issues

### Rotate Redis Secret

```bash
kubectl delete secret -n argocd argocd-redis
kubectl rollout restart -n argocd deployment/argocd-redis
kubectl rollout restart -n argocd deployment/argocd-server
kubectl rollout restart -n argocd deployment/argocd-repo-server
kubectl rollout restart -n argocd deployment/argocd-application-controller
```

## Performance Issues

### Slow Sync

1. Enable selective sync: `ApplyOutOfSyncOnly=true`
2. Increase parallelism in argocd-cm:
```yaml
data:
  controller.resource.parallelism.limit: "50"
```

### Too Many Applications

Use ApplicationSets instead of individual Applications for large deployments.

## Debugging Commands

```bash
# Application status
argocd app get myapp
argocd app diff myapp
argocd app manifests myapp

# Logs
kubectl logs -n argocd deployment/argocd-server
kubectl logs -n argocd deployment/argocd-repo-server
kubectl logs -n argocd deployment/argocd-application-controller
kubectl logs -n argocd deployment/argocd-applicationset-controller

# Events
kubectl get events -n argocd --sort-by='.lastTimestamp'

# RBAC testing
argocd admin settings rbac can myuser get applications 'default/*'
```
