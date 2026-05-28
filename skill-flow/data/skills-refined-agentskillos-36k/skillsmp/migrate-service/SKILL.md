---
name: migrate-service
description: Migrate a service from Docker/LXC to Kubernetes
---

# Migrate Service Skill

Migrate services from Docker (LXC containers) or Runtipi to Kubernetes.

## When to Use
- User wants to move a service from LXC/Docker to K8s
- User mentions migrating from Runtipi, arr LXC, or other Docker hosts
- User asks to "migrate", "move", or "containerize" a service to K8s

## Pre-Migration Checklist

### 1. Verify Service is K8s-Compatible
Check AGENTS.md decision rules. **DO NOT migrate if:**
- Service needs GPU (Plex, Jellyfin)
- Service needs 2.5Gb NIC (qBittorrent)
- Service is DNS (AdGuard, bind9)
- Service needs USB passthrough

### 2. Identify Source Location

| Source | Config Path | Docker Compose |
|--------|-------------|----------------|
| Runtipi (172.16.1.7) | `/root/runtipi/app-data/migrated/<app>/data/` | N/A |
| arr LXC (172.16.1.31) | `/opt/stacks/<app>/` | Yes |
| torrent LXC (172.16.1.32) | `/opt/stacks/<app>/` | Yes |
| status LXC (172.16.1.249) | Varies | Yes |

### 3. Check Domain Requirements

**CRITICAL:** Some services have public domains on `ragas.sh`:
- `request.ragas.sh` → Overseerr (public)
- `plex.ragas.sh` → Plex (public)  
- `jelly.ragas.sh` → Jellyfin (public)

Internal services use `*.ragas.cc`. When migrating:
- If old config has `base_url: /app.ragas.sh/`, change to `base_url: /`
- Update bind9 DNS to point to `172.16.1.61` (envoy-internal)

## Migration Process

### Step 1: Backup Config from Source

```bash
# For Runtipi
ssh root@172.16.1.7 "tar -czf /tmp/<app>-config.tar.gz -C /root/runtipi/app-data/migrated/<app>/data ."
scp root@172.16.1.7:/tmp/<app>-config.tar.gz /tmp/

# For Docker LXC (arr, torrent, etc.)
ssh root@<LXC_IP> "tar -czf /tmp/<app>-config.tar.gz -C /opt/stacks/<app>/config ."
scp root@<LXC_IP>:/tmp/<app>-config.tar.gz /tmp/
```

### Step 2: Create K8s Manifests

Directory structure:
```
kubernetes/apps/default/<app>/
├── app/
│   ├── helmrelease.yaml
│   ├── httproute.yaml      # If needs ingress
│   ├── kustomization.yaml
│   └── secret.sops.yaml    # If needs secrets
└── ks.yaml
```

#### HelmRelease Template (bjw-s app-template)
```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: <app>
spec:
  interval: 30m
  chart:
    spec:
      chart: app-template
      version: 3.6.1
      sourceRef:
        kind: HelmRepository
        name: bjw-s
        namespace: flux-system
  values:
    controllers:
      <app>:
        containers:
          app:
            image:
              repository: ghcr.io/onedr0p/<app>  # or appropriate image
              tag: <version>
            env:
              TZ: America/Los_Angeles
            probes:
              liveness:
                enabled: true
                custom: true
                spec:
                  httpGet:
                    path: /health  # or /ping, /api/health
                    port: <port>
              readiness:
                enabled: true
                custom: true
                spec:
                  httpGet:
                    path: /health
                    port: <port>
            resources:
              requests:
                memory: 256Mi
              limits:
                memory: 1Gi
    service:
      app:
        controller: <app>
        ports:
          http:
            port: <port>
    persistence:
      config:
        existingClaim: <app>-config
      # NFS media mount (when NAS allows K8s workers)
      # media:
      #   type: nfs
      #   server: 172.16.1.250
      #   path: /volume2/media
      #   globalMounts:
      #     - path: /media
```

