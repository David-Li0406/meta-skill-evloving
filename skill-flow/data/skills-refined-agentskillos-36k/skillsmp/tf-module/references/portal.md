# Portal Module Patterns

**When to use this reference:** When creating or modifying the portal module - the top-level module that runs once per Duplocloud instance.

## Purpose

The portal module manages resources that exist at the Duplocloud portal level:
- Global certificates
- GitHub App credentials storage
- Portal-wide settings
- Cross-infrastructure resources

## Directory Structure

```
modules/portal/
├── main.tf           # Context setup, locals
├── providers.tf      # Backend and provider config
├── variables.tf      # Input variables
├── outputs.tf        # Outputs for other modules
└── [resources].tf    # Additional resource files

config/portal/<portal-name>/
└── portal.tfvars     # Portal instance configuration
```

## Main.tf Template

```hcl
locals {
  name = terraform.workspace
}

module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  tenant  = "default"  # Portal uses default tenant
}
```

## Providers.tf Template

### AWS Backend

```hcl
terraform {
  required_version = ">= 1.4.4"
  
  backend "s3" {
    key                  = "portal"
    workspace_key_prefix = "portal"
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
    prefix = "portal"
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

## Common Portal Resources

### GitHub App Credentials (AWS)

Store GitHub App credentials in SSM for use by other modules:

```hcl
variable "github_app_id" {
  description = "GitHub App ID"
  type        = string
  sensitive   = true
}

variable "github_private_key" {
  description = "GitHub App private key (PEM)"
  type        = string
  sensitive   = true
}

resource "aws_ssm_parameter" "github_app_id" {
  name  = "/github/app_id"
  type  = "String"
  value = var.github_app_id
}

resource "aws_ssm_parameter" "github_private_key" {
  name  = "/github/private_key"
  type  = "SecureString"
  value = var.github_private_key
}
```

### GitHub App Credentials (GCP)

```hcl
resource "google_secret_manager_secret" "github_app_id" {
  project   = module.ctx.account_id
  secret_id = "github-app-id"
  
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "github_app_id" {
  secret      = google_secret_manager_secret.github_app_id.id
  secret_data = var.github_app_id
}
```

### Wildcard Certificate

```hcl
resource "duplocloud_plan_certificates" "wildcard" {
  plan_id           = "default"
  certificate_name  = "wildcard"
  certificate_arn   = var.certificate_arn
}
```

## Outputs

```hcl
output "name" {
  description = "Portal workspace name"
  value       = local.name
}

output "account_id" {
  description = "Cloud account ID"
  value       = module.ctx.account_id
}

output "region" {
  description = "Default region"
  value       = module.ctx.region
}
```

## Tfvars Example

```hcl
# config/portal/myportal/portal.tfvars

github_app_id      = "123456"
github_private_key = <<-EOT
-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----
EOT

certificate_arn = "arn:aws:acm:us-west-2:123456789012:certificate/abc123"
```

## Workspace Naming

Portal workspaces are typically named after the Duplocloud instance:
- `mycompany` - Production portal
- `mycompany-dev` - Development portal

```bash
tf ctx mycompany
tf apply -chdir=modules/portal
```

## Referencing Portal from Other Modules

Other modules reference the portal workspace:

```hcl
# In tenant/shared/infrastructure modules
module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  workspaces = {
    portal = {
      name = "myportal"  # Or var.portal_name
    }
  }
}

locals {
  portal = module.ctx.workspaces.portal
  # Access portal outputs:
  # local.portal.account_id
  # local.portal.region
}
```

## Key Characteristics

| Aspect | Portal Module |
|--------|---------------|
| Instances | One per Duplocloud portal |
| admin | Always `true` |
| tenant | `"default"` |
| JIT | Rarely needed |
| State prefix | `portal` |
| Depends on | Nothing (root of hierarchy) |
