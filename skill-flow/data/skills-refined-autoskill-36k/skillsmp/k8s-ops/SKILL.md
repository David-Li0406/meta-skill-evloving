---
name: k8s-ops
description: Kubernetes cluster operations, deployments, and troubleshooting. Use when deploying manifests, checking rollout status, monitoring pods, debugging failures, viewing logs, managing namespaces, or any kubectl operations. Triggers on mentions of kubernetes, k8s, kubectl, pods, deployments, services, namespaces, or cluster management.
---

# Kubernetes Operations

## Core Workflow

### Deployment Lifecycle

```bash
# 1. Validate before applying
kubectl apply --dry-run=server -f <manifest> -n <namespace>

# 2. Apply manifests
kubectl apply -f <manifest> -n <namespace>

# 3. Monitor rollout (blocks until complete or timeout)
kubectl rollout status deployment/<name> -n <namespace> --timeout=300s

# 4. Verify pods running
kubectl get pods -n <namespace> -l app=<label> -o wide

# 5. Check events for issues
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | tail -20
```

### Quick Health Check

```bash
# Cluster overview
kubectl cluster-info
kubectl get nodes -o wide
kubectl top nodes  # requires metrics-server

# Namespace health
kubectl get all -n <namespace>
kubectl get pods -n <namespace> -o wide
kubectl top pods -n <namespace>
```

## Troubleshooting Decision Tree

### Pod Not Starting

1. **Check pod status**: `kubectl get pods -n <ns> -o wide`
2. **Describe for events**: `kubectl describe pod <pod> -n <ns>`
3. **Check logs**: `kubectl logs <pod> -n <ns> --previous` (if crashed)

Common causes:
- `ImagePullBackOff`: Wrong image name/tag, missing imagePullSecrets
- `CrashLoopBackOff`: App crash - check logs, health probes too aggressive
- `Pending`: Insufficient resources, node selector/affinity issues
- `ContainerCreating`: Volume mount issues, init container stuck

### Pod Running But Not Receiving Traffic

1. **Check readiness**: `kubectl get pods -n <ns>` (READY column)
2. **Check endpoints**: `kubectl get endpoints <service> -n <ns>`
3. **Check service selector**: `kubectl describe service <svc> -n <ns>`
4. **Test connectivity**: `kubectl run debug --rm -it --image=busybox -- wget -qO- <service>:<port>`

### High Restart Count

```bash
# Get restart details
kubectl get pods -n <ns> -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.containerStatuses[0].restartCount}{"\n"}{end}'

# Check terminated state
kubectl get pod <pod> -n <ns> -o jsonpath='{.status.containerStatuses[0].lastState.terminated}'

# Review liveness probe config
kubectl get pod <pod> -n <ns> -o jsonpath='{.spec.containers[0].livenessProbe}'
```

## Common Operations

### Logs

```bash
# Single pod
kubectl logs <pod> -n <ns>
kubectl logs <pod> -n <ns> -c <container>  # multi-container
kubectl logs <pod> -n <ns> --previous      # crashed container
kubectl logs <pod> -n <ns> -f              # follow/stream

# All pods with label
kubectl logs -l app=<label> -n <ns> --all-containers

# Since time
kubectl logs <pod> -n <ns> --since=1h
kubectl logs <pod> -n <ns> --since-time="2024-01-01T00:00:00Z"
```

### Exec/Debug

```bash
# Interactive shell
kubectl exec -it <pod> -n <ns> -- /bin/sh
kubectl exec -it <pod> -n <ns> -c <container> -- /bin/bash

# Run command
kubectl exec <pod> -n <ns> -- <command>

# Debug with ephemeral container (k8s 1.25+)
kubectl debug -it <pod> -n <ns> --image=busybox --target=<container>
```

### Scaling

```bash
# Manual scale
kubectl scale deployment/<name> -n <ns> --replicas=3

# Autoscaling
kubectl autoscale deployment/<name> -n <ns> --min=2 --max=10 --cpu-percent=80
kubectl get hpa -n <ns>
```

### Rollback

```bash
# View history
kubectl rollout history deployment/<name> -n <ns>

# Rollback to previous
kubectl rollout undo deployment/<name> -n <ns>

# Rollback to specific revision
kubectl rollout undo deployment/<name> -n <ns> --to-revision=<N>

# Pause/resume rollout
kubectl rollout pause deployment/<name> -n <ns>
kubectl rollout resume deployment/<name> -n <ns>
```

### Resource Management

```bash
# Get resource usage
kubectl top pods -n <ns> --sort-by=memory
kubectl top pods -n <ns> --sort-by=cpu

# Describe resource limits
kubectl describe limitrange -n <ns>
kubectl describe resourcequota -n <ns>

# Get requests/limits for pods
kubectl get pods -n <ns> -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[0].resources}{"\n"}{end}'
```

## Context & Namespace Management

```bash
# View contexts
kubectl config get-contexts
kubectl config current-context

# Switch context
kubectl config use-context <context-name>

# Set default namespace
kubectl config set-context --current --namespace=<ns>

# Create namespace
kubectl create namespace <name>
```

## Output Formats

```bash
# Wide output with more columns
kubectl get pods -o wide

# YAML/JSON export
kubectl get deployment <name> -o yaml
kubectl get pod <name> -o json

# Custom columns
kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,IP:.status.podIP

# JSONPath
kubectl get pods -o jsonpath='{.items[*].metadata.name}'
kubectl get secret <name> -o jsonpath='{.data.password}' | base64 -d
```

## Port Forwarding

```bash
# Forward pod port
kubectl port-forward pod/<name> <local>:<remote> -n <ns>

# Forward service port
kubectl port-forward svc/<name> <local>:<remote> -n <ns>

# Forward deployment (picks a pod)
kubectl port-forward deployment/<name> <local>:<remote> -n <ns>
```

## Labels & Selectors

```bash
# Add label
kubectl label pods <pod> env=prod -n <ns>

# Remove label
kubectl label pods <pod> env- -n <ns>

# Select by label
kubectl get pods -l app=nginx,env=prod -n <ns>
kubectl get pods -l 'env in (prod,staging)' -n <ns>
kubectl delete pods -l app=test -n <ns>
```

## Resource Cleanup

```bash
# Delete by manifest
kubectl delete -f <manifest> -n <ns>

# Delete by label
kubectl delete pods -l app=<label> -n <ns>

# Force delete stuck pod
kubectl delete pod <pod> -n <ns> --grace-period=0 --force

# Delete completed/failed pods
kubectl delete pods -n <ns> --field-selector=status.phase=Succeeded
kubectl delete pods -n <ns> --field-selector=status.phase=Failed
```

## Health Probes Reference

### Probe Types
- **Liveness**: Is container alive? Failure → restart
- **Readiness**: Can container serve traffic? Failure → remove from endpoints
- **Startup**: Has app started? Blocks liveness/readiness until success

### Debugging Probes

```bash
# Check probe config
kubectl get pod <pod> -n <ns> -o yaml | grep -A10 livenessProbe

# Test HTTP probe manually
kubectl exec <pod> -n <ns> -- wget -qO- localhost:<port>/healthz

# Check probe events
kubectl describe pod <pod> -n <ns> | grep -A5 "Liveness\|Readiness"
```

## Tips

- Always use `-n <namespace>` explicitly to avoid mistakes
- Use `--dry-run=client -o yaml` to generate manifests
- Add `--watch` to continuously monitor: `kubectl get pods -w`
- Use `kubectl explain <resource>.<field>` to understand spec fields
- Annotate changes: `kubectl annotate deployment/<name> kubernetes.io/change-cause="<reason>"`
