---
name: diagnose-storage-issue
description: Use this skill when diagnosing storage and persistent volume issues in Kubernetes, particularly when pods are stuck pending due to volume problems.
---

# Skill body

## Preconditions

Before applying this skill, verify:

- PVC name or pod name is known
- Namespace is specified
- Storage issue symptoms observed

## Actions

### 1. Get PVC Status

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

### 2. Get PV Details

Check bound PersistentVolume if it exists.

```yaml
mcp_tool: kubernetes-mcp-server/resources_list
params:
  apiVersion: v1
  kind: PersistentVolume
timeout: 30s
```

### 3. Check Storage Classes

Verify that the storage class exists and is configured.

```yaml
mcp_tool: kubernetes-mcp-server/resources_list
params:
  apiVersion: storage.k8s.io/v1
  kind: StorageClass
timeout: 30s
```

### 4. Get Pod Volume Mounts

Check the pod's volume mount status.

```yaml
mcp_tool: kubernetes-mcp-server/pods_get
params:
  name: $pod_name
  namespace: $namespace
timeout: 30s
```

### 5. Check Events

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

If the storage issue cannot be resolved:

1. Check CSI driver logs.
2. Verify that the node has available storage.
3. Escalate with volume details.

## Examples

**Input Context:**
```json
{
  "pvc_name": "data-volume",
  "namespace": "default",
  "pod_name": "db-pod-abc123"
}
```

**Output:**
```json
{
  "pvc_status": "Pending",
  "pv_bound": false,
  "storage_class": "local-path",
  "diagnosis": "No available PV matching storage class requirements",
  "recommendation": "Create PV with matching storage class or use dynamic provisioning"
}
```