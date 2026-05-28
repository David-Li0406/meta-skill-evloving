---
name: terraform-infrastructure-as-code
description: Use this skill when provisioning cloud resources, managing state, creating modules, or reviewing Terraform configurations for infrastructure as code.
---

# Terraform Infrastructure as Code

Comprehensive guide for building, managing, and scaling infrastructure with Terraform.

## When to Use

- Provisioning cloud infrastructure (AWS, GCP, Azure, etc.)
- Creating reusable infrastructure modules
- Managing multi-environment deployments
- Reviewing Terraform code for best practices
- Debugging state or plan issues
- Migrating infrastructure between providers

## Basic Structure

```hcl
# Provider configuration
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "<your-terraform-state-bucket>"
    key    = "<your-terraform-state-key>"
    region = "<your-region>"
  }
}

provider "aws" {
  region = var.region
}
```

## Resources

```hcl
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name        = "web-server"
    Environment = var.environment
  }

  lifecycle {
    create_before_destroy = true
    prevent_destroy       = false
  }
}
```

## Variables

```hcl
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "development"

  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be development, staging, or production."
  }
}

variable "instance_count" {
  description = "Number of instances"
  type        = number
  default     = 1
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
```

## Outputs

```hcl
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.web.id
}

output "public_ip" {
  description = "Public IP address"
  value       = aws_instance.web.public_ip
  sensitive   = false
}
```

## State Management

**Remote State (Required for Teams)**
```hcl
# backend.tf - S3 backend with DynamoDB locking
terraform {
  backend "s3" {
    bucket         = "<your-terraform-state-bucket>"
    key            = "<your-terraform-state-key>"
    region         = "<your-region>"
    encrypt        = true
    dynamodb_table = "<your-dynamodb-table>"
  }
}
```

**State Commands:**
```bash
# List resources in state
terraform state list

# Show specific resource
terraform state show aws_instance.web

# Move resource (refactoring)
terraform state mv aws_instance.old aws_instance.new

# Remove from state (not destroy)
terraform state rm aws_instance.imported

# Import existing resource
terraform import aws_instance.web <instance-id>
```

## Project Structure

**Standard Module Layout:**
```
project/
├── main.tf              # Primary resources
├── variables.tf         # Input variables
├── outputs.tf           # Output values
├── versions.tf          # Provider versions
├── terraform.tfvars     # Variable values (gitignored)
├── backend.tf           # State configuration
│
├── modules/             # Local modules
│   └── vpc/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
│
└── environments/        # Environment-specific
    ├── dev/
    │   ├── main.tf      # Calls root module
    │   └── terraform.tfvars
    ├── staging/
    └── prod/
```

## Common Commands

```bash
# Initialize (first time or after backend change)
terraform init

# Format code
terraform fmt -recursive

# Validate syntax
terraform validate

# Plan changes (always review!)
terraform plan -out=tfplan

# Apply from plan file
terraform apply tfplan

# Destroy (careful!)
terraform destroy
```

## Best Practices

### File Organization

```
project/
├── main.tf          # Main resources
├── variables.tf     # Variable declarations
├── outputs.tf       # Output declarations
├── versions.tf      # Provider versions
├── terraform.tfvars # Variable values (gitignored if sensitive)
└── modules/         # Local modules
```

### Use Variables for Flexibility

```hcl
resource "aws_instance" "web" {
  instance_type = var.instance_type
}
```

### Use Locals for Computed Values

```hcl
locals {
  timestamp = formatdate("YYYY-MM-DD-hhmmss", timestamp())
  full_name = "${var.prefix}-${var.name}-${var.suffix}"
}
```

### Security Best Practices

**1. Never Hardcode Secrets:**
```hcl
variable "db_password" {
  type      = string
  sensitive = true
}

resource "aws_db_instance" "good" {
  password = var.db_password
}
```

**2. Encrypt Everything:**
```hcl
resource "aws_s3_bucket" "data" {
  bucket = "${var.project}-data"
}
```

**3. Least Privilege IAM:**
```hcl
resource "aws_iam_policy" "app" {
  name = "${var.project}-app-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.data.arn}/*"
      }
    ]
  })
}
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| State lock stuck | `terraform force-unlock LOCK_ID` |
| Resource drift | `terraform plan` to detect, `terraform apply` to fix |
| Import existing | `terraform import TYPE.NAME ID` |
| Module not found | `terraform init -upgrade` |
| Provider version conflict | Check `versions.tf`, run `terraform init -upgrade` |

### Checklist

Before applying:
- [ ] `terraform fmt` - Code formatted
- [ ] `terraform validate` - Syntax valid
- [ ] `terraform plan` reviewed - No surprises
- [ ] Sensitive values marked `sensitive = true`
- [ ] No hardcoded secrets
- [ ] Resources tagged properly
- [ ] State backend configured (not local)
- [ ] Provider versions pinned

## Integration

Works with:
- `/devops` - Infrastructure automation
- `/aws`, `/gcp`, `/azure` - Cloud-specific patterns
- `/security` - Security review of Terraform code
- `policy-as-code` skill - Terraform compliance checking