# CloudWatch Logs

## Quick Status Checks
```bash
# List available log groups
aws logs describe-log-groups --log-group-name-prefix LOG_GROUP_PREFIX

# Get log streams for a group
aws logs describe-log-streams --log-group-name LOG_GROUP_NAME --order-by LastEventTime --descending
```

## Log Access Methods

### Method 1: EB Log Retrieval (Temporary S3 URLs)
```bash
# Request logs
aws elasticbeanstalk request-environment-info --environment-id EB_ENVIRONMENT_ID --info-type tail

# Wait a few seconds, then retrieve log URLs
aws elasticbeanstalk retrieve-environment-info --environment-id EB_ENVIRONMENT_ID --info-type tail

# Download logs using curl (URLs expire quickly)
curl -s "S3_LOG_URL" | tail -100
```

### Method 2: CloudWatch Logs (More Reliable)
```bash
# List available log groups
aws logs describe-log-groups --log-group-name-prefix "/aws/elasticbeanstalk/EB_ENVIRONMENT_NAME"

# Get latest log stream name
aws logs describe-log-streams \
  --log-group-name "/aws/elasticbeanstalk/EB_ENVIRONMENT_NAME/var/log/web.stdout.log" \
  --order-by LastEventTime --descending --max-items 1 \
  --query 'logStreams[0].logStreamName' --output text

# Get recent log events
aws logs get-log-events \
  --log-group-name "/aws/elasticbeanstalk/EB_ENVIRONMENT_NAME/var/log/web.stdout.log" \
  --log-stream-name LOG_STREAM_NAME \
  --query 'events[-30:].message' --output text
```

## Key Log Groups for Node.js Apps
- `/aws/elasticbeanstalk/EB_ENVIRONMENT_NAME/var/log/web.stdout.log` - **Application stdout/stderr** (most important)
- `/aws/elasticbeanstalk/EB_ENVIRONMENT_NAME/var/log/nginx/error.log` - Nginx proxy errors
- `/aws/elasticbeanstalk/EB_ENVIRONMENT_NAME/var/log/eb-hooks.log` - Deployment hooks (prebuild, predeploy)
- `/aws/elasticbeanstalk/EB_ENVIRONMENT_NAME/var/log/eb-engine.log` - EB platform logs

## Time-based Log Filtering
```bash
# Get logs from last hour (timestamp in milliseconds)
aws logs get-log-events \
  --log-group-name LOG_GROUP_NAME \
  --log-stream-name LOG_STREAM_NAME \
  --start-time $(($(date +%s - 3600)*1000))
```

## JSON Parsing Examples
```bash
# Extract log messages with jq
aws logs get-log-events --log-group-name LOG_GROUP_NAME --log-stream-name LOG_STREAM_NAME --output json | jq '.events[].message'

# Query log stream names
aws logs describe-log-streams --log-group-name LOG_GROUP_NAME --query 'logStreams[*].logStreamName'
```
