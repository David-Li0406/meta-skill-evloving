# AWS-Specific Patterns

**When to use this reference:** When creating modules for AWS-based Duplocloud infrastructure.

## Backend Configuration

AWS uses S3 backend with DynamoDB locking:

```hcl
terraform {
  backend "s3" {
    # Static config in providers.tf
    key                  = "mymodule"        # State file key
    workspace_key_prefix = "tenant"          # Organizes by workspace type
    encrypt              = true              # Always encrypt state
    
    # Dynamic config via tf init (or CI/CD)
    # bucket         = "duplo-tfstate-<account-id>"
    # region         = "us-west-2"
    # dynamodb_table = "duplo-tfstate-<account-id>-lock"
  }
}
```

### State File Organization

The S3 state path follows this pattern:
```
s3://duplo-tfstate-<account>/
├── portal/<portal-name>/portal
├── infra/<infra-name>/infrastructure  
├── infra/<shared-name>/shared
├── tenant/<tenant-name>/tenant
└── <app>/<tenant-name>/<app>
```

### workspace_key_prefix vs key

- `workspace_key_prefix`: Directory in S3 (varies by module type)
- `key`: State file name (usually matches module name)

| Module Type | workspace_key_prefix | key |
|-------------|---------------------|-----|
| portal | `portal` | `portal` |
| infrastructure | `infra` | `infrastructure` |
| shared | `infra` | `shared` |
| tenant | `tenant` | `tenant` |
| app | `<app>` | `<app>` |

## AWS Provider with JIT Credentials

```hcl
module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  jit = {
    aws = true
  }
  workspaces = {
    tenant = {}
  }
}

provider "aws" {
  region     = module.ctx.region
  access_key = module.ctx.creds.aws.access_key_id
  secret_key = module.ctx.creds.aws.secret_access_key
  token      = module.ctx.creds.aws.session_token
}
```

### Alternative: Use Local AWS Profile

For local development without JIT:

```hcl
provider "aws" {
  region  = var.region
  profile = var.aws_profile  # From ~/.aws/credentials
}
```

## Common AWS Resources

### RDS Instance

```hcl
resource "duplocloud_rds_instance" "main" {
  tenant_id           = local.tenant.id
  name                = "main"
  engine              = 1  # PostgreSQL
  engine_version      = "15.4"
  size                = "db.t3.micro"
  encrypt_storage     = true
  master_username     = "postgres"
  master_password     = random_password.db.result
  multi_az            = var.multi_az
  
  # Aurora Serverless v2
  v2_scaling_configuration {
    min_capacity = 0.5
    max_capacity = 8
  }
}

resource "random_password" "db" {
  length  = 24
  special = false
}
```

### ElastiCache (Redis)

```hcl
resource "duplocloud_ecache_instance" "redis" {
  tenant_id       = local.tenant.id
  name            = "redis"
  cache_type      = 0  # Redis
  size            = "cache.t3.micro"
  replicas        = var.redis_replicas
  enable_cluster  = false
}
```

### SSM Parameter Store

For GitHub credentials and secrets:

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

### EKS Node Groups

```hcl
module "eks_nodes" {
  source  = "duplocloud/components/duplocloud//modules/eks-nodes"
  version = "0.0.41"
  
  infra_name = local.infra.name
  
  node_groups = {
    default = {
      capacity_type  = "ON_DEMAND"
      instance_types = ["t3.medium"]
      min_size       = 1
      max_size       = 5
      desired_size   = 2
    }
    spot = {
      capacity_type  = "SPOT"
      instance_types = ["t3.medium", "t3.large"]
      min_size       = 0
      max_size       = 10
      desired_size   = 0
    }
  }
}
```

## S3 Backend Auto-Configuration

The `tf init` wrapper auto-configures:

```bash
# Discovers from duploctl system info:
DUPLO_ACCOUNT_ID="123456789012"
AWS_DEFAULT_REGION="us-west-2"

# Constructs:
terraform init \
  -backend-config="bucket=duplo-tfstate-123456789012" \
  -backend-config="region=us-west-2" \
  -backend-config="dynamodb_table=duplo-tfstate-123456789012-lock"
```

## IAM and Security

Duplocloud manages IAM roles per tenant. Access AWS resources via:

1. **JIT credentials** - Temporary STS tokens (recommended)
2. **Tenant IAM role** - Assumed by workloads
3. **Service account** - For Kubernetes pods (IRSA)

```hcl
# Get tenant IAM role ARN
data "duplocloud_tenant" "this" {
  name = local.tenant.name
}

# Use in IAM trust policies
resource "aws_iam_role_policy" "example" {
  role   = data.duplocloud_tenant.this.iam_role_name
  policy = jsonencode({...})
}
```

## AWS Region Handling

Region comes from module.ctx or infrastructure:

```hcl
locals {
  region = module.ctx.region  # From Duplocloud context
}

# Or from infrastructure workspace
locals {
  region = local.infra.region
}
```
