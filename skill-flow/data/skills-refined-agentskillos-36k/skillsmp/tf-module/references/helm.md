# Helm Deployment Pattern

**When to use:** Deploying Helm charts via Terraform.

## Duplocloud Helm Resources

| Resource | Purpose |
|----------|---------|
| [duplocloud_k8_helm_repository](https://registry.terraform.io/providers/duplocloud/duplocloud/latest/docs/resources/k8_helm_repository) | Register Helm repo |
| [duplocloud_k8_helm_release](https://registry.terraform.io/providers/duplocloud/duplocloud/latest/docs/resources/k8_helm_release) | Deploy chart |

## Basic Pattern

```hcl
resource "duplocloud_k8_helm_repository" "this" {
  tenant_id = local.tenant.id
  name      = local.name
  url       = "https://charts.example.com"
}

resource "duplocloud_k8_helm_release" "this" {
  tenant_id    = local.tenant.id
  name         = local.name
  release_name = local.name
  interval     = "5m0s"
  timeout      = "10m0s"
  
  chart {
    name               = local.name
    version            = var.chart_version
    reconcile_strategy = "ChartVersion"
    source_type        = "HelmRepository"
    source_name        = duplocloud_k8_helm_repository.this.name
  }
  
  values = jsonencode({
    # inline values
  })
  
  depends_on = [duplocloud_k8_helm_repository.this]
}
```

## Values Templating Pattern

Use `templatefile` → `yamldecode` → `jsonencode` chain:

```hcl
values = jsonencode(yamldecode(templatefile("${path.module}/values.yaml", {
  namespace   = local.tenant.namespace
  hostname    = local.hostname
  db_host     = local.db_creds.host
  db_password = local.db_creds.password
  image_tag   = var.image_tag
})))
```

**Why this pattern:**
1. `templatefile` - Resolves Terraform variables (`${var}`)
2. `yamldecode` - Parses YAML, resolves anchors (`&`/`*`)
3. `jsonencode` - Converts back to string for the resource

### values.yaml Template

```yaml
# values.yaml
replicaCount: 1

image:
  repository: myapp
  tag: ${image_tag}

ingress:
  enabled: true
  hosts:
    - host: ${hostname}
      paths:
        - path: /
          pathType: Prefix

env:
  DATABASE_URL: "postgresql://${db_host}:5432/app"
```

## Chart Categories

| Category | Description | Module Location |
|----------|-------------|-----------------|
| **Custom app** | Client's in-house applications | `modules/<app>/` with `tenant = {}` |
| **Third-party tool** | Monitoring, CMS, security agents | `modules/<app>/` with `tenant = {}` |
| **Kubernetes operator** | Extends K8s (cert-manager, external-secrets) | `modules/operators/` |

### Determining Module Location

1. **Is it a Kubernetes operator?** → `modules/operators/`
   - Installs CRDs
   - Examples: cert-manager, external-secrets, istio

2. **Otherwise** → `modules/<app>/` as app module
   - Set `tenant = {}` to deploy to target tenant workspace
   - Determine parent: shared tenant for infra tools, app tenant for apps

## Operators Module Example

```hcl
# modules/operators/cert-manager.tf
resource "duplocloud_k8_helm_repository" "jetstack" {
  tenant_id = local.tenant.id
  name      = "jetstack"
  url       = "https://charts.jetstack.io"
}

resource "duplocloud_k8_helm_release" "cert_manager" {
  tenant_id    = local.tenant.id
  name         = "cert-manager"
  release_name = "cert-manager"
  
  chart {
    name        = "cert-manager"
    version     = "v1.14.0"
    source_type = "HelmRepository"
    source_name = duplocloud_k8_helm_repository.jetstack.name
  }
  
  values = jsonencode({
    installCRDs = true
  })
}
```

## App Module Example

```hcl
# modules/airbyte/main.tf
locals {
  name   = "airbyte"
  tenant = module.ctx.workspaces.tenant
  shared = module.ctx.workspaces.shared
}

module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  workspaces = {
    tenant = {}  # Deploy to workspace-named tenant
    shared = {
      nameRef = {
        workspace = "tenant"
        nameKey   = "shared_name"
      }
      prefix = "infra"
    }
  }
}
```

## Common Helm Repos

| Repo | URL |
|------|-----|
| Bitnami | `https://charts.bitnami.com/bitnami` |
| Jetstack | `https://charts.jetstack.io` |
| Ingress-nginx | `https://kubernetes.github.io/ingress-nginx` |
| Prometheus | `https://prometheus-community.github.io/helm-charts` |

## Tips

- **Version pinning**: Always specify `chart.version`
- **Reconcile strategy**: Use `ChartVersion` for controlled upgrades
- **Timeout**: Increase for large charts (default may be too short)
- **Dependencies**: Use `depends_on` for repo → release ordering
