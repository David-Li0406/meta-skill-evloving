---
name: building-terraform-modules
description: Use this skill when you need to create reusable Terraform modules based on user specifications, generate Terraform configurations, or structure infrastructure as code using Terraform.
---

# Skill body

## Overview

This skill allows Claude to efficiently generate Terraform modules, streamlining infrastructure-as-code development. By utilizing the terraform-module-builder plugin, it ensures modules are production-ready, well-documented, and incorporate best practices.

## How It Works

1. **Receiving User Request**: Claude receives a request to create a Terraform module, including details about the module's purpose and desired features.
2. **Generating Module Structure**: Claude invokes the terraform-module-builder plugin to create the basic file structure and configuration files for the module.
3. **Customizing Module Content**: Claude uses the user's specifications to populate the module with variables, outputs, and resource definitions, ensuring best practices are followed.

## When to Use This Skill

This skill activates when you need to:
- Create a new Terraform module from scratch.
- Generate production-ready Terraform configuration files.
- Implement infrastructure as code using Terraform modules.

## Examples

### Example 1: Creating a VPC Module

User request: "Create a Terraform module for a VPC with public and private subnets, a NAT gateway, and appropriate security groups."

The skill will:
1. Invoke the terraform-module-builder plugin to generate a basic VPC module structure.
2. Populate the module with Terraform code to define the VPC, subnets, NAT gateway, and security groups based on best practices.

### Example 2: Generating an S3 Bucket Module

User request: "Generate a Terraform module for an S3 bucket with versioning enabled, encryption at rest, and a lifecycle policy for deleting objects after 30 days."

The skill will:
1. Invoke the terraform-module-builder plugin to create a basic S3 bucket module structure.
2. Populate the module with Terraform code to define the S3 bucket with the specified features.