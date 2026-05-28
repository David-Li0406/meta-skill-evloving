# Investigation Checklist

Systematic debugging checklist for common failure modes.

**How to use:** Work through checklist top-to-bottom. Check each item. Don't skip.

---

## General Debugging Checklist

### 1. What Changed Recently?

```bash
# Git history (last 10 commits)
git log --oneline -10

# Changes in last 24 hours
git log --since="24 hours ago" --oneline

# Diff from last working version
git diff $LAST_WORKING_SHA HEAD

# Recent deployments
gh run list --limit 5

# Recent infrastructure changes
cd terraform && git log --oneline -5
```

**Questions:**
- [ ] Was there a recent deploy?
- [ ] Did Terraform apply run?
- [ ] Were dependencies updated?
- [ ] Did configuration change?

### 2. What's the Exact Error Message?

```bash
# Get recent error logs
aws logs filter-log-events \
  --log-group-name /aws/lambda/worker \
  --start-time $(($(date +%s) - 3600))000 \
  --filter-pattern "ERROR" \
  --query 'events[*].message' \
  --output text

# Search for specific error
aws logs filter-log-events \
  --log-group-name /aws/lambda/worker \
  --filter-pattern "TypeError"
```

**Questions:**
- [ ] What's the exact error type? (TypeError, ValueError, etc.)
- [ ] What's the error message?
- [ ] What's the stack trace?
- [ ] What line number?

### 3. Can You Reproduce Locally?

```bash
# Try to reproduce the error
python3 << 'EOF'
from src.module import function

# Use same input as production
result = function('NVDA19')
EOF
```

**Questions:**
- [ ] Does it reproduce locally?
- [ ] If yes → Debug with breakpoints
- [ ] If no → Environment-specific issue

### 4. Does It Fail Consistently?

```bash
# Test multiple times
for i in {1..10}; do
    aws lambda invoke \
        --function-name worker \
        --payload '{"ticker": "NVDA19"}' \
        /tmp/test-$i.json
    grep -q "errorMessage" /tmp/test-$i.json && echo "Run $i: FAILED" || echo "Run $i: SUCCESS"
done
```

**Questions:**
- [ ] Does it fail 100% of the time? → Deterministic bug
- [ ] Does it fail ~50% of the time? → Race condition
- [ ] Does it fail occasionally? → External dependency issue

### 5. Does It Fail for All Inputs?

```bash
# Test with different inputs
for ticker in NVDA19 AAPL19 TSLA19; do
    aws lambda invoke \
        --function-name worker \
        --payload "{\"ticker\": \"$ticker\"}" \
        /tmp/test-$ticker.json
    grep -q "errorMessage" /tmp/test-$ticker.json && echo "$ticker: FAILED" || echo "$ticker: SUCCESS"
done
```

**Questions:**
- [ ] Fails for all inputs? → Logic bug
- [ ] Fails for specific input? → Data validation issue
- [ ] Fails for edge cases? → Boundary condition bug

---

## AWS Lambda Issues

### Lambda Not Executing

```bash
# Check if Lambda exists
aws lambda get-function --function-name worker

# Check execution role
aws lambda get-function-configuration \
    --function-name worker \
    --query 'Role'

# Check recent invocations
aws lambda get-function \
    --function-name worker \
    --query 'Configuration.LastModified'

# Check CloudWatch metrics
aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Invocations \
    --dimensions Name=FunctionName,Value=worker \
    --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period 300 \
    --statistics Sum
```

**Checklist:**
- [ ] Lambda function exists?
- [ ] Correct function name?
- [ ] IAM role attached?
- [ ] Invocations showing in metrics?

### Lambda Timeout

```bash
# Check timeout configuration
aws lambda get-function-configuration \
    --function-name worker \
    --query 'Timeout'

# Check duration metrics
aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Duration \
    --dimensions Name=FunctionName,Value=worker \
    --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period 300 \
    --statistics Average,Maximum
```

**Checklist:**
- [ ] Timeout value (default: 3 seconds)?
- [ ] Average duration vs timeout?
- [ ] External API calls timing out?
- [ ] Database queries slow?

### Lambda Permissions Error

```bash
# Check IAM role policies
ROLE_NAME=$(aws lambda get-function-configuration \
    --function-name worker \
    --query 'Role' --output text | cut -d'/' -f2)

aws iam list-attached-role-policies --role-name $ROLE_NAME

# Check specific permission
aws iam simulate-principal-policy \
    --policy-source-arn arn:aws:iam::123456789012:role/$ROLE_NAME \
    --action-names s3:PutObject \
    --resource-arns arn:aws:s3:::my-bucket/*
```

