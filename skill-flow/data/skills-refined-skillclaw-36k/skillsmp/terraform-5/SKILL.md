---
name: terraform
description: Terraform patterns for AWS infrastructure. Use when writing IaC for cloud infrastructure.
---

# Terraform (AWS Focus)

## Module Structure

```
modules/
└── vpc/
    ├── main.tf       # Resources
    ├── variables.tf  # Input variables
    ├── outputs.tf    # Output values
    └── versions.tf   # Provider requirements
```

## Variable Validation

```hcl
variable "environment" {
  type        = string
  description = "Environment name"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_type" {
  type    = string
  default = "t3.micro"

  validation {
    condition     = can(regex("^t3\\.", var.instance_type))
    error_message = "Only t3 instance types allowed."
  }
}
```

## Resource Patterns

```hcl
# Conditional resource
resource "aws_eip" "nat" {
  count = var.enable_nat_gateway ? 1 : 0
  vpc   = true
}

# For each from map
resource "aws_subnet" "private" {
  for_each          = var.private_subnets
  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value.cidr
  availability_zone = each.value.az

  tags = merge(local.common_tags, {
    Name = "${var.name}-private-${each.key}"
  })
}

# Dynamic blocks
resource "aws_security_group" "main" {
  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = "tcp"
      cidr_blocks = ingress.value.cidrs
    }
  }
}
```

## State Management

```hcl
# Remote state backend
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "env/prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# Read remote state
data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "my-terraform-state"
    key    = "env/prod/vpc/terraform.tfstate"
    region = "us-east-1"
  }
}
```

## Common Patterns

```hcl
# Locals for computed values
locals {
  common_tags = {
    Environment = var.environment
    ManagedBy   = "terraform"
    Project     = var.project
  }

  az_count = length(data.aws_availability_zones.available.names)
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_caller_identity" "current" {}

# Outputs
output "vpc_id" {
  value       = aws_vpc.main.id
  description = "VPC ID"
}
```

## Best Practices

- Use workspaces or separate state files per environment
- Enable state locking with DynamoDB
- Use `terraform fmt` and `terraform validate`
- Pin provider versions
- Use modules for reusable components
- Tag all resources consistently
- Use `prevent_destroy` for critical resources
- Use `create_before_destroy` for zero-downtime updates
- Store sensitive values in SSM/Secrets Manager
- Run `terraform plan` in CI before apply
