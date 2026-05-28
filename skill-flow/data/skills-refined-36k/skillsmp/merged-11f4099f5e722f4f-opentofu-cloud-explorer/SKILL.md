---
name: opentofu-cloud-explorer
description: Use this skill to explore and manage cloud infrastructure resources, including AWS and Kubernetes, using OpenTofu/Terraform.
---

# OpenTofu Cloud Explorer

## What I do

I guide you through managing cloud infrastructure resources using OpenTofu/Terraform. I help you:

- **AWS Management**: Provision and manage AWS resources such as EC2, S3, RDS, and VPCs.
- **Kubernetes Management**: Deploy and manage Kubernetes clusters, pods, services, and ingress controllers.
- **Resource Deployment**: Create and manage resources across both AWS and Kubernetes environments.
- **Best Practices**: Follow cloud architecture best practices and provider documentation.

## When to use me

Use this skill when you need to:
- Automate cloud infrastructure management as code.
- Provision AWS resources and Kubernetes clusters.
- Manage multi-tier architectures and containerized applications.
- Implement secure networking and resource configurations.
- Follow best practices for cloud governance and architecture.

**Note**: OpenTofu and Terraform are used interchangeably throughout this skill. OpenTofu is an open-source implementation of Terraform and maintains full compatibility with Terraform providers.

## Prerequisites

- **OpenTofu CLI installed**: Install from https://opentofu.org/docs/intro/install/
- **AWS Account**: Valid AWS account with appropriate permissions.
- **Kubernetes Cluster**: Running Kubernetes cluster (EKS, GKE, AKS, or self-managed).
- **kubectl**: Kubernetes command-line tool for local testing.
- **kubeconfig**: Valid Kubernetes configuration file.
- **AWS Credentials**: Access keys or IAM role for authentication.
- **Basic Cloud Knowledge**: Understanding of AWS services, Kubernetes concepts, and cloud infrastructure.

## Provider Documentation

- **Terraform Registry (AWS Provider)**: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- **Terraform Registry (Kubernetes Provider)**: https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs
- **AWS Documentation**: https://docs.aws.amazon.com/
- **Kubernetes Documentation**: https://kubernetes.io/docs/
- **OpenTofu Documentation**: https://opentofu.org/docs/

## Steps

### Step 1: Install and Configure OpenTofu

```bash
# Verify OpenTofu installation
tofu version

# Initialize project
mkdir cloud-terraform
cd cloud-terraform
tofu init
```

### Step 2: Configure AWS Provider

Create `versions.tf`:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.24.0"
    }
  }
  required_version = ">= 1.0"

  # Remote state backend
  backend "s3" {
    bucket         = "terraform-state"
    key            = "cloud/terraform.tfstate"
    region         = "ap-southeast-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Step 3: Configure AWS Authentication

Create `provider.tf`:

```hcl
provider "aws" {
  region = var.aws_region

  # Method 1: Access Keys (environment variables)
  # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

  # Method 2: Shared Credentials File
  # ~/.aws/credentials with profiles

  # Method 3: IAM Role (recommended for production)
  # assume_role {
  #   role_arn = "arn:aws:iam::123456789012:role/TerraformRole"
  # }
}
```

### Step 4: Configure Kubernetes Provider

Create `kubernetes.tf`:

```hcl
provider "kubernetes" {
  config_path = var.kubeconfig_path
}
```

### Step 5: Create AWS Resources

Create `aws_resources.tf`:

```hcl
# Example: Create an S3 Bucket
resource "aws_s3_bucket" "data" {
  bucket_prefix = "${var.project_name}-data-"
  force_destroy = var.environment == "dev" ? true : false
}
```

### Step 6: Create Kubernetes Resources

Create `kubernetes_resources.tf`:

```hcl
# Example: Create a Kubernetes Deployment
resource "kubernetes_deployment" "app" {
  metadata {
    name      = var.application_name
    namespace = var.app_namespace
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = var.application_name
      }
    }

    template {
      metadata {
        labels = {
          app = var.application_name
        }
      }

      spec {
        container {
          name  = var.application_name
          image = var.container_image
        }
      }
    }
  }
}
```

### Step 7: Define Variables

Create `variables.tf`:

```hcl
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-1"
}

variable "kubeconfig_path" {
  description = "Path to kubeconfig file"
  type        = string
  default     = "~/.kube/config"
}

variable "project_name" {
  description = "Project name used for tagging"
  type        = string
}

variable "app_namespace" {
  description = "Application namespace"
  type        = string
  default     = "app"
}

variable "application_name" {
  description = "Application name"
  type        = string
}

variable "container_image" {
  description = "Container image to deploy"
  type        = string
}

variable "replicas" {
  description = "Number of replicas"
  type        = number
  default     = 3
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

### Step 8: Initialize and Apply

```bash
# Initialize providers
tofu init

# Plan changes
tofu plan -out=tfplan

# Apply changes
tofu apply tfplan

# Show outputs
tofu output
```

## Best Practices

### Security

1. **Least Privilege**: Grant minimal permissions in IAM roles and policies.
2. **Secrets Management**: Use Kubernetes Secrets for sensitive data.
3. **Network Policies**: Implement network policies for pod-to-pod communication.

### High Availability

1. **Multi-AZ Deployments**: Spread resources across availability zones in AWS.
2. **Replicas**: Deploy multiple replicas for critical applications in Kubernetes.

### Cost Optimization

1. **Right-Sizing**: Choose appropriate instance types and storage in AWS.
2. **Use Spot Instances**: For fault-tolerant workloads in AWS.

## Common Issues

### Issue: Provider Not Found

**Symptom**: Error `Error: Failed to query available provider packages`

**Solution**:
```bash
# Update provider versions
tofu init -upgrade
```

### Issue: Authentication Failed

**Symptom**: Error `Error: error configuring Terraform AWS Provider`

**Solution**:
```bash
# Verify credentials
aws sts get-caller-identity
```

### Issue: Pod Pending State

**Symptom**: Pods stuck in Pending state

**Solution**:
```bash
# Describe pod for details
kubectl describe pod <pod-name>
```

## Reference Documentation

- **Terraform Registry (AWS Provider)**: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- **Terraform Registry (Kubernetes Provider)**: https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs
- **AWS Documentation**: https://docs.aws.amazon.com/
- **Kubernetes Documentation**: https://kubernetes.io/docs/
- **OpenTofu Documentation**: https://opentofu.org/docs/

## Next Steps

After mastering this skill, explore:
- **Advanced AWS Services**: Learn about Lambda, ECS, and EKS.
- **Kubernetes Advanced**: Explore StatefulSets, DaemonSets, and Operators.