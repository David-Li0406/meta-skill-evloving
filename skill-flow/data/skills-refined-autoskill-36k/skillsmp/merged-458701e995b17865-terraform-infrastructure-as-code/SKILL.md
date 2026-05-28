---
name: terraform-infrastructure-as-code
description: Use this skill when you need to manage cloud infrastructure using Terraform, focusing on best practices, module design, state management, and CI workflows.
---

# Terraform Infrastructure as Code

You are an expert in Terraform and infrastructure-as-code with deep knowledge of cloud providers, deployment patterns, and best practices for managing infrastructure.

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

## State Management

- Implement remote backends (S3, Azure Blob, GCS) for state management.
- Enable state locking to prevent concurrent modifications.
- Enable encryption for state files.
- Separate state files across environments using workspaces or different backends.
- Maintain backup procedures for state files.
- Use `terraform state` commands for resource inspection and migration.

## Best Practices

- Run `terraform fmt` for consistent formatting.
- Use validation tools like `tflint` or `terrascan`.
- Store secrets in Vault, AWS Secrets Manager, or Azure Key Vault.
- Use data sources for dynamic values.
- Implement proper tagging strategies.

## Safety Checklist

- **State**: Use a remote backend with locking; separate state per environment.
- **Reviews**: Plan in CI; apply from a trusted runner with approvals.
- **Guardrails**: Implement `prevent_destroy` and policy checks for production environments.

## Terraform CLI Basic Commands

### Initialization and Planning

```sh
# Initialize workspace (download providers)
terraform init

# Check execution plan
terraform plan

# Save execution plan to file
terraform plan -out=tfplan
```

### Apply and Destroy

WARNING: These commands modify infrastructure. Always run `terraform plan` first and ask for user permission.

```sh
# Apply changes
terraform apply tfplan

# Destroy resources
terraform destroy
```

### State Management Commands

```sh
# Check state
terraform state list

# Show resource details
terraform state show aws_instance.example

# Import existing resource
terraform import aws_instance.example i-1234567890abcdef0
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

## Security Best Practices

- Define access controls and security groups for resources.
- Follow cloud-provider security guidelines for AWS, Azure, and GCP.
- Encrypt state at rest.
- Use IAM roles and policies appropriately.
- Implement least privilege access.

## References

- Official docs: <https://developer.hashicorp.com/terraform/docs>
- Language reference: <https://developer.hashicorp.com/terraform/language>
- CLI reference: <https://developer.hashicorp.com/terraform/cli>
- Provider registry: <https://registry.terraform.io/>
- Module registry: <https://registry.terraform.io/browse/modules>
- HCP Terraform: <https://developer.hashicorp.com/terraform/cloud-docs>