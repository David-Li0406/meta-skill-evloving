# Shared Module Patterns

**When to use this reference:** When creating or modifying shared modules that contain stateful resources used across multiple tenants.

## Purpose

The shared module creates stateful resources shared by tenant modules:
- Databases (RDS, Cloud SQL)
- Caches (ElastiCache, Memorystore)
- Message queues
- Shared storage

The shared module itself is a Duplocloud tenant with special settings.

## Directory Structure

```
modules/shared/
├── main.tf           # Context setup, tenant creation
├── providers.tf      # Backend and provider config
├── variables.tf      # Input variables
├── outputs.tf        # Outputs for tenant modules
├── tenant.tf         # Tenant resource with settings
├── rds.tf            # Database resources
└── [resources].tf    # Additional resources

config/shared/<shared-name>/
└── shared.tfvars
```

## Main.tf Template

```hcl
locals {
  tenant_name = terraform.workspace
  portal      = module.ctx.workspaces.portal
  infra       = module.ctx.workspaces.infra
}

module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  jit = {
    aws = true  # For AWS resources like SSM
  }
  workspaces = {
    portal = {
      name = var.portal_name
    }
    infra = {
      name   = var.infra
      prefix = "infra"
    }
  }
}
```

## Tenant Resource

The shared tenant needs special settings to allow cross-tenant access:

```hcl
# tenant.tf
module "tenant" {
  source     = "duplocloud/components/duplocloud//modules/tenant"
  version    = "0.0.41"
  infra_name = var.infra
  
  settings = {
    enable_host_other_tenants = "true"  # Allow other tenants to access
    delete_protection         = "true"  # Prevent accidental deletion
  }
}
```

Or using the raw resource:

```hcl
resource "duplocloud_tenant" "this" {
  account_name = local.tenant_name
  plan_id      = var.infra
  
  setting {
    key   = "enable_host_other_tenants"
    value = "true"
  }
  
  setting {
    key   = "delete_protection"
    value = "true"
  }
}
```

## Providers.tf Template

### AWS Backend

```hcl
terraform {
  required_version = ">= 1.4.4"
  
  backend "s3" {
    key                  = "shared"
    workspace_key_prefix = "infra"  # Same prefix as infrastructure
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
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
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
```

## Database Patterns

### RDS (AWS)

```hcl
# rds.tf
resource "random_password" "db" {
  length  = 24
  special = false
}

resource "duplocloud_rds_instance" "main" {
  tenant_id       = module.tenant.id
  name            = "main"
  engine          = 1  # PostgreSQL
  engine_version  = var.rds.engine_version
  size            = var.rds.instance_class
  encrypt_storage = true
  multi_az        = var.rds.multi_az
  master_username = "postgres"
  master_password = random_password.db.result
  
  # Aurora Serverless v2
  dynamic "v2_scaling_configuration" {
    for_each = var.rds.scaling_configuration != null ? [1] : []
    content {
      min_capacity = var.rds.scaling_configuration.min_capacity
      max_capacity = var.rds.scaling_configuration.max_capacity
    }
  }
}
```

### Cloud SQL (GCP)

```hcl
resource "duplocloud_gcp_sql_database_instance" "main" {
  tenant_id        = module.tenant.id
  name             = "main"
  database_version = "POSTGRES_15"
  tier             = var.db_tier
  
  settings {
    disk_autoresize = true
    
    backup_configuration {
      enabled    = true
      start_time = "03:00"
    }
  }
}
```

## Outputs

```hcl
# outputs.tf
output "tenant_id" {
  description = "Shared tenant ID"
  value       = module.tenant.id
}

output "infra_name" {
  description = "Infrastructure name"
  value       = var.infra
}

output "namespace" {
  description = "Kubernetes namespace"
  value       = module.tenant.namespace
}

# Database outputs
output "rds_endpoint" {
  description = "RDS endpoint"
  value       = duplocloud_rds_instance.main.endpoint
  sensitive   = true
}

output "rds_credentials" {
  description = "RDS credentials"
  value = {
    host     = duplocloud_rds_instance.main.host
    port     = 5432
    username = duplocloud_rds_instance.main.master_username
    password = random_password.db.result
    database = "postgres"
  }
  sensitive = true
}
```

## Variables

```hcl
# variables.tf
variable "portal_name" {
  description = "Portal workspace name"
  type        = string
}

variable "infra" {
  description = "Infrastructure name"
  type        = string
}

variable "rds" {
  description = "RDS configuration"
  type = object({
    engine_version  = string
    instance_class  = optional(string, "db.t3.micro")
    multi_az        = optional(bool, false)
    scaling_configuration = optional(object({
      min_capacity = number
      max_capacity = number
    }))
  })
  default = null
}
```

## Tfvars Example

```hcl
# config/shared/shrd01/shared.tfvars
portal_name = "myportal"
infra       = "nonprod01"

rds = {
  engine_version = "15.4"
  multi_az       = false
  scaling_configuration = {
    min_capacity = 0.5
    max_capacity = 8
  }
}
```

## Key Characteristics

| Aspect | Shared Module |
|--------|--------------|
| Instances | One per infrastructure |
| admin | Always `true` |
| JIT | aws = true (for SSM/secrets) |
| State prefix | `infra` |
| Depends on | Portal, Infrastructure |
| Depended by | Tenant modules |
| Special setting | `enable_host_other_tenants` |

## Referencing Shared from Tenant Modules

```hcl
# In tenant module
module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  workspaces = {
    shared = {
      name   = var.shared  # From tfvars
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

locals {
  shared = module.ctx.workspaces.shared
  # Access shared outputs:
  # local.shared.rds_endpoint
  # local.shared.rds_credentials
}
```

## Multiple Shared Workspaces

For isolation, you might have multiple shared workspaces per infrastructure:

```
config/shared/
├── shrd01/          # Shared for dev tenants
├── shrd-stg01/      # Shared for staging
└── shrd-prod01/     # Shared for production
```

Each tenant's tfvars specifies which shared workspace to use.
