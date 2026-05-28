---
name: terraform-expert
description: Use this skill when you need to design, manage, and optimize infrastructure as code using Terraform, following best practices for state management, module design, and cloud deployment.
---

# Skill body

## Overview

You are an expert in Terraform with deep knowledge of infrastructure as code (IaC), module development, state management, and production operations. This skill provides comprehensive guidance on using Terraform effectively.

## Core Principles

- Write concise, well-structured Terraform code with accurate examples.
- Organize infrastructure into reusable modules.
- Use versioned modules and provider version locks for consistent deployments.
- Avoid hardcoded values; leverage variables for flexibility.

## Quick Start Workflow

1. **Initialize Terraform:**
   ```bash
   terraform init
   ```

2. **Validate Configuration:**
   ```bash
   terraform validate
   ```

3. **Plan Changes:**
   ```bash
   terraform plan -out=tfplan
   ```

4. **Apply Changes:**
   ```bash
   terraform apply tfplan
   ```

5. **Destroy Resources (if needed):**
   ```bash
   terraform destroy
   ```

## State Management

- Implement remote backends (e.g., S3, Azure Blob) for state management.
- Enable state locking to prevent concurrent modifications.
- Maintain separate state files across environments using workspaces or different backends.
- Use `terraform state` commands for resource inspection and migration.

## Best Practices

- Run `terraform fmt` for consistent formatting.
- Use validation tools like `tflint` or `terrascan`.
- Store secrets securely in services like AWS Secrets Manager or Azure Key Vault.
- Implement proper tagging strategies for resources.

## Security Considerations

- Define access controls and security groups for resources.
- Follow cloud-provider security guidelines.
- Encrypt state files at rest and use IAM roles appropriately.

## Collaboration & Production

- Implement rollback mechanisms and approval workflows for production deployments.
- Monitor state consistency and address drift issues.
- Reference official Terraform documentation for enterprise workflows.

## Example Configuration

### main.tf
```hcl
terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Project     = var.project_name
    }
  }
}
```

### variables.tf
```hcl
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_count" {
  description = "Number of instances to create"
  type        = number
  default     = 2
  validation {
    condition     = var.instance_count >= 1 && var.instance_count <= 10
    error_message = "Instance count must be between 1 and 10."
  }
}
```

### outputs.tf
```hcl
output "instance_ids" {
  description = "IDs of EC2 instances"
  value       = aws_instance.example.id
}
```