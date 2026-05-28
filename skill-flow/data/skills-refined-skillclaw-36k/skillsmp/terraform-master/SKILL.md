---
name: terraform-master
description: Comprehensive Terraform/OpenTofu mastery covering testing (native 1.6+, Terratest), modules, CI/CD, security scanning (trivy, checkov), and production patterns. Use for IaC architecture, module development, testing strategy, state management, and infrastructure decisions.
---

# Terraform Master

> **Load this skill** before working on Terraform/OpenTofu infrastructure, module development, testing, or CI/CD pipelines.

## Core Principles

1. **Modules Over Monoliths** - Compose infrastructure from reusable, tested modules
2. **Test Before Apply** - Validate with native tests, linting, and security scans
3. **State is Sacred** - Remote state, locking, encryption, least-privilege access
4. **Explicit Over Implicit** - Pin versions, declare dependencies, avoid magic

---

## Testing Strategy Framework

### Decision Matrix: Which Testing Approach?

| Scenario | Native Test | Terratest | Mock | Validate |
|----------|-------------|-----------|------|----------|
| Variable validation | - | - | - | ✅ |
| Output format check | ✅ | - | - | - |
| Resource config logic | ✅ | - | ✅ | - |
| Cross-module integration | - | ✅ | - | - |
| Real cloud resources | - | ✅ | - | - |
| CI/CD (fast feedback) | ✅ | - | ✅ | ✅ |
| Cost-sensitive | ✅ | - | ✅ | ✅ |

### Testing Pyramid for Terraform

```
           ╱╲
          ╱  ╲      E2E / Terratest (10%)
         ╱────╲     - Real infrastructure
        ╱      ╲    - Expensive, slow
       ╱────────╲   
      ╱          ╲  Integration Tests (20%)
     ╱────────────╲ - terraform plan analysis
    ╱              ╲- Cross-module validation
   ╱────────────────╲
   ╲                ╱ Unit Tests (70%)
    ╲──────────────╱  - Native tests with mocks
     ╲            ╱   - Variable validation
      ╲──────────╱    - Fast, no cloud costs
```

### Native Testing (Terraform 1.6+)

```hcl
# tests/vpc_basic.tftest.hcl
run "vpc_creates_with_correct_cidr" {
  command = plan  # Use 'plan' for fast tests, 'apply' for real resources

  variables {
    vpc_cidr = "10.0.0.0/16"
    environment = "test"
  }

  assert {
    condition     = aws_vpc.main.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR block mismatch"
  }

  assert {
    condition     = length(aws_subnet.private) == 3
    error_message = "Expected 3 private subnets"
  }
}
```

### Mock Providers (Terraform 1.7+)

```hcl
# tests/mocks/aws.tfmock.hcl
mock_provider "aws" {
  mock_resource "aws_vpc" {
    defaults = {
      id         = "vpc-mock12345"
      arn        = "arn:aws:ec2:us-east-1:123456789:vpc/vpc-mock12345"
      cidr_block = "10.0.0.0/16"
    }
  }
}
```

---

## Module Hierarchy

### The Four Levels

```
┌─────────────────────────────────────────────────────────────┐
│ COMPOSITION (Root Module)                                    │
│ - Environment-specific (dev/staging/prod)                   │
│ - Calls infrastructure modules                              │
│ - Contains terraform.tfvars, backend config                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ INFRASTRUCTURE MODULE                                        │
│ - Business logic (e.g., "microservice", "data-pipeline")    │
│ - Composes multiple resource modules                        │
│ - Opinionated defaults for your organization                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ RESOURCE MODULE                                              │
│ - Single resource type wrapper (e.g., "vpc", "rds")         │
│ - Thin wrapper with sensible defaults                       │
│ - Reusable across infrastructure modules                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ RESOURCE (Terraform primitives)                              │
│ - aws_vpc, google_compute_instance, azurerm_storage_account │
│ - Direct provider resources                                  │
└─────────────────────────────────────────────────────────────┘
```

### Module Composition Example

```hcl
# infrastructure-modules/microservice/main.tf
module "vpc" {
  source = "../../resource-modules/vpc"
  # ...
}

module "ecs_cluster" {
  source = "../../resource-modules/ecs-cluster"
  vpc_id = module.vpc.vpc_id
  # ...
}

module "rds" {
  source = "../../resource-modules/rds"
  vpc_id = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids
  # ...
}
```

---

## Code Structure Standards

### Resource Block Ordering

