---
name: generating-infrastructure-as-code
description: Use this skill when generating Infrastructure as Code (IaC) configurations for cloud infrastructure, specifying the platform (e.g., Terraform, CloudFormation) and cloud provider (e.g., AWS, Azure, GCP).
---

## Overview

This skill empowers Claude to automate the creation of infrastructure code, streamlining the deployment and management of cloud resources. It supports multiple IaC platforms and cloud providers, ensuring flexibility and best practices.

## How It Works

1. **Receiving Request**: Claude receives a request for IaC generation, identifying the desired platform and cloud provider.
2. **Invoking Plugin**: Claude invokes the infrastructure-as-code-generator plugin with the user's specifications.
3. **Generating Code**: The plugin generates the requested IaC configuration based on the user's requirements.
4. **Presenting Code**: Claude presents the generated IaC code to the user for review and deployment.

## When to Use This Skill

This skill activates when you need to:
- Generate Terraform configurations for AWS, GCP, or Azure.
- Create CloudFormation templates for AWS infrastructure.
- Develop Pulumi programs for multi-cloud deployments.
- Write ARM templates or CDK configurations.

## Examples

### Example 1: AWS ECS Fargate Infrastructure

User request: "Generate Terraform configuration for an AWS ECS Fargate cluster."

The skill will:
1. Invoke the infrastructure-as-code-generator plugin, specifying Terraform and AWS ECS Fargate.
2. Generate a Terraform configuration file defining the ECS cluster, task definition, and related resources.

### Example 2: Azure Resource Group Deployment

User request: "Create an ARM template for deploying an Azure Resource Group with a virtual network."

The skill will:
1. Invoke the infrastructure-as-code-generator plugin, specifying ARM template and Azure Resource Group.
2. Generate an ARM template defining the resource group and virtual network resources.

## Best Practices

- **Specificity**: Provide clear and specific requirements for the desired infrastructure.
- **Platform Selection**: Choose the appropriate IaC platform based on your cloud provider and organizational standards.
- **Review & Validation**: Always review and validate the generated IaC code before deploying it to production.

## Integration

This skill can be integrated with other Claude Code plugins for deployment automation, security scanning, and cost estimation, providing a comprehensive DevOps workflow. For example, it can be used with a deployment plugin to automatically deploy the generated infrastructure.

## Prerequisites

Before using this skill, ensure:
- Target cloud provider CLI is installed (aws-cli, gcloud, az).
- IaC tool is installed (Terraform, Pulumi, AWS CDK).
- Cloud credentials are configured locally.
- Understanding of target infrastructure architecture.
- Version control system for IaC storage.

## Output

Generates infrastructure as code files for various platforms, including:

**Terraform Example:**
```hcl
# {baseDir}/terraform/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  enable_dns_hostnames = true

  tags = {
    Name = "${var.project}-vpc"
    Environment = var.environment
  }
}
```

**CloudFormation Example:**
```yaml
# {baseDir}/cloudformation/template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Production VPC infrastructure

Parameters:
  VpcCidr:
    Type: String
    Default: 10.0.0.0/16

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref VpcCidr
      EnableDnsHostnames: true
```

**Pulumi Example:**
```typescript
// {baseDir}/pulumi/index.ts
import * as aws from "@pulumi/aws";

const vpc = new aws.ec2.Vpc("main", {
    cidrBlock: "10.0.0.0/16",
    enableDnsHostnames: true,
    tags: {
        Name: "production-vpc"
    }
});

export const vpcId = vpc.id;
```

## Error Handling

Common issues and solutions:

- **Syntax Errors**: Validate syntax with `terraform validate` or respective tool linter.
- **Provider Authentication**: Configure credentials via environment variables or CLI login.
- **Resource Conflicts**: Import existing resources or use data sources instead of creating new ones.
- **State Lock Issues**: Ensure no other process is running, or force unlock if safe.
- **Dependency Errors**: Check resource references and ensure proper dependency ordering.

## Resources

- Terraform documentation: https://www.terraform.io/docs/
- AWS CloudFormation guide: https://docs.aws.amazon.com/cloudformation/
- Pulumi documentation: https://www.pulumi.com/docs/
- Azure ARM templates: https://docs.microsoft.com/azure/azure-resource-manager/
- IaC best practices guide in {baseDir}/docs/iac-standards.md