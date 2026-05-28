---
name: k8s-debug
description: Kubernetes troubleshooting and debugging workflows. Use when diagnosing pod failures, networking issues, resource problems, CrashLoopBackOff, ImagePullBackOff, pending pods, OOMKilled, or any cluster issues. Covers systematic debugging approaches and common failure patterns.
---

# Kubernetes Troubleshooting

## Diagnostic Commands Cheatsheet

```bash
# Quick cluster health
kubectl get nodes
kubectl get pods -A | grep -v Running
kubectl get events -A --sort-by='.lastTimestamp' | tail -30

# Namespace health
kubectl get all -n <ns>
kubectl get events -n <ns> --sort-by='.lastTimestamp'
kubectl top pods -n <ns>
```

## Pod Status Troubleshooting

### CrashLoopBackOff

**Symptoms**: Pod restarts repeatedly, status shows CrashLoopBackOff

**Diagnosis**:
```bash
# Check exit code and reason
kubectl describe pod <pod> -n <ns> | grep -A10 "Last State"

# View logs from crashed container
kubectl logs <pod> -n <ns> --previous

# Check if OOMKilled
kubectl get pod <pod> -n <ns> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'
```

**Common Causes**:
- Application crash (check logs)
- OOMKilled (increase memory limits)
- Liveness probe too aggressive
- Missing dependencies/config
- Permission issues

**Fixes**:
```bash
# Increase memory if OOMKilled
kubectl set resources deployment/<name> -n <ns> --limits=memory=1Gi

# Disable liveness probe temporarily for debugging
kubectl edit deployment/<name> -n <ns>  # Remove livenessProbe

# Shell into running container to debug
kubectl exec -it <pod> -n <ns> -- /bin/sh
```

### ImagePullBackOff

**Symptoms**: Pod stuck in ImagePullBackOff or ErrImagePull

**Diagnosis**:
```bash
kubectl describe pod <pod> -n <ns> | grep -A5 "Events"
# Look for: "Failed to pull image" messages
```

**Common Causes**:
- Image doesn't exist (typo in name/tag)
- Private registry without imagePullSecrets
- Registry authentication failed
- Network issues to registry

**Fixes**:
```bash
# Verify image exists
docker pull <image>

# Check imagePullSecrets
kubectl get pod <pod> -n <ns> -o jsonpath='{.spec.imagePullSecrets}'

# Create registry secret
kubectl create secret docker-registry regcred \
  --docker-server=<registry> \
  --docker-username=<user> \
  --docker-password=<pass> \
  -n <ns>

# Add to deployment
kubectl patch deployment <name> -n <ns> -p '{"spec":{"template":{"spec":{"imagePullSecrets":[{"name":"regcred"}]}}}}'
```

### Pending

**Symptoms**: Pod stuck in Pending state

**Diagnosis**:
```bash
kubectl describe pod <pod> -n <ns> | grep -A10 "Events"
# Look for scheduling failure reasons
```

**Common Causes**:
- Insufficient CPU/memory
- Node selector/affinity mismatch
- Taint without toleration
- PVC not bound
- Resource quota exceeded

**Fixes**:
```bash
# Check node resources
kubectl describe nodes | grep -A5 "Allocated resources"

# Check taints
kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints

# Check PVC status
kubectl get pvc -n <ns>

# Check resource quota
kubectl describe resourcequota -n <ns>
```

### CreateContainerConfigError

**Symptoms**: Pod in CreateContainerConfigError state

**Diagnosis**:
```bash
kubectl describe pod <pod> -n <ns> | grep -A5 "Warning"
```

**Common Causes**:
- ConfigMap doesn't exist
- Secret doesn't exist
- Volume mount issues

**Fixes**:
```bash
# Check if configmap exists
kubectl get configmap <name> -n <ns>

# Check if secret exists
kubectl get secret <name> -n <ns>

# List expected volumes
kubectl get pod <pod> -n <ns> -o jsonpath='{.spec.volumes[*].name}'
```

