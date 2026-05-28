# AWS Service Diagnostics

AWS-specific error patterns and diagnostic procedures for common services.

**Principle:** Each AWS service has unique failure modes. Know the service-specific diagnostic commands.

---

## Lambda Diagnostics

### Error: Function Not Found

```bash
# List all Lambda functions
aws lambda list-functions --query 'Functions[*].FunctionName'

# Search for function by pattern
aws lambda list-functions \
  --query 'Functions[?contains(FunctionName, `worker`)].FunctionName'

# Check if function exists in specific region
aws lambda get-function --function-name worker --region ap-southeast-1
```

**Common Causes:**
- Wrong function name (case-sensitive)
- Wrong region
- Function deleted
- No permission to see function

### Error: Timeout

```bash
# Check timeout configuration
aws lambda get-function-configuration \
  --function-name worker \
  --query '[Timeout, MemorySize]'

# Check duration statistics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=worker \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 60 \
  --statistics Average,Maximum \
  --query 'Datapoints[*].[Timestamp,Average,Maximum]' \
  --output table

# Check concurrent executions (might be throttled)
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name ConcurrentExecutions \
  --dimensions Name=FunctionName,Value=worker \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 60 \
  --statistics Maximum
```

**Diagnostic Pattern:**

1. Average duration vs timeout? (If avg ≈ timeout → function timing out)
2. External API calls? (Check network timeouts)
3. Database queries? (Check slow query logs)
4. Cold starts? (Check initialization duration)

### Error: Out of Memory

```bash
# Check memory configuration
aws lambda get-function-configuration \
  --function-name worker \
  --query 'MemorySize'

# Get memory usage from logs
aws logs filter-log-events \
  --log-group-name /aws/lambda/worker \
  --filter-pattern "Memory Size" \
  --query 'events[*].message' \
  | jq -r '.[]' | grep "Memory Size"

# Example output:
# REPORT RequestId: abc-123 Duration: 1234.56 ms Billed Duration: 1300 ms
# Memory Size: 512 MB Max Memory Used: 489 MB
```

**Pattern:** If Max Memory Used ≈ Memory Size → increase memory.

### Error: Permission Denied

```bash
# Get Lambda execution role
ROLE_ARN=$(aws lambda get-function-configuration \
  --function-name worker \
  --query 'Role' --output text)

ROLE_NAME=$(echo $ROLE_ARN | cut -d'/' -f2)

# List attached policies
aws iam list-attached-role-policies --role-name $ROLE_NAME

# Get policy document
POLICY_ARN=$(aws iam list-attached-role-policies \
  --role-name $ROLE_NAME \
  --query 'AttachedPolicies[0].PolicyArn' --output text)

aws iam get-policy-version \
  --policy-arn $POLICY_ARN \
  --version-id $(aws iam get-policy --policy-arn $POLICY_ARN \
    --query 'Policy.DefaultVersionId' --output text) \
  --query 'PolicyVersion.Document' | jq .

# Simulate specific permission
aws iam simulate-principal-policy \
  --policy-source-arn $ROLE_ARN \
  --action-names s3:PutObject \
  --resource-arns arn:aws:s3:::my-bucket/*
```

**Common Missing Permissions:**
- S3: `s3:PutObject`, `s3:GetObject`
- DynamoDB: `dynamodb:PutItem`, `dynamodb:Query`
- CloudWatch Logs: `logs:CreateLogStream`, `logs:PutLogEvents`
- Secrets Manager: `secretsmanager:GetSecretValue`

---

## DynamoDB Diagnostics

### Error: ConditionalCheckFailedException

```python
# Error example
# botocore.exceptions.ClientError: ConditionalCheckFailedException

# Diagnostic: What condition failed?
try:
    response = table.put_item(
        Item={'ticker': 'NVDA19', 'data': {...}},
        ConditionExpression='attribute_not_exists(ticker)'
    )
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
        # Check if item already exists
        existing = table.get_item(Key={'ticker': 'NVDA19'})
        print(f"Item exists: {existing.get('Item')}")

        # This is expected behavior, not an error
        logger.info("Item already exists, update instead")
        table.update_item(...)
```

### Error: ValidationException (Type Mismatch)

