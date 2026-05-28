# Infrastructure Module Patterns

**When to use this reference:** When creating or modifying infrastructure modules that define VPCs and Kubernetes clusters.

## Purpose

The infrastructure module creates the network and compute foundation:
- VPC/VNet with subnets
- Kubernetes cluster (EKS/GKE/AKS)
- Security groups and network policies
- Infrastructure-level settings

## Directory Structure

```
modules/infrastructure/
├── main.tf           # Context setup, locals
├── providers.tf      # Backend and provider config  
├── variables.tf      # Input variables
├── outputs.tf        # Outputs for dependent modules
├── infra.tf          # Infrastructure resource
└── [resources].tf    # Additional resources

config/infrastructure/<infra-name>/
└── infrastructure.tfvars
```

## Main.tf Template

```hcl
locals {
  name   = terraform.workspace
  portal = module.ctx.workspaces.portal
}

module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  workspaces = {
    portal = {
      name = var.portal_name
    }
  }
}
```

## Providers.tf Template

### AWS Backend

```hcl
terraform {
  required_version = ">= 1.4.4"
  
  backend "s3" {
    key                  = "infrastructure"
    workspace_key_prefix = "infra"
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
    prefix = "infrastructure"
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

## Infrastructure Resource

### AWS (EKS)

```hcl
# infra.tf
resource "duplocloud_infrastructure" "this" {
  infra_name        = terraform.workspace
  cloud             = 0  # AWS
  region            = var.region
  azcount           = var.az_count
  enable_k8_cluster = true
  address_prefix    = var.address_prefix
  subnet_cidr       = var.subnet_cidr
}
```

### GCP (GKE)

```hcl
resource "duplocloud_infrastructure" "this" {
  infra_name        = terraform.workspace
  cloud             = 2  # GCP
  region            = var.region
  enable_k8_cluster = true
  address_prefix    = var.address_prefix
  subnet_cidr       = var.subnet_cidr
}
```

### Azure (AKS)

```hcl
resource "duplocloud_infrastructure" "this" {
  infra_name        = terraform.workspace
  cloud             = 1  # Azure
  region            = var.region
  enable_k8_cluster = true
  address_prefix    = var.address_prefix
  subnet_cidr       = var.subnet_cidr
}
```

## Variables

```hcl
# variables.tf
variable "portal_name" {
  description = "Portal workspace name"
  type        = string
}

variable "region" {
  description = "Cloud region"
  type        = string
}

variable "az_count" {
  description = "Number of availability zones"
  type        = number
  default     = 2
}

variable "address_prefix" {
  description = "VPC CIDR prefix (e.g., 10.100)"
  type        = string
}

variable "subnet_cidr" {
  description = "Subnet CIDR bits"
  type        = number
  default     = 24
}
```

## Outputs

```hcl
# outputs.tf
output "name" {
  description = "Infrastructure name"
  value       = duplocloud_infrastructure.this.infra_name
}

output "region" {
  description = "Cloud region"
  value       = var.region
}

output "vpc_id" {
  description = "VPC/VNet ID"
  value       = duplocloud_infrastructure.this.vpc_id
}

output "account_id" {
  description = "Cloud account ID"
  value       = module.ctx.account_id
}
```

## Tfvars Examples

### Non-Production

```hcl
# config/infrastructure/nonprod01/infrastructure.tfvars
portal_name    = "myportal"
region         = "us-west-2"
az_count       = 2
address_prefix = "10.100"
subnet_cidr    = 24
```

### Production

```hcl
# config/infrastructure/prod01/infrastructure.tfvars
portal_name    = "myportal"
region         = "us-west-2"
az_count       = 3
address_prefix = "10.200"
subnet_cidr    = 22
```

## Common Patterns

### Multiple Infrastructures

Typical setup has separate infrastructures for environments:

```
config/infrastructure/
├── nonprod01/    # Dev/staging workloads
│   └── infrastructure.tfvars
└── prod01/       # Production workloads
    └── infrastructure.tfvars
```

### EKS Node Groups

Add node groups after infrastructure is created:

```hcl
# nodes.tf
module "eks_nodes" {
  source  = "duplocloud/components/duplocloud//modules/eks-nodes"
  version = "0.0.41"
  
  infra_name = duplocloud_infrastructure.this.infra_name
  
  node_groups = {
    default = {
      capacity_type  = "ON_DEMAND"
      instance_types = ["t3.medium"]
      min_size       = 2
      max_size       = 10
      desired_size   = 2
    }
  }
  
  depends_on = [duplocloud_infrastructure.this]
}
```

## Key Characteristics

| Aspect | Infrastructure Module |
|--------|----------------------|
| Instances | One per environment cluster |
| admin | Always `true` |
| JIT | Rarely needed |
| State prefix | `infra` |
| Depends on | Portal |
| Depended by | Shared, Operators, Tenant |

## Referencing Infrastructure from Other Modules

```hcl
# In shared/tenant modules
module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  workspaces = {
    infra = {
      name   = var.infra_name
      prefix = "infra"  # Matches infrastructure's workspace_key_prefix
    }
  }
}

locals {
  infra = module.ctx.workspaces.infra
  # Access infrastructure outputs:
  # local.infra.name
  # local.infra.region
  # local.infra.vpc_id
}
```
