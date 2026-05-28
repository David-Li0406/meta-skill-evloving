---
name: devops-infrastructure
description: Use this skill when you need to provision cloud infrastructure and local development environments using Infrastructure as Code (IaC) best practices across multiple cloud providers.
---

# Skill body

## Quick Start

### Terraform (AWS)

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "ap-northeast-1"
  }
}

provider "aws" {
  region = "ap-northeast-1"
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "my-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["ap-northeast-1a", "ap-northeast-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
}
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: app
          image: my-app:latest
          ports:
            - containerPort: 8080
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
```

## Infrastructure Design Principles

1. **Infrastructure as Code**: Manage all resources through code.
2. **Immutability**: Changes are made by recreating resources.
3. **Redundancy**: Distribute across multiple availability zones and regions.
4. **Least Privilege**: IAM roles should have the minimum necessary permissions.
5. **Observability**: Implement metrics, logging, and tracing.

## Workflow: New Infrastructure Setup

```
Progress Checklist:
- [ ] 1. Define requirements (availability, scalability, budget)
- [ ] 2. Design architecture
- [ ] 3. Create Terraform code
- [ ] 4. Execute and review plan
- [ ] 5. Deploy to staging environment
- [ ] 6. Set up monitoring and alerts
- [ ] 7. Deploy to production environment
- [ ] 8. Create documentation
```

## Environment Configuration

### Environment Configuration Matrix

| Aspect | Development | Staging | Production |
|--------|-------------|---------|------------|
| **Resources** | Local services, dependencies | Cloud resources | Cloud resources |
| **Reproducibility** | Docker Compose, setup scripts | IaC modules | IaC modules |
| **Security** | Secrets management, least privilege | Network isolation | Network isolation |
| **Documentation** | Variable descriptions, README | Variable descriptions, README | Variable descriptions, README |
| **Local Development** | Docker Compose, env templates | N/A | N/A |

## Utility Scripts

```bash
# Terraform cost estimation
python scripts/estimate_cost.py terraform.tfplan

# Kubernetes resource analysis
python scripts/analyze_k8s.py deployment.yaml

# Security scan
python scripts/security_scan.py --provider aws
```