---
name: terraform-examples
description: 'Comprehensive templates and patterns for creating Terraform module examples. Use when creating examples/ directory, writing inline examples in README.md, or needing example file templates (main.tf, variables.tf, outputs.tf, versions.tf, README.md). Covers basic/complete/scenario examples, placeholder conventions, and testing workflows for ECS, load balancer, and secrets modules.'
---

# Terraform Module Examples - Technical Reference

## When to Use This Skill

- User asks to "create examples", "add example configurations", or "write example code"
- Creating or updating `examples/` directory structure
- Writing inline examples for README.md (minimal and advanced setups)
- Need templates for example files (main.tf, variables.tf, outputs.tf, etc.)
- Determining common scenario directories (with-load-balancer/, service-connect-only/, etc.)
- Setting up example testing or CI/CD validation
- Questions about placeholder conventions or example best practices

## Prerequisites

- Understanding of the module's functionality and use cases
- Knowledge of required vs. optional variables
- Familiarity with CloudPosse label module integration
- Understanding of target scenarios (basic, complete, specific use cases)

## Overview

This skill provides comprehensive reference for creating runnable Terraform module examples. Examples demonstrate real-world usage patterns and help users understand module implementation.

## Example Types

### 1. Inline Examples (README.md)

**Minimal Setup - Required:**
```terraform
module "basic_service" {
  source = "github.com/Luscii/terraform-aws-ecs-service"

  # Required variables only
  name            = "my-service"
  ecs_cluster_name = "production"
  vpc_id          = "vpc-12345678"
  subnets         = ["subnet-12345678", "subnet-87654321"]

  task_cpu    = 256
  task_memory = 512

  container_definitions = [{
    name  = "app"
    image = "nginx:latest"
  }]

  task_role      = { name = "task-role", arn = "arn:aws:iam::123456789012:role/task-role" }
  execution_role = { name = "exec-role", arn = "arn:aws:iam::123456789012:role/exec-role" }

  context = module.label.context
}
```

**Characteristics:**
- Under 30 lines
- Required variables only
- Sensible defaults
- Generic but realistic values
- No optional features

**Advanced Setup - Required:**
```terraform
module "label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = "luscii"
  environment = "production"
  name        = "api"
}

module "advanced_service" {
  source = "github.com/Luscii/terraform-aws-ecs-service"

  name             = module.label.name
  ecs_cluster_name = "production"
  vpc_id           = "vpc-12345678"
  subnets          = ["subnet-12345678", "subnet-87654321"]

  task_cpu    = 1024
  task_memory = 2048

  container_definitions = [{
    name  = "app"
    image = "myregistry.io/api:v1.2.3"

    port_mappings = [{
      containerPort = 8080
      protocol      = "tcp"
      name          = "http"
    }]

    environment = [
      { name = "ENVIRONMENT", value = "production" },
      { name = "LOG_LEVEL", value = "info" }
    ]

    secrets = module.secrets.container_definition
  }]

  load_balancers = [{
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "app"
    container_port   = 8080
  }]

  scaling = {
    min_capacity = 2
    max_capacity = 10
  }

  scaling_target = {
    cpu = {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
      target_value           = 70
    }
  }

  task_role      = module.task_role.role
  execution_role = module.execution_role.role

  context = module.label.context
}

# Output usage demonstration
resource "aws_route53_record" "api" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = "api.example.com"
  type    = "A"

  alias {
    name                   = module.load_balancer.dns_name
    zone_id                = module.load_balancer.zone_id
    evaluate_target_health = true
  }
}
```

**Characteristics:**
- Under 100 lines
- Production-ready configuration
- Multiple optional features
- Output usage demonstrated
- Integration with other resources
- CloudPosse label context shown

### 2. Examples Directory (examples/)

**When to Create:**
- Module supports multiple distinct use cases
- Configurations too complex for inline examples
- Need tested, runnable configurations
- Users benefit from complete examples

**Directory Structure:**
```
examples/
├── README.md                 # Navigation to all examples
├── basic/                    # Minimal working example
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   └── README.md
├── complete/                 # Full-featured example
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   └── README.md
└── {scenario}/               # Use-case specific
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    ├── versions.tf
    └── README.md
```

## File Templates

### main.tf

```terraform
# Provider configuration
provider "aws" {
  region = var.region
}

# CloudPosse label module
module "label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"

  namespace   = var.namespace
  environment = var.environment
  name        = var.name
}

# Reference parent module with relative path
module "example" {
  source = "../../"

  # Configuration specific to this scenario
  name = module.label.name

  # ... other variables

  context = module.label.context
}

# Supporting resources (data sources, IAM roles, etc.)
data "aws_vpc" "this" {
  id = var.vpc_id
}

# Output usage demonstration
resource "aws_route53_record" "example" {
  # ... configuration
}
```