### OOMKilled

**Symptoms**: Container terminated with OOMKilled reason, exit code 137

**Diagnosis**:
```bash
kubectl describe pod <pod> -n <ns> | grep -A5 "Last State"
kubectl top pod <pod> -n <ns>

# Check limits
kubectl get pod <pod> -n <ns> -o jsonpath='{.spec.containers[0].resources}'
```

**Fixes**:
```bash
# Increase memory limit
kubectl set resources deployment/<name> -n <ns> --limits=memory=2Gi

# Or patch
kubectl patch deployment <name> -n <ns> --type='json' -p='[
  {"op":"replace","path":"/spec/template/spec/containers/0/resources/limits/memory","value":"2Gi"}
]'
```

## Service & Networking Issues

### Service Not Reaching Pods

**Diagnosis**:
```bash
# Check endpoints
kubectl get endpoints <service> -n <ns>
# Empty endpoints = selector mismatch or no ready pods

# Check service selector
kubectl get svc <service> -n <ns> -o jsonpath='{.spec.selector}'

# Check pod labels
kubectl get pods -n <ns> --show-labels

# Test from within cluster
kubectl run debug --rm -it --image=busybox -n <ns> -- wget -qO- <service>:<port>
```

**Common Causes**:
- Selector doesn't match pod labels
- No ready pods (readiness probe failing)
- Wrong port configuration
- Network policy blocking traffic

**Fixes**:
```bash
# Fix selector
kubectl patch svc <service> -n <ns> -p '{"spec":{"selector":{"app":"correct-label"}}}'

# Check readiness
kubectl get pods -n <ns> -o wide  # Check READY column
kubectl describe pod <pod> -n <ns> | grep -A10 "Readiness"
```

### DNS Issues

**Diagnosis**:
```bash
# Test DNS from pod
kubectl run dns-test --rm -it --image=busybox -- nslookup kubernetes.default
kubectl run dns-test --rm -it --image=busybox -- nslookup <service>.<namespace>.svc.cluster.local

# Check CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns
```

### Ingress Not Working

**Diagnosis**:
```bash
# Check ingress status
kubectl describe ingress <name> -n <ns>

# Check ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# Verify backend service
kubectl get svc <backend-service> -n <ns>
kubectl get endpoints <backend-service> -n <ns>
```

## Volume Issues

### PVC Stuck in Pending

**Diagnosis**:
```bash
kubectl describe pvc <name> -n <ns>
kubectl get storageclass
kubectl get pv
```

**Common Causes**:
- No matching StorageClass
- StorageClass provisioner not working
- Zone/region mismatch
- Capacity exceeded

### Volume Mount Failures

**Diagnosis**:
```bash
kubectl describe pod <pod> -n <ns> | grep -A10 "Volumes"
kubectl describe pod <pod> -n <ns> | grep -A10 "Mounts"
kubectl get events -n <ns> | grep -i volume
```

## Node Issues

### Node NotReady

**Diagnosis**:
```bash
kubectl describe node <node> | grep -A10 "Conditions"
kubectl get events --field-selector involvedObject.name=<node>

# Check kubelet logs (on node)
journalctl -u kubelet -n 100
```

**Common Causes**:
- Kubelet not running
- Network issues
- Disk pressure
- Memory pressure
- Too many pods

### Drain & Cordon

```bash
# Mark node unschedulable
kubectl cordon <node>

# Drain (evict pods)
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data

# Uncordon
kubectl uncordon <node>
```

## Resource Debugging

### Check Resource Pressure

```bash
# Node resources
kubectl top nodes
kubectl describe nodes | grep -A5 "Allocated resources"

# Pod resources
kubectl top pods -n <ns> --sort-by=memory
kubectl top pods -n <ns> --sort-by=cpu

# Resource quotas
kubectl describe resourcequota -n <ns>
kubectl describe limitrange -n <ns>
```