**Checklist:**
- [ ] S3 read/write permissions?
- [ ] DynamoDB permissions?
- [ ] Secrets Manager permissions?
- [ ] CloudWatch Logs permissions?

---

## Database Issues

### Aurora Connection Failed

```bash
# Check cluster status
aws rds describe-db-clusters \
    --db-cluster-identifier [PROJECT_NAME]-dev \
    --query 'DBClusters[0].Status'

# Check security group
aws ec2 describe-security-groups \
    --group-ids sg-1234567890abcdef0

# Test connectivity (requires SSM tunnel)
aws ssm start-session \
    --target i-1234567890abcdef0 \
    --document-name AWS-StartPortForwardingSessionToRemoteHost \
    --parameters '{"host":["aurora-endpoint"],"portNumber":["3306"],"localPortNumber":["3307"]}'

# Test connection
mysql -h 127.0.0.1 -P 3307 -u admin -p -e "SELECT 1"
```

**Checklist:**
- [ ] Aurora cluster status = "available"?
- [ ] Security group allows Lambda's security group?
- [ ] Endpoint correct in environment variables?
- [ ] Credentials correct?
- [ ] SSM tunnel required? (VPC-only Aurora)

### Query Returning No Data

```bash
# Check if data exists
mysql -h 127.0.0.1 -P 3307 -u admin -p << 'SQL'
SELECT COUNT(*) FROM precomputed_reports;
SELECT * FROM precomputed_reports LIMIT 5;
SQL

# Check query parameters
cat > test_query.py << 'EOF'
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3307, user='admin', password='***', database='reports')
cursor = conn.cursor()

# Test query
cursor.execute("SELECT * FROM precomputed_reports WHERE symbol = %s", ('NVDA19',))
result = cursor.fetchall()

print(f"Rows returned: {len(result)}")
print(f"Sample: {result[0] if result else 'NO DATA'}")
EOF

python3 test_query.py
```

**Checklist:**
- [ ] Table contains data?
- [ ] WHERE clause correct?
- [ ] Column names correct? (case-sensitive)
- [ ] Parameter binding correct?

### INSERT Affected 0 Rows

```bash
# Check for silent failures
cat > test_insert.py << 'EOF'
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3307, user='admin', password='***', database='reports')
cursor = conn.cursor()

# Test INSERT
query = "INSERT INTO precomputed_reports (symbol, report_json) VALUES (%s, %s)"
rowcount = cursor.execute(query, ('TEST19', '{"test": true}'))

print(f"Rows affected: {rowcount}")

# Check constraints
cursor.execute("SHOW CREATE TABLE precomputed_reports")
print(cursor.fetchone()[1])
EOF

python3 test_insert.py
```

**Checklist:**
- [ ] Foreign key constraint? (silent failure)
- [ ] ENUM value mismatch? (silent failure)
- [ ] Duplicate key with INSERT IGNORE? (silent)
- [ ] Check rowcount after execute?

---

## API Integration Issues

### External API Returning Error

```bash
# Test API directly
curl -v https://api.example.com/endpoint \
    -H "Authorization: Bearer $API_KEY" \
    -d '{"ticker": "NVDA19"}' \
    | jq .

# Check response status
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    https://api.example.com/endpoint)

echo "HTTP Status: $HTTP_STATUS"
```

**Checklist:**
- [ ] API key valid?
- [ ] Rate limit exceeded?
- [ ] Request format correct?
- [ ] Response parsing correct?

### Type Mismatch at System Boundary

```bash
# Inspect actual response
curl -s https://api.example.com/endpoint | jq . > response.json

# Check types
cat > inspect_types.py << 'EOF'
import json

with open('response.json') as f:
    data = json.load(f)

def inspect(obj, path=""):
    if isinstance(obj, dict):
        for key, value in obj.items():
            inspect(value, f"{path}.{key}")
    elif isinstance(obj, list):
        if obj:
            inspect(obj[0], f"{path}[0]")
    else:
        print(f"{path}: {type(obj).__name__} = {repr(obj)}")

inspect(data)
EOF

python3 inspect_types.py
```

**Checklist:**
- [ ] API returns dict or list?
- [ ] Field names match?
- [ ] Types match expectations? (str vs int)
- [ ] Null values handled?
- [ ] Nested structures handled?

---

## JSON Serialization Issues

### Lambda Response Not Serializable

