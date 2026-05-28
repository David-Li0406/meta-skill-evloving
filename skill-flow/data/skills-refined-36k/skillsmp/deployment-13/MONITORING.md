# Deployment Monitoring Workflow

**For complete reference**, see [docs/deployment/MONITORING.md](../../../docs/deployment/MONITORING.md)

---

## Pre-Deployment Validation Workflow

**Before deploying, validate infrastructure-deployment contract:**

1. **Query AWS for actual resource IDs**
   ```bash
   # CloudFront distributions
   aws cloudfront list-distributions \
     --query 'DistributionList.Items[?Comment==`[PROJECT_NAME] APP CloudFront - dev`].Id' \
     --output text

   # S3 buckets
   aws s3 ls | grep [PROJECT_NAME]

   # Lambda functions
   aws lambda list-functions \
     --query 'Functions[?starts_with(FunctionName, `[PROJECT_NAME]`)].FunctionName'
   ```

2. **Compare with GitHub secrets**
   ```bash
   # List current secrets
   gh secret list

   # Check specific secret value (requires org/repo permissions)
   gh secret list | grep CLOUDFRONT
   ```

3. **If mismatch detected, update GitHub secrets**
   ```bash
   # Update secret to match AWS reality
   gh secret set CLOUDFRONT_DISTRIBUTION_ID --body "E1ABC234DEF"
   ```

**Automation**: Add validation job as first step in deployment pipeline (see docs for complete YAML).

---

## Multi-Layer Verification Checklist

**After deployment, verify ALL THREE layers:**

### Layer 1: Status Code (Weakest)
```bash
# Did AWS CLI succeed?
aws lambda invoke --function-name worker --payload '{}' /tmp/response.json
echo "Exit code: $?"  # 0 = CLI succeeded (NOT function succeeded!)
```

**Passes if**: AWS API responded
**Does NOT prove**: Function executed successfully

### Layer 2: Response Payload (Stronger)
```bash
# Did function return error?
if grep -q "errorMessage" /tmp/response.json; then
  echo "❌ Lambda returned error"
  exit 1
fi

# Check for expected fields
if ! jq -e '.result' /tmp/response.json > /dev/null; then
  echo "❌ Missing expected result field"
  exit 1
fi
```

**Passes if**: No errorMessage in response
**Does NOT prove**: No errors logged during execution

### Layer 3: CloudWatch Logs (Strongest)
```bash
# Were there ERROR-level logs?
START_TIME=$(($(date +%s) - 120))000

ERROR_COUNT=$(aws logs filter-log-events \
  --log-group-name /aws/lambda/worker \
  --start-time $START_TIME \
  --filter-pattern "ERROR" \
  --query 'length(events)' --output text)

if [ "$ERROR_COUNT" -gt 0 ]; then
  echo "❌ Found $ERROR_COUNT errors in CloudWatch"
  # Show errors
  aws logs filter-log-events \
    --log-group-name /aws/lambda/worker \
    --start-time $START_TIME \
    --filter-pattern "ERROR"
  exit 1
fi
```

**Passes if**: No ERROR-level logs
**Proves**: Function actually executed successfully

---

## Smoke Testing Workflow

**Pattern: Update → Wait → Test → Verify Logs**

```bash
#!/bin/bash
set -euo pipefail

FUNCTION_NAME="[PROJECT_NAME]-telegram-api-dev"

echo "1️⃣ Deploying function..."
aws lambda update-function-code \
  --function-name $FUNCTION_NAME \
  --image-uri $ECR_REPO:$TAG

echo "2️⃣ Waiting for deployment to complete..."
aws lambda wait function-updated --function-name $FUNCTION_NAME

echo "3️⃣ Running smoke test..."
aws lambda invoke \
  --function-name $FUNCTION_NAME \
  --qualifier '$LATEST' \
  --payload '{"httpMethod": "GET", "path": "/api/v1/health"}' \
  /tmp/smoke-test.json

echo "4️⃣ Checking response..."
if grep -q "errorMessage" /tmp/smoke-test.json; then
  echo "❌ Smoke test failed (errorMessage in response)"
  cat /tmp/smoke-test.json
  exit 1
fi

if ! jq -e '.statusCode == 200' /tmp/smoke-test.json > /dev/null; then
  echo "❌ Smoke test failed (statusCode != 200)"
  cat /tmp/smoke-test.json
  exit 1
fi

echo "5️⃣ Checking CloudWatch logs..."
sleep 5  # Wait for logs to propagate

ERROR_COUNT=$(aws logs filter-log-events \
  --log-group-name /aws/lambda/$FUNCTION_NAME \
  --start-time $(($(date +%s) - 120))000 \
  --filter-pattern "ERROR" \
  --query 'length(events)' --output text)

if [ "$ERROR_COUNT" -gt 0 ]; then
  echo "❌ Found errors in CloudWatch logs"
  aws logs tail /aws/lambda/$FUNCTION_NAME --since 2m --filter-pattern "ERROR"
  exit 1
fi

echo "✅ Smoke test passed (all 3 layers verified)"
```

