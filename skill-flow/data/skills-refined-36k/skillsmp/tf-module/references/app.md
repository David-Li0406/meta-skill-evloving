# App Module Patterns

**When to use this reference:** When creating application-specific modules that deploy to tenant environments (Helm charts, custom apps, operators).

## Purpose

App modules deploy specific applications or components to tenant environments:
- Helm chart deployments (Airbyte, n8n, Kafka)
- Custom application infrastructure
- Kubernetes operators (cert-manager, external-secrets)
- Database extensions or plugins

## Directory Structure

```
modules/<app-name>/
├── main.tf           # Context setup, locals
├── providers.tf      # Backend and provider config
├── variables.tf      # Input variables
├── outputs.tf        # Outputs
├── release.tf        # Helm release resources
└── [resources].tf    # Additional resources

config/<app-name>/<tenant-name>/
└── <app-name>.tfvars
```

## Main.tf Template

```hcl
locals {
  name   = "<app-name>"
  tenant = module.ctx.workspaces.tenant
  shared = local.tenant.shared  # From tenant outputs
  portal = local.tenant.portal
}

module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  workspaces = {
    tenant = {}  # Empty = terraform.workspace is the tenant name
  }
}
```

### With Additional Workspace References

```hcl
module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  jit = {
    k8s = true  # For Helm/Kubernetes access
  }
  workspaces = {
    tenant = {}
    shared = {
      nameRef = {
        workspace = "tenant"
        nameKey   = "shared_name"
      }
      prefix = "infra"
    }
  }
}

locals {
  tenant = module.ctx.workspaces.tenant
  shared = module.ctx.workspaces.shared
}
```

## Providers.tf Template

### AWS Backend

```hcl
terraform {
  required_version = ">= 1.4.4"
  
  backend "s3" {
    key                  = "<app-name>"
    workspace_key_prefix = "<app-name>"
    encrypt              = true
  }
  
  required_providers {
    duplocloud = {
      source  = "duplocloud/duplocloud"
      version = ">= 0.11.0"
    }
  }
}

provider "duplocloud" {}
```

### GCP Backend

```hcl
terraform {
  required_version = ">= 1.4.4"
  
  backend "gcs" {
    prefix = "<app-name>"
  }
  
  required_providers {
    duplocloud = {
      source  = "duplocloud/duplocloud"
      version = ">= 0.11.0"
    }
    google = {
      source  = "hashicorp/google"
      version = ">= 6.0"
    }
  }
}

provider "duplocloud" {}

provider "google" {
  project = module.ctx.account_id
  region  = module.ctx.region
}
```

## Helm Deployment Pattern

### Repository and Release

```hcl
# release.tf
resource "duplocloud_k8_helm_repository" "this" {
  tenant_id = local.tenant.id
  name      = local.name
  url       = var.helm_repo_url
}

resource "duplocloud_k8_helm_release" "this" {
  tenant_id    = local.tenant.id
  name         = local.name
  release_name = local.name
  interval     = "5m0s"
  timeout      = "10m0s"
  
  chart {
    name               = var.chart_name
    version            = var.chart_version
    reconcile_strategy = "ChartVersion"
    source_type        = "HelmRepository"
    source_name        = duplocloud_k8_helm_repository.this.name
  }
  
  values = jsonencode(yamldecode(templatefile("${path.module}/values.yaml", {
    namespace   = local.tenant.namespace
    hostname    = local.hostname
    db_host     = local.shared.rds_endpoint
    # ... other template variables
  })))
  
  depends_on = [duplocloud_k8_helm_repository.this]
}
```

### Values Template

```yaml
# values.yaml (in module directory)
replicaCount: 1

image:
  repository: myapp
  tag: ${image_tag}

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: ${hostname}
      paths:
        - path: /
          pathType: Prefix

env:
  DATABASE_URL: "postgresql://${db_host}:5432/app"
  REDIS_URL: "redis://${redis_host}:6379"
```

## Variables

```hcl
# variables.tf
variable "helm_repo_url" {
  description = "Helm repository URL"
  type        = string
  default     = "https://charts.example.com"
}

variable "chart_name" {
  description = "Helm chart name"
  type        = string
  default     = "myapp"
}

variable "chart_version" {
  description = "Helm chart version"
  type        = string
}

variable "image_tag" {
  description = "Container image tag"
  type        = string
  default     = "latest"
}
```

## Outputs

```hcl
# outputs.tf
output "release_name" {
  description = "Helm release name"
  value       = duplocloud_k8_helm_release.this.release_name
}

output "namespace" {
  description = "Kubernetes namespace"
  value       = local.tenant.namespace
}

output "hostname" {
  description = "Application hostname"
  value       = local.hostname
}
```

## Tfvars Example

```hcl
# config/myapp/dev01/myapp.tfvars
chart_version = "1.2.3"
image_tag     = "v1.0.0"
```

## Common App Patterns

### Hostname Generation

```hcl
locals {
  # Pattern: app.tenant.domain
  hostname = "${local.name}.${terraform.workspace}.${var.domain}"
  
  # Or from tenant outputs
  hostname = "${local.name}.${local.tenant.domain}"
}
```

### Database Connection from Shared

```hcl
locals {
  # Decode credentials from shared tenant secret
  db_creds = jsondecode(data.duplocloud_tenant_secret.db.secret_data)
}

data "duplocloud_tenant_secret" "db" {
  tenant_id   = local.shared.tenant_id
  secret_name = "rds-credentials"
}

# Use in Helm values
values = jsonencode({
  database = {
    host     = local.db_creds.host
    port     = local.db_creds.port
    username = local.db_creds.username
    password = local.db_creds.password
  }
})
```

### PostgreSQL Provider for App Database

```hcl
provider "postgresql" {
  host     = local.shared.rds_endpoint
  port     = 5432
  username = local.db_creds.username
  password = local.db_creds.password
  sslmode  = "require"
}

resource "postgresql_database" "app" {
  name  = local.name
  owner = local.db_creds.username
}
```

## Operators Module (Special App Type)

Operators deploy cluster-wide CRDs. They run in their own tenant.

```hcl
# modules/operators/main.tf
locals {
  tenant = module.ctx.workspaces.operators
}

module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  jit = {
    k8s = true
  }
  workspaces = {
    operators = {}  # Workspace = operators tenant name
  }
}

# Cert-manager example
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

## Key Characteristics

| Aspect | App Module |
|--------|-----------|
| Instances | Per-tenant deployment |
| admin | `true` |
| JIT | k8s = true (usually) |
| State prefix | `<app-name>` |
| Workspace reference | `tenant = {}` |
| Depends on | Tenant, Shared |

## Creating a New App Module

1. Create `modules/<app>/` directory
2. Add `main.tf` with context using `tenant = {}`
3. Add `providers.tf` with backend prefix matching app name
4. Add `release.tf` for Helm deployments
5. Add `values.yaml` template if needed
6. Create `config/<app>/<tenant>/` for each deployment
7. Create `.github/workflows/<app>.yml`
