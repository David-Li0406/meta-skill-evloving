# Module Patterns Reference

## Variable Best Practices

### DO: Use Descriptive Descriptions

```hcl
# ✅ GOOD: Clear, actionable description
variable "instance_type" {
  description = "EC2 instance type. Use t3.micro for dev, t3.large+ for prod. See https://aws.amazon.com/ec2/instance-types/"
  type        = string
  default     = "t3.micro"
}

# ❌ BAD: Useless description
variable "instance_type" {
  description = "The instance type"
  type        = string
}
```

### DO: Add Validation Rules

```hcl
# ✅ GOOD: Validates input at plan time
variable "environment" {
  description = "Deployment environment"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "VPC CIDR must be a valid IPv4 CIDR block."
  }
}

variable "instance_count" {
  description = "Number of instances to create"
  type        = number

  validation {
    condition     = var.instance_count >= 1 && var.instance_count <= 10
    error_message = "Instance count must be between 1 and 10."
  }
}
```

### DO: Use Object Types for Related Variables

```hcl
# ✅ GOOD: Related variables grouped
variable "database" {
  description = "Database configuration"
  type = object({
    engine         = string
    engine_version = string
    instance_class = string
    storage_gb     = number
    multi_az       = optional(bool, false)
    backup_retention_days = optional(number, 7)
  })

  validation {
    condition     = contains(["postgres", "mysql", "mariadb"], var.database.engine)
    error_message = "Database engine must be postgres, mysql, or mariadb."
  }
}

# Usage
database = {
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.medium"
  storage_gb     = 100
  multi_az       = true
}

# ❌ BAD: Scattered related variables
variable "db_engine" { }
variable "db_version" { }
variable "db_instance_class" { }
variable "db_storage" { }
variable "db_multi_az" { }
```

### DO: Use Optional Attributes (Terraform 1.3+)

```hcl
# ✅ GOOD: Optional with defaults
variable "monitoring" {
  description = "Monitoring configuration"
  type = object({
    enabled        = optional(bool, true)
    retention_days = optional(number, 30)
    alert_email    = optional(string)
    metrics = optional(list(string), [
      "CPUUtilization",
      "MemoryUtilization"
    ])
  })
  default = {}
}

# All valid usages:
monitoring = {}                           # Uses all defaults
monitoring = { enabled = false }          # Override one field
monitoring = { alert_email = "ops@co.io"} # Add optional field
```

### DON'T: Create "God Variables"

```hcl
# ❌ BAD: Too many unrelated options
variable "config" {
  type = object({
    vpc_cidr           = string
    instance_type      = string
    db_password        = string
    enable_logging     = bool
    domain_name        = string
    certificate_arn    = string
    # ... 50 more fields
  })
}

# ✅ GOOD: Logical groupings
variable "network" {
  type = object({
    vpc_cidr = string
    # network-related fields
  })
}

variable "compute" {
  type = object({
    instance_type = string
    # compute-related fields
  })
}
```

---

## Output Best Practices

### DO: Output Everything Downstream Needs

```hcl
# ✅ GOOD: Complete outputs for module consumers
output "vpc" {
  description = "VPC attributes for downstream modules"
  value = {
    id                  = aws_vpc.main.id
    arn                 = aws_vpc.main.arn
    cidr_block          = aws_vpc.main.cidr_block
    default_route_table_id = aws_vpc.main.default_route_table_id
  }
}

output "subnets" {
  description = "Subnet attributes organized by type"
  value = {
    private = {
      ids  = aws_subnet.private[*].id
      arns = aws_subnet.private[*].arn
      cidrs = aws_subnet.private[*].cidr_block
    }
    public = {
      ids  = aws_subnet.public[*].id
      arns = aws_subnet.public[*].arn
      cidrs = aws_subnet.public[*].cidr_block
    }
  }
}
```

### DO: Use Consistent Output Naming

```hcl
# ✅ GOOD: Consistent pattern
output "cluster_id" { }
output "cluster_arn" { }
output "cluster_endpoint" { }
output "cluster_security_group_id" { }

# ❌ BAD: Inconsistent naming
output "id" { }
output "the_arn" { }
output "endpoint_url" { }
output "sg" { }
```

### DO: Mark Sensitive Outputs

```hcl
# ✅ GOOD: Prevents accidental exposure
output "database_password" {
  description = "Database master password"
  value       = random_password.db.result
  sensitive   = true
}

output "api_key" {
  description = "API key for external service"
  value       = aws_api_gateway_api_key.main.value
  sensitive   = true
}
```

### DON'T: Output Raw Resources

```hcl
# ❌ BAD: Exposes entire resource (may include sensitive data)
output "instance" {
  value = aws_instance.web
}

# ✅ GOOD: Explicit, controlled outputs
output "instance" {
  value = {
    id         = aws_instance.web.id
    arn        = aws_instance.web.arn
    public_ip  = aws_instance.web.public_ip
    private_ip = aws_instance.web.private_ip
  }
}
```