```bash
# Test serialization locally
cat > test_serialization.py << 'EOF'
import json
import numpy as np
import pandas as pd
from datetime import datetime, date

test_data = {
    'numpy_int': np.int64(42),
    'pandas_timestamp': pd.Timestamp('2024-01-01'),
    'datetime_obj': datetime.now(),
    'date_obj': date.today()
}

# Test each field
for key, value in test_data.items():
    try:
        json.dumps({key: value})
        print(f"✅ {key}: {type(value).__name__}")
    except TypeError as e:
        print(f"❌ {key}: {type(value).__name__} - {e}")
EOF

python3 test_serialization.py
```

**Checklist:**
- [ ] NumPy types converted? (np.int64 → int)
- [ ] Pandas types converted? (pd.Timestamp → str)
- [ ] Datetime objects converted? (→ isoformat())
- [ ] Nested dicts/lists serializable?

---

## Deployment Issues

### Deployment Succeeded But Function Broken

```bash
# Check deployment actually updated function
aws lambda get-function \
    --function-name worker \
    --query '[CodeSha256, LastModified]'

# Compare with expected image
aws ecr describe-images \
    --repository-name [PROJECT_NAME]-worker \
    --image-ids imageDigest=$EXPECTED_DIGEST

# Check environment variables
aws lambda get-function-configuration \
    --function-name worker \
    --query 'Environment.Variables'
```

**Checklist:**
- [ ] CodeSha256 changed after deploy?
- [ ] LastModified timestamp recent?
- [ ] Correct image deployed?
- [ ] Environment variables set?

### CloudWatch Logs Show No Errors But Function Failing

```bash
# Check log level configuration
aws lambda get-function-configuration \
    --function-name worker \
    --query 'Environment.Variables.LOG_LEVEL'

# Search for warnings (might be logged at wrong level)
aws logs filter-log-events \
    --log-group-name /aws/lambda/worker \
    --filter-pattern "WARNING"

# Check if logs are even being generated
aws logs describe-log-streams \
    --log-group-name /aws/lambda/worker \
    --order-by LastEventTime \
    --descending \
    --max-items 5
```

**Checklist:**
- [ ] Log level set correctly? (INFO vs WARNING)
- [ ] Errors logged at WARNING level? (invisible to ERROR filter)
- [ ] Logs being generated at all?
- [ ] Check both ERROR and WARNING logs?

---

## Secret Management Issues

### Doppler Secrets Not Loading

```bash
# Verify Doppler configuration
doppler projects get

# Check config for environment
ENV=dev doppler configs get

# Test secret retrieval
ENV=dev doppler secrets get AURORA_HOST --plain

# Verify Doppler token
ENV=dev doppler run -- env | grep DOPPLER
```

**Checklist:**
- [ ] Doppler CLI installed?
- [ ] Project configured?
- [ ] Config exists for environment?
- [ ] Secrets accessible?
- [ ] Doppler token valid?

### GitHub Secrets Out of Sync with AWS

```bash
# Query actual infrastructure
ACTUAL_DIST=$(aws cloudfront list-distributions \
    --query 'DistributionList.Items[?Comment==`app-dev`].Id' \
    --output text)

echo "AWS Reality: $ACTUAL_DIST"
echo "GitHub Secret: (check manually)"

# If mismatch, update GitHub secret
gh secret set CLOUDFRONT_DISTRIBUTION_ID --body "$ACTUAL_DIST"
```

**Checklist:**
- [ ] CloudFront distribution ID matches?
- [ ] S3 bucket name matches?
- [ ] Lambda function name matches?
- [ ] Secrets updated after Terraform changes?

---

## Quick Reference

### Investigation Priority

1. **What changed?** (git log, deployments)
2. **What's the exact error?** (CloudWatch logs)
3. **Reproduce locally** (faster iteration)
4. **Check AWS resources** (permissions, config)
5. **Verify data** (inspect actual values)

### Common Root Causes

| Symptom | Likely Root Cause | Check |
|---------|-------------------|-------|
| **TypeError: not all arguments converted** | Type mismatch | Test with minimal example |
| **INSERT affected 0 rows** | FK constraint, ENUM mismatch | Check rowcount, constraints |
| **403 Forbidden** | IAM permissions | Simulate permissions |
| **Connection timeout** | Security group, VPC | Check network path |
| **Function not found** | Wrong function name | List functions |
| **Logs show no errors but failing** | Wrong log level | Check WARNING logs |

---

## References

- [AWS Lambda Troubleshooting](https://docs.aws.amazon.com/lambda/latest/dg/lambda-troubleshooting.html)
- [MySQL Silent Failures](https://dev.mysql.com/doc/refman/8.0/en/constraint-foreign-key.html)
- [Debugging Distributed Systems](https://sre.google/sre-book/effective-troubleshooting/)