**Best Practices:**
- Use `source = "../../"` for parent module
- Include provider configuration
- Use variables for customizable values
- Add comments for key decisions
- Keep self-contained and runnable

### variables.tf

```terraform
variable "namespace" {
  type        = string
  description = "Namespace for resource naming"
  default     = "example"
}

variable "environment" {
  type        = string
  description = "Environment name (dev, staging, prod)"
  default     = "dev"
}

variable "name" {
  type        = string
  description = "Name of the resource"
  default     = "demo"
}

variable "region" {
  type        = string
  description = "AWS region for resources"
  default     = "eu-west-1"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID where resources will be created"
  default     = null
}

variable "subnet_ids" {
  type        = list(string)
  description = "List of subnet IDs for resource placement"
  default     = []
}
```

**Best Practices:**
- Provide sensible defaults
- Include clear descriptions
- Make infrastructure IDs customizable
- Allow region configuration
- Document expected values

### outputs.tf

```terraform
output "id" {
  value       = module.example.id
  description = "Unique identifier of the created resource"
}

output "arn" {
  value       = module.example.arn
  description = "ARN of the created resource"
}

output "name" {
  value       = module.example.name
  description = "Name of the created resource"
}

output "url" {
  value       = module.example.url
  description = "URL to access the resource"
}

output "security_group_id" {
  value       = module.example.security_group_id
  description = "Security group ID for network configuration"
}
```

**Best Practices:**
- Expose key module outputs
- Include descriptions
- Show integration points
- Document output usage

### versions.tf

```terraform
terraform {
  required_version = ">= 1.3"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.0"
    }
  }
}
```

**Best Practices:**
- Match parent module requirements
- Use >= for flexibility
- Include all required providers

### README.md (Example-specific)

```markdown
# {Scenario Name}

## Purpose

Brief description of what this example demonstrates and when to use it.

## What This Example Deploys

- Resource type 1 (e.g., ECS Fargate service with 2 tasks)
- Resource type 2 (e.g., Application Load Balancer)
- Resource type 3 (e.g., Auto-scaling configuration)
- Integration point (e.g., CloudWatch log group)

## Prerequisites

- Existing VPC with subnets
- ECS cluster (if applicable)
- IAM roles (if applicable)
- Valid AWS credentials configured

## Usage

```bash
# Set required variables (if not using defaults)
export TF_VAR_vpc_id="vpc-12345678"
export TF_VAR_subnet_ids='["subnet-12345678","subnet-87654321"]'

# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Apply the configuration
terraform apply
```

## Configuration

Key configuration points:

- **Feature A**: Explanation (e.g., "Load Balancer deployed in public subnets")
- **Feature B**: Explanation (e.g., "Scales 2-10 tasks based on CPU > 70%")
- **Feature C**: Explanation (e.g., "Health checks on /health endpoint")

## Testing

After deployment:

```bash
# Get output values
terraform output

# Test functionality (example)
curl http://$(terraform output -raw alb_dns_name)/
```

## Cleanup

```bash
terraform destroy
```

## Notes

- Important limitations or assumptions
- Prerequisites details
- Timing considerations (e.g., "Auto-scaling may take 3-5 minutes")
```

### examples/README.md (Root)

```markdown
# Examples

This directory contains examples demonstrating various ways to use this module.

## Available Examples

### [Basic Example](./basic/)

Minimal configuration showing the essential inputs required to use this module.

**Use this when:** You want the simplest possible setup to get started.

**Demonstrates:**
- Required variables only
- Minimal working configuration
- Basic module usage

---

### [Complete Example](./complete/)

Full-featured configuration demonstrating all major features and optional parameters.

**Use this when:** You need a production-ready configuration with common features.

**Demonstrates:**
- All important optional features
- Integration with other AWS services
- Output usage
- Production best practices

---

### [{Scenario Name}](./{scenario}/)

Brief description of the scenario.

**Use this when:** Specific use case description.

**Demonstrates:**
- Key feature 1
- Key feature 2
- Integration pattern

---

## Running Examples

Each example is self-contained. To run an example:

```bash
cd {example-directory}
terraform init
terraform plan
terraform apply
```

## Prerequisites

Common prerequisites for all examples:

- Terraform >= 1.3
- AWS Provider >= 6.0
- Valid AWS credentials configured
- [List specific AWS resources needed]

## Cleaning Up

To remove resources created by an example:

```bash
cd {example-directory}
terraform destroy
```
```

