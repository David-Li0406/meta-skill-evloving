# ArgoCD Sync Options

## Sync Phases

Execution order: PreSync → Sync → PostSync → SyncFail

```yaml
metadata:
  annotations:
    argocd.argoproj.io/hook: PreSync  # PreSync, Sync, PostSync, SyncFail, Skip
```

## Sync Waves

Control ordering within phases. Lower waves execute first.

```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "-1"  # Negative = before default (0)
```

Execution order:
1. Phase (PreSync → Sync → PostSync)
2. Wave number (lowest to highest)
3. Resource kind
4. Resource name

Default wave delay: 2 seconds (configurable via `ARGOCD_SYNC_WAVE_DELAY`)

### Example: Database Migration Before App

```yaml
# Job: wave -1 (runs first)
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/sync-wave: "-1"
spec:
  template:
    spec:
      containers:
        - name: migrate
          image: myapp:latest
          command: ["./migrate.sh"]
      restartPolicy: Never
---
# Deployment: wave 0 (runs after migration)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "0"
```

## Hook Deletion Policies

```yaml
metadata:
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded  # Or: HookFailed, BeforeHookCreation
```

| Policy | Behavior |
|--------|----------|
| HookSucceeded | Delete after hook succeeds |
| HookFailed | Delete after hook fails |
| BeforeHookCreation | Delete existing before creating new |

## Sync Options (Application Level)

```yaml
spec:
  syncPolicy:
    syncOptions:
      - Validate=false           # Skip kubectl validation
      - CreateNamespace=true     # Auto-create namespace
      - PrunePropagationPolicy=foreground  # foreground, background, orphan
      - PruneLast=true           # Prune after all syncs complete
      - Replace=true             # Use replace instead of apply
      - ServerSideApply=true     # Use server-side apply
      - ApplyOutOfSyncOnly=true  # Only sync changed resources
      - RespectIgnoreDifferences=true
      - FailOnSharedResource=true
```

## Sync Options (Resource Level)

Apply via annotation:

```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-options: Prune=false,Validate=false
```

### Common Resource-Level Options

| Option | Description |
|--------|-------------|
| `Prune=false` | Never delete this resource |
| `Delete=false` | Keep on app deletion |
| `Validate=false` | Skip validation |
| `Replace=true` | Use kubectl replace |
| `ServerSideApply=true` | Server-side apply |

## Automated Sync Policy

```yaml
spec:
  syncPolicy:
    automated:
      prune: true       # Auto-delete removed resources
      selfHeal: true    # Revert manual cluster changes
      allowEmpty: false # Prevent accidental deletion of all resources
```

## Retry Policy

```yaml
spec:
  syncPolicy:
    retry:
      limit: 5          # Max retries (0 = no retry, -1 = unlimited)
      backoff:
        duration: 5s    # Initial delay
        factor: 2       # Multiplier per retry
        maxDuration: 3m # Max delay
```

## Selective Sync

Sync specific resources only:

```bash
# Sync single resource
argocd app sync myapp --resource apps:Deployment:nginx

# Sync by label
argocd app sync myapp --label app=frontend

# Sync with prune
argocd app sync myapp --prune

# Force sync (delete and recreate)
argocd app sync myapp --force
```

## Skip Reconciliation

Pause syncing for a resource:

```yaml
metadata:
  annotations:
    argocd.argoproj.io/compare-options: IgnoreExtraneous
```

Or exclude from app entirely:
```yaml
metadata:
  annotations:
    argocd.argoproj.io/tracking-id: ""  # Remove from tracking
```

## Create Namespace with Metadata

```yaml
spec:
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
    managedNamespaceMetadata:
      labels:
        env: production
      annotations:
        owner: platform-team
```
