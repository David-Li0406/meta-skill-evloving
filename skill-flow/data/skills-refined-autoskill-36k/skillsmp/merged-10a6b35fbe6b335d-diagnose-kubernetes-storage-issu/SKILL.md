---
name: diagnose-kubernetes-storage-issues
description: Use this skill to diagnose and debug Kubernetes storage issues, including PVC binding failures, volume mount errors, and StorageClass problems.
---

# Diagnose Kubernetes Storage Issues

This skill helps investigate PersistentVolumeClaim (PVC), PersistentVolume (PV), and mount issues in Kubernetes.

## Preconditions

Before applying this skill, verify:

- PVC name or pod name is known
- Namespace is specified
- Storage issue symptoms observed

## Common Storage Issues

| Symptom | Likely Cause | First Check |
|---------|-------------|-------------|
| PVC Pending | No matching PV, StorageClass issue | PVC events |
| Mount failed | PV not available, node issue | Pod events |
| Multi-attach error | RWO volume on multiple nodes | Access mode |
| Permission denied | fsGroup/runAsUser mismatch | Security context |

## Investigation Workflow

### Step 1: Check PVC Status

Check PersistentVolumeClaim binding status.

```yaml
mcp_tool: kubernetes-mcp-server/resources_get
params:
  apiVersion: v1
  kind: PersistentVolumeClaim
  name: $pvc_name
  namespace: $namespace
timeout: 30s
```

**PVC Pending?** Check Events section for reason.

### Step 2: Get PV Details

Check bound PersistentVolume if exists.

```yaml
mcp_tool: kubernetes-mcp-server/resources_list
params:
  apiVersion: v1
  kind: PersistentVolume
timeout: 30s
```

### Step 3: Check Storage Classes

Verify storage class exists and is configured.

```yaml
mcp_tool: kubernetes-mcp-server/resources_list
params:
  apiVersion: storage.k8s.io/v1
  kind: StorageClass
timeout: 30s
```

### Step 4: Get Pod Volume Mounts

Check pod's volume mount status.

```yaml
mcp_tool: kubernetes-mcp-server/pods_get
params:
  name: $pod_name
  namespace: $namespace
timeout: 30s
```

### Step 5: Check Events

Look for storage-related events.

```yaml
mcp_tool: kubernetes-mcp-server/events_list
params:
  namespace: $namespace
timeout: 30s
```

## Success Criteria

The skill succeeds when:

- [ ] PVC status determined (Bound/Pending/Lost)
- [ ] Storage class availability confirmed
- [ ] Root cause identified

## Failure Handling

If storage issue cannot be resolved:

1. Check CSI driver logs
2. Verify node has available storage
3. Escalate with volume details

## Quick Debug Commands

```bash
# Overview of all PVC/PV
kubectl get pvc,pv -A

# Check CSI drivers (if using CSI)
kubectl get csidrivers

# Storage-related events
kubectl get events -A --field-selector reason=FailedMount
kubectl get events -A --field-selector reason=FailedAttachVolume
```

## Specific Issues

### PVC Stuck in Pending

Common reasons:
1. **No matching PV** (static provisioning)
2. **StorageClass can't provision** (dynamic provisioning)
3. **Capacity not available**
4. **Wrong access mode**

```bash
# Check what the PVC is requesting
kubectl get pvc <pvc> -n <ns> -o yaml | grep -A5 "spec:"

# Check events for provisioning errors
kubectl describe pvc <pvc> -n <ns> | grep -A10 "Events:"
```

### Multi-Attach Error

```bash
# Check access mode (RWO = ReadWriteOnce = single node)
kubectl get pvc <pvc> -n <ns> -o jsonpath='{.spec.accessModes}'

# Check which node has the volume
kubectl get pod -n <ns> -o wide
```

### Volume Mount Timeout

```bash
# Check node where pod is scheduled
kubectl get pod <pod> -n <ns> -o jsonpath='{.spec.nodeName}'

# Check node conditions
kubectl describe node <node> | grep -A5 "Conditions:"
```

### Permission Denied on Volume

```bash
# Check pod security context
kubectl get pod <pod> -n <ns> -o jsonpath='{.spec.securityContext}'

# Check container security context
kubectl get pod <pod> -n <ns> -o jsonpath='{.spec.containers[*].securityContext}'
```

Fix with fsGroup or runAsUser in pod spec.

## Access Modes Reference

| Mode | Short | Description |
|------|-------|-------------|
| ReadWriteOnce | RWO | Single node read-write |
| ReadOnlyMany | ROX | Multiple nodes read-only |
| ReadWriteMany | RWX | Multiple nodes read-write |
| ReadWriteOncePod | RWOP | Single pod read-write |

## Notes

- Load `debugging-k8s-pods` if pod has other issues besides storage
- Load `analyzing-k8s-events` for storage event timeline