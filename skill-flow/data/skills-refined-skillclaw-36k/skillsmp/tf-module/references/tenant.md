# Tenant Module Patterns

**When to use this reference:** When creating or modifying tenant modules for application environments (dev, staging, production).

## Purpose

The tenant module creates application environments:
- Development tenants (dev01, dev02)
- Staging tenants (stg01)
- Production tenants (prod01)
- Feature/preview tenants

Each tenant is an isolated namespace with its own resources and permissions.

## Directory Structure

```
modules/tenant/
├── main.tf           # Context setup, locals
├── providers.tf      # Backend and provider config
├── variables.tf      # Input variables
├── outputs.tf        # Outputs for app modules
├── tenant.tf         # Tenant resource
└── [resources].tf    # Additional resources

config/tenant/<tenant-name>/
└── tenant.tfvars
```

## Main.tf Template

```hcl
locals {
  portal_name = var.portal_name
  portal      = module.ctx.workspaces.portal
  devops      = module.ctx.workspaces.devops
  shared      = module.ctx.workspaces.shared
  infra       = module.ctx.workspaces.infra
}

module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  jit = {
    aws = true
    k8s = true  # For kubernetes resources
  }
  workspaces = {
    portal = {
      name = local.portal_name
    }
    devops = {
      name   = local.portal_name
      prefix = "portal"
    }
    shared = {
      name   = var.shared
      prefix = "infra"
    }
    infra = {
      nameRef = {
        workspace = "shared"
        nameKey   = "infra_name"
      }
    }
  }
}
```

## Tenant Resource

```hcl
# tenant.tf
module "tenant" {
  source     = "duplocloud/components/duplocloud//modules/tenant"
  version    = "0.0.41"
  infra_name = local.shared.infra_name
}
```

Or with additional settings:

```hcl
module "tenant" {
  source     = "duplocloud/components/duplocloud//modules/tenant"
  version    = "0.0.41"
  infra_name = local.shared.infra_name
  
  settings = {
    delete_protection = var.environment == "prod" ? "true" : "false"
  }
}
```

## Providers.tf Template

### AWS Backend

```hcl
terraform {
  required_version = ">= 1.4.4"
  
  backend "s3" {
    key                  = "tenant"
    workspace_key_prefix = "tenant"
    encrypt              = true
  }
  
  required_providers {
    duplocloud = {
      source  = "duplocloud/duplocloud"
      version = ">= 0.11.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0"
    }
    github = {
      source  = "integrations/github"
      version = ">= 6.0"
    }
  }
}

provider "duplocloud" {}

provider "aws" {
  region     = local.infra.region
  access_key = module.ctx.creds.aws.access_key_id
  secret_key = module.ctx.creds.aws.secret_access_key
  token      = module.ctx.creds.aws.session_token
}

provider "kubernetes" {
  host                   = module.ctx.creds.k8s.endpoint
  cluster_ca_certificate = module.ctx.creds.k8s.ca_certificate_data
  token                  = module.ctx.creds.k8s.token
}
```

### GitHub Provider with App Auth

```hcl
data "aws_ssm_parameter" "github_app_id" {
  name = "/github/app_id"
}

data "aws_ssm_parameter" "github_private_key" {
  name            = "/github/private_key"
  with_decryption = true
}

provider "github" {
  owner = var.github_org
  app_auth {
    id              = data.aws_ssm_parameter.github_app_id.value
    installation_id = var.github_installation_id
    pem_file        = data.aws_ssm_parameter.github_private_key.value
  }
}
```

## Variables

```hcl
# variables.tf
variable "portal_name" {
  description = "Portal workspace name"
  type        = string
  default     = "myportal"
}

variable "shared" {
  description = "Shared workspace name"
  type        = string
}

variable "environment" {
  description = "Environment type"
  type        = string
  default     = "dev"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Must be dev, staging, or prod"
  }
}

variable "github_org" {
  description = "GitHub organization"
  type        = string
  default     = ""
}

variable "github_installation_id" {
  description = "GitHub App installation ID"
  type        = string
  default     = ""
}
```

## Outputs

```hcl
# outputs.tf
output "tenant_id" {
  description = "Tenant ID"
  value       = module.tenant.id
}

output "name" {
  description = "Tenant name"
  value       = module.tenant.name
}

output "namespace" {
  description = "Kubernetes namespace"
  value       = module.tenant.namespace
}

output "infra_name" {
  description = "Infrastructure name"
  value       = local.shared.infra_name
}

output "shared_name" {
  description = "Shared workspace name"
  value       = var.shared
}

output "portal_name" {
  description = "Portal workspace name"
  value       = local.portal_name
}

# Pass through shared resources
output "rds_endpoint" {
  description = "Database endpoint from shared"
  value       = local.shared.rds_endpoint
  sensitive   = true
}
```

## Tfvars Examples

### Development

```hcl
# config/tenant/dev01/tenant.tfvars
shared      = "shrd01"
environment = "dev"
```

### Staging

```hcl
# config/tenant/stg01/tenant.tfvars
shared      = "shrd-stg01"
environment = "staging"
```

### Production

```hcl
# config/tenant/prod01/tenant.tfvars
shared      = "shrd-prod01"
environment = "prod"
```

## Common Tenant Resources

### Kubernetes ConfigMaps

```hcl
resource "kubernetes_config_map" "env" {
  metadata {
    name      = "environment"
    namespace = module.tenant.namespace
  }
  
  data = {
    ENVIRONMENT  = var.environment
    DATABASE_URL = "postgresql://${local.shared.rds_endpoint}:5432/app"
  }
}
```

### GitHub Environment

```hcl
resource "github_repository_environment" "this" {
  count       = var.github_org != "" ? 1 : 0
  environment = terraform.workspace
  repository  = var.repository_name
  
  deployment_branch_policy {
    protected_branches     = var.environment == "prod"
    custom_branch_policies = var.environment != "prod"
  }
}
```

## Key Characteristics

| Aspect | Tenant Module |
|--------|--------------|
| Instances | Multiple per infrastructure |
| admin | `true` |
| JIT | aws = true, k8s = true |
| State prefix | `tenant` |
| Depends on | Portal, Infrastructure, Shared |
| Depended by | App modules |

## Referencing Tenant from App Modules

```hcl
# In app module
module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  workspaces = {
    tenant = {}  # Empty = terraform.workspace is tenant name
  }
}

locals {
  tenant = module.ctx.workspaces.tenant
  # Access tenant outputs:
  # local.tenant.id
  # local.tenant.namespace
  # local.tenant.rds_endpoint
}
```

## Workspace Naming Conventions

| Environment | Pattern | Examples |
|-------------|---------|----------|
| Development | `dev##` | dev01, dev02, dev03 |
| Staging | `stg##` | stg01 |
| Production | `prod##` | prod01 |
| Preview | `pr-###` | pr-123, pr-456 |
| Feature | `feat-*` | feat-auth, feat-api |
