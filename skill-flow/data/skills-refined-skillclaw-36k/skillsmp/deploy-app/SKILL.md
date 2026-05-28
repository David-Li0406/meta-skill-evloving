---
name: deploy-app
description: Deploy a new application to the Kubernetes cluster using GitOps patterns
---

# Deploy Application Skill

Deploy a new application to the k3s homelab cluster following GitOps best practices.

## When to Use
- User wants to add a new application to the cluster
- User wants to deploy a Helm chart or container image
- User asks about deploying services

## MANDATORY CHECKLIST

**Every deployment MUST complete ALL of these steps:**

- [ ] 1. Research app requirements (ports, storage, database, env vars)
- [ ] 2. Create app directory structure
- [ ] 3. Create PVC if app needs persistent storage
- [ ] 4. Create ConfigMap if app needs configuration files
- [ ] 5. Create Secret (SOPS-encrypted) for sensitive data
- [ ] 6. Create HelmRelease using app-template chart
- [ ] 7. Create HTTPRoute for ingress (internal or external)
- [ ] 8. Create Flux Kustomization (ks.yaml)
- [ ] 9. Update parent kustomization.yaml to include new app
- [ ] 10. **ADD DNS ENTRY** to bind9 (172.16.1.10)
- [ ] 11. Create PR with all changes
- [ ] 12. Verify CI passes (Validate, Flux Diff)
- [ ] 13. Merge PR
- [ ] 14. Verify pod starts and is healthy

## Directory Structure

```
kubernetes/apps/<namespace>/<app-name>/
├── ks.yaml                    # Flux Kustomization
└── app/
    ├── kustomization.yaml     # Lists all resources
    ├── helmrelease.yaml       # App deployment via app-template
    ├── httproute.yaml         # Ingress route
    ├── pvc.yaml               # Persistent storage (if needed)
    ├── configmap.yaml         # Config files (if needed)
    └── secret.sops.yaml       # Secrets (if needed)
```

## Standard Templates

### 1. Flux Kustomization (`ks.yaml`)
```yaml
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: <app-name>
  namespace: <namespace>
spec:
  targetNamespace: <namespace>
  commonMetadata:
    labels:
      app.kubernetes.io/name: <app-name>
  path: ./kubernetes/apps/<namespace>/<app-name>/app
  prune: true
  sourceRef:
    kind: GitRepository
    name: flux-system
    namespace: flux-system
  wait: true
  interval: 30m
  retryInterval: 1m
  timeout: 5m
  dependsOn:
    - name: media-storage  # if needs NFS
```

### 2. App Kustomization (`app/kustomization.yaml`)
```yaml
---
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - pvc.yaml           # if needed
  - configmap.yaml     # if needed
  - secret.sops.yaml   # if needed
  - helmrelease.yaml
  - httproute.yaml
```

### 3. HelmRelease (`app/helmrelease.yaml`)
```yaml
---
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: <app-name>
spec:
  interval: 30m
  chart:
    spec:
      chart: app-template
      version: 3.6.1
      sourceRef:
        kind: HelmRepository
        name: bjw-s
        namespace: default
  values:
    controllers:
      <app-name>:
        replicas: 1
        strategy: RollingUpdate
        containers:
          app:
            image:
              repository: <image>
              tag: <tag>
            env:
              TZ: America/Los_Angeles
            probes:
              liveness: &probes
                enabled: true
                custom: true
                spec:
                  httpGet:
                    path: /health
                    port: &port <port>
                  initialDelaySeconds: 30
                  periodSeconds: 10
                  timeoutSeconds: 5
                  failureThreshold: 5
              readiness: *probes
            securityContext:
              allowPrivilegeEscalation: false
              readOnlyRootFilesystem: false
              capabilities:
                add: ["CHOWN", "SETGID", "SETUID", "DAC_OVERRIDE", "FOWNER"]

    defaultPodOptions:
      securityContext:
        runAsNonRoot: false
        runAsUser: 0
        runAsGroup: 0
        fsGroup: 1000
        fsGroupChangePolicy: OnRootMismatch
      tolerations:
        - key: "node.kubernetes.io/not-ready"
          operator: "Exists"
          effect: "NoExecute"
          tolerationSeconds: 30
        - key: "node.kubernetes.io/unreachable"
          operator: "Exists"
          effect: "NoExecute"
          tolerationSeconds: 30
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              preference:
                matchExpressions:
                  - key: node-role.kubernetes.io/control-plane
                    operator: DoesNotExist

    service:
      app:
        controller: <app-name>
        ports:
          http:
            port: *port

    persistence:
      config:
        enabled: true
        type: persistentVolumeClaim
        existingClaim: <app-name>-config
        globalMounts:
          - path: /config
      media:  # if needs media access
        enabled: true
        type: persistentVolumeClaim
        existingClaim: media-nfs
        globalMounts:
          - path: /media
```

### 4. HTTPRoute (`app/httproute.yaml`)
```yaml
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: <app-name>
spec:
  parentRefs:
    - name: envoy-internal      # or envoy-external for public
      namespace: network
  hostnames:
    - "<app-name>.ragas.cc"     # or ragas.sh for public
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /
      backendRefs:
        - name: <app-name>
          port: <port>
```

### 5. PVC (`app/pvc.yaml`)
```yaml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: <app-name>-config
  namespace: <namespace>
  annotations:
    kustomize.toolkit.fluxcd.io/prune: disabled
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 5Gi
  storageClassName: ceph-filesystem  # or ceph-block for databases
```

### 6. Secret (`app/secret.sops.yaml`)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: <app-name>-secret
  namespace: <namespace>
type: Opaque
stringData:
  KEY_NAME: <value>
```
Then encrypt: `SOPS_AGE_KEY_FILE=./age.key sops --encrypt --in-place <file>`

## DNS Configuration (CRITICAL - DO NOT SKIP)

**Internal services (*.ragas.cc):**
```bash
ssh root@172.16.1.10 "echo '<app-name>        IN      A       172.16.1.61' >> /etc/bind/db.ragas.cc && systemctl reload bind9"
```

**Verify:**
```bash
dig @172.16.1.10 <app-name>.ragas.cc +short
# Should return: 172.16.1.61
```

## Storage Decision Tree

| Use Case | Storage Class | Access Mode |
|----------|---------------|-------------|
| App configs (SQLite OK) | ceph-filesystem | ReadWriteMany |
| Databases (PostgreSQL) | ceph-block | ReadWriteOnce |
| Media files | media-nfs (existing PVC) | ReadOnlyMany |
| Backups | backup-nfs | ReadWriteMany |

## Database Integration

If app needs PostgreSQL, use the shared instance:
- Host: `postgres.database.svc.cluster.local`
- Port: `5432`
- User: `tipi`
- Create new database for the app
- Store password in SOPS secret

## Post-Deployment Verification

```bash
# Check Flux reconciliation
flux get ks <app-name> -n <namespace>

# Check HelmRelease
flux get hr <app-name> -n <namespace>

# Check pods
kubectl get pods -l app.kubernetes.io/name=<app-name> -n <namespace>

# Check logs
kubectl logs -l app.kubernetes.io/name=<app-name> -n <namespace>

# Test DNS
curl -I https://<app-name>.ragas.cc
```

## Common Issues

1. **Pod stuck in Pending**: Check PVC is bound, node has resources
2. **CrashLoopBackOff**: Check logs, verify env vars and secrets
3. **DNS not resolving**: Verify bind9 entry added and reloaded
4. **502 Bad Gateway**: Service port mismatch or pod not ready
