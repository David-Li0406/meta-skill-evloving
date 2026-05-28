# SDK Debugging Patterns

## Table of Contents
- [Common Issues](#common-issues)
- [Authentication Debugging](#authentication-debugging)
- [Request/Response Debugging](#requestresponse-debugging)
- [Pagination Pitfalls](#pagination-pitfalls)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

## Common Issues

### The "It Works Locally" Checklist
When code works locally but fails in CI/production:

1. **Credentials source**
   - Local: CLI profile, env vars, cached tokens
   - CI: Instance role, service account, secrets injection
   - Check: Are credentials actually being found?

2. **Region/endpoint**
   - Local: Default region in config
   - CI: May need explicit setting
   - Check: Is the SDK hitting the right endpoint?

3. **Network path**
   - Local: Direct internet access
   - CI: VPC, proxy, firewall rules
   - Check: Can you reach the API endpoint?

4. **IAM context**
   - Local: Your user/role
   - CI: Service role (different permissions)
   - Check: Who is the SDK authenticating as?

## Authentication Debugging

### AWS SDK (Go)
```go
import (
    "github.com/aws/aws-sdk-go-v2/config"
    "github.com/aws/aws-sdk-go-v2/aws"
)

cfg, err := config.LoadDefaultConfig(context.TODO())
if err != nil {
    log.Fatalf("config error: %v", err)
}

// Check who we are
creds, err := cfg.Credentials.Retrieve(context.TODO())
if err != nil {
    log.Fatalf("credentials error: %v", err)
}
log.Printf("Access Key: %s", creds.AccessKeyID)
log.Printf("Source: %s", creds.Source)  // e.g., "EnvConfigCredentials", "IAMRoleCredentials"
```

### AWS SDK (Python)
```python
import boto3

session = boto3.Session()
credentials = session.get_credentials()
print(f"Access Key: {credentials.access_key}")
print(f"Method: {credentials.method}")  # e.g., 'env', 'iam-role', 'assume-role'

# Who am I?
sts = session.client('sts')
identity = sts.get_caller_identity()
print(f"ARN: {identity['Arn']}")
```

### Azure SDK (Go)
```go
import "github.com/Azure/azure-sdk-for-go/sdk/azidentity"

cred, err := azidentity.NewDefaultAzureCredential(&azidentity.DefaultAzureCredentialOptions{
    // Enable logging to see which credential is used
    ClientOptions: azcore.ClientOptions{
        Logging: policy.LogOptions{
            IncludeBody: true,
        },
    },
})
```

### Azure SDK (Python)
```python
from azure.identity import DefaultAzureCredential
import logging

# Enable credential chain logging
logging.getLogger('azure.identity').setLevel(logging.DEBUG)

credential = DefaultAzureCredential()
# Will show which credential in the chain succeeded
```

### GCP SDK (Go)
```go
import (
    "golang.org/x/oauth2/google"
    "google.golang.org/api/option"
)

// Find default credentials and inspect
creds, err := google.FindDefaultCredentials(context.Background(), "https://www.googleapis.com/auth/cloud-platform")
if err != nil {
    log.Fatalf("credentials error: %v", err)
}
log.Printf("Project: %s", creds.ProjectID)
// creds.JSON contains the key file if using service account
```

### GCP SDK (Python)
```python
import google.auth

credentials, project = google.auth.default()
print(f"Project: {project}")
print(f"Credential type: {type(credentials).__name__}")

# For service accounts
if hasattr(credentials, 'service_account_email'):
    print(f"Service Account: {credentials.service_account_email}")
```

## Request/Response Debugging

### AWS SDK (Go) - Enable Logging
```go
import (
    "github.com/aws/aws-sdk-go-v2/config"
    "github.com/aws/aws-sdk-go-v2/aws"
)

cfg, _ := config.LoadDefaultConfig(context.TODO(),
    config.WithClientLogMode(aws.LogRequestWithBody|aws.LogResponseWithBody),
)
```

### AWS SDK (Python) - Enable Logging
```python
import boto3
import logging

# Enable all boto3 logging
boto3.set_stream_logger('', logging.DEBUG)

# Or more targeted
boto3.set_stream_logger('botocore', logging.DEBUG)
```

### Azure SDK - HTTP Logging
```go
import "github.com/Azure/azure-sdk-for-go/sdk/azcore/policy"

clientOptions := &azcore.ClientOptions{
    Logging: policy.LogOptions{
        IncludeBody: true,
    },
}
```

```python
import logging
logging.getLogger('azure').setLevel(logging.DEBUG)
```

### GCP SDK - HTTP Logging
```go
import "google.golang.org/api/option"

// Use GODEBUG=http2debug=2 env var for HTTP/2 debugging
// Or use custom HTTP client with logging
```

```python
import httplib2
httplib2.debuglevel = 4
```

## Pagination Pitfalls

### Problem: Incomplete Results
Forgetting to paginate is the #1 cause of "missing resources."

**Wrong (only gets first page):**
```go
// Go - AWS
result, _ := client.DescribeInstances(context.TODO(), &ec2.DescribeInstancesInput{})
// Only processes first page!
```

```python
# Python - AWS
response = client.describe_instances()
# Only first page!
```

**Right:**
```go
// Go - AWS
paginator := ec2.NewDescribeInstancesPaginator(client, &ec2.DescribeInstancesInput{})
for paginator.HasMorePages() {
    page, _ := paginator.NextPage(context.TODO())
    // process page
}
```

```python
# Python - AWS
paginator = client.get_paginator('describe_instances')
for page in paginator.paginate():
    # process page
```

### Problem: Pagination Token Expiry
Some APIs have tokens that expire. If processing is slow, you may get errors mid-pagination.

**Mitigation:**
```python
# Collect all results first, then process
all_results = []
for page in paginator.paginate():
    all_results.extend(page['Items'])

# Now process (no risk of token expiry)
for item in all_results:
    expensive_operation(item)
```

### Problem: Modified Data During Pagination
Resources can be created/deleted while paginating.

**Reality check:** This is usually fine. For consistency-critical operations, use:
- AWS: Point-in-time queries where supported
- Azure: Resource Graph with consistent snapshot
- GCP: Cloud Asset Inventory exports

## Error Handling

### AWS Error Structure
```go
import "github.com/aws/smithy-go"

var apiErr smithy.APIError
if errors.As(err, &apiErr) {
    log.Printf("Code: %s", apiErr.ErrorCode())
    log.Printf("Message: %s", apiErr.ErrorMessage())
    
    // Check specific error
    var notFound *types.ResourceNotFoundException
    if errors.As(err, &notFound) {
        // Handle not found
    }
}
```

```python
from botocore.exceptions import ClientError

try:
    client.describe_instances(InstanceIds=['i-nonexistent'])
except ClientError as e:
    error_code = e.response['Error']['Code']
    error_message = e.response['Error']['Message']
    request_id = e.response['ResponseMetadata']['RequestId']
```

### Azure Error Structure
```go
import "github.com/Azure/azure-sdk-for-go/sdk/azcore"

var respErr *azcore.ResponseError
if errors.As(err, &respErr) {
    log.Printf("Status: %d", respErr.StatusCode)
    log.Printf("Code: %s", respErr.ErrorCode)
    log.Printf("Message: %s", respErr.RawResponse)
}
```

```python
from azure.core.exceptions import HttpResponseError

try:
    client.virtual_machines.get(rg, name)
except HttpResponseError as e:
    print(f"Status: {e.status_code}")
    print(f"Code: {e.error.code}")
    print(f"Message: {e.error.message}")
```

### GCP Error Structure
```go
import "google.golang.org/api/googleapi"

var gerr *googleapi.Error
if errors.As(err, &gerr) {
    log.Printf("Code: %d", gerr.Code)
    log.Printf("Message: %s", gerr.Message)
    for _, e := range gerr.Errors {
        log.Printf("Reason: %s", e.Reason)
    }
}
```

```python
from google.api_core.exceptions import GoogleAPIError

try:
    instance = client.get(project=project, zone=zone, instance=name)
except GoogleAPIError as e:
    print(f"Code: {e.code}")
    print(f"Message: {e.message}")
```

## Rate Limiting

### Retry with Exponential Backoff

**Go (generic pattern):**
```go
func withRetry[T any](operation func() (T, error), maxRetries int) (T, error) {
    var result T
    var err error
    
    for attempt := 0; attempt < maxRetries; attempt++ {
        result, err = operation()
        if err == nil {
            return result, nil
        }
        
        if !isRetryable(err) {
            return result, err
        }
        
        backoff := time.Duration(math.Pow(2, float64(attempt))) * time.Second
        jitter := time.Duration(rand.Intn(1000)) * time.Millisecond
        time.Sleep(backoff + jitter)
    }
    
    return result, err
}
```

**Python (generic pattern):**
```python
import time
import random

def with_retry(operation, max_retries=5, base_delay=1):
    for attempt in range(max_retries):
        try:
            return operation()
        except Exception as e:
            if not is_retryable(e):
                raise
            delay = (2 ** attempt) * base_delay
            jitter = random.uniform(0, 1)
            time.sleep(delay + jitter)
    raise Exception("Max retries exceeded")
```

### SDK Built-in Retry

**AWS:**
```python
from botocore.config import Config
config = Config(retries={'max_attempts': 10, 'mode': 'adaptive'})
client = boto3.client('ec2', config=config)
```

**Azure:**
```python
from azure.core.pipeline.policies import RetryPolicy
# Built into SDK by default, configurable
```

**GCP:**
```python
from google.api_core.retry import Retry
# Most clients have retry built-in
```