```hcl
resource "aws_instance" "web" {
  # 1. Meta-arguments (FIRST)
  count      = var.instance_count
  for_each   = var.instances
  provider   = aws.west
  depends_on = [aws_vpc.main]

  # 2. Required arguments (alphabetical)
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.subnet_id

  # 3. Optional arguments (alphabetical)
  associate_public_ip_address = false
  monitoring                  = true
  
  # 4. Nested blocks (alphabetical)
  root_block_device {
    volume_size = 100
    volume_type = "gp3"
  }

  # 5. Tags (LAST)
  tags = merge(var.tags, {
    Name = "web-${count.index}"
  })

  # 6. Lifecycle (VERY LAST)
  lifecycle {
    create_before_destroy = true
    ignore_changes        = [tags["LastModified"]]
  }
}
```

### Variable Ordering

```hcl
# variables.tf - Ordered by: Required → Optional → Feature Flags

# === REQUIRED ===
variable "environment" {
  description = "Deployment environment (dev/staging/prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

# === OPTIONAL (with defaults) ===
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "tags" {
  description = "Additional tags for all resources"
  type        = map(string)
  default     = {}
}

# === FEATURE FLAGS ===
variable "enable_monitoring" {
  description = "Enable detailed monitoring"
  type        = bool
  default     = false
}

variable "enable_encryption" {
  description = "Enable encryption at rest"
  type        = bool
  default     = true
}
```

### File Structure

```
module/
├── main.tf           # Primary resources
├── variables.tf      # Input variables (ordered: required → optional → flags)
├── outputs.tf        # Output values
├── versions.tf       # Provider and Terraform version constraints
├── locals.tf         # Local values and computed expressions
├── data.tf           # Data sources (optional, can be in main.tf)
├── README.md         # Module documentation
└── tests/
    ├── basic.tftest.hcl
    ├── complete.tftest.hcl
    └── mocks/
        └── aws.tfmock.hcl
```

---

## Count vs For_Each Decision Guide

### Decision Tree

```
Need multiple similar resources?
│
├─► Resources are IDENTICAL (just need N copies)
│   └─► Use COUNT
│       count = 3
│       name  = "server-${count.index}"
│
├─► Resources have UNIQUE identifiers
│   └─► Use FOR_EACH with map/set
│       for_each = toset(["web", "api", "worker"])
│       name     = "server-${each.key}"
│
└─► Resources might be ADDED/REMOVED independently
    └─► Use FOR_EACH (ALWAYS)
        # Prevents index shifting issues
```

### Count Gotchas

```hcl
# ❌ DANGER: Removing item shifts all indices
variable "servers" {
  default = ["web", "api", "db"]  # Remove "api" → db becomes index 1!
}

resource "aws_instance" "server" {
  count = length(var.servers)
  tags  = { Name = var.servers[count.index] }
}

# ✅ SAFE: Each resource has stable identity
resource "aws_instance" "server" {
  for_each = toset(var.servers)
  tags     = { Name = each.key }
}
```

### When to Use Count

```hcl
# ✅ Good: Boolean toggle
resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  count = var.enable_monitoring ? 1 : 0
  # ...
}

# ✅ Good: Fixed number of identical resources
resource "aws_subnet" "private" {
  count             = 3
  availability_zone = data.aws_availability_zones.available.names[count.index]
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index)
}
```

---

## Modern Terraform Features

### Version Feature Matrix

| Feature | Version | Use Case |
|---------|---------|----------|
| `nullable` variables | 1.1+ | Optional object attributes |
| `precondition`/`postcondition` | 1.2+ | Runtime validation |
| `replace_triggered_by` | 1.2+ | Force replacement on changes |
| Optional object attributes | 1.3+ | Flexible variable types |
| `terraform_data` resource | 1.4+ | Replace `null_resource` |
| `import` block | 1.5+ | Declarative imports |
| Native testing | 1.6+ | `.tftest.hcl` files |
| Mock providers | 1.7+ | Fast unit tests |
| `removed` block | 1.7+ | Safe resource removal |
| Provider-defined functions | 1.8+ | Provider-specific helpers |
| `ephemeral` variables | 1.10+ | Sensitive data handling |
| `write_only` attributes | 1.11+ | Credentials management |

### Preconditions and Postconditions

```hcl
resource "aws_instance" "web" {
  instance_type = var.instance_type
  ami           = var.ami_id

  lifecycle {
    precondition {
      condition     = data.aws_ami.selected.architecture == "x86_64"
      error_message = "AMI must be x86_64 architecture."
    }

    postcondition {
      condition     = self.public_ip != ""
      error_message = "Instance must have a public IP."
    }
  }
}
```

### Import Blocks (1.5+)

