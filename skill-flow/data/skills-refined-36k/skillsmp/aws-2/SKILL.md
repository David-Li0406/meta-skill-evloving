---
name: aws
description: "AWS infrastructure security review process. Use when reviewing IAM policies and roles, auditing S3 bucket configurations, securing Lambda functions, reviewing CloudFormation/CDK/Terraform, or configuring VPC and security groups. Also use when IAM policies use wildcards, S3 buckets might be public, Lambda has broad permissions, security groups allow 0.0.0.0/0, or secrets appear in environment variables. Essential for KMS encryption, Secrets Manager, least privilege, and AWS security scanning with Prowler or Checkov."
---

# AWS Skill

## Overview

AWS's shared responsibility model means security is YOUR job, not Amazon's. This skill guides systematic review of AWS infrastructure for security misconfigurations—the #1 cause of cloud breaches.

**Core principle:** Default deny everything. AWS resources should have no access unless explicitly granted, no network exposure unless required, and no permissions beyond the minimum needed.

## The AWS Security Review Process

### Phase 1: Check IAM First

**IAM is the foundation. Start here:**

1. **Review Permission Scope**
   - What actions are allowed?
   - On which resources?
   - Under what conditions?

2. **Check for Privilege Escalation Paths**
   - Can this role create other roles?
   - Can it modify IAM policies?
   - Can it assume more powerful roles?

3. **Verify Least Privilege**
   - Are permissions minimal for the task?
   - Time-bounded where possible?
   - Conditions restricting access?

### Phase 2: Check Network Boundaries

**Then verify network isolation:**

1. **Security Groups**
   - No 0.0.0.0/0 ingress except ALB port 443
   - No overly broad port ranges
   - Source restricted to specific security groups

2. **VPC Design**
   - Private subnets for workloads?
   - NAT Gateway for outbound only?
   - VPC Flow Logs enabled?

3. **Public Exposure**
   - No public IPs on EC2 instances
   - No publicly accessible RDS
   - S3 public access blocked

### Phase 3: Check Data Protection

**Finally, verify data security:**

1. **Encryption**
   - Encryption at rest (KMS)?
   - Encryption in transit (TLS)?
   - Customer-managed keys for sensitive data?

2. **Secrets Management**
   - Secrets in Secrets Manager?
   - Not in environment variables?
   - Rotatable without deploy?

## Red Flags - STOP and Investigate

### IAM Red Flags

```json
// ❌ CRITICAL: Full admin
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}

// ❌ HIGH: IAM modification (privilege escalation)
{
  "Action": ["iam:*", "iam:CreateRole", "iam:AttachRolePolicy"]
}

// ❌ HIGH: No resource restriction
{
  "Action": "s3:*",
  "Resource": "*"  // Should be specific bucket ARN
}

// ❌ MEDIUM: No conditions
{
  "Action": "s3:GetObject"
  // Missing: Condition for IP, MFA, time bounds
}
```

### S3 Red Flags

```json
// ❌ CRITICAL: Public bucket
{
  "Effect": "Allow",
  "Principal": "*",  // Anyone on internet!
  "Action": "s3:GetObject"
}

// ❌ HIGH: Missing encryption
// (No ServerSideEncryptionConfiguration)

// ❌ HIGH: No public access block
// (PublicAccessBlockConfiguration missing or false)
```

### Network Red Flags

```yaml
# ❌ CRITICAL: SSH from anywhere
SecurityGroupIngress:
  - IpProtocol: tcp
    FromPort: 22
    ToPort: 22
    CidrIp: 0.0.0.0/0

# ❌ CRITICAL: All ports open
  - IpProtocol: -1
    CidrIp: 0.0.0.0/0

# ❌ HIGH: RDS publicly accessible
PubliclyAccessible: true
```

### Lambda Red Flags

```yaml
# ❌ HIGH: Hardcoded secrets
Environment:
  Variables:
    API_KEY: "sk-live-actual-secret-key"

# ❌ HIGH: Broad permissions
Policies:
  - AmazonS3FullAccess  # Should be specific bucket

# ❌ MEDIUM: No VPC (if accessing private resources)
# Missing VpcConfig
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "It's only internal" | VPCs get compromised. Defense in depth. |
| "We'll lock it down later" | Later never comes. Secure from day one. |
| "The app needs those permissions" | No app needs `*`. Find exact permissions. |
| "Public bucket is intentional" | Use CloudFront + OAI. Never direct S3. |
| "SSH access is for debugging" | Use SSM Session Manager. No SSH needed. |
| "Secrets are encrypted in Lambda" | They're visible in console. Use Secrets Manager. |

## AWS Security Checklist

Before approving AWS infrastructure:

**IAM:**
- [ ] No `Action: "*"` or `Resource: "*"`
- [ ] MFA required for sensitive operations
- [ ] Service roles follow least privilege
- [ ] No inline policies on users
- [ ] Conditions used where appropriate

**S3:**
- [ ] Public access blocked
- [ ] Encryption enabled (SSE-KMS preferred)
- [ ] Versioning enabled for critical data
- [ ] Access logging enabled

**Network:**
- [ ] No 0.0.0.0/0 except ALB 443
- [ ] Private subnets for workloads
- [ ] VPC Flow Logs enabled
- [ ] No public IPs on compute

**Compute:**
- [ ] No hardcoded secrets
- [ ] Least privilege roles
- [ ] Timeouts and concurrency limits

## Quick Patterns

### Secure IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3ReadWrite",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-specific-bucket/*",
      "Condition": {
        "StringEquals": {
          "aws:PrincipalAccount": "123456789012"
        },
        "IpAddress": {
          "aws:SourceIp": ["10.0.0.0/8"]
        }
      }
    }
  ]
}
```

### Secure S3 Bucket

```yaml
SecureBucket:
  Type: AWS::S3::Bucket
  Properties:
    BucketEncryption:
      ServerSideEncryptionConfiguration:
        - ServerSideEncryptionByDefault:
            SSEAlgorithm: aws:kms
            KMSMasterKeyID: !Ref KMSKey
    PublicAccessBlockConfiguration:
      BlockPublicAcls: true
      BlockPublicPolicy: true
      IgnorePublicAcls: true
      RestrictPublicBuckets: true
    VersioningConfiguration:
      Status: Enabled
    LoggingConfiguration:
      DestinationBucketName: !Ref LoggingBucket
```

### Secure Security Group

```yaml
AppSecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupDescription: Allow only from ALB
    VpcId: !Ref VPC
    SecurityGroupIngress:
      - IpProtocol: tcp
        FromPort: 443
        ToPort: 443
        SourceSecurityGroupId: !Ref ALBSecurityGroup
```

## Quick Security Scans

```bash
# AWS native tools
aws iam get-credential-report
aws s3api get-bucket-policy-status --bucket BUCKET
aws ec2 describe-security-groups --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]]'

# Third-party scanners
prowler aws                          # Comprehensive AWS audit
checkov -f template.yaml             # IaC scanning
cfn-lint template.yaml               # CloudFormation linting
tfsec .                              # Terraform scanning
```

## References

Detailed patterns and examples in `references/`:
- `iam-patterns.md` - Advanced IAM patterns and conditions
- `network-security.md` - VPC and security group patterns
- `encryption.md` - KMS and encryption patterns
