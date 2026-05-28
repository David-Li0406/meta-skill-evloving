---
name: check-flux-status
description: Use this skill to verify the sync status of Flux CD GitOps components, including Kustomizations, HelmReleases, and GitRepositories, for deployment verification and troubleshooting.
---

# Skill body

## Preconditions

Before applying this skill, verify:

- Flux CD is installed in the cluster.
- You have access to the `flux-system` namespace.
- Kubernetes API access is available.

## Actions

### 1. Check Kustomizations

List and verify all Kustomizations:
```yaml
command: kubectl get kustomizations -A -o wide
resources:
  - apiVersion: kustomize.toolkit.fluxcd.io/v1
    kind: Kustomization
expected_conditions:
  - type: Ready
    status: "True"
  - type: Healthy (optional)
    status: "True"
```

### 2. Check HelmReleases

Verify all Helm releases are synced:
```yaml
command: kubectl get helmreleases -A -o wide
resources:
  - apiVersion: helm.toolkit.fluxcd.io/v2
    kind: HelmRelease
expected_conditions:
  - type: Ready
    status: "True"
  - type: Released
    status: "True"
```

### 3. Check GitRepositories

Verify source repositories are fetched:
```yaml
command: kubectl get gitrepositories -A -o wide
resources:
  - apiVersion: source.toolkit.fluxcd.io/v1
    kind: GitRepository
expected_conditions:
  - type: Ready
    status: "True"
check_fields:
  - lastAppliedRevision
  - lastAttemptedRevision
```

### 4. Check HelmRepositories

Verify Helm chart sources:
```yaml
command: kubectl get helmrepositories -A -o wide
resources:
  - apiVersion: source.toolkit.fluxcd.io/v1beta2
    kind: HelmRepository
expected_conditions:
  - type: Ready
    status: "True"
```

### 5. Identify Issues

Collect resources that are not ready:
```python
issues = []
for resource in all_flux_resources:
    ready_condition = get_condition(resource, "Ready")
    if ready_condition.status != "True":
        issues.append({
            "resource": f"{resource.kind}/{resource.name}",
            "namespace": resource.namespace,
            "status": ready_condition.status,
            "message": ready_condition.message,
            "reason": ready_condition.reason
        })
```

### 6. Generate Status Summary

Create a summary report:
```yaml
status:
  overall: healthy|degraded|unhealthy
  components:
    kustomizations:
      total: N
      ready: M
    helmReleases:
      total: P
      ready: Q
    gitRepositories:
      total: R
      ready: S
    helmRepositories:
      total: T
      ready: U
```