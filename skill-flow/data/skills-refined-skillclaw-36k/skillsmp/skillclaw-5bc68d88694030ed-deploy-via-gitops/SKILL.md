---
name: deploy-via-gitops
description: Use this skill when you need to deploy application changes through a GitOps workflow, ensuring safe and auditable deployments.
---

# Skill body

## Preconditions

Before applying this skill, verify:

- GitOps repository access is configured.
- Flux CD is watching the repository.
- The target namespace exists.
- The image exists in the registry.

## Actions

### 1. Prepare Manifest Changes

Identify files to update:
```yaml
manifest_paths:
  - gitops/apps/{app-name}/deployment.yaml
  - gitops/apps/{app-name}/kustomization.yaml
changes:
  - type: image_tag
    field: spec.template.spec.containers[*].image
    new_value: "{registry}/{image}:{tag}"
  - type: replicas
    field: spec.replicas
    new_value: N
```

### 2. Update Git Repository

Commit changes to the GitOps repository:
```python
# Clone or update repository
repo = git.Repo(gitops_path)
repo.remotes.origin.pull()

# Make changes
update_deployment_image(deployment_path, new_image)

# Commit and push
repo.index.add([deployment_path])
repo.index.commit(f"chore(gitops): Update {app_name} to {tag}")
repo.remotes.origin.push()
```

### 3. Trigger Flux Reconciliation

Force immediate sync:
```bash
flux reconcile kustomization {kustomization-name} --with-source --namespace=flux-system --timeout=5m
```

### 4. Monitor Rollout

Watch deployment progress:
```python
# Wait for rollout
while not deployment_ready:
    status = get_deployment_status(app_name, namespace)
    if status.ready_replicas == status.replicas:
        deployment_ready = True
    elif status.conditions.has_failure:
        raise DeploymentFailed(status.conditions.message)
    await asyncio.sleep(5)
```

### 5. Verify Deployment

Confirm successful deployment:
```yaml
verifications:
  - check: deployment_ready
    resource: deployment/{app-name}
    condition: availableReplicas >= desiredReplicas
  - check: pods_healthy
    selector: app={app-name}
    condition: all pods Running/Ready
  - check: endpoint_responding
    url: http://{service-name}/health
    expected_status: 200
```

### 6. Record Deployment Result

Log deployment outcome:
```yaml
deployment_record:
  app: {app-name}
  status: {status}
  timestamp: {timestamp}
```