---

## Module Composition Patterns

### Pattern: Wrapper Module

```hcl
# modules/vpc-wrapper/main.tf
# Thin wrapper around terraform-aws-modules/vpc

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  # Enforce organization standards
  name = "${var.project}-${var.environment}-vpc"
  cidr = var.vpc_cidr

  # Standard AZ configuration
  azs             = slice(data.aws_availability_zones.available.names, 0, 3)
  private_subnets = [for i in range(3) : cidrsubnet(var.vpc_cidr, 4, i)]
  public_subnets  = [for i in range(3) : cidrsubnet(var.vpc_cidr, 4, i + 3)]

  # Enforce standards
  enable_nat_gateway     = true
  single_nat_gateway     = var.environment != "prod"
  enable_dns_hostnames   = true
  enable_dns_support     = true

  # Standard tags
  tags = merge(var.tags, {
    Environment = var.environment
    ManagedBy   = "terraform"
  })
}
```

### Pattern: Facade Module

```hcl
# modules/microservice/main.tf
# Composes multiple resources into one deployable unit

module "vpc" {
  source = "../vpc-wrapper"
  # ...
}

module "ecs_cluster" {
  source = "../ecs-cluster"
  vpc_id = module.vpc.vpc_id
  # ...
}

module "alb" {
  source     = "../alb"
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.public_subnet_ids
  # ...
}

module "service" {
  source     = "../ecs-service"
  cluster_id = module.ecs_cluster.cluster_id
  alb_arn    = module.alb.arn
  # ...
}
```

### Pattern: Feature Flags

```hcl
# Enable/disable features with boolean flags

variable "features" {
  description = "Feature toggles"
  type = object({
    enable_monitoring    = optional(bool, true)
    enable_backup        = optional(bool, true)
    enable_encryption    = optional(bool, true)
    enable_multi_az      = optional(bool, false)
  })
  default = {}
}

resource "aws_cloudwatch_metric_alarm" "cpu" {
  count = var.features.enable_monitoring ? 1 : 0
  # ...
}

resource "aws_backup_plan" "main" {
  count = var.features.enable_backup ? 1 : 0
  # ...
}

resource "aws_db_instance" "main" {
  multi_az        = var.features.enable_multi_az
  storage_encrypted = var.features.enable_encryption
  # ...
}
```

---

## Anti-Patterns to Avoid

### DON'T: Hardcode Values

```hcl
# ❌ BAD: Hardcoded values
resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t3.large"
  
  tags = {
    Environment = "production"
  }
}

# ✅ GOOD: Parameterized
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type
  
  tags = var.tags
}
```

### DON'T: Use Providers in Modules

```hcl
# ❌ BAD: Provider in module
# modules/vpc/main.tf
provider "aws" {
  region = "us-east-1"
}

# ✅ GOOD: Provider passed from root
# modules/vpc/versions.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

# Root module passes provider
module "vpc" {
  source = "./modules/vpc"
  providers = {
    aws = aws.east
  }
}
```

### DON'T: Use Remote State in Modules

```hcl
# ❌ BAD: Data source in module
# modules/app/main.tf
data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "my-state-bucket"
    key    = "vpc/terraform.tfstate"
  }
}

# ✅ GOOD: Accept values as variables
variable "vpc_id" {
  description = "VPC ID to deploy into"
  type        = string
}

variable "subnet_ids" {
  description = "Subnet IDs for deployment"
  type        = list(string)
}
```

### DON'T: Deeply Nest Modules

```hcl
# ❌ BAD: 4+ levels of nesting
module "platform" {
  source = "./modules/platform"
  # which calls...
  #   module "networking"
  #     which calls...
  #       module "vpc"
  #         which calls...
  #           module "subnets"
}

# ✅ GOOD: Max 2-3 levels
module "vpc" {
  source = "./modules/vpc"
}

module "ecs" {
  source = "./modules/ecs"
  vpc_id = module.vpc.vpc_id
}
```

---

## Module Documentation

### README Template

```markdown
# Module Name

Brief description of what this module creates.

## Usage

\```hcl
module "example" {
  source = "path/to/module"

  environment = "prod"
  vpc_cidr    = "10.0.0.0/16"
}
\```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.6.0 |
| aws | >= 5.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| environment | Deployment environment | `string` | n/a | yes |
| vpc_cidr | VPC CIDR block | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| vpc_id | The ID of the VPC |

## Examples

- [Basic](./examples/basic) - Minimal configuration
- [Complete](./examples/complete) - All features enabled
```

### Auto-Generate with terraform-docs

```yaml
# .terraform-docs.yml
formatter: markdown table

output:
  file: README.md
  mode: inject

sort:
  enabled: true
  by: required

settings:
  indent: 2
  escape: true
  html: false
```

```bash
# Generate documentation
terraform-docs markdown table --output-file README.md .
```
