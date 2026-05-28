# AWS Patterns & Knowledge

## Table of Contents
- [Core Concepts](#core-concepts)
- [IAM & Security](#iam--security)
- [SDK Patterns (Go/Python)](#sdk-patterns)
- [Organisations & SCPs](#organisations--scps)
- [Common Services](#common-services)
- [Gotchas & Debugging](#gotchas--debugging)

## Core Concepts

### Resource Model
Everything is a **resource** with an **ARN** (Amazon Resource Name):
```
arn:aws:service:region:account-id:resource-type/resource-id
arn:aws:s3:::my-bucket                    # Global service (no region/account)
arn:aws:ec2:eu-west-2:123456789012:instance/i-abc123
```

### Control Plane vs Data Plane
- **Control plane:** Management operations (CreateBucket, DescribeInstances)
- **Data plane:** Content operations (PutObject, reading from DynamoDB)

Different endpoints, auth models, and rate limits.

### Regions & Availability Zones
- **Region:** Geographic area (eu-west-2 = London)
- **AZ:** Isolated data centre within region (eu-west-2a, eu-west-2b)
- Some services are **global** (IAM, Route53, CloudFront)

## IAM & Security

### Principal Types
| Principal | Format | Use Case |
|-----------|--------|----------|
| IAM User | `arn:aws:iam::123456789012:user/name` | Human access (discouraged for apps) |
| IAM Role | `arn:aws:iam::123456789012:role/name` | Apps, cross-account, federation |
| Service | `service.amazonaws.com` | AWS service acting on your behalf |
| Federated | `arn:aws:sts::123456789012:federated-user/name` | External IdP users |

### Policy Evaluation Logic
1. Explicit **Deny** → DENY
2. **SCP** allows? (if in org) → If no, DENY
3. **Resource policy** allows? → If yes for some ops, ALLOW
4. **Identity policy** allows? → If yes, ALLOW
5. Default → DENY

### Cross-Account Access Pattern
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "AWS": "arn:aws:iam::EXTERNAL_ACCOUNT:root" },
    "Action": "sts:AssumeRole",
    "Condition": {
      "StringEquals": { "sts:ExternalId": "unique-id-here" }
    }
  }]
}
```

**Always use ExternalId** for third-party access to prevent confused deputy attacks.

### Service-Linked Roles
Auto-created by services. Can't modify permissions. Common ones:
- `AWSServiceRoleForOrganizations`
- `AWSServiceRoleForConfig`
- `AWSServiceRoleForSecurityHub`
- `AWSServiceRoleForAutoScaling`

## SDK Patterns

### Go SDK (aws-sdk-go-v2)

**Basic client setup:**
```go
import (
    "context"
    "github.com/aws/aws-sdk-go-v2/config"
    "github.com/aws/aws-sdk-go-v2/service/ec2"
)

cfg, err := config.LoadDefaultConfig(context.TODO(),
    config.WithRegion("eu-west-2"),
)
client := ec2.NewFromConfig(cfg)
```

**Assume role:**
```go
import "github.com/aws/aws-sdk-go-v2/credentials/stscreds"

stsClient := sts.NewFromConfig(cfg)
creds := stscreds.NewAssumeRoleProvider(stsClient, roleARN,
    func(o *stscreds.AssumeRoleOptions) {
        o.ExternalID = aws.String(externalID)
    },
)
cfg.Credentials = aws.NewCredentialsCache(creds)
```

**Pagination:**
```go
paginator := ec2.NewDescribeInstancesPaginator(client, &ec2.DescribeInstancesInput{})
for paginator.HasMorePages() {
    page, err := paginator.NextPage(context.TODO())
    if err != nil { return err }
    for _, reservation := range page.Reservations {
        for _, instance := range reservation.Instances {
            // process instance
        }
    }
}
```

### Python SDK (boto3)

**Basic setup:**
```python
import boto3

client = boto3.client('ec2', region_name='eu-west-2')
# or with assumed role
sts = boto3.client('sts')
creds = sts.assume_role(RoleArn=role_arn, ExternalId=external_id, RoleSessionName='session')
client = boto3.client('ec2',
    aws_access_key_id=creds['Credentials']['AccessKeyId'],
    aws_secret_access_key=creds['Credentials']['SecretAccessKey'],
    aws_session_token=creds['Credentials']['SessionToken'],
)
```

**Pagination:**
```python
paginator = client.get_paginator('describe_instances')
for page in paginator.paginate():
    for reservation in page['Reservations']:
        for instance in reservation['Instances']:
            # process instance
```

**Retry configuration:**
```python
from botocore.config import Config

config = Config(
    retries={'max_attempts': 10, 'mode': 'adaptive'}
)
client = boto3.client('ec2', config=config)
```

## Organisations & SCPs

### Hierarchy
```
Organisation Root
  └── OU (Organisational Unit)
        └── Account
```

### SCP Behaviour
- **Deny by default** at each level
- Child cannot grant what parent denies
- **Management account is exempt** from SCPs (don't put it in an OU)

### Common SCP Pattern (Region Restriction)
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "DenyNonUKRegions",
    "Effect": "Deny",
    "Action": "*",
    "Resource": "*",
    "Condition": {
      "StringNotEquals": {
        "aws:RequestedRegion": ["eu-west-1", "eu-west-2"]
      }
    }
  }]
}
```

## Common Services

### S3 Quirks
- **Bucket names are globally unique** across all AWS accounts
- **Eventual consistency** for overwrite PUTS and DELETES (usually milliseconds now)
- **Bucket policies** can override IAM (and vice versa — both must allow)
- `bucket-owner-full-control` ACL needed for cross-account writes

### EC2 Quirks
- **Instance metadata:** `http://169.254.169.254/latest/meta-data/`
- **IMDSv2** requires token (more secure): `TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")`
- **Spot instances** can be interrupted with 2-minute warning

### Lambda Quirks
- **Cold starts:** First invocation slower (especially VPC-attached)
- **15-minute timeout** maximum
- **Execution role** must have permissions for any AWS services called

## Gotchas & Debugging

| Issue | Cause | Fix |
|-------|-------|-----|
| `AccessDenied` despite policy | Resource policy denying | Check S3/KMS/SQS resource policy |
| IAM changes not working | Propagation delay | Wait 10-60 seconds |
| `MalformedPolicyDocument` | Invalid principal format | Use `AWS` not `Service` for accounts |
| Cross-account S3 403 | Bucket owner enforcement | Add `bucket-owner-full-control` ACL |
| AssumeRole fails silently | Missing ExternalId | Check trust policy conditions |
| `InvalidParameterValue` | Wrong resource ID format | Check ARN vs ID vs name expected |

### Rate Limits
**Per-account limits** (good for parallel multi-account scanning):
- EC2 Describe*: ~100 requests/second (varies by call)
- S3 control plane: 3,500 PUT/POST, 5,500 GET per prefix
- IAM: 20 requests/second
- STS AssumeRole: 20 requests/second (but can burst higher)

### Useful CLI Commands
```bash
# Who am I?
aws sts get-caller-identity

# Simulate policy
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:role/MyRole \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::my-bucket/*

# Decode authorization error message
aws sts decode-authorization-message --encoded-message <message>
```