#### HTTPRoute Template
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: <app>
spec:
  parentRefs:
    - name: envoy-internal
      namespace: network
  hostnames:
    - "<app>.ragas.cc"
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /
      backendRefs:
        - name: <app>
          port: <port>
```

#### Flux Kustomization (ks.yaml)
```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: <app>
  namespace: default
spec:
  targetNamespace: default
  commonMetadata:
    labels:
      app.kubernetes.io/name: <app>
  interval: 1h
  path: ./kubernetes/apps/default/<app>/app
  prune: true
  sourceRef:
    kind: GitRepository
    name: flux-system
    namespace: flux-system
  wait: false
```

### Step 3: Create PVC

Add to helmrelease or create separately:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: <app>-config
spec:
  accessModes: ["ReadWriteOnce"]
  storageClassName: ceph-block
  resources:
    requests:
      storage: 1Gi
```

### Step 4: Register App

Add to `kubernetes/apps/default/kustomization.yaml`:
```yaml
resources:
  - <app>/ks.yaml
```

### Step 5: Deploy and Wait

```bash
git add -A && git commit -m "feat(<app>): migrate from <source> to k8s" && git push
flux reconcile ks cluster-apps -n flux-system --with-source
# Wait for pod to be running
kubectl get pods -n default -l app.kubernetes.io/name=<app> -w
```

### Step 6: Restore Config

```bash
# Copy backup to ansible node
scp /tmp/<app>-config.tar.gz root@172.16.1.9:/tmp/

# From ansible node, copy to pod and extract
POD=$(kubectl get pod -n default -l app.kubernetes.io/name=<app> -o jsonpath="{.items[0].metadata.name}")
kubectl cp /tmp/<app>-config.tar.gz default/$POD:/tmp/<app>-config.tar.gz
kubectl exec -n default $POD -- sh -c "cd /config && rm -rf * && tar -xzf /tmp/<app>-config.tar.gz"

# Fix base_url if needed (check app's config file)
kubectl exec -n default $POD -- sed -i 's|base_url:.*|base_url: /|' /config/config/config.yaml

# Restart pod
kubectl delete pod -n default $POD
```

### Step 7: Update DNS

On bind9 server (172.16.1.10):
```bash
ssh root@172.16.1.10
vim /etc/bind/db.ragas.cc
# Change: <app>  IN  A  <old_ip>
# To:     <app>  IN  A  172.16.1.61
# Increment serial number
systemctl reload bind9
```

### Step 8: Verify

```bash
curl -s http://172.16.1.61 -H "Host: <app>.ragas.cc" -o /dev/null -w "%{http_code}"
# Should return 200 or 302
```

### Step 9: Cleanup Source (Optional)

After confirming K8s deployment works:
```bash
# Stop old container
ssh root@<source_ip> "docker stop <app>" # or runtipi equivalent
# Keep config backup for 1 week before deleting
```

## Common Issues

### Pod stuck in ContainerCreating
- Check PVC is bound: `kubectl get pvc -n default`
- Check NFS mount (if enabled): NAS must allow K8s worker IPs

### HTTP 500 after deployment
- Check service name matches HTTPRoute backendRef
- App-template creates service named `<app>`, not `<app>-app`

### App shows setup wizard instead of config
- Config wasn't restored properly
- Check tar extraction path matches app's expected config location

### Base URL redirect loops
- Old config has wrong base_url
- Fix with sed and restart pod

## Service-Specific Notes

### Arr Stack (Sonarr, Radarr, Prowlarr)
- Config in `/config` directory
- Health endpoint: `/ping`
- Default ports: Sonarr=8989, Radarr=7878, Prowlarr=9696
- Need API keys for inter-service communication

### Overseerr
- Config in `/app/config`
- Health endpoint: `/api/v1/status`
- Port: 5055
- Has public domain `request.ragas.sh` - may need dual routing

### Speedtest Tracker
- Config in `/config`
- Port: 80
- Stateless - can deploy fresh

### NextGBA (Game emulator)
- Static files, minimal config
- Port: 80
- ROM storage may need NFS mount