## Common Scenario Directories

### ECS Service Module

- `basic/` - Minimal service configuration
- `complete/` - Production-ready with all features
- `with-load-balancer/` - Service behind ALB
- `service-connect-only/` - Internal service using Service Connect
- `scheduled-task/` - Scheduled ECS task
- `with-autoscaling/` - Auto-scaling enabled

### Load Balancer Module

- `basic/` - Simple load balancer
- `complete/` - Full-featured ALB
- `public-alb/` - Internet-facing
- `internal-alb/` - Internal only
- `with-waf/` - WAF integration

### Secrets Module

- `basic/` - Simple secrets
- `new-secrets/` - Creating new secrets
- `existing-secrets/` - Using existing secrets
- `mixed/` - Combination of new and existing

## Placeholder Conventions

### In Code Comments

```terraform
# Replace with your VPC ID
vpc_id = "vpc-12345678"

# Replace with your subnet IDs
subnets = ["subnet-12345678", "subnet-87654321"]
```

### In README

Use angle brackets for placeholders:
- `<VPC_ID>` - "e.g., vpc-12345678"
- `<SUBNET_ID>` - "e.g., subnet-12345678"
- `<REGION>` - "e.g., eu-west-1"

Provide example values and where to find them.

### In Variables

```terraform
variable "vpc_id" {
  type        = string
  description = "VPC ID where resources will be created. Find in VPC console or use data source."
  default     = null  # Or sensible default
}
```

## Testing Checklist

Before committing examples:

1. **Initialize:** `terraform init` succeeds
2. **Validate:** `terraform validate` passes
3. **Format:** `terraform fmt` applied
4. **Plan:** `terraform plan` completes without errors
5. **Apply:** (Optional) Test actual deployment
6. **Documentation:** README complete and accurate
7. **Variables:** All have descriptions and defaults
8. **Outputs:** All documented
9. **Source:** Uses `source = "../../"`
10. **Versions:** Constraints specified

## CI/CD Integration Example

```yaml
# .github/workflows/validate-examples.yml
name: Validate Examples

on:
  pull_request:
    paths:
      - 'examples/**'
      - '*.tf'

jobs:
  validate:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        example: [basic, complete]
    steps:
      - uses: actions/checkout@v3

      - uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: "1.3"

      - name: Validate Example
        working-directory: examples/${{ matrix.example }}
        run: |
          terraform init
          terraform validate
          terraform fmt -check
```

## Example Quality Standards

### Working Code
- All examples tested and working
- Run `terraform plan` and `terraform apply`
- Include necessary data sources

### Self-Contained
- Independently runnable
- All required configurations included
- No external state dependencies (except documented prerequisites)

### Realistic
- Production-like configurations
- Realistic naming conventions
- Actual use cases demonstrated

### Documented
- Clear purpose explanation
- Why specific choices made
- Complete usage instructions
- Prerequisites listed
- Cleanup instructions provided

## Anti-Patterns

### ❌ DON'T

1. **Empty Examples:**
   - No placeholder examples
   - Every example must be complete

2. **Over-Complicated:**
   - Don't demonstrate everything in one example
   - Keep focused on specific use case

3. **Undocumented:**
   - Don't assume understanding
   - Document why, not just what

4. **Hardcoded Values:**
   - Use variables for customization
   - Provide defaults but allow overrides

5. **Missing Context:**
   - Don't skip CloudPosse label
   - Show how module fits in infrastructure

6. **Untested:**
   - Don't commit unvalidated examples
   - Run at least `terraform plan`

### ✅ DO

1. **Test Thoroughly:**
   - Validate all examples work
   - Format code consistently
   - Check all files present

2. **Document Completely:**
   - Explain purpose clearly
   - List prerequisites
   - Provide cleanup steps

3. **Keep Current:**
   - Update with module changes
   - Update provider versions
   - Re-test after updates

4. **Use Patterns:**
   - Follow standard structure
   - Use `source = "../../"`
   - Include all 5 required files

5. **Be Realistic:**
   - Show actual use cases
   - Use production-like values
   - Demonstrate integrations

## Maintenance

### Update Triggers

Update examples when:
- Module interface changes
- New features added
- Provider versions updated
- Terraform version updated
- Breaking changes introduced

### Version Management

```terraform
# Pin external modules
module "label" {
  source  = "cloudposse/label/null"
  version = "0.25.0"  # Exact version
}

# Reference parent with relative path
module "example" {
  source = "../../"  # Always relative
}
```

### Dependency Management

- Minimize external dependencies
- Document required resources clearly
- Provide data source examples for lookups
- Use variables for resource references
