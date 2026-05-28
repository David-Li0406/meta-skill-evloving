---
name: upgrade-cluster
description: Upgrade Talos Linux, Kubernetes version, or cluster components safely
---

# Upgrade Cluster Skill

Safely upgrade Talos Linux, Kubernetes, and cluster components.

## When to Use
- User wants to upgrade Kubernetes version
- User wants to upgrade Talos Linux
- User wants to upgrade Cilium or other core components
- Security patches needed

## Pre-Upgrade Checklist

1. **Check current versions:**
   ```bash
   talosctl -n 172.16.1.50 version
   kubectl version
   cilium version
   flux version
   ```

2. **Verify cluster health:**
   ```bash
   kubectl get nodes
   talosctl -n 172.16.1.50 health
   flux get ks -A | grep -v "Applied"
   ```

3. **Check for pending HelmReleases:**
   ```bash
   flux get hr -A | grep -v "Release"
   ```

## Talos Upgrade Process

1. **Update Talos version pin** in `talos/talenv.yaml`
2. **Generate new configs:**
   ```bash
   task talos:generate-config
   ```
3. **Upgrade control plane nodes one at a time:**
   ```bash
   task talos:upgrade-node IP=172.16.1.50
   # Wait for node to rejoin
   kubectl get nodes -w
   task talos:upgrade-node IP=172.16.1.51
   task talos:upgrade-node IP=172.16.1.52
   ```
4. **Upgrade worker nodes:**
   ```bash
   task talos:upgrade-node IP=172.16.1.53
   ```

## Kubernetes Upgrade Process

1. **Update Kubernetes version pin** in `talos/talenv.yaml`
2. **Regenerate configs:**
   ```bash
   task talos:generate-config
   ```
3. **Apply to control plane:**
   ```bash
   task talos:upgrade-k8s
   ```

## Component Upgrades (GitOps)

Components upgrade automatically via Renovate PRs:
- Review Renovate PR for the component
- Check release notes for breaking changes
- Merge PR - Flux will reconcile

### Manual Component Upgrade
1. Update version in relevant HelmRelease
2. Commit and push
3. Monitor: `flux get hr <name> -n <namespace> -w`

## Rollback Procedures

### Talos Rollback
```bash
talosctl -n <node-ip> rollback
```

### Flux HelmRelease Rollback
```bash
flux suspend hr <name> -n <namespace>
# Revert git commit
git revert HEAD
git push
flux resume hr <name> -n <namespace>
```

## Post-Upgrade Verification
```bash
kubectl get nodes -o wide
flux get ks -A
flux get hr -A
cilium status
```
