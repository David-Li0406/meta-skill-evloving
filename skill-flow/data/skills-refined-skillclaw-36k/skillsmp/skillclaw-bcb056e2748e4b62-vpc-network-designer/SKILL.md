---
name: vpc-network-designer
description: Use this skill when you need automated assistance with VPC network design tasks in AWS, including best practices and code generation.
---

# VPC Network Designer

## Overview

This skill provides automated assistance for VPC network designer tasks within the AWS Skills domain.

## When to Use

This skill activates automatically when you:
- Mention "vpc network designer" in your request
- Ask about VPC network design patterns or best practices
- Need help with AWS services related to compute, storage, networking, serverless, and AWS-specific best practices.

## Instructions

1. Provides step-by-step guidance for VPC network design.
2. Follows industry best practices and patterns.
3. Generates production-ready code and configurations.
4. Validates outputs against common standards.

## Examples

- **Request:** "Help me with VPC network designer"
  - **Result:** Provides step-by-step guidance and generates appropriate configurations.
- **Request:** "What are the best practices for VPC design?"
  - **Result:** Offers recommendations based on industry standards.

## Prerequisites

- Relevant development environment configured.
- Access to necessary tools and services.
- Basic understanding of AWS concepts.

## Output

- Generated configurations and code.
- Best practice recommendations.
- Validation results.

## Error Handling

| Error                  | Cause                          | Solution                                      |
|-----------------------|--------------------------------|-----------------------------------------------|
| Configuration invalid  | Missing required fields        | Check documentation for required parameters.  |
| Tool not found        | Dependency not installed       | Install required tools per prerequisites.    |
| Permission denied      | Insufficient access            | Verify credentials and permissions.           |

## Related Skills

Part of the **AWS Skills** skill category.  
Tags: aws, lambda, s3, ec2, cloudformation