```bash
# Error example
# ValidationException: One or more parameter values were invalid:
# Type mismatch for key ticker expected: S actual: N

# Diagnostic: Check table schema
aws dynamodb describe-table \
  --table-name [PROJECT_NAME]-telegram-jobs-dev \
  --query 'Table.KeySchema'

# Output shows expected types:
# [
#   {"AttributeName": "ticker", "KeyType": "HASH"},  # Partition key
#   {"AttributeName": "timestamp", "KeyType": "RANGE"}  # Sort key
# ]

# Check attribute types
aws dynamodb describe-table \
  --table-name [PROJECT_NAME]-telegram-jobs-dev \
  --query 'Table.AttributeDefinitions'

# Output:
# [
#   {"AttributeName": "ticker", "AttributeType": "S"},  # String
#   {"AttributeName": "timestamp", "AttributeType": "N"}  # Number
# ]
```

**Fix:** Ensure types match schema.

```python
# Before: Wrong type
table.put_item(Item={
    'ticker': 12345,  # ❌ Number, expected String
    'timestamp': '2024-01-15'  # ❌ String, expected Number
})

# After: Correct types
table.put_item(Item={
    'ticker': 'NVDA19',  # ✅ String
    'timestamp': int(datetime.now().timestamp())  # ✅ Number
})
```

### Error: ProvisionedThroughputExceededException

```bash
# Check current throughput
aws dynamodb describe-table \
  --table-name [PROJECT_NAME]-telegram-jobs-dev \
  --query 'Table.[BillingModeSummary,ProvisionedThroughput]'

# If on-demand mode:
# BillingModeSummary: {"BillingMode": "PAY_PER_REQUEST"}

# If provisioned mode:
# ProvisionedThroughput: {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}

# Check throttled requests
aws cloudwatch get-metric-statistics \
  --namespace AWS/DynamoDB \
  --metric-name UserErrors \
  --dimensions Name=TableName,Value=[PROJECT_NAME]-telegram-jobs-dev \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum
```

**Solutions:**
1. Switch to on-demand billing
2. Increase provisioned capacity
3. Add exponential backoff retry logic

---

## S3 Diagnostics

### Error: Access Denied (403)

```bash
# Check bucket policy
aws s3api get-bucket-policy \
  --bucket [PROJECT_NAME]-data-dev \
  | jq -r '.Policy | fromjson'

# Check bucket ACL
aws s3api get-bucket-acl \
  --bucket [PROJECT_NAME]-data-dev

# Check object ACL
aws s3api get-object-acl \
  --bucket [PROJECT_NAME]-data-dev \
  --key reports/NVDA19.json

# Test access with specific IAM role
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456:role/lambda-execution-role \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::[PROJECT_NAME]-data-dev/*
```

**Common Causes:**
- Bucket policy blocks access
- IAM role missing S3 permissions
- Object owned by different account
- Bucket encryption requires KMS permissions

### Error: NoSuchKey (404)

```bash
# List objects with prefix
aws s3 ls s3://[PROJECT_NAME]-data-dev/reports/

# Search for object
aws s3api list-objects-v2 \
  --bucket [PROJECT_NAME]-data-dev \
  --prefix reports/ \
  --query 'Contents[?contains(Key, `NVDA19`)]'

# Check if object was deleted
aws s3api list-object-versions \
  --bucket [PROJECT_NAME]-data-dev \
  --prefix reports/NVDA19.json

# If versioning enabled, check delete markers
aws s3api list-object-versions \
  --bucket [PROJECT_NAME]-data-dev \
  --prefix reports/NVDA19.json \
  --query 'DeleteMarkers'
```

### Error: Slow Upload/Download

```bash
# Check S3 transfer metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/S3 \
  --metric-name AllRequests \
  --dimensions Name=BucketName,Value=[PROJECT_NAME]-data-dev \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum

# Check network path (if Lambda in VPC)
# - VPC endpoint for S3? (faster, cheaper)
# - NAT gateway? (slower, costs money)
# - Internet gateway? (fastest, but requires public subnet)
```

**Optimization:**
- Use S3 Transfer Acceleration for large files
- Enable S3 VPC endpoint if Lambda in VPC
- Use multipart upload for files > 100MB

---

## CloudWatch Logs Diagnostics

