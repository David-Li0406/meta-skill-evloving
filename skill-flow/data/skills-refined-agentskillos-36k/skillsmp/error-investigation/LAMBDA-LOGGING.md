# Lambda Logging Diagnostic Workflow

**For complete reference**, see [docs/deployment/LAMBDA_LOGGING.md](../../../docs/deployment/LAMBDA_LOGGING.md)

---

## Quick Diagnostic Workflow

**When logs aren't appearing in CloudWatch:**

1. **Check root logger level**
   ```python
   print(f"Root logger level: {logging.getLevelName(logging.getLogger().level)}")
   ```

2. **Verify log group exists**
   ```bash
   aws logs describe-log-groups --log-group-name-prefix /aws/lambda/worker
   ```

3. **Test with print() as fallback**
   ```python
   print("PROOF OF LIFE")  # Always visible
   ```

4. **Check Lambda execution role permissions**
   ```bash
   aws iam simulate-principal-policy \
     --policy-source-arn $(aws lambda get-function-configuration --function-name worker --query 'Role' --output text) \
     --action-names logs:CreateLogStream logs:PutLogEvents
   ```

---

## Common Failure Patterns

### Pattern 1: INFO Logs Invisible
- **Symptom**: `logger.info()` messages don't appear
- **Root cause**: Root logger still at WARNING (default)
- **Quick fix**: Add `logging.getLogger().setLevel(logging.INFO)` at module level

### Pattern 2: Logs Not Appearing at All
- **Symptom**: No logs in CloudWatch, even ERROR level
- **Root cause**: Missing CloudWatch permissions or log group doesn't exist
- **Quick fix**: Check Lambda execution role has `logs:CreateLogStream` and `logs:PutLogEvents`

### Pattern 3: Duplicate Messages
- **Symptom**: Each log message appears twice
- **Root cause**: Multiple handlers attached to root logger
- **Quick fix**: Clear duplicate handlers before setting level

### Pattern 4: Using basicConfig() in Lambda
- **Symptom**: Configuration code runs but has no effect
- **Root cause**: Lambda already configured logging before your code runs
- **Quick fix**: Replace `logging.basicConfig()` with root logger pattern

---

## Smoke Test Commands

### Test Locally
```bash
# Run handler locally
python handler.py

# Expected: INFO messages appear in console
```

### Test in Lambda
```bash
# Invoke Lambda
aws lambda invoke --function-name worker --payload '{}' /tmp/response.json

# Check recent logs
aws logs tail /aws/lambda/worker --since 1m --follow

# Search for specific message
aws logs tail /aws/lambda/worker --filter-pattern "Handler started"
```

### Verify Log Level
```python
# Add to Lambda handler for debugging
import logging

root_logger = logging.getLogger()
print(f"🔍 Root level: {logging.getLevelName(root_logger.level)}")
print(f"🔍 Handlers: {root_logger.handlers}")

logger = logging.getLogger(__name__)
logger.info("TEST INFO")
logger.warning("TEST WARNING")
```

---

## Quick Fixes

### Fix 1: Set Root Logger Level (Most Common)

**Problem**: INFO logs invisible in CloudWatch

```python
# At top of Lambda handler module (BEFORE lambda_handler function)
import logging

root_logger = logging.getLogger()
if root_logger.handlers:  # Lambda environment
    root_logger.setLevel(logging.INFO)
else:  # Local development
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
```

### Fix 2: Add CloudWatch Permissions

**Problem**: No logs appearing at all

```bash
# Create IAM policy
cat > lambda-logging-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
EOF

# Attach to Lambda execution role
ROLE_NAME=$(aws lambda get-function-configuration --function-name worker --query 'Role' --output text | cut -d'/' -f2)
aws iam put-role-policy --role-name $ROLE_NAME --policy-name CloudWatchLogs --policy-document file://lambda-logging-policy.json
```

### Fix 3: Clear Duplicate Handlers

**Problem**: Each log message appears twice

```python
import logging

root_logger = logging.getLogger()

# Remove duplicates
if len(root_logger.handlers) > 1:
    root_logger.handlers = root_logger.handlers[:1]

root_logger.setLevel(logging.INFO)
```

---

## Reference

**Complete guide**: [docs/deployment/LAMBDA_LOGGING.md](../../../docs/deployment/LAMBDA_LOGGING.md)

**Topics covered in complete guide:**
- Why logging.basicConfig() doesn't work in Lambda
- Structured JSON logging for CloudWatch Insights
- Log levels strategy (INFO vs WARNING in production)
- CloudWatch configuration (retention, subscriptions)
- Comprehensive troubleshooting guide
- Migration checklist for existing Lambda handlers
