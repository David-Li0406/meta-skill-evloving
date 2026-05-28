# ArgoCD Operations & Administration

## AppProjects

Logical grouping with access controls.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: myproject
  namespace: argocd
spec:
  description: My project

  # Allowed source repos
  sourceRepos:
    - https://github.com/org/*
    - '!https://github.com/org/denied-repo'  # Deny pattern

  # Allowed destinations
  destinations:
    - namespace: 'myapp-*'
      server: https://kubernetes.default.svc
    - namespace: '*'
      server: https://production.example.com

  # Allowed cluster resources (cluster-scoped require explicit allow)
  clusterResourceWhitelist:
    - group: ''
      kind: Namespace
    - group: rbac.authorization.k8s.io
      kind: ClusterRole

  # Denied namespaced resources
  namespaceResourceBlacklist:
    - group: ''
      kind: Secret

  # Orphaned resource monitoring
  orphanedResources:
    warn: true

  # Project roles
  roles:
    - name: developer
      description: Developer access
      policies:
        - p, proj:myproject:developer, applications, get, myproject/*, allow
        - p, proj:myproject:developer, applications, sync, myproject/*, allow
      groups:
        - my-oidc-group
```

### CLI Commands

```bash
argocd proj create myproject \
  -d https://kubernetes.default.svc,myapp \
  -s https://github.com/org/repo.git

argocd proj add-destination myproject https://kubernetes.default.svc '*'
argocd proj add-source myproject https://github.com/org/*
argocd proj list
```

## RBAC

Configure in `argocd-rbac-cm` ConfigMap.

### Policy Syntax

```
p, <subject>, <resource>, <action>, <object>, <effect>
g, <user/group>, <role>
```

### Built-in Roles

- `role:readonly` - Read-only access
- `role:admin` - Full access

### Example Configuration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
data:
  policy.default: role:readonly
  policy.csv: |
    # Admins
    g, admin-group, role:admin

    # Developers - specific project access
    p, role:developer, applications, get, */*, allow
    p, role:developer, applications, sync, myproject/*, allow
    p, role:developer, applications, create, myproject/*, allow
    g, dev-group, role:developer

    # Read-only for specific app
    p, viewer@example.com, applications, get, default/myapp, allow

  # Match mode: glob (default) or regex
  policy.matchMode: glob
```

### Resources and Actions

| Resource | Actions |
|----------|---------|
| applications | get, create, update, delete, sync, override, action/* |
| applicationsets | get, create, update, delete |
| clusters | get, create, update, delete |
| projects | get, create, update, delete |
| repositories | get, create, update, delete |
| logs | get |
| exec | create |

### Validate RBAC

```bash
argocd admin settings rbac validate --policy-file policy.csv
argocd admin settings rbac can developer get applications 'default/*'
```

## Health Checks

### Built-in Health Status

| Status | Meaning |
|--------|---------|
| Healthy | Resource functioning properly |
| Progressing | Working toward healthy state |
| Degraded | Resource has problems |
| Suspended | Awaiting external event |
| Missing | Resource not found |
| Unknown | Health not determined |

### Custom Health Check (Lua)

```yaml
# argocd-cm ConfigMap
data:
  resource.customizations.health.mycrd.example.com_MyResource: |
    hs = {}
    if obj.status ~= nil then
      if obj.status.phase == "Running" then
        hs.status = "Healthy"
        hs.message = "Resource is running"
      elseif obj.status.phase == "Pending" then
        hs.status = "Progressing"
        hs.message = "Resource is starting"
      else
        hs.status = "Degraded"
        hs.message = obj.status.message or "Unknown issue"
      end
    end
    return hs
```

### Ignore Health Check

```yaml
metadata:
  annotations:
    argocd.argoproj.io/ignore-healthcheck: "true"
```

## Notifications

### Setup

```yaml
# argocd-notifications-cm ConfigMap
data:
  service.slack: |
    token: $slack-token

  trigger.on-sync-succeeded: |
    - when: app.status.sync.status == 'Synced'
      send: [app-sync-succeeded]

  template.app-sync-succeeded: |
    message: |
      Application {{.app.metadata.name}} synced successfully.
      Revision: {{.app.status.sync.revision}}
```

### Subscribe Application

```yaml
metadata:
  annotations:
    notifications.argoproj.io/subscribe.on-sync-succeeded.slack: my-channel
```

### Common Triggers

- `on-sync-succeeded`
- `on-sync-failed`
- `on-sync-status-unknown`
- `on-health-degraded`
- `on-deployed`

### Supported Services

Slack, Teams, Email, PagerDuty, Webhook, Telegram, Opsgenie, Grafana, Mattermost, Rocket.Chat, Google Chat, AWS SQS, GitHub

## Cluster Management

```bash
# Add cluster (uses current kubeconfig context)
argocd cluster add my-context --name production

# List clusters
argocd cluster list

# Remove cluster
argocd cluster rm https://production.example.com
```

### Cluster Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-cluster
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: cluster
type: Opaque
stringData:
  name: production
  server: https://production.example.com
  config: |
    {
      "bearerToken": "...",
      "tlsClientConfig": {
        "insecure": false,
        "caData": "..."
      }
    }
```
