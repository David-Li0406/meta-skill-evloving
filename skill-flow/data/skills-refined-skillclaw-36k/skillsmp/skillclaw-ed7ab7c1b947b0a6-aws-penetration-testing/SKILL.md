---
name: aws-penetration-testing
description: Use this skill when you need to perform penetration testing on AWS environments, including IAM enumeration, privilege escalation, and exploitation of cloud resources.
---

# AWS Penetration Testing

## Purpose

Provide comprehensive techniques for penetration testing AWS cloud environments. This skill covers IAM enumeration, privilege escalation, SSRF to metadata endpoint, S3 bucket exploitation, Lambda code extraction, and persistence techniques for red team operations.

## Inputs/Prerequisites

- AWS CLI configured with credentials
- Valid AWS credentials (even low-privilege)
- Understanding of AWS IAM model
- Python 3, boto3 library
- Tools: Pacu, Prowler, ScoutSuite, SkyArk

## Outputs/Deliverables

- IAM privilege escalation paths
- Extracted credentials and secrets
- Compromised EC2/Lambda/S3 resources
- Persistence mechanisms
- Security audit findings

## Essential Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| Pacu | AWS exploitation framework | `git clone https://github.com/RhinoSecurityLabs/pacu` |
| SkyArk | Shadow Admin discovery | `Import-Module .\SkyArk.ps1` |
| Prowler | Security auditing | `pip install prowler` |
| ScoutSuite | Multi-cloud auditing | `pip install scoutsuite` |
| enumerate-iam | Permission enumeration | `git clone https://github.com/andresriancho/enumerate-iam` |
| Principal Mapper | IAM analysis | `pip install principalmapper` |

## Core Workflow

### Step 1: Initial Enumeration

Identify the compromised identity and permissions:

```bash
# Check current identity
aws sts get-caller-identity

# Configure profile
aws configure --profile compromised

# List access keys
aws iam list-access-keys

# Enumerate permissions
./enumerate-iam.py --access-key AKIA... --secret-key StF0q...
```

### Step 2: IAM Enumeration

```bash
# List all users
aws iam list-users

# List groups for user
aws iam list-groups-for-user --user-name TARGET_USER

# List attached policies
aws iam list-attached-user-policies --user-name TARGET_USER

# List inline policies
aws iam list-user-policies --user-name TARGET_USER

# Get policy details
aws iam get-policy --policy-arn POLICY_ARN
aws iam get-policy-version --policy-arn POLICY_ARN --version-id v1

# List roles
aws iam list-roles
aws iam list-attached-role-policies --role-name ROLE_NAME
```

### Step 3: Metadata SSRF

# Additional steps for SSRF and Lambda exploitation can be added here.