---

## Post-Deployment Monitoring Workflow

**Monitor deployment for first 5 minutes:**

```bash
#!/bin/bash

FUNCTION_NAME=$1
DURATION_MINUTES=5

echo "Monitoring $FUNCTION_NAME for $DURATION_MINUTES minutes..."

# Track metrics
for i in $(seq 1 $DURATION_MINUTES); do
  echo ""
  echo "[$i/$DURATION_MINUTES] Checking metrics..."

  # Check invocation count
  INVOCATIONS=$(aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Invocations \
    --dimensions Name=FunctionName,Value=$FUNCTION_NAME \
    --statistics Sum \
    --start-time $(date -u -d '1 minute ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period 60 \
    --query 'Datapoints[0].Sum' --output text)

  # Check error count
  ERRORS=$(aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Errors \
    --dimensions Name=FunctionName,Value=$FUNCTION_NAME \
    --statistics Sum \
    --start-time $(date -u -d '1 minute ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period 60 \
    --query 'Datapoints[0].Sum' --output text)

  echo "  Invocations: ${INVOCATIONS:-0}"
  echo "  Errors: ${ERRORS:-0}"

  # Alert if error rate > 5%
  if [ "${ERRORS:-0}" != "None" ] && [ "${INVOCATIONS:-0}" != "None" ]; then
    if [ "$INVOCATIONS" -gt 0 ]; then
      ERROR_RATE=$(echo "scale=2; $ERRORS / $INVOCATIONS * 100" | bc)
      if (( $(echo "$ERROR_RATE > 5" | bc -l) )); then
        echo "  ⚠️  ERROR RATE: ${ERROR_RATE}% (threshold: 5%)"
      fi
    fi
  fi

  # Check recent logs
  RECENT_ERRORS=$(aws logs filter-log-events \
    --log-group-name /aws/lambda/$FUNCTION_NAME \
    --start-time $(($(date +%s) - 60))000 \
    --filter-pattern "ERROR" \
    --query 'length(events)' --output text)

  if [ "$RECENT_ERRORS" -gt 0 ]; then
    echo "  ⚠️  Found $RECENT_ERRORS errors in logs (last minute)"
    aws logs tail /aws/lambda/$FUNCTION_NAME --since 1m --filter-pattern "ERROR"
  fi

  sleep 60
done

echo ""
echo "✅ Monitoring complete"
```

---

## Quick Reference Commands

### AWS Waiters (NEVER use sleep)
```bash
# Lambda function updated
aws lambda wait function-updated --function-name worker

# CloudFront invalidation completed
aws cloudfront wait invalidation-completed --distribution-id E123 --id I456

# DynamoDB table exists
aws dynamodb wait table-exists --table-name jobs
```

### GitHub Actions Monitoring
```bash
# Watch with proper exit codes
gh run watch --exit-status

# Check status AND conclusion
gh run view 12345 --json status,conclusion --jq '{status, conclusion}'

# Get failed logs
gh run view 12345 --log-failed
```

### CloudWatch Logs
```bash
# Tail logs in real-time
aws logs tail /aws/lambda/worker --follow

# Filter for errors
aws logs tail /aws/lambda/worker --filter-pattern "ERROR" --since 5m

# Count errors in last hour
aws logs filter-log-events \
  --log-group-name /aws/lambda/worker \
  --start-time $(($(date +%s) - 3600))000 \
  --filter-pattern "ERROR" \
  --query 'length(events)' --output text
```

---

## Reference

**Complete guide**: [docs/deployment/MONITORING.md](../../../docs/deployment/MONITORING.md)

**Topics covered in complete guide:**
- AWS CLI waiters (Lambda, CloudFront, DynamoDB, API Gateway)
- GitHub Actions monitoring (`gh run watch --exit-status`)
- Lambda CloudWatch logs streaming and metrics
- DynamoDB job status monitoring
- Infrastructure-deployment contract validation (pre-deployment checks)
- Common monitoring mistakes and anti-patterns
- Complete monitoring checklist
