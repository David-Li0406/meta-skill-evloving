# The Context Module (module.ctx)

**When to use this reference:** When setting up a new module, configuring JIT credentials, or referencing other workspace outputs.

## Overview

The `context` module from `duplocloud/components/duplocloud` is the foundational pattern for all Duplocloud Terraform modules. It provides:

- **Data lookups**: Tenant, infrastructure, and account information
- **JIT credentials**: Just-in-time AWS, GCP, Kubernetes, or Helm credentials
- **Workspace references**: Access outputs from other module workspaces
- **Context data**: Account ID, region, namespace, and more

Source: `duplocloud/components/duplocloud//modules/context`

## Basic Usage

```hcl
module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"  # Check for latest version
  admin   = true
  workspaces = {
    tenant = {}  # Empty = use terraform.workspace as tenant name
  }
}

locals {
  tenant = module.ctx.workspaces.tenant
}
```

## Parameters

### admin (bool)
Whether to use admin-level Duplocloud API access. Required `true` for infrastructure-level operations.

```hcl
admin = true   # Infrastructure, shared, operators modules
admin = false  # App modules with tenant-only access (rare)
```

### tenant (string)
Explicit tenant name for context. Use when not using workspace references.

```hcl
tenant = "default"  # Portal module pattern
```

### jit (object)
Enable Just-In-Time credentials for cloud providers:

```hcl
jit = {
  aws  = true   # AWS STS credentials
  gcp  = true   # GCP service account
  k8s  = true   # Kubernetes cluster credentials
  helm = true   # Helm registry credentials
}
```

### workspaces (map)
Define references to other module workspaces:

```hcl
workspaces = {
  # Simple: workspace name = tenant name
  tenant = {}
  
  # Explicit name
  portal = {
    name = "myportal"
  }
  
  # With state prefix (for S3 backend)
  shared = {
    name   = var.shared
    prefix = "infra"
  }
  
  # Reference another workspace's output for name
  infra = {
    nameRef = {
      workspace = "shared"
      nameKey   = "infra_name"
    }
  }
}
```

## Outputs

### Account & Region
```hcl
module.ctx.account_id   # AWS account ID or GCP project ID
module.ctx.region       # Cloud region
```

### JIT Credentials

**AWS credentials** (when `jit.aws = true`):
```hcl
module.ctx.creds.aws.access_key_id
module.ctx.creds.aws.secret_access_key
module.ctx.creds.aws.session_token
```

**Kubernetes credentials** (when `jit.k8s = true`):
```hcl
module.ctx.creds.k8s.endpoint
module.ctx.creds.k8s.ca_certificate_data
module.ctx.creds.k8s.token
```

### Workspace Data

Each workspace reference provides tenant/infrastructure data:

```hcl
local.tenant = module.ctx.workspaces.tenant

# Tenant data
local.tenant.id           # Tenant UUID
local.tenant.name         # Tenant name
local.tenant.namespace    # Kubernetes namespace
local.tenant.infra_name   # Infrastructure name

# From shared workspace output (if defined)
local.shared.rds_endpoint
local.shared.redis_endpoint
```

## Workspace Reference Patterns

### Pattern 1: Simple Tenant Reference

For app modules where workspace = tenant name:

```hcl
workspaces = {
  tenant = {}  # terraform.workspace is the tenant name
}
```

### Pattern 2: Explicit Portal Reference

For modules that need portal-level data:

```hcl
workspaces = {
  portal = {
    name = "myportal"  # Hardcoded portal workspace name
  }
}
```

### Pattern 3: Variable-Based Reference

For modules where the reference comes from tfvars:

```hcl
# main.tf
workspaces = {
  shared = {
    name   = var.shared
    prefix = "infra"  # State prefix for S3 backend
  }
}

# variables.tf
variable "shared" {
  description = "Shared workspace name"
  type        = string
}

# config/tenant/dev01/tenant.tfvars
shared = "shrd01"
```

### Pattern 4: Chained Reference

For getting workspace name from another workspace's output:

```hcl
workspaces = {
  shared = {
    name   = var.shared
    prefix = "infra"
  }
  infra = {
    nameRef = {
      workspace = "shared"
      nameKey   = "infra_name"  # Output key from shared workspace
    }
  }
}
```

## Provider Configuration Examples

### AWS Provider with JIT

```hcl
module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  jit     = { aws = true }
  workspaces = { tenant = {} }
}

provider "aws" {
  region     = module.ctx.region
  access_key = module.ctx.creds.aws.access_key_id
  secret_key = module.ctx.creds.aws.secret_access_key
  token      = module.ctx.creds.aws.session_token
}
```

### Kubernetes Provider with JIT

```hcl
module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  jit     = { k8s = true }
  workspaces = { tenant = {} }
}

provider "kubernetes" {
  host                   = module.ctx.creds.k8s.endpoint
  cluster_ca_certificate = module.ctx.creds.k8s.ca_certificate_data
  token                  = module.ctx.creds.k8s.token
}
```

### Google Provider

```hcl
module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  workspaces = { tenant = {} }
}

provider "google" {
  project = module.ctx.account_id
  region  = module.ctx.region
}
```

## Version Compatibility

Check the latest version at:
- Terraform Registry: https://registry.terraform.io/modules/duplocloud/components/duplocloud/latest
- GitHub: https://github.com/duplocloud/terraform-duplocloud-components

For additional details, search Duplocloud documentation or use web search for current API details.