```hcl
# Import existing resources declaratively
import {
  to = aws_s3_bucket.legacy
  id = "my-existing-bucket"
}

resource "aws_s3_bucket" "legacy" {
  bucket = "my-existing-bucket"
  # Configuration must match existing resource
}
```

### Removed Blocks (1.7+)

```hcl
# Safely remove from state without destroying
removed {
  from = aws_instance.deprecated

  lifecycle {
    destroy = false  # Keep the actual resource
  }
}
```

---

## Security & Compliance Essentials

### Pre-Commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.96.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
        args:
          - --args=--config=__GIT_WORKING_DIR__/.tflint.hcl
      - id: terraform_trivy
      - id: terraform_checkov
        args:
          - --args=--quiet
          - --args=--skip-check CKV_AWS_123,CKV_AWS_456
      - id: terraform_docs
        args:
          - --args=--config=.terraform-docs.yml
```

### Security Scanning Tools

| Tool | Focus | Speed | CI Integration |
|------|-------|-------|----------------|
| **Trivy** | Misconfigurations, CVEs | Fast | Excellent |
| **Checkov** | Policy as code | Medium | Excellent |
| **tfsec** | Security issues | Fast | Good |
| **Terrascan** | Compliance | Medium | Good |
| **Snyk IaC** | Security + license | Medium | Excellent |

### State Security

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "myorg-terraform-state"
    key            = "prod/infrastructure/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true                    # Always encrypt
    dynamodb_table = "terraform-state-lock"  # Always use locking
    
    # Least privilege access
    role_arn       = "arn:aws:iam::123456789:role/TerraformStateAccess"
  }
}
```

### Secrets Management

```hcl
# ❌ NEVER hardcode secrets
resource "aws_db_instance" "main" {
  password = "mysecretpassword"  # Stored in state!
}

# ✅ Use external secret management
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/db/password"
}

resource "aws_db_instance" "main" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}

# ✅ Or use ephemeral variables (1.10+)
variable "db_password" {
  type      = string
  ephemeral = true  # Never written to state
}
```

---

## Version Management Strategy

### Version Constraints

```hcl
# versions.tf
terraform {
  required_version = ">= 1.6.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # Allows 5.x, prevents 6.0
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0.0, < 4.0.0"
    }
  }
}
```

### Constraint Syntax

| Constraint | Meaning | Example |
|------------|---------|---------|
| `= 1.0.0` | Exact version | Lock to specific |
| `!= 1.0.0` | Exclude version | Avoid buggy release |
| `> 1.0.0` | Greater than | Minimum boundary |
| `>= 1.0.0` | Greater or equal | Inclusive minimum |
| `< 2.0.0` | Less than | Maximum boundary |
| `~> 1.0` | Pessimistic (minor) | 1.x only |
| `~> 1.0.0` | Pessimistic (patch) | 1.0.x only |

### Upgrade Strategy

```bash
# 1. Check for updates
terraform init -upgrade

# 2. Review changes
terraform plan

# 3. Update .terraform.lock.hcl
terraform providers lock \
  -platform=linux_amd64 \
  -platform=darwin_amd64 \
  -platform=darwin_arm64

# 4. Commit lock file
git add .terraform.lock.hcl
git commit -m "chore: upgrade provider versions"
```

---

## Quick Reference Commands

```bash
# Formatting
terraform fmt -recursive

# Validation
terraform validate

# Planning
terraform plan -out=tfplan
terraform show -json tfplan | jq '.resource_changes'

# Testing (1.6+)
terraform test
terraform test -filter=tests/basic.tftest.hcl

# State inspection
terraform state list
terraform state show aws_instance.web
terraform state mv aws_instance.old aws_instance.new

# Import (declarative with 1.5+)
terraform plan -generate-config-out=generated.tf

# Debugging
TF_LOG=DEBUG terraform apply
terraform console
```

---

## References

- `references/testing-frameworks.md` - Native tests, Terratest, mocking strategies
- `references/module-patterns.md` - Variable/output best practices, DO vs DON'T
- `references/ci-cd-workflows.md` - GitHub Actions, GitLab CI, cost optimization
- `references/security-compliance.md` - Trivy, Checkov, secrets, state security

---

## Checklist Before Apply

- [ ] `terraform fmt` - Code formatted
- [ ] `terraform validate` - Syntax valid
- [ ] `terraform test` - Tests passing
- [ ] Security scan clean (trivy/checkov)
- [ ] Variables documented with descriptions
- [ ] Outputs defined for downstream consumers
- [ ] Version constraints in versions.tf
- [ ] State backend configured with encryption + locking
- [ ] No hardcoded secrets
- [ ] README.md updated (terraform-docs)
