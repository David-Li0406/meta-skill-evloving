# Infrastructure & Platform

Specific guidance for building infrastructure, platform tools, and DevOps capabilities.

## Product Requirements Focus

### Typical Personas
- **Platform Engineer**: Builds and maintains infrastructure
- **Developer**: Consumes platform capabilities
- **SRE/Operations**: Monitors and responds to incidents
- **Security Team**: Ensures compliance and security
- **Finance/Management**: Cares about costs and efficiency

### Key Questions to Ask
1. What environments need to be supported (dev, staging, prod)?
2. What compliance/regulatory requirements exist?
3. What's the team's infrastructure experience level?
4. Is multi-cloud/hybrid cloud a requirement?
5. What's the disaster recovery requirement (RTO/RPO)?

### Infrastructure-Specific User Stories

```markdown
**As a** developer
**I expect to** provision a new environment in minutes
**So that** I can start development without waiting for ops

**As a** platform engineer
**I expect to** enforce standards across all deployments
**So that** infrastructure is consistent and secure

**As an** SRE
**I expect to** see infrastructure changes before they apply
**So that** I can prevent outages from misconfigurations

**As a** security engineer
**I expect to** audit all infrastructure changes
**So that** I can ensure compliance

**As a** finance manager
**I expect to** see infrastructure costs by team/project
**So that** I can manage cloud spending
```

## Design Principles

### Infrastructure as Code (IaC) Best Practices

1. **Version Control**: All infrastructure in git
2. **Immutability**: Replace, don't modify
3. **Idempotency**: Same input = same output
4. **Modularity**: Reusable components
5. **Environment Parity**: Same code, different configs
6. **Least Privilege**: Minimal permissions
7. **Documentation as Code**: Self-documenting infrastructure

### Security Requirements

| Layer | Requirements |
|-------|-------------|
| **Network** | VPC isolation, security groups, NACLs |
| **Identity** | IAM roles, service accounts, RBAC |
| **Secrets** | Encrypted at rest, secret management |
| **Compute** | Hardened images, patching strategy |
| **Data** | Encryption, backup, retention |
| **Audit** | CloudTrail, audit logs, SIEM |

### Reliability Requirements

| Requirement | Description | Typical Target |
|-------------|-------------|----------------|
| **RTO** | Recovery Time Objective | < 4 hours |
| **RPO** | Recovery Point Objective | < 1 hour |
| **Availability** | Uptime percentage | 99.9% |
| **Durability** | Data preservation | 99.999999999% |

## Architecture Patterns

### Decision: IaC Tool Selection

| Tool | When to Use | Pros | Cons |
|------|-------------|------|------|
| **Terraform** | Multi-cloud, general purpose | Provider ecosystem, state management | HCL learning curve |
| **Pulumi** | Developers, complex logic | Real programming languages | Smaller ecosystem |
| **CloudFormation** | AWS-only, native integration | AWS native, no state management | AWS only, verbose |
| **CDK** | AWS + programming languages | Type safety, abstractions | AWS focus |
| **Crossplane** | Kubernetes-native | GitOps friendly, K8s native | Complexity |

### Environment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Production                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Region A  │  │   Region B  │  │   Region C  │             │
│  │   (Primary) │  │  (Failover) │  │    (DR)     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                          Staging                                 │
│  ┌─────────────┐                                                │
│  │   Region A  │  (Production-like, smaller scale)              │
│  └─────────────┘                                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        Development                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Dev 1     │  │   Dev 2     │  │   Dev N     │             │
│  │ (ephemeral) │  │ (ephemeral) │  │ (ephemeral) │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

### Module Structure (Terraform)

```
infrastructure/
├── modules/                    # Reusable modules
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── eks/
│   ├── rds/
│   └── security-group/
├── environments/               # Environment configurations
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── production/
├── global/                     # Global resources (IAM, DNS)
│   ├── iam/
│   └── route53/
└── scripts/                    # Helper scripts
    ├── init.sh
    └── apply.sh
```

## Interface Contracts

### Module Interface Contract

```hcl
# modules/vpc/variables.tf

variable "name" {
  description = "Name prefix for all VPC resources"
  type        = string

  validation {
    condition     = length(var.name) <= 20
    error_message = "Name must be 20 characters or less."
  }
}

variable "cidr_block" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.cidr_block, 0))
    error_message = "Must be a valid CIDR block."
  }
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)

  validation {
    condition     = length(var.availability_zones) >= 2
    error_message = "At least 2 availability zones required."
  }
}

variable "enable_nat_gateway" {
  description = "Enable NAT gateway for private subnets"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
```

```hcl
# modules/vpc/outputs.tf

output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = aws_subnet.private[*].id
}

output "nat_gateway_ips" {
  description = "Elastic IPs of NAT gateways"
  value       = aws_eip.nat[*].public_ip
}
```

### Configuration Schema

```yaml
# Environment configuration schema
$schema: http://json-schema.org/draft-07/schema#
title: Environment Configuration
type: object
required:
  - environment
  - region
  - vpc
properties:
  environment:
    type: string
    enum: [dev, staging, production]

  region:
    type: string
    pattern: "^[a-z]{2}-[a-z]+-\\d$"

  vpc:
    type: object
    required: [cidr_block]
    properties:
      cidr_block:
        type: string
      availability_zones:
        type: array
        items:
          type: string
        minItems: 2
      enable_nat_gateway:
        type: boolean
        default: true

  kubernetes:
    type: object
    properties:
      version:
        type: string
      node_groups:
        type: array
        items:
          type: object
          required: [name, instance_type, min_size, max_size]
          properties:
            name:
              type: string
            instance_type:
              type: string
            min_size:
              type: integer
              minimum: 0
            max_size:
              type: integer
              minimum: 1
```

