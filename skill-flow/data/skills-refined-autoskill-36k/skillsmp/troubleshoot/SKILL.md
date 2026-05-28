---
name: troubleshoot
description: Diagnose and fix issues with the Kubernetes cluster, Flux reconciliation, or deployed applications
---

# Troubleshoot Skill

Diagnose and resolve issues in the k3s homelab cluster.

## When to Use
- User reports application not working
- Flux reconciliation failures
- Pod crashes or restarts
- Network connectivity issues
- Certificate problems

## Diagnostic Commands

### Check Flux Status
```bash
flux get ks -A                    # Kustomization status
flux get hr -A                    # HelmRelease status
flux get sources all -A           # All sources (git, helm, oci)
flux logs --follow                # Flux controller logs
```

### Check Pod Status
```bash
kubectl get pods -A | grep -v Running
kubectl describe pod <pod> -n <namespace>
kubectl logs <pod> -n <namespace> --previous
```

### Check Events
```bash
kubectl get events -A --sort-by='.lastTimestamp' | tail -20
kubectl get events -n <namespace> --field-selector type=Warning
```

### Network Diagnostics
```bash
cilium status                     # CNI status
cilium connectivity test          # Network connectivity
kubectl get svc -A                # Services
kubectl get httproute -A          # Ingress routes
```

### Certificate Issues
```bash
kubectl get certificates -A
kubectl get certificaterequests -A
kubectl describe certificate <name> -n <namespace>
```

## Common Issues & Fixes

### HelmRelease Stuck
```bash
flux suspend hr <name> -n <namespace>
flux resume hr <name> -n <namespace>
# Or force reconcile:
flux reconcile hr <name> -n <namespace> --force
```

### Image Pull Errors
- Check if image exists and tag is correct
- Verify imagePullSecrets if private registry
- Check Spegel for cached images: `kubectl logs -n kube-system -l app.kubernetes.io/name=spegel`

### SOPS Decryption Failures
```bash
kubectl get secret -n flux-system sops-age
flux logs --kind=Kustomization --name=<ks-name>
```

### Node Issues (Talos)
```bash
talosctl -n <node-ip> health
talosctl -n <node-ip> dmesg | tail -50
talosctl -n <node-ip> services
```
