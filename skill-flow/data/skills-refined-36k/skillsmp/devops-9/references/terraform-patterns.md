# Terraform Best Practices

Infrastructure as code patterns for reliable deployments.

## Project Structure

```
terraform/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── ecs/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── prod/
└── backend.tf
```

## State Management

```hcl
# backend.tf - Remote state with locking
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "prod/infrastructure.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

# Create the lock table
resource "aws_dynamodb_table" "terraform_lock" {
  name         = "terraform-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

## Provider Pinning

```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # Allow patch updates only
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}
```

## Variables and Validation

```hcl
variable "environment" {
  type        = string
  description = "Environment name (dev, staging, prod)"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_type" {
  type        = string
  default     = "t3.micro"
  description = "EC2 instance type"

  validation {
    condition     = can(regex("^t3\\.", var.instance_type))
    error_message = "Must use t3 instance family."
  }
}
```

## Module Patterns

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(var.tags, {
    Name = "${var.name}-vpc"
  })
}

# modules/vpc/variables.tf
variable "name" {
  type        = string
  description = "VPC name prefix"
}

variable "cidr_block" {
  type        = string
  description = "VPC CIDR block"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Additional tags"
}

# modules/vpc/outputs.tf
output "vpc_id" {
  value       = aws_vpc.main.id
  description = "VPC ID"
}
```

## Using Modules

```hcl
module "vpc" {
  source = "../../modules/vpc"

  name       = "production"
  cidr_block = "10.0.0.0/16"

  tags = {
    Environment = "prod"
    ManagedBy   = "terraform"
  }
}

# Reference output
resource "aws_subnet" "private" {
  vpc_id = module.vpc.vpc_id
  # ...
}
```

## Data Sources

```hcl
# Look up existing resources
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

data "aws_caller_identity" "current" {}

resource "aws_instance" "app" {
  ami = data.aws_ami.amazon_linux.id
}
```

## Secrets Management

```hcl
# ❌ Bad: Hardcoded secret
resource "aws_db_instance" "db" {
  password = "supersecret123"  # Stored in state!
}

# ✅ Good: External secret
data "aws_secretsmanager_secret_version" "db" {
  secret_id = "prod/database/password"
}

resource "aws_db_instance" "db" {
  password = data.aws_secretsmanager_secret_version.db.secret_string
}

# ✅ Good: Generated secret
resource "random_password" "db" {
  length  = 32
  special = true
}

resource "aws_secretsmanager_secret_version" "db" {
  secret_id     = aws_secretsmanager_secret.db.id
  secret_string = random_password.db.result
}
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Local state | Lost state = orphaned resources | Use remote backend |
| No state locking | Concurrent runs corrupt state | Use DynamoDB lock |
| Unpinned providers | Breaking changes on update | Pin versions |
| Hardcoded values | Inflexible, error-prone | Use variables |
| No outputs | Can't reference in other configs | Export key values |

## Commands Reference

```bash
# Initialize
terraform init

# Plan (preview changes)
terraform plan -out=plan.tfplan

# Apply saved plan
terraform apply plan.tfplan

# Destroy (careful!)
terraform destroy

# Format code
terraform fmt -recursive

# Validate syntax
terraform validate

# Import existing resource
terraform import aws_instance.app i-1234567890
```