### Find Resource Hogs

```bash
# Top memory consumers
kubectl top pods -A --sort-by=memory | head -20

# Top CPU consumers
kubectl top pods -A --sort-by=cpu | head -20

# Pods without limits
kubectl get pods -A -o json | jq -r '.items[] | select(.spec.containers[].resources.limits == null) | .metadata.namespace + "/" + .metadata.name'
```

## Debug Containers

### Ephemeral Debug Container (k8s 1.25+)

```bash
# Add debug container to running pod
kubectl debug -it <pod> -n <ns> --image=busybox --target=<container>

# Debug with network tools
kubectl debug -it <pod> -n <ns> --image=nicolaka/netshoot --target=<container>
```

### Debug Pod Copy

```bash
# Create copy with different command
kubectl debug <pod> -n <ns> --copy-to=debug-pod --container=<container> -- sleep infinity

# Then exec into it
kubectl exec -it debug-pod -n <ns> -- /bin/sh
```

### Standalone Debug Pod

```bash
# Network debugging
kubectl run netshoot --rm -it --image=nicolaka/netshoot -n <ns> -- /bin/bash

# Common debug commands inside:
curl -v http://<service>:<port>/
nslookup <service>
ping <pod-ip>
traceroute <service>
nc -zv <service> <port>
```

## Log Analysis

```bash
# Follow logs
kubectl logs -f <pod> -n <ns>

# All containers
kubectl logs <pod> -n <ns> --all-containers

# Previous container (after crash)
kubectl logs <pod> -n <ns> --previous

# Since time
kubectl logs <pod> -n <ns> --since=1h
kubectl logs <pod> -n <ns> --since-time="2024-01-01T00:00:00Z"

# Tail specific lines
kubectl logs <pod> -n <ns> --tail=100

# Multiple pods
kubectl logs -l app=<label> -n <ns> --all-containers

# With timestamps
kubectl logs <pod> -n <ns> --timestamps
```

## Events

```bash
# Namespace events
kubectl get events -n <ns> --sort-by='.lastTimestamp'

# Watch events
kubectl get events -n <ns> -w

# Filter warnings
kubectl get events -n <ns> --field-selector type=Warning

# Pod-specific events
kubectl get events -n <ns> --field-selector involvedObject.name=<pod>
```

## Quick Diagnostic Script

```bash
#!/usr/bin/env bash
# k8s-diag.sh - Quick namespace diagnostic

NS="${1:?Usage: $0 <namespace>}"

echo "=== Namespace: $NS ==="
echo ""
echo "--- Pod Status ---"
kubectl get pods -n "$NS" -o wide
echo ""
echo "--- Non-Running Pods ---"
kubectl get pods -n "$NS" | grep -v Running | grep -v Completed
echo ""
echo "--- Recent Events ---"
kubectl get events -n "$NS" --sort-by='.lastTimestamp' | tail -20
echo ""
echo "--- Resource Usage ---"
kubectl top pods -n "$NS" 2>/dev/null || echo "Metrics not available"
echo ""
echo "--- Services ---"
kubectl get svc -n "$NS"
echo ""
echo "--- Endpoints ---"
kubectl get endpoints -n "$NS"
```

## Common Fixes Quick Reference

| Problem | Quick Fix |
|---------|-----------|
| CrashLoopBackOff | `kubectl logs <pod> --previous` then fix app |
| ImagePullBackOff | Verify image name, create imagePullSecret |
| Pending (resources) | Scale down other pods or add nodes |
| Pending (PVC) | Check StorageClass and provisioner |
| OOMKilled | Increase memory limits |
| Readiness failing | Check probe endpoint, increase timeout |
| No endpoints | Fix service selector to match pod labels |
| DNS failure | Check CoreDNS pods in kube-system |
| Permission denied | Check RBAC, ServiceAccount |