### Error: Log Group Not Found

```bash
# List all log groups
aws logs describe-log-groups \
  --query 'logGroups[*].logGroupName'

# Search for log group
aws logs describe-log-groups \
  --log-group-name-prefix /aws/lambda/

# Create log group if missing
aws logs create-log-group \
  --log-group-name /aws/lambda/worker
```

### Error: Logs Not Appearing

```bash
# Check recent log streams
aws logs describe-log-streams \
  --log-group-name /aws/lambda/worker \
  --order-by LastEventTime \
  --descending \
  --max-items 5

# Check if Lambda has CloudWatch Logs permissions
ROLE_ARN=$(aws lambda get-function-configuration \
  --function-name worker \
  --query 'Role' --output text)

aws iam simulate-principal-policy \
  --policy-source-arn $ROLE_ARN \
  --action-names logs:CreateLogStream logs:PutLogEvents
```

**Common Causes:**
- IAM role missing `logs:CreateLogStream` or `logs:PutLogEvents`
- Log group doesn't exist
- Logs buffered (wait 5-10 seconds)

### Advanced Log Queries

```bash
# Query with CloudWatch Logs Insights
aws logs start-query \
  --log-group-name /aws/lambda/worker \
  --start-time $(date -u -d '1 hour ago' +%s) \
  --end-time $(date -u +%s) \
  --query-string '
    fields @timestamp, @message
    | filter @message like /ERROR/
    | stats count() by bin(5m)
  ' \
  --query 'queryId' --output text

# Get query results (wait a few seconds)
QUERY_ID=<query-id-from-above>
aws logs get-query-results --query-id $QUERY_ID
```

**Useful Queries:**

```sql
-- Count errors by hour
fields @timestamp, @message
| filter @message like /ERROR/
| stats count() by bin(1h)

-- Find slow requests
fields @timestamp, @duration
| filter @duration > 1000
| sort @duration desc

-- Parse JSON logs
fields @timestamp, @message
| parse @message '{"level":"*","message":"*"}' as level, msg
| filter level = "ERROR"
```

---

## Aurora/RDS Diagnostics

### Error: Connection Timeout

```bash
# Check cluster status
aws rds describe-db-clusters \
  --db-cluster-identifier [PROJECT_NAME]-dev \
  --query 'DBClusters[0].[Status,Endpoint,ReaderEndpoint]'

# Check security group
SECURITY_GROUP=$(aws rds describe-db-clusters \
  --db-cluster-identifier [PROJECT_NAME]-dev \
  --query 'DBClusters[0].VpcSecurityGroups[0].VpcSecurityGroupId' \
  --output text)

aws ec2 describe-security-groups --group-ids $SECURITY_GROUP

# Check if Lambda can reach Aurora
# Lambda must be in same VPC as Aurora
aws lambda get-function-configuration \
  --function-name worker \
  --query 'VpcConfig'

# If Lambda not in VPC, it CANNOT reach Aurora (private subnet)
```

**Solutions:**
1. Put Lambda in same VPC as Aurora
2. Configure security group to allow Lambda's security group
3. Use RDS Proxy for connection pooling

### Error: Too Many Connections

```bash
# Check max connections
mysql -h aurora-endpoint -u admin -p << 'SQL'
SHOW VARIABLES LIKE 'max_connections';
SHOW STATUS LIKE 'Threads_connected';
SHOW PROCESSLIST;
SQL

# Check active connections from Lambda
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name DatabaseConnections \
  --dimensions Name=DBClusterIdentifier,Value=[PROJECT_NAME]-dev \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 60 \
  --statistics Maximum
```

**Solutions:**
1. Use connection pooling (pymysql with pool)
2. Close connections properly
3. Use RDS Proxy
4. Increase max_connections parameter

### Error: Slow Query

```bash
# Enable slow query log
aws rds modify-db-parameter-group \
  --db-parameter-group-name default.aurora-mysql8.0 \
  --parameters "ParameterName=slow_query_log,ParameterValue=1,ApplyMethod=immediate" \
              "ParameterName=long_query_time,ParameterValue=1,ApplyMethod=immediate"

# Download slow query log
aws rds download-db-log-file-portion \
  --db-instance-identifier [PROJECT_NAME]-dev-instance-1 \
  --log-file-name slowquery/mysql-slowquery.log

# Analyze slow queries
grep "Query_time" mysql-slowquery.log | sort -rn | head -10
```

