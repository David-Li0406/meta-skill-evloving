# Elastic Beanstalk

## Quick Status Checks
```bash
# Check EB environment status (minimal output)
aws elasticbeanstalk describe-environments \
  --application-name APP_NAME \
  --environment-names ENV_NAME \
  --region REGION \
  --query 'Environments[0].[Status,Health,VersionLabel]' \
  --output text

# Check CloudFormation stack status (EB uses CloudFormation)
aws cloudformation describe-stacks \
  --stack-name STACK_NAME \
  --region REGION \
  --query 'Stacks[0].StackStatus' \
  --output text

# List stack resources
aws cloudformation list-stack-resources --stack-name STACK_NAME --region REGION
```

## Environment Status & Events
```bash
# Get environment details
aws elasticbeanstalk describe-environments --environment-ids EB_ENVIRONMENT_ID

# Get recent deployment events (most useful for failures)
aws elasticbeanstalk describe-events --environment-id EB_ENVIRONMENT_ID --max-records 15

# Get detailed health status
aws elasticbeanstalk describe-environment-health --environment-id EB_ENVIRONMENT_ID --attribute-names All

# Get instance-level health details
aws elasticbeanstalk describe-instances-health --environment-id EB_ENVIRONMENT_ID --attribute-names All
```

## Common Patterns

### 1. Deployment Failures
1. Check `describe-events` for high-level errors
2. Look at `eb-hooks.log` for build/deploy script failures  
3. Check `web.stdout.log` for application startup errors

### 2. Runtime 5xx Errors
1. Check environment health with `describe-environment-health`
2. Look at `web.stdout.log` for application crashes/exceptions
3. Check `nginx/error.log` for proxy issues

### 3. Instance Health Problems
1. Use `describe-instances-health` for per-instance details
2. Check system metrics (CPU, load) vs application metrics
3. Look for ELB health check failures

## Monitoring Deployment Progress
```bash
(for i in {1..20}; do
  echo "$(date +%H:%M:%S) #$i"
  eb_info=$(aws elasticbeanstalk describe-environments \
    --application-name APP_NAME \
    --environment-names ENV_NAME \
    --region REGION \
    --query 'Environments[0].[Status,Health,VersionLabel]' \
    --output text 2>/dev/null || echo "NOT_FOUND")
  cf_status=$(aws cloudformation describe-stacks \
    --stack-name STACK_NAME \
    --region REGION \
    --query 'Stacks[0].StackStatus' \
    --output text 2>/dev/null || echo "NOT_FOUND")
  echo "EB: $eb_info | CF: $cf_status"
  [[ "$eb_info" == *"Ready"* ]] && [[ "$cf_status" == *"COMPLETE"* ]] && break
  sleep 60
done) | tail -n 10
```

