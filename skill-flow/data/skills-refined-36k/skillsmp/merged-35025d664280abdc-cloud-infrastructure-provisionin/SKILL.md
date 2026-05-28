---
name: cloud-infrastructure-provisioning
description: Use this skill for provisioning cloud infrastructure and local development environments using Infrastructure as Code (IaC) practices across multiple cloud providers.
---

# Cloud Infrastructure Provisioning

## Overview

This skill focuses on provisioning cloud infrastructure and local development environments using Infrastructure as Code (IaC) principles. It covers Terraform, CloudFormation, and Pulumi for cloud resources, as well as Docker Compose for local setups.

## Quick Start

### Terraform (AWS Example)

```hcl
terraform {
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
  region = "<your-region>"
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "<your-vpc-name>"
  cidr = "<your-cidr-block>"
  
  azs             = ["<your-availability-zones>"]
  private_subnets = ["<your-private-subnets>"]
  public_subnets  = ["<your-public-subnets>"]
  
  enable_nat_gateway = true
}
```

### Docker Compose Example

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://<user>:<password>@db:5432/<db_name>
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: <user>
      POSTGRES_PASSWORD: <password>
      POSTGRES_DB: <db_name>
    ports:
      - "5432:5432"
```

## Infrastructure Design Principles

1. **Infrastructure as Code**: Manage all resources through code.
2. **Immutability**: Changes are made by recreating resources.
3. **Redundancy**: Distribute across multiple availability zones and regions.
4. **Least Privilege**: IAM roles should have the minimum necessary permissions.
5. **Observability**: Implement metrics, logging, and tracing.

## Detailed Guide

### Infrastructure Coverage

| Area | Scope |
|------|-------|
| **Cloud IaC** | Terraform modules, CloudFormation templates, Pulumi stacks |
| **Multi-cloud** | AWS, GCP, Azure resource definitions |
| **Containers** | Docker Compose for local dev, container orchestration configs |
| **Networking** | VPC, security groups, load balancers, DNS |
| **Database** | RDS, Cloud SQL, managed database configurations |

### Environment Configuration Matrix

| Aspect | Development | Staging | Production |
|--------|-------------|---------|------------|
| **Resource Size** | Minimum | Medium | Production spec |
| **Instance Count** | 1 | 2+ | Scale as needed |
| **Availability** | Single AZ | Multi-AZ | Multi-AZ + DR |
| **Backup** | None/manual | Daily | Continuous + PITR |
| **Monitoring** | Basic metrics | Detailed metrics | Detailed + alerts |

## Workflow: New Infrastructure Setup

```
Progress Checklist:
- [ ] 1. Define requirements (availability, scalability, budget)
- [ ] 2. Design architecture
- [ ] 3. Create IaC code
- [ ] 4. Execute and review plan
- [ ] 5. Deploy to staging environment
- [ ] 6. Set up monitoring and alerts
- [ ] 7. Deploy to production environment
- [ ] 8. Create documentation
```

## Security Best Practices

- **Secrets Management**: Use environment variables for local development and cloud secrets managers for production.
- **IAM Least Privilege**: Always grant the minimum required permissions.
- **Network Security**: Implement security groups and network isolation.

## Interaction Triggers

Use `AskUserQuestion` tool to confirm with the user at these decision points.

| Trigger | Timing | When to Ask |
|---------|--------|-------------|
| ON_CLOUD_PROVIDER | BEFORE_START | When selecting or confirming cloud provider |
| ON_ENVIRONMENT | ON_DECISION | When choosing target environment (dev/staging/prod) |

## Agent Collaboration

### Related Agents

| Agent | Collaboration |
|-------|--------------|
| **Gear** | Set up CI/CD pipelines after infrastructure is created. |
| **Sentinel** | Request security reviews for IAM policies and security groups. |

## Activity Logging (REQUIRED)

After completing your task, add a row to `.agents/PROJECT.md` Activity Log:
```
| YYYY-MM-DD | Scaffold | (action) | (files) | (outcome) |
```

## Output Language

All final outputs (reports, comments, etc.) must be written in Japanese.