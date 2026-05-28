---
name: terraform-infrastructure-as-code
description: Use this skill when you need to manage infrastructure as code using Terraform, including resource management, module design, and state management.
---

# Terraform Infrastructure as Code

You are an expert in Terraform with deep knowledge of infrastructure as code, resource management, module design, and state management. This skill provides a comprehensive guide for Terraform development.

## Core Principles

- Write concise, well-structured Terraform code with accurate examples.
- Organize infrastructure into reusable modules.
- Use versioned modules and provider version locks for consistent deployments.
- Avoid hardcoded values; leverage variables for flexibility.

## Code Structure

- Structure configurations into logical sections:
  - `main.tf` - Primary resource definitions.
  - `variables.tf` - Input variable declarations.
  - `outputs.tf` - Output values.
  - `modules/` - Reusable modules.

## Terraform CLI Basic Commands

### Initialization and Planning

```sh
# Initialize workspace (download providers)
terraform init

# Initialize with backend config
terraform init -backend-config="bucket=my-terraform-state"

# Check execution plan
terraform plan

# Save execution plan to file
terraform plan -out=tfplan
```

### Apply and Destroy

WARNING: These commands modify infrastructure. Always run `terraform plan` first and ask for user permission.

```sh
# Apply changes
terraform apply

# Apply saved plan
terraform apply tfplan

# Auto-approve apply (for CI/CD)
terraform apply -auto-approve

# Destroy resources
terraform destroy
```

### State Management

```sh
# Check state
terraform state list

# Show resource details
terraform state show aws_instance.example

# Move resource (for refactoring)
terraform state mv aws_instance.old aws_instance.new

# Import existing resource
terraform import aws_instance.example i-1234567890abcdef0

# Remove resource from state (keeps actual resource)
terraform state rm aws_instance.example
```

## Resource Management

### Basic Resource Block Structure

```hcl
resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "example-instance"
  }
}
```

### Meta-arguments

- `depends_on`: Explicit dependencies.
- `count`: Resource replication (index-based).
- `for_each`: Resource replication (key-based).
- `provider`: Specify alternate provider.
- `lifecycle`: Lifecycle control.

### Lifecycle Settings

```hcl
resource "aws_instance" "example" {
  # ...

  lifecycle {
    create_before_destroy = true  # Create new first on replacement
    prevent_destroy       = true  # Prevent deletion
    ignore_changes        = [tags] # Attributes to ignore changes
  }
}
```

## Module Design

### Module Invocation

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"
}
```

### Module Best Practices

- Standard file structure: `main.tf`, `variables.tf`, `outputs.tf`.
- Document with README.md.
- Set meaningful default values.
- Validate inputs with validation blocks.

## State Management

### Remote Backend Configuration

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### State Management Best Practices

- Use remote backend (required for team development).
- Enable state locking (prevent concurrent execution).
- Enable encryption.
- Do not directly edit state file (use `terraform state` commands).
- Separate state files per environment.

## Variables and Outputs

### Input Variables

```hcl
variable "instance_type" {
  type        = string
  description = "EC2 instance type"
  default     = "t2.micro"

  validation {
    condition     = contains(["t2.micro", "t2.small", "t2.medium"], var.instance_type)
    error_message = "Please specify an allowed instance type"
  }
}
```

### Sensitive Data Handling

```hcl
variable "db_password" {
  type      = string
  sensitive = true  # Mask in output
}

output "connection_string" {
  value     = "postgres://user:${var.db_password}@host/db"
  sensitive = true  # Output contains sensitive data
}
```

## Security Best Practices

- Define access controls and security groups for resources.
- Follow cloud-provider security guidelines for AWS, Azure, and GCP.
- Encrypt state at rest.
- Use IAM roles and policies appropriately.
- Implement least privilege access.

## Collaboration & Production

- Implement rollback mechanisms.
- Use approval workflows for production deployments.
- Monitor state consistency and address drift issues.
- Use resource targeting to optimize changes.

## Reference Links

- Official docs: <https://developer.hashicorp.com/terraform/docs>
- Language reference: <https://developer.hashicorp.com/terraform/language>
- CLI reference: <https://developer.hashicorp.com/terraform/cli>
- Provider registry: <https://registry.terraform.io/>
- Module registry: <https://registry.terraform.io/browse/modules>
- HCP Terraform: <https://developer.hashicorp.com/terraform/cloud-docs>