## Testing Strategy

### Infrastructure Test Categories

| Category | Purpose | Tools |
|----------|---------|-------|
| **Static Analysis** | Syntax, security, best practices | tflint, tfsec, checkov |
| **Unit Tests** | Module behavior | Terratest, terraform test |
| **Integration Tests** | Actual resource creation | Terratest |
| **Compliance Tests** | Policy enforcement | OPA, Sentinel |
| **Drift Detection** | Detect manual changes | terraform plan |

### Static Analysis

```bash
# Terraform validation
terraform validate

# Linting
tflint --recursive

# Security scanning
tfsec .
checkov -d .

# Cost estimation
infracost breakdown --path .
```

### Module Testing (Terratest)

```go
// modules/vpc/test/vpc_test.go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestVPCModule(t *testing.T) {
    t.Parallel()

    terraformOptions := &terraform.Options{
        TerraformDir: "../",
        Vars: map[string]interface{}{
            "name":               "test-vpc",
            "cidr_block":         "10.0.0.0/16",
            "availability_zones": []string{"us-east-1a", "us-east-1b"},
        },
    }

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    vpcId := terraform.Output(t, terraformOptions, "vpc_id")
    assert.NotEmpty(t, vpcId)

    publicSubnets := terraform.OutputList(t, terraformOptions, "public_subnet_ids")
    assert.Len(t, publicSubnets, 2)

    privateSubnets := terraform.OutputList(t, terraformOptions, "private_subnet_ids")
    assert.Len(t, privateSubnets, 2)
}
```

### Policy Testing (OPA)

```rego
# policies/require_tags.rego
package terraform

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_instance"
    not resource.change.after.tags.Environment
    msg := sprintf("Instance %s must have Environment tag", [resource.address])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_instance"
    not resource.change.after.tags.Owner
    msg := sprintf("Instance %s must have Owner tag", [resource.address])
}
```

## Code Scaffolding

### Module Template

```hcl
# modules/MODULE_NAME/main.tf
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Resources here

# modules/MODULE_NAME/variables.tf
# Input variables with validation

# modules/MODULE_NAME/outputs.tf
# Output values

# modules/MODULE_NAME/versions.tf
# Provider version constraints

# modules/MODULE_NAME/README.md
# Module documentation
```

### Environment Template

```hcl
# environments/ENV_NAME/main.tf
terraform {
  required_version = ">= 1.0"

  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "env/ENV_NAME/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "terraform"
      Repository  = "infrastructure"
    }
  }
}

module "vpc" {
  source = "../../modules/vpc"

  name               = "${var.environment}-vpc"
  cidr_block         = var.vpc_cidr
  availability_zones = var.availability_zones
}
```

## GitOps Workflow

### CI/CD Pipeline

```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  pull_request:
    paths:
      - 'environments/**'
      - 'modules/**'
  push:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3

      - name: Terraform Format Check
        run: terraform fmt -check -recursive

      - name: Terraform Validate
        run: |
          for dir in environments/*/; do
            terraform -chdir=$dir init -backend=false
            terraform -chdir=$dir validate
          done

      - name: TFLint
        uses: terraform-linters/setup-tflint@v4
        run: tflint --recursive

      - name: Security Scan
        uses: aquasecurity/tfsec-action@v1.0.0

  plan:
    needs: validate
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, production]
    steps:
      - uses: actions/checkout@v4

      - name: Terraform Plan
        run: |
          cd environments/${{ matrix.environment }}
          terraform init
          terraform plan -out=tfplan

      - name: Upload Plan
        uses: actions/upload-artifact@v4
        with:
          name: plan-${{ matrix.environment }}
          path: environments/${{ matrix.environment }}/tfplan

  apply:
    needs: plan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production  # Requires approval
    steps:
      - name: Apply
        run: terraform apply -auto-approve tfplan
```

## Common Pitfalls to Avoid

1. **Hardcoded Values**: Use variables for everything environment-specific
2. **No State Locking**: Always use remote state with locking
3. **Secrets in Code**: Use secret management (Vault, AWS Secrets Manager)
4. **No Drift Detection**: Regular `terraform plan` to detect drift
5. **Monolithic State**: Split state by service/team/environment
6. **No Tagging Strategy**: Tags are crucial for cost allocation and management
7. **Ignoring Quotas**: Check service limits before scaling
8. **No Rollback Plan**: Know how to roll back failed changes
9. **Over-privileged IAM**: Apply least privilege principle
10. **No Documentation**: Document architecture decisions and runbooks

## Observability Setup

### Monitoring Infrastructure

```hcl
# Monitoring module
module "monitoring" {
  source = "./modules/monitoring"

  cloudwatch_log_groups = [
    "/aws/eks/cluster/logs",
    "/aws/rds/instance/logs"
  ]

  alarms = {
    high_cpu = {
      metric_name = "CPUUtilization"
      threshold   = 80
      period      = 300
    }
    low_disk = {
      metric_name = "DiskSpaceUtilization"
      threshold   = 90
      period      = 300
    }
  }

  dashboard_widgets = [
    "EC2 Overview",
    "RDS Metrics",
    "EKS Cluster Health"
  ]
}
```

### Runbook Template

```markdown
# Runbook: [Incident Type]

## Overview
Brief description of the incident type

## Detection
How is this incident typically detected?
- Alert: [Alert name]
- Dashboard: [Dashboard link]

## Impact
What's affected when this occurs?

## Diagnosis Steps
1. Check [metric/log]
2. Verify [service/component]
3. Review recent changes

## Resolution Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Escalation
- On-call: [contact]
- Subject matter expert: [contact]

## Post-Incident
- [ ] Update incident ticket
- [ ] Schedule post-mortem
- [ ] Create follow-up tasks
```
