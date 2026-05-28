---
name: investigate-dns-config
description: Use this skill when investigating DNSConfigForming warnings on pods, analyzing DNS policy configuration, host network settings, and nameserver limits.
---

# Skill body

## Preconditions

Before applying this skill, verify:

- The event shows a DNSConfigForming reason.
- The pod name and namespace are known from the event.
- The pod may have been recreated (check for similar pods).

## Actions

### 1. Get Related Events

Gather all DNS-related events in the namespace for context.

```yaml
mcp_tool: kubernetes-mcp-server/events_list
params:
  namespace: $namespace
timeout: 30s
```

**Analysis**: Look for DNSConfigForming events, noting affected pods and messages.

### 2. List Affected Pods

Find pods managed by the same controller (may have been recreated).

```yaml
mcp_tool: kubernetes-mcp-server/pods_list_in_namespace
params:
  namespace: $namespace
  labelSelector: $label_selector
timeout: 30s
```

**Analysis**: Identify running pods that may be affected.

### 3. Get Controller Configuration

Get the DaemonSet/Deployment/StatefulSet that manages the pod.

```yaml
mcp_tool: kubernetes-mcp-server/resources_get
params:
  apiVersion: apps/v1
  kind: $controller_kind
  name: $controller_name
  namespace: $namespace
timeout: 30s
```

**Analysis**: Check for:
- `hostNetwork: true` - Pod uses host networking.
- `dnsPolicy` - Current DNS policy setting.

### 4. Determine Root Cause

Based on findings, identify the root cause:

| Condition | Root Cause | Recommendation |
|-----------|------------|----------------|
| `hostNetwork: true` + `dnsPolicy: ClusterFirst` | Nameserver limit exceeded when combining cluster DNS with host DNS | Change to `dnsPolicy: ClusterFirstWithHostNet` |
| `hostNetwork: true` + no explicit dnsPolicy | Same as above (ClusterFirst is default) | Set `dnsPolicy: ClusterFirstWithHostNet` |
| `hostNetwork: false` + DNSConfigForming | Node has >3 nameservers | Usually benign; first 3 nameservers are used. |

## Success Criteria

The skill succeeds when:

- [ ] Root cause of DNSConfigForming identified.
- [ ] Controller configuration analyzed.
- [ ] Remediation recommendation provided.

## Failure Handling

If investigation fails, document findings and escalate as necessary.