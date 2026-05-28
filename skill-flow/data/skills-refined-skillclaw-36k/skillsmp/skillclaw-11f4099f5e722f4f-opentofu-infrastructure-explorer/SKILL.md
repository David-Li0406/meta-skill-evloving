---
name: opentofu-infrastructure-explorer
description: Use this skill when you need to explore and manage cloud infrastructure resources, including AWS and Kubernetes, using OpenTofu/Terraform.
---

# OpenTofu Infrastructure Explorer

## What I do

I guide you through managing cloud infrastructure resources using OpenTofu/Terraform for both AWS and Kubernetes. I help you:

- **AWS Management**: Manage EC2, Lambda, ECS, VPCs, S3, RDS, IAM, and more.
- **Kubernetes Management**: Deploy and manage Kubernetes clusters, pods, services, and Helm charts.
- **Best Practices**: Follow AWS Well-Architected Framework and Kubernetes documentation patterns.

## When to use me

Use this skill when you need to:
- Provision cloud infrastructure as code for AWS and Kubernetes.
- Automate resource creation and management across AWS and Kubernetes environments.
- Implement secure networking and VPC configurations for AWS.
- Manage Kubernetes configurations, including ConfigMaps and Secrets.
- Deploy applications to Kubernetes clusters and manage multi-cluster deployments.
- Follow best practices for both AWS and Kubernetes environments.

**Note**: OpenTofu and Terraform are used interchangeably throughout this skill. OpenTofu is an open-source implementation of Terraform and maintains full compatibility with Terraform providers.

## Prerequisites

- **OpenTofu CLI installed**: Install from https://opentofu.org/docs/intro/install/
- **AWS Account**: Valid AWS account with appropriate permissions.
- **AWS Credentials**: Access keys or IAM role for authentication.
- **Kubernetes Cluster**: Running Kubernetes cluster (EKS, GKE, AKS, or self-managed).
- **kubectl**: Kubernetes command-line tool for local testing.
- **Basic Knowledge**: Understanding of AWS services and Kubernetes concepts.

## Provider Documentation

- **Terraform Registry (AWS Provider)**: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- **Terraform Registry (Kubernetes Provider)**: https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs
- **AWS Well-Architected Framework**: https://docs.aws.amazon.com/wellarchitected/
- **Kubernetes Documentation**: https://kubernetes.io/docs/

## Steps

### Step 1: Install and Configure OpenTofu

```bash
# Verify OpenTofu installation
tofu version

# Initialize project for AWS
mkdir aws-terraform
cd aws-terraform
tofu init
```

### Step 2: Configure AWS Provider

Create `versions.tf` for AWS:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0.0"
    }
  }
  required_version = ">= 1.0"

  # Remote state backend
  backend "s3" {
    bucket         = "your-s3-bucket"
    key            = "terraform/state"
    region         = "us-west-2"
  }
}
```

### Step 3: Initialize Project for Kubernetes

```bash
# Initialize project for Kubernetes
mkdir kubernetes-terraform
cd kubernetes-terraform
tofu init
```

### Step 4: Configure Kubernetes Provider

Create `versions.tf` for Kubernetes:

```hcl
terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.24.0"
    }
  }
  required_version = ">= 1.0"
}
```