---

## Step Functions Diagnostics

### Error: Execution Failed

```bash
# List recent executions
aws stepfunctions list-executions \
  --state-machine-arn arn:aws:states:ap-southeast-1:123456:stateMachine:worker \
  --status-filter FAILED \
  --max-items 5

# Get execution details
aws stepfunctions describe-execution \
  --execution-arn arn:aws:states:ap-southeast-1:123456:execution:worker:abc-123

# Get execution history
aws stepfunctions get-execution-history \
  --execution-arn arn:aws:states:ap-southeast-1:123456:execution:worker:abc-123 \
  --query 'events[?type==`TaskFailed` || type==`ExecutionFailed`]'
```

### Error: Task Timed Out

```bash
# Check state machine definition
aws stepfunctions describe-state-machine \
  --state-machine-arn arn:aws:states:ap-southeast-1:123456:stateMachine:worker \
  --query 'definition' | jq -r . | jq .

# Look for TimeoutSeconds in task states
```

**Pattern:** Increase `TimeoutSeconds` in state definition.

---

## SQS Diagnostics

### Error: Messages Not Being Consumed

```bash
# Get queue URL
QUEUE_URL=$(aws sqs get-queue-url \
  --queue-name [PROJECT_NAME]-worker-dev \
  --query 'QueueUrl' --output text)

# Check queue attributes
aws sqs get-queue-attributes \
  --queue-url $QUEUE_URL \
  --attribute-names All \
  | jq '.Attributes | {
    ApproximateNumberOfMessages,
    ApproximateNumberOfMessagesNotVisible,
    ApproximateNumberOfMessagesDelayed,
    VisibilityTimeout,
    MessageRetentionPeriod
  }'

# Check dead letter queue
aws sqs get-queue-attributes \
  --queue-url $QUEUE_URL \
  --attribute-names RedrivePolicy \
  | jq -r '.Attributes.RedrivePolicy | fromjson'
```

**Common Issues:**
- Visibility timeout too short (message re-delivered before processing completes)
- Consumer crashed (check Lambda errors)
- Messages in DLQ (check dead letter queue)

### Error: MessageTooLarge

```bash
# SQS limit: 256 KB

# Check message size
echo '{"large": "data"}' | wc -c

# Solution: Store large data in S3, send S3 key in SQS
aws s3 cp large-data.json s3://bucket/key
aws sqs send-message \
  --queue-url $QUEUE_URL \
  --message-body '{"s3_key": "key"}'
```

---

## Quick Reference

### Diagnostic Commands by Service

| Service | Check Exists | Check Permissions | Check Status |
|---------|--------------|-------------------|--------------|
| **Lambda** | `get-function` | `simulate-principal-policy` | `get-function-configuration` |
| **DynamoDB** | `describe-table` | `simulate-principal-policy` | CloudWatch metrics |
| **S3** | `head-bucket` | `get-bucket-policy` | CloudWatch metrics |
| **Aurora** | `describe-db-clusters` | Security groups | `describe-db-clusters` Status |
| **CloudWatch Logs** | `describe-log-groups` | `simulate-principal-policy` | `describe-log-streams` |

### Error Code Quick Lookup

| Error Code | Service | Cause | Solution |
|------------|---------|-------|----------|
| **403** | S3, API Gateway | Permission denied | Check IAM policy, bucket policy |
| **404** | S3, Lambda | Resource not found | Verify resource exists, check spelling |
| **ConditionalCheckFailedException** | DynamoDB | Condition failed | Expected behavior, handle gracefully |
| **ProvisionedThroughputExceededException** | DynamoDB | Rate limit | Switch to on-demand or add backoff |
| **ResourceNotFoundException** | All services | Service/resource missing | Create resource or fix name |
| **ValidationException** | DynamoDB | Type mismatch | Check schema, convert types |

---

## References

- [AWS CLI Command Reference](https://awscli.amazonaws.com/v2/documentation/api/latest/index.html)
- [Boto3 Error Handling](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html)
- [CloudWatch Logs Insights Query Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html)
