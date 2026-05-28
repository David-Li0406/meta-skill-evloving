# Troubleshooting Workflows

## Table of Contents
- [Permission Errors](#permission-errors)
- [Connectivity Issues](#connectivity-issues)
- [SDK/API Errors](#sdkapi-errors)
- [IaC Errors](#iac-errors)
- [Performance Issues](#performance-issues)

## Permission Errors

### Universal Triage Order
When facing `AccessDenied`, `Forbidden`, `AuthorizationFailed`, `PERMISSION_DENIED`:

**1. Scope mismatch** (most common)
- Permission granted at wrong level?
- AWS: Check ARN patterns and wildcards
- Azure: Check exact resource ID vs resource group vs subscription
- GCP: Check project ID in resource path

**2. Propagation delay**
- IAM changes take time to propagate
- AWS: 10-60 seconds
- Azure: Up to 10 minutes
- GCP: 60+ seconds
- **Action:** Wait and retry before deeper investigation

**3. Policy restrictions**
- AWS: SCPs denying at org level?
- Azure: Deny assignments? Conditional access?
- GCP: Organisation policies?
- **Action:** Check higher-level policies

**4. Resource policy conflict**
- Some resources have their own policies (S3, KMS, SQS, etc.)
- Both identity AND resource policy must allow
- **Action:** Check resource-level policies

**5. Provider/API not enabled**
- Azure: Resource provider not registered
- GCP: API not enabled on project
- **Action:** Check and enable

### Provider-Specific Commands

**AWS:**
```bash
# Who am I?
aws sts get-caller-identity

# Simulate permissions
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:role/MyRole \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::my-bucket/*

# Decode auth error message
aws sts decode-authorization-message --encoded-message <msg>
```

**Azure:**
```bash
# Who am I?
az account show
az ad signed-in-user show

# Check role assignments (include inherited!)
az role assignment list --assignee <principal-id> --all --include-inherited

# Check deny assignments
az rest --method GET \
  --uri "/subscriptions/{sub}/providers/Microsoft.Authorization/denyAssignments?api-version=2022-04-01"

# Check provider registration
az provider show -n Microsoft.Compute --query "registrationState"
```

**GCP:**
```bash
# Who am I?
gcloud auth list
gcloud config get-value account

# Analyse IAM permissions
gcloud asset analyze-iam-policy \
  --organization=ORG_ID \
  --identity="serviceAccount:sa@project.iam.gserviceaccount.com" \
  --full-resource-name="//compute.googleapis.com/projects/PROJECT/zones/ZONE/instances/INSTANCE"

# Check API enabled
gcloud services list --enabled | grep compute
```

## Connectivity Issues

### Can't Reach Cloud API

**1. DNS resolution**
```bash
# Can we resolve the endpoint?
nslookup ec2.eu-west-2.amazonaws.com
nslookup management.azure.com
nslookup compute.googleapis.com
```

**2. Network path**
```bash
# Can we connect?
curl -v https://ec2.eu-west-2.amazonaws.com/
curl -v https://management.azure.com/
curl -v https://compute.googleapis.com/

# Check for proxy
env | grep -i proxy
```

**3. Firewall/Security group**
- Egress rules allowing HTTPS (443)?
- NACLs (AWS) or NSGs (Azure) blocking?

**4. VPC endpoints / Private Link**
- If no internet access, is private endpoint configured?
- DNS resolving to private endpoint IP?

### Can't Reach Resource from Resource

**1. Same VPC/VNet?**
- If different networks, is there peering/transit?
- Are route tables correct?

**2. Security groups / NSGs**
```bash
# AWS: Check security group rules
aws ec2 describe-security-groups --group-ids sg-xxx

# Azure: Check NSG rules
az network nsg show -g rg-name -n nsg-name
```

**3. NACLs (AWS) / Subnet-level rules**
- NACLs are stateless — need both inbound AND outbound rules
- Check both source and destination subnets

**4. Private DNS**
- Is the hostname resolving to the correct private IP?
- Custom DNS servers configured correctly?

## SDK/API Errors

### Error Response Anatomy

**Always extract:**
1. **Error code:** Machine-readable (e.g., `AccessDenied`, `InvalidParameterValue`)
2. **Error message:** Human-readable description
3. **Request ID:** Essential for support cases

### Common Error Patterns

| Error | Likely Cause | First Check |
|-------|--------------|-------------|
| `AccessDenied` / `Forbidden` | Permission issue | See permission errors section |
| `InvalidParameterValue` | Wrong parameter format | Check API docs for expected format |
| `ResourceNotFound` | Resource doesn't exist or wrong region | Verify resource exists, check region |
| `ThrottlingException` | Rate limit hit | Implement backoff, check limits |
| `ValidationError` | Invalid request structure | Check required fields, data types |
| `ServiceUnavailable` | Cloud provider issue | Retry with backoff, check status page |

### Debugging Checklist

1. **Enable SDK logging** (see sdk-patterns.md)
2. **Check the exact request** being sent
3. **Compare with working example** (CLI, console, etc.)
4. **Check for typos** in resource IDs, regions, etc.
5. **Verify API version** — old SDK may use deprecated endpoints

## IaC Errors

### Terraform Errors

**"Error acquiring the state lock"**
```bash
# Who holds the lock?
aws dynamodb scan --table-name terraform-locks  # AWS
az storage blob show -c tfstate -n terraform.tfstate  # Azure

# Force unlock (careful!)
terraform force-unlock LOCK_ID
```

**"Resource already exists"**
1. Created outside Terraform? → Import: `terraform import <address> <id>`
2. Managed elsewhere? → Remove from state: `terraform state rm <address>`

**"Cycle detected"**
- Circular dependency between resources
- Debug: `terraform graph | dot -Tpng > graph.png`
- Fix: Restructure dependencies, use `depends_on` sparingly

**"Invalid for_each argument"**
- `for_each` value unknown at plan time
- Fix: Use `count` with conditional, or restructure to use known values

**Provider authentication fails**
```bash
# Verify credentials
terraform providers lock -platform=linux_amd64

# Clear cache
rm -rf .terraform
terraform init

# Check environment
env | grep -E 'AWS_|AZURE_|GOOGLE_'
```

### Pulumi Errors

**"conflict: resource already exists"**
```bash
# Import existing resource
pulumi import aws:s3/bucket:Bucket my-bucket existing-bucket-name

# Or refresh state
pulumi refresh
```

**"error: no credentials available"**
```bash
# AWS
export AWS_PROFILE=myprofile
# or
pulumi config set aws:region eu-west-2
pulumi config set aws:profile myprofile
```

### CloudFormation Errors

**"Resource failed to stabilize"**
- Resource creation timing out
- Check CloudWatch Logs for the resource
- Increase timeout in template

**"Circular dependency"**
- Use `DependsOn` to break cycles
- Consider splitting into nested stacks

**Rollback stuck**
```bash
# Force delete (loses resources!)
aws cloudformation delete-stack --stack-name my-stack --retain-resources LogGroup

# Continue update rollback
aws cloudformation continue-update-rollback --stack-name my-stack
```

## Performance Issues

### High Latency

**1. Where is the latency?**
- Network? (traceroute, ping)
- API processing? (check response times)
- Client-side? (SDK overhead, retries)

**2. Check region alignment**
- Is your app in the same region as resources?
- Cross-region calls add 50-200ms+

**3. Connection reuse**
- SDKs should reuse connections
- Check for accidental client recreation per request

### Rate Limiting

**Symptoms:**
- HTTP 429 / 503 responses
- `ThrottlingException`, `RequestLimitExceeded`
- Increasing latency under load

**Diagnosis:**
```bash
# AWS - check service quotas
aws service-quotas get-service-quota \
  --service-code ec2 \
  --quota-code L-0263D0A3

# Azure - check headers
curl -v ... | grep -i ratelimit

# GCP - check quota
gcloud compute project-info describe --project=PROJECT_ID
```

**Mitigation:**
1. Implement exponential backoff with jitter
2. Use bulk APIs where available
3. Cache responses
4. Request quota increase
5. Distribute load across accounts/projects (where rate limits are per-account)

### Memory/Connection Leaks

**Symptoms:**
- Gradually increasing memory usage
- "Too many open files" errors
- Connection timeouts

**Common causes:**
- Not closing HTTP responses
- Paginator not fully consumed
- Client created per request instead of reused

**Go pattern:**
```go
resp, err := client.DoSomething(ctx, input)
if err != nil { return err }
defer resp.Body.Close()  // Don't forget this!
```

**Python pattern:**
```python
# Use context managers
with client.get_object(...) as response:
    data = response['Body'].read()
```
