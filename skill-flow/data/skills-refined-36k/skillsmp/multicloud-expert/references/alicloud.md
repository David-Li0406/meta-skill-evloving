# Alicloud Patterns & Knowledge

## Table of Contents
- [Core Concepts](#core-concepts)
- [RAM (IAM)](#ram-iam)
- [SDK Patterns](#sdk-patterns)
- [Gotchas & Debugging](#gotchas--debugging)

## Core Concepts

### Resource Model
Resources identified by **Alibaba Cloud Resource Names (ARN)**:
```
acs:<service>:<region>:<account-id>:<resource-type>/<resource-id>
acs:ecs:eu-west-1:123456789:instance/i-abc123
```

### Resource Directory
Multi-account structure:
```
Resource Directory (Master Account)
  └── Folder
        └── Member Account
```

### Regions
| Location | Code | Notes |
|----------|------|-------|
| London | eu-west-1 | |
| Frankfurt | eu-central-1 | |
| Singapore | ap-southeast-1 | |
| China regions | cn-* | Separate account required |

**Note:** China regions use different endpoints and require separate account/credentials.

## RAM (IAM)

### Policy Syntax
AWS-style JSON:
```json
{
  "Version": "1",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["ecs:Describe*", "ecs:List*"],
    "Resource": "*",
    "Condition": {
      "StringEquals": { "acs:SourceVpc": "vpc-xxx" }
    }
  }]
}
```

### Principal Types
| Principal | Format | Use Case |
|-----------|--------|----------|
| RAM User | User in account | Human/service access |
| RAM Role | Assumable identity | Cross-account, apps |
| Service Role | `servicename.aliyuncs.com` | Alicloud service |

### Cross-Account Access
```json
{
  "Version": "1",
  "Statement": [{
    "Effect": "Allow",
    "Action": "sts:AssumeRole",
    "Principal": {
      "RAM": ["acs:ram::TRUSTED_ACCOUNT_ID:root"]
    }
  }]
}
```

### Service-Linked Roles
Auto-created by services. Prefix: `AliyunServiceRoleFor*`

## SDK Patterns

### Go SDK
```go
import (
    "github.com/aliyun/alibaba-cloud-sdk-go/services/ecs"
)

client, _ := ecs.NewClientWithAccessKey("eu-west-1", accessKeyID, accessKeySecret)

// With assume role
client, _ := ecs.NewClientWithRamRoleArn("eu-west-1", accessKeyID, accessKeySecret,
    roleArn, roleSessionName)

// Pagination
request := ecs.CreateDescribeInstancesRequest()
request.PageSize = "100"
request.PageNumber = "1"
for {
    response, _ := client.DescribeInstances(request)
    // process response.Instances.Instance
    if len(response.Instances.Instance) < 100 { break }
    pageNum++
    request.PageNumber = fmt.Sprintf("%d", pageNum)
}
```

### Python SDK
```python
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest

client = AcsClient(access_key_id, access_key_secret, 'eu-west-1')

# With STS assume role
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
# ... assume role, use returned credentials

request = DescribeInstancesRequest.DescribeInstancesRequest()
request.set_PageSize(100)
response = client.do_action_with_exception(request)
```

## Gotchas & Debugging

| Issue | Cause | Fix |
|-------|-------|-----|
| `Forbidden.RAM` | Missing permission | Check RAM policy |
| `InvalidAccessKeyId` | Wrong or deactivated key | Verify in console |
| AssumeRole fails | Trust policy wrong | Check Principal in role |
| Region unavailable | Not all services everywhere | Check availability matrix |
| Throttled | Rate limit | Backoff, check `x-acs-request-id` |

### Rate Limits
- Per-account, per-API (AWS-style model)
- ECS: ~100 req/sec for Describe* operations
- Throttling returns HTTP 403 with error code

### Useful CLI Commands
```bash
# Configure CLI
aliyun configure

# Who am I?
aliyun sts GetCallerIdentity

# List instances
aliyun ecs DescribeInstances --RegionId eu-west-1
```
